#!/usr/bin/env python3
"""
Vergleich von feeding- und interested-Annotationen auf Koederbasis (cut_47min)
fuer alle Standorte.

Fragen:
- Unterscheiden sich feeding/interested-Haeufigkeiten zwischen Koedern je Standort?
- Welche Taxa treiben die Unterschiede (signifikant / trendhaft)?
- Welche Taxa sind je Koeder besonders (bait-spezifisch)?

Ausgabe:
- results/interested_feeding/
"""

from __future__ import annotations

import itertools
import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parent.parent
CUT_ROOT = ROOT / "normalized_reports" / "cut_47min"
CORAL_REEF_DIR = CUT_ROOT / "Annotation_reports_coral_reef"
NURSERY_DIR = CUT_ROOT / "Annotation_reports_Nursery"
MAXN_DIR = ROOT / "results" / "taxahäufigkeitköder"

OUT_DIR = ROOT / "results" / "interested_feeding"
SITES = ["milimani", "utumbi", "nursery"]
FLAGS = ["feeding", "interested"]
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


def significance_label(p_value: float) -> str:
    if pd.isna(p_value):
        return "n/a"
    if p_value < 0.001:
        return "***"
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return "ns"


def to_md(df: pd.DataFrame) -> str:
    if df.empty:
        return "Keine Daten."
    return df.to_markdown(index=False)


def load_video_annotations(csv_path: Path) -> Dict[str, object]:
    df = pd.read_csv(csv_path, engine="python", on_bad_lines="skip")

    counts_by_flag: Dict[str, Dict[str, int]] = {f: {} for f in FLAGS}
    total_events: Dict[str, int] = {f: 0 for f in FLAGS}

    for _, row in df.iterrows():
        taxon = build_taxon_key(row)
        if not taxon:
            continue

        for flag in FLAGS:
            if is_truthy(row.get(flag, "")):
                total_events[flag] += 1
                d = counts_by_flag[flag]
                d[taxon] = d.get(taxon, 0) + 1

    date, standort, koeder = parse_video_metadata(csv_path.name)

    return {
        "filename": csv_path.name,
        "date": date,
        "standort": standort,
        "koeder": koeder,
        "feeding_counts_by_taxon": counts_by_flag["feeding"],
        "interested_counts_by_taxon": counts_by_flag["interested"],
        "total_feeding_events": total_events["feeding"],
        "total_interested_events": total_events["interested"],
        "feeding_unique_taxa": len(counts_by_flag["feeding"]),
        "interested_unique_taxa": len(counts_by_flag["interested"]),
    }


def analyze_flag_site(videos_site: pd.DataFrame, site: str, flag: str) -> Dict[str, pd.DataFrame]:
    counts_col = f"{flag}_counts_by_taxon"
    total_col = f"total_{flag}_events"

    bait_order = sorted(videos_site["koeder"].unique().tolist())
    videos_by_bait = {b: videos_site[videos_site["koeder"] == b].copy() for b in bait_order}

    all_taxa = sorted(
        set().union(
            *[
                set().union(*videos_by_bait[b][counts_col].map(dict.keys).tolist())
                for b in bait_order
            ]
        )
    )

    taxa_rows: List[Dict[str, object]] = []
    pairwise_rows: List[Dict[str, object]] = []

    for taxon in all_taxa:
        arrays_by_bait: Dict[str, np.ndarray] = {}
        for bait in bait_order:
            vals = [
                float(v.get(taxon, 0))
                for v in videos_by_bait[bait][counts_col].tolist()
            ]
            arrays_by_bait[bait] = np.array(vals, dtype=float)

        groups = [arrays_by_bait[b] for b in bait_order]
        total_n = int(sum(len(g) for g in groups))
        n_groups = len(groups)

        try:
            h_stat, p_val = stats.kruskal(*groups)
        except ValueError:
            h_stat, p_val = 0.0, 1.0

        mean_by_bait = {b: float(np.mean(arrays_by_bait[b])) for b in bait_order}
        occ_by_bait = {
            b: (float(np.mean(arrays_by_bait[b] > 0)) if len(arrays_by_bait[b]) else math.nan)
            for b in bait_order
        }
        dominant = max(mean_by_bait, key=mean_by_bait.get)
        lowest = min(mean_by_bait, key=mean_by_bait.get)

        eta_sq = (
            float((h_stat - n_groups + 1) / (total_n - n_groups))
            if total_n > n_groups
            else math.nan
        )
        if not pd.isna(eta_sq):
            eta_sq = max(0.0, eta_sq)

        row = {
            "taxon_key": taxon,
            "n_total": total_n,
            "n_koeder": n_groups,
            "h_stat": float(h_stat),
            "p_value": float(p_val),
            "eta_sq": eta_sq,
            "dominant_koeder_mean": dominant,
            "lowest_koeder_mean": lowest,
            "mean_diff_max_minus_min": float(mean_by_bait[dominant] - mean_by_bait[lowest]),
        }
        for bait in bait_order:
            row[f"mean_{bait}"] = mean_by_bait[bait]
            row[f"occ_{bait}"] = occ_by_bait[bait]
        taxa_rows.append(row)

        p_pair: List[float] = []
        tmp_pair_rows: List[Dict[str, object]] = []
        for a, b in itertools.combinations(bait_order, 2):
            xa = arrays_by_bait[a]
            xb = arrays_by_bait[b]
            try:
                u_stat, p = stats.mannwhitneyu(xa, xb, alternative="two-sided")
            except ValueError:
                u_stat, p = 0.0, 1.0
            p_pair.append(float(p))
            tmp_pair_rows.append(
                {
                    "taxon_key": taxon,
                    "koeder_a": a,
                    "koeder_b": b,
                    "n_a": int(len(xa)),
                    "n_b": int(len(xb)),
                    "mean_a": float(np.mean(xa)) if len(xa) else math.nan,
                    "mean_b": float(np.mean(xb)) if len(xb) else math.nan,
                    "u_stat": float(u_stat),
                    "p_value": float(p),
                }
            )

        p_pair_adj = holm_adjust(p_pair)
        for pr, p_adj in zip(tmp_pair_rows, p_pair_adj):
            pr["p_value_holm_within_taxon"] = float(p_adj)
            pr["significant_0_05"] = bool(pr["p_value"] < ALPHA)
            pr["significant_0_05_holm_within_taxon"] = bool(p_adj < ALPHA)
            pairwise_rows.append(pr)

    taxa_df = pd.DataFrame(taxa_rows)
    if not taxa_df.empty:
        taxa_df = taxa_df.sort_values("p_value", ascending=True).reset_index(drop=True)
        taxa_df["p_value_holm"] = holm_adjust(taxa_df["p_value"].tolist())
        taxa_df["significant_0_05"] = taxa_df["p_value"] < ALPHA
        taxa_df["significant_0_05_holm"] = taxa_df["p_value_holm"] < ALPHA
        taxa_df["sig_label_raw"] = taxa_df["p_value"].map(significance_label)
        taxa_df["sig_label_holm"] = taxa_df["p_value_holm"].map(significance_label)
    else:
        taxa_df = pd.DataFrame(
            columns=[
                "taxon_key",
                "n_total",
                "n_koeder",
                "h_stat",
                "p_value",
                "eta_sq",
                "dominant_koeder_mean",
                "lowest_koeder_mean",
                "mean_diff_max_minus_min",
                "p_value_holm",
                "significant_0_05",
                "significant_0_05_holm",
                "sig_label_raw",
                "sig_label_holm",
            ]
        )

    pairwise_df = pd.DataFrame(pairwise_rows)

    # bait-spezifische taxa auf Basis Vorkommen (>0 Events in mindestens einem Video)
    specific_rows: List[Dict[str, object]] = []
    for taxon in all_taxa:
        present_baits: List[str] = []
        for bait in bait_order:
            arr = np.array(
                [float(v.get(taxon, 0)) for v in videos_by_bait[bait][counts_col].tolist()],
                dtype=float,
            )
            if float(np.sum(arr)) > 0:
                present_baits.append(bait)
        if len(present_baits) == 1:
            specific_rows.append(
                {
                    "koeder": present_baits[0],
                    "taxon_key": taxon,
                }
            )
    specific_df = pd.DataFrame(specific_rows)

    # Gesamtvergleich der Total-Events je Video zwischen Koedern
    overall_groups = [videos_by_bait[b][total_col].astype(float).to_numpy() for b in bait_order]
    try:
        h_total, p_total = stats.kruskal(*overall_groups)
    except ValueError:
        h_total, p_total = 0.0, 1.0

    overall_df = pd.DataFrame(
        [
            {
                "site": site,
                "flag": flag,
                "n_videos": int(len(videos_site)),
                "n_koeder": int(len(bait_order)),
                "h_stat": float(h_total),
                "p_value": float(p_total),
                "significant_0_05": bool(p_total < ALPHA),
                "sig_label": significance_label(float(p_total)),
            }
        ]
    )

    overall_pair_rows: List[Dict[str, object]] = []
    raw_ps: List[float] = []
    for a, b in itertools.combinations(bait_order, 2):
        xa = videos_by_bait[a][total_col].astype(float).to_numpy()
        xb = videos_by_bait[b][total_col].astype(float).to_numpy()
        try:
            u_stat, p = stats.mannwhitneyu(xa, xb, alternative="two-sided")
        except ValueError:
            u_stat, p = 0.0, 1.0
        raw_ps.append(float(p))
        overall_pair_rows.append(
            {
                "site": site,
                "flag": flag,
                "koeder_a": a,
                "koeder_b": b,
                "n_a": int(len(xa)),
                "n_b": int(len(xb)),
                "mean_total_a": float(np.mean(xa)) if len(xa) else math.nan,
                "mean_total_b": float(np.mean(xb)) if len(xb) else math.nan,
                "u_stat": float(u_stat),
                "p_value": float(p),
            }
        )

    overall_pair_df = pd.DataFrame(overall_pair_rows)
    if not overall_pair_df.empty:
        overall_pair_df["p_value_holm"] = holm_adjust(raw_ps)
        overall_pair_df["significant_0_05"] = overall_pair_df["p_value"] < ALPHA
        overall_pair_df["significant_0_05_holm"] = overall_pair_df["p_value_holm"] < ALPHA
        overall_pair_df["sig_label_raw"] = overall_pair_df["p_value"].map(significance_label)
        overall_pair_df["sig_label_holm"] = overall_pair_df["p_value_holm"].map(significance_label)

    bait_profile_rows: List[Dict[str, object]] = []
    specific_counts = (
        specific_df.groupby("koeder", as_index=False).size().rename(columns={"size": "n_bait_specific_taxa"})
        if not specific_df.empty
        else pd.DataFrame(columns=["koeder", "n_bait_specific_taxa"])
    )
    specific_map = {r.koeder: int(r.n_bait_specific_taxa) for r in specific_counts.itertuples(index=False)}

    trend_df = taxa_df[taxa_df["significant_0_05"] == True] if not taxa_df.empty else pd.DataFrame()
    for bait in bait_order:
        sub = videos_by_bait[bait]
        trend_count = (
            int((trend_df["dominant_koeder_mean"] == bait).sum()) if not trend_df.empty else 0
        )
        bait_profile_rows.append(
            {
                "site": site,
                "flag": flag,
                "koeder": bait,
                "n_videos": int(len(sub)),
                "mean_total_events": float(sub[total_col].mean()) if len(sub) else math.nan,
                "median_total_events": float(sub[total_col].median()) if len(sub) else math.nan,
                "mean_unique_taxa": float(sub[f"{flag}_unique_taxa"].mean()) if len(sub) else math.nan,
                "n_bait_specific_taxa": int(specific_map.get(bait, 0)),
                "n_trend_taxa_dominant": trend_count,
            }
        )

    bait_profile_df = pd.DataFrame(bait_profile_rows)

    return {
        "taxa_tests": taxa_df,
        "taxa_pairwise": pairwise_df,
        "specific_taxa": specific_df,
        "overall_test": overall_df,
        "overall_pairwise": overall_pair_df,
        "bait_profile": bait_profile_df,
    }


def write_site_report(
    site: str,
    site_df: pd.DataFrame,
    by_flag: Dict[str, Dict[str, pd.DataFrame]],
    maxn_site_df: pd.DataFrame,
) -> None:
    site_dir = OUT_DIR / site
    site_dir.mkdir(parents=True, exist_ok=True)

    lines: List[str] = []
    baits = sorted(site_df["koeder"].unique().tolist())
    lines.append(f"# Interested/Feeding Koedervergleich - {site.capitalize()} (cut_47min)")
    lines.append("")
    lines.append("## Datengrundlage")
    lines.append(f"- Standort: {site}")
    lines.append(f"- Anzahl Videos: {len(site_df)}")
    lines.append(f"- Koeder: {', '.join(baits)}")
    lines.append("- Taxonbildung: species > genus > family/label")
    lines.append("- Betrachtete Annotationen: feeding und interested")
    lines.append("")

    for flag in FLAGS:
        res = by_flag[flag]
        taxa_df = res["taxa_tests"]
        specific_df = res["specific_taxa"]
        overall_df = res["overall_test"]
        overall_pair_df = res["overall_pairwise"]
        bait_profile_df = res["bait_profile"]
        counts_col = f"{flag}_counts_by_taxon"

        lines.append(f"## {flag.capitalize()} - Signifikanz und Trends")

        n_taxa = int(len(taxa_df))
        n_raw = int((taxa_df["p_value"] < ALPHA).sum()) if not taxa_df.empty else 0
        n_holm = int((taxa_df["p_value_holm"] < ALPHA).sum()) if not taxa_df.empty else 0
        p_overall = float(overall_df.iloc[0]["p_value"]) if not overall_df.empty else math.nan

        lines.append(
            f"- Getestete Taxa: {n_taxa}; roh signifikant: {n_raw}; Holm-signifikant: {n_holm}."
        )
        lines.append(
            f"- Globaler Koedereffekt (Total-Events je Video): p={p_overall:.4g} ({'signifikant' if p_overall < ALPHA else 'nicht signifikant'})."
        )
        lines.append("")

        lines.append("### Koederprofile")
        lines.append(
            to_md(
                bait_profile_df[
                    [
                        "koeder",
                        "n_videos",
                        "mean_total_events",
                        "median_total_events",
                        "mean_unique_taxa",
                        "n_bait_specific_taxa",
                        "n_trend_taxa_dominant",
                    ]
                ].sort_values("koeder")
            )
        )
        lines.append("")

        lines.append("### Besondere Taxa (bait-spezifisch)")
        if specific_df.empty:
            lines.append("Keine bait-spezifischen Taxa in diesem Flag.")
        else:
            for bait in sorted(baits):
                t = (
                    specific_df[specific_df["koeder"] == bait]["taxon_key"]
                    .dropna()
                    .sort_values()
                    .tolist()
                )
                lines.append(f"- {bait} ({len(t)}):")
                if not t:
                    lines.append("  - Keine")
                else:
                    for taxon in t[:20]:
                        lines.append(f"  - {taxon}")
                    if len(t) > 20:
                        lines.append(f"  - ... (+{len(t)-20} weitere)")
        lines.append("")

        top_trends = (
            taxa_df[taxa_df["significant_0_05"] == True]
            .sort_values(["p_value", "mean_diff_max_minus_min"], ascending=[True, False])
            .head(15)
        )
        lines.append("### Top-Taxa-Trends (roh p<0.05)")
        lines.append(
            to_md(
                top_trends[
                    [
                        "taxon_key",
                        "dominant_koeder_mean",
                        "lowest_koeder_mean",
                        "p_value",
                        "p_value_holm",
                        "mean_diff_max_minus_min",
                        "eta_sq",
                    ]
                ]
                if not top_trends.empty
                else pd.DataFrame()
            )
        )
        lines.append("")

        lines.append("### Paarweise Koederunterschiede (Total-Events)")
        lines.append(to_md(overall_pair_df.sort_values("p_value", ascending=True)))
        lines.append("")

        # Neue Uebersicht: Taxa mit gesetztem Flag je Koeder + deren MaxN in diesem Koeder
        agg_rows: List[Dict[str, object]] = []
        for row in site_df.itertuples(index=False):
            bait = row.koeder
            cdict = getattr(row, counts_col)
            if not isinstance(cdict, dict):
                continue
            for taxon, n in cdict.items():
                agg_rows.append(
                    {
                        "koeder": bait,
                        "taxon_key": taxon,
                        "event_count": int(n),
                        "filename": row.filename,
                    }
                )

        taxa_bait_df = pd.DataFrame(agg_rows)
        if not taxa_bait_df.empty:
            taxa_bait_df = (
                taxa_bait_df.groupby(["koeder", "taxon_key"], as_index=False)
                .agg(
                    total_flag_events=("event_count", "sum"),
                    n_videos_with_flag=("filename", "nunique"),
                )
                .sort_values(["koeder", "total_flag_events", "n_videos_with_flag", "taxon_key"], ascending=[True, False, False, True])
                .reset_index(drop=True)
            )

            # MaxN-Infos fuer genau diese Taxa und Koeder
            maxn_merge = maxn_site_df[
                [
                    "taxon_key",
                    "koeder",
                    "mean_maxn",
                    "median_maxn",
                    "max_maxn",
                    "occurrence_rate",
                ]
            ].copy()
            taxa_bait_df = taxa_bait_df.merge(maxn_merge, on=["taxon_key", "koeder"], how="left")

            taxa_bait_df.rename(
                columns={
                    "occurrence_rate": "maxn_occurrence_rate",
                },
                inplace=True,
            )

            taxa_bait_df.to_csv(
                site_dir / f"{site}_{flag}_taxa_by_bait_with_maxn.csv",
                index=False,
            )

        lines.append("### Uebersicht: Taxa mit Flag je Koeder (inkl. MaxN dieser Taxa)")
        if taxa_bait_df.empty:
            lines.append("Keine Taxa mit diesem Flag vorhanden.")
            lines.append("")
        else:
            for bait in baits:
                lines.append(f"#### {bait}")
                sub_tbl = taxa_bait_df[taxa_bait_df["koeder"] == bait].copy()
                if sub_tbl.empty:
                    lines.append("Keine Taxa mit diesem Flag bei diesem Koeder.")
                else:
                    lines.append(
                        to_md(
                            sub_tbl[
                                [
                                    "taxon_key",
                                    "total_flag_events",
                                    "n_videos_with_flag",
                                    "mean_maxn",
                                    "median_maxn",
                                    "max_maxn",
                                    "maxn_occurrence_rate",
                                ]
                            ]
                        )
                    )
                lines.append("")

        lines.append("### Interpretation")
        if n_holm > 0:
            lines.append(
                f"- Es gibt robuste (Holm-korrigierte) Unterschiede zwischen Koedern fuer {n_holm} Taxa im Flag {flag}."
            )
        elif n_raw > 0:
            lines.append(
                f"- Es gibt {n_raw} trendhafte Taxa-Unterschiede (roh p<0.05), aber keine Holm-robusten Einzeleffekte."
            )
        else:
            lines.append("- Es zeigen sich keine klaren Taxa-Unterschiede zwischen Koedern in diesem Flag.")

        if not overall_pair_df.empty:
            n_pair_holm = int((overall_pair_df["p_value_holm"] < ALPHA).sum())
            n_pair_raw = int((overall_pair_df["p_value"] < ALPHA).sum())
            lines.append(
                f"- Paarweise Total-Event-Kontraste: roh signifikant {n_pair_raw}, Holm-signifikant {n_pair_holm}."
            )
        lines.append(
            "- Taxa mit hoher bait-spezifischer Anzahl und gleichzeitig trendhaftem Dominanzprofil sind prioritaere Kandidaten fuer koederabhaengiges Verhalten."
        )
        lines.append("")

    (site_dir / f"interested_feeding_{site}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_overall_summary(videos_df: pd.DataFrame, site_results: Dict[str, Dict[str, Dict[str, pd.DataFrame]]]) -> None:
    rows: List[Dict[str, object]] = []
    for site in SITES:
        if site not in site_results:
            continue
        res_feed = site_results[site]["feeding"]
        res_int = site_results[site]["interested"]

        feed_overall_p = float(res_feed["overall_test"].iloc[0]["p_value"])
        int_overall_p = float(res_int["overall_test"].iloc[0]["p_value"])

        rows.append(
            {
                "standort": site,
                "n_videos": int(len(videos_df[videos_df["standort"] == site])),
                "n_koeder": int(videos_df[videos_df["standort"] == site]["koeder"].nunique()),
                "feeding_taxa_tested": int(len(res_feed["taxa_tests"])),
                "feeding_raw_sig_taxa": int((res_feed["taxa_tests"]["p_value"] < ALPHA).sum()),
                "feeding_holm_sig_taxa": int((res_feed["taxa_tests"]["p_value_holm"] < ALPHA).sum()),
                "feeding_total_events_p": feed_overall_p,
                "feeding_total_events_sig": bool(feed_overall_p < ALPHA),
                "interested_taxa_tested": int(len(res_int["taxa_tests"])),
                "interested_raw_sig_taxa": int((res_int["taxa_tests"]["p_value"] < ALPHA).sum()),
                "interested_holm_sig_taxa": int((res_int["taxa_tests"]["p_value_holm"] < ALPHA).sum()),
                "interested_total_events_p": int_overall_p,
                "interested_total_events_sig": bool(int_overall_p < ALPHA),
            }
        )

    summary_df = pd.DataFrame(rows).sort_values("standort")
    summary_df.to_csv(OUT_DIR / "interested_feeding_site_summary.csv", index=False)

    lines: List[str] = []
    lines.append("# Interested/Feeding Koedervergleich (cut_47min) - Gesamtuebersicht")
    lines.append("")
    lines.append("## Kernergebnisse")
    lines.append(to_md(summary_df))
    lines.append("")

    lines.append("## Ausfuehrliche Interpretation")
    for _, r in summary_df.iterrows():
        site = r["standort"]
        lines.append(f"### {site}")
        lines.append(
            f"- Feeding: {int(r['feeding_raw_sig_taxa'])} Roh-Signale, {int(r['feeding_holm_sig_taxa'])} Holm-signifikant; "
            f"Globaltest Total-Events p={float(r['feeding_total_events_p']):.4g}."
        )
        lines.append(
            f"- Interested: {int(r['interested_raw_sig_taxa'])} Roh-Signale, {int(r['interested_holm_sig_taxa'])} Holm-signifikant; "
            f"Globaltest Total-Events p={float(r['interested_total_events_p']):.4g}."
        )
        lines.append(
            "- Ein gemeinsames Muster aus trendhaften Einzeltaxa + bait-spezifischen Taxa spricht fuer koederabhaengige Verhaltensschwerpunkte, "
            "auch wenn konservative Korrekturen einzelne Signale abschwaechen koennen."
        )
        lines.append("")

    # standortuebergreifende Tendenzen
    feed_global_sig = int(summary_df["feeding_total_events_sig"].sum())
    int_global_sig = int(summary_df["interested_total_events_sig"].sum())
    lines.append("## Standortuebergreifende Tendenzen")
    lines.append(
        f"- Global signifikante Koedereffekte auf Total-Events: Feeding in {feed_global_sig}/{len(summary_df)} Standorten, "
        f"Interested in {int_global_sig}/{len(summary_df)} Standorten."
    )

    feed_raw_total = int(summary_df["feeding_raw_sig_taxa"].sum())
    int_raw_total = int(summary_df["interested_raw_sig_taxa"].sum())
    lines.append(
        f"- Roh-signifikante Taxa summiert ueber Standorte: Feeding {feed_raw_total}, Interested {int_raw_total}."
    )
    lines.append(
        "- Fuer robuste Aussagen pro Taxon sollten Holm-signifikante Ergebnisse priorisiert werden; Roh-Signale sind als Trends/Hypothesen zu interpretieren."
    )
    lines.append("")

    lines.append("## Besondere Taxa und Trends")
    lines.append(
        "- Pro Standort finden sich detaillierte Listen bait-spezifischer Taxa sowie Top-Taxa-Trends in den jeweiligen Site-Reports."
    )
    lines.append(
        "- Besonders relevant sind Taxa, die (a) bait-spezifisch auftreten und (b) gleichzeitig trendhaft als dominanter Koeder in den MaxN-Event-Tests erscheinen."
    )
    lines.append("")

    lines.append("## Berichte pro Standort")
    for site in summary_df["standort"].tolist():
        lines.append(f"- {site}/interested_feeding_{site}.md")

    (OUT_DIR / "interested_feeding_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(CORAL_REEF_DIR.glob("*.csv")) + sorted(NURSERY_DIR.glob("*.csv"))
    if not files:
        raise FileNotFoundError("Keine Dateien in cut_47min gefunden.")

    records = [load_video_annotations(p) for p in files]
    videos_df = pd.DataFrame(records)
    videos_df = videos_df[videos_df["standort"].isin(SITES)].copy()
    videos_df = videos_df.sort_values(["standort", "date", "filename"]).reset_index(drop=True)

    # export video-level table
    videos_df[
        [
            "filename",
            "date",
            "standort",
            "koeder",
            "total_feeding_events",
            "total_interested_events",
            "feeding_unique_taxa",
            "interested_unique_taxa",
        ]
    ].to_csv(OUT_DIR / "interested_feeding_video_level.csv", index=False)

    # optional long export per taxon and flag
    long_rows: List[Dict[str, object]] = []
    for r in videos_df.itertuples(index=False):
        for flag in FLAGS:
            d = getattr(r, f"{flag}_counts_by_taxon")
            for taxon, n in d.items():
                long_rows.append(
                    {
                        "filename": r.filename,
                        "date": r.date,
                        "standort": r.standort,
                        "koeder": r.koeder,
                        "flag": flag,
                        "taxon_key": taxon,
                        "event_count": int(n),
                    }
                )
    pd.DataFrame(long_rows).to_csv(OUT_DIR / "interested_feeding_taxon_event_long.csv", index=False)

    site_results: Dict[str, Dict[str, Dict[str, pd.DataFrame]]] = {}
    for site in SITES:
        sub = videos_df[videos_df["standort"] == site].copy()
        if sub.empty:
            continue

        maxn_path = MAXN_DIR / site / f"{site}_taxon_maxn_by_koeder_summary.csv"
        if maxn_path.exists():
            maxn_site_df = pd.read_csv(maxn_path)
        else:
            maxn_site_df = pd.DataFrame(
                columns=[
                    "taxon_key",
                    "koeder",
                    "mean_maxn",
                    "median_maxn",
                    "max_maxn",
                    "occurrence_rate",
                ]
            )

        site_dir = OUT_DIR / site
        site_dir.mkdir(parents=True, exist_ok=True)

        by_flag: Dict[str, Dict[str, pd.DataFrame]] = {}
        for flag in FLAGS:
            res = analyze_flag_site(sub, site, flag)
            by_flag[flag] = res

            res["taxa_tests"].to_csv(site_dir / f"{site}_{flag}_taxa_tests.csv", index=False)
            res["taxa_pairwise"].to_csv(site_dir / f"{site}_{flag}_taxa_pairwise_tests.csv", index=False)
            res["specific_taxa"].to_csv(site_dir / f"{site}_{flag}_bait_specific_taxa.csv", index=False)
            res["overall_test"].to_csv(site_dir / f"{site}_{flag}_overall_total_events_test.csv", index=False)
            res["overall_pairwise"].to_csv(site_dir / f"{site}_{flag}_overall_total_events_pairwise.csv", index=False)
            res["bait_profile"].to_csv(site_dir / f"{site}_{flag}_bait_profile.csv", index=False)

        write_site_report(site, sub, by_flag, maxn_site_df)
        site_results[site] = by_flag

    write_overall_summary(videos_df, site_results)

    print("Interested/Feeding Koedervergleich abgeschlossen.")
    print(f"Ergebnisse: {OUT_DIR}")


if __name__ == "__main__":
    main()
