#!/usr/bin/env python3
"""
Herbivore Feeding Responsiveness Test:
Testet die Hypothese, dass Herbivore häufiger "feeding" bei Algenködern zeigen
als bei Fischködern.

Fokus: Label "feeding" (nicht MaxN, sondern Häufigkeit des Verhaltens).

Ausgabe:
- results/herbivore_analysis/herbivore_feeding_responsiveness.md
- results/herbivore_analysis/herbivore_feeding_responsiveness.csv
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min"
CORAL_REEF_DIR = CUT_ROOT / "Annotation_reports_coral_reef"
NURSERY_DIR = CUT_ROOT / "Annotation_reports_Nursery"

OUT_DIR = ROOT / "results" / "herbivore_analysis"

SITES = ["milimani", "utumbi", "nursery"]
ALPHA = 0.05

# Köder-Kategorisierung
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

# Herbivore-Familien (Kern-Definition)
HERBIVORE_CORE_FAMILIES = {"siganidae", "acanthuridae", "scaridae", "blenniidae"}


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
    if text in {"", "0", "false", "f", "no", "n", "none", "null", "nan"}:
        return False
    return True


def parse_video_metadata(filename: str) -> Tuple[str, str, str]:
    stem = filename.replace(".csv", "")
    parts = stem.split("-", 2)
    if len(parts) < 3:
        return ("", "unknown", "unknown")
    date, standort, koeder = parts
    return (date, standort.lower(), koeder.lower())


def extract_family(row: pd.Series) -> str | None:
    family = clean_text(row.get("family", "")).lower()
    if family in HERBIVORE_CORE_FAMILIES:
        return family
    return None


def parse_frame_time(frame_value: object) -> float | None:
    text = clean_text(frame_value)
    if not text:
        return None
    match = re.search(r"[-+]?\d*\.?\d+", text)
    if not match:
        return None
    try:
        return round(float(match.group(0)), 2)
    except ValueError:
        return None


def load_video_feeding(csv_path: Path) -> Dict[str, object]:
    """Lade Feeding-Daten für Herbivore aus CSV."""
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")

    feeding_count = 0
    total_herbivore_entries = 0
    feeding_by_family_time: Dict[Tuple[str, float], int] = {}
    feeding_families_present: set[str] = set()

    for _, row in df.iterrows():
        family = extract_family(row)
        if not family:
            continue

        total_herbivore_entries += 1
        if is_truthy(row.get("feeding", "")):
            feeding_count += 1
            feeding_families_present.add(family)

            frame_time = parse_frame_time(row.get("frames", ""))
            if frame_time is not None:
                key = (family, frame_time)
                feeding_by_family_time[key] = feeding_by_family_time.get(key, 0) + 1

    feeding_maxn_by_family: Dict[str, int] = {}
    for (family, _), n in feeding_by_family_time.items():
        if family not in feeding_maxn_by_family or n > feeding_maxn_by_family[family]:
            feeding_maxn_by_family[family] = int(n)

    feeding_maxn_sum = float(sum(feeding_maxn_by_family.values()))
    feeding_family_presence = float(len(feeding_families_present) / len(HERBIVORE_CORE_FAMILIES))

    date, standort, koeder = parse_video_metadata(csv_path.name)
    return {
        "filename": csv_path.name,
        "date": date,
        "standort": standort,
        "koeder": koeder,
        "feeding_count": feeding_count,
        "total_herbivore_entries": total_herbivore_entries,
        "feeding_maxn_sum": feeding_maxn_sum,
        "feeding_family_presence": feeding_family_presence,
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


def load_all_videos(site: str) -> pd.DataFrame:
    """Lade alle Video-Daten für einen Standort."""
    if site == "nursery":
        video_dir = NURSERY_DIR
    else:
        video_dir = CORAL_REEF_DIR

    if not video_dir.exists():
        return pd.DataFrame()

    video_files = sorted([f for f in video_dir.glob("*.csv") if "-" in f.name])
    video_data = []

    for csv_file in video_files:
        _, standort, koeder = parse_video_metadata(csv_file.name)
        if standort.lower() == site.lower():
            meta = load_video_feeding(csv_file)
            if meta["total_herbivore_entries"] > 0:
                video_data.append(meta)

    df = pd.DataFrame(video_data)
    return df


def analyze_site(site: str) -> Dict[str, object]:
    """Analysiere Herbivore-Feeding für einen Standort."""
    videos = load_all_videos(site)
    if videos.empty:
        return {"results": pd.DataFrame()}

    # Gruppiere nach Ködertyp
    algae_baits = [bait for bait, typ in BAIT_TYPE.items() if typ == "algae"]
    fish_baits = [bait for bait, typ in BAIT_TYPE.items() if typ == "fish"]

    algae_videos = videos[videos["koeder"].isin(algae_baits)]
    fish_videos = videos[videos["koeder"].isin(fish_baits)]

    if algae_videos.empty or fish_videos.empty:
        return {"results": pd.DataFrame()}

    # Pro Video: Berechne Feeding-Metriken
    algae_feeding_rates = []
    fish_feeding_rates = []
    algae_feeding_maxn_sums = []
    fish_feeding_maxn_sums = []
    algae_feeding_family_presence = []
    fish_feeding_family_presence = []

    for _, row in algae_videos.iterrows():
        if row["total_herbivore_entries"] > 0:
            rate = row["feeding_count"] / row["total_herbivore_entries"]
            algae_feeding_rates.append(rate)
            algae_feeding_maxn_sums.append(float(row["feeding_maxn_sum"]))
            algae_feeding_family_presence.append(float(row["feeding_family_presence"]))

    for _, row in fish_videos.iterrows():
        if row["total_herbivore_entries"] > 0:
            rate = row["feeding_count"] / row["total_herbivore_entries"]
            fish_feeding_rates.append(rate)
            fish_feeding_maxn_sums.append(float(row["feeding_maxn_sum"]))
            fish_feeding_family_presence.append(float(row["feeding_family_presence"]))

    if not algae_feeding_rates or not fish_feeding_rates:
        return {"results": pd.DataFrame()}

    algae_arr = np.array(algae_feeding_rates, dtype=float)
    fish_arr = np.array(fish_feeding_rates, dtype=float)
    algae_maxn_arr = np.array(algae_feeding_maxn_sums, dtype=float)
    fish_maxn_arr = np.array(fish_feeding_maxn_sums, dtype=float)
    algae_presence_arr = np.array(algae_feeding_family_presence, dtype=float)
    fish_presence_arr = np.array(fish_feeding_family_presence, dtype=float)

    # Mann-Whitney U Test: Algae > Fish (directional)
    _stat, pval = stats.mannwhitneyu(algae_arr, fish_arr, alternative="greater")
    _stat_maxn, pval_maxn = stats.mannwhitneyu(algae_maxn_arr, fish_maxn_arr, alternative="greater")
    _stat_presence, pval_presence = stats.mannwhitneyu(
        algae_presence_arr, fish_presence_arr, alternative="greater"
    )

    # Effektgröße (Cliffs Delta)
    total = len(algae_arr) * len(fish_arr)
    gt = sum(1 for a in algae_arr for f in fish_arr if a > f)
    lt = sum(1 for a in algae_arr for f in fish_arr if a < f)
    cliff_d = (gt - lt) / total if total > 0 else math.nan

    result = {
        "site": site,
        "algae_videos": len(algae_arr),
        "fish_videos": len(fish_arr),
        "algae_feeding_rate_mean": float(np.mean(algae_arr)),
        "algae_feeding_rate_median": float(np.median(algae_arr)),
        "algae_feeding_rate_std": float(np.std(algae_arr, ddof=1)) if len(algae_arr) > 1 else 0.0,
        "fish_feeding_rate_mean": float(np.mean(fish_arr)),
        "fish_feeding_rate_median": float(np.median(fish_arr)),
        "fish_feeding_rate_std": float(np.std(fish_arr, ddof=1)) if len(fish_arr) > 1 else 0.0,
        "rate_diff_mean_algae_minus_fish": float(np.mean(algae_arr) - np.mean(fish_arr)),
        "rate_diff_median_algae_minus_fish": float(np.median(algae_arr) - np.median(fish_arr)),
        "p_value": pval,
        "cliffs_delta": cliff_d,
        "algae_feeding_maxn_sum_mean": float(np.mean(algae_maxn_arr)),
        "fish_feeding_maxn_sum_mean": float(np.mean(fish_maxn_arr)),
        "maxn_sum_diff_mean_algae_minus_fish": float(np.mean(algae_maxn_arr) - np.mean(fish_maxn_arr)),
        "p_value_maxn_sum": float(pval_maxn),
        "algae_family_presence_mean": float(np.mean(algae_presence_arr)),
        "fish_family_presence_mean": float(np.mean(fish_presence_arr)),
        "family_presence_diff_mean_algae_minus_fish": float(
            np.mean(algae_presence_arr) - np.mean(fish_presence_arr)
        ),
        "p_value_family_presence": float(pval_presence),
    }

    return {"results": result}


def write_report(all_results: Dict[str, Dict[str, object]]) -> None:
    """Schreibe Gesamtbericht."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    md_path = OUT_DIR / "herbivore_feeding_responsiveness.md"
    csv_path = OUT_DIR / "herbivore_feeding_responsiveness.csv"

    # Sammle CSV-Daten
    csv_rows = []
    for site, result_dict in all_results.items():
        result = result_dict["results"]
        if isinstance(result, dict):
            csv_rows.append(result)

    df_csv = pd.DataFrame(csv_rows)

    # Holm-Korrektur (je 3 Tests: 1 pro Standort, getrennt nach Metrik)
    if len(df_csv) > 0 and "p_value" in df_csv.columns:
        df_csv["p_value_holm"] = holm_adjust(df_csv["p_value"].tolist())
    if len(df_csv) > 0 and "p_value_maxn_sum" in df_csv.columns:
        df_csv["p_value_maxn_sum_holm"] = holm_adjust(df_csv["p_value_maxn_sum"].tolist())
    if len(df_csv) > 0 and "p_value_family_presence" in df_csv.columns:
        df_csv["p_value_family_presence_holm"] = holm_adjust(
            df_csv["p_value_family_presence"].tolist()
        )

    with open(md_path, "w") as f:
        f.write("# Herbivore Feeding Responsiveness Test\n\n")
        f.write("**A priori Hypothese**: Herbivore zeigen signifikant häufiger Feeding-Verhalten bei Algenködern als bei Fischködern.\n\n")
        f.write("**Methode**: Pro Video und Standort wird die Feeding-Rate berechnet als (# Feeding-Events bei Herbivoren) / (# Gesamteinträge von Herbivoren).\n")
        f.write("Mann-Whitney U Test (gerichtet) testet: Algae Feeding-Rate > Fish Feeding-Rate.\n")
        f.write("Sensitivitaetsmetriken (automatisch): (a) Summe familienweiser Feeding-Maxima pro Video (MaxN-konsistent), (b) Anteil Herbivore-Familien mit mindestens einem Feeding-Eintrag.\n\n")

        f.write("## Ergebnisse nach Standort\n\n")

        for site in SITES:
            if site not in all_results:
                continue
            result = all_results[site]["results"]
            if isinstance(result, dict) and result.get("site"):
                f.write(f"### {site.capitalize()}\n\n")
                f.write(f"- **N Videos (Algae | Fish)**: {result['algae_videos']} | {result['fish_videos']}\n")
                f.write(f"- **Feeding-Rate Algae**: μ = {result['algae_feeding_rate_mean']:.4f}, σ = {result['algae_feeding_rate_std']:.4f}, median = {result['algae_feeding_rate_median']:.4f}\n")
                f.write(f"- **Feeding-Rate Fish**: μ = {result['fish_feeding_rate_mean']:.4f}, σ = {result['fish_feeding_rate_std']:.4f}, median = {result['fish_feeding_rate_median']:.4f}\n")
                f.write(f"- **Differenz (Algae - Fish)**: μ = {result['rate_diff_mean_algae_minus_fish']:.4f}, median = {result['rate_diff_median_algae_minus_fish']:.4f}\n")
                f.write(f"- **p-Wert (roh)**: {result['p_value']:.6f}\n")
                f.write(f"- **Cliffs Delta**: {result['cliffs_delta']:.4f}\n\n")
                f.write("Sensitivitaet:\n")
                f.write(
                    f"- Feeding-MaxN-Summe (mean Algae | Fish): {result['algae_feeding_maxn_sum_mean']:.4f} | {result['fish_feeding_maxn_sum_mean']:.4f}; p_raw = {result['p_value_maxn_sum']:.6f}\n"
                )
                f.write(
                    f"- Family-Presence (mean Algae | Fish): {result['algae_family_presence_mean']:.4f} | {result['fish_family_presence_mean']:.4f}; p_raw = {result['p_value_family_presence']:.6f}\n\n"
                )

        f.write("## Zusammenfassung (Holm-korrigiert)\n\n")
        if len(df_csv) > 0:
            summary_cols = [
                "site",
                "algae_feeding_rate_mean",
                "fish_feeding_rate_mean",
                "rate_diff_mean_algae_minus_fish",
                "p_value",
                "p_value_holm",
                "cliffs_delta",
                "algae_feeding_maxn_sum_mean",
                "fish_feeding_maxn_sum_mean",
                "maxn_sum_diff_mean_algae_minus_fish",
                "p_value_maxn_sum",
                "p_value_maxn_sum_holm",
                "algae_family_presence_mean",
                "fish_family_presence_mean",
                "family_presence_diff_mean_algae_minus_fish",
                "p_value_family_presence",
                "p_value_family_presence_holm",
            ]
            f.write(df_csv[summary_cols].to_markdown(index=False))
            f.write("\n\n")

            sig_holm = df_csv[df_csv["p_value_holm"] < ALPHA]
            if not sig_holm.empty:
                f.write("**Holm-signifikant (p < 0.05):**\n")
                for _, row in sig_holm.iterrows():
                    f.write(f"- {row['site']}: p = {row['p_value_holm']:.4f}\n")
            else:
                f.write("**Kein Standort bleibt nach Holm-Korrektur signifikant.**\n")

            if "p_value_maxn_sum_holm" in df_csv.columns:
                sig_maxn = df_csv[df_csv["p_value_maxn_sum_holm"] < ALPHA]
                f.write("\n**Holm-signifikant (MaxN-Sensitivitaet, p < 0.05):**\n")
                if not sig_maxn.empty:
                    for _, row in sig_maxn.iterrows():
                        f.write(f"- {row['site']}: p = {row['p_value_maxn_sum_holm']:.4f}\n")
                else:
                    f.write("- Kein Standort.\n")

            if "p_value_family_presence_holm" in df_csv.columns:
                sig_presence = df_csv[df_csv["p_value_family_presence_holm"] < ALPHA]
                f.write("\n**Holm-signifikant (Family-Presence-Sensitivitaet, p < 0.05):**\n")
                if not sig_presence.empty:
                    for _, row in sig_presence.iterrows():
                        f.write(f"- {row['site']}: p = {row['p_value_family_presence_holm']:.4f}\n")
                else:
                    f.write("- Kein Standort.\n")

    df_csv.to_csv(csv_path, index=False)
    print(f"Wrote {md_path}")
    print(f"Wrote {csv_path}")


def main():
    all_results = {}

    for site in SITES:
        print(f"\n=== {site.upper()} ===")
        result = analyze_site(site)
        if isinstance(result["results"], dict) and result["results"].get("site"):
            print(f"Algae Videos: {result['results']['algae_videos']}")
            print(f"Fish Videos: {result['results']['fish_videos']}")
            print(f"Algae Feeding Rate: {result['results']['algae_feeding_rate_mean']:.4f}")
            print(f"Fish Feeding Rate: {result['results']['fish_feeding_rate_mean']:.4f}")
            print(f"p-value: {result['results']['p_value']:.6f}")
            all_results[site] = result
        else:
            print(f"Keine Daten für {site}.")

    write_report(all_results)
    print(f"\n✓ Herbivore Feeding Analyse abgeschlossen. Ergebnisse in {OUT_DIR}")


if __name__ == "__main__":
    main()
