#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PREV_CSV = ROOT / "results" / "prevalence_threshold_model" / "prevalence_threshold_summary.csv"
OUT_DIR = ROOT / "results" / "ergaenzende_statistische_grafiken"
OUT_PNG = OUT_DIR / "15_prevalence_threshold_fisher_results.png"

def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Load prevalence data
    df = pd.read_csv(PREV_CSV)
    if df.empty:
        print("No prevalence threshold data; skipping plot.")
        return

    # Pivot for heatmap: rows = family, cols = site, values = log10(p_directional)
    # We'll show the -log10(p) so that higher values = more significant
    df_plot = df.copy()
    df_plot["neg_log10_p"] = -np.log10(df_plot["fisher_p_directional"])
    
    # Also encode direction via color
    df_plot["direction_num"] = (df_plot["direction_observed"] == "algae>fish").astype(int)
    # 0 = fish>algae (plot as negative), 1 = algae>fish (plot as positive)
    df_plot["effect_direction"] = df_plot["direction_num"] * 2 - 1  # -1 or +1
    
    # Create a combined measure: neg_log10_p * direction
    df_plot["signed_log10_p"] = df_plot["neg_log10_p"] * df_plot["effect_direction"]

    # Plot 1: Heatmap by site and family
    fig, axes = plt.subplots(1, 3, figsize=(16, 10), sharey=True)
    fig.suptitle(
        "Prevalence-Threshold Fisher-Exact Tests by Site\n(Colors: algae>fish (red) vs fish>algae (blue); Intensity: -log10(p))",
        fontsize=14,
        fontweight="bold",
        y=0.98
    )

    sites = ["milimani", "nursery", "utumbi"]
    v_max = 1.5  # max of -log10(p) for symmetry
    v_min = -v_max

    for idx, (ax, site) in enumerate(zip(axes, sites)):
        subset = df_plot[df_plot["site"] == site].copy()
        if subset.empty:
            ax.text(0.5, 0.5, f"No data for {site}", ha="center", va="center", transform=ax.transAxes)
            ax.set_title(site.capitalize())
            continue

        # Sort by p-value (smallest first = most significant)
        subset = subset.sort_values("fisher_p_directional")
        families = subset["family"].tolist()
        values = subset["signed_log10_p"].tolist()
        
        # Create barplot
        colors = ["#d73027" if v > 0 else "#4575b4" for v in values]
        bars = ax.barh(range(len(families)), values, color=colors, edgecolor="black", linewidth=0.5)
        
        # Add significance threshold line
        ax.axvline(np.log10(0.05), color="gray", linestyle="--", linewidth=1, alpha=0.7, label="p=0.05")
        ax.axvline(-np.log10(0.05), color="gray", linestyle="--", linewidth=1, alpha=0.7)
        
        ax.set_yticks(range(len(families)))
        ax.set_yticklabels(families, fontsize=8)
        ax.set_xlabel("-log10(p) [signed: + = algae>fish, - = fish>algae]", fontsize=10)
        ax.set_title(site.capitalize(), fontsize=12, fontweight="bold")
        ax.grid(axis="x", alpha=0.3)
        ax.set_xlim(v_min, v_max)

        if idx == 0:
            ax.set_ylabel("Family", fontsize=10)

    # Add legend
    red_patch = mpatches.Patch(color="#d73027", label="Algae > Fish")
    blue_patch = mpatches.Patch(color="#4575b4", label="Fish > Algae")
    fig.legend(
        handles=[red_patch, blue_patch],
        loc="lower center",
        ncol=2,
        fontsize=11,
        bbox_to_anchor=(0.5, -0.02)
    )

    plt.tight_layout(rect=[0, 0.02, 1, 0.96])
    plt.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print(f"Saved: {OUT_PNG}")
    plt.close()

    # Plot 2: Summary of Holm-corrected significance
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Count robust signifikant results per site
    df_robust = df[df["q_holm_directional_site"] <= 0.05].copy()
    robust_by_site = df_robust.groupby("site").size()
    
    # Also show trend-level (0.05 < q <= 0.10)
    df_trend = df[(df["q_holm_directional_site"] > 0.05) & (df["q_holm_directional_site"] <= 0.10)].copy()
    trend_by_site = df_trend.groupby("site").size()
    
    # Ensure all sites are present
    for site in sites:
        if site not in robust_by_site.index:
            robust_by_site[site] = 0
        if site not in trend_by_site.index:
            trend_by_site[site] = 0
    
    robust_by_site = robust_by_site.reindex(sites, fill_value=0)
    trend_by_site = trend_by_site.reindex(sites, fill_value=0)
    
    x = np.arange(len(sites))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, robust_by_site.values, width, label="Holm q <= 0.05", color="#1f77b4", edgecolor="black")
    bars2 = ax.bar(x + width/2, trend_by_site.values, width, label="Trend: 0.05 < q <= 0.10", color="#ff7f0e", edgecolor="black")
    
    ax.set_ylabel("Number of Families", fontsize=11, fontweight="bold")
    ax.set_title(
        "Robust vs. Trend-Level Occupancy Signals by Site\n(Fisher-Exact, Holm-corrected within site)",
        fontsize=13,
        fontweight="bold"
    )
    ax.set_xticks(x)
    ax.set_xticklabels([s.capitalize() for s in sites], fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f"{int(height)}", ha="center", va="bottom", fontsize=9)
    for bar in bars2:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f"{int(height)}", ha="center", va="bottom", fontsize=9)
    
    plt.tight_layout()
    plt.savefig(OUT_DIR / "15b_prevalence_threshold_summary_counts.png", dpi=300, bbox_inches="tight")
    print(f"Saved: {OUT_DIR / '15b_prevalence_threshold_summary_counts.png'}")
    plt.close()

    # Plot 3: Directional breakdown (algae>fish vs fish>algae)
    fig, ax = plt.subplots(figsize=(12, 8))
    
    df_algae = df[df["direction_observed"] == "algae>fish"].copy()
    df_fish = df[df["direction_observed"] == "fish>algae"].copy()
    
    algae_by_site = df_algae.groupby("site").size()
    fish_by_site = df_fish.groupby("site").size()
    
    for site in sites:
        if site not in algae_by_site.index:
            algae_by_site[site] = 0
        if site not in fish_by_site.index:
            fish_by_site[site] = 0
    
    algae_by_site = algae_by_site.reindex(sites, fill_value=0)
    fish_by_site = fish_by_site.reindex(sites, fill_value=0)
    
    x = np.arange(len(sites))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, algae_by_site.values, width, label="Algae > Fish (direction)", color="#d73027", edgecolor="black")
    bars2 = ax.bar(x + width/2, fish_by_site.values, width, label="Fish > Algae (direction)", color="#4575b4", edgecolor="black")
    
    ax.set_ylabel("Number of Families", fontsize=11, fontweight="bold")
    ax.set_title(
        "Occupancy Direction Breakdown by Site\n(All families after prevalence threshold filter)",
        fontsize=13,
        fontweight="bold"
    )
    ax.set_xticks(x)
    ax.set_xticklabels([s.capitalize() for s in sites], fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(axis="y", alpha=0.3)
    
    # Add value labels on bars
    for bar in bars1:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f"{int(height)}", ha="center", va="bottom", fontsize=9)
    for bar in bars2:
        height = bar.get_height()
        if height > 0:
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f"{int(height)}", ha="center", va="bottom", fontsize=9)
    
    plt.tight_layout()
    plt.savefig(OUT_DIR / "15c_prevalence_threshold_direction_breakdown.png", dpi=300, bbox_inches="tight")
    print(f"Saved: {OUT_DIR / '15c_prevalence_threshold_direction_breakdown.png'}")
    plt.close()

    print("\nAll prevalence-threshold plots completed.")

if __name__ == "__main__":
    main()
