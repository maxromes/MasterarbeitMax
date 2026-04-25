#!/usr/bin/env python3
"""
Artenvergleich zwischen Standorten auf Basis der cut_47min-Videos.

Ziele:
- Überlappende und standortspezifische Taxa je Standort
- Schwerpunkt Milimani vs Utumbi (gleiche Köderlandschaft)
- Vergleich aller 3 Standorte
- Grafiken + Markdown-Zusammenfassung

Ausgabe:
- results/Artenvergleich_standort/
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
NURSERY_DIR = CUT_ROOT / "Annotation_reports_Nursery"

OUT_DIR = ROOT / "results" / "Artenvergleich_standort"
FIG_DIR = OUT_DIR / "figures"

SITES = ["milimani", "utumbi", "nursery"]
SITE_COLORS = {
    "milimani": "#ff7f0e",
    "utumbi": "#1f77b4",
    "nursery": "#2ca02c",
}


def is_truthy(value: object) -> bool:
    if value is None:
        return False
    text = str(value).strip().lower()
    if text in {"", "0", "false", "f", "no", "n", "none", "null", "nan"}:
        return False
    return True


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


def build_presence_table(site_sets: Dict[str, Set[str]]) -> pd.DataFrame:
    all_taxa = sorted(set().union(*site_sets.values()))
    rows: List[Dict[str, object]] = []
    for taxon in all_taxa:
        m = int(taxon in site_sets["milimani"])
        u = int(taxon in site_sets["utumbi"])
        n = int(taxon in site_sets["nursery"])
        rows.append(
            {
                "taxon_key": taxon,
                "milimani": m,
                "utumbi": u,
                "nursery": n,
                "n_sites_present": m + u + n,
                "presence_pattern": f"{m}{u}{n}",
            }
        )
    return pd.DataFrame(rows)


def make_figures(
    pair_df: pd.DataFrame,
    pattern_df: pd.DataFrame,
    focus_df: pd.DataFrame,
    site_specific_counts: pd.DataFrame,
) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # 1) Pairwise shared/unique
    labels = [f"{r.site_a} vs {r.site_b}" for r in pair_df.itertuples()]
    shared = pair_df["intersection_taxa"].to_numpy()
    unique_a = pair_df["unique_a"].to_numpy()
    unique_b = pair_df["unique_b"].to_numpy()
    x = np.arange(len(labels))

    plt.figure(figsize=(10, 6))
    plt.bar(x, shared, label="geteilt", color="#4c78a8")
    plt.bar(x, unique_a, bottom=shared, label="nur site_a", color="#f58518")
    plt.bar(x, unique_b, bottom=shared + unique_a, label="nur site_b", color="#54a24b")
    plt.xticks(x, labels, rotation=15)
    plt.ylabel("Anzahl Taxa")
    plt.title("Artenüberlappung und standortspezifische Taxa je Standortpaar")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "pairwise_shared_unique_taxa.png", dpi=180)
    plt.close()

    # 2) Pattern-Verteilung (über 3 Standorte)
    pattern_order = ["111", "110", "101", "011", "100", "010", "001"]
    patt = pattern_df.set_index("presence_pattern").reindex(pattern_order).fillna(0).reset_index()
    plt.figure(figsize=(9, 5.5))
    plt.bar(patt["presence_pattern"], patt["n_taxa"], color="#4c78a8")
    plt.xlabel("Präsenzmuster (milimani-utumbi-nursery)")
    plt.ylabel("Anzahl Taxa")
    plt.title("Verteilung der Taxa über Standort-Präsenzmuster")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "taxa_presence_patterns.png", dpi=180)
    plt.close()

    # 3) Fokus Milimani vs Utumbi
    categories = ["geteilt", "nur milimani", "nur utumbi"]
    values = [
        int(focus_df.iloc[0]["intersection_taxa"]),
        int(focus_df.iloc[0]["unique_a"]),
        int(focus_df.iloc[0]["unique_b"]),
    ]
    colors = ["#4c78a8", SITE_COLORS["milimani"], SITE_COLORS["utumbi"]]
    plt.figure(figsize=(7.5, 5))
    plt.bar(categories, values, color=colors)
    plt.ylabel("Anzahl Taxa")
    plt.title("Fokus Milimani vs Utumbi: geteilte und exklusive Taxa")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "focus_milimani_utumbi_shared_unique.png", dpi=180)
    plt.close()

    # 4) Standortspezifische Taxa je Standort
    plt.figure(figsize=(7.5, 5))
    plt.bar(
        site_specific_counts["standort"],
        site_specific_counts["n_site_specific_taxa"],
        color=[SITE_COLORS[s] for s in site_specific_counts["standort"]],
    )
    plt.ylabel("Anzahl standortspezifischer Taxa")
    plt.title("Standortspezifische Taxa pro Standort")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "site_specific_taxa_counts.png", dpi=180)
    plt.close()


def to_md(df: pd.DataFrame) -> str:
    if df.empty:
        return "Keine Daten."
    return df.to_markdown(index=False)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(CORAL_REEF_DIR.glob("*.csv")) + sorted(NURSERY_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError("Keine cut_47min-Dateien gefunden.")

    records = [load_video_taxa(p) for p in files]
    videos_df = pd.DataFrame(records)
    videos_df = videos_df[videos_df["standort"].isin(SITES)].copy()
    videos_df = videos_df.sort_values(["standort", "date", "filename"]).reset_index(drop=True)

    site_sets: Dict[str, Set[str]] = {}
    for s in SITES:
        taxa_union: set[str] = set()
        for taxa in videos_df.loc[videos_df["standort"] == s, "taxa_set"]:
            taxa_union |= set(taxa)
        site_sets[s] = taxa_union

    # Pairwise Vergleiche
    pair_rows: List[Dict[str, object]] = []
    for a, b in itertools.combinations(SITES, 2):
        set_a = site_sets[a]
        set_b = site_sets[b]
        inter = len(set_a & set_b)
        union = len(set_a | set_b)
        jac = jaccard(set_a, set_b)
        pair_rows.append(
            {
                "site_a": a,
                "site_b": b,
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

    # Präsenzmuster über 3 Standorte
    presence_df = build_presence_table(site_sets)
    pattern_df = (
        presence_df.groupby("presence_pattern", as_index=False)
        .size()
        .rename(columns={"size": "n_taxa"})
        .sort_values("n_taxa", ascending=False)
    )

    # Standortspezifisch + geteilt
    shared_all_three = set.intersection(*(site_sets[s] for s in SITES))
    site_specific = {
        s: site_sets[s] - set().union(*(site_sets[o] for o in SITES if o != s))
        for s in SITES
    }
    site_specific_counts = pd.DataFrame(
        [{"standort": s, "n_site_specific_taxa": len(site_specific[s])} for s in SITES]
    )

    # Fokus Milimani vs Utumbi
    focus_df = pair_df[
        ((pair_df["site_a"] == "milimani") & (pair_df["site_b"] == "utumbi"))
        | ((pair_df["site_a"] == "utumbi") & (pair_df["site_b"] == "milimani"))
    ].copy()

    # Taxon-Listen exportieren
    shared_all_three_df = pd.DataFrame({"taxon_key": sorted(shared_all_three)})
    site_specific_long_rows = []
    for s in SITES:
        for taxon in sorted(site_specific[s]):
            site_specific_long_rows.append({"standort": s, "taxon_key": taxon})
    site_specific_long_df = pd.DataFrame(site_specific_long_rows)

    focus_only_milimani = sorted(site_sets["milimani"] - site_sets["utumbi"])
    focus_only_utumbi = sorted(site_sets["utumbi"] - site_sets["milimani"])
    focus_shared = sorted(site_sets["milimani"] & site_sets["utumbi"])
    focus_taxa_df = pd.DataFrame(
        {
            "milimani_only": pd.Series(focus_only_milimani),
            "utumbi_only": pd.Series(focus_only_utumbi),
            "shared_milimani_utumbi": pd.Series(focus_shared),
        }
    )

    # Ergebnisse schreiben
    videos_export = videos_df.copy()
    videos_export["n_taxa_set"] = videos_export["taxa_set"].map(len)
    videos_export = videos_export.drop(columns=["taxa_set"])

    videos_export.to_csv(OUT_DIR / "video_level_taxa_stats.csv", index=False)
    pair_df.to_csv(OUT_DIR / "pairwise_site_overlap.csv", index=False)
    presence_df.to_csv(OUT_DIR / "taxa_presence_by_site.csv", index=False)
    pattern_df.to_csv(OUT_DIR / "taxa_presence_patterns_summary.csv", index=False)
    site_specific_counts.to_csv(OUT_DIR / "site_specific_taxa_counts.csv", index=False)
    shared_all_three_df.to_csv(OUT_DIR / "shared_all_three_sites_taxa.csv", index=False)
    site_specific_long_df.to_csv(OUT_DIR / "site_specific_taxa_long.csv", index=False)
    focus_taxa_df.to_csv(OUT_DIR / "focus_milimani_utumbi_taxa_lists.csv", index=False)

    make_figures(pair_df, pattern_df, focus_df, site_specific_counts)

    # Markdown-Report
    top_patterns = pattern_df.head(7).copy()
    pattern_explain = pd.DataFrame(
        [
            {"presence_pattern": "111", "meaning": "in allen 3 Standorten"},
            {"presence_pattern": "110", "meaning": "milimani + utumbi"},
            {"presence_pattern": "101", "meaning": "milimani + nursery"},
            {"presence_pattern": "011", "meaning": "utumbi + nursery"},
            {"presence_pattern": "100", "meaning": "nur milimani"},
            {"presence_pattern": "010", "meaning": "nur utumbi"},
            {"presence_pattern": "001", "meaning": "nur nursery"},
        ]
    )

    focus_row = focus_df.iloc[0]
    focus_text = (
        f"Milimani vs Utumbi teilen {int(focus_row['intersection_taxa'])} Taxa "
        f"(Jaccard={focus_row['jaccard_similarity']:.3f}). "
        f"Exklusiv: Milimani={int(focus_row['unique_a'])}, Utumbi={int(focus_row['unique_b'])}."
    )

    report = []
    report.append("# Artenvergleich der Standorte (cut_47min)")
    report.append("")
    report.append("## Kurzfazit")
    report.append("Fokus Milimani/Utumbi: hohe Überlappung bei gleichzeitig klar vorhandenen standortspezifischen Taxa.")
    report.append("")
    report.append("## Datengrundlage")
    report.append(f"- Anzahl Videos: {len(videos_df)}")
    report.append("- Standorte: Milimani, Utumbi, Nursery")
    report.append("- Quelle: normalized_reports/cut_47min")
    report.append("- Taxonbildung: species > genus > family/label; feeding/interested ausgeschlossen")
    report.append("")
    report.append("## Fokus: Milimani vs Utumbi")
    report.append(f"- {focus_text}")
    report.append("- Hintergrund: Beide Standorte wurden mit denselben Köderkategorien beprobt.")
    report.append("")
    report.append("## Standortpaare im Vergleich")
    report.append(to_md(pair_df))
    report.append("")
    report.append("## Standortspezifische Taxa")
    report.append(to_md(site_specific_counts.sort_values("n_site_specific_taxa", ascending=False)))
    report.append("")
    report.append("### Vollständige Listen standortspezifischer Taxa")
    for s in ["milimani", "utumbi", "nursery"]:
        taxa_list = sorted(site_specific[s])
        report.append("")
        report.append(f"#### {s} ({len(taxa_list)} Taxa)")
        if not taxa_list:
            report.append("- Keine standortspezifischen Taxa.")
        else:
            for taxon in taxa_list:
                report.append(f"- {taxon}")
    report.append("")
    report.append("## Taxa in allen drei Standorten")
    report.append(f"- Anzahl: {len(shared_all_three)}")
    report.append("")
    report.append("## Präsenzmuster")
    report.append(to_md(top_patterns))
    report.append("")
    report.append("### Bedeutung der Muster-Codes")
    report.append(to_md(pattern_explain))
    report.append("")
    report.append("## Grafiken")
    report.append("- figures/pairwise_shared_unique_taxa.png")
    report.append("- figures/taxa_presence_patterns.png")
    report.append("- figures/focus_milimani_utumbi_shared_unique.png")
    report.append("- figures/site_specific_taxa_counts.png")
    report.append("")
    report.append("### Abbildungen")
    report.append("![Überlappung und exklusive Taxa je Standortpaar](figures/pairwise_shared_unique_taxa.png)")
    report.append("")
    report.append("![Verteilung der Taxa-Präsenzmuster](figures/taxa_presence_patterns.png)")
    report.append("")
    report.append("![Fokus Milimani vs Utumbi](figures/focus_milimani_utumbi_shared_unique.png)")
    report.append("")
    report.append("![Standortspezifische Taxa je Standort](figures/site_specific_taxa_counts.png)")
    report.append("")
    report.append("## Exportierte Detaildateien")
    report.append("- pairwise_site_overlap.csv")
    report.append("- taxa_presence_by_site.csv")
    report.append("- taxa_presence_patterns_summary.csv")
    report.append("- site_specific_taxa_long.csv")
    report.append("- focus_milimani_utumbi_taxa_lists.csv")
    report.append("- shared_all_three_sites_taxa.csv")

    (OUT_DIR / "artenvergleich_standort.md").write_text("\n".join(report) + "\n", encoding="utf-8")

    print("Artenvergleich Standort abgeschlossen.")
    print(f"Ergebnisse: {OUT_DIR}")


if __name__ == "__main__":
    main()
