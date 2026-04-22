from __future__ import annotations

from pathlib import Path
from itertools import combinations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "results" / "mackerel_standortvergleich" / "data" / "mackerel_video_metrics.csv"
GLOBAL_TESTS_FILE = ROOT / "results" / "mackerel_standortvergleich" / "data" / "mackerel_video_metrics_global_tests.csv"
OUT_DIR = ROOT / "results" / "mackerel_standortvergleich" / "figures"

SITE_ORDER = ["milimani", "utumbi", "nursery"]
SITE_COLORS = {
    "milimani": "#1f6f8b",
    "utumbi": "#e07a5f",
    "nursery": "#3d405b",
}


def bootstrap_ci(values: np.ndarray, n_boot: int = 5000, seed: int = 42) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    samples = rng.choice(values, size=(n_boot, len(values)), replace=True)
    means = samples.mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def bootstrap_diff_ci(
    values_a: np.ndarray,
    values_b: np.ndarray,
    n_boot: int = 5000,
    seed: int = 99,
) -> tuple[float, float, float]:
    rng = np.random.default_rng(seed)
    boot_a = rng.choice(values_a, size=(n_boot, len(values_a)), replace=True).mean(axis=1)
    boot_b = rng.choice(values_b, size=(n_boot, len(values_b)), replace=True).mean(axis=1)
    diff = boot_a - boot_b
    return float(diff.mean()), float(np.percentile(diff, 2.5)), float(np.percentile(diff, 97.5))


def main() -> None:
    df = pd.read_csv(DATA_FILE)
    plot_df = df[["standort", "species_richness"]].copy()
    plot_df = plot_df[plot_df["standort"].isin(SITE_ORDER)].copy()

    global_tests = pd.read_csv(GLOBAL_TESTS_FILE)
    sr_test = global_tests[global_tests["metric"] == "species_richness"].iloc[0]
    p_raw = sr_test["p_value"]
    p_holm = sr_test["p_value_holm"]
    p_bh = sr_test["p_value_bh"]

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Plot 1: Boxplot + Einzelpunkte
    fig, ax = plt.subplots(figsize=(10, 6), dpi=160)
    data_by_site = [plot_df.loc[plot_df["standort"] == s, "species_richness"].to_numpy() for s in SITE_ORDER]
    bp = ax.boxplot(
        data_by_site,
        positions=np.arange(1, len(SITE_ORDER) + 1),
        widths=0.55,
        patch_artist=True,
        medianprops={"color": "#111111", "linewidth": 2},
    )

    for patch, site in zip(bp["boxes"], SITE_ORDER):
        patch.set_facecolor(SITE_COLORS[site])
        patch.set_alpha(0.35)
        patch.set_edgecolor(SITE_COLORS[site])
        patch.set_linewidth(2)

    rng = np.random.default_rng(7)
    for i, site in enumerate(SITE_ORDER, start=1):
        y = plot_df.loc[plot_df["standort"] == site, "species_richness"].to_numpy()
        x = i + rng.uniform(-0.08, 0.08, size=len(y))
        ax.scatter(
            x,
            y,
            s=80,
            color=SITE_COLORS[site],
            edgecolor="white",
            linewidth=0.8,
            alpha=0.95,
            zorder=3,
        )
        ax.text(i, y.max() + 1.5, f"n={len(y)}", ha="center", va="bottom", fontsize=10)

    ax.set_xticks(np.arange(1, len(SITE_ORDER) + 1))
    ax.set_xticklabels([s.capitalize() for s in SITE_ORDER], fontsize=11)
    ax.set_ylabel("Species Richness pro Video", fontsize=12)
    ax.set_title("Mackerel-Vergleich: Species Richness je Standort", fontsize=15, weight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    subtitle = f"Kruskal-Wallis: p={p_raw:.4f}, Holm={p_holm:.4f}, BH={p_bh:.4f}"
    ax.text(0.5, 1.02, subtitle, transform=ax.transAxes, ha="center", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "species_richness_mackerel_boxstrip.png")
    fig.savefig(OUT_DIR / "species_richness_mackerel_boxstrip.svg")
    plt.close(fig)

    # Plot 2: Mittelwerte mit 95%-Bootstrap-CI
    summary = []
    for site in SITE_ORDER:
        vals = plot_df.loc[plot_df["standort"] == site, "species_richness"].to_numpy()
        mean_val = float(vals.mean())
        ci_low, ci_high = bootstrap_ci(vals)
        summary.append((site, mean_val, ci_low, ci_high, len(vals)))

    fig, ax = plt.subplots(figsize=(10, 6), dpi=160)
    x = np.arange(len(summary))
    means = np.array([s[1] for s in summary])
    ci_l = np.array([s[2] for s in summary])
    ci_h = np.array([s[3] for s in summary])
    yerr = np.vstack([means - ci_l, ci_h - means])

    colors = [SITE_COLORS[s[0]] for s in summary]
    bars = ax.bar(x, means, color=colors, alpha=0.85, width=0.62)
    ax.errorbar(x, means, yerr=yerr, fmt="none", ecolor="#111111", elinewidth=1.5, capsize=6, zorder=3)

    for i, (_, mean_val, ci_low, ci_high, n) in enumerate(summary):
        ax.text(i, mean_val + 0.7, f"{mean_val:.1f}", ha="center", va="bottom", fontsize=10, weight="bold")
        ax.text(i, ci_low - 1.6, f"n={n}", ha="center", va="top", fontsize=9)

    ax.set_xticks(x)
    ax.set_xticklabels([s[0].capitalize() for s in summary], fontsize=11)
    ax.set_ylabel("Durchschnittliche Species Richness", fontsize=12)
    ax.set_title("Mackerel-Vergleich: Mittelwert Species Richness (95%-Bootstrap-CI)", fontsize=15, weight="bold")
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    ax.set_ylim(bottom=0)

    ax.text(
        0.5,
        1.02,
        "Alle Standorte: keine robuste Signifikanz nach Holm/BH (alpha=0.05)",
        transform=ax.transAxes,
        ha="center",
        fontsize=10,
    )

    fig.tight_layout()
    fig.savefig(OUT_DIR / "species_richness_mackerel_mean_ci.png")
    fig.savefig(OUT_DIR / "species_richness_mackerel_mean_ci.svg")
    plt.close(fig)

    # Plot 3: Paarweise Mittelwert-Differenzen mit 95%-Bootstrap-CI
    pair_labels = []
    pair_means = []
    pair_low = []
    pair_high = []
    for idx, (site_a, site_b) in enumerate(combinations(SITE_ORDER, 2), start=1):
        a = plot_df.loc[plot_df["standort"] == site_a, "species_richness"].to_numpy()
        b = plot_df.loc[plot_df["standort"] == site_b, "species_richness"].to_numpy()
        mean_diff, ci_low, ci_high = bootstrap_diff_ci(a, b, seed=99 + idx)
        pair_labels.append(f"{site_a.capitalize()} - {site_b.capitalize()}")
        pair_means.append(mean_diff)
        pair_low.append(ci_low)
        pair_high.append(ci_high)

    fig, ax = plt.subplots(figsize=(10, 5.8), dpi=160)
    y_pos = np.arange(len(pair_labels))
    pair_means = np.array(pair_means)
    pair_low = np.array(pair_low)
    pair_high = np.array(pair_high)
    xerr = np.vstack([pair_means - pair_low, pair_high - pair_means])

    ax.errorbar(
        pair_means,
        y_pos,
        xerr=xerr,
        fmt="o",
        color="#1f2937",
        ecolor="#374151",
        elinewidth=2,
        capsize=6,
        markersize=8,
    )
    ax.axvline(0, color="#9ca3af", linestyle="--", linewidth=1.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(pair_labels, fontsize=10)
    ax.set_xlabel("Differenz der Mittelwerte (Species Richness)", fontsize=12)
    ax.set_title("Mackerel-Vergleich: Paarweise Differenzen (95%-Bootstrap-CI)", fontsize=14, weight="bold")
    ax.grid(axis="x", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)
    ax.text(
        0.5,
        1.02,
        "Interpretation: CI, die 0 schneidet, spricht gegen klaren Standorteffekt",
        transform=ax.transAxes,
        ha="center",
        fontsize=10,
    )

    fig.tight_layout()
    fig.savefig(OUT_DIR / "species_richness_mackerel_pairwise_diff.png")
    fig.savefig(OUT_DIR / "species_richness_mackerel_pairwise_diff.svg")
    plt.close(fig)

    print(f"Grafiken gespeichert in: {OUT_DIR}")


if __name__ == "__main__":
    main()