from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
ARTEN_DIR = ROOT / "results" / "artenvergleich_köder"
FREQ_DIR = ROOT / "results" / "taxahäufigkeitköder"
OUT_DIR = ROOT / "results" / "artenvergleich_artenhäufigkeit"


def _fmt(x: float | int | None, digits: int = 3) -> str:
    if x is None:
        return "NA"
    if isinstance(x, float) and (np.isnan(x) or np.isinf(x)):
        return "inf" if np.isinf(x) else "NA"
    return f"{x:.{digits}f}" if isinstance(x, float) else str(x)


def _load_optional_csv(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()


def build_integrated_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    sites = ["milimani", "utumbi", "nursery"]
    site_rows: list[dict] = []
    bait_rows: list[dict] = []
    pair_rows: list[dict] = []

    for site in sites:
        kf = FREQ_DIR / site / f"{site}_taxa_kruskal_koeder_tests.csv"
        tf = FREQ_DIR / site / f"{site}_taxon_maxn_by_koeder_summary.csv"
        pf = FREQ_DIR / site / f"{site}_taxa_pairwise_mannwhitney_tests.csv"
        if not (kf.exists() and tf.exists()):
            continue

        k = pd.read_csv(kf)
        t = pd.read_csv(tf)
        p = _load_optional_csv(pf)

        grp = t.groupby("taxon_key")
        taxon_stats = grp["mean_maxn"].agg(["max", "min"]).rename(
            columns={"max": "max_mean", "min": "min_mean"}
        )
        taxon_stats["ratio"] = taxon_stats.apply(
            lambda r: (r["max_mean"] / r["min_mean"])
            if r["min_mean"] > 0
            else (float("inf") if r["max_mean"] > 0 else 1.0),
            axis=1,
        )

        dom = t.loc[
            grp["mean_maxn"].idxmax(),
            ["taxon_key", "koeder", "mean_maxn", "occurrence_rate"],
        ].rename(
            columns={
                "koeder": "dominant_koeder",
                "mean_maxn": "dom_mean_maxn",
                "occurrence_rate": "dom_occurrence_rate",
            }
        )
        low = t.loc[
            grp["mean_maxn"].idxmin(), ["taxon_key", "koeder", "mean_maxn"]
        ].rename(columns={"koeder": "lowest_koeder", "mean_maxn": "low_mean_maxn"})

        per_taxon = (
            taxon_stats.merge(dom, on="taxon_key")
            .merge(low, on="taxon_key")
            .merge(
                k[
                    [
                        "taxon_key",
                        "p_value",
                        "p_value_holm",
                        "significant_0_05",
                        "significant_0_05_holm",
                    ]
                ],
                on="taxon_key",
                how="left",
            )
        )

        species_counts = pd.DataFrame()
        overlap = pd.DataFrame()
        comp_global = None
        comp_pair_raw = 0
        comp_pair_holm = 0

        if site in {"milimani", "utumbi"}:
            species_counts = _load_optional_csv(
                ARTEN_DIR / site / f"{site}_koederspezifische_taxa_counts.csv"
            )
            overlap = _load_optional_csv(
                ARTEN_DIR / site / f"{site}_pairwise_koeder_overlap.csv"
            )
            g = _load_optional_csv(
                ARTEN_DIR / site / f"{site}_composition_permanova_global.csv"
            )
            if not g.empty and "p_value" in g.columns:
                comp_global = float(g.loc[0, "p_value"])
            cp = _load_optional_csv(
                ARTEN_DIR / site / f"{site}_composition_permanova_pairwise.csv"
            )
            if not cp.empty:
                if "p_value" in cp.columns:
                    comp_pair_raw = int((cp["p_value"] < 0.05).sum())
                if "p_value_holm" in cp.columns:
                    comp_pair_holm = int((cp["p_value_holm"] < 0.05).sum())

        raw_pair_freq = int((p["p_value"] < 0.05).sum()) if "p_value" in p.columns else 0
        holm_pair_freq = (
            int((p["p_value_holm"] < 0.05).sum()) if "p_value_holm" in p.columns else 0
        )

        for bait in sorted(t["koeder"].unique()):
            bait_taxa = per_taxon[per_taxon["dominant_koeder"] == bait]
            n_specific = np.nan
            if not species_counts.empty and "n_bait_specific_taxa" in species_counts.columns:
                hit = species_counts.loc[
                    species_counts["koeder"] == bait, "n_bait_specific_taxa"
                ]
                n_specific = int(hit.iloc[0]) if not hit.empty else 0

            avg_dist = np.nan
            if not overlap.empty and "jaccard_distance" in overlap.columns:
                sub = overlap[(overlap["bait_a"] == bait) | (overlap["bait_b"] == bait)]
                if not sub.empty:
                    avg_dist = float(sub["jaccard_distance"].mean())

            bait_rows.append(
                {
                    "standort": site,
                    "koeder": bait,
                    "n_taxa_dominant_mean_maxn": int(len(bait_taxa)),
                    "n_dominant_taxa_raw_sig": int(
                        (bait_taxa["significant_0_05"] == True).sum()
                    ),
                    "n_dominant_taxa_holm_sig": int(
                        (bait_taxa["significant_0_05_holm"] == True).sum()
                    ),
                    "n_dominant_taxa_ratio_ge_3": int((bait_taxa["ratio"] >= 3).sum()),
                    "mean_dominant_mean_maxn": float(bait_taxa["dom_mean_maxn"].mean())
                    if not bait_taxa.empty
                    else 0.0,
                    "n_koederspezifische_taxa_presence": n_specific,
                    "avg_jaccard_distance_to_other_baits": avg_dist,
                }
            )

        tendencies = per_taxon[per_taxon["significant_0_05"] == True].copy()
        tendencies = tendencies.sort_values(["p_value", "ratio"], ascending=[True, False])
        tendencies.head(12)[
            [
                "taxon_key",
                "dominant_koeder",
                "p_value",
                "p_value_holm",
                "ratio",
                "dom_mean_maxn",
                "low_mean_maxn",
            ]
        ].to_csv(OUT_DIR / f"{site}_top_tendenzen_taxa.csv", index=False)

        site_rows.append(
            {
                "standort": site,
                "n_taxa_tested_freq": int(len(k)),
                "n_raw_sig_taxa_freq": int((k["p_value"] < 0.05).sum()),
                "n_holm_sig_taxa_freq": int((k["p_value_holm"] < 0.05).sum()),
                "n_raw_sig_pairwise_freq": raw_pair_freq,
                "n_holm_sig_pairwise_freq": holm_pair_freq,
                "composition_global_p": comp_global,
                "composition_global_sig_0_05": (
                    bool(comp_global < 0.05) if comp_global is not None else False
                ),
                "n_raw_sig_pairwise_composition": comp_pair_raw,
                "n_holm_sig_pairwise_composition": comp_pair_holm,
                "n_taxa_with_raw_tendency": int(len(tendencies)),
                "n_taxa_with_holm_effect": int(
                    (per_taxon["significant_0_05_holm"] == True).sum()
                ),
            }
        )

        if not overlap.empty:
            for _, r in overlap.iterrows():
                pair_rows.append(
                    {
                        "standort": site,
                        "bait_a": r["bait_a"],
                        "bait_b": r["bait_b"],
                        "jaccard_similarity": r["jaccard_similarity"],
                        "jaccard_distance": r["jaccard_distance"],
                        "unique_a": r["unique_a"],
                        "unique_b": r["unique_b"],
                    }
                )

    site_df = pd.DataFrame(site_rows)
    bait_df = pd.DataFrame(bait_rows).sort_values(["standort", "koeder"])
    pair_df = pd.DataFrame(pair_rows)

    site_df.to_csv(OUT_DIR / "integrierte_standort_summary.csv", index=False)
    bait_df.to_csv(OUT_DIR / "integrierte_koederprofile.csv", index=False)
    pair_df.to_csv(OUT_DIR / "integrierte_overlap_paare.csv", index=False)

    return site_df, bait_df, pair_df


def _bait_specialty_text(row: pd.Series, site: str) -> str:
    parts: list[str] = []
    if not pd.isna(row["n_koederspezifische_taxa_presence"]):
        parts.append(
            f"koederspezifische Taxa (Vorkommen): {int(row['n_koederspezifische_taxa_presence'])}"
        )
    if not pd.isna(row["avg_jaccard_distance_to_other_baits"]):
        parts.append(
            "mittlere Distanz in der Taxa-Zusammensetzung zu anderen Koedern: "
            + _fmt(float(row["avg_jaccard_distance_to_other_baits"]), 3)
        )

    parts.append(
        f"dominante Taxa nach MaxN: {int(row['n_taxa_dominant_mean_maxn'])}"
    )
    parts.append(
        f"davon Roh-Signal (p<0.05): {int(row['n_dominant_taxa_raw_sig'])}"
    )
    parts.append(
        f"starke Dominanz (Max/Min >= 3): {int(row['n_dominant_taxa_ratio_ge_3'])}"
    )
    parts.append(
        "mittleres dominantes MaxN-Niveau: " + _fmt(float(row["mean_dominant_mean_maxn"]), 2)
    )

    level = "moderat"
    if (
        int(row["n_dominant_taxa_raw_sig"]) >= 3
        or int(row["n_dominant_taxa_ratio_ge_3"]) >= 20
        or (
            not pd.isna(row["n_koederspezifische_taxa_presence"])
            and int(row["n_koederspezifische_taxa_presence"]) >= 6
        )
    ):
        level = "ausgepraegt"
    elif int(row["n_dominant_taxa_raw_sig"]) == 0 and int(
        row["n_dominant_taxa_ratio_ge_3"]
    ) < 10:
        level = "schwach"

    return f"{site}/{row['koeder']}: Profil {level}; " + "; ".join(parts)


def write_markdown(site_df: pd.DataFrame, bait_df: pd.DataFrame, pair_df: pd.DataFrame) -> None:
    lines: list[str] = []
    lines.append("# Integrierter Koedervergleich: Taxavorkommen + Taxahaeufigkeit (MaxN)")
    lines.append("")
    lines.append(
        "Diese Auswertung verbindet den Artenvergleich nach Koeder (Taxa-Zusammensetzung, Vorkommen) "
        "mit der Taxa-Haeufigkeitsanalyse (MaxN je Taxon, Kruskal/Mann-Whitney)."
    )
    lines.append("")
    lines.append("## Ziel")
    lines.append(
        "Bestimmt wird, bei welchem Koeder sich Unterschiede zu anderen Koedern zeigen, "
        "sowohl in der Taxa-Zusammensetzung als auch in der Taxa-Haeufigkeit."
    )
    lines.append("")

    lines.append("## Signifikanzstatus (integriert)")
    lines.append(
        "| standort | Taxa-Haeufigkeit: Roh-signifikante Taxa | Taxa-Haeufigkeit: Holm-signifikante Taxa | "
        "Pairwise MaxN Roh | Pairwise MaxN Holm | Komposition global p | Komposition global signifikant |"
    )
    lines.append("|:--|--:|--:|--:|--:|--:|:--|")
    for _, r in site_df.iterrows():
        lines.append(
            "| "
            + f"{r['standort']} | {int(r['n_raw_sig_taxa_freq'])} | {int(r['n_holm_sig_taxa_freq'])} | "
            + f"{int(r['n_raw_sig_pairwise_freq'])} | {int(r['n_holm_sig_pairwise_freq'])} | "
            + f"{_fmt(r['composition_global_p'], 4)} | {bool(r['composition_global_sig_0_05'])} |"
        )
    lines.append("")
    lines.append("Interpretation:")
    lines.append(
        "- Milimani und Utumbi zeigen signifikante globale Unterschiede in der Taxa-Zusammensetzung zwischen Koedern."
    )
    lines.append(
        "- Gleichzeitig gibt es in allen Standorten keine Holm-signifikanten taxonweisen MaxN-Effekte; die Haeufigkeitssignale bleiben trendbasiert."
    )
    lines.append(
        "- Das Muster spricht fuer breit verteilte, eher moderate Koedereffekte statt einzelner, sehr robuster Taxon-Einzeleffekte."
    )
    lines.append("")

    for site in ["milimani", "utumbi", "nursery"]:
        sub = bait_df[bait_df["standort"] == site].copy()
        if sub.empty:
            continue
        lines.append(f"## Standort {site}")
        lines.append("")

        srow = site_df[site_df["standort"] == site].iloc[0]
        lines.append("### Gesamtbild")
        if pd.notna(srow["composition_global_p"]):
            sigtxt = (
                "signifikant" if bool(srow["composition_global_sig_0_05"]) else "nicht signifikant"
            )
            lines.append(
                f"- Kompositionsunterschiede ueber alle Koeder: p={_fmt(float(srow['composition_global_p']),4)} ({sigtxt})."
            )
        else:
            lines.append(
                "- Kein separater Kompositionstest aus der Artenvergleich-Analyse verfuegbar (dieser Standort wurde dort nicht separat gerechnet)."
            )
        lines.append(
            f"- Taxa-Haeufigkeit: {int(srow['n_raw_sig_taxa_freq'])} Roh-Signale, {int(srow['n_holm_sig_taxa_freq'])} Holm-signifikante Taxa."
        )
        lines.append(
            f"- Paarweise MaxN-Tests: {int(srow['n_raw_sig_pairwise_freq'])} Roh-signifikante Kontraste, {int(srow['n_holm_sig_pairwise_freq'])} nach Holm."
        )
        lines.append("")

        lines.append("### Koederprofil je Koeder")
        lines.append(
            "| koeder | dominante Taxa (MaxN) | Roh-Tendenzen unter dominanten Taxa | starke Dominanz (Ratio >= 3) | koederspezifische Taxa (Vorkommen) | mittlere Jaccard-Distanz |"
        )
        lines.append("|:--|--:|--:|--:|--:|--:|")
        for _, r in sub.iterrows():
            lines.append(
                "| "
                + f"{r['koeder']} | {int(r['n_taxa_dominant_mean_maxn'])} | {int(r['n_dominant_taxa_raw_sig'])} | "
                + f"{int(r['n_dominant_taxa_ratio_ge_3'])} | "
                + f"{_fmt(r['n_koederspezifische_taxa_presence'],0)} | "
                + f"{_fmt(r['avg_jaccard_distance_to_other_baits'],3)} |"
            )
        lines.append("")

        lines.append("### Besonderheiten je Koeder")
        for _, r in sub.iterrows():
            lines.append("- " + _bait_specialty_text(r, site))
        lines.append("")

        top = _load_optional_csv(OUT_DIR / f"{site}_top_tendenzen_taxa.csv")
        if not top.empty:
            lines.append("### Wichtigste Taxa-Tendenzen (roh p<0.05, nicht Holm-korrigiert)")
            lines.append(
                "| taxon_key | dominanter koeder | p_value | p_value_holm | ratio max/min | mean_maxn dominant | mean_maxn niedrigster koeder |"
            )
            lines.append("|:--|:--|--:|--:|--:|--:|--:|")
            for _, tr in top.head(8).iterrows():
                lines.append(
                    "| "
                    + f"{tr['taxon_key']} | {tr['dominant_koeder']} | {_fmt(float(tr['p_value']),4)} | "
                    + f"{_fmt(float(tr['p_value_holm']),4)} | {_fmt(float(tr['ratio']),2)} | "
                    + f"{_fmt(float(tr['dom_mean_maxn']),2)} | {_fmt(float(tr['low_mean_maxn']),2)} |"
                )
            lines.append("")

        if not pair_df.empty and site in set(pair_df["standort"]):
            s_pairs = pair_df[pair_df["standort"] == site].sort_values(
                "jaccard_distance", ascending=False
            )
            if not s_pairs.empty:
                top_pair = s_pairs.iloc[0]
                lines.append("### Staerkster Vorkommenskontrast (Jaccard-Distanz)")
                lines.append(
                    f"- {top_pair['bait_a']} vs {top_pair['bait_b']}: Distanz={_fmt(float(top_pair['jaccard_distance']),3)}, "
                    f"unique_a={int(top_pair['unique_a'])}, unique_b={int(top_pair['unique_b'])}."
                )
                lines.append("")

    def _cat(b: str) -> str:
        if b in {"fischmix", "mackerel"}:
            return "fisch"
        if b in {"sargassum", "ulva_gutweed", "ulva_salad", "algae_strings", "algaemix"}:
            return "algen"
        return "kontrolle"

    b2 = bait_df.copy()
    b2["koeder_typ"] = b2["koeder"].map(_cat)
    cat_all = b2.groupby("koeder_typ", as_index=False).agg(
        dom_taxa=("n_taxa_dominant_mean_maxn", "sum"),
        raw_trends=("n_dominant_taxa_raw_sig", "sum"),
        strong_ratio=("n_dominant_taxa_ratio_ge_3", "sum"),
    )
    cat_lookup = {
        r["koeder_typ"]: {
            "dom_taxa": int(r["dom_taxa"]),
            "raw_trends": int(r["raw_trends"]),
            "strong_ratio": int(r["strong_ratio"]),
        }
        for _, r in cat_all.iterrows()
    }

    lines.append("## Uebergreifende Einordnung (ausfuehrlich)")
    lines.append(
        "Die kombinierte Evidenz aus Vorkommen (Artenvergleich) und Haeufigkeit (MaxN) zeigt ein konsistentes Muster mit zwei Ebenen:"
    )
    lines.append(
        "- Ebene 1, Gemeinschaft: In Milimani und Utumbi sind die globalen Kompositionsunterschiede zwischen Koedern signifikant. Das bedeutet, dass sich die Taxa-Gemeinschaft als Ganzes je nach Koeder verschiebt."
    )
    lines.append(
        "- Ebene 2, Einzeltaxa: Gleichzeitig fehlen Holm-signifikante Einzeltaxon-Effekte in der MaxN-Analyse. Das spricht gegen wenige, extrem robuste Treibertaxa und eher fuer verteilte, moderate Effekte ueber viele Taxa."
    )
    lines.append("")
    lines.append("Standortuebergreifende Tendenzen:")
    lines.append(
        "- In allen drei Standorten gibt es Roh-Signale (p<0.05), aber keine Holm-signifikanten Taxa. Die Richtung ist damit standortuebergreifend stabil, die inferenzstatistische Sicherheit jedoch begrenzt."
    )
    lines.append(
        "- In allen Standorten treten viele Taxa mit starker Dominanz auf (Ratio Max/Min >= 3). Das zeigt klare Haeufigkeitskontraste zwischen Koedern, auch wenn diese wegen Mehrfachtests nicht als robust signifikant klassifiziert werden."
    )
    lines.append(
        "- Fischkoeder (vor allem fischmix/mackerel) tragen in Milimani und Utumbi viele dominante Taxa und viele Roh-Tendenzen; Algenkoeder liefern parallel starke Kontraste, aber oft mit weniger Roh-signifikanten dominanten Taxa."
    )
    lines.append(
        "- Nursery zeigt ebenfalls deutliche Roh-Tendenzen, aber wegen kleinerer und unausgewogener Stichproben ist die Unsicherheit hoeher; dort ist die Interpretation staerker explorativ."
    )
    lines.append("")

    fish_stats = cat_lookup.get("fisch", {"dom_taxa": 0, "raw_trends": 0, "strong_ratio": 0})
    algae_stats = cat_lookup.get("algen", {"dom_taxa": 0, "raw_trends": 0, "strong_ratio": 0})

    lines.append("## Interpretation Algenkoeder vs Fischkoeder")
    lines.append("Zur Einordnung wurden Koeder in Gruppen zusammengefasst:")
    lines.append("- Fischkoeder: fischmix, mackerel")
    lines.append("- Algenkoeder: sargassum, ulva_gutweed, ulva_salad, algae_strings, algaemix")
    lines.append("")
    lines.append("Zusammengefasste Tendenzen ueber alle Standorte:")
    lines.append(
        f"- Dominante Taxa (MaxN): Fischkoeder {fish_stats['dom_taxa']}, Algenkoeder {algae_stats['dom_taxa']}. Beide Koedertypen zeigen breite taxonomische Wirkung, mit leichter Tendenz zugunsten Fischkoeder."
    )
    lines.append(
        f"- Roh-Tendenzen unter dominanten Taxa: Fischkoeder {fish_stats['raw_trends']}, Algenkoeder {algae_stats['raw_trends']}. Roh-Signale sind etwas haeufiger bei Fischkoedern."
    )
    lines.append(
        f"- Starke Dominanzkontraste (Ratio >= 3): Fischkoeder {fish_stats['strong_ratio']}, Algenkoeder {algae_stats['strong_ratio']}. Beide Koedertypen erzeugen starke Kontraste, Fischkoeder etwas ausgepraegter."
    )
    lines.append("")
    lines.append("Standortspezifische Lesart des Algen-vs-Fisch-Vergleichs:")
    lines.append(
        "- Milimani: Fischkoeder zeigen mehr Roh-Tendenzen als Algenkoeder, bei aehnlichem mittleren Dominanzniveau. Mackerel ist zudem ein klar differenzierender Koeder in der Vorkommensebene."
    )
    lines.append(
        "- Utumbi: Fischkoeder zeigen ebenfalls mehr Roh-Tendenzen. Gleichzeitig hat ein Algenkoeder (ulva_salad) ein sehr hohes mittleres Dominanzniveau. Das spricht fuer gemischte Koederantwort."
    )
    lines.append(
        "- Nursery: Algenkoeder tragen mehrere Roh-Tendenzen, waehrend mackerel in den dominanten Taxa kaum Roh-Signale zeigt. Wegen kleiner Stichprobe ist dies als Hinweis zu lesen."
    )
    lines.append("")
    lines.append("Praktische Folgerung:")
    lines.append(
        "- Ein einfacher Satz \"Fisch ist besser als Algen\" wird durch die Daten nicht getragen."
    )
    lines.append(
        "- Plausibler ist ein differenziertes Modell: Fischkoeder erzeugen haeufiger trendhafte Einzeltaxon-Reaktionen, waehrend Algenkoeder in einzelnen Kontexten sehr hohe lokale MaxN-Spitzen und klare Gemeinschaftsverschiebungen tragen."
    )
    lines.append(
        "- Fuer belastbare Aussagen pro Taxon sind mehr Replikate je Koeder notwendig, besonders um Standort*Koeder-Interaktionen robust zu testen."
    )
    lines.append("")
    lines.append("## Exportdateien in diesem Ordner")
    lines.append("- integrierte_standort_summary.csv")
    lines.append("- integrierte_koederprofile.csv")
    lines.append("- integrierte_overlap_paare.csv")
    lines.append("- <standort>_top_tendenzen_taxa.csv")

    (OUT_DIR / "artenvergleich_artenhaeufigkeit_koeder.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def main() -> None:
    site_df, bait_df, pair_df = build_integrated_tables()
    write_markdown(site_df, bait_df, pair_df)
    print("Integrierte Koeder-Auswertung erstellt:", OUT_DIR)


if __name__ == "__main__":
    main()
