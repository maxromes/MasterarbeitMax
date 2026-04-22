from __future__ import annotations

import ast
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "results" / "nursery_methodik_vergleich" / "data" / "nursery_video_metrics.csv"
OUT_DIR = ROOT / "results" / "nursery_methodik_vergleich" / "taxa_composition"

ALPHA = 0.05


def parse_taxon_dict(value: str) -> dict[str, float]:
    if pd.isna(value) or value == "":
        return {}
    parsed = ast.literal_eval(value)
    if not isinstance(parsed, dict):
        return {}
    return {str(k): float(v) for k, v in parsed.items() if float(v) > 0}


def build_matrix(df: pd.DataFrame, dict_col: str) -> pd.DataFrame:
    taxa = sorted(
        {
            taxon
            for raw in df[dict_col].fillna("{}")
            for taxon in parse_taxon_dict(raw).keys()
        }
    )
    rows = []
    for _, row in df.iterrows():
        d = parse_taxon_dict(row[dict_col])
        rows.append([d.get(t, 0.0) for t in taxa])
    mat = pd.DataFrame(rows, columns=taxa)
    mat.insert(0, "koeder", df["koeder"].values)
    mat.insert(0, "filename", df["filename"].values)
    return mat


def to_relative(arr: np.ndarray) -> np.ndarray:
    sums = arr.sum(axis=1, keepdims=True)
    return np.divide(arr, sums, out=np.zeros_like(arr), where=sums != 0)


def bray_curtis_matrix(x: np.ndarray) -> np.ndarray:
    n = x.shape[0]
    d = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(i + 1, n):
            num = np.abs(x[i] - x[j]).sum()
            den = (x[i] + x[j]).sum()
            val = 0.0 if den == 0 else num / den
            d[i, j] = val
            d[j, i] = val
    return d


def permanova_f_stat(dist: np.ndarray, groups: np.ndarray) -> float:
    n = len(groups)
    uniq = np.unique(groups)
    k = len(uniq)
    if k < 2 or n <= k:
        return np.nan

    tri = np.triu_indices(n, 1)
    sst = np.sum(dist[tri] ** 2) / n

    ssw = 0.0
    for g in uniq:
        idx = np.where(groups == g)[0]
        ng = len(idx)
        if ng < 2:
            continue
        d_g = dist[np.ix_(idx, idx)]
        tri_g = np.triu_indices(ng, 1)
        ssw += np.sum(d_g[tri_g] ** 2) / ng

    ssa = sst - ssw
    dfa = k - 1
    dfw = n - k
    if dfw <= 0:
        return np.nan
    msw = ssw / dfw
    if msw <= 0:
        return np.inf
    return (ssa / dfa) / msw


def permanova_components(dist: np.ndarray, groups: np.ndarray) -> tuple[float, float, float]:
    n = len(groups)
    uniq = np.unique(groups)
    tri = np.triu_indices(n, 1)
    sst = np.sum(dist[tri] ** 2) / n

    ssw = 0.0
    for g in uniq:
        idx = np.where(groups == g)[0]
        ng = len(idx)
        if ng < 2:
            continue
        d_g = dist[np.ix_(idx, idx)]
        tri_g = np.triu_indices(ng, 1)
        ssw += np.sum(d_g[tri_g] ** 2) / ng

    ssa = sst - ssw
    return ssa, ssw, sst


def permanova(dist: np.ndarray, groups: np.ndarray, permutations: int = 9999, seed: int = 42) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    f_obs = permanova_f_stat(dist, groups)
    if not np.isfinite(f_obs):
        return f_obs, np.nan

    ge = 0
    for _ in range(permutations):
        f_perm = permanova_f_stat(dist, rng.permutation(groups))
        if np.isfinite(f_perm) and f_perm >= f_obs:
            ge += 1
    p = (ge + 1) / (permutations + 1)
    return float(f_obs), float(p)


def permanova_with_r2(
    dist: np.ndarray, groups: np.ndarray, permutations: int = 9999, seed: int = 42
) -> tuple[float, float, float]:
    f_obs, p_value = permanova(dist, groups, permutations=permutations, seed=seed)
    ssa, _, sst = permanova_components(dist, groups)
    r2 = float(ssa / sst) if sst > 0 else np.nan
    return f_obs, p_value, r2


def bootstrap_pairwise_r2_ci(
    mat: pd.DataFrame,
    group_col: str,
    n_boot: int = 4000,
    seed: int = 123,
) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    groups = sorted(mat[group_col].unique())
    cols = [c for c in mat.columns if c not in {"filename", group_col}]

    boot_r2 = []
    for _ in range(n_boot):
        sampled_parts = []
        for g in groups:
            part = mat[mat[group_col] == g]
            idx = rng.choice(part.index.to_numpy(), size=len(part), replace=True)
            sampled_parts.append(part.loc[idx])
        sampled = pd.concat(sampled_parts, axis=0, ignore_index=True)
        arr = sampled[cols].to_numpy(dtype=float)
        rel = to_relative(arr)
        dist = bray_curtis_matrix(rel)
        ssa, _, sst = permanova_components(dist, sampled[group_col].to_numpy())
        r2 = ssa / sst if sst > 0 else np.nan
        if np.isfinite(r2):
            boot_r2.append(float(r2))

    if len(boot_r2) == 0:
        return np.nan, np.nan
    return float(np.percentile(boot_r2, 2.5)), float(np.percentile(boot_r2, 97.5))


def holm_correction(p_values: list[float]) -> list[float]:
    m = len(p_values)
    order = np.argsort(p_values)
    adjusted = np.empty(m, dtype=float)
    running_max = 0.0
    for i, idx in enumerate(order):
        adj = (m - i) * p_values[idx]
        running_max = max(running_max, adj)
        adjusted[idx] = min(running_max, 1.0)
    return adjusted.tolist()


def bh_correction(p_values: list[float]) -> list[float]:
    m = len(p_values)
    order = np.argsort(p_values)
    adjusted = np.empty(m, dtype=float)
    running_min = 1.0
    for i in range(m - 1, -1, -1):
        idx = order[i]
        rank = i + 1
        adj = p_values[idx] * m / rank
        running_min = min(running_min, adj)
        adjusted[idx] = min(running_min, 1.0)
    return adjusted.tolist()


def pcoa_coordinates(dist: np.ndarray, n_components: int = 2) -> np.ndarray:
    n = dist.shape[0]
    d2 = dist**2
    j = np.eye(n) - np.ones((n, n)) / n
    b = -0.5 * j @ d2 @ j
    eigvals, eigvecs = np.linalg.eigh(b)
    order = np.argsort(eigvals)[::-1]
    eigvals = eigvals[order]
    eigvecs = eigvecs[:, order]
    positive = eigvals > 1e-12
    eigvals = eigvals[positive]
    eigvecs = eigvecs[:, positive]
    if len(eigvals) == 0:
        return np.zeros((n, n_components))
    coords = eigvecs[:, :n_components] * np.sqrt(eigvals[:n_components])
    if coords.shape[1] < n_components:
        coords = np.hstack([coords, np.zeros((n, n_components - coords.shape[1]))])
    return coords


def make_pcoa_plot(dist: np.ndarray, meta: pd.DataFrame, title: str, out_png: Path, out_svg: Path) -> None:
    coords = pcoa_coordinates(dist)
    palette = {
        "algae_strings": "#1f6f8b",
        "algaemix": "#e07a5f",
        "mackerel": "#3d405b",
        "control": "#6b7280",
    }

    fig, ax = plt.subplots(figsize=(8, 6), dpi=160)
    for koeder in sorted(meta["koeder"].unique()):
        idx = np.where(meta["koeder"].values == koeder)[0]
        ax.scatter(
            coords[idx, 0],
            coords[idx, 1],
            s=85,
            color=palette.get(koeder, "#4b5563"),
            edgecolor="white",
            linewidth=0.8,
            alpha=0.95,
            label=f"{koeder} (n={len(idx)})",
        )

    ax.axhline(0, color="#d1d5db", linewidth=1)
    ax.axvline(0, color="#d1d5db", linewidth=1)
    ax.set_title(title, fontsize=13, weight="bold")
    ax.set_xlabel("PCoA1")
    ax.set_ylabel("PCoA2")
    ax.grid(alpha=0.25, linestyle="--")
    ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(out_png)
    fig.savefig(out_svg)
    plt.close(fig)


def analyze_subset(df: pd.DataFrame, label: str, level: str, dict_col: str) -> dict[str, float | str | int]:
    mat = build_matrix(df, dict_col)
    numeric = mat.drop(columns=["filename", "koeder"]).to_numpy(dtype=float)
    rel = to_relative(numeric)
    dist = bray_curtis_matrix(rel)
    groups = mat["koeder"].to_numpy()

    f_stat, p_value, r2 = permanova_with_r2(dist, groups, permutations=9999, seed=77)
    return {
        "comparison": label,
        "level": level,
        "test": "PERMANOVA (Bray-Curtis)",
        "f_stat": f_stat,
        "p_value": p_value,
        "r2": r2,
        "n_videos": len(df),
        "groups": "|".join(sorted(df["koeder"].unique())),
    }


def pairwise_effects(df: pd.DataFrame, level: str, dict_col: str) -> pd.DataFrame:
    mats = build_matrix(df, dict_col)
    rows = []
    for i, (a, b) in enumerate(combinations(sorted(df["koeder"].unique()), 2), start=1):
        sub = mats[mats["koeder"].isin([a, b])].copy().reset_index(drop=True)
        arr = sub.drop(columns=["filename", "koeder"]).to_numpy(dtype=float)
        rel = to_relative(arr)
        dist = bray_curtis_matrix(rel)
        groups = sub["koeder"].to_numpy()
        f_stat, p_value, r2 = permanova_with_r2(dist, groups, permutations=9999, seed=500 + i)
        ci_low, ci_high = bootstrap_pairwise_r2_ci(sub, "koeder", n_boot=4000, seed=900 + i)
        rows.append(
            {
                "level": level,
                "group_a": a,
                "group_b": b,
                "f_stat": f_stat,
                "p_value": p_value,
                "r2": r2,
                "r2_ci_low": ci_low,
                "r2_ci_high": ci_high,
                "n_a": int((groups == a).sum()),
                "n_b": int((groups == b).sum()),
            }
        )

    out = pd.DataFrame(rows)
    if not out.empty:
        out["p_value_holm"] = holm_correction(out["p_value"].tolist())
        out["p_value_bh"] = bh_correction(out["p_value"].tolist())
        out["significant_raw"] = out["p_value"] < ALPHA
        out["significant_holm"] = out["p_value_holm"] < ALPHA
        out["significant_bh"] = out["p_value_bh"] < ALPHA
    return out


def main() -> None:
    df = pd.read_csv(DATA_FILE)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Inferenz nur auf den drei methodischen Baits; control n=1 bleibt explorativ.
    inf_df = df[df["koeder"].isin(["algae_strings", "algaemix", "mackerel"])].copy()

    subsets = {
        "strings_vs_mix": inf_df[inf_df["koeder"].isin(["algae_strings", "algaemix"])].copy(),
        "mix_vs_mackerel": inf_df[inf_df["koeder"].isin(["algaemix", "mackerel"])].copy(),
        "three_baits": inf_df.copy(),
    }

    rows = []
    for name, sub in subsets.items():
        rows.append(analyze_subset(sub, name, "species", "species_maxn_by_taxon"))
        rows.append(analyze_subset(sub, name, "family", "family_maxn_by_taxon"))

    results = pd.DataFrame(rows)
    results["p_value_holm"] = holm_correction(results["p_value"].tolist())
    results["p_value_bh"] = bh_correction(results["p_value"].tolist())
    results["significant_raw"] = results["p_value"] < ALPHA
    results["significant_holm"] = results["p_value_holm"] < ALPHA
    results["significant_bh"] = results["p_value_bh"] < ALPHA

    results.to_csv(OUT_DIR / "nursery_taxa_permanova.csv", index=False)

    pair_species = pairwise_effects(inf_df, "species", "species_maxn_by_taxon")
    pair_family = pairwise_effects(inf_df, "family", "family_maxn_by_taxon")
    pairwise = pd.concat([pair_species, pair_family], ignore_index=True)
    pairwise.to_csv(OUT_DIR / "nursery_taxa_pairwise_effects.csv", index=False)

    # Matrix export for transparency (three-baits set)
    species_mat = build_matrix(subsets["three_baits"], "species_maxn_by_taxon")
    family_mat = build_matrix(subsets["three_baits"], "family_maxn_by_taxon")
    species_mat.to_csv(OUT_DIR / "nursery_three_baits_species_matrix.csv", index=False)
    family_mat.to_csv(OUT_DIR / "nursery_three_baits_family_matrix.csv", index=False)

    # PCoA plots for visual separation (three-baits + optional control overlay)
    species_three_rel = to_relative(species_mat.drop(columns=["filename", "koeder"]).to_numpy(dtype=float))
    family_three_rel = to_relative(family_mat.drop(columns=["filename", "koeder"]).to_numpy(dtype=float))
    make_pcoa_plot(
        bray_curtis_matrix(species_three_rel),
        species_mat[["filename", "koeder"]],
        "Nursery bait methods: species composition (three baits)",
        OUT_DIR / "nursery_three_baits_species_pcoa.png",
        OUT_DIR / "nursery_three_baits_species_pcoa.svg",
    )
    make_pcoa_plot(
        bray_curtis_matrix(family_three_rel),
        family_mat[["filename", "koeder"]],
        "Nursery bait methods: family composition (three baits)",
        OUT_DIR / "nursery_three_baits_family_pcoa.png",
        OUT_DIR / "nursery_three_baits_family_pcoa.svg",
    )

    # Control-only exploratory distance to three-baits centroid (no significance test).
    control = df[df["koeder"] == "control"].copy()
    if not control.empty:
        combined = df[df["koeder"].isin(["algae_strings", "algaemix", "mackerel", "control"])].copy()
        species_all = build_matrix(combined, "species_maxn_by_taxon")
        rel_all = to_relative(species_all.drop(columns=["filename", "koeder"]).to_numpy(dtype=float))
        dist_all = bray_curtis_matrix(rel_all)
        idx_control = np.where(species_all["koeder"].to_numpy() == "control")[0]
        idx_non_control = np.where(species_all["koeder"].to_numpy() != "control")[0]
        mean_dist = float(dist_all[np.ix_(idx_control, idx_non_control)].mean())
        pd.DataFrame(
            [
                {
                    "note": "control is exploratory only (n=1)",
                    "mean_bray_curtis_distance_control_to_non_control": mean_dist,
                    "n_non_control_videos": int(len(idx_non_control)),
                }
            ]
        ).to_csv(OUT_DIR / "nursery_control_exploratory_distance.csv", index=False)

    summary_path = OUT_DIR / "nursery_taxa_composition_summary.md"
    with summary_path.open("w", encoding="utf-8") as f:
        f.write("# Nursery taxa composition by bait method\n\n")
        f.write("Data basis: results/nursery_methodik_vergleich/data/nursery_video_metrics.csv\n\n")
        f.write("Inference excludes control (n=1); control is reported exploratively only.\n\n")
        f.write("## PERMANOVA results (Bray-Curtis)\n")
        f.write(results.to_markdown(index=False))
        f.write("\n\n## Pairwise effects (PERMANOVA R2 with bootstrap CI)\n")
        f.write(pairwise.to_markdown(index=False))
        f.write("\n")

    print(f"Nursery taxa composition outputs written to: {OUT_DIR}")


if __name__ == "__main__":
    main()
