#!/usr/bin/env python3
from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Sequence, Set, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min"
CORAL_REEF_DIR = CUT_ROOT / "Annotation_reports_coral_reef"
NURSERY_DIR = CUT_ROOT / "Annotation_reports_Nursery"

OUT_DIR = ROOT / "results" / "composition_robustness"
PLOT_DIR = ROOT / "results" / "ergaenzende_statistische_grafiken"

OUT_PERMDISP = OUT_DIR / "permdisp_site_by_bait.csv"
OUT_PERMDISP_ANOVA = OUT_DIR / "permdisp_site_anova.csv"
OUT_RARE = OUT_DIR / "rarefaction_standardized_by_bait.csv"
OUT_RARE_NO_CONTROL = OUT_DIR / "rarefaction_standardized_by_bait_no_control.csv"
OUT_RARE_TYPE = OUT_DIR / "rarefaction_standardized_by_bait_type.csv"
OUT_REPORT = OUT_DIR / "composition_robustness_open_tests.md"

FIG_PERMDISP = PLOT_DIR / "12_permdisp_dispersion_by_site.png"
FIG_RARE = PLOT_DIR / "13_rarefaction_standardized_richness.png"

TARGET_SITES = ["milimani", "utumbi", "nursery"]
FISH_BAITS = {"mackerel", "fischmix"}
ALGAE_BAITS = {"ulva_gutweed", "ulva_salad", "sargassum", "algaemix", "algae_strings"}
N_PERM = 5000
N_RARE_REPS = 4000
SEED = 42


def clean_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in {"", "nan", "none", "null"}:
        return ""
    return text


def is_truthy(value: object) -> bool:
    if value is None:
        return False
    text = str(value).strip().lower()
    return text not in {"", "0", "false", "f", "no", "n", "none", "null", "nan"}


def parse_video_metadata(filename: str) -> Tuple[str, str, str]:
    stem = filename.replace(".csv", "")
    parts = stem.split("-", 2)
    if len(parts) < 3:
        return "", "unknown", "unknown"
    date, standort, koeder = parts
    return date, standort.lower(), koeder.lower()


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


def load_video_taxa(csv_path: Path) -> Dict[str, object]:
    raw = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")
    taxa_set: Set[str] = set()
    for _, row in raw.iterrows():
        if is_truthy(row.get("feeding", "")) or is_truthy(row.get("interested", "")):
            continue
        key = build_taxon_key(row)
        if key:
            taxa_set.add(key)

    date, standort, koeder = parse_video_metadata(csv_path.name)
    return {
        "filename": csv_path.name,
        "date": date,
        "standort": standort,
        "koeder": koeder,
        "taxa_set": taxa_set,
        "species_richness": len(taxa_set),
    }


def load_all_videos() -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    for csv_path in sorted(CORAL_REEF_DIR.glob("*.csv")):
        rows.append(load_video_taxa(csv_path))
    for csv_path in sorted(NURSERY_DIR.glob("*.csv")):
        rows.append(load_video_taxa(csv_path))
    df = pd.DataFrame(rows)
    return df[df["standort"].isin(TARGET_SITES)].copy().reset_index(drop=True)


def build_binary_matrix(site_df: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray, List[Set[str]]]:
    taxa_universe = sorted(set().union(*site_df["taxa_set"].tolist()))
    taxa_index = {t: i for i, t in enumerate(taxa_universe)}
    n = len(site_df)
    m = len(taxa_universe)

    mat = np.zeros((n, m), dtype=np.uint8)
    taxa_sets: List[Set[str]] = []
    for i, taxa in enumerate(site_df["taxa_set"].tolist()):
        taxa_sets.append(set(taxa))
        for key in taxa:
            j = taxa_index[key]
            mat[i, j] = 1
    groups = site_df["koeder"].to_numpy()
    return mat, groups, taxa_sets


def jaccard_distance_matrix(binary_matrix: np.ndarray) -> np.ndarray:
    n = binary_matrix.shape[0]
    dist = np.zeros((n, n), dtype=float)
    for i in range(n):
        a = binary_matrix[i]
        for j in range(i + 1, n):
            b = binary_matrix[j]
            union = np.logical_or(a, b).sum()
            if union == 0:
                d = 0.0
            else:
                inter = np.logical_and(a, b).sum()
                d = 1.0 - (inter / union)
            dist[i, j] = d
            dist[j, i] = d
    return dist


def pcoa(distance_matrix: np.ndarray) -> np.ndarray:
    n = distance_matrix.shape[0]
    a = -0.5 * (distance_matrix ** 2)
    h = np.eye(n) - np.ones((n, n)) / n
    b = h @ a @ h
    evals, evecs = np.linalg.eigh(b)
    idx = np.argsort(evals)[::-1]
    evals = evals[idx]
    evecs = evecs[:, idx]
    pos = evals > 1e-12
    if not np.any(pos):
        return np.zeros((n, 1), dtype=float)
    return evecs[:, pos] * np.sqrt(evals[pos])


def distances_to_group_centroid(coords: np.ndarray, groups: np.ndarray) -> np.ndarray:
    out = np.zeros(len(groups), dtype=float)
    for g in pd.unique(groups):
        idx = np.where(groups == g)[0]
        center = coords[idx].mean(axis=0)
        out[idx] = np.sqrt(np.sum((coords[idx] - center) ** 2, axis=1))
    return out


def one_way_f_stat(values: np.ndarray, groups: np.ndarray) -> float:
    overall_mean = float(np.mean(values))
    uniq = pd.unique(groups)
    k = len(uniq)
    n = len(values)
    if n <= k or k < 2:
        return math.nan

    ss_between = 0.0
    ss_within = 0.0
    for g in uniq:
        idx = groups == g
        vg = values[idx]
        if len(vg) == 0:
            continue
        mu = float(np.mean(vg))
        ss_between += len(vg) * (mu - overall_mean) ** 2
        ss_within += float(np.sum((vg - mu) ** 2))

    dfb = k - 1
    dfw = n - k
    if dfb <= 0 or dfw <= 0 or ss_within <= 0:
        return math.nan
    return (ss_between / dfb) / (ss_within / dfw)


def permanova_dispersion_test(distances: np.ndarray, groups: np.ndarray, n_perm: int, rng: np.random.Generator) -> Tuple[float, float]:
    f_obs = one_way_f_stat(distances, groups)
    if not np.isfinite(f_obs):
        return math.nan, math.nan
    ge = 0
    for _ in range(n_perm):
        f_perm = one_way_f_stat(distances, rng.permutation(groups))
        if np.isfinite(f_perm) and f_perm >= f_obs:
            ge += 1
    p = (ge + 1) / (n_perm + 1)
    return float(f_obs), float(p)


def bh_adjust(p_vals: Sequence[float]) -> np.ndarray:
    p = np.asarray(p_vals, dtype=float)
    mask = np.isfinite(p)
    out = np.full_like(p, np.nan)
    if not np.any(mask):
        return out

    v = p[mask]
    m = len(v)
    order = np.argsort(v)
    ranked = v[order]
    q = ranked * m / (np.arange(m) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.clip(q, 0.0, 1.0)
    q_unsorted = np.empty_like(q)
    q_unsorted[order] = q
    out[np.where(mask)[0]] = q_unsorted
    return out


def holm_adjust(p_vals: Sequence[float]) -> np.ndarray:
    p = np.asarray(p_vals, dtype=float)
    mask = np.isfinite(p)
    out = np.full_like(p, np.nan)
    if not np.any(mask):
        return out
    v = p[mask]
    m = len(v)
    order = np.argsort(v)
    adj_ordered = np.zeros(m, dtype=float)
    for i, idx in enumerate(order):
        adj_ordered[i] = min(1.0, (m - i) * v[idx])
    adj_ordered = np.maximum.accumulate(adj_ordered)
    adj = np.empty_like(adj_ordered)
    adj[order] = adj_ordered
    out[np.where(mask)[0]] = adj
    return out


def rarefied_union_richness(
    taxa_sets: Sequence[Set[str]],
    k: int,
    n_rep: int,
    rng: np.random.Generator,
) -> Tuple[float, float, float]:
    idx = np.arange(len(taxa_sets))
    vals = np.zeros(n_rep, dtype=float)
    for i in range(n_rep):
        chosen = rng.choice(idx, size=k, replace=False)
        union: Set[str] = set()
        for j in chosen:
            union |= taxa_sets[int(j)]
        vals[i] = float(len(union))
    mean = float(np.mean(vals))
    low = float(np.percentile(vals, 2.5))
    high = float(np.percentile(vals, 97.5))
    return mean, low, high


def run_permdisp(videos_df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    rng = np.random.default_rng(SEED)
    detail_rows: List[Dict[str, object]] = []
    site_rows: List[Dict[str, object]] = []

    for site in TARGET_SITES:
        site_df = videos_df[videos_df["standort"] == site].copy().reset_index(drop=True)
        if site_df["koeder"].nunique() < 2 or len(site_df) < 4:
            continue

        mat, groups, _ = build_binary_matrix(site_df)
        dist = jaccard_distance_matrix(mat)
        coords = pcoa(dist)
        d_cent = distances_to_group_centroid(coords, groups)

        f_stat, p_val = permanova_dispersion_test(d_cent, groups, n_perm=N_PERM, rng=rng)

        site_rows.append(
            {
                "standort": site,
                "n_videos": int(len(site_df)),
                "n_koeder": int(site_df["koeder"].nunique()),
                "f_stat": f_stat,
                "p_value": p_val,
            }
        )

        for bait in sorted(site_df["koeder"].unique()):
            idx = np.where(groups == bait)[0]
            vals = d_cent[idx]
            detail_rows.append(
                {
                    "standort": site,
                    "koeder": bait,
                    "n_videos": int(len(idx)),
                    "mean_distance_to_centroid": float(np.mean(vals)),
                    "median_distance_to_centroid": float(np.median(vals)),
                    "sd_distance_to_centroid": float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0,
                }
            )

    per_site = pd.DataFrame(site_rows).sort_values("standort").reset_index(drop=True)
    if not per_site.empty:
        per_site["q_value_bh"] = bh_adjust(per_site["p_value"].to_numpy())
        per_site["p_value_holm"] = holm_adjust(per_site["p_value"].to_numpy())
        per_site["significant_0_05"] = per_site["p_value"] < 0.05
        per_site["significant_bh_0_05"] = per_site["q_value_bh"] < 0.05
    detail = pd.DataFrame(detail_rows).sort_values(["standort", "koeder"]).reset_index(drop=True)
    return detail, per_site


def run_rarefaction(videos_df: pd.DataFrame, exclude_control: bool = False) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    work_df = videos_df.copy()
    if exclude_control:
        work_df = work_df[work_df["koeder"] != "control"].copy()

    rows: List[Dict[str, object]] = []
    for site in TARGET_SITES:
        site_df = work_df[work_df["standort"] == site].copy()
        counts = site_df.groupby("koeder").size().sort_index()
        if counts.empty:
            continue
        k = int(counts.min())
        for bait, part in site_df.groupby("koeder"):
            taxa_sets = [set(x) for x in part["taxa_set"].tolist()]
            mean_r, low_r, high_r = rarefied_union_richness(
                taxa_sets=taxa_sets,
                k=k,
                n_rep=N_RARE_REPS,
                rng=rng,
            )
            rows.append(
                {
                    "standort": site,
                    "koeder": bait,
                    "n_videos": int(len(part)),
                    "k_standardized_videos": k,
                    "rarefied_union_richness_mean": mean_r,
                    "rarefied_union_richness_ci95_low": low_r,
                    "rarefied_union_richness_ci95_high": high_r,
                    "observed_union_richness": int(len(set().union(*taxa_sets))),
                    "exclude_control": bool(exclude_control),
                }
            )
    return pd.DataFrame(rows).sort_values(["standort", "rarefied_union_richness_mean"], ascending=[True, False]).reset_index(drop=True)


def map_bait_type(koeder: str) -> str:
    if koeder in FISH_BAITS:
        return "fish"
    if koeder in ALGAE_BAITS:
        return "algae"
    return "other"


def run_rarefaction_bait_type(videos_df: pd.DataFrame) -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    df = videos_df.copy()
    df["bait_type"] = df["koeder"].map(map_bait_type)
    df = df[df["bait_type"].isin(["fish", "algae"])].copy()

    rows: List[Dict[str, object]] = []
    for site in TARGET_SITES:
        site_df = df[df["standort"] == site].copy()
        counts = site_df.groupby("bait_type").size().sort_index()
        if set(counts.index.tolist()) != {"algae", "fish"}:
            continue
        k = int(counts.min())

        for bait_type, part in site_df.groupby("bait_type"):
            taxa_sets = [set(x) for x in part["taxa_set"].tolist()]
            mean_r, low_r, high_r = rarefied_union_richness(
                taxa_sets=taxa_sets,
                k=k,
                n_rep=N_RARE_REPS,
                rng=rng,
            )
            rows.append(
                {
                    "standort": site,
                    "bait_type": bait_type,
                    "n_videos": int(len(part)),
                    "k_standardized_videos": k,
                    "rarefied_union_richness_mean": mean_r,
                    "rarefied_union_richness_ci95_low": low_r,
                    "rarefied_union_richness_ci95_high": high_r,
                    "observed_union_richness": int(len(set().union(*taxa_sets))),
                }
            )

    return pd.DataFrame(rows).sort_values(["standort", "bait_type"]).reset_index(drop=True)


def make_plots(permdisp_detail: pd.DataFrame, rare: pd.DataFrame) -> None:
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 12,
            "axes.labelsize": 11,
            "legend.fontsize": 8,
            "figure.dpi": 220,
        }
    )

    # Plot 12: mean distance-to-centroid per bait and site
    fig, ax = plt.subplots(figsize=(10, 5.2))
    sites = TARGET_SITES
    site_pos = np.arange(len(sites))
    width = 0.12

    for s_i, site in enumerate(sites):
        sub = permdisp_detail[permdisp_detail["standort"] == site].sort_values("koeder")
        if sub.empty:
            continue
        n = len(sub)
        offsets = (np.arange(n) - (n - 1) / 2.0) * width
        for off, row in zip(offsets, sub.itertuples(index=False)):
            ax.bar(
                site_pos[s_i] + off,
                row.mean_distance_to_centroid,
                width=width * 0.9,
                alpha=0.8,
                label=f"{site}:{row.koeder}",
            )

    ax.set_xticks(site_pos)
    ax.set_xticklabels(["Milimani", "Utumbi", "Nursery"])
    ax.set_ylabel("Mittlere Distanz zum Gruppenzentrum")
    ax.set_title("PERMDISP: Streuung der Taxa-Komposition pro Standort")
    ax.grid(axis="y", alpha=0.25)
    handles, labels = ax.get_legend_handles_labels()
    uniq = dict(zip(labels, handles))
    ax.legend(uniq.values(), uniq.keys(), loc="upper left", bbox_to_anchor=(1.01, 1.0), frameon=False)
    fig.tight_layout()
    fig.savefig(FIG_PERMDISP, dpi=220, bbox_inches="tight")
    plt.close(fig)

    # Plot 13: rarefied richness with CI per bait within each site
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.5), sharey=True)
    for ax, site in zip(axes, sites):
        sub = rare[rare["standort"] == site].sort_values("rarefied_union_richness_mean", ascending=False)
        if sub.empty:
            ax.set_axis_off()
            continue
        x = np.arange(len(sub))
        mean_v = sub["rarefied_union_richness_mean"].to_numpy(dtype=float)
        low_v = sub["rarefied_union_richness_ci95_low"].to_numpy(dtype=float)
        high_v = sub["rarefied_union_richness_ci95_high"].to_numpy(dtype=float)
        yerr = np.vstack([mean_v - low_v, high_v - mean_v])

        ax.bar(x, mean_v, color="#4c78a8", alpha=0.85)
        ax.errorbar(x, mean_v, yerr=yerr, fmt="none", ecolor="black", capsize=3, linewidth=1)
        ax.set_xticks(x)
        ax.set_xticklabels(sub["koeder"].tolist(), rotation=35, ha="right")
        ax.set_title(f"{site} (k={int(sub['k_standardized_videos'].iloc[0])})")
        ax.grid(axis="y", alpha=0.25)

    axes[0].set_ylabel("Rarefied Union Richness")
    fig.suptitle("Rarefaction: standardisierte Taxa-Richness je Koeder")
    fig.tight_layout()
    fig.savefig(FIG_RARE, dpi=220, bbox_inches="tight")
    plt.close(fig)


def write_report(
    per_site: pd.DataFrame,
    rare_all: pd.DataFrame,
    rare_no_control: pd.DataFrame,
    rare_type: pd.DataFrame,
) -> None:
    lines: List[str] = []
    lines.append("# Kompositions-Robustheit: offene Zusatztests (PERMDISP + Rarefaction)")
    lines.append("")
    lines.append("Stand: 2026-08-16")
    lines.append("")
    lines.append("## Ziel")
    lines.append("")
    lines.append("- Offener Punkt 1: PERMDISP als Streuungspruefung ergaenzend zur PERMANOVA.")
    lines.append("- Offener Punkt 2: Rarefaction/Sampling-Normalisierung fuer ungleiche Videozahlen je Koeder.")
    lines.append("")
    lines.append("## Methode")
    lines.append("")
    lines.append("- Datengrundlage: normalized_reports/cut_47min, getrennt nach Standorten.")
    lines.append("- Taxa-Komposition: Presence/Absence je Video mit Jaccard-Distanzen.")
    lines.append("- PERMDISP: Distanz jedes Videos zum Koeder-Zentrum im PCoA-Raum; Signifikanz per Permutationstest (5000).")
    lines.append("- Rarefaction: Monte-Carlo-Subsampling je Koeder auf k = minimale Videozahl je Standort (4000 Wiederholungen).")
    lines.append("")
    lines.append("## PERMDISP pro Standort")
    lines.append("")
    if per_site.empty:
        lines.append("Keine berechenbaren PERMDISP-Resultate.")
    else:
        lines.append(per_site.to_markdown(index=False, floatfmt=".6g"))
    lines.append("")
    lines.append("## Rarefied Richness pro Koeder (alle Koeder inkl. control)")
    lines.append("")
    if rare_all.empty:
        lines.append("Keine berechenbaren Rarefaction-Resultate.")
    else:
        show = rare_all[
            [
                "standort",
                "koeder",
                "n_videos",
                "k_standardized_videos",
                "rarefied_union_richness_mean",
                "rarefied_union_richness_ci95_low",
                "rarefied_union_richness_ci95_high",
                "observed_union_richness",
            ]
        ]
        lines.append(show.to_markdown(index=False, floatfmt=".4f"))

    lines.append("")
    lines.append("## Rarefied Richness pro Koeder (Sensitivitaet ohne control)")
    lines.append("")
    if rare_no_control.empty:
        lines.append("Keine berechenbaren Rarefaction-Resultate ohne control.")
    else:
        show_nc = rare_no_control[
            [
                "standort",
                "koeder",
                "n_videos",
                "k_standardized_videos",
                "rarefied_union_richness_mean",
                "rarefied_union_richness_ci95_low",
                "rarefied_union_richness_ci95_high",
                "observed_union_richness",
            ]
        ]
        lines.append(show_nc.to_markdown(index=False, floatfmt=".4f"))

    lines.append("")
    lines.append("## Rarefied Richness fish vs algae (bait-type Ebene)")
    lines.append("")
    if rare_type.empty:
        lines.append("Keine berechenbaren fish-vs-algae-Rarefaction-Resultate.")
    else:
        show_type = rare_type[
            [
                "standort",
                "bait_type",
                "n_videos",
                "k_standardized_videos",
                "rarefied_union_richness_mean",
                "rarefied_union_richness_ci95_low",
                "rarefied_union_richness_ci95_high",
                "observed_union_richness",
            ]
        ]
        lines.append(show_type.to_markdown(index=False, floatfmt=".4f"))

    lines.append("")
    lines.append("## Kurzinterpretation")
    lines.append("")
    if per_site.empty:
        lines.append("- PERMDISP konnte nicht stabil berechnet werden.")
    else:
        any_sig = bool((per_site["q_value_bh"] < 0.05).any())
        if any_sig:
            lines.append("- Mindestens ein Standort zeigt signifikante Streuungsunterschiede zwischen Koedern (PERMDISP, BH-korrigiert).")
        else:
            lines.append("- Kein Standort zeigt robuste Streuungsunterschiede zwischen Koedern nach BH-Korrektur (PERMDISP).")

    lines.append("- Rarefaction reduziert den Einfluss ungleicher Stichprobengroessen und zeigt, welche Koeder auch bei gleicher Videozahl die hoehere Taxa-Abdeckung behalten.")
    lines.append("- Die Sensitivitaet ohne control ist informativer, wenn control nur mit n=1 vorliegt (sonst wird k auf 1 gedrueckt).")
    lines.append("- Diese Zusatztests trennen besser zwischen Lageeffekt (PERMANOVA) und Streuung/Sampling-Effekt.")

    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PLOT_DIR.mkdir(parents=True, exist_ok=True)

    videos_df = load_all_videos()
    permdisp_detail, permdisp_site = run_permdisp(videos_df)
    rare = run_rarefaction(videos_df, exclude_control=False)
    rare_no_control = run_rarefaction(videos_df, exclude_control=True)
    rare_type = run_rarefaction_bait_type(videos_df)

    permdisp_detail.to_csv(OUT_PERMDISP, index=False)
    permdisp_site.to_csv(OUT_PERMDISP_ANOVA, index=False)
    rare.to_csv(OUT_RARE, index=False)
    rare_no_control.to_csv(OUT_RARE_NO_CONTROL, index=False)
    rare_type.to_csv(OUT_RARE_TYPE, index=False)

    plot_df = rare_no_control if not rare_no_control.empty else rare
    make_plots(permdisp_detail, plot_df)
    write_report(permdisp_site, rare, rare_no_control, rare_type)

    print(f"Wrote: {OUT_PERMDISP}")
    print(f"Wrote: {OUT_PERMDISP_ANOVA}")
    print(f"Wrote: {OUT_RARE}")
    print(f"Wrote: {OUT_RARE_NO_CONTROL}")
    print(f"Wrote: {OUT_RARE_TYPE}")
    print(f"Wrote: {OUT_REPORT}")
    print(f"Wrote: {FIG_PERMDISP}")
    print(f"Wrote: {FIG_RARE}")


if __name__ == "__main__":
    main()
