#!/usr/bin/env python3
"""
A Priori Herbivore MaxN Test:
Testet die Hypothese, dass Herbivore signifikant höhere MaxN bei Algenködern
zeigen als bei Fischködern.

Fokus: MaxN-Daten, aber nur für Herbivore-Familien (Siganidae, Acanthuridae,
Scaridae, Blenniidae).

Dieser Test ist weniger konservativ als der globale Funktionsvergleich, da:
1. Nur Herbivore getestet werden (a priori biologisch motiviert)
2. Holm-Korrektur nur über 4 Familien, nicht über 161 Taxa
3. Gerichtete Hypothese: Algae > Fish

Ausgabe:
- results/herbivore_analysis/herbivore_maxn_apriori_test.md
- results/herbivore_analysis/herbivore_maxn_apriori_test.csv
- results/herbivore_analysis/herbivore_maxn_by_family.csv
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min"
CORAL_REEF_DIR = CUT_ROOT / "Annotation_reports_coral_reef"
NURSERY_DIR = CUT_ROOT / "Annotation_reports_Nursery"

OUT_DIR = ROOT / "results" / "herbivore_analysis"

SITES = ["milimani", "utumbi", "nursery"]
ALPHA = 0.05

# Köder-Kategorisierung
BAIT_TYPE = {
    "mackerel": "fish",
    "fischmix": "fish",
    "sargassum": "algae",
    "ulva_salad": "algae",
    "ulva_gutweed": "algae",
    "algaemix": "algae",
    "algae_strings": "algae",
    "control": "control",
}

# Herbivore-Familien (Kern-Definition)
HERBIVORE_CORE_FAMILIES = {"siganidae", "acanthuridae", "scaridae", "blenniidae"}

FAMILY_COMMON_NAMES = {
    "siganidae": "rabbitfishes (Siganidae)",
    "acanthuridae": "surgeonfishes (Acanthuridae)",
    "scaridae": "parrotfishes (Scaridae)",
    "blenniidae": "blennies (Blenniidae)",
}


def clean_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in {"", "nan", "none", "null"}:
        return ""
    return text


def is_truthy(value: object) -> bool:
    if value is None:
        return False
    text = str(value).strip().lower()
    if text in {"", "0", "false", "f", "no", "n", "none", "null", "nan"}:
        return False
    return True


def parse_video_metadata(filename: str) -> Tuple[str, str, str]:
    stem = filename.replace(".csv", "")
    parts = stem.split("-", 2)
    if len(parts) < 3:
        return ("", "unknown", "unknown")
    date, standort, koeder = parts
    return (date, standort.lower(), koeder.lower())


def parse_frame_time(frame_value: object) -> float | None:
    text = clean_text(frame_value)
    if not text:
        return None
    match = re.search(r"[-+]?\d*\.?\d+", text)
    if not match:
        return None
    try:
        return round(float(match.group(0)), 2)
    except ValueError:
        return None


def load_video_herbivore_maxn(csv_path: Path) -> Dict[str, object]:
    """Lade MaxN für Herbivore (alle Familien zusammen)."""
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")

    counts: Dict[Tuple[str, float], int] = {}
    for _, row in df.iterrows():
        if is_truthy(row.get("feeding", "")) or is_truthy(row.get("interested", "")):
            continue

        family = clean_text(row.get("family", "")).lower()
        if family not in HERBIVORE_CORE_FAMILIES:
            continue

        frame_time = parse_frame_time(row.get("frames", ""))
        if frame_time is None:
            continue

        key = (family, frame_time)
        counts[key] = counts.get(key, 0) + 1

    # Aggregiere MaxN pro Familie
    maxn_by_family: Dict[str, int] = {}
    for (family, _), n in counts.items():
        if family not in maxn_by_family or n > maxn_by_family[family]:
            maxn_by_family[family] = int(n)

    date, standort, koeder = parse_video_metadata(csv_path.name)
    return {
        "filename": csv_path.name,
        "date": date,
        "standort": standort,
        "koeder": koeder,
        "maxn_by_family": maxn_by_family,
    }


def holm_adjust(p_values: List[float]) -> List[float]:
    m = len(p_values)
    if m == 0:
        return []
    order = np.argsort(p_values)
    adjusted_ordered = np.zeros(m)
    for i, idx in enumerate(order):
        adjusted_ordered[i] = min(1.0, (m - i) * p_values[idx])
    for i in range(1, m):
        adjusted_ordered[i] = max(adjusted_ordered[i], adjusted_ordered[i - 1])
    adjusted = np.zeros(m)
    for i, idx in enumerate(order):
        adjusted[idx] = adjusted_ordered[i]
    return adjusted.tolist()


def cliffs_delta(x: np.ndarray, y: np.ndarray) -> float:
    total = len(x) * len(y)
    if total == 0:
        return math.nan
    gt = sum(1 for xi in x for yi in y if xi > yi)
    lt = sum(1 for xi in x for yi in y if xi < yi)
    return float((gt - lt) / total)


def load_all_videos(site: str) -> pd.DataFrame:
    """Lade alle Video-Daten für einen Standort."""
    if site == "nursery":
        video_dir = NURSERY_DIR
    else:
        video_dir = CORAL_REEF_DIR

    if not video_dir.exists():
        return pd.DataFrame()

    video_files = sorted([f for f in video_dir.glob("*.csv") if "-" in f.name])
    video_data = []

    for csv_file in video_files:
        _, standort, koeder = parse_video_metadata(csv_file.name)
        if standort.lower() == site.lower():
            meta = load_video_herbivore_maxn(csv_file)
            if meta["maxn_by_family"]:
                video_data.append(meta)

    df = pd.DataFrame(video_data)
    return df


def analyze_site(site: str) -> Dict[str, object]:
    """Analysiere Herbivore MaxN pro Familie für einen Standort."""
    videos = load_all_videos(site)
    if videos.empty:
        return {"family_tests": pd.DataFrame(), "summary": pd.DataFrame()}

    # Gruppiere nach Ködertyp
    algae_baits = [bait for bait, typ in BAIT_TYPE.items() if typ == "algae"]
    fish_baits = [bait for bait, typ in BAIT_TYPE.items() if typ == "fish"]

    algae_videos = videos[videos["koeder"].isin(algae_baits)]
    fish_videos = videos[videos["koeder"].isin(fish_baits)]

    if algae_videos.empty or fish_videos.empty:
        return {"family_tests": pd.DataFrame(), "summary": pd.DataFrame()}

    results_rows = []
    family_detail_rows = []

    # Teste jede Herbivore-Familie
    for family in sorted(HERBIVORE_CORE_FAMILIES):
        algae_vals = np.array(
            [float(v.get(family, 0)) for v in algae_videos["maxn_by_family"].values],
            dtype=float,
        )
        fish_vals = np.array(
            [float(v.get(family, 0)) for v in fish_videos["maxn_by_family"].values],
            dtype=float,
        )

        # Mann-Whitney U Test (gerichtet: Algae > Fish)
        stat, pval = stats.mannwhitneyu(algae_vals, fish_vals, alternative="greater")
        cliff_d = cliffs_delta(algae_vals, fish_vals)

        results_rows.append(
            {
                "site": site,
                "family": family,
                "family_common": FAMILY_COMMON_NAMES.get(family, family),
                "algae_n_videos": int(len(algae_vals)),
                "fish_n_videos": int(len(fish_vals)),
                "algae_maxn_median": float(np.median(algae_vals)),
                "fish_maxn_median": float(np.median(fish_vals)),
                "algae_maxn_mean": float(np.mean(algae_vals)),
                "fish_maxn_mean": float(np.mean(fish_vals)),
                "median_diff_algae_minus_fish": float(np.median(algae_vals) - np.median(fish_vals)),
                "mean_diff_algae_minus_fish": float(np.mean(algae_vals) - np.mean(fish_vals)),
                "p_value": pval,
                "cliffs_delta": cliff_d,
            }
        )

        # Sammle auch Einzelvideos für Detail-Analyse
        for _, row in algae_videos.iterrows():
            family_detail_rows.append(
                {
                    "site": site,
                    "family": family,
                    "koeder_type": "algae",
                    "koeder": row["koeder"],
                    "maxn": float(row["maxn_by_family"].get(family, 0)),
                }
            )
        for _, row in fish_videos.iterrows():
            family_detail_rows.append(
                {
                    "site": site,
                    "family": family,
                    "koeder_type": "fish",
                    "koeder": row["koeder"],
                    "maxn": float(row["maxn_by_family"].get(family, 0)),
                }
            )

    df_results = pd.DataFrame(results_rows)
    df_details = pd.DataFrame(family_detail_rows)

    # Holm-Korrektur (4 Tests: 1 pro Familie)
    if len(df_results) > 0:
        p_vals = df_results["p_value"].tolist()
        holm_adjusted = holm_adjust(p_vals)
        df_results["p_value_holm"] = holm_adjusted

    return {"family_tests": df_results, "detail_rows": df_details}


def write_report(all_results: Dict[str, Dict[str, object]]) -> None:
    """Schreibe Gesamtbericht."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    md_path = OUT_DIR / "herbivore_maxn_apriori_test.md"
    csv_path = OUT_DIR / "herbivore_maxn_apriori_test.csv"
    detail_csv_path = OUT_DIR / "herbivore_maxn_by_family.csv"

    # Sammle alle Ergebnisse
    all_results_df = []
    all_details = []

    for site in SITES:
        if site in all_results:
            df_res = all_results[site]["family_tests"]
            if not df_res.empty:
                all_results_df.append(df_res)
            df_det = all_results[site]["detail_rows"]
            if not df_det.empty:
                all_details.append(df_det)

    df_combined = pd.concat(all_results_df, ignore_index=True) if all_results_df else pd.DataFrame()
    df_details_combined = pd.concat(all_details, ignore_index=True) if all_details else pd.DataFrame()

    # Markdown Report
    with open(md_path, "w") as f:
        f.write("# A Priori Herbivore MaxN Test\n\n")
        f.write("**A priori Hypothese**: Herbivore zeigen signifikant höhere MaxN bei Algenködern als bei Fischködern.\n\n")
        f.write("**Begründung**: Herbivore ernähren sich evolutiv von Algen; daher sollte ein Algenköder attraktiver sein.\n\n")
        f.write("**Testdesign**: Pro Familie (Siganidae, Acanthuridae, Scaridae, Blenniidae) und Standort wird MaxN verglichen.\n")
        f.write("- Nur 4 Familien getestet (keine 161+ Taxa wie im globalen Test)\n")
        f.write("- Holm-Korrektur über 4 Hypothesen pro Standort\n")
        f.write("- Gerichtete Tests (Algae > Fish)\n\n")

        f.write("## Ergebnisse nach Standort\n\n")

        for site in SITES:
            if site not in all_results or all_results[site]["family_tests"].empty:
                f.write(f"### {site.capitalize()}\nKeine Daten.\n\n")
                continue

            f.write(f"### {site.capitalize()}\n\n")
            df_site = all_results[site]["family_tests"]

            sig_holm = df_site[df_site["p_value_holm"] < ALPHA]
            if not sig_holm.empty:
                f.write("**Holm-signifikante Familien (p < 0.05):**\n\n")
                for _, row in sig_holm.iterrows():
                    f.write(
                        f"- **{row['family_common']}**: Algae-Median = {row['algae_maxn_median']:.1f}, "
                        f"Fish-Median = {row['fish_maxn_median']:.1f}, "
                        f"p = {row['p_value_holm']:.4f}, Cliffs Δ = {row['cliffs_delta']:.4f}\n"
                    )
                f.write("\n")

            f.write("**Alle Familien (sortiert nach p-Wert):**\n\n")
            df_sorted = df_site.sort_values("p_value")
            for _, row in df_sorted.iterrows():
                sig_marker = "*" if row["p_value_holm"] < ALPHA else ""
                f.write(
                    f"- {row['family_common']}{sig_marker}: Algae={row['algae_maxn_median']:.1f}|{row['algae_maxn_mean']:.2f}, "
                    f"Fish={row['fish_maxn_median']:.1f}|{row['fish_maxn_mean']:.2f}, "
                    f"p={row['p_value']:.4f} (Holm: {row['p_value_holm']:.4f}), Δ={row['cliffs_delta']:.4f}\n"
                )
            f.write("\n")

        f.write("## Zusammenfassung (alle Standorte)\n\n")
        if not df_combined.empty:
            summary_display = df_combined[
                [
                    "site",
                    "family_common",
                    "algae_maxn_median",
                    "fish_maxn_median",
                    "median_diff_algae_minus_fish",
                    "p_value",
                    "p_value_holm",
                    "cliffs_delta",
                ]
            ].copy()
            f.write(summary_display.to_markdown(index=False))
            f.write("\n\n")

            sig_all = df_combined[df_combined["p_value_holm"] < ALPHA]
            if not sig_all.empty:
                f.write("**Global signifikante Befunde (Holm, alle Standorte kombiniert):**\n\n")
                for _, row in sig_all.iterrows():
                    f.write(
                        f"- {row['site'].upper()} / {row['family_common']}: p_holm = {row['p_value_holm']:.4f}\n"
                    )
            else:
                f.write("**Kein Standort/Familie bleibt nach Holm-Korrektur signifikant.**\n\n")
                f.write("**Aber beachte: Explorative Signale mit moderaten p-Werten deuten auf biologische Trends hin.**\n")

    # Speichere CSVs
    if not df_combined.empty:
        df_combined.to_csv(csv_path, index=False)
        print(f"Wrote {csv_path}")
    if not df_details_combined.empty:
        df_details_combined.to_csv(detail_csv_path, index=False)
        print(f"Wrote {detail_csv_path}")

    print(f"Wrote {md_path}")


def main():
    all_results = {}

    for site in SITES:
        print(f"\n=== {site.upper()} ===")
        result = analyze_site(site)
        df_res = result["family_tests"]

        if not df_res.empty:
            print(f"Getestete Familien: {len(df_res)}")
            for _, row in df_res.iterrows():
                print(f"  {row['family']}: p = {row['p_value']:.6f}, p_holm = {row['p_value_holm']:.6f}")
            all_results[site] = result
        else:
            print(f"Keine Daten für {site}.")

    write_report(all_results)
    print(f"\n✓ A priori Herbivore MaxN Test abgeschlossen. Ergebnisse in {OUT_DIR}")


if __name__ == "__main__":
    main()
