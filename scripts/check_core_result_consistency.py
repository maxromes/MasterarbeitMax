#!/usr/bin/env python3
"""
Checks consistency between key result artifacts.

Current checks:
1) species_richness_all_46_videos.csv vs standortvergleich_video_level.csv
   - same set of filenames
   - same species_richness and rows_used per filename
2) one_pager_species_richness.md top-10 table vs species_richness_all_46_videos.csv top-10
3) visibility_summary.md raw-correlation table vs visibility_vs_metrics_correlations.csv
4) visibility_adjusted_summary.md adjusted-model table vs visibility_adjusted_model_results.csv

Usage:
    python scripts/check_core_result_consistency.py
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

SPECIES_ALL = ROOT / "results" / "species_richness_report" / "species_richness_all_46_videos.csv"
STANDORT_VIDEO = ROOT / "results" / "Standortvergleich" / "standortvergleich_video_level.csv"
ONE_PAGER = ROOT / "results" / "species_richness_report" / "one_pager_species_richness.md"
VIS_SUMMARY = ROOT / "results" / "visibility_analysis" / "visibility_summary.md"
VIS_CORR = ROOT / "results" / "visibility_analysis" / "visibility_vs_metrics_correlations.csv"
VIS_ADJ_SUMMARY = ROOT / "results" / "visibility_analysis" / "visibility_adjusted_summary.md"
VIS_ADJ = ROOT / "results" / "visibility_analysis" / "visibility_adjusted_model_results.csv"


def _parse_float(value: str) -> float:
    return float(value.strip().replace("%", ""))


def _close(a: float, b: float, tol: float) -> bool:
    return abs(float(a) - float(b)) <= tol


def check_video_level_consistency(errors: list[str]) -> None:
    a = pd.read_csv(SPECIES_ALL)
    b = pd.read_csv(STANDORT_VIDEO)

    cols_a = ["filename", "species_richness", "rows_used"]
    cols_b = ["filename", "species_richness", "rows_used"]

    aa = a[cols_a].copy().sort_values("filename").reset_index(drop=True)
    bb = b[cols_b].copy().sort_values("filename").reset_index(drop=True)

    set_a = set(aa["filename"].tolist())
    set_b = set(bb["filename"].tolist())

    only_a = sorted(set_a - set_b)
    only_b = sorted(set_b - set_a)
    if only_a:
        errors.append(f"Files only in species_richness_all: {only_a[:5]}{' ...' if len(only_a) > 5 else ''}")
    if only_b:
        errors.append(f"Files only in standortvergleich_video_level: {only_b[:5]}{' ...' if len(only_b) > 5 else ''}")

    merged = aa.merge(bb, on="filename", suffixes=("_species", "_standort"), how="inner")
    diff = merged[
        (merged["species_richness_species"] != merged["species_richness_standort"])
        | (merged["rows_used_species"] != merged["rows_used_standort"])
    ]

    if not diff.empty:
        sample = diff.head(10)
        rows = []
        for r in sample.itertuples(index=False):
            rows.append(
                f"{r.filename}: richness {r.species_richness_species} vs {r.species_richness_standort}, "
                f"rows_used {r.rows_used_species} vs {r.rows_used_standort}"
            )
        errors.append("Video-level mismatch between reports: " + " | ".join(rows))


def parse_onepager_top10(markdown_text: str) -> list[tuple[str, int]]:
    out: list[tuple[str, int]] = []
    # Example row:
    # | 1 | 20240516-utumbi-mackerel.csv | utumbi | mackerel | 61 |
    pattern = re.compile(r"^\|\s*\d+\s*\|\s*([^|]+?)\s*\|\s*[^|]+\|\s*[^|]+\|\s*(\d+)\s*\|\s*$")
    in_top10 = False

    for line in markdown_text.splitlines():
        if line.strip().startswith("## Top 10 Videos nach Species Richness"):
            in_top10 = True
            continue
        if in_top10 and line.strip().startswith("## "):
            break
        if not in_top10:
            continue

        m = pattern.match(line.strip())
        if m:
            filename = m.group(1).strip()
            richness = int(m.group(2))
            out.append((filename, richness))

    return out


def check_onepager_top10(errors: list[str]) -> None:
    all_df = pd.read_csv(SPECIES_ALL)
    top = all_df.sort_values(["species_richness", "filename"], ascending=[False, True]).head(10)
    expected = list(zip(top["filename"].tolist(), top["species_richness"].astype(int).tolist()))

    text = ONE_PAGER.read_text(encoding="utf-8")
    got = parse_onepager_top10(text)

    if len(got) != 10:
        errors.append(f"One-pager top-10 table has {len(got)} parsed rows (expected 10).")
        return

    if got != expected:
        errors.append(
            "One-pager top-10 does not match species_richness_all_46_videos.csv. "
            f"Expected first row {expected[0]}, got {got[0]}."
        )


def check_visibility_summary_table(errors: list[str]) -> None:
    corr = pd.read_csv(VIS_CORR)
    text = VIS_SUMMARY.read_text(encoding="utf-8")

    metric_map = {
        "MaxN (video peak)": "maxn_video_peak",
        "Species Richness": "species_richness",
        "First Seen (Median, s)": "first_seen_median_sec",
    }

    found: dict[str, dict[str, float]] = {}
    pattern = re.compile(
        r"^\|\s*(MaxN \(video peak\)|Species Richness|First Seen \(Median, s\))\s*\|\s*"
        r"(\d+)\s*\|\s*([-0-9.eE]+)\s*\|\s*([-0-9.eE]+)\s*\|\s*([-0-9.eE]+)\s*\|\s*"
        r"([-0-9.eE]+)\s*\|\s*([-0-9.eE]+)\s*\|"
    )

    for line in text.splitlines():
        m = pattern.match(line.strip())
        if not m:
            continue
        label = m.group(1)
        found[metric_map[label]] = {
            "n": int(m.group(2)),
            "spearman_rho": _parse_float(m.group(3)),
            "spearman_p": _parse_float(m.group(4)),
            "spearman_q_bh": _parse_float(m.group(5)),
            "kendall_tau": _parse_float(m.group(6)),
            "pearson_r": _parse_float(m.group(7)),
        }

    if len(found) != 3:
        errors.append(f"Could not parse all 3 rows from visibility_summary.md (parsed {len(found)}).")
        return

    for metric in ["maxn_video_peak", "species_richness", "first_seen_median_sec"]:
        row = corr.loc[corr["metric"] == metric]
        if row.empty:
            errors.append(f"Missing metric in visibility_vs_metrics_correlations.csv: {metric}")
            continue
        row = row.iloc[0]
        got = found[metric]

        if int(row["n"]) != int(got["n"]):
            errors.append(f"visibility_summary n mismatch for {metric}: md={got['n']} csv={int(row['n'])}")

        checks = [
            ("spearman_rho", 0.0015),
            ("spearman_p", 0.0007),
            ("spearman_q_bh", 0.0007),
            ("kendall_tau", 0.0015),
            ("pearson_r", 0.0015),
        ]
        for key, tol in checks:
            if not _close(got[key], float(row[key]), tol):
                errors.append(
                    f"visibility_summary mismatch for {metric}.{key}: md={got[key]} csv={float(row[key])}"
                )


def check_visibility_adjusted_table(errors: list[str]) -> None:
    adj = pd.read_csv(VIS_ADJ)
    text = VIS_ADJ_SUMMARY.read_text(encoding="utf-8")

    found: dict[str, dict[str, float]] = {}
    pattern = re.compile(
        r"^\|\s*(maxn_video_peak|species_richness|first_seen_median_sec)\s*\|\s*"
        r"(\d+)\s*\|\s*([-0-9.eE]+)\s*\|\s*\[\s*([-0-9.eE]+)\s*,\s*([-0-9.eE]+)\s*\]\s*\|\s*"
        r"([-0-9.eE]+)%\s*\|\s*([-0-9.eE]+)\s*\|\s*([-0-9.eE]+)\s*\|\s*([-0-9.eE]+)\s*\|\s*([-0-9.eE]+)\s*\|"
    )

    for line in text.splitlines():
        m = pattern.match(line.strip())
        if not m:
            continue
        metric = m.group(1)
        found[metric] = {
            "n": int(m.group(2)),
            "coef_visibility_log1p": _parse_float(m.group(3)),
            "coef_ci95_low": _parse_float(m.group(4)),
            "coef_ci95_high": _parse_float(m.group(5)),
            "pct_change_per_visibility_unit": _parse_float(m.group(6)),
            "p_hc3": _parse_float(m.group(7)),
            "q_hc3_bh": _parse_float(m.group(8)),
            "p_perm": _parse_float(m.group(9)),
            "q_perm_bh": _parse_float(m.group(10)),
        }

    if len(found) != 3:
        errors.append(f"Could not parse all 3 rows from visibility_adjusted_summary.md (parsed {len(found)}).")
        return

    for metric in ["maxn_video_peak", "species_richness", "first_seen_median_sec"]:
        row = adj.loc[adj["metric"] == metric]
        if row.empty:
            errors.append(f"Missing metric in visibility_adjusted_model_results.csv: {metric}")
            continue
        row = row.iloc[0]
        got = found[metric]

        if int(row["n"]) != int(got["n"]):
            errors.append(f"visibility_adjusted_summary n mismatch for {metric}: md={got['n']} csv={int(row['n'])}")

        checks = [
            ("coef_visibility_log1p", 0.0015),
            ("coef_ci95_low", 0.0015),
            ("coef_ci95_high", 0.0015),
            ("pct_change_per_visibility_unit", 0.11),
            ("p_hc3", 0.0007),
            ("q_hc3_bh", 0.0007),
            ("p_perm", 0.0007),
            ("q_perm_bh", 0.0007),
        ]
        for key, tol in checks:
            if not _close(got[key], float(row[key]), tol):
                errors.append(
                    f"visibility_adjusted_summary mismatch for {metric}.{key}: md={got[key]} csv={float(row[key])}"
                )


def main() -> int:
    errors: list[str] = []

    for p in [
        SPECIES_ALL,
        STANDORT_VIDEO,
        ONE_PAGER,
        VIS_SUMMARY,
        VIS_CORR,
        VIS_ADJ_SUMMARY,
        VIS_ADJ,
    ]:
        if not p.exists():
            errors.append(f"Missing file: {p}")

    if errors:
        print("FAILED")
        for e in errors:
            print(f"- {e}")
        return 1

    check_video_level_consistency(errors)
    check_onepager_top10(errors)
    check_visibility_summary_table(errors)
    check_visibility_adjusted_table(errors)

    if errors:
        print("FAILED")
        for e in errors:
            print(f"- {e}")
        return 1

    print("OK: Core result files are consistent.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
