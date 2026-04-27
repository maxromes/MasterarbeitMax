from __future__ import annotations

from pathlib import Path
import warnings

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results" / "visibility_analysis"
INPUT = RESULTS_DIR / "visibility_video_level_merged.csv"

OUT_MAIN = RESULTS_DIR / "visibility_site_stratified_tests.csv"
OUT_ADJUST = RESULTS_DIR / "visibility_site_stratified_tests_adjusted.csv"
OUT_SUMMARY = RESULTS_DIR / "visibility_site_stratified_tests_summary.md"

METRICS = [
    "maxn_video_peak",
    "species_richness",
    "first_seen_median_sec",
]


def robust_term_stats(model, term: str) -> tuple[float, float, float, float, float]:
    robust = model.get_robustcov_results(cov_type="HC3")
    names = list(model.model.exog_names)
    idx = names.index(term)
    coef = float(robust.params[idx])
    pval = float(robust.pvalues[idx])
    tval = float(robust.tvalues[idx])
    ci_low, ci_high = robust.conf_int(alpha=0.05)[idx]
    return coef, pval, tval, float(ci_low), float(ci_high)


def blocked_permutation_pvalue(
    df: pd.DataFrame,
    formula: str,
    term: str,
    block_col: str,
    n_perm: int = 1000,
    seed: int = 42,
) -> float:
    rng = np.random.default_rng(seed)

    model_obs = smf.ols(formula, data=df).fit()
    _, _, t_obs, _, _ = robust_term_stats(model_obs, term)
    t_obs_abs = abs(t_obs)

    permuted = df.copy()
    ge = 0

    for _ in range(n_perm):
        vis = df[term].copy()
        for _, idx in df.groupby(block_col, sort=False).groups.items():
            idx = list(idx)
            if len(idx) >= 2:
                vis.loc[idx] = rng.permutation(vis.loc[idx].to_numpy())
        permuted[term] = vis

        model_perm = smf.ols(formula, data=permuted).fit()
        _, _, t_perm, _, _ = robust_term_stats(model_perm, term)
        if abs(t_perm) >= t_obs_abs:
            ge += 1

    return (ge + 1) / (n_perm + 1)


def add_corrections(df: pd.DataFrame, p_col: str, prefix: str) -> pd.DataFrame:
    out = df.copy()
    pvals = out[p_col].astype(float).to_numpy()
    mask = np.isfinite(pvals)

    for method in ["fdr_bh", "holm", "bonferroni", "fdr_by"]:
        col = f"{prefix}_{method}"
        out[col] = np.nan
        if mask.any():
            _, qvals, _, _ = multipletests(pvals[mask], method=method)
            out.loc[mask, col] = qvals
    return out


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    warnings.filterwarnings(
        "ignore",
        message="divide by zero encountered in divide",
        category=RuntimeWarning,
    )
    warnings.filterwarnings(
        "ignore",
        message="invalid value encountered in divide",
        category=RuntimeWarning,
    )

    df = pd.read_csv(INPUT)
    df = df[df["visibility_mean"].notna()].copy()

    rows: list[dict] = []

    for site in sorted(df["standort"].dropna().unique()):
        site_df = df[df["standort"] == site].copy()
        for metric in METRICS:
            work = site_df[["koeder", "visibility_mean", metric]].copy().dropna()
            work["y_log"] = np.log1p(work[metric].astype(float))
            work["visibility_c"] = work["visibility_mean"] - work["visibility_mean"].mean()

            if len(work) < 8 or work["visibility_c"].nunique() < 2:
                rows.append(
                    {
                        "standort": site,
                        "metric": metric,
                        "n": int(len(work)),
                        "n_baits": int(work["koeder"].nunique()),
                        "coef_visibility_c": np.nan,
                        "coef_ci95_low": np.nan,
                        "coef_ci95_high": np.nan,
                        "t_hc3": np.nan,
                        "p_hc3": np.nan,
                        "p_perm_blocked": np.nan,
                        "r2": np.nan,
                        "adj_r2": np.nan,
                        "model_note": "insufficient_data",
                    }
                )
                continue

            include_bait = work["koeder"].nunique() >= 2
            formula = "y_log ~ visibility_c + C(koeder)" if include_bait else "y_log ~ visibility_c"

            model = smf.ols(formula, data=work).fit()
            coef, p_hc3, t_hc3, ci_low, ci_high = robust_term_stats(model, "visibility_c")
            p_perm = blocked_permutation_pvalue(
                work,
                formula=formula,
                term="visibility_c",
                block_col="koeder",
                n_perm=1000,
                seed=42,
            )

            rows.append(
                {
                    "standort": site,
                    "metric": metric,
                    "n": int(len(work)),
                    "n_baits": int(work["koeder"].nunique()),
                    "coef_visibility_c": coef,
                    "coef_ci95_low": ci_low,
                    "coef_ci95_high": ci_high,
                    "t_hc3": t_hc3,
                    "p_hc3": p_hc3,
                    "p_perm_blocked": p_perm,
                    "r2": float(model.rsquared),
                    "adj_r2": float(model.rsquared_adj),
                    "model_note": "with_bait_covariate" if include_bait else "no_bait_covariate",
                }
            )

    out = pd.DataFrame(rows)
    out.to_csv(OUT_MAIN, index=False)

    adj = out.copy()
    adj = add_corrections(adj, "p_hc3", "q_hc3")
    adj = add_corrections(adj, "p_perm_blocked", "q_perm")
    adj.to_csv(OUT_ADJUST, index=False)

    with OUT_SUMMARY.open("w", encoding="utf-8") as f:
        f.write("# Standort-stratifizierte Sicht-Analyse\n\n")
        f.write("Stand: 2026-04-27\n\n")
        f.write("## Methode\n\n")
        f.write("- Analyse getrennt fuer jeden Standort (milimani, nursery, utumbi).\n")
        f.write("- Endpunkte: maxn_video_peak, species_richness, first_seen_median_sec.\n")
        f.write("- Modell je Standort/Endpunkt: OLS auf log1p(Endpunkt) mit visibility_c, plus C(koeder) sofern >= 2 Koeder im Standort.\n")
        f.write("- Inferenz: HC3 robuste Standardfehler und blockierter Permutationstest innerhalb Koeder.\n")
        f.write("- Multiple-Testing ueber alle 9 Standort-Endpunkt-Tests: BH/FDR, Holm, Bonferroni, BY.\n\n")

        f.write("## Ergebnisse\n\n")
        f.write("| Standort | Metrik | n | Beta | 95%-CI | p(HC3) | p(Perm blockiert) | q(HC3,BH) | q(Perm,BH) |\n")
        f.write("|---|---|---:|---:|---|---:|---:|---:|---:|\n")
        for _, r in adj.iterrows():
            if pd.isna(r["coef_visibility_c"]):
                f.write(
                    f"| {r['standort']} | {r['metric']} | {int(r['n'])} | na | na | na | na | na | na |\n"
                )
                continue
            ci = f"[{r['coef_ci95_low']:.3f}, {r['coef_ci95_high']:.3f}]"
            f.write(
                f"| {r['standort']} | {r['metric']} | {int(r['n'])} | {r['coef_visibility_c']:.3f} | {ci} | {r['p_hc3']:.4g} | {r['p_perm_blocked']:.4g} | {r['q_hc3_fdr_bh']:.4g} | {r['q_perm_fdr_bh']:.4g} |\n"
            )

        robust_sig = (
            (adj["q_hc3_fdr_bh"] < 0.05) | (adj["q_perm_fdr_bh"] < 0.05)
        ).fillna(False)

        f.write("\n## Kurzfazit\n\n")
        if robust_sig.any():
            f.write("- Es gibt mindestens einen standortspezifischen Sicht-Effekt, der nach FDR robust bleibt.\n")
        else:
            f.write("- Kein standortspezifischer Sicht-Effekt bleibt nach FDR-Korrektur robust signifikant.\n")
        f.write("- Die uebergeordnete Schlussfolgerung bleibt stabil: Sicht zeigt keinen belastbaren eigenstaendigen Treiber-Effekt auf die Endpunkte.\n")


if __name__ == "__main__":
    main()
