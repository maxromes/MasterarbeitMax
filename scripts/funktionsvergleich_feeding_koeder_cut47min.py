#!/usr/bin/env python3
"""
Funktioneller Koedervergleich mit FEEDING-Filter (cut_47min).

Unterschied zum Standard-Funktionsvergleich:
- Dieser Test inkludiert NUR Annotations-Einträge mit feeding=true
- MaxN wird nicht verwendet; stattdessen wird gezählt, wie oft eine Gruppe feeding zeigt
- Sinnvoll für: "Welche Funktionsgruppen fressen signifikant unterschiedlich je Köder?"

Ziel:
- Nutzt die Ernaehrungsinformationen aus der Word-Tabelle
- Testet getrennt je Standort, welche Gruppen sich je Koeder unterscheiden
- ABER: Nur counting Feeding-Events, nicht MaxN

Statistik:
- Global je Gruppe: Kruskal-Wallis ueber Koeder.
- Pairweise je Gruppe: Mann-Whitney U zwischen Koedern.
- Extra: Fish-baits vs Algae-baits (Mann-Whitney U).
- Mehrfachtest-Korrektur: Holm und Benjamini-Hochberg (FDR/BH).

Ausgabe:
- results/funktionsvergleich_feeding/<site>/*.csv
- results/funktionsvergleich_feeding/funktionsvergleich_feeding_bericht.md
"""

from __future__ import annotations

import itertools
import math
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min" / "Annotation_reports_coral_reef"
NURSERY_CUT_ROOT = ROOT / "normalized_reports" / "cut_47min" / "Annotation_reports_Nursery"
OUT_DIR = ROOT / "results" / "funktionsvergleich_feeding"

TARGET_SITES = ["milimani", "utumbi", "nursery"]
ALPHA = 0.05

# Koeder-Typen
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

# Word-basiertes Mapping: Gruppe -> Diet-Labels
WORD_GROUP_DIETS: Dict[str, List[str]] = {
    "blennies": ["algae"],
    "rabbitfishes": ["algae"],
    "surgeonfishes": ["algae"],
    "parrotfishes": ["algae"],
    "wrasses": ["invertebrates", "plankton"],
    "eels": ["fish"],
    "groupers_large": ["fish"],
    "snappers": ["fish", "invertebrates"],
    "triggerfishes": ["invertebrates"],
}

# Familie -> Word-Gruppe
FAMILY_TO_WORD_GROUP = {
    "blenniidae": "blennies",
    "siganidae": "rabbitfishes",
    "acanthuridae": "surgeonfishes",
    "scaridae": "parrotfishes",
    "labridae": "wrasses",
    "muraenidae": "eels",
    "serranidae": "groupers_large",
    "lutjanidae": "snappers",
    "balistidae": "triggerfishes",
}

# Zusammengesetzte Gruppen
COMPOSITE_GROUP_RULES: Dict[str, Dict[str, object]] = {
    "herbivore_core_families": {
        "description": "Kern-Herbivore (Familien): Siganidae, Acanthuridae, Scaridae, Blenniidae",
        "families": ["siganidae", "acanthuridae", "scaridae", "blenniidae"],
    },
    "herbivore_extended_with_damselfishes": {
        "description": "Erweiterte Herbivore: rabbitfishes/surgeonfishes/parrotfishes/blennies + small_ovals_damselfishes",
        "word_groups": ["rabbitfishes", "surgeonfishes", "parrotfishes", "blennies"],
    },
    "piscivore_core_families": {
        "description": "Kern-Piscivore (Familien): Serranidae, Lutjanidae, Muraenidae",
        "families": ["serranidae", "lutjanidae", "muraenidae"],
    },
    "invertivore_general": {
        "description": "Breite Invertivore: triggerfishes, wrasses",
        "word_groups": ["triggerfishes", "wrasses"],
    },
    "algae_oriented_diet_mode": {
        "description": "Alle Taxa mit Algenbezug",
        "diets": ["algae"],
    },
    "fish_oriented_diet_mode": {
        "description": "Alle Taxa mit Fischbezug",
        "diets": ["fish"],
    },
    "invertebrate_oriented_diet_mode": {
        "description": "Alle Taxa mit Wirbellosenbezug",
        "diets": ["invertebrates"],
    },
}


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


def parse_word_group_from_row(row: pd.Series) -> str | None:
    family = clean_text(row.get("family", "")).lower()
    if family in FAMILY_TO_WORD_GROUP:
        return FAMILY_TO_WORD_GROUP[family]
    return None


def get_composite_groups(family: str, word_group: str | None, diets: List[str]) -> List[str]:
    hits: List[str] = []
    diet_set = set(diets)

    for name, rule in COMPOSITE_GROUP_RULES.items():
        families = set(rule.get("families", []))
        word_groups = set(rule.get("word_groups", []))
        rule_diets = set(rule.get("diets", []))

        matched = False
        if family and family in families:
            matched = True
        if word_group and word_group in word_groups:
            matched = True
        if rule_diets and (diet_set & rule_diets):
            matched = True

        if matched:
            hits.append(name)

    return hits


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


def bh_adjust(p_values: List[float]) -> List[float]:
    m = len(p_values)
    if m == 0:
        return []
    order = np.argsort(p_values)
    adjusted_ordered = np.zeros(m)
    for i, idx in enumerate(order, start=1):
        adjusted_ordered[i - 1] = p_values[idx] * m / i
    for i in range(m - 2, -1, -1):
        adjusted_ordered[i] = min(adjusted_ordered[i], adjusted_ordered[i + 1])
    adjusted_ordered = np.clip(adjusted_ordered, 0.0, 1.0)
    adjusted = np.zeros(m)
    for i, idx in enumerate(order):
        adjusted[idx] = adjusted_ordered[i]
    return adjusted.tolist()


def cliffs_delta(x: np.ndarray, y: np.ndarray) -> float:
    total = len(x) * len(y)
    if total == 0:
        return math.nan
    gt = sum(1 for xi in x for yi in y if xi > yi)
    lt = sum(1 for xi in x for yi in y if xi < yi)
    return float((gt - lt) / total)


def load_video_features_feeding(csv_path: Path) -> Dict[str, object]:
    """
    Lade Feeding-Daten: zähle pro Gruppe/Familie wie oft feeding=true.
    """
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")

    # Zähle Feeding-Events pro Gruppe
    feeding_counts: Dict[str, int] = {}

    for _, row in df.iterrows():
        # Nur Zeilen mit feeding=true
        if not is_truthy(row.get("feeding", "")):
            continue

        family = clean_text(row.get("family", "")).lower()
        word_group = parse_word_group_from_row(row)

        # Word-Gruppe
        if word_group:
            key = f"word_group::{word_group}"
            feeding_counts[key] = feeding_counts.get(key, 0) + 1

        # Familie
        if family:
            key = f"family::{family}"
            feeding_counts[key] = feeding_counts.get(key, 0) + 1

        # Diets
        diets = []
        for diet_label in ["algae", "fish", "invertebrates", "plankton"]:
            if clean_text(row.get(diet_label, "")).lower() == "yes":
                diets.append(diet_label)
        for diet in diets:
            key = f"diet::{diet}"
            feeding_counts[key] = feeding_counts.get(key, 0) + 1

        # Composite Groups
        composite_hits = get_composite_groups(family, word_group, diets)
        for comp in composite_hits:
            key = f"composite::{comp}"
            feeding_counts[key] = feeding_counts.get(key, 0) + 1

    date, standort, koeder = parse_video_metadata(csv_path.name)
    return {
        "filename": csv_path.name,
        "date": date,
        "standort": standort,
        "koeder": koeder,
        "feeding_counts": feeding_counts,
    }


def load_all_videos_feeding(site: str) -> pd.DataFrame:
    """Lade Videos mit Feeding-Daten."""
    if site == "nursery":
        video_dir = NURSERY_CUT_ROOT
    else:
        video_dir = CUT_ROOT

    if not video_dir.exists():
        return pd.DataFrame()

    video_files = sorted([f for f in video_dir.glob("*.csv") if "-" in f.name])
    data = []

    for csv_file in video_files:
        _, standort, koeder = parse_video_metadata(csv_file.name)
        if standort.lower() == site.lower():
            meta = load_video_features_feeding(csv_file)
            if meta["feeding_counts"]:
                data.append(meta)

    return pd.DataFrame(data)


def analyze_site_feeding(site: str) -> Dict[str, pd.DataFrame]:
    """Analysiere Feeding für einen Standort."""
    videos = load_all_videos_feeding(site)
    if videos.empty:
        return {}

    bait_order = sorted(videos["koeder"].unique().tolist())
    site_videos = {b: videos[videos["koeder"] == b].copy() for b in bait_order}

    # Alle Gruppen
    all_groups = set()
    for counts_dict in videos["feeding_counts"]:
        all_groups.update(counts_dict.keys())
    all_groups = sorted(all_groups)

    results_rows: List[Dict[str, object]] = []
    fish_vs_algae_rows: List[Dict[str, object]] = []

    for group in all_groups:
        bait_arrays: Dict[str, np.ndarray] = {}
        for bait in bait_order:
            vals = np.array(
                [float(v.feeding_counts.get(group, 0)) for v in site_videos[bait].itertuples(index=False)],
                dtype=float,
            )
            bait_arrays[bait] = vals

        groups = [bait_arrays[b] for b in bait_order]

        # Kruskal-Wallis Global Test
        if len(groups) > 1 and sum(len(g) for g in groups) > 0:
            kw_stat, kw_pval = stats.kruskal(*groups)
        else:
            kw_stat, kw_pval = math.nan, math.nan

        results_rows.append(
            {
                "site": site,
                "group": group,
                "n_baits": len(bait_order),
                "kw_p_value": kw_pval,
            }
        )

        # Fish vs Algae
        algae_baits = [b for b in bait_order if BAIT_TYPE.get(b) == "algae"]
        fish_baits = [b for b in bait_order if BAIT_TYPE.get(b) == "fish"]

        if algae_baits and fish_baits:
            algae_vals = np.concatenate([bait_arrays[b] for b in algae_baits])
            fish_vals = np.concatenate([bait_arrays[b] for b in fish_baits])

            if len(algae_vals) > 0 and len(fish_vals) > 0:
                stat_mw, pval_mw = stats.mannwhitneyu(algae_vals, fish_vals, alternative="two-sided")
                cliff_d = cliffs_delta(algae_vals, fish_vals)
                higher_side = "algae" if np.median(algae_vals) > np.median(fish_vals) else "fish"
            else:
                pval_mw = math.nan
                cliff_d = math.nan
                higher_side = "n/a"

            fish_vs_algae_rows.append(
                {
                    "site": site,
                    "group": group,
                    "algae_median_feeding": float(np.median(algae_vals)) if len(algae_vals) > 0 else 0.0,
                    "fish_median_feeding": float(np.median(fish_vals)) if len(fish_vals) > 0 else 0.0,
                    "p_value": pval_mw,
                    "cliffs_delta": cliff_d,
                    "higher_side": higher_side,
                }
            )

    df_results = pd.DataFrame(results_rows)
    df_fva = pd.DataFrame(fish_vs_algae_rows)

    # Holm-Korrektur
    if not df_fva.empty:
        p_vals = df_fva["p_value"].fillna(1.0).tolist()
        holm_adj = holm_adjust(p_vals)
        bh_adj = bh_adjust(p_vals)
        df_fva["p_value_holm"] = holm_adj
        df_fva["p_value_bh"] = bh_adj

    return {"global": df_results, "fish_vs_algae": df_fva}


def write_summary_report(all_results: Dict[str, Dict[str, pd.DataFrame]]) -> None:
    """Schreibe Gesamtbericht."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    md_path = OUT_DIR / "funktionsvergleich_feeding_bericht.md"

    with open(md_path, "w") as f:
        f.write("# Funktionsvergleich mit Feeding-Filter\n\n")
        f.write("Testet Koederverschiedenheiten basierend auf **Feeding-Events** (nicht MaxN).\n\n")
        f.write("**Methode**: Pro Standort und Gruppe wird gezählt, wie oft diese Gruppe feeding=true zeigt je Köder.\n")
        f.write("Mann-Whitney U Test (gerichtet) für Fish-vs-Algae Vergleich.\n\n")

        f.write("## Fish-vs-Algae Ergebnisse\n\n")

        for site in TARGET_SITES:
            if site not in all_results or all_results[site]["fish_vs_algae"].empty:
                f.write(f"### {site.capitalize()}\nKeine Daten.\n\n")
                continue

            f.write(f"### {site.capitalize()}\n\n")
            df = all_results[site]["fish_vs_algae"]

            sig_holm = df[df["p_value_holm"] < ALPHA]
            sig_bh = df[df["p_value_bh"] < ALPHA]

            f.write(f"**Signifikanz-Übersicht**: Holm-sig: {len(sig_holm)}, BH-sig: {len(sig_bh)}\n\n")

            if not sig_holm.empty:
                f.write("**Holm-signifikante Gruppen (p < 0.05):**\n\n")
                for _, row in sig_holm.iterrows():
                    f.write(
                        f"- **{row['group']}**: Algae-Median = {row['algae_median_feeding']:.1f}, "
                        f"Fish-Median = {row['fish_median_feeding']:.1f}, "
                        f"Higher: {row['higher_side']}, p = {row['p_value_holm']:.4f}, "
                        f"Cliffs Δ = {row['cliffs_delta']:.4f}\n"
                    )
                f.write("\n")

            f.write("**Top explorative Signale (sortiert nach p-Wert, Holm-korrigiert):**\n\n")
            df_sorted = df.sort_values("p_value_holm").head(10)
            for _, row in df_sorted.iterrows():
                f.write(
                    f"- {row['group']}: Algae={row['algae_median_feeding']:.1f}, Fish={row['fish_median_feeding']:.1f}, "
                    f"p_holm={row['p_value_holm']:.4f}, Δ={row['cliffs_delta']:.4f}\n"
                )
            f.write("\n")

    print(f"Wrote {md_path}")


def main():
    all_results = {}

    for site in TARGET_SITES:
        print(f"\n=== Analysiere {site.upper()} ===")
        result = analyze_site_feeding(site)

        if result and not result["fish_vs_algae"].empty:
            df_fva = result["fish_vs_algae"]
            sig_holm = df_fva[df_fva["p_value_holm"] < ALPHA]
            print(f"Getestete Gruppen: {len(df_fva)}")
            print(f"Holm-signifikant: {len(sig_holm)}")

            # Speichern
            site_dir = OUT_DIR / site
            site_dir.mkdir(parents=True, exist_ok=True)
            result["fish_vs_algae"].to_csv(site_dir / "fish_vs_algae_feeding.csv", index=False)
            print(f"Wrote {site_dir / 'fish_vs_algae_feeding.csv'}")

            all_results[site] = result
        else:
            print(f"Keine Daten für {site}.")

    write_summary_report(all_results)
    print(f"\n✓ Funktionsvergleich mit Feeding-Filter abgeschlossen. Ergebnisse in {OUT_DIR}")


if __name__ == "__main__":
    main()
