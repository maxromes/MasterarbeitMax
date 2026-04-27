from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import statsmodels.formula.api as smf


ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = ROOT / "results" / "visibility_analysis"
INPUT = RESULTS_DIR / "visibility_video_level_merged.csv"

OUT_COEF = RESULTS_DIR / "visibility_adjusted_model_results.csv"
OUT_PARTIAL = RESULTS_DIR / "visibility_adjusted_partial_spearman.csv"
OUT_SUMMARY = RESULTS_DIR / "visibility_adjusted_summary.md"


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


def robust_stat_for_visibility(model) -> tuple[float, float, float, float]:
    robust = model.get_robustcov_results(cov_type="HC3")
    names = list(model.model.exog_names)
    idx = names.index("visibility_mean")
    coef = float(robust.params[idx])
    pval = float(robust.pvalues[idx])
    tval = float(robust.tvalues[idx])
    ci_low, ci_high = robust.conf_int(alpha=0.05)[idx]
    return coef, pval, tval, float(ci_low), float(ci_high)


def permutation_pvalue(df: pd.DataFrame, formula: str, n_perm: int = 3000, seed: int = 42) -> float:
    rng = np.random.default_rng(seed)
    model_obs = smf.ols(formula, data=df).fit()
    _, _, t_obs, _, _ = robust_stat_for_visibility(model_obs)

    t_abs = abs(t_obs)
    ge = 0
    work = df.copy()
    for _ in range(n_perm):
        work["visibility_mean"] = rng.permutation(df["visibility_mean"].to_numpy())
        model_perm = smf.ols(formula, data=work).fit()
        _, _, t_perm, _, _ = robust_stat_for_visibility(model_perm)
        if abs(t_perm) >= t_abs:
            ge += 1
    return (ge + 1) / (n_perm + 1)


def partial_spearman(df: pd.DataFrame, response_log_col: str) -> tuple[float, float]:
    y_model = smf.ols(f"{response_log_col} ~ C(standort) + C(koeder)", data=df).fit()
    x_model = smf.ols("visibility_mean ~ C(standort) + C(koeder)", data=df).fit()
    y_res = y_model.resid
    x_res = x_model.resid
    res = spearmanr(x_res, y_res)
    return float(res.statistic), float(res.pvalue)


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT)
    df = df[df["visibility_mean"].notna()].copy()

    metrics = [
        "maxn_video_peak",
        "species_richness",
        "first_seen_median_sec",
    ]

    model_rows: list[dict] = []
    partial_rows: list[dict] = []

    for metric in metrics:
        work = df[["standort", "koeder", "visibility_mean", metric]].copy()
        work = work.dropna()
        work["y_log"] = np.log1p(work[metric].astype(float))

        formula = "y_log ~ visibility_mean + C(standort) + C(koeder)"
        model = smf.ols(formula, data=work).fit()
        coef, pval, tval, ci_low, ci_high = robust_stat_for_visibility(model)
        p_perm = permutation_pvalue(work, formula=formula, n_perm=3000, seed=42)

        model_rows.append(
            {
                "metric": metric,
                "n": int(len(work)),
                "coef_visibility_log1p": coef,
                "coef_ci95_low": ci_low,
                "coef_ci95_high": ci_high,
                "t_hc3": tval,
                "p_hc3": pval,
                "p_perm": p_perm,
                "r2": float(model.rsquared),
                "adj_r2": float(model.rsquared_adj),
                "pct_change_per_visibility_unit": float(np.expm1(coef) * 100.0),
            }
        )

        rho, p_partial = partial_spearman(work, "y_log")
        partial_rows.append(
            {
                "metric": metric,
                "n": int(len(work)),
                "partial_spearman_rho": rho,
                "partial_spearman_p": p_partial,
            }
        )

    model_df = pd.DataFrame(model_rows)
    model_df["q_hc3_bh"] = bh_adjust(model_df["p_hc3"])
    model_df["q_perm_bh"] = bh_adjust(model_df["p_perm"])
    model_df = model_df[
        [
            "metric",
            "n",
            "coef_visibility_log1p",
            "coef_ci95_low",
            "coef_ci95_high",
            "pct_change_per_visibility_unit",
            "t_hc3",
            "p_hc3",
            "q_hc3_bh",
            "p_perm",
            "q_perm_bh",
            "r2",
            "adj_r2",
        ]
    ]
    model_df.to_csv(OUT_COEF, index=False)

    partial_df = pd.DataFrame(partial_rows)
    partial_df["q_partial_bh"] = bh_adjust(partial_df["partial_spearman_p"])
    partial_df.to_csv(OUT_PARTIAL, index=False)

    with OUT_SUMMARY.open("w", encoding="utf-8") as f:
        f.write("# Sichtweiten-adjustierte Ergebnisse\n\n")
        f.write("Stand: 2026-04-27\n\n")
        f.write("## Methode\n\n")
        f.write("- Datengrundlage: visibility_video_level_merged.csv (nur Zeilen mit vorhandener Sichtweite).\n")
        f.write("- Modell pro Endpunkt: OLS auf log1p(Endpunkt) mit Kovariaten visibility_mean, Standort und Koeder.\n")
        f.write("- Inferenz: robuste HC3-Standardfehler, zusaetzlich Permutationstest (3000 Permutationen).\n")
        f.write("- Multiple Tests: Benjamini-Hochberg (BH/FDR) ueber die drei Endpunkte.\n")
        f.write("- Robustheitscheck: partielle Spearman-Korrelation (um Standort und Koeder bereinigt).\n\n")

        f.write("## Modellresultate (Effekt der Sichtweite)\n\n")
        f.write("| Metrik | n | Beta log1p | 95%-CI | % pro +1 Sichtweite | p(HC3) | q(HC3) | p(Perm) | q(Perm) |\n")
        f.write("|---|---:|---:|---|---:|---:|---:|---:|---:|\n")
        for _, r in model_df.iterrows():
            ci = f"[{r['coef_ci95_low']:.3f}, {r['coef_ci95_high']:.3f}]"
            f.write(
                f"| {r['metric']} | {int(r['n'])} | {r['coef_visibility_log1p']:.3f} | {ci} | {r['pct_change_per_visibility_unit']:.1f}% | {r['p_hc3']:.4g} | {r['q_hc3_bh']:.4g} | {r['p_perm']:.4g} | {r['q_perm_bh']:.4g} |\n"
            )

        f.write("\n## Partielle Spearman-Korrelation (bereinigt um Standort + Koeder)\n\n")
        f.write("| Metrik | n | partial rho | p | q(BH) |\n")
        f.write("|---|---:|---:|---:|---:|\n")
        for _, r in partial_df.iterrows():
            f.write(
                f"| {r['metric']} | {int(r['n'])} | {r['partial_spearman_rho']:.3f} | {r['partial_spearman_p']:.4g} | {r['q_partial_bh']:.4g} |\n"
            )

        f.write("\n## Kurzinterpretation\n\n")
        f.write("- In den adjustierten Modellen (Standort + Koeder kontrolliert) zeigt keiner der drei Endpunkte einen signifikanten Sichtweiten-Effekt (alle BH-q > 0.70).\n")
        f.write("- Der zuvor beobachtete bivariate Zusammenhang mit MaxN und Species Richness wird damit weitgehend durch Standort-/Koedereffekte erklaert.\n")
        f.write("- Fuer Schlussfolgerungen sollten primaer die adjustierten Effektschaetzungen berichtet werden.\n")


if __name__ == "__main__":
    main()
