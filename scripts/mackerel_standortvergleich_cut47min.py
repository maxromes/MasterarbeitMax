#!/usr/bin/env python3
"""
Standortvergleich nur fuer mackerel auf Basis cut_47min.

Ausgabe:
- results/mackerel_standortvergleich/
"""

from __future__ import annotations

import itertools
import math
import re
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min"
CORAL_REEF_DIR = CUT_ROOT / "Annotation_reports_coral_reef"
NURSERY_DIR = CUT_ROOT / "Annotation_reports_Nursery"
OUT_DIR = ROOT / "results" / "mackerel_standortvergleich"
DATA_DIR = OUT_DIR / "data"

ALPHA = 0.05
SITES = ["milimani", "utumbi", "nursery"]


def clean_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in {"", "nan", "none", "null"}:
        return ""
    return text


def is_truthy(value: object) -> bool:
    return clean_text(value).lower() in {"1", "true", "t", "yes", "y"}


def parse_video_meta(filename: str) -> Tuple[str, str, str]:
    stem = filename.replace(".csv", "")
    parts = stem.split("-", 2)
    if len(parts) < 3:
        return "", "unknown", "unknown"
    return parts[0], parts[1].lower(), parts[2].lower()


def parse_frame_seconds(frame_value: object) -> float | None:
    text = clean_text(frame_value)
    if not text:
        return None
    m = re.search(r"[-+]?\d*\.?\d+", text)
    if not m:
        return None
    try:
        return float(m.group(0))
    except ValueError:
        return None


def build_general_taxon_key(row: pd.Series) -> str:
    species = clean_text(row.get("species", ""))
    genus = clean_text(row.get("genus", ""))
    family = clean_text(row.get("family", ""))
    label = clean_text(row.get("label_name", ""))

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


def build_species_key(row: pd.Series) -> str:
    s = clean_text(row.get("species", ""))
    return s.lower() if s else ""


def build_family_key(row: pd.Series) -> str:
    s = clean_text(row.get("family", ""))
    return s.lower() if s else ""


def holm_adjust(p_values: Sequence[float]) -> List[float]:
    m = len(p_values)
    if m == 0:
        return []
    order = np.argsort(p_values)
    adjusted_order = np.zeros(m, dtype=float)
    for i, idx in enumerate(order):
        adjusted_order[i] = min(1.0, (m - i) * float(p_values[idx]))
    adjusted_order = np.maximum.accumulate(adjusted_order)
    out = np.empty(m, dtype=float)
    out[order] = adjusted_order
    return out.tolist()


def benjamini_hochberg(p_values: Sequence[float]) -> List[float]:
    m = len(p_values)
    if m == 0:
        return []
    order = np.argsort(p_values)
    ranked = np.array([p_values[i] for i in order], dtype=float)
    adjusted = np.empty(m, dtype=float)
    prev = 1.0
    for i in range(m - 1, -1, -1):
        rank = i + 1
        val = (ranked[i] * m) / rank
        prev = min(prev, val)
        adjusted[i] = min(1.0, prev)
    out = np.empty(m, dtype=float)
    out[order] = adjusted
    return out.tolist()


def significance_label(p: float) -> str:
    if pd.isna(p):
        return "n/a"
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return "ns"


def to_md(df: pd.DataFrame) -> str:
    if df.empty:
        return "Keine Daten."
    return df.to_markdown(index=False)


def safe_cols(df: pd.DataFrame, cols: Sequence[str]) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=list(cols))
    for c in cols:
        if c not in df.columns:
            return pd.DataFrame(columns=list(cols))
    return df.loc[:, list(cols)].copy()


def load_video_data(csv_path: Path) -> Dict[str, object]:
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")

    non_behavior = df[(~df["feeding"].map(is_truthy)) & (~df["interested"].map(is_truthy))].copy()
    feeding_df = df[df["feeding"].map(is_truthy)].copy()
    interested_df = df[df["interested"].map(is_truthy)].copy()

    species_counts: Dict[str, int] = {}
    species_first_seen: Dict[str, float] = {}
    family_first_seen: Dict[str, float] = {}
    species_by_time: Dict[Tuple[str, float], int] = {}
    family_by_time: Dict[Tuple[str, float], int] = {}

    species_set: set[str] = set()
    family_set: set[str] = set()
    general_set: set[str] = set()
    non_behavior_frames: List[float] = []

    for _, row in non_behavior.iterrows():
        sec = parse_frame_seconds(row.get("frames", ""))
        if sec is not None:
            non_behavior_frames.append(sec)

        g_key = build_general_taxon_key(row)
        s_key = build_species_key(row)
        f_key = build_family_key(row)

        if g_key:
            general_set.add(g_key)
        if s_key:
            species_set.add(s_key)
            species_counts[s_key] = species_counts.get(s_key, 0) + 1
            if sec is not None and (s_key not in species_first_seen or sec < species_first_seen[s_key]):
                species_first_seen[s_key] = sec
            if sec is not None:
                k = (s_key, round(sec, 2))
                species_by_time[k] = species_by_time.get(k, 0) + 1
        if f_key:
            family_set.add(f_key)
            if sec is not None and (f_key not in family_first_seen or sec < family_first_seen[f_key]):
                family_first_seen[f_key] = sec
            if sec is not None:
                k = (f_key, round(sec, 2))
                family_by_time[k] = family_by_time.get(k, 0) + 1

    species_maxn: Dict[str, int] = {}
    for (taxon, _), n in species_by_time.items():
        species_maxn[taxon] = max(species_maxn.get(taxon, 0), int(n))

    family_maxn: Dict[str, int] = {}
    for (taxon, _), n in family_by_time.items():
        family_maxn[taxon] = max(family_maxn.get(taxon, 0), int(n))

    feeding_species: Dict[str, int] = {}
    feeding_family: Dict[str, int] = {}
    interested_species: Dict[str, int] = {}
    interested_family: Dict[str, int] = {}

    for _, row in feeding_df.iterrows():
        s = build_species_key(row)
        f = build_family_key(row)
        if s:
            feeding_species[s] = feeding_species.get(s, 0) + 1
        if f:
            feeding_family[f] = feeding_family.get(f, 0) + 1

    for _, row in interested_df.iterrows():
        s = build_species_key(row)
        f = build_family_key(row)
        if s:
            interested_species[s] = interested_species.get(s, 0) + 1
        if f:
            interested_family[f] = interested_family.get(f, 0) + 1

    date, standort, koeder = parse_video_meta(csv_path.name)
    return {
        "filename": csv_path.name,
        "date": date,
        "standort": standort,
        "koeder": koeder,
        "duration_sec_non_behavior": float(np.nanmax(non_behavior_frames)) if non_behavior_frames else math.nan,
        "species_richness": len(species_set),
        "family_richness": len(family_set),
        "general_richness": len(general_set),
        "total_non_behavior_annotations": int(len(non_behavior)),
        "shannon_species": float(stats.entropy(np.array(list(species_counts.values()), dtype=float), base=np.e)) if species_counts else math.nan,
        "median_first_seen_species_sec": float(np.median(list(species_first_seen.values()))) if species_first_seen else math.nan,
        "median_first_seen_family_sec": float(np.median(list(family_first_seen.values()))) if family_first_seen else math.nan,
        "sum_species_maxn": float(np.sum(list(species_maxn.values()))) if species_maxn else 0.0,
        "sum_family_maxn": float(np.sum(list(family_maxn.values()))) if family_maxn else 0.0,
        "peak_species_maxn": float(np.max(list(species_maxn.values()))) if species_maxn else 0.0,
        "peak_family_maxn": float(np.max(list(family_maxn.values()))) if family_maxn else 0.0,
        "total_feeding_events": int(len(feeding_df)),
        "total_interested_events": int(len(interested_df)),
        "feeding_unique_species": len(feeding_species),
        "feeding_unique_family": len(feeding_family),
        "interested_unique_species": len(interested_species),
        "interested_unique_family": len(interested_family),
        "feeding_ratio_total": float(len(feeding_df) / len(df)) if len(df) else math.nan,
        "interested_ratio_total": float(len(interested_df) / len(df)) if len(df) else math.nan,
        "species_maxn_by_taxon": species_maxn,
        "family_maxn_by_taxon": family_maxn,
        "feeding_species_by_taxon": feeding_species,
        "feeding_family_by_taxon": feeding_family,
        "interested_species_by_taxon": interested_species,
        "interested_family_by_taxon": interested_family,
    }


def run_video_metric_tests(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    metrics = [
        "duration_sec_non_behavior",
        "species_richness",
        "family_richness",
        "general_richness",
        "total_non_behavior_annotations",
        "shannon_species",
        "median_first_seen_species_sec",
        "median_first_seen_family_sec",
        "sum_species_maxn",
        "sum_family_maxn",
        "peak_species_maxn",
        "peak_family_maxn",
        "total_feeding_events",
        "total_interested_events",
        "feeding_unique_species",
        "feeding_unique_family",
        "interested_unique_species",
        "interested_unique_family",
        "feeding_ratio_total",
        "interested_ratio_total",
    ]

    global_rows: List[Dict[str, object]] = []
    pair_rows: List[Dict[str, object]] = []

    for metric in metrics:
        arrays = []
        for s in SITES:
            arr = df.loc[df["standort"] == s, metric].astype(float).dropna().to_numpy()
            if len(arr) > 0:
                arrays.append(arr)

        if len(arrays) < 2:
            continue

        joined = np.concatenate(arrays)
        if len(joined) == 0 or np.allclose(joined, joined[0]):
            h, p = 0.0, 1.0
        else:
            try:
                h, p = stats.kruskal(*arrays)
                if pd.isna(p):
                    h, p = 0.0, 1.0
            except ValueError:
                h, p = 0.0, 1.0

        n_total = int(sum(len(a) for a in arrays))
        eps_sq = float((h - len(arrays) + 1) / (n_total - len(arrays))) if n_total > len(arrays) else math.nan
        if not pd.isna(eps_sq):
            eps_sq = max(0.0, eps_sq)

        row = {
            "metric": metric,
            "test": "Kruskal-Wallis",
            "h_stat": float(h),
            "p_value": float(p),
            "epsilon_sq": eps_sq,
        }
        for s in SITES:
            arr = df.loc[df["standort"] == s, metric].astype(float).dropna().to_numpy()
            row[f"n_{s}"] = int(len(arr))
            row[f"mean_{s}"] = float(np.mean(arr)) if len(arr) else math.nan
            row[f"median_{s}"] = float(np.median(arr)) if len(arr) else math.nan
        global_rows.append(row)

        p_vals = []
        temp = []
        for a, b in itertools.combinations(SITES, 2):
            xa = df.loc[df["standort"] == a, metric].astype(float).dropna().to_numpy()
            xb = df.loc[df["standort"] == b, metric].astype(float).dropna().to_numpy()
            if len(xa) == 0 or len(xb) == 0:
                continue
            try:
                u, p_pair = stats.mannwhitneyu(xa, xb, alternative="two-sided", method="exact")
            except TypeError:
                u, p_pair = stats.mannwhitneyu(xa, xb, alternative="two-sided")
            except ValueError:
                u, p_pair = 0.0, 1.0
            p_vals.append(float(p_pair))
            temp.append({
                "metric": metric,
                "site_a": a,
                "site_b": b,
                "n_a": int(len(xa)),
                "n_b": int(len(xb)),
                "u_stat": float(u),
                "p_value": float(p_pair),
            })

        p_adj = holm_adjust(p_vals)
        for r, pa in zip(temp, p_adj):
            r["p_value_holm_within_metric"] = float(pa)
            pair_rows.append(r)

    global_df = pd.DataFrame(global_rows)
    if not global_df.empty:
        global_df = global_df.sort_values("p_value", ascending=True).reset_index(drop=True)
        global_df["p_value_holm"] = holm_adjust(global_df["p_value"].tolist())
        global_df["p_value_bh"] = benjamini_hochberg(global_df["p_value"].tolist())
        global_df["sig_raw"] = global_df["p_value"].map(significance_label)
        global_df["sig_holm"] = global_df["p_value_holm"].map(significance_label)
        global_df["sig_bh"] = global_df["p_value_bh"].map(significance_label)
        global_df["significant_raw"] = global_df["p_value"] < ALPHA
        global_df["significant_holm"] = global_df["p_value_holm"] < ALPHA
        global_df["significant_bh"] = global_df["p_value_bh"] < ALPHA

    pair_df = pd.DataFrame(pair_rows)
    if not pair_df.empty:
        pair_df = pair_df.sort_values(["metric", "p_value"]).reset_index(drop=True)
        pair_df["sig_raw"] = pair_df["p_value"].map(significance_label)
        pair_df["sig_holm_within_metric"] = pair_df["p_value_holm_within_metric"].map(significance_label)
    return global_df, pair_df


def run_taxon_tests(df: pd.DataFrame, dict_col: str, level_name: str) -> pd.DataFrame:
    site_dicts = {s: df.loc[df["standort"] == s, dict_col].tolist() for s in SITES}
    all_taxa = sorted(set().union(*[set().union(*[set(d.keys()) for d in site_dicts[s]]) for s in SITES if site_dicts[s]]))

    rows: List[Dict[str, object]] = []
    for taxon in all_taxa:
        arrays = []
        row = {"level": level_name, "metric_source": dict_col, "taxon": taxon}
        for s in SITES:
            vals = np.array([float(d.get(taxon, 0)) for d in site_dicts[s]], dtype=float)
            arrays.append(vals)
            row[f"mean_{s}"] = float(np.mean(vals)) if len(vals) else math.nan
            row[f"occ_{s}"] = float(np.mean(vals > 0)) if len(vals) else math.nan
            row[f"n_{s}"] = int(len(vals))

        valid = [a for a in arrays if len(a) > 0]
        if len(valid) < 2:
            continue

        joined = np.concatenate(valid)
        if len(joined) == 0 or np.allclose(joined, joined[0]):
            h, p = 0.0, 1.0
        else:
            try:
                h, p = stats.kruskal(*valid)
                if pd.isna(p):
                    h, p = 0.0, 1.0
            except ValueError:
                h, p = 0.0, 1.0

        n_total = int(sum(len(a) for a in valid))
        eps_sq = float((h - len(valid) + 1) / (n_total - len(valid))) if n_total > len(valid) else math.nan
        if not pd.isna(eps_sq):
            eps_sq = max(0.0, eps_sq)

        row["h_stat"] = float(h)
        row["p_value"] = float(p)
        row["epsilon_sq"] = eps_sq
        rows.append(row)

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out = out.sort_values("p_value", ascending=True).reset_index(drop=True)
    out["p_value_holm"] = holm_adjust(out["p_value"].tolist())
    out["p_value_bh"] = benjamini_hochberg(out["p_value"].tolist())
    out["sig_raw"] = out["p_value"].map(significance_label)
    out["sig_holm"] = out["p_value_holm"].map(significance_label)
    out["sig_bh"] = out["p_value_bh"].map(significance_label)
    out["significant_raw"] = out["p_value"] < ALPHA
    out["significant_holm"] = out["p_value_holm"] < ALPHA
    out["significant_bh"] = out["p_value_bh"] < ALPHA
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted((CORAL_REEF_DIR.glob("*.csv"))) + sorted((NURSERY_DIR.glob("*.csv")))
    videos = []
    for p in files:
        _, _, bait = parse_video_meta(p.name)
        if bait == "mackerel":
            videos.append(load_video_data(p))

    df = pd.DataFrame(videos).sort_values(["standort", "date", "filename"]).reset_index(drop=True)
    if df.empty:
        raise FileNotFoundError("Keine mackerel-Dateien in cut_47min gefunden.")

    df.to_csv(DATA_DIR / "mackerel_video_metrics.csv", index=False)

    global_video_df, pair_video_df = run_video_metric_tests(df)
    species_maxn_df = run_taxon_tests(df, "species_maxn_by_taxon", "species")
    family_maxn_df = run_taxon_tests(df, "family_maxn_by_taxon", "family")
    feeding_species_df = run_taxon_tests(df, "feeding_species_by_taxon", "species")
    feeding_family_df = run_taxon_tests(df, "feeding_family_by_taxon", "family")
    interested_species_df = run_taxon_tests(df, "interested_species_by_taxon", "species")
    interested_family_df = run_taxon_tests(df, "interested_family_by_taxon", "family")

    global_video_df.to_csv(DATA_DIR / "mackerel_video_metrics_global_tests.csv", index=False)
    pair_video_df.to_csv(DATA_DIR / "mackerel_video_metrics_pairwise_tests.csv", index=False)
    species_maxn_df.to_csv(DATA_DIR / "mackerel_species_maxn_site_tests.csv", index=False)
    family_maxn_df.to_csv(DATA_DIR / "mackerel_family_maxn_site_tests.csv", index=False)
    feeding_species_df.to_csv(DATA_DIR / "mackerel_feeding_species_site_tests.csv", index=False)
    feeding_family_df.to_csv(DATA_DIR / "mackerel_feeding_family_site_tests.csv", index=False)
    interested_species_df.to_csv(DATA_DIR / "mackerel_interested_species_site_tests.csv", index=False)
    interested_family_df.to_csv(DATA_DIR / "mackerel_interested_family_site_tests.csv", index=False)

    site_counts = df.groupby("standort", as_index=False).agg(n_videos=("filename", "count"))

    report: List[str] = []
    report.append("# Mackerel-Standortvergleich (cut_47min)")
    report.append("")
    report.append("## Datengrundlage")
    report.append("- Koeder: mackerel (nur mackerel-Videos)")
    report.append("- Quelle: normalized_reports/cut_47min")
    report.append("- Signifikanzniveau: alpha=0.05")
    report.append("- Multiple-Testing-Korrektur: Holm und Benjamini-Hochberg (BH/FDR)")
    report.append("")
    report.append("### Stichprobe je Standort")
    report.append(to_md(site_counts))
    report.append("")

    report.append("## 1) Videoebene (Species Richness, MaxN, First Seen, Interested/Feeding, weitere)")
    report.append(to_md(safe_cols(global_video_df, [
        "metric", "test", "h_stat", "p_value", "p_value_holm", "p_value_bh", "sig_raw", "sig_holm", "sig_bh"
    ])))
    report.append("")
    report.append("### Paarweise Standortvergleiche je Metrik")
    report.append(to_md(safe_cols(pair_video_df, [
        "metric", "site_a", "site_b", "p_value", "p_value_holm_within_metric", "sig_raw", "sig_holm_within_metric"
    ])))
    report.append("")

    report.append("## 2) Taxon-Ebene: MaxN")
    report.append("### Species")
    report.append(to_md(safe_cols(species_maxn_df[species_maxn_df.get("significant_raw", pd.Series(dtype=bool))], [
        "taxon", "p_value", "p_value_holm", "p_value_bh", "sig_raw", "sig_holm", "sig_bh"
    ])))
    report.append("")
    report.append("### Family")
    report.append(to_md(safe_cols(family_maxn_df[family_maxn_df.get("significant_raw", pd.Series(dtype=bool))], [
        "taxon", "p_value", "p_value_holm", "p_value_bh", "sig_raw", "sig_holm", "sig_bh"
    ])))
    report.append("")

    report.append("## 3) Interested/Feeding nach Standort")
    report.append("### Feeding (Species)")
    report.append(to_md(safe_cols(feeding_species_df[feeding_species_df.get("significant_raw", pd.Series(dtype=bool))], [
        "taxon", "p_value", "p_value_holm", "p_value_bh", "sig_raw", "sig_holm", "sig_bh"
    ])))
    report.append("")
    report.append("### Feeding (Family)")
    report.append(to_md(safe_cols(feeding_family_df[feeding_family_df.get("significant_raw", pd.Series(dtype=bool))], [
        "taxon", "p_value", "p_value_holm", "p_value_bh", "sig_raw", "sig_holm", "sig_bh"
    ])))
    report.append("")
    report.append("### Interested (Species)")
    report.append(to_md(safe_cols(interested_species_df[interested_species_df.get("significant_raw", pd.Series(dtype=bool))], [
        "taxon", "p_value", "p_value_holm", "p_value_bh", "sig_raw", "sig_holm", "sig_bh"
    ])))
    report.append("")
    report.append("### Interested (Family)")
    report.append(to_md(safe_cols(interested_family_df[interested_family_df.get("significant_raw", pd.Series(dtype=bool))], [
        "taxon", "p_value", "p_value_holm", "p_value_bh", "sig_raw", "sig_holm", "sig_bh"
    ])))
    report.append("")

    n_sig_vid_holm = int(global_video_df["significant_holm"].sum()) if not global_video_df.empty else 0
    n_sig_vid_bh = int(global_video_df["significant_bh"].sum()) if not global_video_df.empty else 0
    n_sig_sp_holm = int(species_maxn_df["significant_holm"].sum()) if not species_maxn_df.empty else 0
    n_sig_fa_holm = int(family_maxn_df["significant_holm"].sum()) if not family_maxn_df.empty else 0

    report.append("## Fazit")
    report.append(f"- Videoebene: Holm-signifikant {n_sig_vid_holm}, BH-signifikant {n_sig_vid_bh}.")
    report.append(f"- Species-MaxN: Holm-signifikant {n_sig_sp_holm}.")
    report.append(f"- Family-MaxN: Holm-signifikant {n_sig_fa_holm}.")
    report.append("- Robust signifikant gelten nur Befunde nach Holm/BH.")
    report.append("")

    (OUT_DIR / "mackerel_standortvergleich.md").write_text("\n".join(report), encoding="utf-8")


if __name__ == "__main__":
    main()
