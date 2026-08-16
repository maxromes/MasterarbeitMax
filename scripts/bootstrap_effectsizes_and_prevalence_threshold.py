#!/usr/bin/env python3
from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests


ROOT = Path(__file__).resolve().parents[1]
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min"
CORAL_REEF_DIR = CUT_ROOT / "Annotation_reports_coral_reef"
NURSERY_DIR = CUT_ROOT / "Annotation_reports_Nursery"

HERB_MAXN_PATH = ROOT / "results" / "herbivore_analysis" / "herbivore_maxn_by_family.csv"

OUT_BOOT_DIR = ROOT / "results" / "effectsize_bootstrap"
OUT_PREV_DIR = ROOT / "results" / "prevalence_threshold_model"

OUT_BOOT_CSV = OUT_BOOT_DIR / "prioritized_effectsize_bootstrap.csv"
OUT_BOOT_MD = OUT_BOOT_DIR / "prioritized_effectsize_bootstrap.md"

OUT_PREV_CSV = OUT_PREV_DIR / "prevalence_threshold_summary.csv"
OUT_PREV_MD = OUT_PREV_DIR / "prevalence_threshold_model.md"

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

HERBIVORE_CORE_FAMILIES = {"siganidae", "acanthuridae", "scaridae", "blenniidae"}
SITES = ["milimani", "utumbi", "nursery"]

N_BOOT = 5000
SEED = 20260816

# Mindestnachweis-Schwellen fuer Occupancy-Analyse
THRESH_PREV_ANY = 0.20
THRESH_PRESENT_TOTAL = 3


def is_truthy(value: object) -> bool:
    if value is None:
        return False
    text = str(value).strip().lower()
    return text not in {"", "0", "false", "f", "no", "n", "none", "null", "nan"}


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
        return "", "unknown", "unknown"
    date, site, bait = parts
    return date, site.lower(), bait.lower()


def parse_frame_time(value: object) -> float | None:
    text = str(value).strip()
    if not text:
        return None
    num = ""
    started = False
    for ch in text:
        if ch.isdigit() or ch in ".-+":
            num += ch
            started = True
        elif started:
            break
    if not num:
        return None
    try:
        return round(float(num), 2)
    except ValueError:
        return None


def cliffs_delta(algae_vals: np.ndarray, fish_vals: np.ndarray) -> float:
    n = len(algae_vals) * len(fish_vals)
    if n == 0:
        return np.nan
    gt = sum(1 for a in algae_vals for f in fish_vals if a > f)
    lt = sum(1 for a in algae_vals for f in fish_vals if a < f)
    return float((gt - lt) / n)


def bootstrap_effect_cis(
    algae_vals: np.ndarray,
    fish_vals: np.ndarray,
    n_boot: int,
    rng: np.random.Generator,
) -> Dict[str, float]:
    if len(algae_vals) == 0 or len(fish_vals) == 0:
        return {
            "ci_mean_diff_low": np.nan,
            "ci_mean_diff_high": np.nan,
            "ci_median_diff_low": np.nan,
            "ci_median_diff_high": np.nan,
            "ci_cliffs_delta_low": np.nan,
            "ci_cliffs_delta_high": np.nan,
        }

    mean_diffs = np.zeros(n_boot, dtype=float)
    med_diffs = np.zeros(n_boot, dtype=float)
    deltas = np.zeros(n_boot, dtype=float)

    for i in range(n_boot):
        a = rng.choice(algae_vals, size=len(algae_vals), replace=True)
        f = rng.choice(fish_vals, size=len(fish_vals), replace=True)
        mean_diffs[i] = float(np.mean(a) - np.mean(f))
        med_diffs[i] = float(np.median(a) - np.median(f))
        deltas[i] = cliffs_delta(a, f)

    return {
        "ci_mean_diff_low": float(np.percentile(mean_diffs, 2.5)),
        "ci_mean_diff_high": float(np.percentile(mean_diffs, 97.5)),
        "ci_median_diff_low": float(np.percentile(med_diffs, 2.5)),
        "ci_median_diff_high": float(np.percentile(med_diffs, 97.5)),
        "ci_cliffs_delta_low": float(np.percentile(deltas, 2.5)),
        "ci_cliffs_delta_high": float(np.percentile(deltas, 97.5)),
    }


def load_herbivore_feeding_rates() -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    files = sorted(list(CORAL_REEF_DIR.glob("*.csv")) + list(NURSERY_DIR.glob("*.csv")))

    for csv_path in files:
        _, site, bait = parse_video_metadata(csv_path.name)
        bait_type = BAIT_TYPE.get(bait, "other")
        if site not in SITES or bait_type not in {"fish", "algae"}:
            continue

        raw = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")
        total = 0
        feeding = 0

        for _, row in raw.iterrows():
            fam = clean_text(row.get("family", "")).lower()
            if fam not in HERBIVORE_CORE_FAMILIES:
                continue
            total += 1
            if is_truthy(row.get("feeding", "")):
                feeding += 1

        if total == 0:
            continue

        rows.append(
            {
                "site": site,
                "bait_type": bait_type,
                "feeding_rate": float(feeding / total),
            }
        )

    return pd.DataFrame(rows)


def run_bootstrap_effectsizes() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    rows: List[Dict[str, object]] = []

    # 1) Priorisierte Herbivore-MaxN-Kontraste (alle site x family des a-priori-Tests)
    herb = pd.read_csv(HERB_MAXN_PATH)
    for (site, family), part in herb.groupby(["site", "family"], sort=True):
        algae_vals = part.loc[part["koeder_type"] == "algae", "maxn"].to_numpy(dtype=float)
        fish_vals = part.loc[part["koeder_type"] == "fish", "maxn"].to_numpy(dtype=float)
        if len(algae_vals) == 0 or len(fish_vals) == 0:
            continue

        mean_diff = float(np.mean(algae_vals) - np.mean(fish_vals))
        med_diff = float(np.median(algae_vals) - np.median(fish_vals))
        delta = cliffs_delta(algae_vals, fish_vals)
        p_mwu = float(stats.mannwhitneyu(algae_vals, fish_vals, alternative="greater").pvalue)

        cis = bootstrap_effect_cis(algae_vals, fish_vals, N_BOOT, rng)
        rows.append(
            {
                "analysis_block": "herbivore_maxn_apriori",
                "site": site,
                "target": family,
                "n_algae": int(len(algae_vals)),
                "n_fish": int(len(fish_vals)),
                "mean_diff_algae_minus_fish": mean_diff,
                "median_diff_algae_minus_fish": med_diff,
                "cliffs_delta": delta,
                "p_value_mwu_one_sided": p_mwu,
                **cis,
            }
        )

    # 2) Priorisierter Herbivore-Feeding-Responsiveness-Kontrast (pro Standort)
    feeding = load_herbivore_feeding_rates()
    for site, part in feeding.groupby("site", sort=True):
        algae_vals = part.loc[part["bait_type"] == "algae", "feeding_rate"].to_numpy(dtype=float)
        fish_vals = part.loc[part["bait_type"] == "fish", "feeding_rate"].to_numpy(dtype=float)
        if len(algae_vals) == 0 or len(fish_vals) == 0:
            continue

        mean_diff = float(np.mean(algae_vals) - np.mean(fish_vals))
        med_diff = float(np.median(algae_vals) - np.median(fish_vals))
        delta = cliffs_delta(algae_vals, fish_vals)
        p_mwu = float(stats.mannwhitneyu(algae_vals, fish_vals, alternative="greater").pvalue)

        cis = bootstrap_effect_cis(algae_vals, fish_vals, N_BOOT, rng)
        rows.append(
            {
                "analysis_block": "herbivore_feeding_responsiveness",
                "site": site,
                "target": "herbivore_core_feeding_rate",
                "n_algae": int(len(algae_vals)),
                "n_fish": int(len(fish_vals)),
                "mean_diff_algae_minus_fish": mean_diff,
                "median_diff_algae_minus_fish": med_diff,
                "cliffs_delta": delta,
                "p_value_mwu_one_sided": p_mwu,
                **cis,
            }
        )

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    out["q_bh"] = np.nan
    out["q_holm"] = np.nan
    for block, idx in out.groupby("analysis_block").groups.items():
        pvals = out.loc[list(idx), "p_value_mwu_one_sided"].to_numpy(dtype=float)
        _, q_bh, _, _ = multipletests(pvals, method="fdr_bh")
        _, q_holm, _, _ = multipletests(pvals, method="holm")
        out.loc[list(idx), "q_bh"] = q_bh
        out.loc[list(idx), "q_holm"] = q_holm

    out = out.sort_values(["analysis_block", "q_holm", "p_value_mwu_one_sided", "site", "target"]).reset_index(drop=True)
    return out


def build_family_maxn_matrix() -> pd.DataFrame:
    rows: List[Dict[str, object]] = []
    files = sorted(list(CORAL_REEF_DIR.glob("*.csv")) + list(NURSERY_DIR.glob("*.csv")))

    for csv_path in files:
        _, site, bait = parse_video_metadata(csv_path.name)
        bait_type = BAIT_TYPE.get(bait, "other")
        if site not in SITES or bait_type not in {"fish", "algae"}:
            continue

        raw = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")
        counts: Dict[Tuple[str, float], int] = {}

        for _, row in raw.iterrows():
            if is_truthy(row.get("feeding", "")) or is_truthy(row.get("interested", "")):
                continue
            fam = clean_text(row.get("family", "")).lower()
            if not fam:
                continue
            t = parse_frame_time(row.get("frames", ""))
            if t is None:
                continue
            key = (fam, t)
            counts[key] = counts.get(key, 0) + 1

        by_family: Dict[str, int] = {}
        for (fam, _), n in counts.items():
            by_family[fam] = max(by_family.get(fam, 0), n)

        for fam, maxn in by_family.items():
            rows.append(
                {
                    "filename": csv_path.name,
                    "site": site,
                    "bait": bait,
                    "bait_type": bait_type,
                    "family": fam,
                    "maxn": int(maxn),
                }
            )

    return pd.DataFrame(rows)


def run_prevalence_threshold() -> pd.DataFrame:
    fam_df = build_family_maxn_matrix()
    if fam_df.empty:
        return fam_df

    video_df = fam_df[["filename", "site", "bait_type"]].drop_duplicates().copy()

    rows: List[Dict[str, object]] = []
    for site in SITES:
        site_videos = video_df[video_df["site"] == site].copy()
        n_algae_total = int((site_videos["bait_type"] == "algae").sum())
        n_fish_total = int((site_videos["bait_type"] == "fish").sum())
        if n_algae_total == 0 or n_fish_total == 0:
            continue

        site_fam = fam_df[fam_df["site"] == site]
        families = sorted(site_fam["family"].unique().tolist())

        for fam in families:
            subset = site_fam[site_fam["family"] == fam]
            present_files = set(subset.loc[subset["maxn"] > 0, "filename"].tolist())

            algae_files = set(site_videos.loc[site_videos["bait_type"] == "algae", "filename"].tolist())
            fish_files = set(site_videos.loc[site_videos["bait_type"] == "fish", "filename"].tolist())

            algae_present = len(algae_files & present_files)
            fish_present = len(fish_files & present_files)

            algae_rate = algae_present / n_algae_total
            fish_rate = fish_present / n_fish_total
            present_total = algae_present + fish_present

            if max(algae_rate, fish_rate) < THRESH_PREV_ANY:
                continue
            if present_total < THRESH_PRESENT_TOTAL:
                continue

            table = np.array(
                [
                    [algae_present, n_algae_total - algae_present],
                    [fish_present, n_fish_total - fish_present],
                ],
                dtype=int,
            )

            # Two-sided plus one-sided in observed direction.
            p_two = float(stats.fisher_exact(table, alternative="two-sided").pvalue)
            if algae_rate >= fish_rate:
                direction = "algae>fish"
                p_dir = float(stats.fisher_exact(table, alternative="greater").pvalue)
            else:
                direction = "fish>algae"
                p_dir = float(stats.fisher_exact(table, alternative="less").pvalue)

            rows.append(
                {
                    "site": site,
                    "family": fam,
                    "algae_present": algae_present,
                    "algae_total": n_algae_total,
                    "fish_present": fish_present,
                    "fish_total": n_fish_total,
                    "algae_rate": algae_rate,
                    "fish_rate": fish_rate,
                    "present_total": present_total,
                    "direction_observed": direction,
                    "fisher_p_two_sided": p_two,
                    "fisher_p_directional": p_dir,
                }
            )

    out = pd.DataFrame(rows)
    if out.empty:
        return out

    out["q_bh_two_sided_site"] = np.nan
    out["q_holm_two_sided_site"] = np.nan
    out["q_bh_directional_site"] = np.nan
    out["q_holm_directional_site"] = np.nan

    for site, idx in out.groupby("site").groups.items():
        idx_list = list(idx)
        p_two = out.loc[idx_list, "fisher_p_two_sided"].to_numpy(dtype=float)
        p_dir = out.loc[idx_list, "fisher_p_directional"].to_numpy(dtype=float)

        _, q_bh_two, _, _ = multipletests(p_two, method="fdr_bh")
        _, q_holm_two, _, _ = multipletests(p_two, method="holm")
        _, q_bh_dir, _, _ = multipletests(p_dir, method="fdr_bh")
        _, q_holm_dir, _, _ = multipletests(p_dir, method="holm")

        out.loc[idx_list, "q_bh_two_sided_site"] = q_bh_two
        out.loc[idx_list, "q_holm_two_sided_site"] = q_holm_two
        out.loc[idx_list, "q_bh_directional_site"] = q_bh_dir
        out.loc[idx_list, "q_holm_directional_site"] = q_holm_dir

    out = out.sort_values(["site", "q_holm_directional_site", "fisher_p_directional", "family"]).reset_index(drop=True)
    return out


def write_bootstrap_report(df: pd.DataFrame) -> None:
    OUT_BOOT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_BOOT_CSV, index=False)

    lines: List[str] = []
    lines.append("# Priorisierte Effektgroessen: Bootstrap-Konfidenzintervalle")
    lines.append("")
    lines.append("Stand: 2026-08-16")
    lines.append("")
    lines.append("## Methode")
    lines.append("")
    lines.append("- Kontraste: a-priori Herbivore-MaxN (site x family) und Herbivore-Feeding-Responsiveness (site).")
    lines.append("- Bootstrap: 5000 Resamples je Kontrast (mit Zuruecklegen, gruppenweise).")
    lines.append("- Ausgegeben: CIs fuer Mittelwertdifferenz, Mediandifferenz und Cliff's Delta.")
    lines.append("- p-Werte: gerichteter Mann-Whitney-Test (algae > fish), Korrektur mit BH/Holm je Analyseblock.")
    lines.append("")

    if df.empty:
        lines.append("Keine Ergebnisse berechnet.")
    else:
        for block in ["herbivore_maxn_apriori", "herbivore_feeding_responsiveness"]:
            part = df[df["analysis_block"] == block].copy()
            if part.empty:
                continue
            lines.append(f"## {block}")
            lines.append("")
            show = part[
                [
                    "site",
                    "target",
                    "n_algae",
                    "n_fish",
                    "mean_diff_algae_minus_fish",
                    "ci_mean_diff_low",
                    "ci_mean_diff_high",
                    "median_diff_algae_minus_fish",
                    "ci_median_diff_low",
                    "ci_median_diff_high",
                    "cliffs_delta",
                    "ci_cliffs_delta_low",
                    "ci_cliffs_delta_high",
                    "p_value_mwu_one_sided",
                    "q_holm",
                ]
            ]
            lines.append(show.to_markdown(index=False, floatfmt=".4f"))
            lines.append("")

    OUT_BOOT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_prevalence_report(df: pd.DataFrame) -> None:
    OUT_PREV_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_PREV_CSV, index=False)

    lines: List[str] = []
    lines.append("# Prevalence-/Occupancy-Modell mit Mindestnachweis-Schwellen")
    lines.append("")
    lines.append("Stand: 2026-08-16")
    lines.append("")
    lines.append("## Methode")
    lines.append("")
    lines.append("- Einheit: Familie x Video (Presence via family-maxn > 0; fish/algae-Koeder).")
    lines.append(f"- Filter 1: max(Prevalenz_algae, Prevalenz_fish) >= {THRESH_PREV_ANY:.2f}.")
    lines.append(f"- Filter 2: Gesamtzahl praesenter Videos >= {THRESH_PRESENT_TOTAL}.")
    lines.append("- Test: Fisher-Exact (two-sided und zusaetzlich one-sided in beobachteter Richtung).")
    lines.append("- Multiple Tests: BH/Holm je Standort.")
    lines.append("")

    if df.empty:
        lines.append("Keine Familien erfuellen die Schwellenkriterien.")
    else:
        for site in SITES:
            part = df[df["site"] == site].copy()
            if part.empty:
                continue
            lines.append(f"## {site}")
            lines.append("")
            show = part[
                [
                    "family",
                    "algae_present",
                    "algae_total",
                    "fish_present",
                    "fish_total",
                    "algae_rate",
                    "fish_rate",
                    "direction_observed",
                    "fisher_p_directional",
                    "q_holm_directional_site",
                    "q_bh_directional_site",
                ]
            ]
            lines.append(show.to_markdown(index=False, floatfmt=".4f"))
            lines.append("")

    OUT_PREV_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    boot_df = run_bootstrap_effectsizes()
    prev_df = run_prevalence_threshold()

    write_bootstrap_report(boot_df)
    write_prevalence_report(prev_df)

    print(f"Wrote: {OUT_BOOT_CSV}")
    print(f"Wrote: {OUT_BOOT_MD}")
    print(f"Wrote: {OUT_PREV_CSV}")
    print(f"Wrote: {OUT_PREV_MD}")


if __name__ == "__main__":
    main()
