#!/usr/bin/env python3
"""
Artenvergleich nach Koedern (cut_47min), getrennt nach Standort.

Standorte:
- Milimani
- Utumbi

Ausgabeordner:
- results/artenvergleich_köder/
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path
from typing import Dict, List, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min"
CORAL_REEF_DIR = CUT_ROOT / "Annotation_reports_coral_reef"

OUT_DIR = ROOT / "results" / "artenvergleich_köder"
FIG_DIR = OUT_DIR / "figures"

TARGET_SITES = ["milimani", "utumbi"]


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


def load_video_taxa(csv_path: Path) -> Dict[str, object]:
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")
    taxa: set[str] = set()

    for _, row in df.iterrows():
        if is_truthy(row.get("feeding", "")) or is_truthy(row.get("interested", "")):
            continue
        key = build_taxon_key(row)
        if key:
            taxa.add(key)

    date, standort, koeder = parse_video_metadata(csv_path.name)
    return {
        "filename": csv_path.name,
        "date": date,
        "standort": standort,
        "koeder": koeder,
        "taxa_set": taxa,
        "species_richness": len(taxa),
    }


def jaccard(a: Set[str], b: Set[str]) -> float:
    union = len(a | b)
    if union == 0:
        return math.nan
    return len(a & b) / union


def to_md(df: pd.DataFrame) -> str:
    if df.empty:
        return "Keine Daten."
    return df.to_markdown(index=False)


def build_presence_table(bait_sets: Dict[str, Set[str]], bait_order: List[str]) -> pd.DataFrame:
    all_taxa = sorted(set().union(*bait_sets.values()))
    rows: List[Dict[str, object]] = []
    for taxon in all_taxa:
        presence_bits: List[str] = []
        row: Dict[str, object] = {"taxon_key": taxon}
        present_count = 0
        for bait in bait_order:
            present = int(taxon in bait_sets[bait])
            row[bait] = present
            presence_bits.append(str(present))
            present_count += present
        row["n_baits_present"] = present_count
        row["presence_pattern"] = "".join(presence_bits)
        rows.append(row)
    return pd.DataFrame(rows)


def make_site_figures(
    site: str,
    pair_df: pd.DataFrame,
    pattern_df: pd.DataFrame,
    bait_specific_counts: pd.DataFrame,
) -> None:
    site_fig_dir = FIG_DIR / site
    site_fig_dir.mkdir(parents=True, exist_ok=True)

    # 1) Pairwise shared/unique
    labels = [f"{r.bait_a} vs {r.bait_b}" for r in pair_df.itertuples()]
    shared = pair_df["intersection_taxa"].to_numpy()
    ua = pair_df["unique_a"].to_numpy()
    ub = pair_df["unique_b"].to_numpy()
    x = np.arange(len(labels))

    plt.figure(figsize=(12, 6))
    plt.bar(x, shared, label="geteilt", color="#4c78a8")
    plt.bar(x, ua, bottom=shared, label="nur bait_a", color="#f58518")
    plt.bar(x, ub, bottom=shared + ua, label="nur bait_b", color="#54a24b")
    plt.xticks(x, labels, rotation=40, ha="right")
    plt.ylabel("Anzahl Taxa")
    plt.title(f"{site.capitalize()}: Artenueberlappung und exklusive Taxa je Koederpaar")
    plt.legend()
    plt.tight_layout()
    plt.savefig(site_fig_dir / "pairwise_shared_unique_taxa.png", dpi=180)
    plt.close()

    # 2) Praesenzmuster
    patt = pattern_df.sort_values("n_taxa", ascending=False).head(15)
    plt.figure(figsize=(10, 5.5))
    plt.bar(patt["presence_pattern"], patt["n_taxa"], color="#4c78a8")
    plt.xlabel("Praesenzmuster ueber Koeder")
    plt.ylabel("Anzahl Taxa")
    plt.title(f"{site.capitalize()}: Verteilung der Taxa-Praesenzmuster")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(site_fig_dir / "taxa_presence_patterns.png", dpi=180)
    plt.close()

    # 3) Koederspezifische Taxa
    plt.figure(figsize=(9, 5.5))
    plt.bar(bait_specific_counts["koeder"], bait_specific_counts["n_bait_specific_taxa"], color="#1f77b4")
    plt.ylabel("Anzahl koederspezifischer Taxa")
    plt.title(f"{site.capitalize()}: Koederspezifische Taxa pro Koeder")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(site_fig_dir / "bait_specific_taxa_counts.png", dpi=180)
    plt.close()


def analyze_site(videos_df: pd.DataFrame, site: str) -> Dict[str, object]:
    sub = videos_df[videos_df["standort"] == site].copy()
    bait_sets: Dict[str, Set[str]] = {}
    bait_video_counts = sub.groupby("koeder").size().to_dict()

    for bait, part in sub.groupby("koeder"):
        taxa_union: set[str] = set()
        for taxa in part["taxa_set"]:
            taxa_union |= set(taxa)
        bait_sets[bait] = taxa_union

    bait_order = sorted(bait_sets.keys())

    pair_rows: List[Dict[str, object]] = []
    for a, b in itertools.combinations(bait_order, 2):
        set_a = bait_sets[a]
        set_b = bait_sets[b]
        inter = len(set_a & set_b)
        union = len(set_a | set_b)
        jac = jaccard(set_a, set_b)
        pair_rows.append(
            {
                "bait_a": a,
                "bait_b": b,
                "n_taxa_a": len(set_a),
                "n_taxa_b": len(set_b),
                "intersection_taxa": inter,
                "union_taxa": union,
                "jaccard_similarity": jac,
                "jaccard_distance": (1.0 - jac) if not math.isnan(jac) else math.nan,
                "unique_a": len(set_a - set_b),
                "unique_b": len(set_b - set_a),
            }
        )
    pair_df = pd.DataFrame(pair_rows).sort_values("jaccard_similarity", ascending=False).reset_index(drop=True)

    presence_df = build_presence_table(bait_sets, bait_order)
    pattern_df = (
        presence_df.groupby("presence_pattern", as_index=False)
        .size()
        .rename(columns={"size": "n_taxa"})
        .sort_values("n_taxa", ascending=False)
    )

    # Koederspezifische Taxa: nur in genau einem Koeder vorhanden
    bait_specific: Dict[str, Set[str]] = {}
    for bait in bait_order:
        others_union = set().union(*(bait_sets[b] for b in bait_order if b != bait)) if len(bait_order) > 1 else set()
        bait_specific[bait] = bait_sets[bait] - others_union

    bait_specific_counts = pd.DataFrame(
        [
            {
                "koeder": bait,
                "n_bait_specific_taxa": len(bait_specific[bait]),
                "n_videos": int(bait_video_counts.get(bait, 0)),
            }
            for bait in bait_order
        ]
    ).sort_values("koeder")

    all_shared = set.intersection(*(bait_sets[b] for b in bait_order)) if bait_order else set()

    return {
        "site": site,
        "bait_order": bait_order,
        "bait_sets": bait_sets,
        "pair_df": pair_df,
        "presence_df": presence_df,
        "pattern_df": pattern_df,
        "bait_specific": bait_specific,
        "bait_specific_counts": bait_specific_counts,
        "all_shared": all_shared,
        "n_videos": int(len(sub)),
    }


def write_site_outputs(result: Dict[str, object]) -> None:
    site = result["site"]
    pair_df: pd.DataFrame = result["pair_df"]
    presence_df: pd.DataFrame = result["presence_df"]
    pattern_df: pd.DataFrame = result["pattern_df"]
    bait_specific_counts: pd.DataFrame = result["bait_specific_counts"]
    bait_specific: Dict[str, Set[str]] = result["bait_specific"]
    all_shared: Set[str] = result["all_shared"]
    bait_sets: Dict[str, Set[str]] = result["bait_sets"]
    bait_order: List[str] = result["bait_order"]

    site_dir = OUT_DIR / site
    site_dir.mkdir(parents=True, exist_ok=True)

    pair_df.to_csv(site_dir / f"{site}_pairwise_koeder_overlap.csv", index=False)
    presence_df.to_csv(site_dir / f"{site}_taxa_presence_by_koeder.csv", index=False)
    pattern_df.to_csv(site_dir / f"{site}_taxa_presence_patterns_summary.csv", index=False)
    bait_specific_counts.to_csv(site_dir / f"{site}_koederspezifische_taxa_counts.csv", index=False)
    pd.DataFrame({"taxon_key": sorted(all_shared)}).to_csv(site_dir / f"{site}_taxa_shared_all_koeder.csv", index=False)

    specific_rows = []
    for bait in bait_order:
        for taxon in sorted(bait_specific[bait]):
            specific_rows.append({"koeder": bait, "taxon_key": taxon})
    pd.DataFrame(specific_rows).to_csv(site_dir / f"{site}_koederspezifische_taxa_long.csv", index=False)

    bait_list_export = {}
    max_len = 0
    for bait in bait_order:
        col = sorted(bait_sets[bait])
        bait_list_export[bait] = col
        max_len = max(max_len, len(col))
    export_df = pd.DataFrame({k: pd.Series(v) for k, v in bait_list_export.items()})
    export_df.to_csv(site_dir / f"{site}_taxa_lists_by_koeder.csv", index=False)

    make_site_figures(site, pair_df, pattern_df, bait_specific_counts)

    top_pair_text = "kein Koederpaar"
    if not pair_df.empty:
        top = pair_df.iloc[0]
        top_pair_text = (
            f"Hoechste Ueberlappung: {top['bait_a']} vs {top['bait_b']} "
            f"(Jaccard={top['jaccard_similarity']:.3f}, geteilt={int(top['intersection_taxa'])})."
        )

    report: List[str] = []
    report.append(f"# Artenvergleich Koeder - {site.capitalize()} (cut_47min)")
    report.append("")
    report.append("## Datengrundlage")
    report.append(f"- Standort: {site}")
    report.append(f"- Anzahl Videos: {result['n_videos']}")
    report.append(f"- Koeder: {', '.join(bait_order)}")
    report.append("- Taxonbildung: species > genus > family/label; feeding/interested ausgeschlossen")
    report.append("")
    report.append("## Kurzfazit")
    report.append(f"- {top_pair_text}")
    report.append(f"- Taxa, die in allen Koedern dieses Standorts vorkommen: {len(all_shared)}")
    report.append("")
    report.append("## Koederpaare im Vergleich")
    report.append(to_md(pair_df))
    report.append("")
    report.append("## Koederspezifische Taxa (Anzahl)")
    report.append(to_md(bait_specific_counts.sort_values("n_bait_specific_taxa", ascending=False)))
    report.append("")
    report.append("## Vollstaendige Listen koederspezifischer Taxa")
    for bait in bait_order:
        taxa_list = sorted(bait_specific[bait])
        report.append("")
        report.append(f"### {bait} ({len(taxa_list)} Taxa)")
        if not taxa_list:
            report.append("- Keine koederspezifischen Taxa.")
        else:
            for taxon in taxa_list:
                report.append(f"- {taxon}")
    report.append("")
    report.append("## Praesenzmuster ueber Koeder")
    report.append(to_md(pattern_df.head(15)))
    report.append("")
    report.append("## Grafiken")
    report.append(f"- ../figures/{site}/pairwise_shared_unique_taxa.png")
    report.append(f"- ../figures/{site}/taxa_presence_patterns.png")
    report.append(f"- ../figures/{site}/bait_specific_taxa_counts.png")
    report.append("")
    report.append("### Abbildungen")
    report.append(f"![Koederpaare: geteilt vs exklusiv](../figures/{site}/pairwise_shared_unique_taxa.png)")
    report.append("")
    report.append(f"![Praesenzmuster ueber Koeder](../figures/{site}/taxa_presence_patterns.png)")
    report.append("")
    report.append(f"![Koederspezifische Taxa pro Koeder](../figures/{site}/bait_specific_taxa_counts.png)")

    (site_dir / f"artenvergleich_koeder_{site}.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def write_overall_summary(results: Dict[str, Dict[str, object]]) -> None:
    lines: List[str] = []
    lines.append("# Artenvergleich Koeder (cut_47min) - Gesamtuebersicht")
    lines.append("")
    lines.append("Die Koederanalysen wurden getrennt nach Standort gerechnet, da Milimani und Utumbi nicht als Replikate behandelt werden.")
    lines.append("")

    summary_rows = []
    for site in TARGET_SITES:
        res = results[site]
        pair_df: pd.DataFrame = res["pair_df"]
        all_shared: Set[str] = res["all_shared"]
        bait_specific_counts: pd.DataFrame = res["bait_specific_counts"]

        top_pair = "-"
        top_j = math.nan
        if not pair_df.empty:
            r = pair_df.iloc[0]
            top_pair = f"{r['bait_a']} vs {r['bait_b']}"
            top_j = float(r["jaccard_similarity"])

        summary_rows.append(
            {
                "standort": site,
                "n_videos": res["n_videos"],
                "n_koeder": len(res["bait_order"]),
                "taxa_in_all_koeder": len(all_shared),
                "top_koederpaar": top_pair,
                "top_jaccard": top_j,
                "max_koederspezifische_taxa": int(bait_specific_counts["n_bait_specific_taxa"].max()) if not bait_specific_counts.empty else 0,
            }
        )

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUT_DIR / "artenvergleich_koeder_summary.csv", index=False)

    lines.append("## Kernergebnisse")
    lines.append(to_md(summary_df))
    lines.append("")
    lines.append("## Berichte pro Standort")
    lines.append("- milimani/artenvergleich_koeder_milimani.md")
    lines.append("- utumbi/artenvergleich_koeder_utumbi.md")
    lines.append("")
    lines.append("## Wichtige Exportdateien pro Standort")
    lines.append("- <standort>_pairwise_koeder_overlap.csv")
    lines.append("- <standort>_taxa_presence_by_koeder.csv")
    lines.append("- <standort>_koederspezifische_taxa_long.csv")
    lines.append("- <standort>_taxa_lists_by_koeder.csv")

    (OUT_DIR / "artenvergleich_koeder_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(CORAL_REEF_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError("Keine Dateien in normalized_reports/cut_47min/Annotation_reports_coral_reef gefunden.")

    records = [load_video_taxa(p) for p in files]
    videos_df = pd.DataFrame(records)
    videos_df = videos_df[videos_df["standort"].isin(TARGET_SITES)].copy()
    videos_df = videos_df.sort_values(["standort", "date", "filename"]).reset_index(drop=True)

    results: Dict[str, Dict[str, object]] = {}
    for site in TARGET_SITES:
        res = analyze_site(videos_df, site)
        write_site_outputs(res)
        results[site] = res

    write_overall_summary(results)

    print("Artenvergleich Koeder abgeschlossen.")
    print(f"Ergebnisse: {OUT_DIR}")


if __name__ == "__main__":
    main()
