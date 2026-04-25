#!/usr/bin/env python3
"""
Vergleicht Taxon-Haeufigkeiten (MaxN) zwischen Koedern, getrennt nach Standort
auf Basis cut_47min.

Fragestellungen (pro Standort):
- Unterscheiden sich die MaxN-Haeufigkeiten je Taxon zwischen Koedern?
- Welche Taxa kommen ueber alle Koeder aehnlich oft vor?
- Bei welchen Taxa liegen die groessten Koederunterschiede?

Ausgabe:
- results/taxahaeufigkeitkoeder/
"""

from __future__ import annotations

import itertools
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

OUT_DIR = ROOT / "results" / "taxahäufigkeitköder"
FIG_DIR = OUT_DIR / "figures"

SITES = ["milimani", "utumbi", "nursery"]
ALPHA = 0.05


def is_truthy(value: object) -> bool:
    if value is None:
        return False
    text = str(value).strip().lower()
    if text in {"", "0", "false", "f", "no", "n", "none", "null", "nan"}:
        return False
    return True


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


def significance_label(p_val: float) -> str:
    if p_val < 0.001:
        return "***"
    if p_val < 0.01:
        return "**"
    if p_val < 0.05:
        return "*"
    return "ns"


def to_md(df: pd.DataFrame) -> str:
    if df.empty:
        return "Keine Daten."
    return df.to_markdown(index=False)


def create_site_figures(site: str, taxon_tests_df: pd.DataFrame, taxon_bait_df: pd.DataFrame) -> None:
    site_fig_dir = FIG_DIR / site
    site_fig_dir.mkdir(parents=True, exist_ok=True)

    raw_sig = int((taxon_tests_df["p_value"] < ALPHA).sum())
    holm_sig = int((taxon_tests_df["p_value_holm"] < ALPHA).sum())

    plt.figure(figsize=(7, 4.8))
    plt.bar(["roh p<0.05", "Holm p<0.05"], [raw_sig, holm_sig], color=["#4c78a8", "#f58518"])
    plt.ylabel("Anzahl Taxa")
    plt.title(f"{site.capitalize()}: Signifikante Koederunterschiede je Taxon (MaxN)")
    plt.tight_layout()
    plt.savefig(site_fig_dir / "significant_taxa_counts.png", dpi=180)
    plt.close()

    top_taxa = (
        taxon_bait_df.groupby("taxon_key", as_index=False)["mean_maxn"]
        .mean()
        .sort_values("mean_maxn", ascending=False)
        .head(20)["taxon_key"]
        .tolist()
    )
    if top_taxa:
        bait_order = sorted(taxon_bait_df["koeder"].unique().tolist())
        mat = (
            taxon_bait_df[taxon_bait_df["taxon_key"].isin(top_taxa)]
            .pivot(index="taxon_key", columns="koeder", values="mean_maxn")
            .reindex(index=top_taxa, columns=bait_order)
            .fillna(0.0)
        )

        plt.figure(figsize=(11, max(6, len(top_taxa) * 0.28)))
        im = plt.imshow(mat.values, aspect="auto", cmap="YlGnBu")
        plt.xticks(range(len(bait_order)), bait_order, rotation=35, ha="right")
        plt.yticks(range(len(top_taxa)), top_taxa)
        plt.title(f"{site.capitalize()}: Top-20 Taxa nach mittlerem MaxN (Koedervergleich)")
        plt.colorbar(im, fraction=0.03, pad=0.02, label="Mean MaxN")
        plt.tight_layout()
        plt.savefig(site_fig_dir / "top20_taxa_mean_maxn_heatmap.png", dpi=180)
        plt.close()


def analyze_site(videos_site: pd.DataFrame, site: str) -> Dict[str, pd.DataFrame]:
    bait_order = sorted(videos_site["koeder"].unique().tolist())
    site_videos = {b: videos_site[videos_site["koeder"] == b].copy() for b in bait_order}

    all_taxa = sorted(set().union(*[set().union(*site_videos[b]["maxn_by_taxon"].map(dict.keys).tolist()) for b in bait_order]))

    taxon_rows: List[Dict[str, object]] = []
    bait_rows: List[Dict[str, object]] = []
    pairwise_rows: List[Dict[str, object]] = []

    for taxon in all_taxa:
        bait_arrays: Dict[str, np.ndarray] = {}
        for bait in bait_order:
            vals = [float(v.maxn_by_taxon.get(taxon, 0)) for v in site_videos[bait].itertuples(index=False)]
            arr = np.array(vals, dtype=float)
            bait_arrays[bait] = arr

            bait_rows.append(
                {
                    "taxon_key": taxon,
                    "koeder": bait,
                    "n_videos": int(len(arr)),
                    "n_present": int(np.sum(arr > 0)),
                    "occurrence_rate": float(np.mean(arr > 0)) if len(arr) else math.nan,
                    "mean_maxn": float(np.mean(arr)) if len(arr) else math.nan,
                    "median_maxn": float(np.median(arr)) if len(arr) else math.nan,
                    "std_maxn": float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0,
                    "max_maxn": float(np.max(arr)) if len(arr) else math.nan,
                }
            )

        groups = [bait_arrays[b] for b in bait_order]
        total_n = int(sum(len(g) for g in groups))
        k_groups = len(groups)
        try:
            h_stat, p_val = stats.kruskal(*groups)
        except ValueError:
            h_stat, p_val = 0.0, 1.0

        eta_sq = float((h_stat - k_groups + 1) / (total_n - k_groups)) if total_n > k_groups else math.nan
        eta_sq = max(0.0, eta_sq) if not math.isnan(eta_sq) else math.nan

        mean_vals = {b: float(np.mean(bait_arrays[b])) for b in bait_order}
        med_vals = {b: float(np.median(bait_arrays[b])) for b in bait_order}
        dom_bait = max(mean_vals, key=mean_vals.get)
        low_bait = min(mean_vals, key=mean_vals.get)

        row = {
            "taxon_key": taxon,
            "n_total": total_n,
            "n_koeder": k_groups,
            "h_stat": float(h_stat),
            "p_value": float(p_val),
            "eta_sq": eta_sq,
            "dominant_koeder_mean": dom_bait,
            "lowest_koeder_mean": low_bait,
            "mean_diff_max_minus_min": float(mean_vals[dom_bait] - mean_vals[low_bait]),
        }
        for bait in bait_order:
            row[f"mean_{bait}"] = mean_vals[bait]
            row[f"median_{bait}"] = med_vals[bait]
        taxon_rows.append(row)

        pair_ps: List[float] = []
        pair_tmp: List[Dict[str, object]] = []
        for a, b in itertools.combinations(bait_order, 2):
            xa = bait_arrays[a]
            xb = bait_arrays[b]
            try:
                u_stat, p_pair = stats.mannwhitneyu(xa, xb, alternative="two-sided")
            except ValueError:
                u_stat, p_pair = 0.0, 1.0
            pair_ps.append(float(p_pair))
            pair_tmp.append(
                {
                    "taxon_key": taxon,
                    "koeder_a": a,
                    "koeder_b": b,
                    "n_a": int(len(xa)),
                    "n_b": int(len(xb)),
                    "mean_a": float(np.mean(xa)) if len(xa) else math.nan,
                    "mean_b": float(np.mean(xb)) if len(xb) else math.nan,
                    "median_a": float(np.median(xa)) if len(xa) else math.nan,
                    "median_b": float(np.median(xb)) if len(xb) else math.nan,
                    "u_stat": float(u_stat),
                    "p_value": float(p_pair),
                    "cliffs_delta": cliffs_delta(xa, xb),
                }
            )

        pair_adj = holm_adjust(pair_ps)
        for prow, p_adj in zip(pair_tmp, pair_adj):
            prow["p_value_holm_within_taxon"] = float(p_adj)
            prow["significant_0_05"] = bool(prow["p_value"] < ALPHA)
            prow["significant_0_05_holm_within_taxon"] = bool(p_adj < ALPHA)
            pairwise_rows.append(prow)

    taxon_tests_df = pd.DataFrame(taxon_rows).sort_values("p_value", ascending=True).reset_index(drop=True)
    taxon_tests_df["p_value_holm"] = holm_adjust(taxon_tests_df["p_value"].tolist())
    taxon_tests_df["significant_0_05"] = taxon_tests_df["p_value"] < ALPHA
    taxon_tests_df["significant_0_05_holm"] = taxon_tests_df["p_value_holm"] < ALPHA
    taxon_tests_df["sig_label_raw"] = taxon_tests_df["p_value"].map(significance_label)
    taxon_tests_df["sig_label_holm"] = taxon_tests_df["p_value_holm"].map(significance_label)

    taxon_bait_df = pd.DataFrame(bait_rows).sort_values(["taxon_key", "koeder"]).reset_index(drop=True)
    pairwise_df = pd.DataFrame(pairwise_rows).sort_values(["taxon_key", "p_value"]).reset_index(drop=True)

    wide = taxon_bait_df.pivot(index="taxon_key", columns="koeder", values=["occurrence_rate", "mean_maxn"]).copy()
    wide.columns = [f"{a}_{b}" for a, b in wide.columns]
    wide = wide.reset_index()

    similar_df = taxon_tests_df.merge(wide, on="taxon_key", how="left")
    mean_cols = [f"mean_{b}" for b in bait_order]
    occ_cols = [f"occurrence_rate_{b}" for b in bait_order]
    similar_df["mean_ratio_max_min"] = similar_df[mean_cols].max(axis=1) / (
        similar_df[mean_cols].replace(0, np.nan).min(axis=1)
    )
    mask_occ = np.logical_and.reduce([similar_df[c] >= 0.5 for c in occ_cols]) if occ_cols else pd.Series(False, index=similar_df.index)
    similar_df = similar_df[
        (similar_df["significant_0_05_holm"] == False)
        & mask_occ
        & (similar_df["mean_ratio_max_min"] <= 1.5)
    ].copy()
    similar_df = similar_df.sort_values(["mean_ratio_max_min", "p_value_holm", "taxon_key"]).reset_index(drop=True)

    diff_df = taxon_tests_df[taxon_tests_df["significant_0_05_holm"]].copy()
    diff_df = diff_df.sort_values(["p_value_holm", "mean_diff_max_minus_min"], ascending=[True, False]).reset_index(drop=True)

    return {
        "taxon_tests_df": taxon_tests_df,
        "taxon_bait_df": taxon_bait_df,
        "pairwise_df": pairwise_df,
        "similar_df": similar_df,
        "diff_df": diff_df,
        "bait_order": pd.DataFrame({"koeder": bait_order}),
    }


def build_site_markdown(site: str, n_videos: int, outputs: Dict[str, pd.DataFrame]) -> str:
    taxon_tests_df = outputs["taxon_tests_df"]
    pairwise_df = outputs["pairwise_df"]
    similar_df = outputs["similar_df"]
    diff_df = outputs["diff_df"]
    bait_order = outputs["bait_order"]["koeder"].tolist()

    n_taxa = int(taxon_tests_df["taxon_key"].nunique()) if not taxon_tests_df.empty else 0
    n_sig_raw = int((taxon_tests_df["p_value"] < ALPHA).sum()) if not taxon_tests_df.empty else 0
    n_sig_holm = int((taxon_tests_df["p_value_holm"] < ALPHA).sum()) if not taxon_tests_df.empty else 0

    top_diff = diff_df.head(25)
    top_sig = taxon_tests_df.sort_values(["p_value_holm", "p_value"]).head(25)
    top_similar = similar_df.head(30)
    top_diff_expl = taxon_tests_df.sort_values(["p_value", "mean_diff_max_minus_min"], ascending=[True, False]).head(25)

    sig_taxa = set(taxon_tests_df.loc[taxon_tests_df["p_value_holm"] < ALPHA, "taxon_key"].tolist())
    pairwise_sig = pairwise_df[pairwise_df["taxon_key"].isin(sig_taxa)].copy()
    pairwise_sig = pairwise_sig.sort_values(["taxon_key", "p_value_holm_within_taxon", "p_value"]).head(120)

    summary_sig = pd.DataFrame(
        [
            {
                "standort": site,
                "n_videos": n_videos,
                "n_koeder": len(bait_order),
                "n_taxa_tested": n_taxa,
                "n_significant_raw_p_lt_0_05": n_sig_raw,
                "n_significant_holm_p_lt_0_05": n_sig_holm,
                "share_significant_holm": (n_sig_holm / n_taxa) if n_taxa else math.nan,
            }
        ]
    )

    lines: List[str] = []
    lines.append(f"# Taxa-Haeufigkeit nach Koeder - {site.capitalize()} (MaxN, cut_47min)")
    lines.append("")
    lines.append("## Kurzfazit")
    lines.append(
        f"- Von {n_taxa} getesteten Taxa zeigen {n_sig_holm} Taxa signifikante Koederunterschiede nach Holm-Korrektur (roh: {n_sig_raw})."
    )
    lines.append("- Die Tabellen trennen Taxa mit aehnlicher Haeufigkeit ueber alle Koeder von Taxa mit deutlichen Koederunterschieden.")
    lines.append("")
    lines.append("## Datengrundlage")
    lines.append(f"- Standort: {site}")
    lines.append(f"- Anzahl Videos: {n_videos}")
    lines.append(f"- Koeder: {', '.join(bait_order)}")
    lines.append("- Quelle: normalized_reports/cut_47min")
    lines.append("- Metrik: MaxN je Taxon und Video (feeding/interested ausgeschlossen)")
    lines.append("- Test pro Taxon: Kruskal-Wallis ueber alle Koeder des Standorts, Holm-Korrektur ueber alle Taxa")
    lines.append("- Paarweise Folgeanalysen: Mann-Whitney U mit Holm-Korrektur je Taxon")
    lines.append("")
    lines.append("## Signifikanz ueber alle Taxa")
    lines.append(to_md(summary_sig))
    lines.append("")
    lines.append("## Taxa mit den staerksten Koederunterschieden")
    if top_diff.empty:
        lines.append("Keine Holm-signifikanten Taxa. Explorative Uebersicht (ungekorrigiert) siehe unten.")
        lines.append("")
        lines.append("### Explorative Top-Unterschiede (ohne Holm-Signifikanz)")
        lines.append(to_md(top_diff_expl))
    else:
        lines.append(to_md(top_diff))
    lines.append("")
    lines.append("## Taxa mit aehnlicher Haeufigkeit ueber alle Koeder")
    lines.append("Kriterium: in jedem Koeder in >=50% der Videos nachgewiesen, nicht signifikant nach Holm, aehnlicher Mittelwert (max/min <= 1.5).")
    lines.append(to_md(top_similar))
    lines.append("")
    lines.append("## Signifikante Taxa (Top nach Holm-p)")
    lines.append(to_md(top_sig))
    lines.append("")
    lines.append("## Paarweise Koeder-Tests (Auszug fuer signifikante Taxa)")
    lines.append(to_md(pairwise_sig))
    lines.append("")
    lines.append("## Ausfuehrliche Interpretation")
    if n_sig_holm > 0:
        lines.append(
            "Die Analyse zeigt, dass innerhalb dieses Standorts ein relevanter Teil der Taxa seine MaxN-Haeufigkeit "
            "abwaegig vom verwendeten Koeder veraendert. Ein signifikanter Anteil nach Holm-Korrektur spricht gegen "
            "einen rein zufaelligen Koedereffekt."
        )
    else:
        lines.append(
            "Nach strenger Holm-Korrektur ergibt sich innerhalb dieses Standorts kein robuster Taxon-spezifischer "
            "Koedereffekt. Die ungekorrigierten Signale (roh p<0.05) sollten daher als explorativ gelesen werden."
        )
    lines.append(
        "Taxa mit sehr hohen Differenzen zwischen dominierendem und niedrigstem Koeder sind die wichtigsten Treiber "
        "der Koedertrennung. Diese Taxa sind oekologisch besonders informativ, weil sie auf koederspezifische "
        "Anlockungs- oder Sichtbarkeitseffekte hinweisen koennen."
    )
    lines.append(
        "Die paarweisen Tests zeigen, welche konkreten Koederpaare die Unterschiede tragen. Wenn global signifikante "
        "Taxa vor allem in wenigen Paaren differieren, deutet das auf selektive Koederkontraste hin; wenn viele Paare "
        "signifikant sind, ist der Koedereffekt breit ueber das Koederspektrum verteilt."
    )
    lines.append(
        "Taxa in der Tabelle mit aehnlicher Haeufigkeit ueber alle Koeder sind Kandidaten fuer koederrobuste "
        "Abundanzindikatoren innerhalb dieses Standorts."
    )
    lines.append(
        "Methodisch wichtig: Abwesenheiten wurden als MaxN=0 in die Videoebene aufgenommen. Dadurch fliessen sowohl "
        "Nachweishaeufigkeit als auch Hoehe der MaxN-Werte in die Testentscheidung ein."
    )
    lines.append("")
    lines.append("## Grafiken")
    lines.append(f"- ../figures/{site}/significant_taxa_counts.png")
    lines.append(f"- ../figures/{site}/top20_taxa_mean_maxn_heatmap.png")

    return "\n".join(lines) + "\n"


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(CORAL_REEF_DIR.glob("*.csv")) + sorted(NURSERY_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError("Keine CSV-Dateien unter normalized_reports/cut_47min gefunden.")

    records = [load_video_maxn(p) for p in files]
    videos_df = pd.DataFrame(records)
    videos_df = videos_df[videos_df["standort"].isin(SITES)].copy()
    videos_df = videos_df.sort_values(["standort", "date", "filename"]).reset_index(drop=True)

    video_level_rows: List[Dict[str, object]] = []
    for row in videos_df.itertuples(index=False):
        for taxon, maxn in row.maxn_by_taxon.items():
            video_level_rows.append(
                {
                    "filename": row.filename,
                    "date": row.date,
                    "standort": row.standort,
                    "koeder": row.koeder,
                    "taxon_key": taxon,
                    "maxn": int(maxn),
                }
            )
    video_level_df = pd.DataFrame(video_level_rows)
    video_level_df.to_csv(OUT_DIR / "taxon_maxn_video_level.csv", index=False)

    summary_rows: List[Dict[str, object]] = []

    for site in SITES:
        sub = videos_df[videos_df["standort"] == site].copy().reset_index(drop=True)
        if sub.empty or sub["koeder"].nunique() < 2:
            continue

        outputs = analyze_site(sub, site)
        site_dir = OUT_DIR / site
        site_dir.mkdir(parents=True, exist_ok=True)

        taxon_tests_df = outputs["taxon_tests_df"]
        taxon_bait_df = outputs["taxon_bait_df"]
        pairwise_df = outputs["pairwise_df"]
        similar_df = outputs["similar_df"]
        diff_df = outputs["diff_df"]

        taxon_tests_df.to_csv(site_dir / f"{site}_taxa_kruskal_koeder_tests.csv", index=False)
        taxon_bait_df.to_csv(site_dir / f"{site}_taxon_maxn_by_koeder_summary.csv", index=False)
        pairwise_df.to_csv(site_dir / f"{site}_taxa_pairwise_mannwhitney_tests.csv", index=False)
        similar_df.to_csv(site_dir / f"{site}_taxa_similar_frequency_all_koeder.csv", index=False)
        diff_df.to_csv(site_dir / f"{site}_taxa_significant_koeder_differences.csv", index=False)

        create_site_figures(site, taxon_tests_df, taxon_bait_df)

        report = build_site_markdown(site, len(sub), outputs)
        (site_dir / f"taxahaeufigkeit_koeder_{site}.md").write_text(report, encoding="utf-8")

        summary_rows.append(
            {
                "standort": site,
                "n_videos": int(len(sub)),
                "n_koeder": int(sub["koeder"].nunique()),
                "n_taxa_tested": int(taxon_tests_df["taxon_key"].nunique()),
                "n_significant_raw_p_lt_0_05": int((taxon_tests_df["p_value"] < ALPHA).sum()),
                "n_significant_holm_p_lt_0_05": int((taxon_tests_df["p_value_holm"] < ALPHA).sum()),
            }
        )

    summary_df = pd.DataFrame(summary_rows).sort_values("standort").reset_index(drop=True)
    summary_df.to_csv(OUT_DIR / "taxahaeufigkeit_koeder_summary.csv", index=False)

    lines: List[str] = []
    lines.append("# Taxa-Haeufigkeit Koedervergleich (MaxN, cut_47min) - Gesamtuebersicht")
    lines.append("")
    lines.append("Die Koedervergleiche wurden getrennt je Standort durchgefuehrt.")
    lines.append("")
    lines.append("## Kernergebnisse")
    lines.append(to_md(summary_df))
    lines.append("")
    lines.append("## Kurzinterpretation")
    for row in summary_df.itertuples(index=False):
        lines.append(
            f"- {row.standort}: {row.n_significant_holm_p_lt_0_05} signifikante Taxa (Holm) bei "
            f"{row.n_taxa_tested} getesteten Taxa im Koedervergleich."
        )
    lines.append("")
    lines.append("## Berichte pro Standort")
    for row in summary_df.itertuples(index=False):
        lines.append(f"- {row.standort}/taxahaeufigkeit_koeder_{row.standort}.md")
    lines.append("")
    lines.append("## Wichtige Exportdateien pro Standort")
    lines.append("- <standort>_taxa_kruskal_koeder_tests.csv")
    lines.append("- <standort>_taxon_maxn_by_koeder_summary.csv")
    lines.append("- <standort>_taxa_pairwise_mannwhitney_tests.csv")
    lines.append("- <standort>_taxa_significant_koeder_differences.csv")
    lines.append("- <standort>_taxa_similar_frequency_all_koeder.csv")

    (OUT_DIR / "taxahaeufigkeit_koeder_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("Taxa-Haeufigkeit Koedervergleich abgeschlossen.")
    print(f"Ergebnisse: {OUT_DIR}")


if __name__ == "__main__":
    main()
