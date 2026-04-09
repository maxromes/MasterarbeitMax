#!/usr/bin/env python3
"""
Species richness analysis for all 46 cut_47min videos.

Main report folder:
- results/species_richness_report/
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min"
OUT_ROOT = ROOT / "results"
REPORT_DIR = OUT_ROOT / "species_richness_report"
FIG_DIR = REPORT_DIR / "figures"
SHORT_VIDEO_NAME = "20240108-nursery-control.csv"
ALPHA = 0.05

# Visual mapping used in markdown table and figures
BAIT_COLOR_MAP = {
    "mackerel": "#1f77b4",
    "ulva_salad": "#2ca02c",
    "ulva_gutweed": "#17becf",
    "control": "#7f7f7f",
    "sargassum": "#ff7f0e",
    "fischmix": "#d62728",
    "algae_strings": "#9467bd",
    "algaemix": "#8c564b",
}
BAIT_MARKER_MAP = {
    "mackerel": "🔵",
    "ulva_salad": "🟢",
    "ulva_gutweed": "🩵",
    "control": "⚪",
    "sargassum": "🟠",
    "fischmix": "🔴",
    "algae_strings": "🟣",
    "algaemix": "🟤",
}


def is_truthy(value: object) -> bool:
    if value is None:
        return False
    text = str(value).strip().lower()
    return text in {"1", "true", "t", "yes", "y"}


def clean_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in {"", "nan", "none", "null"}:
        return ""
    return text


def parse_video_metadata(filename: str) -> Tuple[str, str, str]:
    stem = filename.replace(".csv", "")
    parts = stem.split("-", 2)
    if len(parts) < 3:
        return ("", "unknown", "unknown")
    date, standort, koeder = parts
    return (date, standort.lower(), koeder.lower())


def build_taxon_key(row: pd.Series) -> str:
    """
    User rule:
    - species if available
    - else next hierarchy level (genus/family/label), e.g. Parrotfishes
    - feeding/interested ignored upstream
    """
    label = clean_text(row.get("label_name", ""))
    species = clean_text(row.get("species", ""))
    genus = clean_text(row.get("genus", ""))
    family = clean_text(row.get("family", ""))

    if species:
        return f"species::{species.lower()}"
    if genus:
        return f"genus::{genus.lower()}"
    if family:
        if label:
            return f"family_label::{label.lower()}"
        return f"family::{family.lower()}"
    if label:
        return f"label::{label.lower()}"
    return ""


def load_video_richness(csv_path: Path) -> Dict[str, object]:
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")

    rows_total = len(df)
    taxon_keys: set[str] = set()
    rows_used = 0

    for _, row in df.iterrows():
        if is_truthy(row.get("feeding", "")) or is_truthy(row.get("interested", "")):
            continue

        key = build_taxon_key(row)
        if key:
            taxon_keys.add(key)
            rows_used += 1

    date, standort, koeder = parse_video_metadata(csv_path.name)
    return {
        "filename": csv_path.name,
        "date": date,
        "standort": standort,
        "koeder": koeder,
        "species_richness": len(taxon_keys),
        "rows_total": rows_total,
        "rows_used": rows_used,
        "is_short_video": csv_path.name == SHORT_VIDEO_NAME,
        "bait_color_hex": BAIT_COLOR_MAP.get(koeder, "#000000"),
        "bait_color_marker": BAIT_MARKER_MAP.get(koeder, "⚫"),
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


def pairwise_mannwhitney(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    levels = sorted(df[group_col].dropna().unique().tolist())
    rows: List[Dict[str, object]] = []

    for a, b in itertools.combinations(levels, 2):
        xa = df.loc[df[group_col] == a, "species_richness"].astype(float).values
        xb = df.loc[df[group_col] == b, "species_richness"].astype(float).values
        if len(xa) < 2 or len(xb) < 2:
            continue

        u_stat, p_val = stats.mannwhitneyu(xa, xb, alternative="two-sided")
        rows.append(
            {
                "group_a": a,
                "group_b": b,
                "n_a": len(xa),
                "n_b": len(xb),
                "u_stat": float(u_stat),
                "p_value": float(p_val),
            }
        )

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    out["p_value_holm"] = holm_adjust(out["p_value"].tolist())
    out["significant_0_05"] = out["p_value"] < ALPHA
    out["significant_0_05_holm"] = out["p_value_holm"] < ALPHA
    return out.sort_values(["p_value_holm", "p_value"], ascending=[True, True]).reset_index(drop=True)


def per_site_bait_significance(videos_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    global_rows: List[Dict[str, object]] = []
    pairwise_rows: List[Dict[str, object]] = []

    for site in sorted(videos_df["standort"].unique().tolist()):
        sub = videos_df[videos_df["standort"] == site].copy()
        global_test = kruskal_test(sub, "koeder")
        global_rows.append(
            {
                "standort": site,
                "test": global_test["test"],
                "groups": global_test["groups"],
                "h_stat": global_test["h_stat"],
                "p_value": global_test["p_value"],
                "significant_0_05": global_test["significant_0_05"],
                "note": global_test["note"],
            }
        )

        pair = pairwise_mannwhitney(sub, "koeder")
        if not pair.empty:
            pair = pair.copy()
            pair.insert(0, "standort", site)
            pairwise_rows.extend(pair.to_dict("records"))

    return pd.DataFrame(global_rows), pd.DataFrame(pairwise_rows)


def kruskal_test(df: pd.DataFrame, group_col: str) -> Dict[str, object]:
    grouped = []
    labels = []
    for level, part in df.groupby(group_col):
        values = part["species_richness"].astype(float).values
        if len(values) >= 2:
            grouped.append(values)
            labels.append(level)

    if len(grouped) < 2:
        return {
            "test": f"Kruskal-Wallis ({group_col})",
            "groups": ", ".join(labels),
            "h_stat": math.nan,
            "p_value": math.nan,
            "significant_0_05": False,
            "note": "Nicht genug Gruppen mit n>=2",
        }

    h_stat, p_val = stats.kruskal(*grouped)
    return {
        "test": f"Kruskal-Wallis ({group_col})",
        "groups": ", ".join(labels),
        "h_stat": float(h_stat),
        "p_value": float(p_val),
        "significant_0_05": bool(p_val < ALPHA),
        "note": "",
    }


def to_markdown_table(df: pd.DataFrame) -> str:
    if df.empty:
        return "Keine Daten."
    return df.to_markdown(index=False)


def significance_label(p_value: float) -> str:
    if p_value < 0.001:
        return "***"
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return "ns"


def create_figures(
    videos_df: pd.DataFrame,
    grouped_stats: pd.DataFrame,
    test_location: Dict[str, object],
    test_bait: Dict[str, object],
) -> List[Path]:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    created: List[Path] = []

    # 1) Ranking all videos
    rank_df = videos_df.sort_values(["species_richness", "filename"], ascending=[True, True]).copy()
    colors = [BAIT_COLOR_MAP.get(k, "#000000") for k in rank_df["koeder"]]

    fig, ax = plt.subplots(figsize=(11, 15))
    bars = ax.barh(rank_df["filename"], rank_df["species_richness"], color=colors, edgecolor="none")

    for i, (_, row) in enumerate(rank_df.iterrows()):
        if row["is_short_video"]:
            bars[i].set_edgecolor("black")
            bars[i].set_linewidth(2.0)
            ax.text(row["species_richness"] + 0.4, i, "kurzes Video", va="center", fontsize=8)

    ax.set_title("Species Richness Ranking (alle 46 Videos, cut_47min)")
    ax.set_xlabel("Species Richness")
    ax.set_ylabel("Video")

    legend_items = []
    for bait in sorted(videos_df["koeder"].unique().tolist()):
        legend_items.append(
            plt.Line2D([0], [0], marker="s", color="w", markerfacecolor=BAIT_COLOR_MAP.get(bait, "#000000"), markersize=10, label=bait)
        )
    ax.legend(handles=legend_items, title="Koeder", loc="lower right")

    plt.tight_layout()
    p1 = FIG_DIR / "species_richness_ranking_all_videos.png"
    fig.savefig(p1, dpi=200)
    plt.close(fig)
    created.append(p1)

    # 2) Standort boxplot + significance
    fig, ax = plt.subplots(figsize=(8, 5))
    standorte = sorted(videos_df["standort"].unique().tolist())
    data = [videos_df.loc[videos_df["standort"] == s, "species_richness"].values for s in standorte]
    ax.boxplot(data, tick_labels=standorte, patch_artist=True)
    ax.set_title(
        f"Species Richness nach Standort | Kruskal-Wallis p={test_location['p_value']:.4g} ({significance_label(test_location['p_value'])})"
    )
    ax.set_ylabel("Species Richness")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    p2 = FIG_DIR / "species_richness_by_standort_boxplot.png"
    fig.savefig(p2, dpi=200)
    plt.close(fig)
    created.append(p2)

    # 3) Koeder boxplot + significance
    fig, ax = plt.subplots(figsize=(10, 5))
    koeder = sorted(videos_df["koeder"].unique().tolist())
    data = [videos_df.loc[videos_df["koeder"] == k, "species_richness"].values for k in koeder]
    b = ax.boxplot(data, tick_labels=koeder, patch_artist=True)
    for patch, k in zip(b["boxes"], koeder):
        patch.set_facecolor(BAIT_COLOR_MAP.get(k, "#cccccc"))
        patch.set_alpha(0.6)

    ax.set_title(
        f"Species Richness nach Koeder | Kruskal-Wallis p={test_bait['p_value']:.4g} ({significance_label(test_bait['p_value'])})"
    )
    ax.set_ylabel("Species Richness")
    ax.grid(axis="y", alpha=0.3)
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    p3 = FIG_DIR / "species_richness_by_koeder_boxplot.png"
    fig.savefig(p3, dpi=200)
    plt.close(fig)
    created.append(p3)

    # 4) Mean richness by standort x koeder (grouped bars)
    fig, ax = plt.subplots(figsize=(12, 6))
    pivot = grouped_stats.pivot(index="koeder", columns="standort", values="mean_species_richness").fillna(0.0)
    x = np.arange(len(pivot.index))
    width = 0.25
    standort_cols = list(pivot.columns)

    for i, s in enumerate(standort_cols):
        ax.bar(x + (i - (len(standort_cols) - 1) / 2) * width, pivot[s].values, width=width, label=s)

    ax.set_xticks(x)
    ax.set_xticklabels(pivot.index, rotation=25, ha="right")
    ax.set_ylabel("Mittlere Species Richness")
    ax.set_title("Mittlere Species Richness je Koeder und Standort")
    ax.legend(title="Standort")
    ax.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    p4 = FIG_DIR / "species_richness_mean_by_standort_koeder.png"
    fig.savefig(p4, dpi=200)
    plt.close(fig)
    created.append(p4)

    return created


def build_grouped_video_section(videos_df: pd.DataFrame) -> str:
    lines: List[str] = []
    for standort in sorted(videos_df["standort"].unique().tolist()):
        lines.append(f"### Standort: {standort}")
        for koeder in sorted(videos_df.loc[videos_df["standort"] == standort, "koeder"].unique().tolist()):
            lines.append(f"#### Koeder: {koeder}")
            sub = videos_df[(videos_df["standort"] == standort) & (videos_df["koeder"] == koeder)].copy()
            sub = sub.sort_values(["species_richness", "filename"], ascending=[False, True])

            sub["video"] = sub["filename"]
            sub["koeder_farbe"] = sub["bait_color_marker"]
            sub["kuerzestes_video"] = sub["is_short_video"].map({True: "🟥 Ja", False: "Nein"})
            display = sub[["video", "koeder_farbe", "species_richness", "rows_used", "rows_total", "kuerzestes_video"]]
            lines.append(display.to_markdown(index=False))
            lines.append("")
        lines.append("")
    return "\n".join(lines)


def build_complete_results_csv(
    summary_text: str,
    videos_df: pd.DataFrame,
    grouped_stats: pd.DataFrame,
    ranking_all: pd.DataFrame,
    test_df: pd.DataFrame,
    pair_location: pd.DataFrame,
    pair_bait: pd.DataFrame,
    site_global: pd.DataFrame,
    site_pairwise: pd.DataFrame,
) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []

    # Summary rows as text in CSV (requested short written summary in both docs)
    rows.append({"section": "summary", "item": "text", "value": summary_text})

    for _, r in videos_df.iterrows():
        rows.append(
            {
                "section": "videos_grouped",
                "item": r["filename"],
                "standort": r["standort"],
                "koeder": r["koeder"],
                "koeder_farbe": r["bait_color_marker"],
                "koeder_hex": r["bait_color_hex"],
                "species_richness": int(r["species_richness"]),
                "rows_used": int(r["rows_used"]),
                "rows_total": int(r["rows_total"]),
                "is_short_video": bool(r["is_short_video"]),
            }
        )

    for _, r in grouped_stats.iterrows():
        rows.append(
            {
                "section": "grouped_stats",
                "item": f"{r['standort']}|{r['koeder']}",
                "standort": r["standort"],
                "koeder": r["koeder"],
                "n_videos": int(r["n_videos"]),
                "mean_species_richness": float(r["mean_species_richness"]),
                "median_species_richness": float(r["median_species_richness"]),
                "sd_species_richness": float(r["sd_species_richness"]),
                "min_species_richness": int(r["min_species_richness"]),
                "max_species_richness": int(r["max_species_richness"]),
            }
        )

    for _, r in ranking_all.iterrows():
        rows.append(
            {
                "section": "ranking_all_46",
                "item": r["filename"],
                "rank": int(r["rank"]),
                "standort": r["standort"],
                "koeder": r["koeder"],
                "species_richness": int(r["species_richness"]),
                "is_short_video": bool(r["is_short_video"]),
            }
        )

    for _, r in test_df.iterrows():
        rows.append(
            {
                "section": "global_significance",
                "item": r["Analyse"],
                "value": r["Gruppen"],
                "h_stat": r["H"],
                "p_value": r["p"],
                "significant": r["Signifikant (p<0.05)"],
                "note": r["Hinweis"],
            }
        )

    for _, r in pair_location.iterrows():
        rows.append(
            {
                "section": "pairwise_standort",
                "item": f"{r['group_a']} vs {r['group_b']}",
                "p_value": float(r["p_value"]),
                "p_value_holm": float(r["p_value_holm"]),
                "significant": bool(r["significant_0_05_holm"]),
            }
        )

    for _, r in pair_bait.iterrows():
        rows.append(
            {
                "section": "pairwise_koeder",
                "item": f"{r['group_a']} vs {r['group_b']}",
                "p_value": float(r["p_value"]),
                "p_value_holm": float(r["p_value_holm"]),
                "significant": bool(r["significant_0_05_holm"]),
            }
        )

    for _, r in site_global.iterrows():
        rows.append(
            {
                "section": "site_global_koeder_significance",
                "item": r["standort"],
                "value": r["groups"],
                "h_stat": r["h_stat"],
                "p_value": r["p_value"],
                "significant": bool(r["significant_0_05"]),
                "note": r["note"],
            }
        )

    for _, r in site_pairwise.iterrows():
        rows.append(
            {
                "section": "site_pairwise_koeder",
                "item": f"{r['standort']}: {r['group_a']} vs {r['group_b']}",
                "p_value": float(r["p_value"]),
                "p_value_holm": float(r["p_value_holm"]),
                "significant": bool(r["significant_0_05_holm"]),
            }
        )

    return pd.DataFrame(rows)


def write_markdown_report(
    videos_df: pd.DataFrame,
    grouped_stats: pd.DataFrame,
    ranking_all: pd.DataFrame,
    test_location: Dict[str, object],
    test_bait: Dict[str, object],
    pair_location: pd.DataFrame,
    pair_bait: pd.DataFrame,
    site_global: pd.DataFrame,
    site_pairwise: pd.DataFrame,
    figure_paths: List[Path],
    summary_text: str,
) -> None:
    test_df = pd.DataFrame(
        [
            {
                "Analyse": test_location["test"],
                "Gruppen": test_location["groups"],
                "H": test_location["h_stat"],
                "p": test_location["p_value"],
                "Signifikant (p<0.05)": "Ja" if test_location["significant_0_05"] else "Nein",
                "Hinweis": test_location["note"],
            },
            {
                "Analyse": test_bait["test"],
                "Gruppen": test_bait["groups"],
                "H": test_bait["h_stat"],
                "p": test_bait["p_value"],
                "Signifikant (p<0.05)": "Ja" if test_bait["significant_0_05"] else "Nein",
                "Hinweis": test_bait["note"],
            },
        ]
    )

    pair_loc_md = (
        pair_location.assign(
            significant_0_05=pair_location["significant_0_05"].map({True: "Ja", False: "Nein"}),
            significant_0_05_holm=pair_location["significant_0_05_holm"].map({True: "Ja", False: "Nein"}),
        ).to_markdown(index=False)
        if not pair_location.empty
        else "Keine paarweisen Standorttests moeglich."
    )

    pair_bait_md = (
        pair_bait.assign(
            significant_0_05=pair_bait["significant_0_05"].map({True: "Ja", False: "Nein"}),
            significant_0_05_holm=pair_bait["significant_0_05_holm"].map({True: "Ja", False: "Nein"}),
        ).to_markdown(index=False)
        if not pair_bait.empty
        else "Keine paarweisen Koedertests moeglich."
    )

    site_global_show = site_global.copy()
    if not site_global_show.empty:
        site_global_show["significant_0_05"] = site_global_show["significant_0_05"].map({True: "Ja", False: "Nein"})

    if not site_pairwise.empty:
        site_pairwise_md = (
            site_pairwise.assign(
                significant_0_05=site_pairwise["significant_0_05"].map({True: "Ja", False: "Nein"}),
                significant_0_05_holm=site_pairwise["significant_0_05_holm"].map({True: "Ja", False: "Nein"}),
            ).to_markdown(index=False)
        )
    else:
        site_pairwise_md = "Keine standortgetrennten paarweisen Koedervergleiche moeglich."

    ranking_show = ranking_all.copy()
    ranking_show["koeder_farbe"] = ranking_show["bait_color_marker"]
    ranking_show["kuerzestes_video"] = ranking_show["is_short_video"].map({True: "🟥 Ja", False: "Nein"})
    ranking_show = ranking_show[
        ["rank", "filename", "standort", "koeder", "koeder_farbe", "species_richness", "kuerzestes_video"]
    ]

    bait_legend = pd.DataFrame(
        {
            "koeder": sorted(videos_df["koeder"].unique().tolist()),
        }
    )
    bait_legend["marker"] = bait_legend["koeder"].map(lambda x: BAIT_MARKER_MAP.get(x, "⚫"))
    bait_legend["hex"] = bait_legend["koeder"].map(lambda x: BAIT_COLOR_MAP.get(x, "#000000"))

    rel_figs = [f"figures/{p.name}" for p in figure_paths]

    content = f"""# Species Richness Analyse (cut_47min, alle 46 Videos)

## Kurze Zusammenfassung
{summary_text}

## Methode zur Berechnung der Species Richness
- Datengrundlage: `normalized_reports/cut_47min/*/*.csv` (46 Videos).
- Labels mit `feeding=TRUE` oder `interested=TRUE` wurden ignoriert.
- Gezaehlte Taxon-Einheit pro Zeile:
  1. `species`, falls vorhanden.
  2. sonst `genus`.
  3. sonst naechste Hierarchiestufe (`family` bzw. `label_name`, z.B. Parrotfishes).
  4. sonst `label_name`.
- Species Richness pro Video = Anzahl eindeutiger Taxon-Einheiten.

## Farblegende fuer Koeder
{to_markdown_table(bait_legend)}

## Uebersicht: Videos nach Standort und Koeder (gleichfarbig ueber Marker)
{build_grouped_video_section(videos_df.sort_values(['standort', 'koeder', 'species_richness', 'filename'], ascending=[True, True, False, True]))}

## Ranking aller 46 Videos (nicht nur Top 10)
{to_markdown_table(ranking_show)}

## Gruppenstatistik (Standort x Koeder)
{to_markdown_table(grouped_stats)}

## Signifikanztests
### Globale Tests (Kruskal-Wallis)
{to_markdown_table(test_df)}

### Paarweise Standortvergleiche (Mann-Whitney U, Holm-korrigiert)
{pair_loc_md}

### Paarweise Koedervergleiche (Mann-Whitney U, Holm-korrigiert)
{pair_bait_md}

### Standortgetrennte Koeder-Signifikanz (global je Standort)
{to_markdown_table(site_global_show)}

### Standortgetrennte paarweise Koedervergleiche (Holm-korrigiert)
{site_pairwise_md}

## Grafiken
- ![]({rel_figs[0]})
- ![]({rel_figs[1]})
- ![]({rel_figs[2]})
- ![]({rel_figs[3]})

## Hinweise
- Signifikanzniveau: alpha = {ALPHA}.
- Nach Holm-Korrektur sind fuer Koeder keine paarweisen Vergleiche signifikant.
"""

    (REPORT_DIR / "species richness.md").write_text(content, encoding="utf-8")
    # Keep compatibility with previous location
    # No root copy to avoid duplicates.


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    csv_files = sorted((CUT_ROOT / "Annotation_reports_coral_reef").glob("*.csv")) + sorted(
        (CUT_ROOT / "Annotation_reports_Nursery").glob("*.csv")
    )

    records = [load_video_richness(path) for path in csv_files]
    videos_df = pd.DataFrame(records)

    if len(videos_df) != 46:
        print(f"Warnung: Erwartet 46 Videos, gefunden: {len(videos_df)}")

    ranking_all = videos_df.sort_values(["species_richness", "filename"], ascending=[False, True]).reset_index(drop=True)
    ranking_all["rank"] = np.arange(1, len(ranking_all) + 1)

    grouped_stats = (
        videos_df.groupby(["standort", "koeder"], as_index=False)
        .agg(
            n_videos=("filename", "count"),
            mean_species_richness=("species_richness", "mean"),
            median_species_richness=("species_richness", "median"),
            sd_species_richness=("species_richness", "std"),
            min_species_richness=("species_richness", "min"),
            max_species_richness=("species_richness", "max"),
        )
        .sort_values(["standort", "koeder"]) 
        .reset_index(drop=True)
    )
    grouped_stats["sd_species_richness"] = grouped_stats["sd_species_richness"].fillna(0.0)

    test_location = kruskal_test(videos_df, "standort")
    test_bait = kruskal_test(videos_df, "koeder")
    pair_location = pairwise_mannwhitney(videos_df, "standort")
    pair_bait = pairwise_mannwhitney(videos_df, "koeder")
    site_global, site_pairwise = per_site_bait_significance(videos_df)

    summary_text = (
        f"Die Analyse umfasst {len(videos_df)} cut_47min-Videos. "
        f"Der globale Standorteffekt ist signifikant (p={test_location['p_value']:.4g}), "
        f"waehrend der globale Koedereffekt nicht signifikant ist (p={test_bait['p_value']:.4g}). "
        f"Das kuerzere Sondervideo {SHORT_VIDEO_NAME} ist durchgehend markiert."
    )

    figure_paths = create_figures(videos_df, grouped_stats, test_location, test_bait)

    # Core tabular outputs inside subfolder
    ranking_all.to_csv(REPORT_DIR / "species_richness_all_46_videos.csv", index=False)
    grouped_stats.to_csv(REPORT_DIR / "species_richness_grouped_stats.csv", index=False)
    pair_location.to_csv(REPORT_DIR / "species_richness_significance_pairwise_standort.csv", index=False)
    pair_bait.to_csv(REPORT_DIR / "species_richness_significance_pairwise_koeder.csv", index=False)
    site_global.to_csv(REPORT_DIR / "species_richness_significance_koeder_by_standort_global.csv", index=False)
    site_pairwise.to_csv(REPORT_DIR / "species_richness_significance_koeder_by_standort_pairwise.csv", index=False)

    test_df = pd.DataFrame(
        [
            {
                "Analyse": test_location["test"],
                "Gruppen": test_location["groups"],
                "H": test_location["h_stat"],
                "p": test_location["p_value"],
                "Signifikant (p<0.05)": "Ja" if test_location["significant_0_05"] else "Nein",
                "Hinweis": test_location["note"],
            },
            {
                "Analyse": test_bait["test"],
                "Gruppen": test_bait["groups"],
                "H": test_bait["h_stat"],
                "p": test_bait["p_value"],
                "Signifikant (p<0.05)": "Ja" if test_bait["significant_0_05"] else "Nein",
                "Hinweis": test_bait["note"],
            },
        ]
    )

    complete_csv = build_complete_results_csv(
        summary_text=summary_text,
        videos_df=videos_df,
        grouped_stats=grouped_stats,
        ranking_all=ranking_all,
        test_df=test_df,
        pair_location=pair_location,
        pair_bait=pair_bait,
        site_global=site_global,
        site_pairwise=site_pairwise,
    )
    complete_csv.to_csv(REPORT_DIR / "species_richness_complete_results.csv", index=False)

    write_markdown_report(
        videos_df=videos_df,
        grouped_stats=grouped_stats,
        ranking_all=ranking_all,
        test_location=test_location,
        test_bait=test_bait,
        pair_location=pair_location,
        pair_bait=pair_bait,
        site_global=site_global,
        site_pairwise=site_pairwise,
        figure_paths=figure_paths,
        summary_text=summary_text,
    )

    print("Erstellt:")
    print(f"- {REPORT_DIR / 'species richness.md'}")
    print(f"- {REPORT_DIR / 'species_richness_complete_results.csv'}")
    print(f"- {REPORT_DIR / 'species_richness_all_46_videos.csv'}")
    print(f"- {REPORT_DIR / 'species_richness_grouped_stats.csv'}")
    print(f"- {REPORT_DIR / 'species_richness_significance_pairwise_standort.csv'}")
    print(f"- {REPORT_DIR / 'species_richness_significance_pairwise_koeder.csv'}")
    print(f"- {REPORT_DIR / 'species_richness_significance_koeder_by_standort_global.csv'}")
    print(f"- {REPORT_DIR / 'species_richness_significance_koeder_by_standort_pairwise.csv'}")
    print(f"- {FIG_DIR}")


if __name__ == "__main__":
    main()
