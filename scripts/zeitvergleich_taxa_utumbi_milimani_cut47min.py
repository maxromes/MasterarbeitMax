#!/usr/bin/env python3
"""
Zeitvergleich der Taxa fuer Utumbi und Milimani auf Basis cut_47min.

Fragestellungen:
1) Gibt es je Standort und Koeder Unterschiede, welche Arten frueh erscheinen?
2) Gibt es je Standort und Koeder Unterschiede, welche Arten frueh feeding sind?
3) Optionaler Standortvergleich (Utumbi vs Milimani) innerhalb gleicher Koeder.

Ausgabe:
- results/zeitvergleich_taxa_utumbi_milimani/
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
INPUT_DIR = ROOT / "normalized_reports" / "cut_47min" / "Annotation_reports_coral_reef"
OUT_DIR = ROOT / "results" / "zeitvergleich_taxa_utumbi_milimani"
DATA_DIR = OUT_DIR / "data"

TARGET_SITES = {"utumbi", "milimani"}
ALPHA = 0.05


def clean_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in {"", "nan", "none", "null"}:
        return ""
    return text


def is_truthy(value: object) -> bool:
    text = clean_text(value).lower()
    if text in {"", "0", "false", "f", "no", "n", "none", "null", "nan"}:
        return False
    return True


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
    match = re.search(r"[-+]?\d*\.?\d+", text)
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None


def build_species_key(row: pd.Series) -> str:
    species = clean_text(row.get("species", ""))
    if species:
        return species.lower()

    genus = clean_text(row.get("genus", ""))
    if genus:
        return f"genus::{genus.lower()}"

    family = clean_text(row.get("family", ""))
    if family:
        return f"family::{family.lower()}"

    label = clean_text(row.get("label_name", ""))
    if label:
        return f"label::{label.lower()}"

    return ""


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


def cliffs_delta(x: np.ndarray, y: np.ndarray) -> float:
    total = len(x) * len(y)
    if total == 0:
        return math.nan
    gt = 0
    lt = 0
    for xi in x:
        gt += int(np.sum(xi > y))
        lt += int(np.sum(xi < y))
    return float((gt - lt) / total)


def to_md(df: pd.DataFrame) -> str:
    if df.empty:
        return "Keine Daten."
    return df.to_markdown(index=False)


def load_video_taxa_timings(csv_path: Path) -> Dict[str, object]:
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")

    non_behavior = df[(~df["feeding"].map(is_truthy)) & (~df["interested"].map(is_truthy))].copy()
    feeding_df = df[df["feeding"].map(is_truthy)].copy()

    first_seen_by_species: Dict[str, float] = {}
    first_feeding_by_species: Dict[str, float] = {}

    for _, row in non_behavior.iterrows():
        taxon = build_species_key(row)
        sec = parse_frame_seconds(row.get("frames", ""))
        if not taxon or sec is None:
            continue
        prev = first_seen_by_species.get(taxon)
        if prev is None or sec < prev:
            first_seen_by_species[taxon] = sec

    for _, row in feeding_df.iterrows():
        taxon = build_species_key(row)
        sec = parse_frame_seconds(row.get("frames", ""))
        if not taxon or sec is None:
            continue
        prev = first_feeding_by_species.get(taxon)
        if prev is None or sec < prev:
            first_feeding_by_species[taxon] = sec

    date, site, bait = parse_video_meta(csv_path.name)
    return {
        "filename": csv_path.name,
        "date": date,
        "standort": site,
        "koeder": bait,
        "first_seen_by_species": first_seen_by_species,
        "first_feeding_by_species": first_feeding_by_species,
    }


def explode_metric(records_df: pd.DataFrame, dict_col: str, metric_name: str) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    for rec in records_df.itertuples(index=False):
        d = getattr(rec, dict_col)
        if not isinstance(d, dict):
            continue
        for taxon, sec in d.items():
            rows.append(
                {
                    "filename": rec.filename,
                    "date": rec.date,
                    "standort": rec.standort,
                    "koeder": rec.koeder,
                    "taxon": taxon,
                    metric_name: float(sec),
                }
            )
    return pd.DataFrame(rows)


def per_site_per_bait_taxon_tests(metric_df: pd.DataFrame, metric_col: str) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []

    for site in sorted(metric_df["standort"].unique().tolist()):
        sub = metric_df[metric_df["standort"] == site].copy()
        if sub.empty:
            continue

        for taxon, tax_sub in sub.groupby("taxon"):
            groups = []
            bait_names = []
            for bait, part in tax_sub.groupby("koeder"):
                arr = part[metric_col].astype(float).to_numpy()
                if len(arr) >= 2:
                    groups.append(arr)
                    bait_names.append(bait)

            if len(groups) < 2:
                continue

            h_stat, p_val = stats.kruskal(*groups)
            n_total = int(sum(len(g) for g in groups))
            k = len(groups)
            eps_sq = float((h_stat - k + 1) / (n_total - k)) if n_total > k else math.nan
            if not pd.isna(eps_sq):
                eps_sq = max(0.0, eps_sq)

            medians = {
                bait: float(np.median(tax_sub.loc[tax_sub["koeder"] == bait, metric_col].to_numpy(dtype=float)))
                for bait in sorted(tax_sub["koeder"].unique().tolist())
            }
            earliest_bait = min(medians, key=medians.get)

            row = {
                "standort": site,
                "taxon": taxon,
                "metric": metric_col,
                "n_total": n_total,
                "n_koeder_with_n_ge_2": k,
                "koeder_groups_tested": " | ".join(bait_names),
                "h_stat": float(h_stat),
                "p_value": float(p_val),
                "epsilon_squared": eps_sq,
                "earliest_bait_by_median": earliest_bait,
                "earliest_median_sec": float(medians[earliest_bait]),
            }
            for bait in sorted(tax_sub["koeder"].unique().tolist()):
                bait_vals = tax_sub.loc[tax_sub["koeder"] == bait, metric_col].to_numpy(dtype=float)
                row[f"median_{bait}"] = float(np.median(bait_vals)) if len(bait_vals) else math.nan
                row[f"n_{bait}"] = int(len(bait_vals))
            rows.append(row)

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    out["p_value_holm"] = np.nan
    out["p_value_bh"] = np.nan

    for (site, metric), idx in out.groupby(["standort", "metric"]).groups.items():
        pvals = out.loc[idx, "p_value"].to_numpy(dtype=float)
        out.loc[idx, "p_value_holm"] = holm_adjust(pvals)
        out.loc[idx, "p_value_bh"] = benjamini_hochberg(pvals)

    out["sig_raw_0_05"] = out["p_value"] < ALPHA
    out["sig_holm_0_05"] = out["p_value_holm"] < ALPHA
    out["sig_bh_0_05"] = out["p_value_bh"] < ALPHA

    return out.sort_values(["standort", "metric", "p_value_bh", "p_value"]).reset_index(drop=True)


def pairwise_site_tests_within_bait(metric_df: pd.DataFrame, metric_col: str) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []

    for bait in sorted(metric_df["koeder"].unique().tolist()):
        bait_df = metric_df[metric_df["koeder"] == bait].copy()
        if bait_df.empty:
            continue

        for taxon, tax_sub in bait_df.groupby("taxon"):
            u_vals = tax_sub.loc[tax_sub["standort"] == "utumbi", metric_col].to_numpy(dtype=float)
            m_vals = tax_sub.loc[tax_sub["standort"] == "milimani", metric_col].to_numpy(dtype=float)
            if len(u_vals) < 2 or len(m_vals) < 2:
                continue

            u_stat, p_val = stats.mannwhitneyu(u_vals, m_vals, alternative="two-sided")
            rows.append(
                {
                    "koeder": bait,
                    "taxon": taxon,
                    "metric": metric_col,
                    "n_utumbi": int(len(u_vals)),
                    "n_milimani": int(len(m_vals)),
                    "u_stat": float(u_stat),
                    "p_value": float(p_val),
                    "cliffs_delta": cliffs_delta(u_vals, m_vals),
                    "median_utumbi_sec": float(np.median(u_vals)),
                    "median_milimani_sec": float(np.median(m_vals)),
                    "median_diff_utumbi_minus_milimani_sec": float(np.median(u_vals) - np.median(m_vals)),
                }
            )

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    out["p_value_holm"] = np.nan
    out["p_value_bh"] = np.nan

    for (bait, metric), idx in out.groupby(["koeder", "metric"]).groups.items():
        pvals = out.loc[idx, "p_value"].to_numpy(dtype=float)
        out.loc[idx, "p_value_holm"] = holm_adjust(pvals)
        out.loc[idx, "p_value_bh"] = benjamini_hochberg(pvals)

    out["sig_raw_0_05"] = out["p_value"] < ALPHA
    out["sig_holm_0_05"] = out["p_value_holm"] < ALPHA
    out["sig_bh_0_05"] = out["p_value_bh"] < ALPHA

    return out.sort_values(["koeder", "metric", "p_value_bh", "p_value"]).reset_index(drop=True)


def summarize_video_level(metric_df: pd.DataFrame, metric_col: str) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    for (site, bait, filename), part in metric_df.groupby(["standort", "koeder", "filename"]):
        vals = part[metric_col].to_numpy(dtype=float)
        rows.append(
            {
                "standort": site,
                "koeder": bait,
                "filename": filename,
                "n_taxa": int(len(vals)),
                "median_sec": float(np.median(vals)) if len(vals) else math.nan,
                "q25_sec": float(np.quantile(vals, 0.25)) if len(vals) else math.nan,
                "min_sec": float(np.min(vals)) if len(vals) else math.nan,
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values(["standort", "koeder", "filename"]).reset_index(drop=True)


def write_report(
    first_seen_long: pd.DataFrame,
    first_feeding_long: pd.DataFrame,
    site_bait_tests: pd.DataFrame,
    site_compare_tests: pd.DataFrame,
    first_seen_video_summary: pd.DataFrame,
    first_feeding_video_summary: pd.DataFrame,
) -> None:
    lines: List[str] = []
    lines.append("# Zeitvergleich Taxa: Utumbi vs Milimani (cut_47min)")
    lines.append("")
    lines.append("## Kurzfazit")

    def count_sig(df: pd.DataFrame, metric: str, col: str) -> int:
        if df.empty:
            return 0
        s = df[df["metric"] == metric]
        if s.empty:
            return 0
        return int(s[col].sum())

    lines.append(
        f"- Koeder-Effekt auf fruehes Auftreten (BH-signifikante Taxa): "
        f"{count_sig(site_bait_tests, 'first_seen_species_sec', 'sig_bh_0_05')}"
    )
    lines.append(
        f"- Koeder-Effekt auf fruehes Feeding (BH-signifikante Taxa): "
        f"{count_sig(site_bait_tests, 'first_feeding_species_sec', 'sig_bh_0_05')}"
    )
    lines.append(
        f"- Standortunterschiede innerhalb gleicher Koeder fuer fruehes Auftreten (BH-signifikante Taxa): "
        f"{count_sig(site_compare_tests, 'first_seen_species_sec', 'sig_bh_0_05')}"
    )
    lines.append(
        f"- Standortunterschiede innerhalb gleicher Koeder fuer fruehes Feeding (BH-signifikante Taxa): "
        f"{count_sig(site_compare_tests, 'first_feeding_species_sec', 'sig_bh_0_05')}"
    )
    lines.append("")

    lines.append("## Datenbasis")
    lines.append("- Quelle: normalized_reports/cut_47min/Annotation_reports_coral_reef")
    lines.append("- Standorte: utumbi, milimani")
    lines.append("- Metric 1: first_seen_species_sec (erstes nicht-feeding/nicht-interested Auftreten eines Taxons pro Video)")
    lines.append("- Metric 2: first_feeding_species_sec (erstes feeding-Ereignis eines Taxons pro Video)")
    lines.append("- Tests: Kruskal-Wallis je Standort ueber Koeder; Mann-Whitney fuer Standortvergleich je Koeder")
    lines.append("- Multiple Testing: Holm und Benjamini-Hochberg (BH/FDR)")
    lines.append("")

    lines.append("## Videoebene: Fruehes Auftreten")
    lines.append(to_md(first_seen_video_summary))
    lines.append("")

    lines.append("## Videoebene: Fruehes Feeding")
    lines.append(to_md(first_feeding_video_summary))
    lines.append("")

    for site in ["milimani", "utumbi"]:
        lines.append(f"## Standort {site}: Koederunterschiede in fruehem Auftreten")
        sub = site_bait_tests[(site_bait_tests["standort"] == site) & (site_bait_tests["metric"] == "first_seen_species_sec")]
        lines.append(to_md(sub.head(30)))
        lines.append("")

        lines.append(f"## Standort {site}: Koederunterschiede in fruehem Feeding")
        sub = site_bait_tests[(site_bait_tests["standort"] == site) & (site_bait_tests["metric"] == "first_feeding_species_sec")]
        lines.append(to_md(sub.head(30)))
        lines.append("")

    lines.append("## Standortvergleich (Utumbi vs Milimani) innerhalb gleicher Koeder: fruehes Auftreten")
    sub = site_compare_tests[site_compare_tests["metric"] == "first_seen_species_sec"]
    lines.append(to_md(sub.head(40)))
    lines.append("")

    lines.append("## Standortvergleich (Utumbi vs Milimani) innerhalb gleicher Koeder: fruehes Feeding")
    sub = site_compare_tests[site_compare_tests["metric"] == "first_feeding_species_sec"]
    lines.append(to_md(sub.head(40)))
    lines.append("")

    lines.append("## Interpretation")
    lines.append("- Relevante robuste Befunde sind primar jene mit BH- oder Holm-Signifikanz.")
    lines.append("- Roh-p-Werte ohne Korrektur nur als explorativ interpretieren.")

    (OUT_DIR / "zeitvergleich_taxa_utumbi_milimani.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(INPUT_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError("Keine CSV-Dateien in normalized_reports/cut_47min/Annotation_reports_coral_reef gefunden.")

    records = [load_video_taxa_timings(p) for p in files]
    rec_df = pd.DataFrame(records)
    rec_df = rec_df[rec_df["standort"].isin(TARGET_SITES)].copy()
    rec_df = rec_df.sort_values(["standort", "date", "filename"]).reset_index(drop=True)

    first_seen_long = explode_metric(rec_df, "first_seen_by_species", "first_seen_species_sec")
    first_feeding_long = explode_metric(rec_df, "first_feeding_by_species", "first_feeding_species_sec")

    first_seen_video_summary = summarize_video_level(first_seen_long, "first_seen_species_sec")
    first_feeding_video_summary = summarize_video_level(first_feeding_long, "first_feeding_species_sec")

    first_seen_tests = per_site_per_bait_taxon_tests(first_seen_long, "first_seen_species_sec")
    first_feeding_tests = per_site_per_bait_taxon_tests(first_feeding_long, "first_feeding_species_sec")
    site_bait_tests = pd.concat([first_seen_tests, first_feeding_tests], ignore_index=True)

    first_seen_site_cmp = pairwise_site_tests_within_bait(first_seen_long, "first_seen_species_sec")
    first_feeding_site_cmp = pairwise_site_tests_within_bait(first_feeding_long, "first_feeding_species_sec")
    site_compare_tests = pd.concat([first_seen_site_cmp, first_feeding_site_cmp], ignore_index=True)

    rec_df.to_csv(DATA_DIR / "utumbi_milimani_video_records.csv", index=False)
    first_seen_long.to_csv(DATA_DIR / "first_seen_species_long.csv", index=False)
    first_feeding_long.to_csv(DATA_DIR / "first_feeding_species_long.csv", index=False)
    first_seen_video_summary.to_csv(DATA_DIR / "first_seen_species_video_summary.csv", index=False)
    first_feeding_video_summary.to_csv(DATA_DIR / "first_feeding_species_video_summary.csv", index=False)
    site_bait_tests.to_csv(DATA_DIR / "site_bait_taxon_time_tests.csv", index=False)
    site_compare_tests.to_csv(DATA_DIR / "site_comparison_within_bait_taxon_time_tests.csv", index=False)

    write_report(
        first_seen_long=first_seen_long,
        first_feeding_long=first_feeding_long,
        site_bait_tests=site_bait_tests,
        site_compare_tests=site_compare_tests,
        first_seen_video_summary=first_seen_video_summary,
        first_feeding_video_summary=first_feeding_video_summary,
    )

    print("Erstellt:")
    print(OUT_DIR / "zeitvergleich_taxa_utumbi_milimani.md")
    print(DATA_DIR / "site_bait_taxon_time_tests.csv")
    print(DATA_DIR / "site_comparison_within_bait_taxon_time_tests.csv")


if __name__ == "__main__":
    main()
