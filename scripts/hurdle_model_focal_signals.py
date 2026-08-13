#!/usr/bin/env python3
from __future__ import annotations

import math
import re
import warnings
from pathlib import Path
from typing import Iterable, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats
from statsmodels.tools.sm_exceptions import PerfectSeparationError

warnings.filterwarnings("ignore", category=sm.tools.sm_exceptions.PerfectSeparationWarning)

ROOT = Path(__file__).resolve().parents[1]
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min"
CORAL_REEF_DIR = CUT_ROOT / "Annotation_reports_coral_reef"
NURSERY_DIR = CUT_ROOT / "Annotation_reports_Nursery"
OUT_DIR = ROOT / "results" / "hurdle_model"
FIG_DIR = ROOT / "results" / "ergaenzende_statistische_grafiken"

BAIT_MAP = {
    "mackerel": "fish",
    "fischmix": "fish",
    "sargassum": "algae",
    "ulva_salad": "algae",
    "ulva_gutweed": "algae",
    "algaemix": "algae",
    "algae_strings": "algae",
}

TARGETS = [
    {
        "signal": "nursery_acanthuridae",
        "label": "Nursery: Acanthuridae",
        "sites": ["nursery"],
        "family": "acanthuridae",
        "expected_direction": "algae > fish",
    },
    {
        "signal": "coral_labridae",
        "label": "Coral reef: Labridae",
        "sites": ["milimani", "utumbi"],
        "family": "labridae",
        "expected_direction": "fish > algae",
    },
    {
        "signal": "coral_balistidae",
        "label": "Coral reef: Balistidae",
        "sites": ["milimani", "utumbi"],
        "family": "balistidae",
        "expected_direction": "fish > algae",
    },
    {
        "signal": "coral_muraenidae",
        "label": "Coral reef: Muraenidae",
        "sites": ["milimani", "utumbi"],
        "family": "muraenidae",
        "expected_direction": "fish > algae",
    },
    {
        "signal": "coral_siganidae",
        "label": "Coral reef: Siganidae",
        "sites": ["milimani", "utumbi"],
        "family": "siganidae",
        "expected_direction": "algae > fish",
    },
    {
        "signal": "coral_scaridae",
        "label": "Coral reef: Scaridae",
        "sites": ["milimani", "utumbi"],
        "family": "scaridae",
        "expected_direction": "algae > fish",
    },
]


def parse_video_metadata(filename: str) -> tuple[str, str, str]:
    stem = filename.replace(".csv", "")
    parts = stem.split("-", 2)
    if len(parts) < 3:
        return "", "unknown", "unknown"
    date, site, bait = parts
    return date, site.lower(), bait.lower()


def is_truthy(value: object) -> bool:
    if value is None:
        return False
    text = str(value).strip().lower()
    return text not in {"", "0", "false", "f", "no", "n", "none", "null", "nan"}


def parse_frame_time(frame_value: object) -> float | None:
    text = str(frame_value).strip()
    if not text:
        return None
    match = re.search(r"[-+]?\d*\.?\d+", text)
    if not match:
        return None
    try:
        return round(float(match.group(0)), 2)
    except ValueError:
        return None


def bh_adjust(pvals: Iterable[float]) -> List[float]:
    vals = np.asarray(list(pvals), dtype=float)
    m = len(vals)
    if m == 0:
        return []
    order = np.argsort(vals)
    adjusted = np.empty(m, dtype=float)
    ranked = vals[order]
    tmp = ranked * m / np.arange(1, m + 1)
    tmp = np.minimum.accumulate(tmp[::-1])[::-1]
    tmp = np.clip(tmp, 0.0, 1.0)
    adjusted[order] = tmp
    return adjusted.tolist()


def one_sided_p_from_z(z_value: float, expected_direction: str) -> float:
    if expected_direction == "algae > fish":
        return 1.0 - stats.norm.cdf(z_value)
    return stats.norm.cdf(z_value)


def bootstrap_ci_median_diff(algae_vals: np.ndarray, fish_vals: np.ndarray, n_boot: int = 4000) -> tuple[float, float]:
    if len(algae_vals) == 0 or len(fish_vals) == 0:
        return (np.nan, np.nan)
    rng = np.random.default_rng(20260813)
    diffs = []
    for _ in range(n_boot):
        a = rng.choice(algae_vals, size=len(algae_vals), replace=True)
        f = rng.choice(fish_vals, size=len(fish_vals), replace=True)
        diffs.append(float(np.median(a) - np.median(f)))
    return (float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5)))


def maxn_per_video(target: dict) -> pd.DataFrame:
    family = target["family"]
    sites = set(target["sites"])
    rows = []
    files = list(CORAL_REEF_DIR.glob("*.csv")) + list(NURSERY_DIR.glob("*.csv"))
    for csv_path in sorted(files):
        _, site, bait = parse_video_metadata(csv_path.name)
        if site not in sites or bait not in BAIT_MAP:
            continue
        bait_type = BAIT_MAP[bait]
        if bait_type not in {"algae", "fish"}:
            continue

        df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")
        counts: dict[tuple[str, float], int] = {}
        for _, row in df.iterrows():
            if is_truthy(row.get("feeding", "")) or is_truthy(row.get("interested", "")):
                continue
            fam = str(row.get("family", "")).strip().lower()
            if fam != family:
                continue
            frame_time = parse_frame_time(row.get("frames", ""))
            if frame_time is None:
                continue
            counts[(fam, frame_time)] = counts.get((fam, frame_time), 0) + 1

        maxn = max(counts.values()) if counts else 0
        rows.append(
            {
                "signal": target["signal"],
                "label": target["label"],
                "site": site,
                "family": family,
                "bait_type": bait_type,
                "bait_is_algae": 1 if bait_type == "algae" else 0,
                "maxn": int(maxn),
            }
        )

    return pd.DataFrame(rows)


def fit_presence_model(df: pd.DataFrame, expected_direction: str) -> dict:
    y = (df["maxn"] > 0).astype(int)
    X = sm.add_constant(df[["bait_is_algae"]], has_constant="add")
    out = {
        "presence_coef": np.nan,
        "presence_or": np.nan,
        "presence_ci_low": np.nan,
        "presence_ci_high": np.nan,
        "presence_p_one_sided": np.nan,
        "presence_p_two_sided": np.nan,
        "presence_method": "glm_binomial",
    }

    try:
        fit = sm.GLM(y, X, family=sm.families.Binomial()).fit()
        coef = float(fit.params["bait_is_algae"])
        se = float(fit.bse["bait_is_algae"])
        z_value = coef / se if se > 0 else np.nan
        ci = fit.conf_int().loc["bait_is_algae"].to_numpy(dtype=float)

        # With near-perfect separation, OR CI can explode and become numerically unstable.
        if (not np.isfinite(coef)) or (not np.isfinite(ci).all()) or max(abs(ci[0]), abs(ci[1]), abs(coef)) > 20:
            raise ValueError("unstable logistic estimate")

        out.update(
            {
                "presence_coef": coef,
                "presence_or": float(math.exp(coef)),
                "presence_ci_low": float(math.exp(ci[0])),
                "presence_ci_high": float(math.exp(ci[1])),
                "presence_p_one_sided": float(one_sided_p_from_z(z_value, expected_direction)) if np.isfinite(z_value) else np.nan,
                "presence_p_two_sided": float(fit.pvalues["bait_is_algae"]),
            }
        )
    except (PerfectSeparationError, np.linalg.LinAlgError, ValueError, OverflowError):
        algae = (df.loc[df["bait_type"] == "algae", "maxn"] > 0).astype(int)
        fish = (df.loc[df["bait_type"] == "fish", "maxn"] > 0).astype(int)
        table = np.array(
            [
                [int(algae.sum()), int(len(algae) - algae.sum())],
                [int(fish.sum()), int(len(fish) - fish.sum())],
            ],
            dtype=int,
        )
        alt = "greater" if expected_direction == "algae > fish" else "less"
        out["presence_p_one_sided"] = float(stats.fisher_exact(table, alternative=alt).pvalue)
        out["presence_method"] = "fisher_fallback"

    return out


def fit_positive_intensity_model(df: pd.DataFrame, expected_direction: str) -> dict:
    pos = df[df["maxn"] > 0].copy()
    out = {
        "intensity_coef_log1p": np.nan,
        "intensity_ci_low": np.nan,
        "intensity_ci_high": np.nan,
        "intensity_p_one_sided": np.nan,
        "intensity_p_two_sided": np.nan,
        "positive_algae_n": int((pos["bait_type"] == "algae").sum()),
        "positive_fish_n": int((pos["bait_type"] == "fish").sum()),
        "median_diff_positive_maxn": np.nan,
        "median_diff_ci_low": np.nan,
        "median_diff_ci_high": np.nan,
        "intensity_method": "ols_hc3",
    }

    algae_pos = pos.loc[pos["bait_type"] == "algae", "maxn"].to_numpy(dtype=float)
    fish_pos = pos.loc[pos["bait_type"] == "fish", "maxn"].to_numpy(dtype=float)
    if len(algae_pos) == 0 or len(fish_pos) == 0:
        out["intensity_method"] = "insufficient_positive_data"
        return out

    out["median_diff_positive_maxn"] = float(np.median(algae_pos) - np.median(fish_pos))
    ci_low, ci_high = bootstrap_ci_median_diff(algae_pos, fish_pos)
    out["median_diff_ci_low"] = ci_low
    out["median_diff_ci_high"] = ci_high

    if len(algae_pos) < 2 or len(fish_pos) < 2:
        out["intensity_method"] = "insufficient_group_size"
        return out

    pos["y_log1p"] = np.log1p(pos["maxn"].astype(float))
    X = sm.add_constant(pos[["bait_is_algae"]], has_constant="add")
    fit = sm.OLS(pos["y_log1p"], X).fit(cov_type="HC3")

    coef = float(fit.params["bait_is_algae"])
    se = float(fit.bse["bait_is_algae"])
    z_value = coef / se if se > 0 else np.nan
    ci = fit.conf_int().loc["bait_is_algae"].to_numpy(dtype=float)
    out.update(
        {
            "intensity_coef_log1p": coef,
            "intensity_ci_low": float(ci[0]),
            "intensity_ci_high": float(ci[1]),
            "intensity_p_one_sided": float(one_sided_p_from_z(z_value, expected_direction)) if np.isfinite(z_value) else np.nan,
            "intensity_p_two_sided": float(fit.pvalues["bait_is_algae"]),
        }
    )
    return out


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []

    for target in TARGETS:
        df = maxn_per_video(target)
        if df.empty:
            continue

        presence = fit_presence_model(df, target["expected_direction"])
        intensity = fit_positive_intensity_model(df, target["expected_direction"])

        algae_mask = df["bait_type"] == "algae"
        fish_mask = df["bait_type"] == "fish"
        rows.append(
            {
                "signal": target["signal"],
                "label": target["label"],
                "family": target["family"],
                "sites": ", ".join(target["sites"]),
                "expected_direction": target["expected_direction"],
                "n_algae_total": int(algae_mask.sum()),
                "n_fish_total": int(fish_mask.sum()),
                "n_algae_present": int((df.loc[algae_mask, "maxn"] > 0).sum()),
                "n_fish_present": int((df.loc[fish_mask, "maxn"] > 0).sum()),
                "presence_rate_algae": float((df.loc[algae_mask, "maxn"] > 0).mean()),
                "presence_rate_fish": float((df.loc[fish_mask, "maxn"] > 0).mean()),
                "maxn_median_algae": float(df.loc[algae_mask, "maxn"].median()),
                "maxn_median_fish": float(df.loc[fish_mask, "maxn"].median()),
                **presence,
                **intensity,
            }
        )

    summary = pd.DataFrame(rows)
    if summary.empty:
        raise RuntimeError("No focal signals could be analyzed")

    summary["presence_q_bh"] = np.nan
    summary["intensity_q_bh"] = np.nan

    p_mask = summary["presence_p_one_sided"].notna()
    summary.loc[p_mask, "presence_q_bh"] = bh_adjust(summary.loc[p_mask, "presence_p_one_sided"].tolist())

    i_mask = summary["intensity_p_one_sided"].notna()
    summary.loc[i_mask, "intensity_q_bh"] = bh_adjust(summary.loc[i_mask, "intensity_p_one_sided"].tolist())

    summary["presence_sig_q_0_05"] = summary["presence_q_bh"] < 0.05
    summary["intensity_sig_q_0_05"] = summary["intensity_q_bh"] < 0.05

    summary = summary.sort_values(["presence_q_bh", "intensity_q_bh"], na_position="last").reset_index(drop=True)
    summary_path = OUT_DIR / "hurdle_model_summary.csv"
    summary.to_csv(summary_path, index=False)

    lines = [
        "# Hurdle-Modell fuer fokussierte Signale",
        "",
        "Zweistufiges Modell pro Signal:",
        "1) Praesenzteil: GLM Binomial (logistische Regression) fuer Nachweis ja/nein.",
        "2) Intensitaetsteil: OLS auf log1p(MaxN) nur fuer Videos mit MaxN > 0 (HC3 robuste Standardfehler).",
        "",
        "Die gerichtete Hypothese folgt der biologischen Erwartung (algae > fish bzw. fish > algae).",
        "BH/FDR wird getrennt fuer Praesenz- und Intensitaetsteil ueber alle fokussierten Signale korrigiert.",
        "",
        "| signal | direction | pres_algae | pres_fish | presence_p | presence_q | intensity_beta | intensity_p | intensity_q |",
        "|:---|:---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary.itertuples(index=False):
        lines.append(
            f"| {row.signal} | {row.expected_direction} | {row.presence_rate_algae:.3f} | {row.presence_rate_fish:.3f} | {row.presence_p_one_sided:.6f} | {row.presence_q_bh:.6f} | {row.intensity_coef_log1p:.4f} | {row.intensity_p_one_sided:.6f} | {row.intensity_q_bh:.6f} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- Das Hurdle-Modell trennt explizit zwischen Occurrence und Dichte. Dadurch wird sichtbar, ob ein Koedereffekt auf haeufigeres Auftreten oder auf staerkere Auspraegung bei bereits vorhandenem Taxon basiert.",
            "- Ein signifikanter Praesenzteil bei nicht-signifikantem Intensitaetsteil spricht fuer occurrence-getriebene Unterschiede.",
            "- Ein signifikanter Intensitaetsteil bei nicht-signifikantem Praesenzteil spricht fuer dichte-/aktivitaetsgetriebene Unterschiede.",
            "- Konsistente Signifikanz in beiden Stufen waere der staerkste Hinweis auf einen breiten, biologisch robusten Koedereffekt.",
        ]
    )
    (OUT_DIR / "hurdle_model_focal_signals.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 6.4), sharey=True)
    y = np.arange(len(summary))

    # Left panel: log(OR) for presence
    ax = axes[0]
    for i, row in enumerate(summary.itertuples(index=False)):
        if np.isfinite(row.presence_or) and row.presence_or > 0 and np.isfinite(row.presence_ci_low) and np.isfinite(row.presence_ci_high) and row.presence_ci_low > 0:
            center = math.log(row.presence_or)
            low = math.log(row.presence_ci_low)
            high = math.log(row.presence_ci_high)
            ax.hlines(i, low, high, color="#1f77b4", linewidth=2)
            ax.plot(center, i, "o", color="#1f77b4")
        else:
            # Fisher fallback or non-estimable model
            ax.plot(0.0, i, "x", color="#666666")

    ax.axvline(0.0, color="black", linewidth=1, alpha=0.6)
    ax.set_title("Praesenzteil: log(OR) Algae vs Fish")
    ax.set_xlabel("log(odds ratio)")
    ax.grid(axis="x", alpha=0.2)

    # Right panel: beta on log1p(MaxN) among positives
    ax2 = axes[1]
    for i, row in enumerate(summary.itertuples(index=False)):
        if np.isfinite(row.intensity_coef_log1p):
            ax2.hlines(i, row.intensity_ci_low, row.intensity_ci_high, color="#d62728", linewidth=2)
            ax2.plot(row.intensity_coef_log1p, i, "o", color="#d62728")
        else:
            ax2.plot(0.0, i, "x", color="#666666")

    ax2.axvline(0.0, color="black", linewidth=1, alpha=0.6)
    ax2.set_title("Intensitaetsteil: beta auf log1p(MaxN)")
    ax2.set_xlabel("Koeffizient (Algae - Fish)")
    ax2.grid(axis="x", alpha=0.2)

    axes[0].set_yticks(y)
    axes[0].set_yticklabels(summary["label"].tolist())
    axes[0].invert_yaxis()

    fig.suptitle("Hurdle-Modell: Zerlegung in Praesenz- und Intensitaetseffekt", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(FIG_DIR / "11_hurdle_model_effect_decomposition.png", dpi=220, bbox_inches="tight")
    plt.close(fig)

    print(f"Wrote {summary_path}")
    print(f"Wrote {OUT_DIR / 'hurdle_model_focal_signals.md'}")
    print(f"Wrote {FIG_DIR / '11_hurdle_model_effect_decomposition.png'}")


if __name__ == "__main__":
    main()
