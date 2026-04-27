from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import kendalltau, pearsonr, spearmanr


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results" / "visibility_analysis"
BASE_MERGED = RESULTS_DIR / "visibility_video_level_merged.csv"
EXCEL_PATH = ROOT / "Zeitplan-Aktuell-CNR4PQP(Automatisch wiederhergestellt).xlsx"

OUT_MERGED = RESULTS_DIR / "visibility_video_level_merged.csv"
OUT_MISSING = RESULTS_DIR / "visibility_missing_videos.csv"
OUT_COVERAGE = RESULTS_DIR / "visibility_coverage_by_site_bait.csv"
OUT_CORR = RESULTS_DIR / "visibility_vs_metrics_correlations.csv"


SITE_MAP = {
    "chole nursery": "nursery",
    "nursery": "nursery",
    "milimani": "milimani",
    "utumbi": "utumbi",
}

BAIT_MAP = {
    "makerel": "mackerel",
    "mackerel": "mackerel",
    "meersalat": "ulva_salad",
    "ulva salad": "ulva_salad",
    "ulva_salad": "ulva_salad",
    "glasnudel": "ulva_gutweed",
    "ulva gutweed": "ulva_gutweed",
    "ulva_gutweed": "ulva_gutweed",
    "control": "control",
    "sargassum": "sargassum",
    "algae strings": "algae_strings",
    "algae_strings": "algae_strings",
    "algae mix": "algaemix",
    "algaemix": "algaemix",
    "fisch mix": "fischmix",
    "fischmix": "fischmix",
}


def bh_adjust(pvals: pd.Series) -> pd.Series:
    vals = pvals.astype(float).to_numpy()
    mask = np.isfinite(vals)
    out = np.full(vals.shape, np.nan, dtype=float)
    if not mask.any():
        return pd.Series(out, index=pvals.index)

    valid = vals[mask]
    m = len(valid)
    order = np.argsort(valid)
    ranked = valid[order]
    q = ranked * m / (np.arange(m) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.clip(q, 0.0, 1.0)

    q_unsorted = np.empty_like(q)
    q_unsorted[order] = q
    out[np.where(mask)[0]] = q_unsorted
    return pd.Series(out, index=pvals.index)


def norm_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip().lower()


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    base = pd.read_csv(BASE_MERGED)
    base = base[
        [
            "filename",
            "date",
            "standort",
            "koeder",
            "species_richness",
            "maxn_video_peak",
            "first_seen_median_sec",
        ]
    ].copy()
    base["date"] = base["date"].astype(str).str.strip()

    plan = pd.read_excel(EXCEL_PATH)
    plan = plan.rename(columns={"Unnamed: 0": "date_raw", "Bait": "bait_raw", "Visability": "visibility_raw"})

    plan["date"] = pd.to_datetime(plan["date_raw"], errors="coerce").dt.strftime("%Y%m%d")
    plan["standort"] = plan["site"].map(lambda x: SITE_MAP.get(norm_text(x), norm_text(x)))
    plan["koeder"] = plan["bait_raw"].map(lambda x: BAIT_MAP.get(norm_text(x), norm_text(x)))
    plan["visibility"] = pd.to_numeric(
        plan["visibility_raw"].astype(str).str.replace(",", ".", regex=False), errors="coerce"
    )

    vis_agg = (
        plan.groupby(["date", "standort", "koeder"], dropna=False)
        .agg(
            visibility_min=("visibility", "min"),
            visibility_max=("visibility", "max"),
            visibility_mean=("visibility", "mean"),
            n_plan_rows=("visibility", "size"),
            n_plan_vis_nonnull=("visibility", lambda s: int(s.notna().sum())),
        )
        .reset_index()
    )

    merged = base.merge(vis_agg, on=["date", "standort", "koeder"], how="left")
    merged = merged.sort_values(["date", "standort", "koeder"]).reset_index(drop=True)
    merged.to_csv(OUT_MERGED, index=False)

    missing = merged.loc[merged["visibility_mean"].isna(), ["filename", "date", "standort", "koeder"]].copy()
    missing.to_csv(OUT_MISSING, index=False)

    coverage = (
        merged.groupby(["standort", "koeder"], dropna=False)
        .agg(n_videos=("filename", "size"), n_vis=("visibility_mean", lambda s: int(s.notna().sum())))
        .reset_index()
        .sort_values(["standort", "koeder"])
    )
    coverage.to_csv(OUT_COVERAGE, index=False)

    corr_rows = []
    analysis = merged.loc[merged["visibility_mean"].notna()].copy()
    for metric in ["maxn_video_peak", "species_richness", "first_seen_median_sec"]:
        x = pd.to_numeric(analysis["visibility_mean"], errors="coerce")
        y = pd.to_numeric(analysis[metric], errors="coerce")
        pair = pd.DataFrame({"x": x, "y": y}).dropna()

        if len(pair) >= 3:
            sp = spearmanr(pair["x"], pair["y"])
            kt = kendalltau(pair["x"], pair["y"])
            pr = pearsonr(pair["x"], pair["y"])
            corr_rows.append(
                {
                    "metric": metric,
                    "n": int(len(pair)),
                    "spearman_rho": float(sp.statistic),
                    "spearman_p": float(sp.pvalue),
                    "kendall_tau": float(kt.statistic),
                    "kendall_p": float(kt.pvalue),
                    "pearson_r": float(pr.statistic),
                    "pearson_p": float(pr.pvalue),
                }
            )
        else:
            corr_rows.append(
                {
                    "metric": metric,
                    "n": int(len(pair)),
                    "spearman_rho": np.nan,
                    "spearman_p": np.nan,
                    "kendall_tau": np.nan,
                    "kendall_p": np.nan,
                    "pearson_r": np.nan,
                    "pearson_p": np.nan,
                }
            )

    corr = pd.DataFrame(corr_rows)
    corr["spearman_q_bh"] = bh_adjust(corr["spearman_p"])
    corr.to_csv(OUT_CORR, index=False)


if __name__ == "__main__":
    main()
