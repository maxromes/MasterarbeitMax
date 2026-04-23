#!/usr/bin/env python3
"""
Funktioneller Koedervergleich (cut_47min) fuer Milimani und Utumbi.

Ziel:
- Nutzt die Ernaehrungs-Informationen aus der Word-Tabelle
  BRUV_Algae_vs_Fish_Bait_Thesis_Template.docx.
- Testet getrennt je Standort, welche Gruppen sich je Koeder unterscheiden.
- Probiert mehrere Gruppierungen:
  1) Word-Gruppen (z. B. Wrasses, Groupers)
  2) Ernaehrungsmodi (algae/fish/invertebrates/plankton/omnivore)
  3) Familien
  4) Genus
  5) Unspezifische Gruppen

Statistik:
- Global je Gruppe: Kruskal-Wallis ueber Koeder.
- Paarweise je Gruppe: Mann-Whitney U zwischen Koedern.
- Extra: Fish-baits vs Algae-baits (Mann-Whitney U).
- Mehrfachtest-Korrektur: Holm und Benjamini-Hochberg (FDR/BH).

Ausgabe:
- results/funktionsvergleich/<site>/*.csv
- results/funktionsvergleich/funktionsvergleich_bericht.md
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
OUT_DIR = ROOT / "results" / "funktionsvergleich"

TARGET_SITES = ["milimani", "utumbi"]
ALPHA = 0.05

# Koeder-Typen fuer die gezielte Fish-vs-Algae-Analyse
BAIT_TYPE = {
    "mackerel": "fish",
    "fischmix": "fish",
    "sargassum": "algae",
    "ulva_salad": "algae",
    "ulva_gutweed": "algae",
    "control": "control",
}

# Word-basiertes Mapping: Gruppe -> Diet-Labels
WORD_GROUP_DIETS: Dict[str, List[str]] = {
    "blennies": ["algae"],
    "cardinalfishes": ["plankton"],
    "cephalopoda": ["fish", "invertebrates"],
    "angelfishes": ["invertebrates", "algae"],
    "batfishes": ["omnivore"],
    "butterflyfishes": ["invertebrates", "fish"],
    "eels": ["fish"],
    "elongate_sand_burrow_dwellers": ["invertebrates"],
    "gobies": ["algae", "plankton", "invertebrates"],
    "groupers_large": ["fish"],
    "hawkfishes": ["invertebrates"],
    "sweetlips": ["invertebrates"],
    "moorish_idol": ["invertebrates"],
    "rabbitfishes": ["algae"],
    "surgeonfishes": ["algae"],
    "frogfishes": ["fish"],
    "scorpion_lionfishes": ["fish", "invertebrates"],
    "stonefishes": ["fish"],
    "boxfishes": ["omnivore"],
    "cornetfishes": ["fish"],
    "filefishes": ["algae", "invertebrates"],
    "goatfishes": ["invertebrates"],
    "porcupinefishes": ["invertebrates"],
    "puffers": ["invertebrates", "algae"],
    "sweepers": ["plankton"],
    "triggerfishes": ["invertebrates"],
    "trumpetfishes": ["fish"],
    "parrotfishes": ["algae"],
    "pipefishes_seahorses": ["plankton"],
    "bigeyes": ["fish", "invertebrates"],
    "soldier_squirrelfishes": ["invertebrates"],
    "sharks_rays": ["fish", "invertebrates"],
    "barracudas": ["fish"],
    "jacks_trevallies": ["fish"],
    "tunas_mackerels": ["fish"],
    "anthias": ["plankton"],
    "fusiliers": ["plankton"],
    "coral_breams": ["invertebrates"],
    "emperors": ["invertebrates", "fish"],
    "snappers": ["fish", "invertebrates"],
    "small_ovals_damselfishes": ["algae", "plankton"],
    "stomatapoda": ["fish", "invertebrates"],
    "turtles": ["algae", "invertebrates"],
    "wrasses": ["invertebrates", "plankton"],
}

# Familie -> Word-Gruppe
FAMILY_TO_WORD_GROUP = {
    "blenniidae": "blennies",
    "apogonidae": "cardinalfishes",
    "pomacanthidae": "angelfishes",
    "ephippidae": "batfishes",
    "chaetodontidae": "butterflyfishes",
    "muraenidae": "eels",
    "gobiidae": "gobies",
    "serranidae": "groupers_large",
    "cirrhitidae": "hawkfishes",
    "haemulidae": "sweetlips",
    "zanclidae": "moorish_idol",
    "siganidae": "rabbitfishes",
    "acanthuridae": "surgeonfishes",
    "antennariidae": "frogfishes",
    "synanceiidae": "stonefishes",
    "ostraciidae": "boxfishes",
    "fistulariidae": "cornetfishes",
    "monacanthidae": "filefishes",
    "mullidae": "goatfishes",
    "diodontidae": "porcupinefishes",
    "tetraodontidae": "puffers",
    "pempheridae": "sweepers",
    "balistidae": "triggerfishes",
    "aulostomidae": "trumpetfishes",
    "scaridae": "parrotfishes",
    "priacanthidae": "bigeyes",
    "sphyraenidae": "barracudas",
    "caesionidae": "fusiliers",
    "nemipteridae": "coral_breams",
    "lethrinidae": "emperors",
    "lutjanidae": "snappers",
    "labridae": "wrasses",
}

# Zusaetzliche zusammengesetzte Gruppen fuer erweiterte Tests.
# Regeln werden ueber Familien, Word-Gruppen, Unspecific-Labels und Diet-Labels gematcht.
COMPOSITE_GROUP_RULES: Dict[str, Dict[str, object]] = {
    "herbivore_core_families": {
        "description": "Kern-Herbivore (Familien): Siganidae, Acanthuridae, Scaridae, Blenniidae",
        "families": ["siganidae", "acanthuridae", "scaridae", "blenniidae"],
    },
    "herbivore_extended_with_damselfishes": {
        "description": "Erweiterte Herbivore: rabbitfishes/surgeonfishes/parrotfishes/blennies + small_ovals_damselfishes",
        "word_groups": [
            "rabbitfishes",
            "surgeonfishes",
            "parrotfishes",
            "blennies",
            "small_ovals_damselfishes",
        ],
    },
    "piscivore_core_families": {
        "description": "Kern-Piscivore (Familien): Serranidae, Lutjanidae, Muraenidae, Sphyraenidae, Aulostomidae, Fistulariidae",
        "families": ["serranidae", "lutjanidae", "muraenidae", "sphyraenidae", "aulostomidae", "fistulariidae"],
    },
    "piscivore_active_hunters": {
        "description": "Aktive/ambush Fischjaeger: groupers_large, eels, snappers, barracudas, trumpetfishes, cornetfishes, jacks_trevallies",
        "word_groups": [
            "groupers_large",
            "eels",
            "snappers",
            "barracudas",
            "trumpetfishes",
            "cornetfishes",
            "jacks_trevallies",
        ],
    },
    "invertivore_benthic_core": {
        "description": "Benthos-Invertivore: Mullidae, Haemulidae, Balistidae, Diodontidae, Nemipteridae, Lethrinidae",
        "families": ["mullidae", "haemulidae", "balistidae", "diodontidae", "nemipteridae", "lethrinidae"],
    },
    "invertivore_general": {
        "description": "Breite Invertivore (Word): goatfishes, sweetlips, triggerfishes, porcupinefishes, coral_breams, emperors, hawkfishes",
        "word_groups": [
            "goatfishes",
            "sweetlips",
            "triggerfishes",
            "porcupinefishes",
            "coral_breams",
            "emperors",
            "hawkfishes",
        ],
    },
    "planktivore_core": {
        "description": "Planktivore Kernfamilien: Apogonidae, Caesionidae, Pempheridae (+ Anthias als Word-Gruppe)",
        "families": ["apogonidae", "caesionidae", "pempheridae"],
        "word_groups": ["anthias"],
    },
    "wrasses_trigger_combo": {
        "description": "Kombination Labridae + Balistidae (Wrasses + Triggerfishes)",
        "families": ["labridae", "balistidae"],
    },
    "snappers_groupers_combo": {
        "description": "Kombination Lutjanidae + Serranidae (Snappers + Groupers)",
        "families": ["lutjanidae", "serranidae"],
    },
    "predator_reef_core": {
        "description": "Riff-Praedatoren (familienbasiert): Lutjanidae, Serranidae, Muraenidae, Sphyraenidae, Synanceiidae, Antennariidae",
        "families": ["lutjanidae", "serranidae", "muraenidae", "sphyraenidae", "synanceiidae", "antennariidae"],
    },
    "bioeroder_set": {
        "description": "Bioeroder/Hard-substrate feeder: Scaridae + Balistidae",
        "families": ["scaridae", "balistidae"],
    },
    "omnivore_box_puffer_file": {
        "description": "Omnivore/Tendenz-gemischt: Ostraciidae, Tetraodontidae, Monacanthidae",
        "families": ["ostraciidae", "tetraodontidae", "monacanthidae"],
    },
    "nocturnal_predator_mixture": {
        "description": "Nachtaktive Jaeger-Mischung: eels, snappers, bigeyes, soldier_squirrelfishes",
        "word_groups": ["eels", "snappers", "bigeyes", "soldier_squirrelfishes"],
    },
    "algae_oriented_diet_mode": {
        "description": "Alle Taxa mit Algenbezug gemaess Word-Diet-Mapping",
        "diets": ["algae"],
    },
    "fish_oriented_diet_mode": {
        "description": "Alle Taxa mit Fischbezug gemaess Word-Diet-Mapping",
        "diets": ["fish"],
    },
    "invertebrate_oriented_diet_mode": {
        "description": "Alle Taxa mit Wirbellosenbezug gemaess Word-Diet-Mapping",
        "diets": ["invertebrates"],
    },
    "plankton_oriented_diet_mode": {
        "description": "Alle Taxa mit Planktonbezug gemaess Word-Diet-Mapping",
        "diets": ["plankton"],
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
    return text in {"1", "true", "t", "yes", "y"}


def parse_video_metadata(filename: str) -> Tuple[str, str, str]:
    stem = filename.replace(".csv", "")
    parts = stem.split("-", 2)
    if len(parts) < 3:
        return ("", "unknown", "unknown")
    date, standort, koeder = parts
    return (date, standort.lower(), koeder.lower())


def parse_frame_time(frame_value: object) -> float | None:
    text = clean_text(frame_value)
    if not text:
        return None
    match = re.search(r"[-+]?\d*\.?\d+", text)
    if not match:
        return None
    try:
        return round(float(match.group(0)), 3)
    except ValueError:
        return None


def parse_word_group_from_row(row: pd.Series) -> str | None:
    family = clean_text(row.get("family", "")).lower()
    unspecific = clean_text(row.get("unspecific", "")).lower()
    label = clean_text(row.get("label_name", "")).lower()

    if family in FAMILY_TO_WORD_GROUP:
        grp = FAMILY_TO_WORD_GROUP[family]
        # Serranidae in der Word-Tabelle als zwei Gruppen; hier per Label trennen
        if family == "serranidae" and "anthias" in label:
            return "anthias"
        if family == "serranidae" and "anthias" not in label:
            return "groupers_large"
        return grp

    if "cephalopod" in unspecific or "cephalopod" in label:
        return "cephalopoda"
    if "shark" in unspecific or "ray" in unspecific or "shark" in label or "ray" in label:
        return "sharks_rays"
    if "turtle" in unspecific or "turtle" in label:
        return "turtles"
    if "stomatopod" in unspecific or "stomatopod" in label:
        return "stomatapoda"
    if "small ovals" in unspecific:
        return "small_ovals_damselfishes"
    if "wrasses" in unspecific:
        return "wrasses"
    if "groupers" in unspecific:
        return "groupers_large"
    if "elongate" in unspecific:
        return "elongate_sand_burrow_dwellers"
    if "scorpion" in unspecific or "lion" in unspecific:
        return "scorpion_lionfishes"
    if "pipefishes" in unspecific or "seahorses" in unspecific:
        return "pipefishes_seahorses"
    if "soldier" in unspecific or "squirrel" in unspecific:
        return "soldier_squirrelfishes"
    if "jacks" in unspecific or "trevallies" in unspecific:
        return "jacks_trevallies"
    if "tunas" in unspecific or "mackerels" in unspecific:
        return "tunas_mackerels"

    return None


def get_composite_groups(
    family: str,
    word_group: str | None,
    unspecific: str,
    diets: List[str],
) -> List[str]:
    hits: List[str] = []
    diet_set = set(diets)

    for name, rule in COMPOSITE_GROUP_RULES.items():
        families = set(rule.get("families", []))
        word_groups = set(rule.get("word_groups", []))
        unspecific_contains = rule.get("unspecific_contains", [])
        rule_diets = set(rule.get("diets", []))

        matched = False
        if family and family in families:
            matched = True
        if word_group and word_group in word_groups:
            matched = True
        if any(token in unspecific for token in unspecific_contains):
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
    gt = 0
    lt = 0
    for xi in x:
        gt += np.sum(xi > y)
        lt += np.sum(xi < y)
    return float((gt - lt) / total)


def load_video_features(csv_path: Path) -> Dict[str, object]:
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")

    # count[(feature_type, feature_name, frame_time)] = n
    count_map: Dict[Tuple[str, str, float], int] = {}

    for _, row in df.iterrows():
        if is_truthy(row.get("feeding", "")) or is_truthy(row.get("interested", "")):
            continue

        frame_time = parse_frame_time(row.get("frames", ""))
        if frame_time is None:
            continue

        family = clean_text(row.get("family", "")).lower()
        genus = clean_text(row.get("genus", "")).lower()
        unspecific = clean_text(row.get("unspecific", "")).lower()
        word_group = parse_word_group_from_row(row)

        if family:
            key = ("family", family, frame_time)
            count_map[key] = count_map.get(key, 0) + 1

        if genus:
            key = ("genus", genus, frame_time)
            count_map[key] = count_map.get(key, 0) + 1

        if unspecific:
            key = ("unspecific", unspecific, frame_time)
            count_map[key] = count_map.get(key, 0) + 1

        if word_group:
            key = ("word_group", word_group, frame_time)
            count_map[key] = count_map.get(key, 0) + 1
            diets = WORD_GROUP_DIETS.get(word_group, [])
            for diet in diets:
                dkey = ("diet", diet, frame_time)
                count_map[dkey] = count_map.get(dkey, 0) + 1
        else:
            diets = []

        for comp in get_composite_groups(
            family=family,
            word_group=word_group,
            unspecific=unspecific,
            diets=diets,
        ):
            ckey = ("composite_group", comp, frame_time)
            count_map[ckey] = count_map.get(ckey, 0) + 1

    maxn_by_type: Dict[str, Dict[str, int]] = {}
    for (ftype, fname, _), n in count_map.items():
        d = maxn_by_type.setdefault(ftype, {})
        if fname not in d or n > d[fname]:
            d[fname] = int(n)

    date, site, bait = parse_video_metadata(csv_path.name)
    return {
        "filename": csv_path.name,
        "date": date,
        "site": site,
        "bait": bait,
        "bait_type": BAIT_TYPE.get(bait, "other"),
        "maxn_by_type": maxn_by_type,
    }


def prepare_feature_matrix(videos: pd.DataFrame, feature_type: str, min_present_videos: int, min_baits: int) -> Tuple[List[str], pd.DataFrame]:
    all_features: List[str] = sorted(
        set().union(*videos["maxn_by_type"].map(lambda d: set(d.get(feature_type, {}).keys())).tolist())
    )

    rows: List[Dict[str, object]] = []
    for v in videos.itertuples(index=False):
        base = {
            "filename": v.filename,
            "site": v.site,
            "bait": v.bait,
            "bait_type": v.bait_type,
        }
        fmap = v.maxn_by_type.get(feature_type, {})
        for f in all_features:
            base[f] = float(fmap.get(f, 0))
        rows.append(base)

    mat = pd.DataFrame(rows)
    if mat.empty or not all_features:
        return [], mat

    keep_features: List[str] = []
    for f in all_features:
        present = int((mat[f] > 0).sum())
        baits_with_presence = int(mat.loc[mat[f] > 0, "bait"].nunique())
        if present >= min_present_videos and baits_with_presence >= min_baits:
            keep_features.append(f)

    keep_cols = ["filename", "site", "bait", "bait_type"] + keep_features
    return keep_features, mat[keep_cols].copy()


def test_features_across_baits(mat: pd.DataFrame, features: Iterable[str], site: str, feature_type: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    bait_order = sorted(mat["bait"].unique().tolist())

    global_rows: List[Dict[str, object]] = []
    pair_rows: List[Dict[str, object]] = []

    for feature in features:
        groups = [mat.loc[mat["bait"] == b, feature].to_numpy(dtype=float) for b in bait_order]
        total_n = int(sum(len(g) for g in groups))
        k_groups = len(groups)

        try:
            h_stat, p_val = stats.kruskal(*groups)
        except ValueError:
            h_stat, p_val = 0.0, 1.0

        eta_sq = float((h_stat - k_groups + 1) / (total_n - k_groups)) if total_n > k_groups else math.nan
        if not math.isnan(eta_sq):
            eta_sq = max(0.0, eta_sq)

        means = {b: float(np.mean(mat.loc[mat["bait"] == b, feature])) for b in bait_order}
        dominant_bait = max(means, key=means.get)
        weakest_bait = min(means, key=means.get)

        global_rows.append(
            {
                "site": site,
                "feature_type": feature_type,
                "feature": feature,
                "n_total": total_n,
                "n_baits": k_groups,
                "h_stat": float(h_stat),
                "p_value": float(p_val),
                "eta_sq": eta_sq,
                "dominant_bait": dominant_bait,
                "weakest_bait": weakest_bait,
                "mean_diff_max_minus_min": float(means[dominant_bait] - means[weakest_bait]),
            }
        )

        pair_pvals: List[float] = []
        tmp_pair: List[Dict[str, object]] = []
        for a, b in itertools.combinations(bait_order, 2):
            xa = mat.loc[mat["bait"] == a, feature].to_numpy(dtype=float)
            xb = mat.loc[mat["bait"] == b, feature].to_numpy(dtype=float)
            try:
                u_stat, p_pair = stats.mannwhitneyu(xa, xb, alternative="two-sided")
            except ValueError:
                u_stat, p_pair = 0.0, 1.0
            delta = cliffs_delta(xa, xb)
            pair_pvals.append(float(p_pair))
            tmp_pair.append(
                {
                    "site": site,
                    "feature_type": feature_type,
                    "feature": feature,
                    "bait_a": a,
                    "bait_b": b,
                    "n_a": int(len(xa)),
                    "n_b": int(len(xb)),
                    "mean_a": float(np.mean(xa)) if len(xa) else math.nan,
                    "mean_b": float(np.mean(xb)) if len(xb) else math.nan,
                    "u_stat": float(u_stat),
                    "p_value": float(p_pair),
                    "cliffs_delta": delta,
                }
            )

        pair_holm = holm_adjust(pair_pvals)
        pair_bh = bh_adjust(pair_pvals)
        for row, p_h, p_bh in zip(tmp_pair, pair_holm, pair_bh):
            row["p_value_holm_within_feature"] = float(p_h)
            row["p_value_bh_within_feature"] = float(p_bh)
            row["significant_holm_within_feature"] = bool(p_h < ALPHA)
            row["significant_bh_within_feature"] = bool(p_bh < ALPHA)
            pair_rows.append(row)

    global_df = pd.DataFrame(global_rows)
    if not global_df.empty:
        global_df = global_df.sort_values("p_value", ascending=True).reset_index(drop=True)
        global_df["p_value_holm"] = holm_adjust(global_df["p_value"].tolist())
        global_df["p_value_bh"] = bh_adjust(global_df["p_value"].tolist())
        global_df["significant_holm"] = global_df["p_value_holm"] < ALPHA
        global_df["significant_bh"] = global_df["p_value_bh"] < ALPHA

    pair_df = pd.DataFrame(pair_rows)
    return global_df, pair_df


def test_fish_vs_algae(mat: pd.DataFrame, features: Iterable[str], site: str, feature_type: str) -> pd.DataFrame:
    sub = mat[mat["bait_type"].isin(["fish", "algae"])].copy()
    if sub.empty:
        return pd.DataFrame()

    rows: List[Dict[str, object]] = []
    for feature in features:
        fish = sub.loc[sub["bait_type"] == "fish", feature].to_numpy(dtype=float)
        algae = sub.loc[sub["bait_type"] == "algae", feature].to_numpy(dtype=float)
        if len(fish) == 0 or len(algae) == 0:
            continue

        try:
            u_stat, p_val = stats.mannwhitneyu(fish, algae, alternative="two-sided")
        except ValueError:
            u_stat, p_val = 0.0, 1.0

        rows.append(
            {
                "site": site,
                "feature_type": feature_type,
                "feature": feature,
                "n_fish": int(len(fish)),
                "n_algae": int(len(algae)),
                "mean_fish": float(np.mean(fish)),
                "mean_algae": float(np.mean(algae)),
                "median_fish": float(np.median(fish)),
                "median_algae": float(np.median(algae)),
                "u_stat": float(u_stat),
                "p_value": float(p_val),
                "cliffs_delta_fish_minus_algae": cliffs_delta(fish, algae),
                "higher_side": "fish" if np.mean(fish) > np.mean(algae) else "algae",
            }
        )

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("p_value", ascending=True).reset_index(drop=True)
        df["p_value_holm"] = holm_adjust(df["p_value"].tolist())
        df["p_value_bh"] = bh_adjust(df["p_value"].tolist())
        df["significant_holm"] = df["p_value_holm"] < ALPHA
        df["significant_bh"] = df["p_value_bh"] < ALPHA
    return df


def write_summary_report(
    all_global: List[pd.DataFrame],
    all_fva: List[pd.DataFrame],
    all_pairwise: List[pd.DataFrame],
) -> None:
    md_lines: List[str] = []
    md_lines.append("# Funktionsvergleich: Koederunterschiede in Milimani und Utumbi")
    md_lines.append("")
    md_lines.append("Datengrundlage: normalized_reports/cut_47min/Annotation_reports_coral_reef")
    md_lines.append("")
    md_lines.append("Verwendete Korrekturen fuer multiples Testen: Holm und Benjamini-Hochberg (FDR/BH).")
    md_lines.append("")
    md_lines.append("## Getestete Zusammenfassungen und Kombinationen")
    md_lines.append("Die folgenden Gruppen wurden explizit als zusammengesetzte Features getestet:")
    defs_rows = [
        {"composite_group": name, "beschreibung": cfg["description"]}
        for name, cfg in COMPOSITE_GROUP_RULES.items()
    ]
    defs_df = pd.DataFrame(defs_rows).sort_values("composite_group")
    md_lines.append(defs_df.to_markdown(index=False))
    md_lines.append("")
    md_lines.append("Zusatzebenen (ebenfalls getestet): diet, word_group, family, genus, unspecific.")
    md_lines.append("")

    if all_global:
        g = pd.concat(all_global, ignore_index=True)
    else:
        g = pd.DataFrame()

    if all_fva:
        fva = pd.concat(all_fva, ignore_index=True)
    else:
        fva = pd.DataFrame()

    if all_pairwise:
        pair = pd.concat(all_pairwise, ignore_index=True)
    else:
        pair = pd.DataFrame()

    md_lines.append("## Signifikanz-Uebersicht")
    if g.empty:
        md_lines.append("Keine globalen Ergebnisse verfuegbar.")
    else:
        global_summary = (
            g.groupby(["site", "feature_type"], as_index=False)
            .agg(
                n_tested=("feature", "count"),
                n_sig_holm=("significant_holm", "sum"),
                n_sig_bh=("significant_bh", "sum"),
            )
            .sort_values(["site", "feature_type"])
        )
        md_lines.append("Globaltest ueber Koeder:")
        md_lines.append(global_summary.to_markdown(index=False))

    if not fva.empty:
        fva_summary = (
            fva.groupby(["site", "feature_type"], as_index=False)
            .agg(
                n_tested=("feature", "count"),
                n_sig_holm=("significant_holm", "sum"),
                n_sig_bh=("significant_bh", "sum"),
            )
            .sort_values(["site", "feature_type"])
        )
        md_lines.append("")
        md_lines.append("Fish-vs-Algae-Test:")
        md_lines.append(fva_summary.to_markdown(index=False))
    md_lines.append("")

    md_lines.append("## Signifikante Gruppen (Globaltest ueber Koeder)")
    if g.empty:
        md_lines.append("Keine Ergebnisse.")
    else:
        sig = g[(g["significant_holm"] == True) | (g["significant_bh"] == True)].copy()
        if sig.empty:
            md_lines.append("Keine Gruppe erreicht Signifikanz nach Holm/BH.")
            top = g.sort_values(["p_value", "mean_diff_max_minus_min"], ascending=[True, False]).head(20)
            md_lines.append("")
            md_lines.append("Top explorative Signale (roh p):")
            md_lines.append(top[["site", "feature_type", "feature", "p_value", "p_value_holm", "p_value_bh", "dominant_bait", "mean_diff_max_minus_min"]].to_markdown(index=False))
        else:
            sig = sig.sort_values(["p_value_bh", "p_value_holm", "p_value"], ascending=True)
            md_lines.append(sig[["site", "feature_type", "feature", "p_value", "p_value_holm", "p_value_bh", "eta_sq", "dominant_bait", "mean_diff_max_minus_min"]].to_markdown(index=False))

    md_lines.append("")
    md_lines.append("## Signifikante paarweise Koederunterschiede")
    if pair.empty:
        md_lines.append("Keine paarweisen Ergebnisse verfuegbar.")
    else:
        sig_pair = pair[(pair["significant_holm_within_feature"] == True) | (pair["significant_bh_within_feature"] == True)].copy()
        if sig_pair.empty:
            md_lines.append("Keine paarweisen Vergleiche signifikant nach Holm/BH (innerhalb Feature).")
        else:
            sig_pair = sig_pair.sort_values(["p_value_bh_within_feature", "p_value_holm_within_feature", "p_value"], ascending=True)
            md_lines.append(
                sig_pair[
                    [
                        "site",
                        "feature_type",
                        "feature",
                        "bait_a",
                        "bait_b",
                        "p_value",
                        "p_value_holm_within_feature",
                        "p_value_bh_within_feature",
                        "cliffs_delta",
                    ]
                ]
                .head(80)
                .to_markdown(index=False)
            )

    md_lines.append("")
    md_lines.append("## Signifikante Fish-vs-Algae-Unterschiede")
    if fva.empty:
        md_lines.append("Keine Fish-vs-Algae-Ergebnisse verfuegbar.")
    else:
        sig_fva = fva[(fva["significant_holm"] == True) | (fva["significant_bh"] == True)].copy()
        if sig_fva.empty:
            md_lines.append("Keine Gruppe signifikant nach Holm/BH im Fish-vs-Algae-Vergleich.")
            md_lines.append("")
            md_lines.append("Top explorative Signale (roh p):")
            md_lines.append(
                fva.sort_values("p_value", ascending=True)
                .head(20)[["site", "feature_type", "feature", "p_value", "p_value_holm", "p_value_bh", "higher_side", "cliffs_delta_fish_minus_algae"]]
                .to_markdown(index=False)
            )
        else:
            sig_fva = sig_fva.sort_values(["p_value_bh", "p_value_holm", "p_value"], ascending=True)
            md_lines.append(sig_fva[["site", "feature_type", "feature", "p_value", "p_value_holm", "p_value_bh", "higher_side", "cliffs_delta_fish_minus_algae"]].to_markdown(index=False))

    (OUT_DIR / "funktionsvergleich_bericht.md").write_text("\n".join(md_lines), encoding="utf-8")
    defs_df.to_csv(OUT_DIR / "composite_group_definitions.csv", index=False)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    video_rows: List[Dict[str, object]] = []
    for csv_path in sorted(CUT_ROOT.glob("*.csv")):
        date, site, _ = parse_video_metadata(csv_path.name)
        if not date or site not in TARGET_SITES:
            continue
        video_rows.append(load_video_features(csv_path))

    videos = pd.DataFrame(video_rows)
    if videos.empty:
        raise RuntimeError("Keine Videos fuer milimani/utumbi gefunden.")

    feature_settings = {
        "diet": {"min_present_videos": 1, "min_baits": 2},
        "word_group": {"min_present_videos": 2, "min_baits": 2},
        "family": {"min_present_videos": 3, "min_baits": 2},
        "genus": {"min_present_videos": 3, "min_baits": 2},
        "unspecific": {"min_present_videos": 3, "min_baits": 2},
        "composite_group": {"min_present_videos": 2, "min_baits": 2},
    }

    all_global: List[pd.DataFrame] = []
    all_fva: List[pd.DataFrame] = []
    all_pairwise: List[pd.DataFrame] = []

    for site in TARGET_SITES:
        site_dir = OUT_DIR / site
        site_dir.mkdir(parents=True, exist_ok=True)

        site_videos = videos[videos["site"] == site].copy()
        site_videos.to_csv(site_dir / f"{site}_video_metadata.csv", index=False)

        for feature_type, cfg in feature_settings.items():
            features, mat = prepare_feature_matrix(
                site_videos,
                feature_type=feature_type,
                min_present_videos=cfg["min_present_videos"],
                min_baits=cfg["min_baits"],
            )

            if not features:
                continue

            mat.to_csv(site_dir / f"{site}_{feature_type}_video_level.csv", index=False)

            global_df, pair_df = test_features_across_baits(mat, features, site, feature_type)
            fva_df = test_fish_vs_algae(mat, features, site, feature_type)

            global_df.to_csv(site_dir / f"{site}_{feature_type}_global_kruskal.csv", index=False)
            pair_df.to_csv(site_dir / f"{site}_{feature_type}_pairwise_mannwhitney.csv", index=False)
            fva_df.to_csv(site_dir / f"{site}_{feature_type}_fish_vs_algae.csv", index=False)

            if not global_df.empty:
                all_global.append(global_df)
            if not fva_df.empty:
                all_fva.append(fva_df)
            if not pair_df.empty:
                all_pairwise.append(pair_df)

    write_summary_report(all_global, all_fva, all_pairwise)


if __name__ == "__main__":
    main()
