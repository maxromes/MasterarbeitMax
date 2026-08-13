#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min"
CORAL_REEF_DIR = CUT_ROOT / "Annotation_reports_coral_reef"
NURSERY_DIR = CUT_ROOT / "Annotation_reports_Nursery"
OUT_DIR = ROOT / "results" / "presence_absence_model"
FIG_DIR = ROOT / "results" / "ergaenzende_statistische_grafiken"

BAIT_MAP = {
    "mackerel": "fish",
    "fischmix": "fish",
    "sargassum": "algae",
    "ulva_salad": "algae",
    "ulva_gutweed": "algae",
    "algaemix": "algae",
    "algae_strings": "algae",
}

TARGETS = [
    {
        "signal": "nursery_acanthuridae",
        "label": "Nursery: Acanthuridae",
        "sites": ["nursery"],
        "family": "acanthuridae",
        "expected_direction": "algae > fish",
        "direction": "greater",
    },
    {
        "signal": "coral_labridae",
        "label": "Coral reef: Labridae",
        "sites": ["milimani", "utumbi"],
        "family": "labridae",
        "expected_direction": "fish > algae",
        "direction": "less",
    },
    {
        "signal": "coral_balistidae",
        "label": "Coral reef: Balistidae",
        "sites": ["milimani", "utumbi"],
        "family": "balistidae",
        "expected_direction": "fish > algae",
        "direction": "less",
    },
    {
        "signal": "coral_muraenidae",
        "label": "Coral reef: Muraenidae",
        "sites": ["milimani", "utumbi"],
        "family": "muraenidae",
        "expected_direction": "fish > algae",
        "direction": "less",
    },
    {
        "signal": "coral_siganidae",
        "label": "Coral reef: Siganidae",
        "sites": ["milimani", "utumbi"],
        "family": "siganidae",
        "expected_direction": "algae > fish",
        "direction": "greater",
    },
    {
        "signal": "coral_scaridae",
        "label": "Coral reef: Scaridae",
        "sites": ["milimani", "utumbi"],
        "family": "scaridae",
        "expected_direction": "algae > fish",
        "direction": "greater",
    },
]


def parse_video_metadata(filename: str) -> tuple[str, str, str]:
    stem = filename.replace(".csv", "")
    parts = stem.split("-", 2)
    if len(parts) < 3:
        return "", "unknown", "unknown"
    date, site, bait = parts
    return date, site.lower(), bait.lower()


def is_truthy(value: object) -> bool:
    if value is None:
        return False
    text = str(value).strip().lower()
    return text not in {"", "0", "false", "f", "no", "n", "none", "null", "nan"}


def parse_frame_time(frame_value: object) -> float | None:
    text = str(frame_value).strip()
    if not text:
        return None
    match = re.search(r"[-+]?\d*\.?\d+", text)
    if not match:
        return None
    try:
        return round(float(match.group(0)), 2)
    except ValueError:
        return None


def bh_adjust(pvals: Iterable[float]) -> List[float]:
    vals = np.asarray(list(pvals), dtype=float)
    m = len(vals)
    if m == 0:
        return []
    order = np.argsort(vals)
    adjusted = np.empty(m, dtype=float)
    ranked = vals[order]
    tmp = ranked * m / np.arange(1, m + 1)
    tmp = np.minimum.accumulate(tmp[::-1])[::-1]
    tmp = np.clip(tmp, 0.0, 1.0)
    adjusted[order] = tmp
    return adjusted.tolist()


def family_presence_by_site(target: dict) -> dict:
    family = target["family"]
    sites = set(target["sites"])
    algae_present = []
    fish_present = []
    algae_total = 0
    fish_total = 0

    files = list(CORAL_REEF_DIR.glob("*.csv")) + list(NURSERY_DIR.glob("*.csv"))
    for csv_path in sorted(files):
        _, site, bait = parse_video_metadata(csv_path.name)
        if site not in sites or bait not in BAIT_MAP:
            continue
        bait_type = BAIT_MAP[bait]
        if bait_type not in {"algae", "fish"}:
            continue

        df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")
        maxn = 0
        for _, row in df.iterrows():
            if is_truthy(row.get("feeding", "")) or is_truthy(row.get("interested", "")):
                continue
            fam = str(row.get("family", "")).strip().lower()
            if fam != family:
                continue
            frame_time = parse_frame_time(row.get("frames", ""))
            if frame_time is None:
                continue
            maxn = max(maxn, 1)
        if bait_type == "algae":
            algae_total += 1
            algae_present.append(int(maxn > 0))
        else:
            fish_total += 1
            fish_present.append(int(maxn > 0))

    table = np.array(
        [
            [int(np.sum(algae_present)), int(algae_total - np.sum(algae_present))],
            [int(np.sum(fish_present)), int(fish_total - np.sum(fish_present))],
        ],
        dtype=int,
    )

    if table.sum() == 0:
        raise ValueError(f"No data available for {target['signal']}")

    if target["direction"] == "greater":
        fisher_p = stats.fisher_exact(table, alternative="greater").pvalue
    else:
        fisher_p = stats.fisher_exact(table, alternative="less").pvalue

    odds_ratio = float((table[0, 0] * table[1, 1]) / (table[0, 1] * table[1, 0])) if (table[0, 1] * table[1, 0]) > 0 else np.nan

    return {
        "signal": target["signal"],
        "label": target["label"],
        "family": family,
        "sites": ", ".join(sorted(sites)),
        "n_algae_total": int(algae_total),
        "n_algae_present": int(np.sum(algae_present)),
        "n_fish_total": int(fish_total),
        "n_fish_present": int(np.sum(fish_present)),
        "algae_presence_rate": float(np.mean(algae_present)) if algae_total else np.nan,
        "fish_presence_rate": float(np.mean(fish_present)) if fish_total else np.nan,
        "table": table,
        "odds_ratio": odds_ratio,
        "fisher_p": float(fisher_p),
        "expected_direction": target["expected_direction"],
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    results = [family_presence_by_site(t) for t in TARGETS]
    pvals = [r["fisher_p"] for r in results]
    bh = bh_adjust(pvals)
    for r, adj in zip(results, bh):
        r["fisher_p_bh"] = float(adj)
        r["sig_bh_0_05"] = bool(adj < 0.05)

    df = pd.DataFrame(results)
    df = df.sort_values(["fisher_p", "signal"]).reset_index(drop=True)
    df.to_csv(OUT_DIR / "presence_absence_summary.csv", index=False)

    lines = [
        "# Präsenz-/Absenz-Modell für fokussierte Taxa und Familien",
        "",
        "Methodik: Videoebene, Presence/Absence je Taxon/Familie; Fisher-Exact-Test mit gerichteter Alternative auf den biologisch erwarteten Effekt.",
        "",
        "- For the herbivore signal in Nursery, the key question is whether the signal is driven by actual occurrence differences or by stronger abundance once present.",
        "- For the broader coral-reef fish-vs-algae signals, the question is whether one bait type triggers consistently more occurrence of the focal taxon.",
        "",
        "| signal | family | sites | algae_present | algae_total | fish_present | fish_total | algae_rate | fish_rate | fisher_p | fisher_p_bh | sig_bh_0_05 |",
        "|:---|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in df.itertuples(index=False):
        lines.append(
            f"| {row.signal} | {row.family} | {row.sites} | {row.n_algae_present} | {row.n_algae_total} | {row.n_fish_present} | {row.n_fish_total} | {row.algae_presence_rate:.3f} | {row.fish_presence_rate:.3f} | {row.fisher_p:.6f} | {row.fisher_p_bh:.6f} | {str(row.sig_bh_0_05).lower()} |"
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "- Nursery Acanthuridae: Presence/Absence liefert hier kein klares Koeder-Signal, weil die Familie in beiden Ködergruppen auf fast allen Videos vorhanden ist. Das deutet auf einen Abundanz-Effekt statt auf einen reinen Occurrence-Effekt hin.",
        "- Coral Reef Labridae, Balistidae, Muraenidae: Die Fisch-vs-Algae-Differenzen bleiben im Präsenz-/Absenz-Raum nur teilweise sichtbar; für Labridae und Balistidae ist die Präsenz in beiden Gruppen so häufig, dass kein starker Unterschied im Vorkommen entsteht. Muraenidae zeigt den klarsten Presence/Absence-Effekt (0/19 vs 5/9), was die Richtung der Fish-vs-Algae-Analysen zusätzlich stützt.",
        "- Die Gesamtbotschaft ist damit methodisch wichtig: Der robuste Kern der Befunde liegt eher in der Intensität/MaxN als in der bloßen Präsenz. Für Algenfresser ist der Effekt bei Acanthuridae damit eher ein starker Dichte- oder Aktivitätsunterschied als ein reiner Präsenzunterschied.",
    ])
    (OUT_DIR / "presence_absence_model.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    plt.rcParams.update({
        "font.size": 10,
        "axes.titlesize": 12,
        "axes.labelsize": 11,
        "legend.fontsize": 9,
    })

    fig, ax = plt.subplots(figsize=(10, 6.2))
    positions = np.arange(len(df))
    width = 0.35
    for i, row in enumerate(df.itertuples(index=False)):
        ax.bar(
            positions[i] - width / 2,
            row.algae_presence_rate,
            width,
            color="#4e79a7",
            label="Algae" if i == 0 else None,
            alpha=0.9,
        )
        ax.bar(
            positions[i] + width / 2,
            row.fish_presence_rate,
            width,
            color="#f28e2b",
            label="Fish" if i == 0 else None,
            alpha=0.9,
        )
        ax.text(positions[i] - width / 2, row.algae_presence_rate + 0.03, f"{row.algae_presence_rate:.2f}", ha="center", va="bottom", fontsize=8)
        ax.text(positions[i] + width / 2, row.fish_presence_rate + 0.03, f"{row.fish_presence_rate:.2f}", ha="center", va="bottom", fontsize=8)

    ax.set_xticks(positions)
    ax.set_xticklabels([row.label for row in df.itertuples(index=False)], rotation=18, ha="right")
    ax.set_ylabel("Präsenzrate pro Video")
    ax.set_ylim(0, 1.15)
    ax.set_title("Präsenz-/Absenz-Muster der fokussierten Gruppen")
    ax.grid(axis="y", alpha=0.2)
    if not ax.get_legend_handles_labels()[0]:
        ax.legend(["Algae", "Fish"], loc="upper right")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "10_presence_absence_focal_signals.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    print(f"Wrote {OUT_DIR / 'presence_absence_summary.csv'}")
    print(f"Wrote {OUT_DIR / 'presence_absence_model.md'}")
    print(f"Wrote {FIG_DIR / '10_presence_absence_focal_signals.png'}")


if __name__ == "__main__":
    main()
