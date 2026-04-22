from __future__ import annotations

import ast
from itertools import combinations
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "results" / "mackerel_standortvergleich" / "data" / "mackerel_video_metrics.csv"
OUT_DIR = ROOT / "results" / "mackerel_standortvergleich" / "taxa_composition"

SITE_ORDER = ["milimani", "utumbi", "nursery"]
SITE_COLORS = {
    "milimani": "#1f6f8b",
    "utumbi": "#e07a5f",
    "nursery": "#3d405b",
}


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
    mat.insert(0, "standort", df["standort"].values)
    mat.insert(0, "filename", df["filename"].values)
    return mat


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
        tri_g = np.triu_indices(ng, 1)
        d_g = dist[np.ix_(idx, idx)]
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
    pos = eigvals > 1e-12
    eigvals = eigvals[pos]
    eigvecs = eigvecs[:, pos]
    if len(eigvals) == 0:
        return np.zeros((n, n_components))
    coords = eigvecs[:, :n_components] * np.sqrt(eigvals[:n_components])
    if coords.shape[1] < n_components:
        pad = np.zeros((n, n_components - coords.shape[1]))
        coords = np.hstack([coords, pad])
    return coords


def make_pcoa_plot(dist: np.ndarray, meta: pd.DataFrame, title: str, out_png: Path, out_svg: Path) -> None:
    coords = pcoa_coordinates(dist)
    fig, ax = plt.subplots(figsize=(8, 6), dpi=160)
    for site in SITE_ORDER:
        idx = np.where(meta["standort"].values == site)[0]
        if len(idx) == 0:
            continue
        ax.scatter(
            coords[idx, 0],
            coords[idx, 1],
            s=85,
            color=SITE_COLORS[site],
            edgecolor="white",
            linewidth=0.8,
            label=f"{site} (n={len(idx)})",
            alpha=0.95,
        )
    ax.axhline(0, color="#d1d5db", linewidth=1)
    ax.axvline(0, color="#d1d5db", linewidth=1)
    ax.set_title(title, fontsize=14, weight="bold")
    ax.set_xlabel("PCoA1")
    ax.set_ylabel("PCoA2")
    ax.legend(frameon=False)
    ax.grid(alpha=0.25, linestyle="--")
    fig.tight_layout()
    fig.savefig(out_png)
    fig.savefig(out_svg)
    plt.close(fig)


def run_level(df: pd.DataFrame, dict_col: str, level_name: str, permutations: int = 9999) -> tuple[pd.DataFrame, pd.DataFrame]:
    mat = build_matrix(df, dict_col)
    numeric = mat.drop(columns=["filename", "standort"]).to_numpy(dtype=float)

    row_sums = numeric.sum(axis=1, keepdims=True)
    rel = np.divide(numeric, row_sums, out=np.zeros_like(numeric), where=row_sums != 0)
    dist = bray_curtis_matrix(rel)

    groups = mat["standort"].to_numpy()
    f_stat, p_value = permanova(dist, groups, permutations=permutations, seed=44)

    global_res = pd.DataFrame(
        [
            {
                "level": level_name,
                "test": "PERMANOVA (Bray-Curtis)",
                "f_stat": f_stat,
                "p_value": p_value,
                "permutations": permutations,
                "n_videos": len(mat),
            }
        ]
    )

    pair_rows = []
    for i, (a, b) in enumerate(combinations(SITE_ORDER, 2), start=1):
        sub = mat[mat["standort"].isin([a, b])].copy()
        sub_num = sub.drop(columns=["filename", "standort"]).to_numpy(dtype=float)
        sub_row_sums = sub_num.sum(axis=1, keepdims=True)
        sub_rel = np.divide(sub_num, sub_row_sums, out=np.zeros_like(sub_num), where=sub_row_sums != 0)
        sub_dist = bray_curtis_matrix(sub_rel)
        sub_groups = sub["standort"].to_numpy()
        f_pair, p_pair = permanova(sub_dist, sub_groups, permutations=permutations, seed=100 + i)
        pair_rows.append(
            {
                "level": level_name,
                "site_a": a,
                "site_b": b,
                "f_stat": f_pair,
                "p_value": p_pair,
                "n_a": int((sub_groups == a).sum()),
                "n_b": int((sub_groups == b).sum()),
            }
        )

    pair_df = pd.DataFrame(pair_rows)
    if not pair_df.empty:
        p_vals = pair_df["p_value"].to_list()
        pair_df["p_value_holm"] = holm_correction(p_vals)
        pair_df["p_value_bh"] = bh_correction(p_vals)
        pair_df["significant_raw"] = pair_df["p_value"] < 0.05
        pair_df["significant_holm"] = pair_df["p_value_holm"] < 0.05
        pair_df["significant_bh"] = pair_df["p_value_bh"] < 0.05

    return global_res, pair_df


def main() -> None:
    df = pd.read_csv(DATA_FILE)
    df = df[df["standort"].isin(SITE_ORDER)].copy()
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    global_species, pair_species = run_level(df, "species_maxn_by_taxon", "species")
    global_family, pair_family = run_level(df, "family_maxn_by_taxon", "family")

    global_all = pd.concat([global_species, global_family], ignore_index=True)
    global_all["p_value_holm"] = holm_correction(global_all["p_value"].to_list())
    global_all["p_value_bh"] = bh_correction(global_all["p_value"].to_list())
    global_all["significant_raw"] = global_all["p_value"] < 0.05
    global_all["significant_holm"] = global_all["p_value_holm"] < 0.05
    global_all["significant_bh"] = global_all["p_value_bh"] < 0.05

    pair_all = pd.concat([pair_species, pair_family], ignore_index=True)

    global_all.to_csv(OUT_DIR / "mackerel_taxa_permanova_global.csv", index=False)
    pair_all.to_csv(OUT_DIR / "mackerel_taxa_permanova_pairwise.csv", index=False)

    species_mat = build_matrix(df, "species_maxn_by_taxon")
    family_mat = build_matrix(df, "family_maxn_by_taxon")
    species_mat.to_csv(OUT_DIR / "mackerel_species_composition_matrix.csv", index=False)
    family_mat.to_csv(OUT_DIR / "mackerel_family_composition_matrix.csv", index=False)

    species_num = species_mat.drop(columns=["filename", "standort"]).to_numpy(dtype=float)
    family_num = family_mat.drop(columns=["filename", "standort"]).to_numpy(dtype=float)
    species_rel = np.divide(species_num, species_num.sum(axis=1, keepdims=True), out=np.zeros_like(species_num), where=species_num.sum(axis=1, keepdims=True) != 0)
    family_rel = np.divide(family_num, family_num.sum(axis=1, keepdims=True), out=np.zeros_like(family_num), where=family_num.sum(axis=1, keepdims=True) != 0)

    make_pcoa_plot(
        bray_curtis_matrix(species_rel),
        species_mat[["filename", "standort"]],
        "Mackerel: Taxa-Komposition (Species, Bray-Curtis PCoA)",
        OUT_DIR / "mackerel_species_composition_pcoa.png",
        OUT_DIR / "mackerel_species_composition_pcoa.svg",
    )
    make_pcoa_plot(
        bray_curtis_matrix(family_rel),
        family_mat[["filename", "standort"]],
        "Mackerel: Taxa-Komposition (Family, Bray-Curtis PCoA)",
        OUT_DIR / "mackerel_family_composition_pcoa.png",
        OUT_DIR / "mackerel_family_composition_pcoa.svg",
    )

    with (OUT_DIR / "mackerel_taxa_composition_summary.md").open("w", encoding="utf-8") as f:
        f.write("# Mackerel-Taxa-Komposition nach Standort\n\n")
        f.write("Test: PERMANOVA auf Bray-Curtis-Distanzen, basierend auf relativen Taxon-MaxN-Profilen pro Video.\n\n")
        f.write("## Globaler Test\n")
        f.write(global_all.to_markdown(index=False))
        f.write("\n\n## Paarweise Tests\n")
        f.write(pair_all.to_markdown(index=False))
        f.write("\n")

    print(f"Taxa-Kompositions-Analyse gespeichert in: {OUT_DIR}")


if __name__ == "__main__":
    main()
