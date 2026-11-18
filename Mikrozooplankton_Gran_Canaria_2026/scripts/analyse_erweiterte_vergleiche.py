from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import spearmanr
from statsmodels.stats.multitest import multipletests


PROJECT_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_DIR / "results"
MICRO_XLSX = RESULTS_DIR / "microzooplankton_analysis" / "microzooplankton_analysis.xlsx"
PHYTO_XLSX = RESULTS_DIR / "phytoplankton_analysis" / "phytoplankton_analysis.xlsx"
COMPARISON_DIR = RESULTS_DIR / "microzooplankton_vs_phytoplankton"
COMPARISON_XLSX = COMPARISON_DIR / "microzooplankton_vs_phytoplankton.xlsx"
REPORT_DIR = RESULTS_DIR / "report_documents"
FIGURES_DIR = REPORT_DIR / "figures"
MESOCOSMS = [1, 2, 3, 6, 8, 9]
COMMON_DAYS = [1, 3, 5, 7, 11, 15, 19, 23, 27, 31]
CONTROL = { "concrete": 3, "naoh": 6 }
TREATMENT_COLORS = {"Concrete": "#0072B2", "NaOH": "#D55E00", "Kontrolle": "#555555"}
MARKERS = {"Kontrolle": "o", "300": "^", "500": "s"}


def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    micro = pd.read_excel(MICRO_XLSX, sheet_name="Gruppenverlauf")
    micro = micro[micro.mesocosm.isin(MESOCOSMS)].pivot_table(
        index=["mesocosm", "sample_day", "treatment_group", "material", "dose"],
        columns="group", values="cells_L", aggfunc="sum"
    ).reset_index()
    micro = micro.rename(columns={
        "sample_day": "day", "Ciliate": "ciliate", "Dinoflagellate": "dinoflagellate"
    })
    micro["micro_total"] = micro["ciliate"] + micro["dinoflagellate"]

    phyto = pd.read_excel(PHYTO_XLSX, sheet_name="Gesamtverlauf")
    phyto = phyto.rename(columns={
        "Mesocosm": "mesocosm", "Day": "day", "total_cells_L": "phyto_total",
        "small_cells_L": "phyto_small", "large_cells_L": "phyto_large"
    })
    phyto = phyto[phyto.mesocosm.isin(MESOCOSMS)][
        ["mesocosm", "day", "phyto_total", "phyto_small", "phyto_large"]
    ]
    data = micro.merge(phyto, on=["mesocosm", "day"], validate="one_to_one")
    data["material"] = data["material"].str.title()
    data["material"] = data["material"].replace({"Concrete": "Concrete", "Naoh": "NaOH"})
    data["dose_label"] = np.where(data.dose == 0, "Kontrolle", data.dose.astype(str))
    data["phase"] = np.where(data.day <= 3, "Vorbehandlung",
                             np.where(data.day <= 7, "Fruhe Nachbehandlung",
                                      np.where(data.day <= 15, "Mittlere Nachbehandlung", "Spate Nachbehandlung")))
    data["micro_phyto_ratio"] = data["micro_total"] / data["phyto_total"].replace(0, np.nan)
    data["ciliate_phyto_ratio"] = data["ciliate"] / data["phyto_total"].replace(0, np.nan)
    data["dino_phyto_ratio"] = data["dinoflagellate"] / data["phyto_total"].replace(0, np.nan)
    return data, micro


def control_corrected(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mesocosm, frame in data.groupby("mesocosm"):
        if mesocosm in (3, 6):
            continue
        material = str(frame.material.iloc[0]).lower()
        control_meso = CONTROL[material]
        control = data[data.mesocosm == control_meso]
        for day in frame.day:
            treatment_row = frame[frame.day == day]
            control_row = control[control.day == day]
            if treatment_row.empty or control_row.empty:
                continue
            result = {"mesocosm": mesocosm, "treatment": treatment_row.treatment_group.iloc[0],
                      "control_mesocosm": control_meso, "day": day}
            for variable in ["micro_total", "ciliate", "dinoflagellate",
                             "phyto_total", "phyto_small", "phyto_large"]:
                treatment = float(treatment_row[variable].iloc[0])
                control_value = float(control_row[variable].iloc[0])
                result[f"{variable}_treatment"] = treatment
                result[f"{variable}_control"] = control_value
                result[f"log2_{variable}_vs_control"] = np.log2((treatment + 1) / (control_value + 1))
            rows.append(result)
    return pd.DataFrame(rows)


def ratios_and_phases(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    ratio = data.copy()
    phase_rows = []
    for phase, frame in data.groupby("phase"):
        for x, y, label in [
            ("phyto_total", "micro_total", "Mikrozooplankton gesamt vs. Phytoplankton gesamt"),
            ("phyto_total", "ciliate", "Ciliaten vs. Phytoplankton gesamt"),
            ("phyto_total", "dinoflagellate", "Dinoflagellaten vs. Phytoplankton gesamt"),
            ("phyto_small", "ciliate", "Ciliaten vs. Small-Phytoplankton"),
            ("phyto_large", "ciliate", "Ciliaten vs. Large-Phytoplankton"),
        ]:
            for mesocosm, pair in frame.groupby("mesocosm"):
                pair = pair[[x, y]].replace(0, np.nan).dropna()
                if len(pair) < 3:
                    continue
                rho, p = spearmanr(np.log10(pair[x] + 1), np.log10(pair[y] + 1))
                phase_rows.append({"phase": phase, "comparison": label, "mesocosm": mesocosm,
                                   "n_pairs": len(pair), "spearman_rho": rho, "spearman_p": p})
    phase = pd.DataFrame(phase_rows)
    if not phase.empty:
        valid = phase.spearman_p.notna()
        phase.loc[valid, "spearman_p_fdr"] = multipletests(phase.loc[valid, "spearman_p"], method="fdr_bh")[1]
    return ratio, phase


def size_and_lag_correlations(data: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    micro_sizes = pd.read_excel(MICRO_XLSX, sheet_name="Groessenklassen")
    micro_sizes = micro_sizes[micro_sizes.mesocosm.isin(MESOCOSMS)]
    micro_sizes = micro_sizes.groupby(
        ["mesocosm", "sample_day", "group", "size_class"], as_index=False
    ).cells_L.sum()
    micro_sizes = micro_sizes.pivot_table(
        index=["mesocosm", "sample_day"], columns=["group", "size_class"],
        values="cells_L", aggfunc="sum"
    )
    micro_sizes.columns = [f"micro_{group.lower()}_{size.replace('<', 'lt').replace('>', 'gt')}" for group, size in micro_sizes.columns]
    micro_sizes = micro_sizes.reset_index().rename(columns={"sample_day": "day"})
    combined = micro_sizes.merge(
        data[["mesocosm", "day", "phyto_total", "phyto_small", "phyto_large"]].drop_duplicates(),
        on=["mesocosm", "day"], validate="one_to_one"
    )

    size_rows = []
    for lag in [-4, -2, 0, 2, 4]:
        for micro_col in ["micro_ciliate_lt30", "micro_ciliate_gt30",
                          "micro_dinoflagellate_lt30", "micro_dinoflagellate_gt30"]:
            for phyto_col, phyto_label in [
                ("phyto_small", "Small"), ("phyto_large", "Large"), ("phyto_total", "Gesamt")
            ]:
                for mesocosm, frame in combined.groupby("mesocosm"):
                    left = frame[["day", micro_col]].rename(columns={micro_col: "x"})
                    right = frame[["day", phyto_col]].rename(columns={phyto_col: "y"}).copy()
                    right["day"] = right["day"] - lag
                    pair = left.merge(right, on="day").replace(0, np.nan).dropna()
                    if len(pair) < 3:
                        continue
                    rho, p = spearmanr(np.log10(pair.x + 1), np.log10(pair.y + 1))
                    size_rows.append({
                        "micro_group": micro_col, "phyto_group": phyto_label,
                        "mesocosm": mesocosm, "lag_days": lag,
                        "n_pairs": len(pair), "spearman_rho": rho, "spearman_p": p
                    })
    size = pd.DataFrame(size_rows)
    size_summary = size.groupby(["micro_group", "phyto_group", "lag_days"], as_index=False).agg(
        n_mesocosms=("mesocosm", "count"),
        mean_spearman_rho=("spearman_rho", "mean"),
        median_spearman_rho=("spearman_rho", "median")
    )
    return size, size_summary


def signal_correlations(data: pd.DataFrame) -> pd.DataFrame:
    signals = pd.read_excel(PHYTO_XLSX, sheet_name="Signalgruppen")
    signals = signals[signals.Mesocosm.isin(MESOCOSMS)]
    signals = signals[~signals.Set.isin(["Ciliates_dinoflagellates"])]
    wide = signals.pivot_table(
        index=["Mesocosm", "Day"], columns="Set", values="cells_L", aggfunc="sum"
    ).reset_index().rename(columns={"Mesocosm": "mesocosm", "Day": "day"})
    combined = data.merge(wide, on=["mesocosm", "day"], validate="one_to_one")
    rows = []
    signal_columns = [column for column in wide.columns if column not in ("mesocosm", "day")]
    for signal in signal_columns:
        for micro_col, micro_label in [
            ("micro_total", "Mikrozooplankton gesamt"),
            ("ciliate", "Ciliaten"),
            ("dinoflagellate", "Dinoflagellaten")
        ]:
            rho, p = spearmanr(
                np.log10(combined[micro_col] + 1),
                np.log10(combined[signal].fillna(0) + 1)
            )
            rows.append({"micro_group": micro_label, "phyto_signal": signal,
                         "n_pairs": len(combined), "spearman_rho": rho, "spearman_p": p})
    return pd.DataFrame(rows)


def peak_recovery(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mesocosm, frame in data.groupby("mesocosm"):
        post = frame[frame.day >= 5].sort_values("day")
        for organism, column in [
            ("Mikrozooplankton gesamt", "micro_total"),
            ("Ciliaten", "ciliate"),
            ("Dinoflagellaten", "dinoflagellate"),
            ("Phytoplankton gesamt", "phyto_total")
        ]:
            minimum = post.loc[post[column].idxmin()]
            maximum = post.loc[post[column].idxmax()]
            rows.append({
                "mesocosm": mesocosm,
                "treatment": frame.treatment_group.iloc[0],
                "organism": organism,
                "minimum_day": int(minimum.day),
                "minimum_cells_L": float(minimum[column]),
                "maximum_day": int(maximum.day),
                "maximum_cells_L": float(maximum[column]),
            })
    return pd.DataFrame(rows)


def difference_in_differences(data: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mesocosm, frame in data.groupby("mesocosm"):
        if mesocosm in (3, 6):
            continue
        material = str(frame.material.iloc[0]).lower()
        control_meso = CONTROL[material]
        control = data[data.mesocosm == control_meso]
        for variable in ["micro_total", "ciliate", "dinoflagellate", "phyto_total", "phyto_small", "phyto_large"]:
            treatment_pre = np.log2(frame[frame.day <= 3][variable].mean() + 1)
            treatment_post = np.log2(frame[frame.day >= 5][variable].mean() + 1)
            control_pre = np.log2(control[control.day <= 3][variable].mean() + 1)
            control_post = np.log2(control[control.day >= 5][variable].mean() + 1)
            rows.append({
                "mesocosm": mesocosm,
                "treatment": frame.treatment_group.iloc[0],
                "control_mesocosm": control_meso,
                "variable": variable,
                "did_log2_change": (treatment_post - treatment_pre) - (control_post - control_pre)
            })
    return pd.DataFrame(rows)


def bootstrap_lag_summary(existing_comparison: pd.DataFrame) -> pd.DataFrame:
    selected = existing_comparison[
        existing_comparison.comparison.isin([
            "Ciliaten vs. Phytoplankton gesamt",
            "Dinoflagellaten vs. Phytoplankton gesamt",
            "Mikrozooplankton gesamt vs. Phytoplankton gesamt"
        ])
    ].copy()
    rng = np.random.default_rng(2026)
    rows = []
    for comparison, frame in selected.groupby("comparison"):
        for lag, lag_frame in frame.groupby("lag_days"):
            values = lag_frame.spearman_rho.dropna().to_numpy()
            if len(values) == 0:
                continue
            estimates = [
                rng.choice(values, size=len(values), replace=True).mean()
                for _ in range(2000)
            ]
            rows.append({
                "comparison": comparison,
                "lag_days": lag,
                "mean_spearman_rho": float(values.mean()),
                "bootstrap_low_95": float(np.quantile(estimates, 0.025)),
                "bootstrap_high_95": float(np.quantile(estimates, 0.975))
            })
    return pd.DataFrame(rows)


def treatment_style(row):
    if row.dose_label == "Kontrolle":
        return TREATMENT_COLORS["Kontrolle"], "o"
    return TREATMENT_COLORS[row.material], MARKERS[row.dose_label]


def plot_control_corrected(control: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
    for ax, variable, title in [
        (axes[0], "micro_total", "Mikrozooplankton gegen passende Kontrolle"),
        (axes[1], "phyto_total", "Phytoplankton gegen passende Kontrolle")
    ]:
        column = f"log2_{variable}_vs_control"
        for mesocosm, frame in control.groupby("mesocosm"):
            treatment = frame.treatment.iloc[0]
            material = "Concrete" if "concrete" in treatment.lower() else "NaOH"
            dose = "Kontrolle" if "kontrolle" in treatment.lower() else treatment.split()[0]
            ax.plot(frame.day, frame[column], color=TREATMENT_COLORS[material],
                    marker=MARKERS[dose], linewidth=1.8, markersize=7)
        ax.axhline(0, color="#555555", linestyle="-", linewidth=0.8)
        ax.axvline(4, color="black", linestyle="--", linewidth=1)
        ax.set_ylabel("log2(Treatment / Kontrolle)")
        ax.set_title(title)
    axes[-1].set_xlabel("Probetag")
    handles = [
        plt.Line2D([0], [0], color="#0072B2", marker="^", linestyle="-", label="300 Concrete"),
        plt.Line2D([0], [0], color="#0072B2", marker="s", linestyle="-", label="500 Concrete"),
        plt.Line2D([0], [0], color="#D55E00", marker="^", linestyle="-", label="300 NaOH"),
        plt.Line2D([0], [0], color="#D55E00", marker="s", linestyle="-", label="500 NaOH"),
    ]
    fig.legend(handles=handles, title="Treatment", loc="upper right")
    fig.suptitle("Kontrollkorrigierte Zellzahldynamik")
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(FIGURES_DIR / "05_kontrollkorrigiert.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_ratios(data: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for mesocosm, frame in data.groupby("mesocosm"):
        treatment = frame.treatment_group.iloc[0]
        material = "Concrete" if "concrete" in treatment.lower() else "NaOH"
        dose = "Kontrolle" if "kontrolle" in treatment.lower() else treatment.split()[0]
        color = TREATMENT_COLORS["Kontrolle"] if dose == "Kontrolle" else TREATMENT_COLORS[material]
        marker = MARKERS[dose]
        ax.plot(frame.day, frame.micro_phyto_ratio, color=color, marker=marker,
                linewidth=1.7, markersize=6)
    ax.axvline(4, color="black", linestyle="--", linewidth=1)
    ax.set_yscale("log")
    ax.set_xlabel("Probetag")
    ax.set_ylabel("Mikrozooplankton / Phytoplankton")
    ax.set_title("Verhältnis der Gesamtzellzahlen")
    handles = [
        plt.Line2D([0], [0], color="#555555", marker="o", label="Kontrolle"),
        plt.Line2D([0], [0], color="#0072B2", marker="^", label="300 Concrete"),
        plt.Line2D([0], [0], color="#0072B2", marker="s", label="500 Concrete"),
        plt.Line2D([0], [0], color="#D55E00", marker="^", label="300 NaOH"),
        plt.Line2D([0], [0], color="#D55E00", marker="s", label="500 NaOH"),
    ]
    ax.legend(handles=handles, title="Treatment", ncol=2)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "06_micro_phyto_verhaeltnis.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_phase(phase: pd.DataFrame) -> None:
    selected = phase[phase.comparison.isin([
        "Ciliaten vs. Phytoplankton gesamt",
        "Dinoflagellaten vs. Phytoplankton gesamt"
    ])]
    summary = selected.groupby(["phase", "comparison"], as_index=False).spearman_rho.mean()
    phase_order = ["Vorbehandlung", "Fruhe Nachbehandlung", "Mittlere Nachbehandlung", "Spate Nachbehandlung"]
    summary["phase"] = pd.Categorical(summary.phase, phase_order, ordered=True)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=summary, x="phase", y="spearman_rho", hue="comparison",
                 hue_order=["Ciliaten vs. Phytoplankton gesamt", "Dinoflagellaten vs. Phytoplankton gesamt"],
                 palette={"Ciliaten vs. Phytoplankton gesamt": "#009E73",
                          "Dinoflagellaten vs. Phytoplankton gesamt": "#E69F00"},
                 marker="o", markersize=8, linewidth=2.5, ax=ax)
    ax.axhline(0, color="#555555", linewidth=0.8)
    ax.set_xlabel("")
    ax.set_ylabel("Mittlere Spearman-Korrelation")
    ax.set_title("Kopplung nach experimentellen Phasen")
    ax.tick_params(axis="x", rotation=20)
    ax.legend(title="")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "07_phasenvergleich.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def plot_size_lags(size_summary: pd.DataFrame) -> None:
    selected = size_summary[
        size_summary.micro_group.isin(["micro_ciliate_lt30", "micro_ciliate_gt30"])
    ]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    for ax, (micro_group, title) in zip(axes, [
        ("micro_ciliate_lt30", "Ciliaten <30 um"),
        ("micro_ciliate_gt30", "Ciliaten >30 um")
    ]):
        frame = selected[selected.micro_group == micro_group]
        sns.lineplot(data=frame, x="lag_days", y="mean_spearman_rho",
                     hue="phyto_group", marker="o", palette=["#56B4E9", "#CC79A7", "#333333"],
                     linewidth=2.2, markersize=8, ax=ax)
        ax.axhline(0, color="#555555", linewidth=0.8)
        ax.set_title(title)
        ax.set_xlabel("Lag (Tage)")
        ax.set_ylabel("Mittlere Spearman-Korrelation")
    axes[-1].legend(title="Phytoplankton")
    axes[0].legend(title="Phytoplankton")
    fig.suptitle("Grose-Klassen-Kopplung")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "08_groessen_lags.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def append_excel(sheets: dict[str, pd.DataFrame]) -> None:
    with pd.ExcelWriter(COMPARISON_XLSX, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        for name, frame in sheets.items():
            frame.to_excel(writer, sheet_name=name, index=False)
        for sheet in writer.book.worksheets:
            sheet.freeze_panes = "A2"
            sheet.auto_filter.ref = sheet.dimensions


def write_extension_markdown(control, ratios, phases, size, size_summary, signals,
                             peaks, did, bootstrap) -> None:
    text = f"""# Erweiterte Vergleiche: Mikrozooplankton und Phytoplankton

## Wichtigste Ergebnisse

- Die kontrollkorrigierte Darstellung trennt Treatmentverläufe von den lokalen Controldynamiken von M3 beziehungsweise M6.
- Die Verhältniszeitreihe Mikrozooplankton/Phytoplankton zeigt, ob die Konsumentendichte oder die Ressourcenbasis stärker variiert.
- Die Phasenanalyse trennt Vorbehandlung, frühe, mittlere und späte Nachbehandlung.
- Die Größenklassenanalyse prüft, ob Ciliaten und Dinoflagellaten unterschiedlicher Größe mit Small- oder Large-Phytoplankton gekoppelt sind.
- Die Peak- und Recovery-Werte dokumentieren zeitliche Extrema beider Organismengruppen.

## Kontrollkorrigierte Dynamik

Für Concrete-Treatments wurde gegen M3 und für NaOH-Treatments gegen M6 korrigiert:

{control.groupby(["mesocosm", "treatment"], as_index=False).agg(
    mean_micro_vs_control=("log2_micro_total_vs_control", "mean"),
    mean_phyto_vs_control=("log2_phyto_total_vs_control", "mean")
).round(3).to_string(index=False)}

## Difference-in-Differences

{did.round(3).to_string(index=False)}

## Verhältnisse und Phasen

Die mittleren Mikrozooplankton/Phytoplankton-Verhältnisse je Mesokosmos waren:

{ratios.groupby(["mesocosm", "treatment_group"], as_index=False).agg(
    mean_ratio=("micro_phyto_ratio", "mean")
).round(4).to_string(index=False)}

Phasenspezifische mittlere Spearman-Korrelationen:

{phases.groupby(["phase", "comparison"], as_index=False).agg(
    n_mesokosmen=("mesocosm", "count"),
    mean_spearman_rho=("spearman_rho", "mean")
).round(3).to_string(index=False)}

## Großenklassen und Lag

Die stärksten mittleren Größenklassen-Lags waren:

{size_summary.sort_values("mean_spearman_rho", ascending=False).groupby(
    ["micro_group", "phyto_group"], as_index=False
).first().head(12).round(3).to_string(index=False)}

## Phytoplankton-Signalgruppen

Die stärksten explorativen Zusammenhänge zwischen Mikrozooplanktongruppen und ausgewählten Phytoplankton-Signalen waren:

{signals.reindex(signals.spearman_rho.abs().sort_values(ascending=False).index).head(15).round(3).to_string(index=False)}

## Peak und Recovery

{peaks.round(1).to_string(index=False)}

## Bootstrap-Lags

{bootstrap.round(3).to_string(index=False)}

## Grafiken

- `05_kontrollkorrigiert.png`: Kontrollkorrigierte Gesamtzellzahlen.
- `06_micro_phyto_verhaeltnis.png`: Verhältnis Mikrozooplankton/Phytoplankton.
- `07_phasenvergleich.png`: Mesokosmosgemittelte Kopplung nach Phasen.
- `08_groessen_lags.png`: Lag-Muster für kleine und große Ciliaten.
"""
    (COMPARISON_DIR / "erweiterte_vergleiche.md").write_text(text, encoding="utf-8")


def main() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    data, _ = load_data()
    control = control_corrected(data)
    ratios, phases = ratios_and_phases(data)
    size, size_summary = size_and_lag_correlations(data)
    signals = signal_correlations(data)
    peaks = peak_recovery(data)
    did = difference_in_differences(data)
    existing = pd.read_excel(COMPARISON_XLSX, sheet_name="Korrelationen")
    bootstrap = bootstrap_lag_summary(existing)

    plot_control_corrected(control)
    plot_ratios(data)
    plot_phase(phases)
    plot_size_lags(size_summary)

    append_excel({
        "Kontrollkorrigiert": control,
        "Verhaeltnisse": ratios[["mesocosm", "day", "treatment_group", "micro_phyto_ratio",
                                  "ciliate_phyto_ratio", "dino_phyto_ratio"]],
        "Phasen_Korrelationen": phases,
        "Groessen_Lags": size,
        "Groessen_Lag_Summary": size_summary,
        "Signal_Korrelationen": signals,
        "Peak_Recovery": peaks,
        "Difference_in_Difference": did,
        "Bootstrap_Lags": bootstrap,
    })
    write_extension_markdown(control, ratios, phases, size, size_summary, signals, peaks, did, bootstrap)
    print(f"Erweiterte Auswertung: {COMPARISON_DIR}")


if __name__ == "__main__":
    main()
