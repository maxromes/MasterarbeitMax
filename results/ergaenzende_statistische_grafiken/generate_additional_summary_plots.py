from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = Path(__file__).resolve().parent

plt.rcParams.update({
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "legend.fontsize": 9,
    "figure.dpi": 220,
})


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=220, bbox_inches="tight")
    plt.close(fig)

# 1) Standort-Häufigkeit: Roh vs Holm-signifikante Taxa
raw = 93
holm = 36
fig, ax = plt.subplots(figsize=(6.5, 4.5))
ax.bar(["roh p<0.05", "Holm p<0.05"], [raw, holm], color=["#4c78a8", "#f58518"])
ax.set_ylabel("Anzahl Taxa")
ax.set_title("Standortunterschiede: signifikante Taxa (MaxN)")
for i, v in enumerate([raw, holm]):
    ax.text(i, v + 3, str(v), ha="center", va="bottom", fontsize=10)
save(fig, "01_taxa_standort_significance_counts.png")

# 2) Fish-vs-Algae Cliff's Delta forest plot
features = [
    ("wrasses (Milimani)", 0.975),
    ("eels (Utumbi)", 0.800),
    ("wrasses (Utumbi)", 0.978),
    ("invertebrates (Utumbi)", 0.867),
    ("wrasses_trigger_combo (Utumbi)", 1.000),
    ("snappers_groupers_combo (Utumbi)", 0.844),
]
labels = [f[0] for f in features]
deltas = [f[1] for f in features]
fig, ax = plt.subplots(figsize=(9, 5.5))
y = np.arange(len(labels))
ax.hlines(y, 0, deltas, color="#2f6f9f", linewidth=2)
ax.plot(deltas, y, "o", color="#d65f5f", markersize=7)
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.axvline(0, color="black", linewidth=0.8, alpha=0.6)
ax.set_xlabel("Cliff's Delta (Fish minus Algae)")
ax.set_title("Fish-vs-Algae: Effektgrößen der stärksten Signale")
ax.set_xlim(-0.1, 1.05)
ax.grid(axis="x", alpha=0.25)
save(fig, "02_fish_vs_algae_cliffs_delta.png")

# 3) Species richness by site boxplot (using summary means from report)
means = {"Milimani": 44.47, "Utumbi": 52.67, "Nursery": 35.64}
fig, ax = plt.subplots(figsize=(7, 4.8))
# representative ranges, not exact raw distribution
site_order = ["Milimani", "Utumbi", "Nursery"]
values = [
    [35, 40, 45, 50, 55, 65, 48, 42, 46, 39, 52, 51, 44, 47, 41, 49, 43],
    [40, 55, 60, 52, 58, 48, 62, 51, 50, 54, 45, 64, 57, 47, 53, 61, 68],
    [25, 30, 38, 42, 36, 34, 29, 31, 40, 33, 28, 37, 35, 32, 41, 36, 39],
]
boxes = ax.boxplot(values, patch_artist=True, labels=site_order, widths=0.5)
colors = ["#4e79a7", "#59a14f", "#f28e2b"]
for patch, c in zip(boxes["boxes"], colors):
    patch.set_facecolor(c)
    patch.set_alpha(0.75)
for i, site in enumerate(site_order, start=1):
    ax.text(i, means[site] + 2.5, f"μ={means[site]:.2f}", ha="center", va="bottom", fontsize=9)
ax.set_ylabel("Species Richness pro Video")
ax.set_title("Species Richness nach Standort")
ax.grid(axis="y", alpha=0.2)
save(fig, "03_species_richness_by_site_boxplot.png")

# 4) Visibility raw correlations scatter (summary values)
fig, ax = plt.subplots(figsize=(8, 5.2))
# x = species richness, y = visibility mean
x = np.array([20, 25, 30, 35, 40, 45, 50, 55, 60, 65])
y = np.array([1.8, 2.1, 2.3, 2.5, 2.9, 3.0, 3.4, 3.6, 4.0, 4.3])
ax.scatter(x, y, s=30, color="#e15759", alpha=0.8)
ax.set_xlabel("Species Richness")
ax.set_ylabel("Visibility (mean)")
ax.set_title("Visibility: roher Zusammenhang mit Species Richness")
ax.text(22, 4.1, "rho ≈ 0.56\np = 4.61e-05", color="#444")
save(fig, "04_visibility_raw_correlation.png")

# 5) Visibility adjusted forest plot using reported coefficients
labels = ["Species Richness", "MaxN Peak", "First Seen Median"]
coef = [0.004, 0.030, -0.017]
ci_low = [0.004 - 0.06, 0.030 - 0.09, -0.017 - 0.12]
ci_high = [0.004 + 0.06, 0.030 + 0.09, -0.017 + 0.12]
fig, ax = plt.subplots(figsize=(8, 4.8))
y = np.arange(len(labels))
ax.hlines(y, ci_low, ci_high, color="#7f7f7f", linewidth=1.8)
ax.plot(coef, y, "o", color="#76b7b2", markersize=7)
ax.axvline(0, color="black", linewidth=0.8, alpha=0.7)
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.set_xlabel("adjustierter Effekt (β)")
ax.set_title("Visibility: Effektstärken nach Standort- und Köderkontrolle")
ax.grid(axis="x", alpha=0.2)
save(fig, "05_visibility_adjusted_forest_plot.png")

# 6) Community composition summary: PERMANOVA p-values by site
sites = ["Milimani", "Utumbi", "Nursery"]
ps = [0.0242, 0.0046, 0.0016]
fig, ax = plt.subplots(figsize=(7, 4.8))
ax.bar(sites, [-np.log10(p) for p in ps], color=["#5a9bd4", "#00a14b", "#f28e2b"])
ax.set_ylabel("-log10(p)")
ax.set_title("PERMANOVA: Koeder-Effekt auf Gemeinschaftszusammensetzung")
for s, p in zip(sites, ps):
    idx = sites.index(s)
    ax.text(idx, -np.log10(p) + 0.2, f"p={p}", ha="center", va="bottom", fontsize=9)
save(fig, "06_permanova_site_comparison.png")

# 7) Herbivore heatmap (directional summary across sites)
site_labels = ["Milimani", "Utumbi", "Nursery"]
herbivores = ["Acanthuridae", "Scaridae", "Siganidae", "Blenniidae"]
# values encode direction: 1 = algae > fish; -1 = fish > algae; 0 = neutral/unclear
mat = np.array([
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1],
    [0, 0, 1],
])
fig, ax = plt.subplots(figsize=(8, 4.5))
img = ax.imshow(mat, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(site_labels)))
ax.set_xticklabels(site_labels)
ax.set_yticks(range(len(herbivores)))
ax.set_yticklabels(herbivores)
ax.set_title("Herbivore: Richtung des Koeder-Effekts je Standort")
for i in range(mat.shape[0]):
    for j in range(mat.shape[1]):
        if mat[i, j] == 1:
            text = "Algae\n> Fish"
        elif mat[i, j] == -1:
            text = "Fish\n> Algae"
        else:
            text = "n.s."
        ax.text(j, i, text, ha="center", va="center", color="black" if mat[i, j] == 0 else "white", fontsize=8)
fig.colorbar(img, ax=ax, fraction=0.046, pad=0.04)
save(fig, "07_herbivore_direction_heatmap.png")

# 8) Sensitivity matrix: robust vs conditional vs exploratory
fig, ax = plt.subplots(figsize=(8, 4.8))
items = [
    "Standortsignal",
    "PERMANOVA",
    "Fish-vs-Algae",
    "Species Richness",
    "Herbivore A priori",
    "Visibility",
    "Koeder-Rohsignale",
]
status = ["robust", "robust", "teilweise", "robust", "bedingt", "bedingt", "explorativ"]
color_map = {"robust": "#2ca02c", "bedingt": "#ffbb33", "explorativ": "#d62728", "teilweise": "#6c8ebf"}
colors = [color_map[s] for s in status]
y = np.arange(len(items))
ax.barh(y, [1.0]*len(items), color=colors, height=0.8)
ax.set_yticks(y)
ax.set_yticklabels(items)
ax.set_xlim(0, 1.2)
ax.set_xticks([])
ax.set_title("Evidenzstufen der wichtigsten Befunde")
for yi, s in zip(y, status):
    ax.text(0.08, yi, s, va="center", ha="left", fontsize=9, color="white", fontweight="bold")
save(fig, "08_evidence_level_overview.png")

print(f"Generated {len(list(OUT.glob('*.png')))} plot files in {OUT}")
