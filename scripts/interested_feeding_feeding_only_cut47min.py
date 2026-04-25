#!/usr/bin/env python3
"""
Feeding-only Koedervergleich (cut_47min) fuer alle Standorte.

Anforderung:
- Nur feeding-Annotationen auswerten.
- Je Standort in results/interested_feeding/<site>/feeding ausgeben.
- Signifikanz zwischen Koedern pruefen (gesamt und taxonbasiert).
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min"
CORAL_REEF_DIR = CUT_ROOT / "Annotation_reports_coral_reef"
NURSERY_DIR = CUT_ROOT / "Annotation_reports_Nursery"
OUT_ROOT = ROOT / "results" / "interested_feeding"

SITES = ["milimani", "utumbi", "nursery"]
ALPHA = 0.05


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


def bh_adjust(p_values: List[float]) -> List[float]:
    m = len(p_values)
    if m == 0:
        return []
    order = np.argsort(p_values)
    adjusted_ordered = np.zeros(m)
    for i, idx in enumerate(order, start=1):
        adjusted_ordered[i - 1] = p_values[idx] * m / i
    for i in range(m - 2, -1, -1):
        adjusted_ordered[i] = min(adjusted_ordered[i], adjusted_ordered[i + 1])
    adjusted_ordered = np.clip(adjusted_ordered, 0.0, 1.0)
    adjusted = np.zeros(m)
    for i, idx in enumerate(order):
        adjusted[idx] = adjusted_ordered[i]
    return adjusted.tolist()


def significance_label(p_value: float) -> str:
    if pd.isna(p_value):
        return "n/a"
    if p_value < 0.001:
        return "***"
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return "ns"


def to_md(df: pd.DataFrame) -> str:
    if df.empty:
        return "Keine Daten."
    return df.to_markdown(index=False)


def safe_kruskal(groups: List[np.ndarray]) -> Tuple[float, float]:
    flat = np.concatenate(groups) if groups else np.array([], dtype=float)
    if flat.size == 0:
        return 0.0, 1.0
    if float(np.nanmax(flat) - np.nanmin(flat)) == 0.0:
        return 0.0, 1.0
    try:
        h_stat, p_val = stats.kruskal(*groups)
    except ValueError:
        return 0.0, 1.0
    if pd.isna(h_stat):
        h_stat = 0.0
    if pd.isna(p_val):
        p_val = 1.0
    return float(h_stat), float(p_val)


def load_video_feeding(csv_path: Path) -> Dict[str, object]:
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")

    counts_by_taxon: Dict[str, int] = {}
    for _, row in df.iterrows():
        if not is_truthy(row.get("feeding", "")):
            continue
        taxon = build_taxon_key(row)
        if not taxon:
            continue
        counts_by_taxon[taxon] = counts_by_taxon.get(taxon, 0) + 1

    date, site, bait = parse_video_metadata(csv_path.name)
    return {
        "filename": csv_path.name,
        "date": date,
        "standort": site,
        "koeder": bait,
        "feeding_counts_by_taxon": counts_by_taxon,
        "total_feeding_events": int(sum(counts_by_taxon.values())),
        "feeding_unique_taxa": int(len(counts_by_taxon)),
    }


def analyze_site(site_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    bait_order = sorted(site_df["koeder"].unique().tolist())
    videos_by_bait = {b: site_df[site_df["koeder"] == b].copy() for b in bait_order}

    # Globaltest auf total feeding events je Video
    groups = [videos_by_bait[b]["total_feeding_events"].astype(float).to_numpy() for b in bait_order]
    h_total, p_total = safe_kruskal(groups)

    overall_df = pd.DataFrame(
        [
            {
                "n_videos": int(len(site_df)),
                "n_koeder": int(len(bait_order)),
                "h_stat": float(h_total),
                "p_value": float(p_total),
                "significant_0_05": bool(p_total < ALPHA),
                "sig_label": significance_label(float(p_total)),
            }
        ]
    )

    # Paarweise total feeding events
    pair_rows: List[Dict[str, object]] = []
    raw_ps: List[float] = []
    for a, b in itertools.combinations(bait_order, 2):
        xa = videos_by_bait[a]["total_feeding_events"].astype(float).to_numpy()
        xb = videos_by_bait[b]["total_feeding_events"].astype(float).to_numpy()
        try:
            u_stat, p_val = stats.mannwhitneyu(xa, xb, alternative="two-sided")
        except ValueError:
            u_stat, p_val = 0.0, 1.0
        raw_ps.append(float(p_val))
        pair_rows.append(
            {
                "koeder_a": a,
                "koeder_b": b,
                "n_a": int(len(xa)),
                "n_b": int(len(xb)),
                "mean_total_a": float(np.mean(xa)) if len(xa) else math.nan,
                "mean_total_b": float(np.mean(xb)) if len(xb) else math.nan,
                "u_stat": float(u_stat),
                "p_value": float(p_val),
            }
        )

    overall_pair_df = pd.DataFrame(pair_rows)
    if not overall_pair_df.empty:
        overall_pair_df["p_value_holm"] = holm_adjust(raw_ps)
        overall_pair_df["p_value_bh"] = bh_adjust(raw_ps)
        overall_pair_df["significant_holm"] = overall_pair_df["p_value_holm"] < ALPHA
        overall_pair_df["significant_bh"] = overall_pair_df["p_value_bh"] < ALPHA
        overall_pair_df["sig_label_raw"] = overall_pair_df["p_value"].map(significance_label)
        overall_pair_df["sig_label_holm"] = overall_pair_df["p_value_holm"].map(significance_label)

    # Taxon-Tests
    all_taxa = sorted(
        set().union(
            *[set().union(*videos_by_bait[b]["feeding_counts_by_taxon"].map(dict.keys).tolist()) for b in bait_order]
        )
    )

    taxa_rows: List[Dict[str, object]] = []
    taxa_pair_rows: List[Dict[str, object]] = []

    for taxon in all_taxa:
        arrays_by_bait: Dict[str, np.ndarray] = {}
        for bait in bait_order:
            vals = [float(v.get(taxon, 0)) for v in videos_by_bait[bait]["feeding_counts_by_taxon"].tolist()]
            arrays_by_bait[bait] = np.array(vals, dtype=float)

        # Nur Taxa testen, die in >=2 Koedern vorkommen
        present_baits = [b for b in bait_order if float(np.sum(arrays_by_bait[b])) > 0]
        if len(present_baits) < 2:
            continue

        groups_tax = [arrays_by_bait[b] for b in bait_order]
        total_n = int(sum(len(g) for g in groups_tax))
        n_groups = len(groups_tax)

        h_stat, p_val = safe_kruskal(groups_tax)

        means = {b: float(np.mean(arrays_by_bait[b])) for b in bait_order}
        dominant = max(means, key=means.get)
        weakest = min(means, key=means.get)

        eta_sq = (
            float((h_stat - n_groups + 1) / (total_n - n_groups))
            if total_n > n_groups
            else math.nan
        )
        if not pd.isna(eta_sq):
            eta_sq = max(0.0, eta_sq)

        row = {
            "taxon_key": taxon,
            "n_total": total_n,
            "n_koeder": n_groups,
            "h_stat": float(h_stat),
            "p_value": float(p_val),
            "eta_sq": eta_sq,
            "dominant_koeder_mean": dominant,
            "weakest_koeder_mean": weakest,
            "mean_diff_max_minus_min": float(means[dominant] - means[weakest]),
        }
        for bait in bait_order:
            row[f"mean_{bait}"] = means[bait]
        taxa_rows.append(row)

        pair_ps: List[float] = []
        tmp_pairs: List[Dict[str, object]] = []
        for a, b in itertools.combinations(bait_order, 2):
            xa = arrays_by_bait[a]
            xb = arrays_by_bait[b]
            try:
                u_stat, p_pair = stats.mannwhitneyu(xa, xb, alternative="two-sided")
            except ValueError:
                u_stat, p_pair = 0.0, 1.0
            pair_ps.append(float(p_pair))
            tmp_pairs.append(
                {
                    "taxon_key": taxon,
                    "koeder_a": a,
                    "koeder_b": b,
                    "n_a": int(len(xa)),
                    "n_b": int(len(xb)),
                    "mean_a": float(np.mean(xa)) if len(xa) else math.nan,
                    "mean_b": float(np.mean(xb)) if len(xb) else math.nan,
                    "u_stat": float(u_stat),
                    "p_value": float(p_pair),
                }
            )

        pair_holm = holm_adjust(pair_ps)
        pair_bh = bh_adjust(pair_ps)
        for rec, p_h, p_bh in zip(tmp_pairs, pair_holm, pair_bh):
            rec["p_value_holm_within_taxon"] = float(p_h)
            rec["p_value_bh_within_taxon"] = float(p_bh)
            rec["significant_holm_within_taxon"] = bool(p_h < ALPHA)
            rec["significant_bh_within_taxon"] = bool(p_bh < ALPHA)
            taxa_pair_rows.append(rec)

    taxa_df = pd.DataFrame(taxa_rows)
    if not taxa_df.empty:
        taxa_df = taxa_df.sort_values("p_value", ascending=True).reset_index(drop=True)
        taxa_df["p_value_holm"] = holm_adjust(taxa_df["p_value"].tolist())
        taxa_df["p_value_bh"] = bh_adjust(taxa_df["p_value"].tolist())
        taxa_df["significant_holm"] = taxa_df["p_value_holm"] < ALPHA
        taxa_df["significant_bh"] = taxa_df["p_value_bh"] < ALPHA

    taxa_pair_df = pd.DataFrame(taxa_pair_rows)

    # bait-spezifische Taxa
    spec_rows: List[Dict[str, object]] = []
    for taxon in all_taxa:
        present_baits = []
        for bait in bait_order:
            arr = np.array([float(v.get(taxon, 0)) for v in videos_by_bait[bait]["feeding_counts_by_taxon"].tolist()], dtype=float)
            if float(np.sum(arr)) > 0:
                present_baits.append(bait)
        if len(present_baits) == 1:
            spec_rows.append({"koeder": present_baits[0], "taxon_key": taxon})
    specific_df = pd.DataFrame(spec_rows)

    # Profile
    profile_rows: List[Dict[str, object]] = []
    spec_map = {}
    if not specific_df.empty:
        spec_counts = specific_df.groupby("koeder", as_index=False).size().rename(columns={"size": "n_bait_specific_taxa"})
        spec_map = {r.koeder: int(r.n_bait_specific_taxa) for r in spec_counts.itertuples(index=False)}

    trend_df = taxa_df[taxa_df["p_value"] < ALPHA] if not taxa_df.empty else pd.DataFrame()
    for bait in bait_order:
        sub = videos_by_bait[bait]
        profile_rows.append(
            {
                "koeder": bait,
                "n_videos": int(len(sub)),
                "mean_total_feeding_events": float(sub["total_feeding_events"].mean()) if len(sub) else math.nan,
                "median_total_feeding_events": float(sub["total_feeding_events"].median()) if len(sub) else math.nan,
                "mean_unique_feeding_taxa": float(sub["feeding_unique_taxa"].mean()) if len(sub) else math.nan,
                "n_bait_specific_taxa": int(spec_map.get(bait, 0)),
                "n_trend_taxa_dominant": int((trend_df["dominant_koeder_mean"] == bait).sum()) if not trend_df.empty else 0,
            }
        )
    profile_df = pd.DataFrame(profile_rows)

    return {
        "overall": overall_df,
        "overall_pairwise": overall_pair_df,
        "taxa_tests": taxa_df,
        "taxa_pairwise": taxa_pair_df,
        "specific_taxa": specific_df,
        "bait_profile": profile_df,
    }


def write_site_markdown(site: str, site_df: pd.DataFrame, results: Dict[str, pd.DataFrame], out_dir: Path) -> None:
    baits = sorted(site_df["koeder"].unique().tolist())
    taxa_df = results["taxa_tests"]
    overall_df = results["overall"]
    overall_pairwise_df = results["overall_pairwise"]
    profile_df = results["bait_profile"]
    specific_df = results["specific_taxa"]

    n_taxa = int(len(taxa_df))
    n_raw = int((taxa_df["p_value"] < ALPHA).sum()) if not taxa_df.empty else 0
    n_holm = int((taxa_df["p_value_holm"] < ALPHA).sum()) if not taxa_df.empty else 0

    p_overall = float(overall_df.iloc[0]["p_value"]) if not overall_df.empty else math.nan

    # Spezifisch fuer Nursery: algaemix vs mackerel
    nursery_pair_total = pd.DataFrame()
    nursery_pair_taxa = pd.DataFrame()
    if site == "nursery" and not overall_pairwise_df.empty:
        nursery_pair_total = overall_pairwise_df[
            ((overall_pairwise_df["koeder_a"] == "algaemix") & (overall_pairwise_df["koeder_b"] == "mackerel"))
            | ((overall_pairwise_df["koeder_a"] == "mackerel") & (overall_pairwise_df["koeder_b"] == "algaemix"))
        ].copy()

    if site == "nursery" and not results["taxa_pairwise"].empty:
        tp = results["taxa_pairwise"]
        nursery_pair_taxa = tp[
            ((tp["koeder_a"] == "algaemix") & (tp["koeder_b"] == "mackerel"))
            | ((tp["koeder_a"] == "mackerel") & (tp["koeder_b"] == "algaemix"))
        ].copy()

    lines: List[str] = []
    lines.append(f"# Feeding-only Koedervergleich - {site.capitalize()} (cut_47min)")
    lines.append("")
    lines.append("## Beschreibung")
    lines.append("- Es wurden ausschliesslich feeding-Annotationen ausgewertet.")
    lines.append("- Taxonschluessel: species > genus > family/label.")
    lines.append(f"- Standort: {site}; Videos: {len(site_df)}; Koeder: {', '.join(baits)}.")
    lines.append("- Tests: Kruskal-Wallis (global), Mann-Whitney U (paarweise), Holm und BH fuer multiple Tests.")
    lines.append("")

    lines.append("## Zusammenfassung der Ergebnisse")
    lines.append(f"- Getestete Taxa: {n_taxa}")
    lines.append(f"- Roh signifikante Taxa (p<0.05): {n_raw}")
    lines.append(f"- Holm-signifikante Taxa: {n_holm}")
    lines.append(
        f"- Globaler Koedereffekt auf totale feeding Events je Video: p={p_overall:.4g} ({'signifikant' if p_overall < ALPHA else 'nicht signifikant'})"
    )
    lines.append("")

    lines.append("## Kernaussagen")
    if n_holm > 0:
        lines.append("- Es gibt robuste, multipel-korrigierte Taxa-Unterschiede zwischen Koedern.")
    elif n_raw > 0:
        lines.append("- Es gibt trendhafte Taxa-Unterschiede zwischen Koedern (roh signifikant), aber keine Holm-robusten Effekte.")
    else:
        lines.append("- Es zeigen sich keine klaren Taxa-Unterschiede zwischen den Koedern.")
    lines.append("- Die stärksten Hinweise liegen bei Taxa mit hoher Mitteldifferenz zwischen dominantem und schwächstem Koeder.")
    lines.append("- Bait-spezifische Taxa liefern zusaetzlich biologische Plausibilitaet fuer koederabhaengige feeding-Muster.")
    lines.append("")

    lines.append("## Koederprofile")
    lines.append(to_md(profile_df.sort_values("koeder") if not profile_df.empty else pd.DataFrame()))
    lines.append("")

    lines.append("## Top-Taxa (global, nach p-Wert)")
    top_taxa = (
        taxa_df.sort_values(["p_value", "mean_diff_max_minus_min"], ascending=[True, False]).head(20)
        if not taxa_df.empty
        else pd.DataFrame()
    )
    if not top_taxa.empty:
        cols = [
            "taxon_key",
            "dominant_koeder_mean",
            "weakest_koeder_mean",
            "p_value",
            "p_value_holm",
            "p_value_bh",
            "mean_diff_max_minus_min",
            "eta_sq",
        ]
        lines.append(to_md(top_taxa[cols]))
    else:
        lines.append("Keine Taxa-Testergebnisse.")
    lines.append("")

    lines.append("## Paarweise Koedervergleiche (Total feeding Events je Video)")
    lines.append(to_md(overall_pairwise_df.sort_values("p_value") if not overall_pairwise_df.empty else pd.DataFrame()))
    lines.append("")

    lines.append("## Bait-spezifische Taxa")
    if specific_df.empty:
        lines.append("Keine bait-spezifischen Taxa.")
    else:
        for bait in baits:
            taxa = specific_df[specific_df["koeder"] == bait]["taxon_key"].dropna().sort_values().tolist()
            lines.append(f"- {bait} ({len(taxa)}):")
            if not taxa:
                lines.append("  - Keine")
            else:
                for t in taxa[:20]:
                    lines.append(f"  - {t}")
                if len(taxa) > 20:
                    lines.append(f"  - ... (+{len(taxa) - 20} weitere)")
    lines.append("")

    if site == "nursery":
        lines.append("## Fokus Nursery: Algaemix vs Mackerel")
        if nursery_pair_total.empty:
            lines.append("- Kein direkter Paarvergleich algaemix vs mackerel in den Total-Events verfuegbar.")
        else:
            row = nursery_pair_total.iloc[0]
            lines.append(
                f"- Total feeding Events: p={float(row['p_value']):.4g}, Holm={float(row['p_value_holm']):.4g}, BH={float(row['p_value_bh']):.4g}."
            )
            lines.append(
                f"- Signifikant (roh/Holm/BH): {bool(row['p_value'] < ALPHA)}/{bool(row['p_value_holm'] < ALPHA)}/{bool(row['p_value_bh'] < ALPHA)}"
            )

        if nursery_pair_taxa.empty:
            lines.append("- Keine Taxa-Paarvergleiche algaemix vs mackerel verfuegbar.")
        else:
            raw_sig = nursery_pair_taxa[nursery_pair_taxa["p_value"] < ALPHA]
            holm_sig = nursery_pair_taxa[nursery_pair_taxa["p_value_holm_within_taxon"] < ALPHA]
            bh_sig = nursery_pair_taxa[nursery_pair_taxa["p_value_bh_within_taxon"] < ALPHA]
            lines.append(
                f"- Taxa mit signifikantem algaemix-vs-mackerel Unterschied: roh={len(raw_sig)}, Holm={len(holm_sig)}, BH={len(bh_sig)}."
            )
            lines.append("")
            lines.append("Top Taxa fuer algaemix vs mackerel:")
            lines.append(
                to_md(
                    nursery_pair_taxa.sort_values("p_value").head(20)[
                        [
                            "taxon_key",
                            "mean_a",
                            "mean_b",
                            "p_value",
                            "p_value_holm_within_taxon",
                            "p_value_bh_within_taxon",
                        ]
                    ]
                )
            )
        lines.append("")

    lines.append("## Interpretation")
    if p_overall < ALPHA:
        lines.append(
            "- Der globale Test ist signifikant: die Gesamthaefigkeit von feeding-Ereignissen unterscheidet sich zwischen Koedern am Standort."
        )
    else:
        lines.append(
            "- Der globale Test ist nicht signifikant: auf Ebene der totalen feeding-Ereignisse zeigt sich kein robuster Koedereffekt am Standort."
        )
    lines.append(
        "- Taxon-spezifische Signifikanz (insb. nach Holm/BH) ist der robusteste Nachweis fuer echte koederabhaengige Unterschiede auf Arten/Gattungs/Familienebene."
    )
    lines.append(
        "- Roh-signifikante Effekte ohne Korrektur sind als Trends zu lesen und sollten mit groesserer Stichprobe oder fokussierten Hypothesentests validiert werden."
    )

    (out_dir / f"feeding_{site}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    files = sorted(CORAL_REEF_DIR.glob("*.csv")) + sorted(NURSERY_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError("Keine cut_47min-Dateien gefunden.")

    records = [load_video_feeding(p) for p in files]
    videos_df = pd.DataFrame(records)
    videos_df = videos_df[videos_df["standort"].isin(SITES)].copy()
    videos_df = videos_df.sort_values(["standort", "date", "filename"]).reset_index(drop=True)

    overall_rows: List[Dict[str, object]] = []

    for site in SITES:
        site_df = videos_df[videos_df["standort"] == site].copy()
        if site_df.empty:
            continue

        out_dir = OUT_ROOT / site / "feeding"
        out_dir.mkdir(parents=True, exist_ok=True)

        # Video-Level Export
        site_df[
            [
                "filename",
                "date",
                "standort",
                "koeder",
                "total_feeding_events",
                "feeding_unique_taxa",
            ]
        ].to_csv(out_dir / f"feeding_{site}_video_level.csv", index=False)

        results = analyze_site(site_df)
        results["overall"].to_csv(out_dir / f"feeding_{site}_overall_kruskal.csv", index=False)
        results["overall_pairwise"].to_csv(out_dir / f"feeding_{site}_overall_pairwise_mannwhitney.csv", index=False)
        results["taxa_tests"].to_csv(out_dir / f"feeding_{site}_taxa_global_kruskal.csv", index=False)
        results["taxa_pairwise"].to_csv(out_dir / f"feeding_{site}_taxa_pairwise_mannwhitney.csv", index=False)
        results["specific_taxa"].to_csv(out_dir / f"feeding_{site}_bait_specific_taxa.csv", index=False)
        results["bait_profile"].to_csv(out_dir / f"feeding_{site}_bait_profile.csv", index=False)

        write_site_markdown(site, site_df, results, out_dir)

        overall_row = {
            "site": site,
            "n_videos": int(len(site_df)),
            "n_baits": int(site_df["koeder"].nunique()),
            "n_taxa_tested": int(len(results["taxa_tests"])),
            "n_raw_sig_taxa": int((results["taxa_tests"]["p_value"] < ALPHA).sum()) if not results["taxa_tests"].empty else 0,
            "n_holm_sig_taxa": int((results["taxa_tests"]["p_value_holm"] < ALPHA).sum()) if not results["taxa_tests"].empty else 0,
            "overall_total_events_p": float(results["overall"].iloc[0]["p_value"]),
            "overall_total_events_sig": bool(float(results["overall"].iloc[0]["p_value"]) < ALPHA),
        }

        if site == "nursery" and not results["overall_pairwise"].empty:
            cmp_df = results["overall_pairwise"]
            cmp_df = cmp_df[
                ((cmp_df["koeder_a"] == "algaemix") & (cmp_df["koeder_b"] == "mackerel"))
                | ((cmp_df["koeder_a"] == "mackerel") & (cmp_df["koeder_b"] == "algaemix"))
            ]
            if not cmp_df.empty:
                overall_row["nursery_algaemix_vs_mackerel_p"] = float(cmp_df.iloc[0]["p_value"])
                overall_row["nursery_algaemix_vs_mackerel_p_holm"] = float(cmp_df.iloc[0]["p_value_holm"])
                overall_row["nursery_algaemix_vs_mackerel_sig_holm"] = bool(float(cmp_df.iloc[0]["p_value_holm"]) < ALPHA)

        overall_rows.append(overall_row)

    overall_df = pd.DataFrame(overall_rows).sort_values("site")
    overall_df.to_csv(OUT_ROOT / "feeding_site_summary.csv", index=False)

    lines: List[str] = []
    lines.append("# Feeding-only Koedervergleich - Gesamtuebersicht")
    lines.append("")
    lines.append(to_md(overall_df))
    lines.append("")
    lines.append("## Kurzinterpretation")
    for r in overall_df.itertuples(index=False):
        lines.append(
            f"- {r.site}: Taxa getestet={r.n_taxa_tested}, roh signifikant={r.n_raw_sig_taxa}, Holm-signifikant={r.n_holm_sig_taxa}, Gesamt-p={r.overall_total_events_p:.4g}."
        )
    lines.append("")
    lines.append("## Hinweis")
    lines.append(
        "Die detaillierten Berichte liegen pro Standort unter results/interested_feeding/<site>/feeding/feeding_<site>.md."
    )

    (OUT_ROOT / "feeding_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Feeding-only Koedervergleich abgeschlossen.")
    print(f"Ergebnisse: {OUT_ROOT}")


if __name__ == "__main__":
    main()
