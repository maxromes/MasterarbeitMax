#!/usr/bin/env python3
"""
Algae-Responsiveness Ranking: Finde Taxa mit signifikant oder praktisch höherer
Präsenz bei Algenködern vs. Fischködern (Reverse-Fokus zum Funktionsvergleich).

Ziele:
- Pro Standort vergleiche Algen vs Fisch bezüglich Häufigkeit (MaxN) je Taxon.
- Filtere auf Taxa mit ALGAE-Vorteil (algae_median > fish_median).
- Führe Mann-Whitney U Tests durch für diese gefilterten Taxa.
- Sortiere nach Cliffs Delta (Algae - Fish).
- Hebe Herbivore-Familien hervor.

Ausgabe:
- results/algae_responsiveness/
  - <site>_algae_responsive_taxa.csv
  - <site>_algae_responsive_taxa.md
  - algae_responsiveness_summary.md
  - figures (optional: Visualisierungen)
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Dict, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parent.parent
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min"
CORAL_REEF_DIR = CUT_ROOT / "Annotation_reports_coral_reef"
NURSERY_DIR = CUT_ROOT / "Annotation_reports_Nursery"

OUT_DIR = ROOT / "results" / "algae_responsiveness"
FIG_DIR = OUT_DIR / "figures"

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

# Familie -> Word-Gruppe für Identifizierung
FAMILY_TO_WORD_GROUP = {
    "siganidae": "rabbitfishes",
    "acanthuridae": "surgeonfishes",
    "scaridae": "parrotfishes",
    "blenniidae": "blennies",
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


def extract_family(taxon_key: str) -> str:
    """Extrahiere Familie aus taxon_key."""
    # Format: family::xyz oder family_label::xyz
    if "::" in taxon_key:
        parts = taxon_key.split("::")
        if parts[0] in {"family", "family_label"}:
            return parts[1].lower()
    return ""


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


def load_video_maxn(csv_path: Path) -> Dict[str, object]:
    """Lade MaxN-Daten aus CSV."""
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")

    counts: Dict[Tuple[str, float], int] = {}
    for _, row in df.iterrows():
        if is_truthy(row.get("feeding", "")) or is_truthy(row.get("interested", "")):
            continue

        taxon = build_taxon_key(row)
        if not taxon:
            continue

        frame_time = parse_frame_time(row.get("frames", ""))
        if frame_time is None:
            continue

        key = (taxon, frame_time)
        counts[key] = counts.get(key, 0) + 1

    maxn_by_taxon: Dict[str, int] = {}
    for (taxon, _), n in counts.items():
        if taxon not in maxn_by_taxon or n > maxn_by_taxon[taxon]:
            maxn_by_taxon[taxon] = int(n)

    date, standort, koeder = parse_video_metadata(csv_path.name)
    return {
        "filename": csv_path.name,
        "date": date,
        "standort": standort,
        "koeder": koeder,
        "maxn_by_taxon": maxn_by_taxon,
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
    """Berechne Cliffs Delta für x vs y."""
    total = len(x) * len(y)
    if total == 0:
        return math.nan
    gt = 0
    lt = 0
    for xi in x:
        gt += np.sum(xi > y)
        lt += np.sum(xi < y)
    return float((gt - lt) / total)


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
            meta = load_video_maxn(csv_file)
            if meta["maxn_by_taxon"]:
                video_data.append(meta)

    df = pd.DataFrame(video_data)
    return df


def analyze_site(site: str) -> Dict[str, pd.DataFrame]:
    """Analysiere Algae-Responsiveness für einen Standort."""
    videos = load_all_videos(site)
    if videos.empty:
        return {"algae_responsive": pd.DataFrame()}

    # Gruppiere nach Ködertyp
    algae_baits = [bait for bait, typ in BAIT_TYPE.items() if typ == "algae"]
    fish_baits = [bait for bait, typ in BAIT_TYPE.items() if typ == "fish"]

    algae_videos = videos[videos["koeder"].isin(algae_baits)]
    fish_videos = videos[videos["koeder"].isin(fish_baits)]

    if algae_videos.empty or fish_videos.empty:
        return {"algae_responsive": pd.DataFrame()}

    # Sammle alle Taxa
    all_taxa = set()
    for maxn_dict in videos["maxn_by_taxon"]:
        all_taxa.update(maxn_dict.keys())
    all_taxa = sorted(all_taxa)

    results: List[Dict[str, object]] = []

    for taxon in all_taxa:
        # MaxN-Werte sammeln
        algae_vals = np.array(
            [float(v.get(taxon, 0)) for v in algae_videos["maxn_by_taxon"].values],
            dtype=float,
        )
        fish_vals = np.array(
            [float(v.get(taxon, 0)) for v in fish_videos["maxn_by_taxon"].values],
            dtype=float,
        )

        # Statistiken
        algae_median = float(np.median(algae_vals))
        fish_median = float(np.median(fish_vals))
        algae_mean = float(np.mean(algae_vals))
        fish_mean = float(np.mean(fish_vals))

        # Filter: Nur Taxa mit Algen-Vorteil behalten
        if algae_median <= fish_median:
            continue

        # Mann-Whitney U Test
        if len(algae_vals) > 0 and len(fish_vals) > 0:
            stat, pval = stats.mannwhitneyu(algae_vals, fish_vals, alternative="greater")
            cliff_d = cliffs_delta(algae_vals, fish_vals)
        else:
            pval = math.nan
            cliff_d = math.nan

        # Familie und Herbivore-Status
        family = extract_family(taxon)
        is_herbivore = family.lower() in HERBIVORE_CORE_FAMILIES

        results.append(
            {
                "taxon": taxon,
                "family": family,
                "is_herbivore": is_herbivore,
                "algae_n_videos": int(len(algae_vals)),
                "fish_n_videos": int(len(fish_vals)),
                "algae_median": algae_median,
                "fish_median": fish_median,
                "algae_mean": algae_mean,
                "fish_mean": fish_mean,
                "median_diff_algae_minus_fish": algae_median - fish_median,
                "mean_diff_algae_minus_fish": algae_mean - fish_mean,
                "p_value": pval,
                "cliffs_delta_algae_minus_fish": cliff_d,
            }
        )

    df = pd.DataFrame(results)

    # Holm-Korrektur
    if not df.empty:
        p_vals = df["p_value"].fillna(1.0).values.tolist()
        holm_adjusted = holm_adjust(p_vals)
        bh_adjusted = bh_adjust(p_vals)
        df["p_value_holm"] = holm_adjusted
        df["p_value_bh"] = bh_adjusted

        # Sortiere nach Cliffs Delta (absteigend)
        df = df.sort_values("cliffs_delta_algae_minus_fish", ascending=False)

    return {"algae_responsive": df}


def write_site_report(site: str, df: pd.DataFrame) -> None:
    """Schreibe Markdown-Bericht für einen Standort."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Signifikante Taxa (Holm)
    sig_holm = df[df["p_value_holm"] < ALPHA]
    sig_bh = df[df["p_value_bh"] < ALPHA]

    md_path = OUT_DIR / f"{site}_algae_responsive_taxa.md"
    csv_path = OUT_DIR / f"{site}_algae_responsive_taxa.csv"

    with open(md_path, "w") as f:
        f.write(f"# Algae-Responsive Taxa: {site.capitalize()}\n\n")
        f.write(f"Datengrundlage: {len(df)} Taxa mit Algen-Median > Fisch-Median\n\n")
        f.write(
            f"**Signifikant (Holm): {len(sig_holm)} | Signifikant (BH): {len(sig_bh)}**\n\n"
        )

        if not sig_holm.empty:
            f.write("## Robust signifikante Taxa (Holm-korrigiert, p < 0.05)\n\n")
            sig_holm_display = sig_holm[
                [
                    "taxon",
                    "family",
                    "is_herbivore",
                    "algae_median",
                    "fish_median",
                    "median_diff_algae_minus_fish",
                    "cliffs_delta_algae_minus_fish",
                    "p_value",
                    "p_value_holm",
                ]
            ].copy()
            f.write(sig_holm_display.to_markdown(index=False))
            f.write("\n\n")
        else:
            f.write("## Robust signifikante Taxa (Holm-korrigiert)\nKeine.\n\n")

        if not sig_bh.empty:
            f.write("## Signifikante Taxa (BH/FDR-korrigiert, q < 0.05)\n\n")
            sig_bh_display = sig_bh[
                [
                    "taxon",
                    "family",
                    "is_herbivore",
                    "algae_median",
                    "fish_median",
                    "median_diff_algae_minus_fish",
                    "cliffs_delta_algae_minus_fish",
                    "p_value_bh",
                ]
            ].copy()
            f.write(sig_bh_display.to_markdown(index=False))
            f.write("\n\n")

        f.write("## Top Taxa nach Cliffs Delta (Algae - Fish) [explorative Rangordnung]\n\n")
        top_display = df.head(20)[
            [
                "taxon",
                "family",
                "is_herbivore",
                "algae_median",
                "fish_median",
                "cliffs_delta_algae_minus_fish",
                "p_value",
            ]
        ].copy()
        f.write(top_display.to_markdown(index=False))
        f.write("\n\n")

        f.write("## Herbivore-Status Verteilung\n\n")
        herbivore_counts = df["is_herbivore"].value_counts()
        f.write(f"- Herbivore (Siganidae, Acanthuridae, Scaridae, Blenniidae): {herbivore_counts.get(True, 0)}\n")
        f.write(
            f"- Andere Taxa: {herbivore_counts.get(False, 0)}\n\n"
        )

        if (df["is_herbivore"]).any():
            f.write("### Herbivore unter den algae-responsive Taxa\n\n")
            herbivores = df[df["is_herbivore"]][
                [
                    "taxon",
                    "family",
                    "algae_median",
                    "fish_median",
                    "cliffs_delta_algae_minus_fish",
                    "p_value_holm",
                ]
            ].copy()
            f.write(herbivores.to_markdown(index=False))
            f.write("\n\n")

    # CSV speichern
    df.to_csv(csv_path, index=False)
    print(f"Wrote {csv_path}")
    print(f"Wrote {md_path}")


def write_summary_report(results: Dict[str, Dict[str, pd.DataFrame]]) -> None:
    """Schreibe Gesamtbericht über alle Standorte."""
    md_path = OUT_DIR / "algae_responsiveness_summary.md"

    with open(md_path, "w") as f:
        f.write("# Algae-Responsiveness Ranking: Gesamtbericht\n\n")
        f.write("Vergleich von Algae-Ködern vs. Fisch-Ködern für alle Taxa.\n\n")

        for site in SITES:
            if site not in results or results[site]["algae_responsive"].empty:
                f.write(f"## {site.capitalize()}\nKeine Daten vorhanden.\n\n")
                continue

            df = results[site]["algae_responsive"]
            sig_holm = df[df["p_value_holm"] < ALPHA]
            sig_bh = df[df["p_value_bh"] < ALPHA]
            herbivores = df[df["is_herbivore"]]

            f.write(f"## {site.capitalize()}\n\n")
            f.write(f"- **Taxa mit Algen-Vorteil (Algae-Median > Fisch-Median)**: {len(df)}\n")
            f.write(f"- **Holm-signifikant (p < 0.05)**: {len(sig_holm)}\n")
            f.write(f"- **BH-signifikant (q < 0.05)**: {len(sig_bh)}\n")
            f.write(f"- **Herbivore (Siganidae, Acanthuridae, Scaridae, Blenniidae)**: {len(herbivores)}\n\n")

            if not sig_holm.empty:
                f.write(f"### Holm-signifikante Taxa\n\n")
                for _, row in sig_holm.iterrows():
                    herbivore_tag = " [HERBIVORE]" if row["is_herbivore"] else ""
                    f.write(
                        f"- **{row['taxon']}**{herbivore_tag}: Cliffs Δ = {row['cliffs_delta_algae_minus_fish']:.3f}, "
                        f"p={row['p_value_holm']:.4f}, Algae-Med={row['algae_median']:.1f}, "
                        f"Fish-Med={row['fish_median']:.1f}\n"
                    )
                f.write("\n")

            if not herbivores.empty:
                f.write(f"### Herbivore (Top 10 nach Cliffs Delta)\n\n")
                for _, row in herbivores.head(10).iterrows():
                    sig_marker = " *" if row["p_value_holm"] < ALPHA else ""
                    f.write(
                        f"- **{row['taxon']}**{sig_marker}: Cliffs Δ = {row['cliffs_delta_algae_minus_fish']:.3f}, "
                        f"p={row['p_value']:.4f}, Algae-Med={row['algae_median']:.1f}\n"
                    )
                f.write("\n")

    print(f"Wrote {md_path}")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    results: Dict[str, Dict[str, pd.DataFrame]] = {}

    for site in SITES:
        print(f"\n=== Analysiere {site.upper()} ===")
        site_results = analyze_site(site)

        if not site_results["algae_responsive"].empty:
            df = site_results["algae_responsive"]
            print(f"Taxa mit Algen-Vorteil: {len(df)}")
            print(f"Holm-signifikant: {len(df[df['p_value_holm'] < ALPHA])}")
            print(f"BH-signifikant: {len(df[df['p_value_bh'] < ALPHA])}")
            print(f"Davon Herbivore: {len(df[df['is_herbivore']])}")

            write_site_report(site, df)
            results[site] = site_results
        else:
            print(f"Keine Daten für {site}.")

    write_summary_report(results)
    print(f"\n✓ Analyse abgeschlossen. Ergebnisse in {OUT_DIR}")


if __name__ == "__main__":
    main()
