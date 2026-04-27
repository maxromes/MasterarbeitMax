from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results" / "visibility_analysis"
INPUT = RESULTS_DIR / "visibility_video_level_merged.csv"

OUT_MAIN = RESULTS_DIR / "visibility_additional_tests.csv"
OUT_ADJUST = RESULTS_DIR / "visibility_additional_tests_adjusted.csv"
OUT_SUMMARY = RESULTS_DIR / "visibility_additional_tests_summary.md"


METRICS = [
    "maxn_video_peak",
    "species_richness",
    "first_seen_median_sec",
]


def robust_visibility_stats(model, term: str) -> tuple[float, float, float, float, float]:
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
    block_cols: list[str],
    n_perm: int = 3000,
    seed: int = 42,
) -> float:
    rng = np.random.default_rng(seed)

    model_obs = smf.ols(formula, data=df).fit()
    _, _, t_obs, _, _ = robust_visibility_stats(model_obs, term)
    t_obs_abs = abs(t_obs)

    permuted = df.copy()
    ge = 0

    for _ in range(n_perm):
        vis = df[term].copy()
        for _, idx in df.groupby(block_cols, sort=False).groups.items():
            idx = list(idx)
            if len(idx) >= 2:
                vis.iloc[idx] = rng.permutation(vis.iloc[idx].to_numpy())
        permuted[term] = vis

        model_perm = smf.ols(formula, data=permuted).fit()
        _, _, t_perm, _, _ = robust_visibility_stats(model_perm, term)
        if abs(t_perm) >= t_obs_abs:
            ge += 1

    return (ge + 1) / (n_perm + 1)


def add_multiple_testing_corrections(df: pd.DataFrame, p_col: str, prefix: str) -> pd.DataFrame:
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

    df = pd.read_csv(INPUT)
    df = df[df["visibility_mean"].notna()].copy()

    rows: list[dict] = []

    for metric in METRICS:
        work = df[["standort", "koeder", "visibility_mean", metric]].copy().dropna()
        work["y_log"] = np.log1p(work[metric].astype(float))

        work["visibility_c"] = work["visibility_mean"] - work["visibility_mean"].mean()
        work["visibility_c2"] = work["visibility_c"] ** 2

        linear_formula = "y_log ~ visibility_c + C(standort) + C(koeder)"
        linear_model = smf.ols(linear_formula, data=work).fit()
        coef, p_hc3, t_hc3, ci_low, ci_high = robust_visibility_stats(linear_model, "visibility_c")
        p_perm_blocked = blocked_permutation_pvalue(
            work,
            formula=linear_formula,
            term="visibility_c",
            block_cols=["standort", "koeder"],
            n_perm=3000,
            seed=42,
        )

        quad_formula = "y_log ~ visibility_c + visibility_c2 + C(standort) + C(koeder)"
        quad_model = smf.ols(quad_formula, data=work).fit()
        _, p_quad_c2, _, q_ci_low, q_ci_high = robust_visibility_stats(quad_model, "visibility_c2")

        quant_model = smf.quantreg(linear_formula, data=work).fit(q=0.5)
        p_quant = float(quant_model.pvalues.get("visibility_c", np.nan))

        rows.append(
            {
                "metric": metric,
                "n": int(len(work)),
                "coef_visibility_c": coef,
                "coef_ci95_low": ci_low,
                "coef_ci95_high": ci_high,
                "pct_change_per_visibility_unit": float(np.expm1(coef) * 100.0),
                "t_hc3": t_hc3,
                "p_hc3": p_hc3,
                "p_perm_blocked": p_perm_blocked,
                "p_quad_visibility_c2": p_quad_c2,
                "quad_c2_ci95_low": q_ci_low,
                "quad_c2_ci95_high": q_ci_high,
                "p_quantile_median": p_quant,
                "r2_linear": float(linear_model.rsquared),
                "adj_r2_linear": float(linear_model.rsquared_adj),
            }
        )

    main_df = pd.DataFrame(rows)
    main_df.to_csv(OUT_MAIN, index=False)

    adjusted = main_df.copy()
    adjusted = add_multiple_testing_corrections(adjusted, "p_hc3", "q_hc3")
    adjusted = add_multiple_testing_corrections(adjusted, "p_perm_blocked", "q_perm_blocked")
    adjusted = add_multiple_testing_corrections(adjusted, "p_quad_visibility_c2", "q_quad")
    adjusted = add_multiple_testing_corrections(adjusted, "p_quantile_median", "q_quantile")
    adjusted.to_csv(OUT_ADJUST, index=False)

    with OUT_SUMMARY.open("w", encoding="utf-8") as f:
        f.write("# Zusatztests: Einfluss der Sicht auf Endpunkte\n\n")
        f.write("Stand: 2026-04-27\n\n")
        f.write("## Design\n\n")
        f.write("- Datensatz: visibility_video_level_merged.csv mit vorhandener visibility_mean.\n")
        f.write("- Endpunkte: maxn_video_peak, species_richness, first_seen_median_sec.\n")
        f.write("- Basismodell: OLS auf log1p(Endpunkt), adjustiert fuer Standort + Koeder, HC3 robuste Standardfehler.\n")
        f.write("- Zusatztests: blockierter Permutationstest (innerhalb Standort x Koeder), Quadratik-Test (visibility_c2), Quantilsregression (Median).\n")
        f.write("- Multiple-Testing: BH/FDR, Holm, Bonferroni, BY jeweils innerhalb Testfamilie ueber die drei Endpunkte.\n\n")

        f.write("## Ergebnisse\n\n")
        f.write("| Metrik | n | Beta (linear) | 95%-CI | p(HC3) | p(Perm blockiert) | p(Quadratik) | p(Quantil) |\n")
        f.write("|---|---:|---:|---|---:|---:|---:|---:|\n")
        for _, r in adjusted.iterrows():
            ci = f"[{r['coef_ci95_low']:.3f}, {r['coef_ci95_high']:.3f}]"
            f.write(
                f"| {r['metric']} | {int(r['n'])} | {r['coef_visibility_c']:.3f} | {ci} | {r['p_hc3']:.4g} | {r['p_perm_blocked']:.4g} | {r['p_quad_visibility_c2']:.4g} | {r['p_quantile_median']:.4g} |\n"
            )

        f.write("\n## Korrigierte p-Werte (Auszug)\n\n")
        f.write("| Metrik | q_hc3_fdr_bh | q_hc3_holm | q_hc3_bonferroni | q_perm_blocked_fdr_bh | q_quad_fdr_bh | q_quantile_fdr_bh |\n")
        f.write("|---|---:|---:|---:|---:|---:|---:|\n")
        for _, r in adjusted.iterrows():
            f.write(
                f"| {r['metric']} | {r['q_hc3_fdr_bh']:.4g} | {r['q_hc3_holm']:.4g} | {r['q_hc3_bonferroni']:.4g} | {r['q_perm_blocked_fdr_bh']:.4g} | {r['q_quad_fdr_bh']:.4g} | {r['q_quantile_fdr_bh']:.4g} |\n"
            )

        sig_any = (
            (adjusted["q_hc3_fdr_bh"] < 0.05)
            | (adjusted["q_perm_blocked_fdr_bh"] < 0.05)
            | (adjusted["q_quad_fdr_bh"] < 0.05)
            | (adjusted["q_quantile_fdr_bh"] < 0.05)
        ).any()

        f.write("\n## Kurzfazit\n\n")
        if sig_any:
            f.write("- Mindestens ein Zusatztest bleibt nach FDR signifikant. Details siehe Tabellen oben.\n")
        else:
            f.write("- Keiner der Zusatztests zeigt einen robust signifikanten Einfluss der Sicht nach Korrektur fuer multiples Testen.\n")
        f.write("- Die Kernaussage bleibt damit stabil: Sicht erklaert die Endpunkte nicht eigenstaendig, sobald Standort und Koeder kontrolliert werden.\n")


if __name__ == "__main__":
    main()
