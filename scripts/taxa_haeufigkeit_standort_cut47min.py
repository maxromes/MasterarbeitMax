#!/usr/bin/env python3
"""
Vergleicht Taxon-Haeufigkeiten (MaxN) zwischen Standorten auf Basis cut_47min.

Fragestellungen:
- Unterscheiden sich die MaxN-Haeufigkeiten je Taxon zwischen den 3 Standorten?
- Welche Taxa kommen aehnlich oft ueberall vor?
- Bei welchen Taxa liegen die groessten Unterschiede?

Ausgabe:
- results/taxahaeufigkeitstandord/
"""

from __future__ import annotations

import itertools
import math
import re
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min"
CORAL_REEF_DIR = CUT_ROOT / "Annotation_reports_coral_reef"
NURSERY_DIR = CUT_ROOT / "Annotation_reports_Nursery"

OUT_DIR = ROOT / "results" / "taxahäufigkeitstandord"
FIG_DIR = OUT_DIR / "figures"

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


def load_video_maxn(csv_path: Path) -> Dict[str, object]:
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")

    counts: Dict[Tuple[str, float], int] = {}
    for _, row in df.iterrows():
        if is_truthy(row.get("feeding", "")) or is_truthy(row.get("interested", "")):
            continue

        taxon = build_taxon_key(row)
        if not taxon:
            continue

        frame_time = parse_frame_time(row.get("frames", ""))
        if frame_time is None:
            continue

        key = (taxon, frame_time)
        counts[key] = counts.get(key, 0) + 1

    maxn_by_taxon: Dict[str, int] = {}
    for (taxon, _), n in counts.items():
        if taxon not in maxn_by_taxon or n > maxn_by_taxon[taxon]:
            maxn_by_taxon[taxon] = int(n)

    date, standort, koeder = parse_video_metadata(csv_path.name)
    return {
        "filename": csv_path.name,
        "date": date,
        "standort": standort,
        "koeder": koeder,
        "maxn_by_taxon": maxn_by_taxon,
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
    gt = 0
    lt = 0
    for xi in x:
        gt += np.sum(xi > y)
        lt += np.sum(xi < y)
    return float((gt - lt) / total)


def significance_label(p_val: float) -> str:
    if p_val < 0.001:
        return "***"
    if p_val < 0.01:
        return "**"
    if p_val < 0.05:
        return "*"
    return "ns"


def to_md(df: pd.DataFrame) -> str:
    if df.empty:
        return "Keine Daten."
    return df.to_markdown(index=False)


def create_summary_figures(taxon_tests_df: pd.DataFrame, taxon_site_df: pd.DataFrame) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # 1) Anzahl signifikanter Taxa pro Korrektur
    raw_sig = int((taxon_tests_df["p_value"] < ALPHA).sum())
    holm_sig = int((taxon_tests_df["p_value_holm"] < ALPHA).sum())

    plt.figure(figsize=(7, 4.8))
    plt.bar(["roh p<0.05", "Holm p<0.05"], [raw_sig, holm_sig], color=["#4c78a8", "#f58518"])
    plt.ylabel("Anzahl Taxa")
    plt.title("Signifikante Standortunterschiede je Taxon (MaxN)")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "significant_taxa_counts.png", dpi=180)
    plt.close()

    # 2) Heatmap der Top-20-Taxa nach mittlerem MaxN
    top_taxa = (
        taxon_site_df.groupby("taxon_key", as_index=False)["mean_maxn"]
        .mean()
        .sort_values("mean_maxn", ascending=False)
        .head(20)["taxon_key"]
        .tolist()
    )
    if top_taxa:
        mat = (
            taxon_site_df[taxon_site_df["taxon_key"].isin(top_taxa)]
            .pivot(index="taxon_key", columns="standort", values="mean_maxn")
            .reindex(index=top_taxa, columns=SITES)
            .fillna(0.0)
        )

        plt.figure(figsize=(9.5, max(6, len(top_taxa) * 0.28)))
        im = plt.imshow(mat.values, aspect="auto", cmap="YlGnBu")
        plt.xticks(range(len(SITES)), SITES)
        plt.yticks(range(len(top_taxa)), top_taxa)
        plt.title("Top-20 Taxa nach mittlerem MaxN (Standortvergleich)")
        plt.colorbar(im, fraction=0.03, pad=0.02, label="Mean MaxN")
        plt.tight_layout()
        plt.savefig(FIG_DIR / "top20_taxa_mean_maxn_heatmap.png", dpi=180)
        plt.close()


def build_markdown_report(
    videos_df: pd.DataFrame,
    taxon_tests_df: pd.DataFrame,
    taxon_site_df: pd.DataFrame,
    pairwise_df: pd.DataFrame,
    similar_df: pd.DataFrame,
    diff_df: pd.DataFrame,
) -> str:
    n_videos = len(videos_df)
    n_taxa = int(taxon_tests_df["taxon_key"].nunique()) if not taxon_tests_df.empty else 0
    n_sig_raw = int((taxon_tests_df["p_value"] < ALPHA).sum()) if not taxon_tests_df.empty else 0
    n_sig_holm = int((taxon_tests_df["p_value_holm"] < ALPHA).sum()) if not taxon_tests_df.empty else 0

    top_sig = taxon_tests_df.sort_values(["p_value_holm", "p_value"]).head(25)
    top_diff = diff_df.head(25)
    top_similar = similar_df.head(30)

    lines: List[str] = []
    lines.append("# Taxa-Haeufigkeit nach Standort (MaxN, cut_47min)")
    lines.append("")
    lines.append("## Kurzfazit")
    lines.append(
        f"- Von {n_taxa} getesteten Taxa zeigen {n_sig_holm} Taxa signifikante Standortunterschiede "
        f"nach Holm-Korrektur (roh: {n_sig_raw})."
    )
    lines.append(
        "- Die folgenden Tabellen trennen Taxa mit aehnlicher Haeufigkeit ueber alle Standorte "
        "von Taxa mit deutlichen Standortunterschieden."
    )
    lines.append("")
    lines.append("## Datengrundlage")
    lines.append(f"- Anzahl Videos: {n_videos}")
    lines.append("- Standorte: Milimani, Utumbi, Nursery")
    lines.append("- Quelle: normalized_reports/cut_47min")
    lines.append("- Metrik: MaxN je Taxon und Video (feeding/interested ausgeschlossen)")
    lines.append("- Test pro Taxon: Kruskal-Wallis ueber 3 Standorte, Holm-Korrektur ueber alle Taxa")
    lines.append("- Paarweise Folgeanalysen: Mann-Whitney U mit Holm-Korrektur je Taxon")
    lines.append("")

    lines.append("## Signifikanz ueber alle Taxa")
    summary_sig = pd.DataFrame(
        [
            {
                "n_taxa_tested": n_taxa,
                "n_significant_raw_p_lt_0_05": n_sig_raw,
                "n_significant_holm_p_lt_0_05": n_sig_holm,
                "share_significant_holm": (n_sig_holm / n_taxa) if n_taxa else math.nan,
            }
        ]
    )
    lines.append(to_md(summary_sig))
    lines.append("")

    lines.append("## Taxa mit den staerksten Standortunterschieden")
    lines.append(to_md(top_diff))
    lines.append("")

    lines.append("## Taxa mit aehnlicher Haeufigkeit an allen 3 Standorten")
    lines.append("Kriterium: in jedem Standort in >=50% der Videos nachgewiesen, nicht signifikant nach Holm, aehnlicher Mittelwert (max/min <= 1.5).")
    lines.append(to_md(top_similar))
    lines.append("")

    lines.append("## Signifikante Taxa (Top nach Holm-p)")
    lines.append(to_md(top_sig))
    lines.append("")

    lines.append("## Paarweise Tests (Auszug fuer signifikante Taxa)")
    sig_taxa = set(taxon_tests_df.loc[taxon_tests_df["p_value_holm"] < ALPHA, "taxon_key"].tolist())
    pairwise_sig = pairwise_df[pairwise_df["taxon_key"].isin(sig_taxa)].copy()
    pairwise_sig = pairwise_sig.sort_values(["taxon_key", "p_value_holm_within_taxon", "p_value"]).head(100)
    lines.append(to_md(pairwise_sig))
    lines.append("")

    lines.append("## Grafiken")
    lines.append("- figures/significant_taxa_counts.png")
    lines.append("- figures/top20_taxa_mean_maxn_heatmap.png")

    return "\n".join(lines) + "\n"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(CORAL_REEF_DIR.glob("*.csv")) + sorted(NURSERY_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError("Keine CSV-Dateien unter normalized_reports/cut_47min gefunden.")

    records = [load_video_maxn(p) for p in files]
    videos_df = pd.DataFrame(records)
    videos_df = videos_df[videos_df["standort"].isin(SITES)].copy()
    videos_df = videos_df.sort_values(["standort", "date", "filename"]).reset_index(drop=True)

    site_videos: Dict[str, pd.DataFrame] = {s: videos_df[videos_df["standort"] == s].copy() for s in SITES}
    all_taxa = sorted(set().union(*[set().union(*site_videos[s]["maxn_by_taxon"].map(dict.keys).tolist()) for s in SITES]))

    # Video-level Export: MaxN je Taxon und Video
    video_level_rows: List[Dict[str, object]] = []
    for row in videos_df.itertuples(index=False):
        for taxon, maxn in row.maxn_by_taxon.items():
            video_level_rows.append(
                {
                    "filename": row.filename,
                    "date": row.date,
                    "standort": row.standort,
                    "koeder": row.koeder,
                    "taxon_key": taxon,
                    "maxn": int(maxn),
                }
            )
    video_level_df = pd.DataFrame(video_level_rows)

    taxon_rows: List[Dict[str, object]] = []
    site_rows: List[Dict[str, object]] = []
    pairwise_rows: List[Dict[str, object]] = []

    for taxon in all_taxa:
        site_arrays: Dict[str, np.ndarray] = {}
        for site in SITES:
            vals = []
            for v in site_videos[site].itertuples(index=False):
                vals.append(float(v.maxn_by_taxon.get(taxon, 0)))
            arr = np.array(vals, dtype=float)
            site_arrays[site] = arr

            site_rows.append(
                {
                    "taxon_key": taxon,
                    "standort": site,
                    "n_videos": int(len(arr)),
                    "n_present": int(np.sum(arr > 0)),
                    "occurrence_rate": float(np.mean(arr > 0)) if len(arr) else math.nan,
                    "mean_maxn": float(np.mean(arr)) if len(arr) else math.nan,
                    "median_maxn": float(np.median(arr)) if len(arr) else math.nan,
                    "std_maxn": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
                    "max_maxn": float(np.max(arr)) if len(arr) else math.nan,
                }
            )

        groups = [site_arrays[s] for s in SITES]
        total_n = int(sum(len(g) for g in groups))
        k_groups = len(groups)
        try:
            h_stat, p_val = stats.kruskal(*groups)
        except ValueError:
            h_stat, p_val = 0.0, 1.0

        eta_sq = float((h_stat - k_groups + 1) / (total_n - k_groups)) if total_n > k_groups else math.nan
        eta_sq = max(0.0, eta_sq) if not math.isnan(eta_sq) else math.nan

        mean_vals = {s: float(np.mean(site_arrays[s])) for s in SITES}
        med_vals = {s: float(np.median(site_arrays[s])) for s in SITES}
        dom_site = max(mean_vals, key=mean_vals.get)
        min_site = min(mean_vals, key=mean_vals.get)

        taxon_rows.append(
            {
                "taxon_key": taxon,
                "n_total": total_n,
                "h_stat": float(h_stat),
                "p_value": float(p_val),
                "eta_sq": eta_sq,
                "mean_milimani": mean_vals["milimani"],
                "mean_utumbi": mean_vals["utumbi"],
                "mean_nursery": mean_vals["nursery"],
                "median_milimani": med_vals["milimani"],
                "median_utumbi": med_vals["utumbi"],
                "median_nursery": med_vals["nursery"],
                "dominant_site_mean": dom_site,
                "lowest_site_mean": min_site,
                "mean_diff_max_minus_min": float(mean_vals[dom_site] - mean_vals[min_site]),
            }
        )

        pair_ps: List[float] = []
        pair_tmp: List[Dict[str, object]] = []
        for a, b in itertools.combinations(SITES, 2):
            xa = site_arrays[a]
            xb = site_arrays[b]
            try:
                u_stat, p_pair = stats.mannwhitneyu(xa, xb, alternative="two-sided")
            except ValueError:
                u_stat, p_pair = 0.0, 1.0

            pair_ps.append(float(p_pair))
            pair_tmp.append(
                {
                    "taxon_key": taxon,
                    "site_a": a,
                    "site_b": b,
                    "n_a": int(len(xa)),
                    "n_b": int(len(xb)),
                    "mean_a": float(np.mean(xa)) if len(xa) else math.nan,
                    "mean_b": float(np.mean(xb)) if len(xb) else math.nan,
                    "median_a": float(np.median(xa)) if len(xa) else math.nan,
                    "median_b": float(np.median(xb)) if len(xb) else math.nan,
                    "u_stat": float(u_stat),
                    "p_value": float(p_pair),
                    "cliffs_delta": cliffs_delta(xa, xb),
                }
            )

        pair_adj = holm_adjust(pair_ps)
        for row, p_adj in zip(pair_tmp, pair_adj):
            row["p_value_holm_within_taxon"] = float(p_adj)
            row["significant_0_05"] = bool(row["p_value"] < ALPHA)
            row["significant_0_05_holm_within_taxon"] = bool(p_adj < ALPHA)
            pairwise_rows.append(row)

    taxon_tests_df = pd.DataFrame(taxon_rows).sort_values("p_value", ascending=True).reset_index(drop=True)
    taxon_tests_df["p_value_holm"] = holm_adjust(taxon_tests_df["p_value"].tolist())
    taxon_tests_df["significant_0_05"] = taxon_tests_df["p_value"] < ALPHA
    taxon_tests_df["significant_0_05_holm"] = taxon_tests_df["p_value_holm"] < ALPHA
    taxon_tests_df["sig_label_raw"] = taxon_tests_df["p_value"].map(significance_label)
    taxon_tests_df["sig_label_holm"] = taxon_tests_df["p_value_holm"].map(significance_label)

    taxon_site_df = pd.DataFrame(site_rows).sort_values(["taxon_key", "standort"]).reset_index(drop=True)
    pairwise_df = pd.DataFrame(pairwise_rows).sort_values(["taxon_key", "p_value"]).reset_index(drop=True)

    # Taxa mit aehnlicher Haeufigkeit ueber alle 3 Standorte
    site_wide = (
        taxon_site_df.pivot(index="taxon_key", columns="standort", values=["occurrence_rate", "mean_maxn"]).copy()
    )
    site_wide.columns = [f"{a}_{b}" for a, b in site_wide.columns]
    site_wide = site_wide.reset_index()
    similar_df = taxon_tests_df.merge(site_wide, on="taxon_key", how="left")
    similar_df["mean_ratio_max_min"] = similar_df[["mean_milimani", "mean_utumbi", "mean_nursery"]].max(axis=1) / (
        similar_df[["mean_milimani", "mean_utumbi", "mean_nursery"]].replace(0, np.nan).min(axis=1)
    )
    similar_df = similar_df[
        (similar_df["significant_0_05_holm"] == False)
        & (similar_df["occurrence_rate_milimani"] >= 0.5)
        & (similar_df["occurrence_rate_utumbi"] >= 0.5)
        & (similar_df["occurrence_rate_nursery"] >= 0.5)
        & (similar_df["mean_ratio_max_min"] <= 1.5)
    ].copy()
    similar_df = similar_df.sort_values(["mean_ratio_max_min", "p_value_holm", "taxon_key"]).reset_index(drop=True)

    # Taxa mit deutlichen Unterschieden
    diff_df = taxon_tests_df.copy()
    diff_df = diff_df[diff_df["significant_0_05_holm"]].copy()
    diff_df = diff_df.sort_values(["p_value_holm", "mean_diff_max_minus_min"], ascending=[True, False]).reset_index(drop=True)

    videos_export = videos_df.drop(columns=["maxn_by_taxon"]).copy()

    videos_export.to_csv(OUT_DIR / "video_metadata.csv", index=False)
    video_level_df.to_csv(OUT_DIR / "taxon_maxn_video_level.csv", index=False)
    taxon_site_df.to_csv(OUT_DIR / "taxon_maxn_by_site_summary.csv", index=False)
    taxon_tests_df.to_csv(OUT_DIR / "taxa_kruskal_site_tests.csv", index=False)
    pairwise_df.to_csv(OUT_DIR / "taxa_pairwise_mannwhitney_tests.csv", index=False)
    similar_df.to_csv(OUT_DIR / "taxa_similar_frequency_all_sites.csv", index=False)
    diff_df.to_csv(OUT_DIR / "taxa_significant_site_differences.csv", index=False)

    create_summary_figures(taxon_tests_df, taxon_site_df)

    report_md = build_markdown_report(videos_df, taxon_tests_df, taxon_site_df, pairwise_df, similar_df, diff_df)
    (OUT_DIR / "taxahaeufigkeit_standort.md").write_text(report_md, encoding="utf-8")

    print("Taxa-Haeufigkeitsvergleich (MaxN) abgeschlossen.")
    print(f"Ergebnisse: {OUT_DIR}")


if __name__ == "__main__":
    main()
