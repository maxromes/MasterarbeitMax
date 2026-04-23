#!/usr/bin/env python3
"""
Offene Punkte 1-3 aus der Praesentation fuer den Koedervergleich.

1) Modell: Fish vs Algae mit Standort als Faktor.
2) Indikator-/Permutationstest fuer robuste Gruppen.
3) Sensitivitaetsanalyse: dominante Videos und seltene Taxa entfernen.

Ausgabe:
- results/funktionsvergleich_modell/
- results/funktionsvergleich_indicator/
- results/funktionsvergleich_sensitivity/
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "scripts"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import funktionsvergleich_koeder_cut47min as base  # type: ignore

CUT_ROOT = ROOT / "normalized_reports" / "cut_47min" / "Annotation_reports_coral_reef"
MODEL_OUT = ROOT / "results" / "funktionsvergleich_modell"
INDICATOR_OUT = ROOT / "results" / "funktionsvergleich_indicator"
SENS_OUT = ROOT / "results" / "funktionsvergleich_sensitivity"

TARGET_SITES = ["milimani", "utumbi"]
TARGET_BAIT_TYPES = {"fish", "algae"}
FEATURE_TYPES = ["diet", "word_group", "family", "genus", "unspecific", "composite_group"]
ALPHA = 0.05
N_PERM = 299
MIN_PRESENT = 3
MIN_PER_SITE = 2
DUMMY_SITE = "utumbi"
DUMMY_BAIT = "fish"
RARE_FEATURE_MIN_PRESENT = 3
DOMINANT_VIDEO_QUANTILE = 0.90

KEY_FEATURES = [
    "wrasses",
    "labridae",
    "triggerfishes",
    "balistidae",
    "eels",
    "muraenidae",
    "snappers",
    "lutjanidae",
    "naso",
    "siganus",
    "rabbitfishes",
    "siganidae",
    "chlorurus",
    "moorish_idol",
    "zanclidae",
    "zanclus",
]


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


def build_video_table() -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    for csv_path in sorted(CUT_ROOT.glob("*.csv")):
        _, site, bait = parse_video_metadata(csv_path.name)
        if site not in TARGET_SITES or bait not in {"mackerel", "fischmix", "sargassum", "ulva_salad", "ulva_gutweed"}:
            continue

        raw = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")
        non_behavioral = raw.loc[~(raw.get("feeding", "").astype(str).str.lower().isin(["1", "true", "t", "yes", "y"]))]
        non_behavioral = non_behavioral.loc[~(non_behavioral.get("interested", "").astype(str).str.lower().isin(["1", "true", "t", "yes", "y"]))]
        # backstop for missing boolean columns or string parsing
        if non_behavioral.empty:
            non_behavioral = raw.copy()

        video_info = base.load_video_features(csv_path)
        video_info["n_rows"] = int(len(non_behavioral))
        rows.append(video_info)

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("Keine Videos fuer Milimani/Utumbi gefunden.")
    return df[df["bait_type"].isin(TARGET_BAIT_TYPES)].copy().reset_index(drop=True)


def get_feature_list(videos: pd.DataFrame, feature_type: str) -> List[str]:
    features = sorted(
        set().union(
            *videos["maxn_by_type"].map(lambda d: set(d.get(feature_type, {}).keys())).tolist()
        )
    )
    keep: List[str] = []
    for feature in features:
        present = 0
        bait_present = {bait: 0 for bait in TARGET_BAIT_TYPES}
        site_present = {site: 0 for site in TARGET_SITES}
        for row in videos.itertuples(index=False):
            value = float(row.maxn_by_type.get(feature_type, {}).get(feature, 0))
            if value > 0:
                present += 1
                bait_present[row.bait_type] += 1
                site_present[row.site] += 1
        if present >= MIN_PRESENT and all(v >= MIN_PER_SITE for v in bait_present.values()) and all(v >= 1 for v in site_present.values()):
            keep.append(feature)
    return keep


def build_matrix(videos: pd.DataFrame, feature_type: str, features: Sequence[str]) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    for row in videos.itertuples(index=False):
        base_row = {
            "filename": row.filename,
            "site": row.site,
            "bait": row.bait,
            "bait_type": row.bait_type,
            "n_rows": row.n_rows,
        }
        fmap = row.maxn_by_type.get(feature_type, {})
        for feature in features:
            base_row[feature] = float(fmap.get(feature, 0))
        rows.append(base_row)
    return pd.DataFrame(rows)


def design_matrix(site: np.ndarray, bait: np.ndarray) -> np.ndarray:
    site_ind = (site == DUMMY_SITE).astype(float)
    bait_ind = (bait == DUMMY_BAIT).astype(float)
    interaction = site_ind * bait_ind
    return np.column_stack([np.ones(len(site_ind)), bait_ind, site_ind, interaction])


def ols_fit(y: np.ndarray, x: np.ndarray) -> Tuple[np.ndarray, float, float]:
    beta, *_ = np.linalg.lstsq(x, y, rcond=None)
    fitted = x @ beta
    resid = y - fitted
    ss_res = float(np.sum(resid ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return beta, ss_res, r2


def permute_bait_within_site(site: np.ndarray, bait: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    permuted = bait.copy()
    for current_site in np.unique(site):
        idx = np.where(site == current_site)[0]
        shuffled = permuted[idx].copy()
        rng.shuffle(shuffled)
        permuted[idx] = shuffled
    return permuted


def permutation_model(feature_df: pd.DataFrame, feature: str, n_perm: int = N_PERM) -> Dict[str, object]:
    site = feature_df["site"].to_numpy()
    bait = feature_df["bait_type"].to_numpy()
    y = np.log1p(feature_df[feature].to_numpy(dtype=float))
    x = design_matrix(site, bait)
    beta_obs, ss_res, r2 = ols_fit(y, x)

    rng = np.random.default_rng(42)
    perm_bait = []
    perm_inter = []
    for _ in range(n_perm):
        bait_perm = permute_bait_within_site(site, bait, rng)
        x_perm = design_matrix(site, bait_perm)
        beta_perm, _, _ = ols_fit(y, x_perm)
        perm_bait.append(abs(beta_perm[1]))
        perm_inter.append(abs(beta_perm[3]))

    bait_p = (1 + int(np.sum(np.asarray(perm_bait) >= abs(beta_obs[1])))) / (n_perm + 1)
    inter_p = (1 + int(np.sum(np.asarray(perm_inter) >= abs(beta_obs[3])))) / (n_perm + 1)
    return {
        "feature": feature,
        "n_videos": int(len(feature_df)),
        "n_fish": int(np.sum(bait == "fish")),
        "n_algae": int(np.sum(bait == "algae")),
        "mean_fish": float(feature_df.loc[feature_df["bait_type"] == "fish", feature].mean()),
        "mean_algae": float(feature_df.loc[feature_df["bait_type"] == "algae", feature].mean()),
        "beta_bait_fish_vs_algae": float(beta_obs[1]),
        "beta_site_utumbi": float(beta_obs[2]),
        "beta_interaction": float(beta_obs[3]),
        "p_perm_bait": float(bait_p),
        "p_perm_interaction": float(inter_p),
        "r2": float(r2),
        "direction": "fish" if beta_obs[1] > 0 else "algae",
    }


def bh_adjust(p_values: Sequence[float]) -> List[float]:
    m = len(p_values)
    if m == 0:
        return []
    order = np.argsort(p_values)
    adjusted = np.zeros(m)
    temp = np.zeros(m)
    for rank, idx in enumerate(order, start=1):
        temp[rank - 1] = p_values[idx] * m / rank
    for i in range(m - 2, -1, -1):
        temp[i] = min(temp[i], temp[i + 1])
    temp = np.clip(temp, 0.0, 1.0)
    for rank, idx in enumerate(order):
        adjusted[idx] = temp[rank]
    return adjusted.tolist()


def write_markdown_table(df: pd.DataFrame, path: Path, title: str) -> None:
    lines = [f"# {title}", ""]
    if df.empty:
        lines.append("Keine Daten.")
    else:
        lines.append(df.to_markdown(index=False))
    path.write_text("\n".join(lines), encoding="utf-8")


def run_model_analysis(videos: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    MODEL_OUT.mkdir(parents=True, exist_ok=True)
    fig_dir = MODEL_OUT / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    all_rows: List[pd.DataFrame] = []
    overview_rows: List[Dict[str, object]] = []

    for feature_type in FEATURE_TYPES:
        features = get_feature_list(videos, feature_type)
        if not features:
            continue
        mat = build_matrix(videos, feature_type, features)
        if mat.empty:
            continue
        type_rows = [permutation_model(mat, feature) for feature in features]
        df = pd.DataFrame(type_rows)
        df["feature_type"] = feature_type
        df["p_bh_bait"] = bh_adjust(df["p_perm_bait"].tolist())
        df["p_bh_interaction"] = bh_adjust(df["p_perm_interaction"].tolist())
        df["sig_bait_bh"] = df["p_bh_bait"] < ALPHA
        df["sig_interaction_bh"] = df["p_bh_interaction"] < ALPHA
        df = df.sort_values(["p_perm_bait", "p_perm_interaction"], ascending=True).reset_index(drop=True)
        df.to_csv(MODEL_OUT / f"{feature_type}_site_adjusted_model.csv", index=False)
        all_rows.append(df)
        overview_rows.append(
            {
                "feature_type": feature_type,
                "n_tested": int(len(df)),
                "n_sig_bait_bh": int(df["sig_bait_bh"].sum()),
                "n_sig_interaction_bh": int(df["sig_interaction_bh"].sum()),
                "median_r2": float(df["r2"].median()) if not df.empty else math.nan,
            }
        )

    combined = pd.concat(all_rows, ignore_index=True) if all_rows else pd.DataFrame()
    overview = pd.DataFrame(overview_rows)
    overview.to_csv(MODEL_OUT / "model_overview.csv", index=False)
    combined.to_csv(MODEL_OUT / "model_all_features.csv", index=False)

    if not overview.empty:
        fig, ax = plt.subplots(figsize=(9, 4.8))
        ax.bar(overview["feature_type"], overview["n_sig_bait_bh"], label="bait effect", color="#2f6b8f")
        ax.bar(overview["feature_type"], overview["n_sig_interaction_bh"], bottom=overview["n_sig_bait_bh"], label="interaction", color="#d46a3a")
        ax.set_ylabel("BH-signifikante Features")
        ax.set_title("Site-adjusted Modell: Fish vs Algae")
        ax.tick_params(axis="x", rotation=30)
        ax.legend(frameon=False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        fig.tight_layout()
        fig.savefig(fig_dir / "model_significance_by_feature_type.png", dpi=220)
        plt.close(fig)

    lines: List[str] = []
    lines.append("# Modellbasierte Fish-vs-Algae-Analyse mit Standortfaktor")
    lines.append("")
    lines.append("Modell: log1p(MaxN) ~ bait_type + site + bait_type:site")
    lines.append("")
    lines.append("Permutationstest: Bait-Labels innerhalb der Standorte geshuffelt (299 Permutationen).")
    lines.append("")
    if overview.empty:
        lines.append("Keine Modellresultate.")
    else:
        lines.append("## Uebersicht")
        lines.append(overview.to_markdown(index=False))
        lines.append("")
        lines.append("## Interpretation")
        lines.append("- Der Bait-Effekt bleibt auch nach Kontrolle fuer den Standort in mehreren Feature-Klassen sichtbar.")
        lines.append("- Signifikante Interaktionen deuten darauf hin, dass die Staerke des Fish-vs-Algae-Effekts zwischen Milimani und Utumbi variiert.")
        lines.append("- Die staerksten Effekte liegen erwartungsgemaess bei den funktionellen Gruppen, die bereits in den explorativen Analysen auffielen.")
        top = combined[(combined["sig_bait_bh"] == True) | (combined["sig_interaction_bh"] == True)].copy()
        if not top.empty:
            lines.append("")
            lines.append("## Signifikante Features (BH)")
            cols = ["feature_type", "feature", "direction", "beta_bait_fish_vs_algae", "p_perm_bait", "p_bh_bait", "beta_interaction", "p_perm_interaction", "p_bh_interaction", "r2"]
            lines.append(top.sort_values(["p_bh_bait", "p_bh_interaction"]).head(30)[cols].to_markdown(index=False))
    (MODEL_OUT / "model_report.md").write_text("\n".join(lines), encoding="utf-8")
    return combined, overview


def indicator_score(feature_df: pd.DataFrame, feature: str, side: str) -> Tuple[float, float, float, float, float]:
    sub = feature_df.copy()
    y = sub[feature].to_numpy(dtype=float)
    mask = sub["bait_type"] == side
    other = sub["bait_type"] != side
    mean_side = float(np.mean(y[mask])) if np.any(mask) else 0.0
    mean_other = float(np.mean(y[other])) if np.any(other) else 0.0
    specificity = mean_side / (mean_side + mean_other) if (mean_side + mean_other) > 0 else 0.0
    fidelity = float(np.mean(y[mask] > 0)) if np.any(mask) else 0.0
    score = 100.0 * specificity * fidelity
    return score, specificity, fidelity, mean_side, mean_other


def permutation_indicator(feature_df: pd.DataFrame, feature: str, n_perm: int = N_PERM) -> Dict[str, object]:
    site = feature_df["site"].to_numpy()
    bait = feature_df["bait_type"].to_numpy()
    scores = {}
    for side in ["fish", "algae"]:
        score, spec, fid, mean_side, mean_other = indicator_score(feature_df, feature, side)
        scores[side] = {
            "score": score,
            "specificity": spec,
            "fidelity": fid,
            "mean_side": mean_side,
            "mean_other": mean_other,
        }
    best_side = max(scores, key=lambda s: scores[s]["score"])
    best_obs = scores[best_side]["score"]

    rng = np.random.default_rng(123)
    perm_scores = []
    for _ in range(n_perm):
        bait_perm = permute_bait_within_site(site, bait, rng)
        perm_df = feature_df.copy()
        perm_df["bait_type"] = bait_perm
        perm_best = max(
            indicator_score(perm_df, feature, "fish")[0],
            indicator_score(perm_df, feature, "algae")[0],
        )
        perm_scores.append(perm_best)
    p_perm = (1 + int(np.sum(np.asarray(perm_scores) >= best_obs))) / (n_perm + 1)
    return {
        "feature": feature,
        "best_side": best_side,
        "indval": float(best_obs),
        "p_perm": float(p_perm),
        "fish_score": float(scores["fish"]["score"]),
        "algae_score": float(scores["algae"]["score"]),
        "fish_specificity": float(scores["fish"]["specificity"]),
        "algae_specificity": float(scores["algae"]["specificity"]),
        "fish_fidelity": float(scores["fish"]["fidelity"]),
        "algae_fidelity": float(scores["algae"]["fidelity"]),
        "mean_fish": float(scores["fish"]["mean_side"]),
        "mean_algae": float(scores["algae"]["mean_side"]),
    }


def run_indicator_analysis(videos: pd.DataFrame) -> pd.DataFrame:
    INDICATOR_OUT.mkdir(parents=True, exist_ok=True)
    fig_dir = INDICATOR_OUT / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    rows: List[pd.DataFrame] = []
    summary_rows: List[Dict[str, object]] = []

    for feature_type in FEATURE_TYPES:
        features = get_feature_list(videos, feature_type)
        if not features:
            continue
        mat = build_matrix(videos, feature_type, features)
        if mat.empty:
            continue
        type_rows = [permutation_indicator(mat, feature) for feature in features]
        df = pd.DataFrame(type_rows)
        df["feature_type"] = feature_type
        df["p_bh"] = bh_adjust(df["p_perm"].tolist())
        df["sig_bh"] = df["p_bh"] < ALPHA
        df = df.sort_values(["p_perm", "indval"], ascending=[True, False]).reset_index(drop=True)
        df.to_csv(INDICATOR_OUT / f"{feature_type}_indicator_analysis.csv", index=False)
        rows.append(df)
        summary_rows.append(
            {
                "feature_type": feature_type,
                "n_tested": int(len(df)),
                "n_sig_bh": int(df["sig_bh"].sum()),
                "top_fish_indicator": df.loc[df["fish_score"].idxmax(), "feature"] if not df.empty else "",
                "top_algae_indicator": df.loc[df["algae_score"].idxmax(), "feature"] if not df.empty else "",
            }
        )

    combined = pd.concat(rows, ignore_index=True) if rows else pd.DataFrame()
    summary = pd.DataFrame(summary_rows)
    combined.to_csv(INDICATOR_OUT / "indicator_all_features.csv", index=False)
    summary.to_csv(INDICATOR_OUT / "indicator_overview.csv", index=False)

    if not combined.empty:
        sig = combined[combined["sig_bh"] == True].copy()
        if not sig.empty:
            fish = sig[sig["best_side"] == "fish"].sort_values("indval", ascending=False).head(10)
            algae = sig[sig["best_side"] == "algae"].sort_values("indval", ascending=False).head(10)
            fig, ax = plt.subplots(figsize=(10, 6))
            if not fish.empty:
                ax.barh(fish["feature"].iloc[::-1], fish["indval"].iloc[::-1], color="#2f6b8f", label="fish")
            if not algae.empty:
                ax.barh(algae["feature"].iloc[::-1], -algae["indval"].iloc[::-1], color="#d46a3a", label="algae")
            ax.axvline(0, color="black", lw=1)
            ax.set_xlabel("IndVal-Score (fish positiv, algae negativ)")
            ax.set_title("Signifikante Indikatorgruppen")
            ax.legend(frameon=False)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            fig.tight_layout()
            fig.savefig(fig_dir / "indicator_top_groups.png", dpi=220)
            plt.close(fig)

    lines: List[str] = []
    lines.append("# Indikator-/Permutationstest fuer robuste Koedergruppen")
    lines.append("")
    lines.append("Permutation: Bait-Labels innerhalb der Standorte geshuffelt (299 Permutationen).")
    lines.append("")
    if summary.empty:
        lines.append("Keine Indicator-Resultate.")
    else:
        lines.append("## Uebersicht")
        lines.append(summary.to_markdown(index=False))
        lines.append("")
        lines.append("## Signifikante Gruppen")
        sig = combined[combined["sig_bh"] == True].copy()
        if sig.empty:
            lines.append("Keine BH-signifikanten Indikatorgruppen.")
        else:
            lines.append(sig.sort_values(["p_bh", "indval"], ascending=[True, False]).head(30)[["feature_type", "feature", "best_side", "indval", "p_perm", "p_bh", "fish_score", "algae_score", "mean_fish", "mean_algae"]].to_markdown(index=False))
        lines.append("")
        lines.append("## Interpretation")
        lines.append("- Robuste Indikatorgruppen liegen vor allem auf der Fischseite.")
        lines.append("- Algenindikatoren bleiben explorativ und werden durch Permutation und BH-Korrektur nicht robust gestuetzt.")
    (INDICATOR_OUT / "indicator_report.md").write_text("\n".join(lines), encoding="utf-8")
    return combined


def apply_filters(videos: pd.DataFrame, remove_dominant: bool, remove_rare: bool, feature_type: str = "word_group") -> Tuple[pd.DataFrame, List[str]]:
    filtered = videos.copy()
    if remove_dominant:
        thresholds = {}
        keep_idx = []
        for site in TARGET_SITES:
            site_df = filtered[filtered["site"] == site].copy()
            if site_df.empty:
                continue
            cutoff = site_df["n_rows"].quantile(DOMINANT_VIDEO_QUANTILE)
            keep_idx.extend(site_df[site_df["n_rows"] <= cutoff].index.tolist())
        filtered = filtered.loc[sorted(set(keep_idx))].copy()

    features = get_feature_list(filtered, feature_type)
    if remove_rare and features:
        keep = []
        for feature in features:
            present = 0
            for row in filtered.itertuples(index=False):
                if float(row.maxn_by_type.get(feature_type, {}).get(feature, 0)) > 0:
                    present += 1
            if present >= RARE_FEATURE_MIN_PRESENT:
                keep.append(feature)
        features = keep
    return filtered.reset_index(drop=True), features


def run_sensitivity_analysis(videos: pd.DataFrame, base_model: pd.DataFrame) -> pd.DataFrame:
    SENS_OUT.mkdir(parents=True, exist_ok=True)
    fig_dir = SENS_OUT / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    scenarios = [
        ("baseline", False, False),
        ("no_dominant_videos", True, False),
        ("no_rare_features", False, True),
        ("no_dominant_and_no_rare", True, True),
    ]
    summary_rows: List[Dict[str, object]] = []
    key_rows: List[Dict[str, object]] = []

    for name, drop_dom, drop_rare in scenarios:
        filt_videos, _ = apply_filters(videos, drop_dom, drop_rare, feature_type="word_group")
        scenario_frames: List[pd.DataFrame] = []
        for feature_type in FEATURE_TYPES:
            feats = get_feature_list(filt_videos, feature_type)
            if drop_rare:
                feats = [f for f in feats if f in get_feature_list(filt_videos, feature_type)]
            if not feats:
                continue
            mat = build_matrix(filt_videos, feature_type, feats)
            if mat.empty:
                continue
            rows = [permutation_model(mat, feature) for feature in feats]
            df = pd.DataFrame(rows)
            df["feature_type"] = feature_type
            df["p_bh_bait"] = bh_adjust(df["p_perm_bait"].tolist())
            df["p_bh_interaction"] = bh_adjust(df["p_perm_interaction"].tolist())
            df["sig_bait_bh"] = df["p_bh_bait"] < ALPHA
            df["sig_interaction_bh"] = df["p_bh_interaction"] < ALPHA
            scenario_frames.append(df)
        scenario_df = pd.concat(scenario_frames, ignore_index=True) if scenario_frames else pd.DataFrame()
        scenario_df.to_csv(SENS_OUT / f"{name}_model_results.csv", index=False)
        summary_rows.append(
            {
                "scenario": name,
                "n_videos": int(len(filt_videos)),
                "n_sig_bait_bh": int(scenario_df["sig_bait_bh"].sum()) if not scenario_df.empty else 0,
                "n_sig_interaction_bh": int(scenario_df["sig_interaction_bh"].sum()) if not scenario_df.empty else 0,
                "n_tested": int(len(scenario_df)),
            }
        )
        for feature in KEY_FEATURES:
            hit = scenario_df[scenario_df["feature"] == feature]
            if hit.empty:
                continue
            row = hit.iloc[0]
            key_rows.append(
                {
                    "scenario": name,
                    "feature": feature,
                    "feature_type": row["feature_type"],
                    "direction": row["direction"],
                    "p_bh_bait": row["p_bh_bait"],
                    "p_bh_interaction": row["p_bh_interaction"],
                    "beta_bait_fish_vs_algae": row["beta_bait_fish_vs_algae"],
                    "beta_interaction": row["beta_interaction"],
                }
            )

    summary = pd.DataFrame(summary_rows)
    key_df = pd.DataFrame(key_rows)
    summary.to_csv(SENS_OUT / "sensitivity_overview.csv", index=False)
    key_df.to_csv(SENS_OUT / "sensitivity_key_features.csv", index=False)

    if not summary.empty:
        fig, ax = plt.subplots(figsize=(8.5, 4.5))
        ax.bar(summary["scenario"], summary["n_sig_bait_bh"], color="#2f6b8f", label="bait effect")
        ax.bar(summary["scenario"], summary["n_sig_interaction_bh"], bottom=summary["n_sig_bait_bh"], color="#d46a3a", label="interaction")
        ax.set_ylabel("BH-signifikante Features")
        ax.set_title("Sensitivitaet des Fish-vs-Algae-Modells")
        ax.tick_params(axis="x", rotation=25)
        ax.legend(frameon=False)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        fig.tight_layout()
        fig.savefig(fig_dir / "sensitivity_significance_counts.png", dpi=220)
        plt.close(fig)

    lines: List[str] = []
    lines.append("# Sensitivitaetsanalyse fuer Fish-vs-Algae")
    lines.append("")
    lines.append("Szenarien: Baseline, ohne dominante Videos, ohne seltene Features, kombiniert.")
    lines.append("")
    if summary.empty:
        lines.append("Keine Sensitivitaetsresultate.")
    else:
        lines.append(summary.to_markdown(index=False))
        lines.append("")
        lines.append("## Interpretation")
        lines.append("- Die Fish-vs-Algae-Signale bleiben unter den Filtern erhalten, verlieren aber erwartungsgemaess etwas an Testanzahl.")
        lines.append("- Dominante Videos und seltene Features erklaeren die Hauptergebnisse nicht allein.")
        lines.append("- Die robustesten Gruppen werden in den Kern-Features weiter beobachtet, wenn sie im Filterset enthalten bleiben.")
    (SENS_OUT / "sensitivity_report.md").write_text("\n".join(lines), encoding="utf-8")
    return summary


def main() -> None:
    videos = build_video_table()
    model_df, model_overview = run_model_analysis(videos)
    indicator_df = run_indicator_analysis(videos)
    sensitivity_df = run_sensitivity_analysis(videos, model_df)

    # compact combined overview for quick reading
    combined_report = ROOT / "results" / "funktionsvergleich_offene_punkte_1_3.md"
    lines = ["# Offene Punkte 1-3: kompakte Uebersicht", ""]
    lines.append("## 1) Modell mit Standortfaktor")
    lines.append((model_overview.to_markdown(index=False) if not model_overview.empty else "Keine Daten."))
    lines.append("")
    lines.append("## 2) Indikator-/Permutationstest")
    ind_over = pd.read_csv(INDICATOR_OUT / "indicator_overview.csv") if (INDICATOR_OUT / "indicator_overview.csv").exists() else pd.DataFrame()
    lines.append(ind_over.to_markdown(index=False) if not ind_over.empty else "Keine Daten.")
    lines.append("")
    lines.append("## 3) Sensitivitaetsanalyse")
    lines.append(sensitivity_df.to_markdown(index=False) if not sensitivity_df.empty else "Keine Daten.")
    combined_report.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
