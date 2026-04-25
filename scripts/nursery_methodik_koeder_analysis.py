#!/usr/bin/env python3
"""
Spezifische Koederanalyse fuer den Standort Nursery (cut_47min).

Vergleichsbloecke:
1) algae_strings vs algaemix
2) algaemix vs mackerel
3) algae_strings vs algaemix vs mackerel
4) Kontrollvideo (control) separat als explorativer Kontext

Ausgabe:
- results/nursery_methodik_vergleich/
"""

from __future__ import annotations

import itertools
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = ROOT / "normalized_reports" / "cut_47min" / "Annotation_reports_Nursery"
OUT_DIR = ROOT / "results" / "nursery_methodik_vergleich"
DATA_DIR = OUT_DIR / "data"

ALPHA = 0.05
SHORT_VIDEO_NAME = "20240108-nursery-control.csv"
NON_CONTROL_MAIN_BAITS = ["algae_strings", "algaemix", "mackerel"]
PAIR_COMPARISONS = [
    ("algae_strings", "algaemix"),
    ("algaemix", "mackerel"),
]


@dataclass(frozen=True)
class ComparisonBlock:
    key: str
    title: str
    baits: Tuple[str, ...]
    include_control_note: bool = False


def clean_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in {"", "nan", "none", "null"}:
        return ""
    return text


def is_truthy(value: object) -> bool:
    text = clean_text(value).lower()
    if text in {"", "0", "false", "f", "no", "n", "none", "null", "nan"}:
        return False
    return True


def parse_video_meta(filename: str) -> Tuple[str, str, str]:
    stem = filename.replace(".csv", "")
    parts = stem.split("-", 2)
    if len(parts) < 3:
        return "", "unknown", "unknown"
    return parts[0], parts[1].lower(), parts[2].lower()


def parse_frame_seconds(frame_value: object) -> float | None:
    text = clean_text(frame_value)
    if not text:
        return None
    match = re.search(r"[-+]?\d*\.?\d+", text)
    if not match:
        return None
    try:
        return float(match.group(0))
    except ValueError:
        return None


def benjamini_hochberg(p_values: Sequence[float]) -> List[float]:
    m = len(p_values)
    if m == 0:
        return []
    order = np.argsort(p_values)
    ranked = np.array([p_values[i] for i in order], dtype=float)
    adjusted = np.empty(m, dtype=float)
    prev = 1.0
    for i in range(m - 1, -1, -1):
        rank = i + 1
        val = (ranked[i] * m) / rank
        prev = min(prev, val)
        adjusted[i] = min(1.0, prev)
    out = np.empty(m, dtype=float)
    out[order] = adjusted
    return out.tolist()


def holm_adjust(p_values: Sequence[float]) -> List[float]:
    m = len(p_values)
    if m == 0:
        return []
    order = np.argsort(p_values)
    adjusted_order = np.zeros(m, dtype=float)
    for i, idx in enumerate(order):
        adjusted_order[i] = min(1.0, (m - i) * float(p_values[idx]))
    adjusted_order = np.maximum.accumulate(adjusted_order)
    out = np.empty(m, dtype=float)
    out[order] = adjusted_order
    return out.tolist()


def significance_label(p_value: float) -> str:
    if pd.isna(p_value):
        return "n/a"
    if p_value < 0.001:
        return "***"
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return "ns"


def cliffs_delta(x: np.ndarray, y: np.ndarray) -> float:
    total = len(x) * len(y)
    if total == 0:
        return math.nan
    gt = 0
    lt = 0
    for xi in x:
        gt += int(np.sum(xi > y))
        lt += int(np.sum(xi < y))
    return float((gt - lt) / total)


def permutation_pvalue_mean_diff(
    x: np.ndarray, y: np.ndarray, n_perm: int = 10000, seed: int = 42
) -> float:
    if len(x) == 0 or len(y) == 0:
        return math.nan
    obs = abs(float(np.mean(x) - np.mean(y)))
    joined = np.concatenate([x, y])
    n_x = len(x)

    # Fuer sehr kleine n ist exakte Enumeration stabiler als random Permutationen.
    if len(joined) <= 14:
        ge = 0
        total = 0
        idx = np.arange(len(joined))
        for comb in itertools.combinations(idx, n_x):
            mask = np.zeros(len(joined), dtype=bool)
            mask[list(comb)] = True
            a = joined[mask]
            b = joined[~mask]
            stat = abs(float(np.mean(a) - np.mean(b)))
            ge += int(stat >= obs)
            total += 1
        return ge / total if total else math.nan

    rng = np.random.default_rng(seed)
    ge = 0
    for _ in range(n_perm):
        perm = rng.permutation(joined)
        a = perm[:n_x]
        b = perm[n_x:]
        stat = abs(float(np.mean(a) - np.mean(b)))
        if stat >= obs:
            ge += 1
    return (ge + 1.0) / (n_perm + 1.0)


def to_md(df: pd.DataFrame) -> str:
    if df.empty:
        return "Keine Daten."
    return df.to_markdown(index=False)


def safe_cols(df: pd.DataFrame, cols: Sequence[str]) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=list(cols))
    missing = [c for c in cols if c not in df.columns]
    if missing:
        return pd.DataFrame(columns=list(cols))
    return df.loc[:, list(cols)].copy()


def build_general_taxon_key(row: pd.Series) -> str:
    species = clean_text(row.get("species", ""))
    genus = clean_text(row.get("genus", ""))
    family = clean_text(row.get("family", ""))
    label = clean_text(row.get("label_name", ""))

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


def build_species_key(row: pd.Series) -> str:
    species = clean_text(row.get("species", ""))
    if not species:
        return ""
    return species.lower()


def build_family_key(row: pd.Series) -> str:
    family = clean_text(row.get("family", ""))
    if not family:
        return ""
    return family.lower()


def load_video_data(csv_path: Path) -> Dict[str, object]:
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")

    non_behavior = df[(~df["feeding"].map(is_truthy)) & (~df["interested"].map(is_truthy))].copy()
    feeding_df = df[df["feeding"].map(is_truthy)].copy()
    interested_df = df[df["interested"].map(is_truthy)].copy()

    general_taxa: set[str] = set()
    species_taxa: set[str] = set()
    family_taxa: set[str] = set()

    species_counts: Dict[str, int] = {}
    family_counts: Dict[str, int] = {}
    species_first_seen: Dict[str, float] = {}
    family_first_seen: Dict[str, float] = {}

    general_by_time: Dict[Tuple[str, float], int] = {}
    species_by_time: Dict[Tuple[str, float], int] = {}
    family_by_time: Dict[Tuple[str, float], int] = {}

    non_behavior_frames: List[float] = []

    for _, row in non_behavior.iterrows():
        sec = parse_frame_seconds(row.get("frames", ""))
        if sec is not None:
            non_behavior_frames.append(sec)

        g_key = build_general_taxon_key(row)
        s_key = build_species_key(row)
        f_key = build_family_key(row)

        if g_key:
            general_taxa.add(g_key)
        if s_key:
            species_taxa.add(s_key)
            species_counts[s_key] = species_counts.get(s_key, 0) + 1
            if sec is not None and (s_key not in species_first_seen or sec < species_first_seen[s_key]):
                species_first_seen[s_key] = sec
        if f_key:
            family_taxa.add(f_key)
            family_counts[f_key] = family_counts.get(f_key, 0) + 1
            if sec is not None and (f_key not in family_first_seen or sec < family_first_seen[f_key]):
                family_first_seen[f_key] = sec

        if sec is not None:
            if g_key:
                general_by_time[(g_key, round(sec, 2))] = general_by_time.get((g_key, round(sec, 2)), 0) + 1
            if s_key:
                species_by_time[(s_key, round(sec, 2))] = species_by_time.get((s_key, round(sec, 2)), 0) + 1
            if f_key:
                family_by_time[(f_key, round(sec, 2))] = family_by_time.get((f_key, round(sec, 2)), 0) + 1

    species_maxn: Dict[str, int] = {}
    for (taxon, _), n in species_by_time.items():
        species_maxn[taxon] = max(species_maxn.get(taxon, 0), int(n))

    family_maxn: Dict[str, int] = {}
    for (taxon, _), n in family_by_time.items():
        family_maxn[taxon] = max(family_maxn.get(taxon, 0), int(n))

    feeding_species: Dict[str, int] = {}
    feeding_family: Dict[str, int] = {}
    interested_species: Dict[str, int] = {}
    interested_family: Dict[str, int] = {}

    for _, row in feeding_df.iterrows():
        s_key = build_species_key(row)
        f_key = build_family_key(row)
        if s_key:
            feeding_species[s_key] = feeding_species.get(s_key, 0) + 1
        if f_key:
            feeding_family[f_key] = feeding_family.get(f_key, 0) + 1

    for _, row in interested_df.iterrows():
        s_key = build_species_key(row)
        f_key = build_family_key(row)
        if s_key:
            interested_species[s_key] = interested_species.get(s_key, 0) + 1
        if f_key:
            interested_family[f_key] = interested_family.get(f_key, 0) + 1

    date, site, bait = parse_video_meta(csv_path.name)
    duration_sec = float(np.nanmax(non_behavior_frames)) if non_behavior_frames else math.nan

    return {
        "filename": csv_path.name,
        "date": date,
        "standort": site,
        "koeder": bait,
        "is_control_short": csv_path.name == SHORT_VIDEO_NAME,
        "duration_sec_non_behavior": duration_sec,
        "species_richness": len(species_taxa),
        "family_richness": len(family_taxa),
        "general_richness": len(general_taxa),
        "total_non_behavior_annotations": int(len(non_behavior)),
        "shannon_species": (
            float(stats.entropy(np.array(list(species_counts.values()), dtype=float), base=np.e))
            if species_counts
            else math.nan
        ),
        "median_first_seen_species_sec": (
            float(np.median(list(species_first_seen.values()))) if species_first_seen else math.nan
        ),
        "q25_first_seen_species_sec": (
            float(np.quantile(list(species_first_seen.values()), 0.25)) if species_first_seen else math.nan
        ),
        "median_first_seen_family_sec": (
            float(np.median(list(family_first_seen.values()))) if family_first_seen else math.nan
        ),
        "sum_species_maxn": float(np.sum(list(species_maxn.values()))) if species_maxn else 0.0,
        "sum_family_maxn": float(np.sum(list(family_maxn.values()))) if family_maxn else 0.0,
        "peak_species_maxn": float(np.max(list(species_maxn.values()))) if species_maxn else 0.0,
        "peak_family_maxn": float(np.max(list(family_maxn.values()))) if family_maxn else 0.0,
        "total_feeding_events": int(len(feeding_df)),
        "total_interested_events": int(len(interested_df)),
        "feeding_unique_species": len(feeding_species),
        "feeding_unique_family": len(feeding_family),
        "interested_unique_species": len(interested_species),
        "interested_unique_family": len(interested_family),
        "feeding_ratio_total": float(len(feeding_df) / len(df)) if len(df) else math.nan,
        "interested_ratio_total": float(len(interested_df) / len(df)) if len(df) else math.nan,
        "species_maxn_by_taxon": species_maxn,
        "family_maxn_by_taxon": family_maxn,
        "feeding_species_by_taxon": feeding_species,
        "feeding_family_by_taxon": feeding_family,
        "interested_species_by_taxon": interested_species,
        "interested_family_by_taxon": interested_family,
    }


def run_metric_tests(df: pd.DataFrame, block: ComparisonBlock) -> pd.DataFrame:
    metrics = [
        "duration_sec_non_behavior",
        "species_richness",
        "family_richness",
        "general_richness",
        "total_non_behavior_annotations",
        "shannon_species",
        "median_first_seen_species_sec",
        "q25_first_seen_species_sec",
        "median_first_seen_family_sec",
        "sum_species_maxn",
        "sum_family_maxn",
        "peak_species_maxn",
        "peak_family_maxn",
        "total_feeding_events",
        "total_interested_events",
        "feeding_unique_species",
        "feeding_unique_family",
        "interested_unique_species",
        "interested_unique_family",
        "feeding_ratio_total",
        "interested_ratio_total",
    ]

    rows: List[Dict[str, object]] = []
    k = len(block.baits)

    for metric in metrics:
        sub = df[df["koeder"].isin(block.baits)].copy()
        if sub.empty:
            continue

        arrays = []
        means = {}
        medians = {}
        ns = {}
        for bait in block.baits:
            arr = sub.loc[sub["koeder"] == bait, metric].astype(float).dropna().to_numpy()
            arrays.append(arr)
            means[bait] = float(np.mean(arr)) if len(arr) else math.nan
            medians[bait] = float(np.median(arr)) if len(arr) else math.nan
            ns[bait] = int(len(arr))

        if k == 2:
            x, y = arrays
            if len(x) == 0 or len(y) == 0:
                continue
            try:
                stat, p_value = stats.mannwhitneyu(x, y, alternative="two-sided", method="exact")
            except TypeError:
                stat, p_value = stats.mannwhitneyu(x, y, alternative="two-sided")
            except ValueError:
                stat, p_value = 0.0, 1.0

            rows.append(
                {
                    "comparison_key": block.key,
                    "comparison": block.title,
                    "metric": metric,
                    "test": "Mann-Whitney U",
                    "n_groups": 2,
                    "groups": " vs ".join(block.baits),
                    "statistic": float(stat),
                    "p_value": float(p_value),
                    "effect_size": cliffs_delta(x, y),
                    "effect_name": "cliffs_delta",
                    "perm_p_value_mean_diff": permutation_pvalue_mean_diff(x, y),
                    "mean_diff_last_minus_first": float(np.mean(y) - np.mean(x)),
                    "n_" + block.baits[0]: ns[block.baits[0]],
                    "n_" + block.baits[1]: ns[block.baits[1]],
                    "mean_" + block.baits[0]: means[block.baits[0]],
                    "mean_" + block.baits[1]: means[block.baits[1]],
                    "median_" + block.baits[0]: medians[block.baits[0]],
                    "median_" + block.baits[1]: medians[block.baits[1]],
                }
            )
        else:
            valid = [arr for arr in arrays if len(arr) > 0]
            if len(valid) < 2:
                continue
            joined = np.concatenate(valid)
            if len(joined) == 0 or np.allclose(joined, joined[0]):
                stat, p_value = 0.0, 1.0
            else:
                try:
                    stat, p_value = stats.kruskal(*valid)
                    if pd.isna(p_value):
                        stat, p_value = 0.0, 1.0
                except ValueError:
                    stat, p_value = 0.0, 1.0

            n_total = int(sum(len(arr) for arr in valid))
            eps_sq = (
                float((stat - len(valid) + 1) / (n_total - len(valid)))
                if n_total > len(valid)
                else math.nan
            )
            if not pd.isna(eps_sq):
                eps_sq = max(0.0, eps_sq)

            row = {
                "comparison_key": block.key,
                "comparison": block.title,
                "metric": metric,
                "test": "Kruskal-Wallis",
                "n_groups": len(valid),
                "groups": " | ".join(block.baits),
                "statistic": float(stat),
                "p_value": float(p_value),
                "effect_size": eps_sq,
                "effect_name": "epsilon_squared",
                "perm_p_value_mean_diff": math.nan,
                "mean_diff_last_minus_first": math.nan,
            }
            for bait in block.baits:
                row["n_" + bait] = ns[bait]
                row["mean_" + bait] = means[bait]
                row["median_" + bait] = medians[bait]
            rows.append(row)

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    out = out.sort_values("p_value", ascending=True).reset_index(drop=True)
    out["p_value_holm"] = holm_adjust(out["p_value"].tolist())
    out["p_value_bh"] = benjamini_hochberg(out["p_value"].tolist())
    out["sig_raw"] = out["p_value"].map(significance_label)
    out["sig_holm"] = out["p_value_holm"].map(significance_label)
    out["sig_bh"] = out["p_value_bh"].map(significance_label)
    out["significant_raw"] = out["p_value"] < ALPHA
    out["significant_holm"] = out["p_value_holm"] < ALPHA
    out["significant_bh"] = out["p_value_bh"] < ALPHA
    return out


def run_taxon_tests(
    df: pd.DataFrame,
    block: ComparisonBlock,
    dict_col: str,
    level_name: str,
    min_presence_videos: int = 1,
) -> pd.DataFrame:
    sub = df[df["koeder"].isin(block.baits)].copy()
    if sub.empty:
        return pd.DataFrame(
            columns=[
                "comparison_key",
                "comparison",
                "level",
                "metric_source",
                "taxon",
                "n_present_videos_total",
                "groups",
                "test",
                "statistic",
                "p_value",
                "effect_name",
                "effect_size",
                "perm_p_value_mean_diff",
                "p_value_holm",
                "p_value_bh",
                "sig_raw",
                "sig_holm",
                "sig_bh",
                "significant_raw",
                "significant_holm",
                "significant_bh",
            ]
        )

    bait_to_dicts = {
        bait: sub.loc[sub["koeder"] == bait, dict_col].tolist() for bait in block.baits
    }

    all_taxa = sorted(
        set().union(
            *[
                set().union(*[set(d.keys()) for d in bait_to_dicts[bait]])
                for bait in block.baits
                if bait_to_dicts[bait]
            ]
        )
    )

    rows: List[Dict[str, object]] = []
    for taxon in all_taxa:
        arrays = []
        present_total = 0
        per_bait_mean = {}
        per_bait_occ = {}

        for bait in block.baits:
            vals = np.array([float(d.get(taxon, 0)) for d in bait_to_dicts[bait]], dtype=float)
            arrays.append(vals)
            present_total += int(np.sum(vals > 0))
            per_bait_mean[bait] = float(np.mean(vals)) if len(vals) else math.nan
            per_bait_occ[bait] = float(np.mean(vals > 0)) if len(vals) else math.nan

        if present_total < min_presence_videos:
            continue

        k = len(block.baits)
        row = {
            "comparison_key": block.key,
            "comparison": block.title,
            "level": level_name,
            "metric_source": dict_col,
            "taxon": taxon,
            "n_present_videos_total": int(present_total),
            "groups": " | ".join(block.baits),
        }

        for bait in block.baits:
            row["mean_" + bait] = per_bait_mean[bait]
            row["occ_" + bait] = per_bait_occ[bait]
            row["n_" + bait] = int(len(arrays[block.baits.index(bait)]))

        if k == 2:
            x, y = arrays
            try:
                stat, p_value = stats.mannwhitneyu(x, y, alternative="two-sided", method="exact")
            except TypeError:
                stat, p_value = stats.mannwhitneyu(x, y, alternative="two-sided")
            except ValueError:
                stat, p_value = 0.0, 1.0

            row["test"] = "Mann-Whitney U"
            row["statistic"] = float(stat)
            row["p_value"] = float(p_value)
            row["effect_name"] = "cliffs_delta"
            row["effect_size"] = cliffs_delta(x, y)
            row["perm_p_value_mean_diff"] = permutation_pvalue_mean_diff(x, y)
        else:
            valid = [arr for arr in arrays if len(arr) > 0]
            if len(valid) < 2:
                continue
            joined = np.concatenate(valid)
            if len(joined) == 0 or np.allclose(joined, joined[0]):
                stat, p_value = 0.0, 1.0
            else:
                try:
                    stat, p_value = stats.kruskal(*valid)
                    if pd.isna(p_value):
                        stat, p_value = 0.0, 1.0
                except ValueError:
                    stat, p_value = 0.0, 1.0
            n_total = int(sum(len(arr) for arr in valid))
            eps_sq = (
                float((stat - len(valid) + 1) / (n_total - len(valid)))
                if n_total > len(valid)
                else math.nan
            )
            if not pd.isna(eps_sq):
                eps_sq = max(0.0, eps_sq)

            row["test"] = "Kruskal-Wallis"
            row["statistic"] = float(stat)
            row["p_value"] = float(p_value)
            row["effect_name"] = "epsilon_squared"
            row["effect_size"] = eps_sq
            row["perm_p_value_mean_diff"] = math.nan

        rows.append(row)

    out = pd.DataFrame(rows)
    if out.empty:
        return pd.DataFrame(
            columns=[
                "comparison_key",
                "comparison",
                "level",
                "metric_source",
                "taxon",
                "n_present_videos_total",
                "groups",
                "test",
                "statistic",
                "p_value",
                "effect_name",
                "effect_size",
                "perm_p_value_mean_diff",
                "p_value_holm",
                "p_value_bh",
                "sig_raw",
                "sig_holm",
                "sig_bh",
                "significant_raw",
                "significant_holm",
                "significant_bh",
            ]
        )

    out = out.sort_values("p_value", ascending=True).reset_index(drop=True)
    out["p_value_holm"] = holm_adjust(out["p_value"].tolist())
    out["p_value_bh"] = benjamini_hochberg(out["p_value"].tolist())
    out["sig_raw"] = out["p_value"].map(significance_label)
    out["sig_holm"] = out["p_value_holm"].map(significance_label)
    out["sig_bh"] = out["p_value_bh"].map(significance_label)
    out["significant_raw"] = out["p_value"] < ALPHA
    out["significant_holm"] = out["p_value_holm"] < ALPHA
    out["significant_bh"] = out["p_value_bh"] < ALPHA
    return out


def summarize_top_significant(df: pd.DataFrame, top_n: int = 15) -> pd.DataFrame:
    if df.empty:
        return df
    filt = df[df["significant_bh"] | df["significant_holm"] | df["significant_raw"]].copy()
    if filt.empty:
        return filt
    return filt.sort_values(["p_value_holm", "p_value_bh", "p_value"], ascending=[True, True, True]).head(top_n)


def collect_control_context(video_df: pd.DataFrame) -> pd.DataFrame:
    control = video_df[video_df["koeder"] == "control"].copy()
    if control.empty:
        return pd.DataFrame()
    metrics = [
        "duration_sec_non_behavior",
        "species_richness",
        "family_richness",
        "sum_species_maxn",
        "sum_family_maxn",
        "total_feeding_events",
        "total_interested_events",
        "median_first_seen_species_sec",
    ]
    rows: List[Dict[str, object]] = []

    for metric in metrics:
        c_val = float(control.iloc[0][metric]) if pd.notna(control.iloc[0][metric]) else math.nan
        row = {
            "metric": metric,
            "control_value": c_val,
            "control_file": control.iloc[0]["filename"],
        }
        for bait in NON_CONTROL_MAIN_BAITS:
            arr = video_df.loc[video_df["koeder"] == bait, metric].astype(float).dropna().to_numpy()
            row[f"{bait}_mean"] = float(np.mean(arr)) if len(arr) else math.nan
            row[f"{bait}_median"] = float(np.median(arr)) if len(arr) else math.nan
        rows.append(row)

    return pd.DataFrame(rows)


def write_report(
    video_df: pd.DataFrame,
    block_results: Dict[str, Dict[str, pd.DataFrame]],
    control_context_df: pd.DataFrame,
) -> None:
    report_path = OUT_DIR / "nursery_methodik_koeder_bericht.md"

    bait_counts = (
        video_df.groupby("koeder", as_index=False)
        .agg(n_videos=("filename", "count"), median_duration_s=("duration_sec_non_behavior", "median"))
        .sort_values("koeder")
    )

    lines: List[str] = []
    lines.append("# Nursery-Methodik: Koedervergleich (cut_47min)")
    lines.append("")
    lines.append("## Datengrundlage")
    lines.append("- Standort: nursery")
    lines.append(f"- Anzahl Videos gesamt: {len(video_df)}")
    lines.append("- Hauptvergleich: algae_strings (n=3), algaemix (n=3), mackerel (n=4)")
    lines.append("- Kontrollvideo: control (n=1), kuerzeres Einzelvideo -> separat als explorativer Kontext")
    lines.append("- Signifikanzniveau: alpha=0.05")
    lines.append("- Korrekturen fuer multiples Testen: Holm (FWER) und Benjamini-Hochberg/FDR")
    lines.append("- Robuste Zusatzpruefung fuer 2-Gruppen-Metriken: exakter/perm-basierter Mittelwert-Differenztest")
    lines.append("")
    lines.append("### Videoanzahl je Koeder")
    lines.append(to_md(bait_counts))
    lines.append("")

    for block_key in ["strings_vs_mix", "mix_vs_mackerel", "three_baits"]:
        res = block_results[block_key]
        title = res["meta"].iloc[0]["title"]
        baits = res["meta"].iloc[0]["baits"]

        lines.append(f"## {title}")
        lines.append(f"- Gruppen: {baits}")
        lines.append("")

        video_tests = res["video_tests"]
        lines.append("### 1) Videoebene: Species Richness, MaxN, First Seen, Interested/Feeding und weitere Kennzahlen")
        lines.append(to_md(safe_cols(video_tests, [
            "metric",
            "test",
            "p_value",
            "p_value_holm",
            "p_value_bh",
            "sig_raw",
            "sig_holm",
            "sig_bh",
            "effect_name",
            "effect_size",
            "perm_p_value_mean_diff",
        ])))
        lines.append("")

        sig_video = summarize_top_significant(video_tests, top_n=10)
        lines.append("Top signifikante Video-Metriken:")
        lines.append(to_md(safe_cols(sig_video, ["metric", "p_value", "p_value_holm", "p_value_bh", "sig_holm", "sig_bh"])))
        lines.append("")

        lines.append("### 2) Artenebene (Species): Unterschiede in MaxN")
        species_maxn = res["species_maxn"]
        lines.append(to_md(safe_cols(summarize_top_significant(species_maxn), [
            "taxon",
            "p_value",
            "p_value_holm",
            "p_value_bh",
            "sig_holm",
            "sig_bh",
        ])))
        lines.append("")

        lines.append("### 3) Familienebene (Family): Unterschiede in MaxN")
        family_maxn = res["family_maxn"]
        lines.append(to_md(safe_cols(summarize_top_significant(family_maxn), [
            "taxon",
            "p_value",
            "p_value_holm",
            "p_value_bh",
            "sig_holm",
            "sig_bh",
        ])))
        lines.append("")

        lines.append("### 4) Interested vs Feeding: Artenebene")
        feeding_species = res["feeding_species"]
        interested_species = res["interested_species"]

        lines.append("**Feeding (Species) signifikante Taxa**")
        lines.append(to_md(safe_cols(summarize_top_significant(feeding_species), [
            "taxon",
            "p_value",
            "p_value_holm",
            "p_value_bh",
            "sig_holm",
            "sig_bh",
        ])))
        lines.append("")

        lines.append("**Interested (Species) signifikante Taxa**")
        lines.append(to_md(safe_cols(summarize_top_significant(interested_species), [
            "taxon",
            "p_value",
            "p_value_holm",
            "p_value_bh",
            "sig_holm",
            "sig_bh",
        ])))
        lines.append("")

        lines.append("### 5) Interested vs Feeding: Familienebene")
        feeding_family = res["feeding_family"]
        interested_family = res["interested_family"]

        lines.append("**Feeding (Family) signifikante Taxa/Familien**")
        lines.append(to_md(safe_cols(summarize_top_significant(feeding_family), [
            "taxon",
            "p_value",
            "p_value_holm",
            "p_value_bh",
            "sig_holm",
            "sig_bh",
        ])))
        lines.append("")

        lines.append("**Interested (Family) signifikante Taxa/Familien**")
        lines.append(to_md(safe_cols(summarize_top_significant(interested_family), [
            "taxon",
            "p_value",
            "p_value_holm",
            "p_value_bh",
            "sig_holm",
            "sig_bh",
        ])))
        lines.append("")

        lines.append("### Kurzinterpretation")
        n_sig_video_holm = int(video_tests["significant_holm"].sum()) if not video_tests.empty else 0
        n_sig_video_bh = int(video_tests["significant_bh"].sum()) if not video_tests.empty else 0

        n_sig_species_holm = int(species_maxn["significant_holm"].sum()) if not species_maxn.empty else 0
        n_sig_species_bh = int(species_maxn["significant_bh"].sum()) if not species_maxn.empty else 0

        n_sig_family_holm = int(family_maxn["significant_holm"].sum()) if not family_maxn.empty else 0
        n_sig_family_bh = int(family_maxn["significant_bh"].sum()) if not family_maxn.empty else 0

        lines.append(
            f"- Videoebene: Holm-signifikant {n_sig_video_holm}, BH-signifikant {n_sig_video_bh} Kennzahlen."
        )
        lines.append(
            f"- Artenebene (MaxN): Holm-signifikant {n_sig_species_holm}, BH-signifikant {n_sig_species_bh}."
        )
        lines.append(
            f"- Familienebene (MaxN): Holm-signifikant {n_sig_family_holm}, BH-signifikant {n_sig_family_bh}."
        )
        lines.append("- Interested/Feeding ist oben getrennt nach Arten und Familien ausgewiesen.")
        lines.append("")

    lines.append("## Kontrollvideo (explorativ, getrennt)")
    lines.append(
        "Hinweis: Das Kontrollvideo hat n=1 und kuerzere Laufzeit. Aussagen sind daher rein deskriptiv und nicht als gleichwertige Signifikanztests zu interpretieren."
    )
    lines.append("")
    lines.append(to_md(control_context_df))
    lines.append("")

    lines.append("## Gesamtfazit")
    lines.append(
        "Die drei Hauptkoeder wurden auf Videoebene sowie auf Arten-/Familienebene fuer MaxN und Interested/Feeding verglichen. "
        "Signifikanzen sind immer roh, Holm-korrigiert und BH-korrigiert angegeben; dadurch ist transparent, welche Befunde robust gegen multiples Testen bleiben."
    )
    lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def save_results(block_key: str, result: Dict[str, pd.DataFrame]) -> None:
    for name, df in result.items():
        if name == "meta":
            continue
        out = DATA_DIR / f"{block_key}_{name}.csv"
        df.to_csv(out, index=False)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(INPUT_DIR.glob("*.csv"))
    videos = [load_video_data(p) for p in files if "-nursery-" in p.name]
    video_df = pd.DataFrame(videos).sort_values(["koeder", "date", "filename"]).reset_index(drop=True)

    video_df.to_csv(DATA_DIR / "nursery_video_metrics.csv", index=False)

    blocks = [
        ComparisonBlock("strings_vs_mix", "Vergleich 1: algae_strings vs algaemix", ("algae_strings", "algaemix")),
        ComparisonBlock("mix_vs_mackerel", "Vergleich 2: algaemix vs mackerel", ("algaemix", "mackerel")),
        ComparisonBlock("three_baits", "Vergleich 3: algae_strings vs algaemix vs mackerel", ("algae_strings", "algaemix", "mackerel")),
    ]

    block_results: Dict[str, Dict[str, pd.DataFrame]] = {}

    for block in blocks:
        sub = video_df[video_df["koeder"].isin(block.baits)].copy()
        result: Dict[str, pd.DataFrame] = {
            "meta": pd.DataFrame([{"title": block.title, "baits": ", ".join(block.baits)}]),
            "video_tests": run_metric_tests(sub, block),
            "species_maxn": run_taxon_tests(sub, block, "species_maxn_by_taxon", "species", min_presence_videos=1),
            "family_maxn": run_taxon_tests(sub, block, "family_maxn_by_taxon", "family", min_presence_videos=1),
            "feeding_species": run_taxon_tests(sub, block, "feeding_species_by_taxon", "species", min_presence_videos=1),
            "feeding_family": run_taxon_tests(sub, block, "feeding_family_by_taxon", "family", min_presence_videos=1),
            "interested_species": run_taxon_tests(sub, block, "interested_species_by_taxon", "species", min_presence_videos=1),
            "interested_family": run_taxon_tests(sub, block, "interested_family_by_taxon", "family", min_presence_videos=1),
        }
        block_results[block.key] = result
        save_results(block.key, result)

    control_context_df = collect_control_context(video_df)
    control_context_df.to_csv(DATA_DIR / "control_explorative_context.csv", index=False)

    write_report(video_df, block_results, control_context_df)


if __name__ == "__main__":
    main()
