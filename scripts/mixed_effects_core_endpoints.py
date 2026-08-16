#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "visibility_analysis" / "visibility_video_level_merged.csv"

OUT_DIR = ROOT / "results" / "mixed_effects_core_endpoints"
OUT_EFFECTS = OUT_DIR / "mixed_effects_endpoint_effects.csv"
OUT_SUMMARY = OUT_DIR / "mixed_effects_core_endpoints.md"

PLOT_DIR = ROOT / "results" / "ergaenzende_statistische_grafiken"
OUT_PLOT = PLOT_DIR / "14_mixed_effects_fish_vs_algae_forest.png"

ENDPOINTS = ["species_richness", "maxn_video_peak", "first_seen_median_sec"]

BAIT_TYPE = {
    "mackerel": "fish",
    "fischmix": "fish",
    "sargassum": "algae",
    "ulva_salad": "algae",
    "ulva_gutweed": "algae",
    "algaemix": "algae",
    "algae_strings": "algae",
    "control": "control",
}


def prepare_input(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["bait_type"] = out["koeder"].map(BAIT_TYPE)
    out = out[out["bait_type"].isin(["fish", "algae"])].copy()
    out = out[out["visibility_mean"].notna()].copy()
    out["visibility_z"] = (out["visibility_mean"] - out["visibility_mean"].mean()) / out["visibility_mean"].std(ddof=0)
    return out


def fit_endpoint_mixed_model(df: pd.DataFrame, endpoint: str) -> Dict[str, float]:
    work = df[["standort", "bait_type", "visibility_z", endpoint]].dropna().copy()
    work["y_log"] = np.log1p(work[endpoint].astype(float))

    # Random intercept by site captures clustered structure at standort level.
    model = smf.mixedlm("y_log ~ C(bait_type) + visibility_z", data=work, groups=work["standort"])
    fit = model.fit(reml=False, method="powell", maxiter=400, disp=False)

    beta = float(fit.params.get("C(bait_type)[T.fish]", np.nan))
    se = float(fit.bse.get("C(bait_type)[T.fish]", np.nan))
    p = float(fit.pvalues.get("C(bait_type)[T.fish]", np.nan))

    ci_low = beta - 1.96 * se if np.isfinite(beta) and np.isfinite(se) else np.nan
    ci_high = beta + 1.96 * se if np.isfinite(beta) and np.isfinite(se) else np.nan

    return {
        "endpoint": endpoint,
        "n_videos": int(len(work)),
        "n_fish": int((work["bait_type"] == "fish").sum()),
        "n_algae": int((work["bait_type"] == "algae").sum()),
        "beta_fish_vs_algae": beta,
        "se": se,
        "ci95_low": float(ci_low),
        "ci95_high": float(ci_high),
        "p_value": p,
        "pct_change_fish_vs_algae": float(np.expm1(beta) * 100.0) if np.isfinite(beta) else np.nan,
        "random_intercept_variance_site": float(fit.cov_re.iloc[0, 0]) if fit.cov_re.shape == (1, 1) else np.nan,
        "residual_variance": float(fit.scale),
        "converged": bool(getattr(fit, "converged", False)),
    }


def make_forest_plot(effects_df: pd.DataFrame) -> None:
    labels = {
        "species_richness": "Species Richness",
        "maxn_video_peak": "MaxN Video Peak",
        "first_seen_median_sec": "First Seen Median",
    }

    plot_df = effects_df.copy()
    plot_df["order"] = plot_df["endpoint"].map({k: i for i, k in enumerate(ENDPOINTS)})
    plot_df = plot_df.sort_values("order", ascending=False)

    y = np.arange(len(plot_df))
    x = plot_df["beta_fish_vs_algae"].to_numpy(dtype=float)
    lo = plot_df["ci95_low"].to_numpy(dtype=float)
    hi = plot_df["ci95_high"].to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=(8.2, 4.8))
    ax.hlines(y, lo, hi, color="#6b6b6b", linewidth=2)
    ax.plot(x, y, "o", color="#1f77b4", markersize=7)
    ax.axvline(0.0, color="black", linewidth=1.0, alpha=0.75)
    ax.set_yticks(y)
    ax.set_yticklabels([labels.get(ep, ep) for ep in plot_df["endpoint"].tolist()])
    ax.set_xlabel("Mixed-Effects Koeffizient (fish vs algae; log1p-Skala)")
    ax.set_title("Mixed-Effects: Fish-vs-Algae Effekte je Kernendpunkt")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT_PLOT, dpi=220, bbox_inches="tight")
    plt.close(fig)


def write_summary(effects_df: pd.DataFrame) -> None:
    with OUT_SUMMARY.open("w", encoding="utf-8") as f:
        f.write("# Mixed-Effects Modell: Kernendpunkte\n\n")
        f.write("Stand: 2026-08-16\n\n")
        f.write("## Modell\n\n")
        f.write("- Datengrundlage: visibility_video_level_merged.csv, fish- und algae-Koeder.\n")
        f.write("- Endpunkte: species_richness, maxn_video_peak, first_seen_median_sec.\n")
        f.write("- Response: log1p(Endpunkt).\n")
        f.write("- Fixed Effects: bait_type (fish vs algae) + visibility_z.\n")
        f.write("- Random Effects: Random Intercept fuer Standort.\n")
        f.write("- Inferenz: p-Werte fuer fish-vs-algae-Koeffizient je Endpunkt; Korrektur via BH und Holm ueber 3 Endpunkte.\n")
        f.write("- Hinweis: Ein Random-Intercept fuer Video ist in endpoint-spezifischen Modellen nicht identifizierbar, da je Endpunkt genau eine Beobachtung pro Video vorliegt.\n\n")

        f.write("## Endpoint-spezifische fish-vs-algae Effekte\n\n")
        f.write("| Endpoint | n fish | n algae | Beta (log1p) | 95%-CI | p | q_BH | q_Holm | % fish vs algae |\n")
        f.write("|---|---:|---:|---:|---|---:|---:|---:|---:|\n")

        for _, r in effects_df.iterrows():
            ci = f"[{r['ci95_low']:.4f}, {r['ci95_high']:.4f}]"
            f.write(
                f"| {r['endpoint']} | {int(r['n_fish'])} | {int(r['n_algae'])} | {r['beta_fish_vs_algae']:.4f} | {ci} | {r['p_value']:.4g} | {r['q_bh']:.4g} | {r['q_holm']:.4g} | {r['pct_change_fish_vs_algae']:.2f}% |\n"
            )

        robust_holm = bool((effects_df["q_holm"] < 0.05).any())
        robust_bh = bool((effects_df["q_bh"] < 0.05).any())

        f.write("\n## Kurzfazit\n\n")
        if robust_holm:
            f.write("- Mindestens ein endpoint-spezifischer fish-vs-algae-Effekt bleibt im Mixed-Effects-Rahmen Holm-signifikant.\n")
        elif robust_bh:
            f.write("- Kein Effekt ist Holm-signifikant, aber mindestens ein endpoint-spezifischer fish-vs-algae-Effekt bleibt nach BH signifikant.\n")
        else:
            f.write("- Kein endpoint-spezifischer fish-vs-algae-Effekt bleibt nach BH/Holm-Korrektur signifikant.\n")
        f.write("- Das Modell ergaenzt die bisherigen standortgetrennten Analysen um einen hierarchischen Ansatz mit Standort-Random-Intercept.\n")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PLOT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT)
    work = prepare_input(df)

    rows: List[Dict[str, float]] = []
    for ep in ENDPOINTS:
        rows.append(fit_endpoint_mixed_model(work, ep))

    effects_df = pd.DataFrame(rows)

    valid = effects_df["p_value"].to_numpy(dtype=float)
    _, q_bh, _, _ = multipletests(valid, method="fdr_bh")
    _, q_holm, _, _ = multipletests(valid, method="holm")
    effects_df["q_bh"] = q_bh
    effects_df["q_holm"] = q_holm

    effects_df = effects_df[
        [
            "endpoint",
            "n_videos",
            "n_fish",
            "n_algae",
            "beta_fish_vs_algae",
            "se",
            "ci95_low",
            "ci95_high",
            "p_value",
            "q_bh",
            "q_holm",
            "pct_change_fish_vs_algae",
            "random_intercept_variance_site",
            "residual_variance",
            "converged",
        ]
    ]

    effects_df.to_csv(OUT_EFFECTS, index=False)
    make_forest_plot(effects_df)
    write_summary(effects_df)

    print(f"Wrote: {OUT_EFFECTS}")
    print(f"Wrote: {OUT_SUMMARY}")
    print(f"Wrote: {OUT_PLOT}")


if __name__ == "__main__":
    main()
