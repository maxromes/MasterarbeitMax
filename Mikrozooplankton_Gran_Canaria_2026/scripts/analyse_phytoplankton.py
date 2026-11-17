from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


PROJECT_DIR = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_DIR / "concatenated_file_2026_GC_M1_M2_M3_M6_M8_M9_T31.csv"
RESULTS_DIR = PROJECT_DIR / "results" / "phytoplankton_analysis"
FIGURES_DIR = RESULTS_DIR / "figures"
MESOCOSMS = [1, 2, 3, 6, 8, 9]
CONTROL_MESOCOSMS = [3, 6]
SAMPLE_DAYS = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31]
SIGNAL_SETS = {
    "Picophytoplankton (other)",
    "Synechococcus right",
    "high SSC (pico)",
    "Nanophytoplankton (other)",
    "Nanophytoplankton 2 (FL-orange)",
    "Cryptophyites",
    "long chain-forming Diatoms",
    "Chain-forming Microphytoplankton",
    "short chain-forming microphytoplankton",
    "Ciliates_dinoflagellates",
}


def load_data() -> pd.DataFrame:
    data = pd.read_csv(SOURCE)
    data = data[
        data.Mesocosm.isin(MESOCOSMS) & data.Day.isin(SAMPLE_DAYS)
    ].copy()
    data["concentration_n_L"] = pd.to_numeric(
        data["Concentration [n/µl]"], errors="coerce"
    ) * 1000
    data["count"] = pd.to_numeric(data["Count"], errors="coerce").fillna(0)
    data[["dose", "material"]] = data["Treat_Meso"].str.extract(
        r"(?P<dose>\d+)\s*/\s*(?P<material>Concrete|NaOH)"
    )
    data["dose"] = data.dose.astype(int)
    data["control"] = data.Mesocosm.isin(CONTROL_MESOCOSMS)
    data["treatment_group"] = np.where(
        data.control,
        "Kontrolle",
        data.dose.astype(str) + " " + data.material,
    )
    data["phase"] = np.where(data.Day <= 3, "Vorbehandlung", "Nachbehandlung")
    data["is_total"] = data.Set.eq("All cells")
    data["is_signal"] = data.Set.isin(SIGNAL_SETS)
    return data


def totals(data: pd.DataFrame) -> pd.DataFrame:
    result = (
        data[data.is_total]
        .groupby(
            ["Mesocosm", "Day", "treatment_group", "dose", "material", "control"],
            as_index=False,
        )
        .agg(
            small_cells_L=("concentration_n_L", lambda x: x[data.loc[x.index, "Settings"].eq("small")].sum()),
            large_cells_L=("concentration_n_L", lambda x: x[data.loc[x.index, "Settings"].eq("large")].sum()),
            total_cells_L=("concentration_n_L", "sum"),
        )
    )
    return result.sort_values(["Mesocosm", "Day"])


def signals(data: pd.DataFrame) -> pd.DataFrame:
    signal = data[data.is_signal].copy()
    result = (
        signal.groupby(
            ["Mesocosm", "Day", "Set", "treatment_group", "dose", "material", "control"],
            as_index=False,
        )
        .agg(cells_L=("concentration_n_L", "sum"), count=("count", "sum"))
    )
    totals_signal = result.groupby(["Mesocosm", "Day"], as_index=False).cells_L.sum().rename(
        columns={"cells_L": "selected_signal_cells_L"}
    )
    result = result.merge(totals_signal, on=["Mesocosm", "Day"], validate="many_to_one")
    result["signal_share"] = result.cells_L / result.selected_signal_cells_L.replace(0, np.nan)
    return result


def pretrend(total: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mesocosm, frame in total.groupby("Mesocosm"):
        frame = frame[frame.Day <= 3].sort_values("Day")
        slope = np.polyfit(frame.Day, np.log10(frame.total_cells_L + 1), 1)[0]
        rows.append(
            {
                "mesocosm": mesocosm,
                "treatment": frame.treatment_group.iloc[0],
                "T1_cells_L": frame.loc[frame.Day == 1, "total_cells_L"].iloc[0],
                "T3_cells_L": frame.loc[frame.Day == 3, "total_cells_L"].iloc[0],
                "slope_log10_cells_per_day": slope,
                "direction": "Anstieg" if slope > 0 else "Abnahme",
            }
        )
    return pd.DataFrame(rows)


def normalized_effects(total: pd.DataFrame) -> pd.DataFrame:
    baseline = total[total.Day == 3][["Mesocosm", "total_cells_L"]].rename(
        columns={"total_cells_L": "T3_cells_L"}
    )
    result = total[total.Day >= 5].merge(baseline, on="Mesocosm", validate="many_to_one")
    result["percent_change_vs_T3"] = (
        (result.total_cells_L - result.T3_cells_L) / result.T3_cells_L * 100
    )
    result["log2_change_vs_T3"] = np.log2(
        (result.total_cells_L + 1) / (result.T3_cells_L + 1)
    )
    return result


def auc_minimum(total: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mesocosm, frame in total[total.Day >= 5].groupby("Mesocosm"):
        minimum = frame.loc[frame.total_cells_L.idxmin()]
        rows.append(
            {
                "mesocosm": mesocosm,
                "treatment": frame.treatment_group.iloc[0],
                "post_auc_cells_day_L": np.trapezoid(frame.total_cells_L, frame.Day),
                "minimum_cells_L": minimum.total_cells_L,
                "minimum_day": minimum.Day,
                "T31_cells_L": frame.loc[frame.Day == 31, "total_cells_L"].iloc[0],
            }
        )
    return pd.DataFrame(rows)


def control_effects(total: pd.DataFrame) -> pd.DataFrame:
    control_for_material = {"Concrete": 3, "NaOH": 6}
    rows = []
    for mesocosm, frame in total.groupby("Mesocosm"):
        if frame.dose.iloc[0] == 0:
            continue
        control = total[total.Mesocosm == control_for_material[frame.material.iloc[0]]]
        for day in SAMPLE_DAYS:
            treatment_value = frame.loc[frame.Day == day, "total_cells_L"].iloc[0]
            control_value = control.loc[control.Day == day, "total_cells_L"].iloc[0]
            rows.append(
                {
                    "mesocosm": mesocosm,
                    "treatment": frame.treatment_group.iloc[0],
                    "sample_day": day,
                    "control_mesocosm": int(control.Mesocosm.iloc[0]),
                    "treatment_cells_L": treatment_value,
                    "control_cells_L": control_value,
                    "difference_cells_L": treatment_value - control_value,
                    "ratio_treatment_control": treatment_value / control_value
                    if control_value
                    else np.nan,
                }
            )
    return pd.DataFrame(rows)


def similarity(total: pd.DataFrame, signal: pd.DataFrame) -> pd.DataFrame:
    composition = signal.pivot_table(
        index=["Mesocosm", "Day"], columns="Set", values="signal_share", fill_value=0
    ).reset_index()
    rows = []
    for day in SAMPLE_DAYS:
        counts = total[total.Day == day].total_cells_L
        profile = composition[composition.Day == day].drop(columns=["Mesocosm", "Day"])
        rows.append(
            {
                "sample_day": day,
                "mean_total_cells_L": counts.mean(),
                "cv_total_cells": counts.std(ddof=1) / counts.mean(),
                "min_total_cells_L": counts.min(),
                "max_total_cells_L": counts.max(),
                "mean_signal_profile_sd": profile.std(axis=0, ddof=1).mean(),
                "max_signal_profile_sd": profile.std(axis=0, ddof=1).max(),
            }
        )
    return pd.DataFrame(rows)


def save_figures(data: pd.DataFrame, total: pd.DataFrame, signal: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid", context="notebook")
    palette = {
        "300 Concrete": "#0072B2",
        "500 NaOH": "#D55E00",
        "Kontrolle": "#009E73",
        "300 NaOH": "#CC79A7",
        "500 Concrete": "#E69F00",
    }
    fig, axes = plt.subplots(2, 1, figsize=(11, 9), sharex=True)
    for ax, settings, title in zip(
        axes, ["small", "large"], ["Small-Signal", "Large-Signal"]
    ):
        plot_data = total.copy()
        plot_data["cells_L"] = np.where(
            settings == "small", plot_data.small_cells_L, plot_data.large_cells_L
        )
        sns.lineplot(
            data=plot_data,
            x="Day",
            y="cells_L",
            hue="treatment_group",
            style="Mesocosm",
            markers=True,
            dashes=False,
            palette=palette,
            ax=ax,
        )
        ax.axvline(4, color="black", linestyle="--")
        ax.set_yscale("log")
        ax.set_title(title)
        ax.set_ylabel("Zellen L$^{-1}$")
        ax.legend(title="Treatment / M", bbox_to_anchor=(1.01, 1), loc="upper left")
    axes[-1].set_xlabel("Probetag")
    fig.suptitle("Phytoplankton: zeitlicher Verlauf", y=1.01)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "01_zeitverlauf.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 6))
    signal_data = signal[signal.Set.isin(SIGNAL_SETS)]
    top = signal_data.groupby("Set").cells_L.sum().nlargest(8).index
    signal_data = signal_data[signal_data.Set.isin(top)]
    sns.lineplot(
        data=signal_data,
        x="Day",
        y="cells_L",
        hue="Set",
        style="Mesocosm",
        markers=True,
        dashes=False,
        ax=ax,
    )
    ax.axvline(4, color="black", linestyle="--")
    ax.set_yscale("log")
    ax.set_title("Häufigste spezifische Phytoplankton-Signale")
    ax.set_xlabel("Probetag")
    ax.set_ylabel("Zellen L$^{-1}$")
    ax.legend(title="Signal / M", bbox_to_anchor=(1.01, 1), loc="upper left")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "02_signale.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    short_chain = (
        data[
            (data.Set == "short chain-forming microphytoplankton")
            & data.Settings.eq("large")
        ]
        .groupby(["Mesocosm", "Day", "treatment_group"], as_index=False)
        .agg(cells_L=("concentration_n_L", "sum"))
    )
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.lineplot(
        data=short_chain,
        x="Day",
        y="cells_L",
        hue="treatment_group",
        style="Mesocosm",
        markers=True,
        dashes=False,
        linewidth=1.8,
        palette=palette,
        ax=ax,
    )
    ax.axvline(4, color="black", linestyle="--", linewidth=1)
    ax.set_yscale("log")
    ax.set_title("Short chain-forming microphytoplankton (large particles)")
    ax.set_xlabel("Probetag")
    ax.set_ylabel("Zellen L$^{-1}$")
    ax.legend(title="Treatment / M", bbox_to_anchor=(1.01, 1), loc="upper left")
    fig.tight_layout()
    fig.savefig(
        FIGURES_DIR / "03_short_chain_forming_microphytoplankton_large.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)

    short_chain_chla = data[
        (data.Set == "short chain-forming microphytoplankton")
        & data.Settings.eq("large")
    ].copy()
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.lineplot(
        data=short_chain_chla,
        x="Day",
        y="ChlaProxyRaw",
        hue="treatment_group",
        style="Mesocosm",
        markers=True,
        dashes=False,
        linewidth=1.8,
        palette=palette,
        ax=ax,
    )
    ax.axvline(4, color="black", linestyle="--", linewidth=1)
    ax.set_yscale("log")
    ax.set_title("Short chain-forming microphytoplankton (large particles)")
    ax.set_xlabel("Probetag")
    ax.set_ylabel("Chlorophyll proxy (ChlaProxyRaw)")
    ax.legend(title="Treatment / M", bbox_to_anchor=(1.01, 1), loc="upper left")
    fig.tight_layout()
    fig.savefig(
        FIGURES_DIR / "04_short_chain_forming_microphytoplankton_large_chlorophyll_proxy.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)


def write_outputs(
    data: pd.DataFrame,
    total: pd.DataFrame,
    signal: pd.DataFrame,
    trend: pd.DataFrame,
    effects: pd.DataFrame,
    auc: pd.DataFrame,
    control: pd.DataFrame,
    similarity_data: pd.DataFrame,
) -> None:
    signal_summary = (
        signal.groupby("Set", as_index=False)
        .agg(
            total_cells_L=("cells_L", "sum"),
            samples_with_signal=("cells_L", lambda x: int((x > 0).sum())),
            mean_share=("signal_share", "mean"),
        )
        .sort_values("total_cells_L", ascending=False)
    )
    output = RESULTS_DIR / "phytoplankton_analysis.xlsx"
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        data.to_excel(writer, sheet_name="Rohdaten", index=False)
        total.to_excel(writer, sheet_name="Gesamtverlauf", index=False)
        signal.to_excel(writer, sheet_name="Signalgruppen", index=False)
        trend.to_excel(writer, sheet_name="Vorbehandlung", index=False)
        effects.to_excel(writer, sheet_name="Treatment_gegen_T3", index=False)
        auc.to_excel(writer, sheet_name="AUC_Minimum", index=False)
        control.to_excel(writer, sheet_name="Kontrollbasierte_Effekte", index=False)
        signal_summary.to_excel(writer, sheet_name="Signalzusammenfassung", index=False)
        similarity_data.to_excel(writer, sheet_name="Aehnlichkeit_Zeitverlauf", index=False)
        for sheet in writer.book.worksheets:
            sheet.freeze_panes = "A2"
            sheet.auto_filter.ref = sheet.dimensions
            for column in sheet.columns:
                sheet.column_dimensions[column[0].column_letter].width = min(
                    max(len(str(cell.value or "")) for cell in column) + 2, 42
                )

    directions = trend.direction.value_counts().to_dict()
    pre = similarity_data[similarity_data.sample_day <= 3]
    post = similarity_data[similarity_data.sample_day >= 5]
    top = signal_summary.head(8).to_string(index=False)
    effect_table = effects.groupby("Mesocosm", as_index=False).agg(
        treatment=("treatment_group", "first"),
        mean_post_cells_L=("total_cells_L", "mean"),
        T31_cells_L=("total_cells_L", "last"),
        mean_change_vs_T3=("percent_change_vs_T3", "mean"),
    ).to_string(index=False)
    control_table = control.groupby("mesocosm", as_index=False).agg(
        treatment=("treatment", "first"),
        mean_ratio_treatment_control=("ratio_treatment_control", "mean"),
        mean_difference_cells_L=("difference_cells_L", "mean"),
    ).to_string(index=False)
    report = f"""# Phytoplanktonanalyse

## Datengrundlage

Die Auswertung wurde aus `{SOURCE.name}` erstellt. Berücksichtigt wurden M1, M2, M3, M6, M8 und M9 sowie die Probetage T1 bis T31 (ungerade Probetage; T4 ist der Behandlungstag und wurde nicht gemessen). Die Flow-Cytometrie enthält pro Probe eine `small`- und eine `large`-Messung.

Für die Gesamtzellzahl wurden ausschließlich die beiden `All cells`-Zeilen verwendet und zu Zellen L⁻¹ addiert. Die spezifischen Signalgruppen wurden getrennt ausgewertet. Aggregierte Zeilen wie `All cells Not Microphytoplankton total`, `Microphytoplankton total` oder `Nanophytoplankyon_total` wurden nicht zu den spezifischen Signalgruppen addiert, um Doppelzählungen zu vermeiden. Die Phytoplankton-Komposition bezieht sich deshalb auf die ausgewählten spezifischen Signale und nicht auf eine künstlich geschlossene taxonomische Summe.

## Ergebnisse

### Genereller Verlauf und Vorbehandlung

Vor T4 zeigten **{directions.get("Anstieg", 0)} von 6 Mesokosmen einen Anstieg** und **{directions.get("Abnahme", 0)} eine Abnahme** der Gesamtzellzahl. Die Ausgangsentwicklung war daher nicht vollständig synchron.

### Deskriptive Treatment-Effekte

Die folgenden Werte sind deskriptive Muster trotz fehlender Replikate:

{effect_table}

M2 (500 NaOH) und M1 (300 Concrete) werden ebenso wie die Kontrollen und die übrigen Treatments einzeln berichtet. Die Treatmentkombinationen sind nicht unabhängig repliziert; Unterschiede dürfen daher nicht als allgemeine statistische Dosis- oder Materialeffekte verallgemeinert werden.

### AUC und Minimum

Die AUC fasst die gesamte Nachbehandlungszellzahl von T5 bis T31 zusammen. `AUC_Minimum` enthält außerdem den Zeitpunkt und die Größe des Minimums.

{auc.to_string(index=False)}

### Kontrollbasierte Effekte

Die Treatments wurden zusätzlich gegen die jeweils passende Kontrolle verglichen (Concrete gegen M3, NaOH gegen M6). Ein Verhältnis über 1 bedeutet höhere Gesamtzellzahlen im Treatment:

{control_table}

### Spezifische Signalgruppen

Die häufigsten ausgewerteten spezifischen Signale waren:

{top}

Diese Signalgruppen sind durch das Messverfahren definiert und teilweise nicht als vollständig exklusive biologische Taxa zu interpretieren. Die vollständigen Einzelverläufe stehen im Blatt `Signalgruppen`.

### Ähnlichkeit: Zellzahlen oder Komposition?

Die absolute Gesamtzellzahl wurde über den Variationskoeffizienten zwischen Mesokosmen verglichen. Die Komposition wurde über die Streuung der Anteile der spezifischen Signalgruppen verglichen.

Vor T4 betrug der mittlere CV der Gesamtzellzahl **{pre.cv_total_cells.mean():.1%}**. Die mittlere Standardabweichung der Signalprofile lag bei **{pre.mean_signal_profile_sd.mean():.3f}**. Nach T4 lag der CV der Gesamtzellzahl im Mittel bei **{post.cv_total_cells.mean():.1%}**, während die mittlere Profilstreuung **{post.mean_signal_profile_sd.mean():.3f}** betrug. Die vollständige Zeitreihe befindet sich im Blatt `Aehnlichkeit_Zeitverlauf`.

## Einschränkungen

Jede Treatmentkombination ist nur durch einen Mesokosmos repräsentiert. Die Ergebnisse sind deshalb deskriptive Verläufe und Effektmuster. Zusätzlich unterscheiden sich die Flow-Cytometrie-Signalgruppen von vollständig taxonomischen Zählkategorien; aggregierte Signale wurden daher nicht mit ihren Untergruppen zusammenaddiert.

## Dateien

- `phytoplankton_analysis.xlsx`: Rohdaten, Gesamtverlauf, Signalgruppen, Vorbehandlung, Treatments, AUC, Kontrollen und Ähnlichkeitsvergleich.
- `figures/01_zeitverlauf.png`: Small- und Large-Signalverläufe.
- `figures/02_signale.png`: häufigste spezifische Signalgruppen.
"""
    (RESULTS_DIR / "phytoplankton_analysis.md").write_text(report, encoding="utf-8")


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    data = load_data()
    total = totals(data)
    signal = signals(data)
    trend = pretrend(total)
    effects = normalized_effects(total)
    auc = auc_minimum(total)
    control = control_effects(total)
    similarity_data = similarity(total, signal)
    save_figures(data, total, signal)
    write_outputs(data, total, signal, trend, effects, auc, control, similarity_data)
    print(f"Ergebnisse: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
