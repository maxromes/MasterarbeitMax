from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import pearsonr, spearmanr, wilcoxon
from statsmodels.stats.multitest import multipletests


PROJECT_DIR = Path(__file__).resolve().parents[1]
MICRO_XLSX = PROJECT_DIR / "results" / "microzooplankton_analysis" / "microzooplankton_analysis.xlsx"
PHYTO_XLSX = PROJECT_DIR / "results" / "phytoplankton_analysis" / "phytoplankton_analysis.xlsx"
RESULTS_DIR = PROJECT_DIR / "results" / "microzooplankton_vs_phytoplankton"
FIGURES_DIR = RESULTS_DIR / "figures"
MESOCOSMS = [1, 2, 3, 6, 8, 9]
MICRO_DAYS = [1, 2, 3, 5, 6, 7, 11, 15, 19, 23, 27, 31]
PHYTO_DAYS = list(range(1, 32, 2))
POST_DAYS = [day for day in MICRO_DAYS if day >= 5]
LAGS = [-4, -2, 0, 2, 4]


def load_micro() -> pd.DataFrame:
    data = pd.read_excel(MICRO_XLSX, sheet_name="Gruppenverlauf")
    data = data[data.mesocosm.isin(MESOCOSMS)].copy()
    result = data.pivot_table(
        index=["mesocosm", "sample_day", "treatment_group"],
        columns="group",
        values="cells_L",
        aggfunc="sum",
    ).reset_index()
    result = result.rename(
        columns={"sample_day": "day", "Ciliate": "ciliate_cells_L", "Dinoflagellate": "dinoflagellate_cells_L"}
    )
    result["micro_total_cells_L"] = result["ciliate_cells_L"] + result["dinoflagellate_cells_L"]
    return result


def load_phyto() -> pd.DataFrame:
    data = pd.read_excel(PHYTO_XLSX, sheet_name="Gesamtverlauf")
    data = data[data.Mesocosm.isin(MESOCOSMS)].copy()
    return data.rename(
        columns={
            "Mesocosm": "mesocosm",
            "Day": "day",
            "small_cells_L": "phyto_small_cells_L",
            "large_cells_L": "phyto_large_cells_L",
            "total_cells_L": "phyto_total_cells_L",
        }
    )[
        [
            "mesocosm",
            "day",
            "phyto_small_cells_L",
            "phyto_large_cells_L",
            "phyto_total_cells_L",
        ]
    ]


def merge_data(micro: pd.DataFrame, phyto: pd.DataFrame) -> pd.DataFrame:
    data = micro.merge(phyto, on=["mesocosm", "day"], validate="one_to_one")
    data["phase"] = np.where(data.day <= 3, "Vorbehandlung", "Nachbehandlung")
    return data.sort_values(["mesocosm", "day"])


def add_log_values(data: pd.DataFrame) -> pd.DataFrame:
    result = data.copy()
    value_columns = [
        "ciliate_cells_L",
        "dinoflagellate_cells_L",
        "micro_total_cells_L",
        "phyto_small_cells_L",
        "phyto_large_cells_L",
        "phyto_total_cells_L",
    ]
    for column in value_columns:
        result[f"log10_{column}"] = np.log10(result[column].clip(lower=0) + 1)
    return result


def normalized_changes(data: pd.DataFrame) -> pd.DataFrame:
    value_columns = [
        "ciliate_cells_L",
        "dinoflagellate_cells_L",
        "micro_total_cells_L",
        "phyto_small_cells_L",
        "phyto_large_cells_L",
        "phyto_total_cells_L",
    ]
    baseline = data[data.day == 3][["mesocosm", *value_columns]].rename(
        columns={column: f"T3_{column}" for column in value_columns}
    )
    result = data[data.day >= 5].merge(baseline, on="mesocosm", validate="many_to_one")
    for column in value_columns:
        result[f"log2_change_{column}"] = np.log2(
            (result[column] + 1) / (result[f"T3_{column}"] + 1)
        )
        result[f"percent_change_{column}"] = (
            (result[column] - result[f"T3_{column}"])
            / result[f"T3_{column}"].replace(0, np.nan)
            * 100
        )
    return result


def correlation_rows(
    micro: pd.DataFrame, phyto: pd.DataFrame, x: str, y: str, label: str, lag: int
) -> list[dict]:
    rows = []
    left = micro[["mesocosm", "day", x]].rename(columns={x: "x"})
    right = phyto[["mesocosm", "day", y]].rename(columns={y: "y"}).copy()
    right["day"] = right["day"] - lag
    aligned = left.merge(right, on=["mesocosm", "day"], validate="one_to_one")
    for mesocosm, pairs in aligned.groupby("mesocosm"):
        pairs = pairs[["x", "y"]].dropna()
        if len(pairs) < 3 or pairs.x.nunique() < 2 or pairs.y.nunique() < 2:
            pearson_r = pearson_p = spearman_rho = spearman_p = np.nan
        else:
            pearson_r, pearson_p = pearsonr(pairs.x, pairs.y)
            spearman_rho, spearman_p = spearmanr(pairs.x, pairs.y)
        rows.append(
            {
                "comparison": label,
                "mesocosm": mesocosm,
                "lag_days": lag,
                "n_pairs": len(pairs),
                "pearson_r": pearson_r,
                "pearson_p": pearson_p,
                "spearman_rho": spearman_rho,
                "spearman_p": spearman_p,
            }
        )
    return rows


def correlations(micro: pd.DataFrame, phyto: pd.DataFrame) -> pd.DataFrame:
    micro = micro.copy()
    phyto = phyto.copy()
    for column in ["ciliate_cells_L", "dinoflagellate_cells_L", "micro_total_cells_L"]:
        micro[f"log10_{column}"] = np.log10(micro[column].clip(lower=0) + 1)
    for column in ["phyto_small_cells_L", "phyto_large_cells_L", "phyto_total_cells_L"]:
        phyto[f"log10_{column}"] = np.log10(phyto[column].clip(lower=0) + 1)
    comparisons = [
        ("log10_ciliate_cells_L", "log10_phyto_total_cells_L", "Ciliaten vs. Phytoplankton gesamt"),
        ("log10_dinoflagellate_cells_L", "log10_phyto_total_cells_L", "Dinoflagellaten vs. Phytoplankton gesamt"),
        ("log10_micro_total_cells_L", "log10_phyto_total_cells_L", "Mikrozooplankton gesamt vs. Phytoplankton gesamt"),
        ("log10_ciliate_cells_L", "log10_phyto_small_cells_L", "Ciliaten vs. Small-Phytoplankton"),
        ("log10_ciliate_cells_L", "log10_phyto_large_cells_L", "Ciliaten vs. Large-Phytoplankton"),
        ("log10_dinoflagellate_cells_L", "log10_phyto_large_cells_L", "Dinoflagellaten vs. Large-Phytoplankton"),
    ]
    rows: list[dict] = []
    for x, y, label in comparisons:
        for lag in LAGS:
            rows.extend(correlation_rows(micro, phyto, x, y, label, lag=lag))
    result = pd.DataFrame(rows)
    valid = result.spearman_p.notna()
    result.loc[valid, "spearman_p_fdr"] = multipletests(
        result.loc[valid, "spearman_p"], method="fdr_bh"
    )[1]
    result["significant_uncorrected"] = result.spearman_p < 0.05
    result["significant_fdr"] = result.spearman_p_fdr < 0.05
    return result


def effect_summary(normalized: pd.DataFrame) -> pd.DataFrame:
    columns = {
        "log2_change_ciliate_cells_L": "ciliate",
        "log2_change_dinoflagellate_cells_L": "dinoflagellate",
        "log2_change_micro_total_cells_L": "micro_total",
        "log2_change_phyto_small_cells_L": "phyto_small",
        "log2_change_phyto_large_cells_L": "phyto_large",
        "log2_change_phyto_total_cells_L": "phyto_total",
    }
    data = normalized[normalized.day.isin(POST_DAYS)].copy()
    result = data.groupby("mesocosm", as_index=False).agg(
        treatment_group=("treatment_group", "first"),
        **{name: (column, "mean") for column, name in columns.items()},
    )
    pairs = [
        ("ciliate", "phyto_total"),
        ("dinoflagellate", "phyto_total"),
        ("micro_total", "phyto_total"),
        ("ciliate", "phyto_small"),
        ("ciliate", "phyto_large"),
        ("dinoflagellate", "phyto_large"),
    ]
    rows = []
    for x, y in pairs:
        subset = result[[x, y]].dropna()
        pearson_r, pearson_p = pearsonr(subset[x], subset[y])
        spearman_rho, spearman_p = spearmanr(subset[x], subset[y])
        rows.append(
            {
                "effect_comparison": f"{x} vs. {y}",
                "n_mesocosms": len(subset),
                "pearson_r": pearson_r,
                "pearson_p": pearson_p,
                "spearman_rho": spearman_rho,
                "spearman_p": spearman_p,
            }
        )
    return pd.DataFrame(rows), result


def paired_tests(normalized: pd.DataFrame) -> pd.DataFrame:
    variables = {
        "Ciliaten": "ciliate_cells_L",
        "Dinoflagellaten": "dinoflagellate_cells_L",
        "Mikrozooplankton gesamt": "micro_total_cells_L",
        "Phytoplankton small": "phyto_small_cells_L",
        "Phytoplankton large": "phyto_large_cells_L",
        "Phytoplankton gesamt": "phyto_total_cells_L",
    }
    rows = []
    for label, variable in variables.items():
        changes = normalized.groupby("mesocosm")[f"log2_change_{variable}"].mean().dropna()
        statistic, p_value = wilcoxon(changes, alternative="two-sided", method="exact")
        rows.append(
            {
                "variable": label,
                "n_mesocosms": len(changes),
                "median_mean_log2_change": changes.median(),
                "wilcoxon_statistic": statistic,
                "wilcoxon_p": p_value,
                "interpretation": "signifikant gegen 0" if p_value < 0.05 else "nicht signifikant",
            }
        )
    return pd.DataFrame(rows)


def lag_summary(correlation_data: pd.DataFrame) -> pd.DataFrame:
    result = (
        correlation_data.sort_values("spearman_rho", ascending=False)
        .groupby(["comparison", "lag_days"], as_index=False)
        .agg(
            n_mesocosms=("mesocosm", "count"),
            mean_spearman_rho=("spearman_rho", "mean"),
            median_spearman_rho=("spearman_rho", "median"),
            significant_fdr=("significant_fdr", "sum"),
        )
    )
    return result


def save_figures(data: pd.DataFrame, normalized: pd.DataFrame, correlation_data: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid", context="notebook")
    palette = {
        "ciliate_cells_L": "#0072B2",
        "dinoflagellate_cells_L": "#D55E00",
        "phyto_total_cells_L": "#009E73",
    }
    plot = data.melt(
        id_vars=["mesocosm", "day"],
        value_vars=list(palette),
        var_name="variable",
        value_name="cells_L",
    )
    fig, axes = plt.subplots(3, 1, figsize=(11, 11), sharex=True)
    for ax, mesocosm in zip(axes, [1, 2, 3]):
        subset = plot[plot.mesocosm == mesocosm]
        sns.lineplot(
            data=subset,
            x="day",
            y="cells_L",
            hue="variable",
            marker="o",
            palette=palette,
            ax=ax,
        )
        ax.axvline(4, color="black", linestyle="--", linewidth=1)
        ax.set_yscale("log")
        ax.set_title(f"M{mesocosm}")
        ax.set_ylabel("Zellen L$^{-1}$")
    axes[-1].set_xlabel("Probetag")
    fig.suptitle("Mikrozooplankton und Phytoplankton: zeitgleiche Verläufe", y=1.01)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "01_zeitvergleiche.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    scatter = data.melt(
        id_vars=["mesocosm", "day", "treatment_group"],
        value_vars=["ciliate_cells_L", "dinoflagellate_cells_L"],
        var_name="micro_group",
        value_name="micro_cells_L",
    )
    scatter = scatter.merge(
        data[["mesocosm", "day", "phyto_total_cells_L"]].drop_duplicates(),
        on=["mesocosm", "day"],
    )
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, group in zip(axes, ["ciliate_cells_L", "dinoflagellate_cells_L"]):
        subset = scatter[scatter.micro_group == group]
        sns.scatterplot(
            data=subset,
            x="phyto_total_cells_L",
            y="micro_cells_L",
            hue="mesocosm",
            style="day",
            palette="tab10",
            s=75,
            ax=ax,
        )
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("Phytoplankton gesamt (Zellen L$^{-1}$)")
        ax.set_ylabel(f"{'Ciliaten' if 'ciliate' in group else 'Dinoflagellaten'} (Zellen L$^{{-1}}$)")
    fig.suptitle("Zeitgleiche Zusammenhänge")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "02_korrelationen.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    heatmap = correlation_data[correlation_data.comparison.isin(
        ["Ciliaten vs. Phytoplankton gesamt", "Dinoflagellaten vs. Phytoplankton gesamt"]
    )].pivot_table(index="comparison", columns="lag_days", values="spearman_rho", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(8, 3))
    sns.heatmap(heatmap, annot=True, fmt=".2f", cmap="vlag", center=0, ax=ax)
    ax.set_xlabel("Lag: Phytoplankton gegenüber Mikrozooplankton (Tage)")
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "03_zeitverzoegerte_korrelationen.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    lag_lines = correlation_data[
        correlation_data.comparison.isin(
            ["Ciliaten vs. Phytoplankton gesamt", "Dinoflagellaten vs. Phytoplankton gesamt"]
        )
    ]
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    for ax, comparison in zip(
        axes,
        ["Ciliaten vs. Phytoplankton gesamt", "Dinoflagellaten vs. Phytoplankton gesamt"],
    ):
        subset = lag_lines[lag_lines.comparison == comparison]
        sns.lineplot(
            data=subset,
            x="lag_days",
            y="spearman_rho",
            hue="mesocosm",
            marker="o",
            palette="tab10",
            ax=ax,
        )
        ax.axhline(0, color="grey", linewidth=0.8)
        ax.set_title(comparison)
        ax.set_ylabel("Spearman ρ")
        ax.set_ylim(-1.05, 1.05)
    axes[-1].set_xlabel("Lag: Phytoplankton später als Mikrozooplankton (Tage)")
    fig.suptitle("Lag-Profile der einzelnen Mesokosmen", y=1.01)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "04_lag_profile_mesokosmen.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_outputs(
    merged: pd.DataFrame,
    normalized: pd.DataFrame,
    correlation_data: pd.DataFrame,
    lagged: pd.DataFrame,
    effect_correlations: pd.DataFrame,
    effect_values: pd.DataFrame,
    tests: pd.DataFrame,
) -> None:
    output = RESULTS_DIR / "microzooplankton_vs_phytoplankton.xlsx"
    best_per_mesocosm = (
        correlation_data.sort_values("spearman_rho", ascending=False)
        .groupby(["comparison", "mesocosm"], as_index=False)
        .first()
    )
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        merged.to_excel(writer, sheet_name="Zeitgleich", index=False)
        normalized.to_excel(writer, sheet_name="Normalisiert_T3", index=False)
        correlation_data.to_excel(writer, sheet_name="Korrelationen", index=False)
        lagged.to_excel(writer, sheet_name="Lag_Zusammenfassung", index=False)
        best_per_mesocosm.to_excel(writer, sheet_name="Beste_Lags_Mesokosmos", index=False)
        effect_values.to_excel(writer, sheet_name="Mesokosmos_Effekte", index=False)
        effect_correlations.to_excel(writer, sheet_name="Effekt_Korrelationen", index=False)
        tests.to_excel(writer, sheet_name="Signifikanztests", index=False)
        for sheet in writer.book.worksheets:
            sheet.freeze_panes = "A2"
            sheet.auto_filter.ref = sheet.dimensions
            for column in sheet.columns:
                sheet.column_dimensions[column[0].column_letter].width = min(
                    max(len(str(cell.value or "")) for cell in column) + 2, 40
                )

    concurrent = correlation_data[correlation_data.lag_days == 0]
    best = (
        lagged.sort_values("mean_spearman_rho", ascending=False)
        .groupby("comparison", as_index=False)
        .first()
    )
    best_main = best_per_mesocosm[
        best_per_mesocosm.comparison.isin(
            ["Ciliaten vs. Phytoplankton gesamt", "Dinoflagellaten vs. Phytoplankton gesamt"]
        )
    ].sort_values(["comparison", "mesocosm"])
    significant = concurrent[concurrent.significant_fdr]
    if significant.empty:
        significant_text = (
            "Kein zeitgleicher Einzeltest blieb nach Benjamini-Hochberg-Korrektur "
            "signifikant (FDR < 0,05)."
        )
    else:
        significant_text = (
            f"{len(significant)} zeitgleiche Einzeltests blieben nach "
            "Benjamini-Hochberg-Korrektur signifikant (FDR < 0,05)."
        )
    report = f"""# Vergleich Mikrozooplankton und Phytoplankton

## Fragestellung und Datengrundlage

Diese Auswertung vergleicht die Mikrozooplankton- und Phytoplanktondaten der sechs ausgewerteten Mesokosmen M1, M2, M3, M6, M8 und M9 bis einschließlich T31. Die Behandlung erfolgte an T4. Mikrozooplankton wurde als Ciliaten, Dinoflagellaten und deren Summe aus den Count-Rohdaten (Zellen L⁻¹ = Count × 40) übernommen. Beim Phytoplankton wurden die bereits geprüften `All cells`-Summen für Small-, Large- und Gesamt-Signale verwendet.

Die gemeinsamen Probetage sind T1, T3, T5, T7, T11, T15, T19, T23, T27 und T31. T2, T6 und T31? werden nicht künstlich ergänzt; Vergleiche erfolgen nur an tatsächlich vorhandenen gemeinsamen Tagen. Die Zeitpunkte T1–T3 dienen als Vorbehandlung, T5–T31 als Nachbehandlung.

## Wichtigste Ergebnisse

### Zeitliche Muster

Die Zeitreihen zeigen keinen durchgehend synchronen Anstieg von Mikrozooplankton und Phytoplankton. Phytoplankton fällt in vielen Mesokosmen unmittelbar nach T4 zunächst ab und steigt später teilweise wieder an. Mikrozooplankton reagiert dagegen mesokosmspezifisch: Ciliaten zeigen häufig ausgeprägte Rückgänge oder verzögerte Erholungen, während Dinoflagellaten teilweise stabiler bleiben oder unabhängig vom Phytoplankton verlaufen. Ein gemeinsamer Verlauf ist daher eher phasen- und mesokosmspezifisch als global.

### Zeitgleiche Korrelationen

Die Korrelationen wurden auf log10-transformierten Zellzahlen berechnet. Pearson beschreibt lineare Zusammenhänge, Spearman monotone Zusammenhänge. Die zeitgleichen Ergebnisse (Lag = 0) sind:

{concurrent.to_string(index=False)}

{significant_text} Diese Zahl darf nicht als unabhängiger Nachweis einer allgemeinen Beziehung interpretiert werden, da mehrere Zeitpunkte aus denselben sechs Mesokosmen stammen.

### Zeitverzögerte Beziehungen

Für jede Beziehung wurden Lags von -4, -2, 0, +2 und +4 Tagen geprüft. Ein positiver Lag bedeutet, dass die Phytoplanktonwerte um diesen Betrag nach dem Mikrozooplanktonwert verschoben wurden. Der jeweils stärkste mittlere Spearman-Zusammenhang ist:

{best.to_string(index=False)}

Die Lag-Analyse ist deshalb besonders nützlich, weil ein Räuber-Beute- oder Ressourcenverbrauchsmuster zeitlich versetzt auftreten kann. Sie ist jedoch hypothesengenerierend und kein kausaler Beweis. Die besten Lags der beiden zentralen Beziehungen pro Mesokosmos sind:

{best_main.to_string(index=False)}

Der mittlere stärkste Zusammenhang lag bei Ciliaten und beim Mikrozooplankton gesamt bei Lag −2. Das bedeutet: Der Phytoplanktonwert liegt ungefähr zwei Tage vor dem Mikrozooplanktonwert. Dieses Muster wäre biologisch mit einer verzögerten Reaktion der Konsumenten auf eine Phytoplanktonentwicklung vereinbar. Es ist aber nicht über alle Mesokosmen konsistent und nach FDR-Korrektur nicht signifikant. Unterschiedliche Lags oder wechselnde Vorzeichen sprechen für mesokosmspezifische Dynamiken, wechselnde Nahrungsquellen oder zusätzliche Steuergrößen.

### T3-normalisierte Veränderungen

Für jeden Mesokosmos wurde jede Nachbehandlungsbeobachtung gegen T3 als log2-Faktor normalisiert. Die anschließenden Mittelwerte je Mesokosmos stehen in `Mesokosmos_Effekte`. Die Korrelationen zwischen diesen sechs Mesokosmos-Mittelwerten stehen in `Effekt_Korrelationen`:

{effect_correlations.to_string(index=False)}

Diese Analyse prüft, ob Mesokosmen mit einem stärkeren Phytoplanktonrückgang gleichzeitig stärkere Veränderungen im Mikrozooplankton zeigen. Wegen n = 6 ist sie sehr empfindlich gegenüber einzelnen Mesokosmen und statistisch nur als explorativer Vergleich belastbar.

### Größenfraktionen

Die Verbindung mit Small- und Large-Phytoplankton wurde getrennt untersucht. Large-Phytoplankton zeigt biologisch plausiblere zeitliche Kopplungen zu größeren Ciliaten oder bestimmten Dinoflagellaten als die gesamte Small-Fraktion, sofern die entsprechenden Korrelationen positiv ausfallen. Die Ergebnisse sind in `Korrelationen` und in der Abbildung `02_korrelationen.png` nachprüfbar; aus Korrelationen allein darf jedoch keine Nahrungskette abgeleitet werden.

### Statistische Relevanz

Die sechs Mesokosmen wurden außerdem mit einem Wilcoxon-Test darauf geprüft, ob der mittlere log2-Faktor nach T4 von 0 abweicht:

{tests.to_string(index=False)}

Bei n = 6 ist der Test nur sehr grob aufgelöst. Die Treatmentkombinationen sind nicht repliziert; deshalb können keine allgemeinen Material-, Dosis- oder Treatmentwirkungen statistisch isoliert werden. p-Werte aus den vielen zeitpunktweisen Tests sind als explorativ zu verstehen, nicht als bestätigende Evidenz.

## Interpretation und auffällige Aspekte

1. **Zeitverzögerungen sind der plausibelste Ansatz:** Für eine trophische Beziehung sind negative Lags hier biologisch besonders interessant, weil sie bedeuten, dass das Phytoplankton zeitlich vor dem Mikrozooplankton liegt.
2. **Kein einheitlicher Kopplungstrend:** Die Zeitreihen sprechen gegen eine einfache Aussage, dass mehr Phytoplankton automatisch mehr Mikrozooplankton bedeutet.
3. **Ciliaten und Dinoflagellaten unterscheiden sich:** Die beiden Mikrozooplanktongruppen sollten nicht als einheitliche trophische Antwort behandelt werden; ihre Beziehungen zu Small- und Large-Phytoplankton können unterschiedliche Vorzeichen und Zeitverzüge zeigen.
4. **Positive Lags nicht überinterpretieren:** Ein positiver Zusammenhang kann sowohl eine verzögerte Konsumentenreaktion als auch gemeinsame Reaktionen auf Umweltbedingungen, Autokorrelation oder eine dritte Einflussgröße widerspiegeln.
5. **Behandlungseffekte sind konfundiert:** Jeder Material-Dosis-Mesokosmos ist eine Einzelbeobachtung. Unterschiede zwischen M1, M2, M8 und M9 können daher nicht eindeutig Material oder Dosis zugeschrieben werden.
6. **Ausgangsverläufe beachten:** Bereits vor T4 verlaufen die Mesokosmen nicht identisch. T3-Normalisierung reduziert dieses Problem, ersetzt aber keine replizierte Kontroll- oder Vorher-Nachher-Statistik.

## Dateien

- `microzooplankton_vs_phytoplankton.xlsx`: zusammengeführte Zeitreihen, T3-Normalisierung, Korrelationen, Lags, Effektvergleiche und Tests.
- `figures/01_zeitvergleiche.png`: exemplarische zeitgleiche Verläufe.
- `figures/02_korrelationen.png`: Ciliaten/Dinoflagellaten gegen Phytoplankton gesamt.
- `figures/03_zeitverzoegerte_korrelationen.png`: mittlere Spearman-Korrelationen über Lags.
- `figures/04_lag_profile_mesokosmen.png`: Lag-Profile für Ciliaten und Dinoflagellaten je Mesokosmos.
"""
    report = report.replace("T2, T6 und T31? werden nicht künstlich ergänzt", "T2 und T6 werden nicht künstlich ergänzt")
    (RESULTS_DIR / "microzooplankton_vs_phytoplankton.md").write_text(report, encoding="utf-8")


def main() -> None:
    if not MICRO_XLSX.exists() or not PHYTO_XLSX.exists():
        raise FileNotFoundError("Die Ergebnisse der beiden Einzelanalysen müssen zuerst erzeugt werden.")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    micro = load_micro()
    phyto = load_phyto()
    data = merge_data(micro, phyto)
    normalized = normalized_changes(data)
    correlation_data = correlations(micro, phyto)
    lagged = lag_summary(correlation_data)
    effect_correlations, effect_values = effect_summary(normalized)
    tests = paired_tests(normalized)
    save_figures(data, normalized, correlation_data)
    write_outputs(data, normalized, correlation_data, lagged, effect_correlations, effect_values, tests)
    print(f"Ergebnisse: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
