from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "results" / "visibility_analysis"
FIG_DIR = BASE / "figures"

CORR_CSV = BASE / "visibility_vs_metrics_correlations.csv"
ADJ_CSV = BASE / "visibility_adjusted_model_results.csv"
ADD_CSV = BASE / "visibility_additional_tests_adjusted.csv"
SITE_CSV = BASE / "visibility_site_stratified_tests_adjusted.csv"


def friendly_metric(name: str) -> str:
    mapping = {
        "maxn_video_peak": "MaxN (Video-Peak)",
        "species_richness": "Species Richness",
        "first_seen_median_sec": "First Seen Median (s)",
    }
    return mapping.get(name, name)


def save_raw_correlations() -> None:
    df = pd.read_csv(CORR_CSV).copy()
    df["metric_label"] = df["metric"].map(friendly_metric)
    df = df.sort_values("spearman_rho", ascending=True)

    fig, ax = plt.subplots(figsize=(9, 4.8))
    colors = ["#1b9e77" if q < 0.05 else "#7f8c8d" for q in df["spearman_q_bh"]]

    bars = ax.barh(df["metric_label"], df["spearman_rho"], color=colors, edgecolor="black", linewidth=0.6)
    ax.axvline(0, color="black", linewidth=1)
    ax.set_xlabel("Spearman rho")
    ax.set_title("Rohzusammenhaenge: Sicht vs. Endpunkte")

    for bar, p, q in zip(bars, df["spearman_p"], df["spearman_q_bh"]):
        x = bar.get_width()
        ax.text(
            x + (0.015 if x >= 0 else -0.02),
            bar.get_y() + bar.get_height() / 2,
            f"p={p:.3g}, q={q:.3g}",
            va="center",
            ha="left" if x >= 0 else "right",
            fontsize=9,
        )

    ax.set_xlim(min(-0.05, float(df["spearman_rho"].min()) - 0.08), float(df["spearman_rho"].max()) + 0.22)
    ax.text(
        0.99,
        -0.22,
        "Gruen = BH-signifikant (q<0.05)",
        transform=ax.transAxes,
        ha="right",
        va="center",
        fontsize=9,
    )

    fig.tight_layout()
    fig.savefig(FIG_DIR / "visibility_raw_correlations.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def save_adjusted_forest() -> None:
    df = pd.read_csv(ADJ_CSV).copy()
    df["metric_label"] = df["metric"].map(friendly_metric)
    df = df.iloc[::-1].reset_index(drop=True)

    y = np.arange(len(df))
    coef = df["coef_visibility_log1p"].to_numpy()
    low = df["coef_ci95_low"].to_numpy()
    high = df["coef_ci95_high"].to_numpy()

    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.hlines(y, low, high, color="#2c3e50", linewidth=2)
    ax.plot(coef, y, "o", color="#d35400", markersize=7)
    ax.axvline(0, color="black", linestyle="--", linewidth=1)

    ax.set_yticks(y)
    ax.set_yticklabels(df["metric_label"])
    ax.set_xlabel("Beta fuer Sicht (log1p-Modell)")
    ax.set_title("Adjustierte Sicht-Effekte (mit 95%-CI)")

    for i, row in df.iterrows():
        ax.text(
            float(high[i]) + 0.01,
            y[i],
            f"q(HC3)={row['q_hc3_bh']:.3g}, q(Perm)={row['q_perm_bh']:.3g}",
            va="center",
            fontsize=9,
        )

    xmin = min(float(low.min()) - 0.05, -0.12)
    xmax = max(float(high.max()) + 0.34, 0.35)
    ax.set_xlim(xmin, xmax)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "visibility_adjusted_effects_forest.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def save_robustness_qvalues() -> None:
    df = pd.read_csv(ADD_CSV).copy()
    df["metric_label"] = df["metric"].map(friendly_metric)

    q_cols = [
        "q_hc3_fdr_bh",
        "q_perm_blocked_fdr_bh",
        "q_quad_fdr_bh",
        "q_quantile_fdr_bh",
    ]
    col_labels = ["HC3", "Perm block", "Quadratik", "Quantil (Median)"]

    mat = df[q_cols].to_numpy(dtype=float)

    fig, ax = plt.subplots(figsize=(8.8, 4.8))
    im = ax.imshow(mat, cmap="YlOrRd_r", vmin=0, vmax=1, aspect="auto")

    ax.set_xticks(np.arange(len(col_labels)))
    ax.set_xticklabels(col_labels, rotation=0)
    ax.set_yticks(np.arange(len(df)))
    ax.set_yticklabels(df["metric_label"])
    ax.set_title("Robustheitschecks: BH-q-Werte")

    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            val = mat[i, j]
            ax.text(j, i, f"{val:.3f}", ha="center", va="center", fontsize=9, color="black")

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("BH-q")

    fig.tight_layout()
    fig.savefig(FIG_DIR / "visibility_robustness_qvalues_heatmap.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def save_site_stratified_perm() -> None:
    df = pd.read_csv(SITE_CSV).copy()
    df["metric_label"] = df["metric"].map(friendly_metric)

    site_order = ["milimani", "nursery", "utumbi"]
    metric_order = ["maxn_video_peak", "species_richness", "first_seen_median_sec"]

    xlabels: list[str] = []
    values: list[float] = []
    colors: list[str] = []

    palette = {
        "maxn_video_peak": "#1f77b4",
        "species_richness": "#2ca02c",
        "first_seen_median_sec": "#ff7f0e",
    }

    for site in site_order:
        for metric in metric_order:
            row = df[(df["standort"] == site) & (df["metric"] == metric)]
            if row.empty:
                continue
            values.append(float(row.iloc[0]["p_perm_blocked"]))
            xlabels.append(f"{site}\n{friendly_metric(metric)}")
            colors.append(palette[metric])

    x = np.arange(len(values))
    fig, ax = plt.subplots(figsize=(12, 4.8))
    bars = ax.bar(x, values, color=colors, edgecolor="black", linewidth=0.5)
    ax.axhline(0.05, color="red", linestyle="--", linewidth=1, label="alpha=0.05")
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Blockierter Permutations-p")
    ax.set_title("Standort-stratifizierte Sichttests (Permutation innerhalb Koeder)")
    ax.set_xticks(x)
    ax.set_xticklabels(xlabels, rotation=30, ha="right")
    ax.legend(loc="upper left")

    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.015, f"{b.get_height():.3f}", ha="center", va="bottom", fontsize=8)

    fig.tight_layout()
    fig.savefig(FIG_DIR / "visibility_site_stratified_permutation_pvalues.png", dpi=220, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    save_raw_correlations()
    save_adjusted_forest()
    save_robustness_qvalues()
    save_site_stratified_perm()


if __name__ == "__main__":
    main()
