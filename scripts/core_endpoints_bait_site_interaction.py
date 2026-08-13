#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
VIS_PATH = ROOT / "results" / "visibility_analysis" / "visibility_video_level_merged.csv"
BEHAVIOR_PATH = ROOT / "results" / "interested_feeding" / "interested_feeding_video_level.csv"
CORAL_REEF_DIR = ROOT / "normalized_reports" / "cut_47min" / "Annotation_reports_coral_reef"
NURSERY_DIR = ROOT / "normalized_reports" / "cut_47min" / "Annotation_reports_Nursery"
OUT_DIR = ROOT / "results" / "core_endpoints_bait_site_interaction"

N_PERM = 10000
SEED = 20260812

BAIT_TYPE = {
    "mackerel": "fish",
    "fischmix": "fish",
    "sargassum": "algae",
    "ulva_salad": "algae",
    "ulva_gutweed": "algae",
    "algaemix": "algae",
    "algae_strings": "algae",
    "control": "control",
}

HERBIVORE_CORE_FAMILIES = ["acanthuridae", "siganidae", "scaridae", "blenniidae"]
SITES = ["milimani", "utumbi", "nursery"]


def is_truthy(value: object) -> bool:
    if value is None:
        return False
    text = str(value).strip().lower()
    return text not in {"", "0", "false", "f", "no", "n", "none", "null", "nan"}


def parse_frame_time(frame_value: object) -> float | None:
    text = str(frame_value).strip()
    if not text:
        return None
    num = ""
    found = False
    for ch in text:
        if ch.isdigit() or ch in ".-+":
            num += ch
            found = True
        elif found:
            break
    if not num:
        return None
    try:
        return round(float(num), 2)
    except ValueError:
        return None


def parse_video_metadata(filename: str) -> tuple[str, str, str]:
    stem = filename.replace(".csv", "")
    parts = stem.split("-", 2)
    if len(parts) < 3:
        return ("", "unknown", "unknown")
    date, site, bait = parts
    return date, site.lower(), bait.lower()


def compute_herbivore_maxn_video_level() -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    files = sorted(list(CORAL_REEF_DIR.glob("*.csv")) + list(NURSERY_DIR.glob("*.csv")))

    for csv_path in files:
        _, site, bait = parse_video_metadata(csv_path.name)
        if site not in SITES:
            continue

        df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")
        counts: Dict[tuple[str, float], int] = {}

        for _, row in df.iterrows():
            if is_truthy(row.get("feeding", "")) or is_truthy(row.get("interested", "")):
                continue

            family = str(row.get("family", "")).strip().lower()
            if family not in HERBIVORE_CORE_FAMILIES:
                continue

            frame_time = parse_frame_time(row.get("frames", ""))
            if frame_time is None:
                continue

            key = (family, frame_time)
            counts[key] = counts.get(key, 0) + 1

        maxn_by_family = {f: 0 for f in HERBIVORE_CORE_FAMILIES}
        for (family, _), n in counts.items():
            if n > maxn_by_family[family]:
                maxn_by_family[family] = int(n)

        out = {
            "filename": csv_path.name,
            "standort": site,
            "koeder": bait,
            "herbivore_core_total_maxn": int(sum(maxn_by_family.values())),
        }
        for family in HERBIVORE_CORE_FAMILIES:
            out[f"herbivore_{family}_maxn"] = int(maxn_by_family[family])
        rows.append(out)

    return pd.DataFrame(rows)


def build_design(site: pd.Series, bait_is_fish: pd.Series, with_interaction: bool) -> np.ndarray:
    site_cat = pd.Categorical(site, categories=SITES)
    site_dummies = pd.get_dummies(site_cat, drop_first=True)
    bait = bait_is_fish.astype(float)

    cols = [np.ones(len(site), dtype=float), bait.to_numpy()]
    for col in site_dummies.columns:
        cols.append(site_dummies[col].astype(float).to_numpy())

    if with_interaction:
        for col in site_dummies.columns:
            cols.append((bait.to_numpy() * site_dummies[col].astype(float).to_numpy()))

    return np.column_stack(cols)


def ols_fit(y: np.ndarray, X: np.ndarray) -> tuple[np.ndarray, float, float]:
    beta, _, _, _ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    sse = float(np.sum(resid**2))
    y_mean = float(np.mean(y))
    sst = float(np.sum((y - y_mean) ** 2))
    return beta, sse, sst


def nested_f_stat(y: np.ndarray, X_full: np.ndarray, X_reduced: np.ndarray) -> tuple[float, float, float, int, int]:
    _, sse_full, sst = ols_fit(y, X_full)
    _, sse_red, _ = ols_fit(y, X_reduced)
    df_full = X_full.shape[0] - X_full.shape[1]
    df_num = X_full.shape[1] - X_reduced.shape[1]

    if df_num <= 0 or df_full <= 0:
        return float("nan"), sse_full, sse_red, df_num, df_full

    ms_num = (sse_red - sse_full) / df_num
    ms_den = sse_full / df_full
    if ms_den <= 0:
        return float("nan"), sse_full, sse_red, df_num, df_full
    return float(ms_num / ms_den), sse_full, sse_red, df_num, df_full


def permute_bait_within_site(bait_is_fish: pd.Series, site: pd.Series, rng: np.random.Generator) -> pd.Series:
    out = bait_is_fish.to_numpy(copy=True)
    site_arr = site.to_numpy()
    for s in np.unique(site_arr):
        idx = np.where(site_arr == s)[0]
        out[idx] = rng.permutation(out[idx])
    return pd.Series(out, index=bait_is_fish.index)


def bh_adjust(pvals: pd.Series) -> pd.Series:
    vals = pvals.astype(float).to_numpy()
    m = len(vals)
    order = np.argsort(vals)
    ranked = vals[order]
    q = ranked * m / (np.arange(m) + 1)
    q = np.minimum.accumulate(q[::-1])[::-1]
    q = np.clip(q, 0.0, 1.0)
    out = np.empty_like(q)
    out[order] = q
    return pd.Series(out, index=pvals.index)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    vis = pd.read_csv(VIS_PATH)
    beh = pd.read_csv(BEHAVIOR_PATH)
    herb = compute_herbivore_maxn_video_level()

    merged = vis.merge(
        beh[["filename", "total_feeding_events", "total_interested_events"]],
        on="filename",
        how="left",
    ).merge(
        herb,
        on=["filename", "standort", "koeder"],
        how="left",
    )

    merged["bait_type"] = merged["koeder"].map(BAIT_TYPE)
    model_df = merged[merged["bait_type"].isin(["fish", "algae"])].copy()
    model_df["bait_is_fish"] = (model_df["bait_type"] == "fish").astype(int)

    endpoints = [
        "species_richness",
        "maxn_video_peak",
        "total_feeding_events",
        "total_interested_events",
        "herbivore_core_total_maxn",
        "herbivore_acanthuridae_maxn",
        "herbivore_siganidae_maxn",
        "herbivore_scaridae_maxn",
        "herbivore_blenniidae_maxn",
    ]

    rows = []
    rng = np.random.default_rng(SEED)

    for endpoint in endpoints:
        df = model_df[["filename", "standort", "koeder", "bait_type", "bait_is_fish", endpoint]].copy()
        df = df.dropna()
        y = np.log1p(df[endpoint].astype(float).to_numpy())

        X_full = build_design(df["standort"], df["bait_is_fish"], with_interaction=True)
        X_no_interaction = build_design(df["standort"], df["bait_is_fish"], with_interaction=False)

        site_cat = pd.Categorical(df["standort"], categories=SITES)
        site_dummies = pd.get_dummies(site_cat, drop_first=True)
        X_site_only = np.column_stack([np.ones(len(df), dtype=float)] + [site_dummies[c].astype(float).to_numpy() for c in site_dummies.columns])

        beta_full, sse_full, sst = ols_fit(y, X_full)
        r2 = float(1.0 - (sse_full / sst)) if sst > 0 else float("nan")

        f_bait, _, _, df_num_bait, df_den = nested_f_stat(y, X_full, X_site_only)
        f_inter, _, _, df_num_inter, _ = nested_f_stat(y, X_full, X_no_interaction)

        f_bait_perm = []
        f_inter_perm = []
        for _ in range(N_PERM):
            bait_perm = permute_bait_within_site(df["bait_is_fish"], df["standort"], rng)
            X_full_p = build_design(df["standort"], bait_perm, with_interaction=True)
            X_no_interaction_p = build_design(df["standort"], bait_perm, with_interaction=False)

            f_b, _, _, _, _ = nested_f_stat(y, X_full_p, X_site_only)
            f_i, _, _, _, _ = nested_f_stat(y, X_full_p, X_no_interaction_p)
            f_bait_perm.append(f_b)
            f_inter_perm.append(f_i)

        f_bait_perm = np.array(f_bait_perm, dtype=float)
        f_inter_perm = np.array(f_inter_perm, dtype=float)
        p_bait = float((np.sum(f_bait_perm >= f_bait) + 1) / (len(f_bait_perm) + 1))
        p_inter = float((np.sum(f_inter_perm >= f_inter) + 1) / (len(f_inter_perm) + 1))

        # Effektrichtung des Bait-Haupteffekts ist Koeffizient bei bait_is_fish.
        beta_bait_fish_vs_algae = float(beta_full[1])
        direction = "fish" if beta_bait_fish_vs_algae > 0 else ("algae" if beta_bait_fish_vs_algae < 0 else "neutral")

        rows.append(
            {
                "endpoint": endpoint,
                "n_videos": int(len(df)),
                "n_fish": int((df["bait_type"] == "fish").sum()),
                "n_algae": int((df["bait_type"] == "algae").sum()),
                "model": "log1p(y) ~ bait_type + site + bait_type:site",
                "beta_bait_fish_vs_algae": beta_bait_fish_vs_algae,
                "direction": direction,
                "f_bait": float(f_bait),
                "df_num_bait": int(df_num_bait),
                "f_interaction": float(f_inter),
                "df_num_interaction": int(df_num_inter),
                "df_den": int(df_den),
                "p_perm_bait": p_bait,
                "p_perm_interaction": p_inter,
                "r2": r2,
            }
        )

    out = pd.DataFrame(rows)
    out["p_bh_bait"] = bh_adjust(out["p_perm_bait"])
    out["p_bh_interaction"] = bh_adjust(out["p_perm_interaction"])
    out["sig_bait_bh_0_05"] = out["p_bh_bait"] < 0.05
    out["sig_interaction_bh_0_05"] = out["p_bh_interaction"] < 0.05

    out = out.sort_values(["p_bh_bait", "p_bh_interaction", "endpoint"]).reset_index(drop=True)

    out_csv = OUT_DIR / "core_endpoints_bait_site_interaction.csv"
    out_md = OUT_DIR / "core_endpoints_bait_site_interaction.md"
    model_df.to_csv(OUT_DIR / "core_endpoints_model_input.csv", index=False)
    out.to_csv(out_csv, index=False)

    lines = []
    lines.append("# Einheitliches Bait x Standort-Interaktionsmodell (Kern-Endpunkte)")
    lines.append("")
    lines.append("Modell: log1p(y) ~ bait_type + site + bait_type:site")
    lines.append("Permutation: Bait-Labels innerhalb der Standorte permutiert")
    lines.append(f"Permutationen je Endpunkt: {N_PERM}")
    lines.append("")
    lines.append("## Ergebnisuebersicht")
    lines.append("")
    show_cols = [
        "endpoint",
        "n_videos",
        "direction",
        "beta_bait_fish_vs_algae",
        "p_perm_bait",
        "p_bh_bait",
        "p_perm_interaction",
        "p_bh_interaction",
        "sig_bait_bh_0_05",
        "sig_interaction_bh_0_05",
        "r2",
    ]
    lines.append(out[show_cols].to_markdown(index=False))
    lines.append("")

    bait_sig = int(out["sig_bait_bh_0_05"].sum())
    inter_sig = int(out["sig_interaction_bh_0_05"].sum())
    lines.append("## Kurzfazit")
    lines.append("")
    lines.append(f"- BH-signifikante Bait-Effekte: {bait_sig} von {len(out)} Endpunkten.")
    lines.append(f"- BH-signifikante Bait x Standort-Interaktionen: {inter_sig} von {len(out)} Endpunkten.")
    lines.append("- Die Richtung ist als fish/algae fuer den Bait-Haupteffekt kodiert (positiv = fish > algae auf log1p-Skala).")

    out_md.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote: {out_csv}")
    print(f"Wrote: {out_md}")


if __name__ == "__main__":
    main()
