#!/usr/bin/env python3
"""
Standortvergleich für alle cut_47min Videos.

Analysen:
- Vergleich Species Richness zwischen Standorten (global + paarweise)
- Fokus Utumbi vs. Milimani (zusätzlich köder-stratifizierter Permutationstest)
- Vergleich beider Standorte mit Nursery
- Artenpool-Überlappung und Jaccard-Ähnlichkeit
- PCoA auf Jaccard-Distanzen (Video-Ebene) zur Visualisierung der Überlappung

Ausgabeordner:
- results/Standortvergleich/
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy import stats
from scipy.spatial.distance import pdist, squareform

ROOT = Path(__file__).resolve().parent.parent
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min"
CORAL_REEF_DIR = CUT_ROOT / "Annotation_reports_coral_reef"
NURSERY_DIR = CUT_ROOT / "Annotation_reports_Nursery"

OUT_DIR = ROOT / "results" / "Standortvergleich"
FIG_DIR = OUT_DIR / "figures"

ALPHA = 0.05
RNG = np.random.default_rng(42)

SITE_COLORS = {
    "utumbi": "#1f77b4",
    "milimani": "#ff7f0e",
    "nursery": "#2ca02c",
}


def is_truthy(value: object) -> bool:
    if value is None:
        return False
    text = str(value).strip().lower()
    return text in {"1", "true", "t", "yes", "y"}


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


def load_video_data(csv_path: Path) -> Dict[str, object]:
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")

    taxa: set[str] = set()
    rows_used = 0
    for _, row in df.iterrows():
        if is_truthy(row.get("feeding", "")) or is_truthy(row.get("interested", "")):
            continue
        key = build_taxon_key(row)
        if key:
            taxa.add(key)
            rows_used += 1

    date, standort, koeder = parse_video_metadata(csv_path.name)
    return {
        "filename": csv_path.name,
        "date": date,
        "standort": standort,
        "koeder": koeder,
        "species_richness": len(taxa),
        "rows_total": int(len(df)),
        "rows_used": int(rows_used),
        "taxa_set": taxa,
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


def pairwise_site_tests(videos_df: pd.DataFrame) -> pd.DataFrame:
    sites = ["utumbi", "milimani", "nursery"]
    rows: List[Dict[str, object]] = []

    for a, b in itertools.combinations(sites, 2):
        xa = videos_df.loc[videos_df["standort"] == a, "species_richness"].astype(float).values
        xb = videos_df.loc[videos_df["standort"] == b, "species_richness"].astype(float).values
        if len(xa) < 2 or len(xb) < 2:
            continue

        u_stat, p_val = stats.mannwhitneyu(xa, xb, alternative="two-sided")
        rows.append(
            {
                "site_a": a,
                "site_b": b,
                "n_a": len(xa),
                "n_b": len(xb),
                "median_a": float(np.median(xa)),
                "median_b": float(np.median(xb)),
                "mean_a": float(np.mean(xa)),
                "mean_b": float(np.mean(xb)),
                "mean_diff_a_minus_b": float(np.mean(xa) - np.mean(xb)),
                "u_stat": float(u_stat),
                "p_value": float(p_val),
                "cliffs_delta": cliffs_delta(xa, xb),
            }
        )

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    out["p_value_holm"] = holm_adjust(out["p_value"].tolist())
    out["significant_0_05"] = out["p_value"] < ALPHA
    out["significant_0_05_holm"] = out["p_value_holm"] < ALPHA
    out["sig_label_raw"] = out["p_value"].map(significance_label)
    out["sig_label_holm"] = out["p_value_holm"].map(significance_label)
    return out.sort_values(["p_value_holm", "p_value"]).reset_index(drop=True)


def stratified_permutation_utumbi_vs_milimani(videos_df: pd.DataFrame, n_perm: int = 20000) -> Dict[str, object]:
    sub = videos_df[videos_df["standort"].isin(["utumbi", "milimani"])].copy()

    valid_baits = []
    for bait, part in sub.groupby("koeder"):
        sites_here = set(part["standort"].unique())
        if {"utumbi", "milimani"}.issubset(sites_here):
            valid_baits.append(bait)

    sub = sub[sub["koeder"].isin(valid_baits)].copy()
    if sub.empty:
        return {
            "test": "Stratifizierter Permutationstest (Utumbi vs Milimani | by koeder)",
            "n_perm": n_perm,
            "n_rows": 0,
            "n_baits": 0,
            "stat_mean_diff": math.nan,
            "p_value": math.nan,
            "significant_0_05": False,
            "note": "Keine gemeinsamen Köder zwischen Utumbi und Milimani.",
        }

    x = sub.loc[sub["standort"] == "utumbi", "species_richness"].astype(float).values
    y = sub.loc[sub["standort"] == "milimani", "species_richness"].astype(float).values
    obs = float(np.mean(x) - np.mean(y))

    parts = []
    for bait, part in sub.groupby("koeder"):
        vals = part["species_richness"].astype(float).to_numpy()
        labels = part["standort"].astype(str).to_numpy().copy()
        parts.append((vals, labels))

    perm_stats = np.empty(n_perm, dtype=float)
    for i in range(n_perm):
        x_vals = []
        y_vals = []
        for vals, labels in parts:
            shuffled = labels.copy()
            RNG.shuffle(shuffled)
            x_vals.extend(vals[shuffled == "utumbi"])
            y_vals.extend(vals[shuffled == "milimani"])
        perm_stats[i] = float(np.mean(x_vals) - np.mean(y_vals))

    p_val = float(np.mean(np.abs(perm_stats) >= abs(obs)))

    return {
        "test": "Stratifizierter Permutationstest (Utumbi vs Milimani | by koeder)",
        "n_perm": n_perm,
        "n_rows": int(len(sub)),
        "n_baits": int(len(valid_baits)),
        "stat_mean_diff": obs,
        "p_value": p_val,
        "significant_0_05": bool(p_val < ALPHA),
        "note": f"Gemeinsame Köder: {', '.join(sorted(valid_baits))}",
    }


def compute_site_pool_overlap(videos_df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, set[str]]]:
    site_sets: Dict[str, set[str]] = {}
    for site in ["utumbi", "milimani", "nursery"]:
        taxa_union: set[str] = set()
        for taxa in videos_df.loc[videos_df["standort"] == site, "taxa_set"]:
            taxa_union |= set(taxa)
        site_sets[site] = taxa_union

    rows = []
    for a, b in itertools.combinations(["utumbi", "milimani", "nursery"], 2):
        set_a = site_sets[a]
        set_b = site_sets[b]
        inter = len(set_a & set_b)
        union = len(set_a | set_b)
        jaccard = inter / union if union else math.nan
        rows.append(
            {
                "site_a": a,
                "site_b": b,
                "n_taxa_a": len(set_a),
                "n_taxa_b": len(set_b),
                "intersection_taxa": inter,
                "union_taxa": union,
                "jaccard_similarity": jaccard,
                "jaccard_distance": (1.0 - jaccard) if not math.isnan(jaccard) else math.nan,
                "unique_a": len(set_a - set_b),
                "unique_b": len(set_b - set_a),
            }
        )

    return pd.DataFrame(rows), site_sets


def pcoa_from_jaccard(binary_matrix: np.ndarray) -> np.ndarray:
    if binary_matrix.shape[0] < 3:
        return np.zeros((binary_matrix.shape[0], 2))

    dist_vec = pdist(binary_matrix, metric="jaccard")
    dist_mat = squareform(dist_vec)

    n = dist_mat.shape[0]
    d2 = dist_mat ** 2
    j = np.eye(n) - np.ones((n, n)) / n
    b = -0.5 * j @ d2 @ j

    eigvals, eigvecs = np.linalg.eigh(b)
    idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]

    positive = eigvals > 1e-12
    eigvals = eigvals[positive]
    eigvecs = eigvecs[:, positive]

    if len(eigvals) == 0:
        return np.zeros((n, 2))

    coords = eigvecs * np.sqrt(eigvals)
    if coords.shape[1] == 1:
        coords = np.column_stack([coords[:, 0], np.zeros(n)])
    return coords[:, :2]


def create_figures(videos_df: pd.DataFrame, overlap_df: pd.DataFrame, site_sets: Dict[str, set[str]]) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    # 1) Richness pro Standort
    plt.figure(figsize=(9, 6))
    site_order = ["utumbi", "milimani", "nursery"]
    data = [videos_df.loc[videos_df["standort"] == s, "species_richness"].values for s in site_order]
    bp = plt.boxplot(data, tick_labels=site_order, patch_artist=True)
    for patch, s in zip(bp["boxes"], site_order):
        patch.set_facecolor(SITE_COLORS[s])
        patch.set_alpha(0.45)
    for i, s in enumerate(site_order, start=1):
        y = videos_df.loc[videos_df["standort"] == s, "species_richness"].values
        x = np.full_like(y, i, dtype=float) + RNG.normal(0, 0.04, size=len(y))
        plt.scatter(x, y, s=28, color=SITE_COLORS[s], alpha=0.75)
    plt.ylabel("Species Richness (pro Video)")
    plt.title("Standortvergleich: Species Richness (cut_47min)")
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "species_richness_by_site_boxplot.png", dpi=180)
    plt.close()

    # 2) Jaccard-Heatmap auf Standort-Artenpools
    sim = np.eye(3)
    sites = ["utumbi", "milimani", "nursery"]
    idx = {s: i for i, s in enumerate(sites)}
    for _, r in overlap_df.iterrows():
        i = idx[r["site_a"]]
        j = idx[r["site_b"]]
        sim[i, j] = r["jaccard_similarity"]
        sim[j, i] = r["jaccard_similarity"]

    plt.figure(figsize=(6.5, 5.5))
    im = plt.imshow(sim, vmin=0, vmax=1, cmap="YlGnBu")
    plt.xticks([0, 1, 2], sites)
    plt.yticks([0, 1, 2], sites)
    for i in range(3):
        for j in range(3):
            plt.text(j, i, f"{sim[i, j]:.2f}", ha="center", va="center", color="black")
    plt.title("Jaccard-Ähnlichkeit der Standort-Artenpools")
    plt.colorbar(im, fraction=0.046, pad=0.04, label="Jaccard")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "site_pool_jaccard_heatmap.png", dpi=180)
    plt.close()

    # 3) PCoA auf Video x Taxa (presence/absence)
    all_taxa = sorted(set().union(*videos_df["taxa_set"].tolist()))
    tax_idx = {t: i for i, t in enumerate(all_taxa)}
    mat = np.zeros((len(videos_df), len(all_taxa)), dtype=int)
    for row_i, taxa in enumerate(videos_df["taxa_set"].tolist()):
        for t in taxa:
            mat[row_i, tax_idx[t]] = 1
    coords = pcoa_from_jaccard(mat)

    plt.figure(figsize=(8.5, 6.5))
    for s in ["utumbi", "milimani", "nursery"]:
        mask = videos_df["standort"].values == s
        plt.scatter(
            coords[mask, 0],
            coords[mask, 1],
            s=45,
            alpha=0.8,
            label=f"{s} (n={mask.sum()})",
            color=SITE_COLORS[s],
        )
    plt.axhline(0, color="grey", lw=0.8, alpha=0.4)
    plt.axvline(0, color="grey", lw=0.8, alpha=0.4)
    plt.xlabel("PCoA 1")
    plt.ylabel("PCoA 2")
    plt.title("Überlappung der Standorte (PCoA auf Jaccard-Distanzen)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "site_overlap_pcoa_jaccard.png", dpi=180)
    plt.close()

    # 4) Pairwise shared/unique Arten
    labels = []
    shared = []
    ua = []
    ub = []
    for _, r in overlap_df.iterrows():
        labels.append(f"{r['site_a']} vs {r['site_b']}")
        shared.append(r["intersection_taxa"])
        ua.append(r["unique_a"])
        ub.append(r["unique_b"])

    x = np.arange(len(labels))
    plt.figure(figsize=(9.5, 6))
    plt.bar(x, shared, label="geteilt", color="#4c78a8")
    plt.bar(x, ua, bottom=shared, label="nur site_a", color="#f58518")
    plt.bar(x, ub, bottom=np.array(shared) + np.array(ua), label="nur site_b", color="#54a24b")
    plt.xticks(x, labels, rotation=15)
    plt.ylabel("Anzahl Taxa")
    plt.title("Geteilte und einzigartige Taxa pro Standortpaar")
    plt.legend()
    plt.tight_layout()
    plt.savefig(FIG_DIR / "shared_unique_taxa_pairwise.png", dpi=180)
    plt.close()

    # 5) Dendrogramm der Standort-Distanzen (Jaccard-Distanz auf Artenpool)
    sites = ["utumbi", "milimani", "nursery"]
    dist_lookup = {}
    for _, r in overlap_df.iterrows():
        key = tuple(sorted([r["site_a"], r["site_b"]]))
        dist_lookup[key] = float(r["jaccard_distance"])

    condensed = np.array(
        [
            dist_lookup[tuple(sorted(["utumbi", "milimani"]))],
            dist_lookup[tuple(sorted(["utumbi", "nursery"]))],
            dist_lookup[tuple(sorted(["milimani", "nursery"]))],
        ],
        dtype=float,
    )

    z = linkage(condensed, method="average")
    plt.figure(figsize=(7.5, 5.5))
    dendrogram(z, labels=sites, color_threshold=0)
    plt.ylabel("Jaccard-Distanz")
    plt.title("Dendrogramm der Standortähnlichkeit")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "site_distance_dendrogram.png", dpi=180)
    plt.close()


def to_md(df: pd.DataFrame) -> str:
    if df.empty:
        return "Keine Daten."
    return df.to_markdown(index=False)


def build_markdown_report(
    videos_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    global_df: pd.DataFrame,
    pairwise_df: pd.DataFrame,
    strat_df: pd.DataFrame,
    overlap_df: pd.DataFrame,
) -> str:
    # Entscheidungsheuristik zur Replikat-Frage
    holm_sig_any = bool(pairwise_df.get("significant_0_05_holm", pd.Series(dtype=bool)).fillna(False).any())
    global_sig = bool(global_df.iloc[0]["significant_0_05"]) if not global_df.empty else False
    decision = (
        "Standorte **nicht** als direkte Replikate behandeln (signifikante Standorteffekte vorhanden)."
        if (holm_sig_any or global_sig)
        else "Standorte können mit Vorsicht als Replikate betrachtet werden (kein signifikanter Standorteffekt nachgewiesen)."
    )

    # Fokuszeilen
    def row_for(a: str, b: str) -> str:
        sel = pairwise_df[((pairwise_df["site_a"] == a) & (pairwise_df["site_b"] == b)) |
                          ((pairwise_df["site_a"] == b) & (pairwise_df["site_b"] == a))]
        if sel.empty:
            return f"- {a} vs {b}: kein Test möglich"
        r = sel.iloc[0]
        return (
            f"- {a} vs {b}: p={r['p_value']:.4g}, Holm-p={r['p_value_holm']:.4g}, "
            f"signifikant(Holm)={bool(r['significant_0_05_holm'])}, "
            f"Delta={r['cliffs_delta']:.3f}"
        )

    lines = []
    lines.append("# Standortvergleich (cut_47min)")
    lines.append("")
    lines.append("## Kurzfazit")
    lines.append(decision)
    lines.append("")
    lines.append("## Datengrundlage")
    lines.append(f"- Anzahl Videos gesamt: {len(videos_df)}")
    lines.append("- Standorte: Utumbi, Milimani, Nursery")
    lines.append("- Basis: normalized_reports/cut_47min")
    lines.append("- Metrik pro Video: Species Richness (unique Taxa; feeding/interested ausgeschlossen)")
    lines.append("")
    lines.append("## Schwerpunktvergleiche")
    lines.append(row_for("utumbi", "milimani"))
    lines.append(row_for("utumbi", "nursery"))
    lines.append(row_for("milimani", "nursery"))
    lines.append("")
    lines.append("## Köder-kontrollierter Test (Utumbi vs Milimani)")
    if strat_df.empty or pd.isna(strat_df.iloc[0]["p_value"]):
        lines.append("- Nicht berechenbar (keine gemeinsamen Köder mit Daten in beiden Standorten).")
    else:
        r = strat_df.iloc[0]
        lines.append(
            f"- {r['test']}: p={r['p_value']:.4g}, signifikant={bool(r['significant_0_05'])}, "
            f"Mittelwertdifferenz (Utumbi-Milimani)={r['stat_mean_diff']:.3f}"
        )
        lines.append(f"- {r['note']}")
    lines.append("")
    lines.append("## Statistik-Tabellen")
    lines.append("### Deskriptive Statistik je Standort")
    lines.append(to_md(summary_df))
    lines.append("")
    lines.append("### Globaltest über alle 3 Standorte")
    lines.append(to_md(global_df))
    lines.append("")
    lines.append("### Paarweise Standorttests")
    lines.append(to_md(pairwise_df))
    lines.append("")
    lines.append("### Artenpool-Überlappung")
    lines.append(to_md(overlap_df))
    lines.append("")
    lines.append("## Grafiken")
    lines.append("- figures/species_richness_by_site_boxplot.png")
    lines.append("- figures/site_pool_jaccard_heatmap.png")
    lines.append("- figures/site_overlap_pcoa_jaccard.png")
    lines.append("- figures/shared_unique_taxa_pairwise.png")
    lines.append("- figures/site_distance_dendrogram.png")
    lines.append("")
    lines.append("## Interpretation zur Replikat-Frage")
    lines.append("- Wenn global oder paarweise (Holm-korrigiert) signifikant: Standorteffekt spricht gegen Replikatannahme.")
    lines.append("- Wenn nicht signifikant, aber Überlappung gering (niedriger Jaccard) oder klare Cluster in PCoA: ebenfalls Vorsicht bei Replikatannahme.")

    return "\n".join(lines) + "\n"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    csv_files = sorted(CORAL_REEF_DIR.glob("*.csv")) + sorted(NURSERY_DIR.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError("Keine CSV-Dateien unter normalized_reports/cut_47min gefunden.")

    records = [load_video_data(p) for p in csv_files]
    videos_df = pd.DataFrame(records)

    keep_sites = {"utumbi", "milimani", "nursery"}
    videos_df = videos_df[videos_df["standort"].isin(keep_sites)].copy()
    videos_df = videos_df.sort_values(["standort", "date", "filename"]).reset_index(drop=True)

    summary_df = (
        videos_df.groupby("standort")["species_richness"]
        .agg(n="count", mean="mean", median="median", std="std", min="min", max="max")
        .reset_index()
        .sort_values("standort")
    )
    summary_df["std"] = summary_df["std"].fillna(0.0)

    grouped = [
        videos_df.loc[videos_df["standort"] == s, "species_richness"].astype(float).values
        for s in ["utumbi", "milimani", "nursery"]
    ]
    h_stat, p_val = stats.kruskal(*grouped)
    global_df = pd.DataFrame(
        [
            {
                "test": "Kruskal-Wallis (species_richness ~ standort)",
                "groups": "utumbi, milimani, nursery",
                "h_stat": float(h_stat),
                "p_value": float(p_val),
                "significant_0_05": bool(p_val < ALPHA),
                "sig_label": significance_label(float(p_val)),
            }
        ]
    )

    pairwise_df = pairwise_site_tests(videos_df)
    strat_result = stratified_permutation_utumbi_vs_milimani(videos_df, n_perm=20000)
    strat_df = pd.DataFrame([strat_result])

    overlap_df, site_sets = compute_site_pool_overlap(videos_df)

    videos_export = videos_df.copy()
    videos_export["n_taxa_set"] = videos_export["taxa_set"].map(len)
    videos_export = videos_export.drop(columns=["taxa_set"])

    videos_export.to_csv(OUT_DIR / "standortvergleich_video_level.csv", index=False)
    summary_df.to_csv(OUT_DIR / "standortvergleich_summary_stats.csv", index=False)
    global_df.to_csv(OUT_DIR / "standortvergleich_global_test.csv", index=False)
    pairwise_df.to_csv(OUT_DIR / "standortvergleich_pairwise_tests.csv", index=False)
    strat_df.to_csv(OUT_DIR / "standortvergleich_utumbi_milimani_stratified_test.csv", index=False)
    overlap_df.to_csv(OUT_DIR / "standortvergleich_species_pool_overlap.csv", index=False)

    create_figures(videos_df, overlap_df, site_sets)

    report_md = build_markdown_report(videos_df, summary_df, global_df, pairwise_df, strat_df, overlap_df)
    (OUT_DIR / "standortvergleich.md").write_text(report_md, encoding="utf-8")

    print("Standortvergleich abgeschlossen.")
    print(f"Ergebnisse: {OUT_DIR}")


if __name__ == "__main__":
    main()
