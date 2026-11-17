from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


PROJECT_DIR = Path(__file__).resolve().parents[1]
WORKBOOK = PROJECT_DIR / "MicroZP_Gran_Canaria_2026_MaxRomes_AntoniaKirner (1).xlsx"
PROTOCOL = PROJECT_DIR / "MicroZP_Kosmos_GC_2026_Max_Romes.xlsx"
RESULTS_DIR = PROJECT_DIR / "results" / "microzooplankton_analysis"
FIGURES_DIR = RESULTS_DIR / "figures"
MESOCOSMS = [1, 2, 3, 6, 8, 9]
CONTROL_MESOCOSMS = [3, 6]
SAMPLE_DAYS = [1, 2, 3, 5, 6, 7, 11, 15, 19, 23, 27, 31]
CILIATE_CATEGORIES = {
    "Strombidium sp. <30",
    "Strombidium sp. >30",
    "Strobilidium sp. <30",
    "Strobilidium sp. >30",
    "Tintinnid sp. <30",
    "Tintinnid sp. >30",
    "Mesodinium sp. <30",
    "Mesodinium sp. >30",
    "Unknown Ciliate <30",
    "Unknown Ciliate >30",
}
COUNT_TO_LITRE = 40


def sheet_metadata(name: str) -> tuple[int, int] | None:
    match = re.search(r"_M(\d+)_T(\d+)_", name)
    if not match:
        return None
    mesocosm, day = map(int, match.groups())
    if mesocosm not in MESOCOSMS or day not in SAMPLE_DAYS:
        return None
    return mesocosm, day


def load_metadata() -> pd.DataFrame:
    protocol = pd.read_excel(PROTOCOL, sheet_name="Protocol", header=None)
    treatments = {
        int(str(protocol.iloc[1, col]).removeprefix("M")): str(protocol.iloc[0, col])
        for col in range(protocol.shape[1])
        if str(protocol.iloc[1, col]).startswith("M") and pd.notna(protocol.iloc[0, col])
    }
    metadata = pd.DataFrame(
        {"mesocosm": MESOCOSMS, "treatment": [treatments[m] for m in MESOCOSMS]}
    )
    metadata[["dose", "material"]] = metadata["treatment"].str.extract(
        r"(?P<dose>\d+)\s+(?P<material>concrete|NaOH)"
    )
    metadata["dose"] = metadata["dose"].astype(int)
    metadata["control"] = metadata["mesocosm"].isin(CONTROL_MESOCOSMS)
    metadata["treatment_group"] = np.where(
        metadata["control"],
        "Kontrolle",
        metadata["dose"].astype(str) + " " + metadata["material"],
    )
    return metadata


def load_counts() -> pd.DataFrame:
    workbook = pd.ExcelFile(WORKBOOK)
    records: list[pd.DataFrame] = []
    for name in workbook.sheet_names:
        parsed = sheet_metadata(name)
        if parsed is None:
            continue
        mesocosm, day = parsed
        frame = pd.read_excel(WORKBOOK, sheet_name=name)
        if "Species_SizeClass" not in frame or "Count" not in frame:
            raise ValueError(f"{name} enthält nicht die benötigten Spalten Species_SizeClass und Count.")
        data = pd.DataFrame(
            {
                "mesocosm": mesocosm,
                "sample_day": day,
                "sheet": name,
                "category": frame["Species_SizeClass"].astype("string"),
                "count_raw": pd.to_numeric(frame["Count"], errors="coerce"),
            }
        )
        data["count_raw"] = data["count_raw"].fillna(0)
        data["group"] = np.where(
            data["category"].isin(CILIATE_CATEGORIES), "Ciliate", "Dinoflagellate"
        )
        data["size_class"] = data["category"].str.extract(r"(<30|>30)", expand=False)
        data["cells_L"] = data["count_raw"] * COUNT_TO_LITRE
        records.append(data)
    observations = pd.concat(records, ignore_index=True)
    return observations.merge(load_metadata(), on="mesocosm", validate="many_to_one")


def add_phase(data: pd.DataFrame) -> pd.DataFrame:
    result = data.copy()
    result["phase"] = np.where(result["sample_day"] <= 3, "Vorbehandlung", "Nachbehandlung")
    return result


def aggregate(data: pd.DataFrame, include_total: bool = False) -> pd.DataFrame:
    grouped = (
        data.groupby(
            [
                "mesocosm",
                "sample_day",
                "treatment",
                "dose",
                "material",
                "control",
                "treatment_group",
                "group",
            ],
            as_index=False,
        )
        .agg(
            count_raw=("count_raw", "sum"),
            cells_L=("cells_L", "sum"),
            positive_categories=("count_raw", lambda x: int((x > 0).sum())),
        )
    )
    if include_total:
        keys = [
            "mesocosm",
            "sample_day",
            "treatment",
            "dose",
            "material",
            "control",
            "treatment_group",
        ]
        grouped = (
            grouped.groupby(keys, as_index=False)
            .agg(count_raw=("count_raw", "sum"), cells_L=("cells_L", "sum"))
        )
        grouped["group"] = "Gesamt"
    return add_phase(grouped)


def aggregate_sizes(data: pd.DataFrame) -> pd.DataFrame:
    result = (
        data.groupby(
            [
                "mesocosm",
                "sample_day",
                "treatment",
                "dose",
                "material",
                "control",
                "treatment_group",
                "group",
                "size_class",
            ],
            as_index=False,
        )
        .agg(count_raw=("count_raw", "sum"), cells_L=("cells_L", "sum"))
    )
    return add_phase(result)


def pre_treatment_trends(total: pd.DataFrame, groups: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for label, source in [("Gesamt", total), ("Ciliate", groups[groups.group == "Ciliate"]),
                          ("Dinoflagellate", groups[groups.group == "Dinoflagellate"])]:
        for mesocosm, frame in source.groupby("mesocosm"):
            frame = frame[frame.sample_day <= 3].sort_values("sample_day")
            x = frame.sample_day.to_numpy()
            y = np.log10(frame.cells_L.to_numpy() + 1)
            slope = float(np.polyfit(x, y, 1)[0])
            rows.append(
                {
                    "group": label,
                    "mesocosm": mesocosm,
                    "treatment": frame.treatment.iloc[0],
                    "slope_log10_cells_per_day": slope,
                    "direction": "Anstieg" if slope > 0 else "Abnahme" if slope < 0 else "konstant",
                    "T1_cells_L": frame.loc[frame.sample_day == 1, "cells_L"].iloc[0],
                    "T3_cells_L": frame.loc[frame.sample_day == 3, "cells_L"].iloc[0],
                }
            )
    return pd.DataFrame(rows)


def normalized_changes(groups: pd.DataFrame) -> pd.DataFrame:
    data = groups[groups.sample_day >= 3].copy()
    baseline = data[data.sample_day == 3][["mesocosm", "group", "cells_L"]].rename(
        columns={"cells_L": "T3_cells_L"}
    )
    data = data.merge(baseline, on=["mesocosm", "group"], validate="many_to_one")
    data["log2_change_vs_T3"] = np.log2((data.cells_L + 1) / (data.T3_cells_L + 1))
    return data


def treatment_summary(normalized: pd.DataFrame) -> pd.DataFrame:
    post = normalized[normalized.sample_day >= 5]
    summary = (
        post.groupby(["group", "mesocosm", "treatment", "dose", "material", "control"], as_index=False)
        .agg(
            mean_post_cells_L=("cells_L", "mean"),
            T31_cells_L=("cells_L", lambda x: x.iloc[-1]),
            mean_log2_change_vs_T3=("log2_change_vs_T3", "mean"),
            minimum_log2_change_vs_T3=("log2_change_vs_T3", "min"),
            maximum_log2_change_vs_T3=("log2_change_vs_T3", "max"),
        )
    )
    return summary


def control_comparison(total: pd.DataFrame, groups: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for label, source in [("Gesamt", total), ("Ciliate", groups[groups.group == "Ciliate"]),
                          ("Dinoflagellate", groups[groups.group == "Dinoflagellate"])]:
        control = source[source.mesocosm.isin(CONTROL_MESOCOSMS)]
        pivot = control.pivot(index="sample_day", columns="mesocosm", values="cells_L")
        pivot = pivot.rename(columns={3: "M3_cells_L", 6: "M6_cells_L"}).reset_index()
        pivot["difference_M3_minus_M6"] = pivot.M3_cells_L - pivot.M6_cells_L
        pivot["relative_difference_vs_mean"] = pivot.difference_M3_minus_M6 / pivot[
            ["M3_cells_L", "M6_cells_L"]
        ].mean(axis=1)
        pivot["group"] = label
        rows.append(pivot)
    return pd.concat(rows, ignore_index=True)


def category_summary(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.groupby(["group", "category"], as_index=False)
        .agg(
            total_count=("count_raw", "sum"),
            total_cells_L=("cells_L", "sum"),
            samples_with_count=("count_raw", lambda x: int((x > 0).sum())),
            samples=("count_raw", "size"),
        )
        .sort_values(["group", "total_count"], ascending=[True, False])
    )


def descriptive_effects(source: pd.DataFrame, dimensions: list[str]) -> pd.DataFrame:
    keys = ["mesocosm", "sample_day", *dimensions]
    baseline = source[source.sample_day == 3][keys + ["cells_L"]].rename(
        columns={"cells_L": "T3_cells_L"}
    )
    post = source[source.sample_day >= 5].merge(
        baseline, on=["mesocosm", *dimensions], validate="many_to_one"
    )
    post["change_vs_T3_percent"] = (
        (post["cells_L"] - post["T3_cells_L"]) / post["T3_cells_L"].replace(0, np.nan) * 100
    )
    post["log2_change_vs_T3"] = np.log2((post["cells_L"] + 1) / (post["T3_cells_L"] + 1))
    result = (
        post.groupby(["mesocosm", *dimensions], as_index=False)
        .agg(
            mean_post_cells_L=("cells_L", "mean"),
            T31_cells_L=("cells_L", lambda values: values.iloc[-1]),
            mean_change_vs_T3_percent=("change_vs_T3_percent", "mean"),
            mean_log2_change_vs_T3=("log2_change_vs_T3", "mean"),
            minimum_log2_change_vs_T3=("log2_change_vs_T3", "min"),
            maximum_log2_change_vs_T3=("log2_change_vs_T3", "max"),
        )
    )
    return result


def quality_summary(data: pd.DataFrame) -> pd.DataFrame:
    sheets = data[["sheet", "mesocosm", "sample_day"]].drop_duplicates()
    values = [
        ("Arbeitsblätter", len(sheets), 72, "6 Mesokosmen × 12 Probetage"),
        ("Mesokosmen", sheets.mesocosm.nunique(), 6, "M1, M2, M3, M6, M8, M9"),
        ("Probetage", sheets.sample_day.nunique(), 12, "T1 bis T31 ohne T4"),
        ("Kategorien pro Arbeitsblatt", data.groupby("sheet").category.nunique().min(), 28, "20 Ciliaten-/Dinoflagellaten-Größenkategorien"),
        ("Nichtnumerische Counts", int(pd.to_numeric(data.count_raw, errors="coerce").isna().sum()), 0, "Count wird numerisch eingelesen"),
    ]
    return pd.DataFrame(values, columns=["Prüfung", "Beobachtet", "Erwartet", "Einordnung"])


def auc_and_minimum(source: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (mesocosm, group), frame in source.groupby(["mesocosm", "group"]):
        frame = frame[frame.sample_day >= 5].sort_values("sample_day")
        minimum = frame.loc[frame.cells_L.idxmin()]
        rows.append(
            {
                "mesocosm": mesocosm,
                "group": group,
                "treatment": frame.treatment.iloc[0],
                "post_auc_cells_day_L": float(np.trapezoid(frame.cells_L, frame.sample_day)),
                "minimum_cells_L": minimum.cells_L,
                "minimum_day": int(minimum.sample_day),
                "T31_cells_L": frame.loc[frame.sample_day == 31, "cells_L"].iloc[0],
            }
        )
    return pd.DataFrame(rows)


def group_ratios(groups: pd.DataFrame, total: pd.DataFrame) -> pd.DataFrame:
    ciliate = groups[groups.group == "Ciliate"][["mesocosm", "sample_day", "cells_L"]].rename(
        columns={"cells_L": "ciliate_cells_L"}
    )
    dino = groups[groups.group == "Dinoflagellate"][["mesocosm", "sample_day", "cells_L"]].rename(
        columns={"cells_L": "dinoflagellate_cells_L"}
    )
    result = ciliate.merge(dino, on=["mesocosm", "sample_day"]).merge(
        total[["mesocosm", "sample_day", "treatment", "cells_L"]].rename(
            columns={"cells_L": "total_cells_L"}
        ),
        on=["mesocosm", "sample_day"],
        validate="one_to_one",
    )
    result["ciliate_share"] = result.ciliate_cells_L / result.total_cells_L.replace(0, np.nan)
    result["ciliate_dino_ratio"] = result.ciliate_cells_L / result.dinoflagellate_cells_L.replace(0, np.nan)
    baseline = result[result.sample_day == 3][
        ["mesocosm", "ciliate_share", "ciliate_dino_ratio"]
    ].rename(columns={"ciliate_share": "T3_ciliate_share", "ciliate_dino_ratio": "T3_ciliate_dino_ratio"})
    return result.merge(baseline, on="mesocosm", validate="many_to_one")


def size_structure(sizes: pd.DataFrame) -> pd.DataFrame:
    totals = sizes.groupby(["mesocosm", "sample_day", "group"], as_index=False).cells_L.sum()
    result = sizes.merge(totals, on=["mesocosm", "sample_day", "group"], suffixes=("", "_group_total"))
    result["size_share"] = result.cells_L / result.cells_L_group_total.replace(0, np.nan)
    baseline = result[result.sample_day == 3][
        ["mesocosm", "group", "size_class", "size_share"]
    ].rename(columns={"size_share": "T3_size_share"})
    return result.merge(baseline, on=["mesocosm", "group", "size_class"], validate="many_to_one")


def control_based_effects(groups: pd.DataFrame) -> pd.DataFrame:
    control_for_material = {"concrete": 3, "NaOH": 6}
    rows = []
    for mesocosm, frame in groups.groupby("mesocosm"):
        if frame.dose.iloc[0] == 0:
            continue
        control_meso = control_for_material[frame.material.iloc[0]]
        control = groups[groups.mesocosm == control_meso]
        for group in ["Ciliate", "Dinoflagellate"]:
            treated = frame[(frame.group == group) & (frame.sample_day >= 5)].set_index("sample_day")
            reference = control[(control.group == group) & (control.sample_day >= 5)].set_index("sample_day")
            for day in treated.index:
                treatment_value = treated.loc[day, "cells_L"]
                control_value = reference.loc[day, "cells_L"]
                rows.append(
                    {
                        "mesocosm": mesocosm,
                        "treatment": frame.treatment.iloc[0],
                        "group": group,
                        "sample_day": day,
                        "control_mesocosm": control_meso,
                        "treatment_cells_L": treatment_value,
                        "control_cells_L": control_value,
                        "difference_cells_L": treatment_value - control_value,
                        "ratio_treatment_control": treatment_value / control_value if control_value else np.nan,
                    }
                )
    return pd.DataFrame(rows)


def category_winners_losers(observations: pd.DataFrame) -> pd.DataFrame:
    category_data = observations.groupby(
        ["mesocosm", "sample_day", "category"], as_index=False
    ).cells_L.sum()
    effects = descriptive_effects(category_data, ["category"])
    effects["response_class"] = np.select(
        [effects.mean_change_vs_T3_percent >= 25, effects.mean_change_vs_T3_percent <= -25],
        ["Gewinner", "Verlierer"],
        default="geringe Veränderung",
    )
    return effects.sort_values(["response_class", "mean_change_vs_T3_percent"])


def lagged_relationships(groups: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for mesocosm, frame in groups.groupby("mesocosm"):
        ciliate = frame[frame.group == "Ciliate"].set_index("sample_day").cells_L
        dino = frame[frame.group == "Dinoflagellate"].set_index("sample_day").cells_L
        for lag in [-4, -2, -1, 0, 1, 2, 4]:
            pairs = pd.concat(
                [ciliate.rename("ciliate"), dino.rename("dino").shift(lag)], axis=1
            ).dropna()
            rows.append(
                {
                    "mesocosm": mesocosm,
                    "treatment": frame.treatment.iloc[0],
                    "lag_days": lag,
                    "n_pairs": len(pairs),
                    "correlation_log10": pairs.apply(np.log10).corr().iloc[0, 1],
                }
            )
    return pd.DataFrame(rows)


def similarity_over_time(total: pd.DataFrame, groups: pd.DataFrame) -> pd.DataFrame:
    composition = groups.pivot_table(
        index=["mesocosm", "sample_day"], columns="group", values="cells_L"
    ).reset_index()
    composition["ciliate_share"] = composition["Ciliate"] / (
        composition["Ciliate"] + composition["Dinoflagellate"]
    )
    rows = []
    for day in SAMPLE_DAYS:
        counts = total[total.sample_day == day].cells_L
        shares = composition[composition.sample_day == day].ciliate_share
        rows.append(
            {
                "sample_day": day,
                "mean_total_cells_L": counts.mean(),
                "cv_total_cells": counts.std(ddof=1) / counts.mean(),
                "min_total_cells_L": counts.min(),
                "max_total_cells_L": counts.max(),
                "mean_ciliate_share": shares.mean(),
                "sd_ciliate_share": shares.std(ddof=1),
                "cv_ciliate_share": shares.std(ddof=1) / shares.mean(),
                "min_ciliate_share": shares.min(),
                "max_ciliate_share": shares.max(),
            }
        )
    return pd.DataFrame(rows)


def save_figures(total: pd.DataFrame, groups: pd.DataFrame, sizes: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid", context="notebook")
    palette = {
        "300 concrete": "#0072B2",
        "500 NaOH": "#D55E00",
        "Kontrolle": "#009E73",
        "300 NaOH": "#CC79A7",
        "500 concrete": "#E69F00",
    }

    fig, axes = plt.subplots(3, 1, figsize=(11, 13), sharex=True)
    for ax, label, title in zip(
        axes, ["Gesamt", "Ciliate", "Dinoflagellate"], ["Gesamt", "Ciliaten", "Dinoflagellaten"]
    ):
        source = total if label == "Gesamt" else groups[groups.group == label]
        sns.lineplot(
            data=source,
            x="sample_day",
            y="cells_L",
            hue="treatment_group",
            style="mesocosm",
            markers=True,
            dashes=False,
            palette=palette,
            ax=ax,
        )
        ax.axvline(4, color="black", linestyle="--", linewidth=1)
        ax.set_yscale("log")
        ax.set_title(title)
        ax.set_ylabel("Zellen L$^{-1}$")
        ax.legend(title="Treatment / M", bbox_to_anchor=(1.01, 1), loc="upper left")
    axes[-1].set_xlabel("Probetag")
    fig.suptitle("Mikrozooplankton: zeitlicher Verlauf", y=1.01)
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "01_zeitverlauf.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    normalized = normalized_changes(groups)
    grid = sns.FacetGrid(
        normalized,
        row="group",
        hue="treatment_group",
        height=3.8,
        aspect=2.2,
        sharey=False,
        palette=palette,
    )
    grid.map_dataframe(
        sns.lineplot,
        x="sample_day",
        y="log2_change_vs_T3",
        markers=True,
        dashes=False,
    )
    for ax in grid.axes.flat:
        ax.axvline(4, color="black", linestyle="--", linewidth=1)
        ax.axhline(0, color="grey", linewidth=0.8)
        ax.set_ylabel("log2-Faktor vs. T3")
        ax.set_xlabel("Probetag")
    grid.add_legend(title="Treatment / M", bbox_to_anchor=(1.02, 0.5), loc="center left")
    grid.fig.suptitle("Veränderung relativ zu T3", y=1.03)
    grid.fig.savefig(FIGURES_DIR / "02_normalisiert_T3.png", dpi=300, bbox_inches="tight")
    plt.close(grid.fig)

    control = groups[groups.mesocosm.isin(CONTROL_MESOCOSMS)]
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True)
    for ax, label in zip(axes, ["Ciliate", "Dinoflagellate"]):
        sns.lineplot(
            data=control[control.group == label],
            x="sample_day",
            y="cells_L",
            hue="mesocosm",
            marker="o",
            palette={3: "#0072B2", 6: "#D55E00"},
            ax=ax,
        )
        ax.axvline(4, color="black", linestyle="--", linewidth=1)
        ax.set_yscale("log")
        ax.set_title(label)
        ax.set_ylabel("Zellen L$^{-1}$")
        ax.set_xlabel("Probetag")
    fig.suptitle("Kontrollvergleich: M3 (0 Concrete) und M6 (0 NaOH)")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "03_kontrollen.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    ciliate_sizes = sizes[sizes.group == "Ciliate"]
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.lineplot(
        data=ciliate_sizes,
        x="sample_day",
        y="cells_L",
        hue="size_class",
        style="mesocosm",
        markers=True,
        dashes=False,
        ax=ax,
    )
    ax.axvline(4, color="black", linestyle="--", linewidth=1)
    ax.set_yscale("log")
    ax.set_title("Ciliaten nach Größenklasse")
    ax.set_xlabel("Probetag")
    ax.set_ylabel("Zellen L$^{-1}$")
    ax.legend(title="Größenklasse / M", bbox_to_anchor=(1.01, 1), loc="upper left")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "04_ciliaten_groessenklassen.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_outputs(
    observations: pd.DataFrame,
    total: pd.DataFrame,
    groups: pd.DataFrame,
    sizes: pd.DataFrame,
    trends: pd.DataFrame,
    normalized: pd.DataFrame,
    effects: pd.DataFrame,
    controls: pd.DataFrame,
    categories: pd.DataFrame,
    quality: pd.DataFrame,
) -> None:
    total_effects = descriptive_effects(total, [])
    group_effects = descriptive_effects(groups, ["group"])
    size_effects = descriptive_effects(sizes, ["group", "size_class"])
    category_data = (
        observations.groupby(["mesocosm", "sample_day", "category"], as_index=False)
        .agg(cells_L=("cells_L", "sum"))
    )
    category_effects = descriptive_effects(category_data, ["category"])
    auc_minimum = auc_and_minimum(pd.concat([total, groups], ignore_index=True))
    ratios = group_ratios(groups, total)
    structure = size_structure(sizes)
    control_effects = control_based_effects(groups)
    winners_losers = category_winners_losers(observations)
    lagged = lagged_relationships(groups)
    similarity = similarity_over_time(total, groups)

    output = RESULTS_DIR / "microzooplankton_analysis.xlsx"
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        observations.to_excel(writer, sheet_name="Counts_klassifiziert", index=False)
        total.to_excel(writer, sheet_name="Gesamtverlauf", index=False)
        groups.to_excel(writer, sheet_name="Gruppenverlauf", index=False)
        sizes.to_excel(writer, sheet_name="Groessenklassen", index=False)
        trends.to_excel(writer, sheet_name="Vorbehandlung", index=False)
        normalized.to_excel(writer, sheet_name="Normalisiert_T3", index=False)
        effects.to_excel(writer, sheet_name="Treatmentvergleich", index=False)
        total_effects.to_excel(writer, sheet_name="Effekt_Gesamt", index=False)
        group_effects.to_excel(writer, sheet_name="Effekt_Gruppen", index=False)
        size_effects.to_excel(writer, sheet_name="Effekt_Groessen", index=False)
        category_effects.to_excel(writer, sheet_name="Effekt_Kategorien", index=False)
        auc_minimum.to_excel(writer, sheet_name="AUC_Minimum", index=False)
        ratios.to_excel(writer, sheet_name="Ciliate_Dino_Verhaeltnis", index=False)
        structure.to_excel(writer, sheet_name="Groessenstruktur", index=False)
        control_effects.to_excel(writer, sheet_name="Kontrollbasierte_Effekte", index=False)
        winners_losers.to_excel(writer, sheet_name="Gewinner_Verlierer", index=False)
        lagged.to_excel(writer, sheet_name="Zeitverzoegerte_Beziehung", index=False)
        similarity.to_excel(writer, sheet_name="Aehnlichkeit_Zeitverlauf", index=False)
        controls.to_excel(writer, sheet_name="Kontrollen", index=False)
        categories.to_excel(writer, sheet_name="Kategorien", index=False)
        quality.to_excel(writer, sheet_name="Datenqualitaet", index=False)
        for sheet in writer.book.worksheets:
            sheet.freeze_panes = "A2"
            sheet.auto_filter.ref = sheet.dimensions
            for column in sheet.columns:
                width = min(max(len(str(cell.value or "")) for cell in column) + 2, 42)
                sheet.column_dimensions[column[0].column_letter].width = width

    total_pre = trends[trends.group == "Gesamt"]
    directions = total_pre.direction.value_counts().to_dict()
    control = controls[controls.group == "Gesamt"]
    pre_difference = control[control.sample_day <= 3].relative_difference_vs_mean.abs().mean()
    post_difference = control[control.sample_day >= 5].relative_difference_vs_mean.abs().mean()
    top = categories.head(10)[
        ["group", "category", "total_count", "samples_with_count"]
    ].to_string(index=False)
    missing_count = int((observations.count_raw == 0).sum())
    treatment_rows = group_effects[
        ["mesocosm", "group", "mean_post_cells_L", "T31_cells_L", "mean_change_vs_T3_percent"]
    ].to_string(index=False)
    size_rows = size_effects[
        ["mesocosm", "group", "size_class", "mean_change_vs_T3_percent", "T31_cells_L"]
    ].to_string(index=False)
    auc_rows = auc_minimum[auc_minimum.group == "Gesamt"].to_string(index=False)
    ratio_summary = ratios[ratios.sample_day >= 5].groupby("mesocosm", as_index=False).agg(
        mean_ciliate_share=("ciliate_share", "mean"),
        mean_ciliate_dino_ratio=("ciliate_dino_ratio", "mean"),
    ).to_string(index=False)
    control_summary = control_effects.groupby(
        ["mesocosm", "treatment", "group"], as_index=False
    ).agg(
        mean_ratio_treatment_control=("ratio_treatment_control", "mean"),
        mean_difference_cells_L=("difference_cells_L", "mean"),
    ).to_string(index=False)
    winners = winners_losers[winners_losers.response_class == "Gewinner"].sort_values(
        "mean_change_vs_T3_percent", ascending=False
    ).head(8)[["mesocosm", "category", "mean_change_vs_T3_percent"]].to_string(index=False)
    losers = winners_losers[winners_losers.response_class == "Verlierer"].sort_values(
        "mean_change_vs_T3_percent"
    ).head(8)[["mesocosm", "category", "mean_change_vs_T3_percent"]].to_string(index=False)
    lag_summary = lagged.loc[lagged.groupby("mesocosm").correlation_log10.idxmax()][
        ["mesocosm", "lag_days", "correlation_log10"]
    ].to_string(index=False)
    similarity_mean_cv_counts = similarity.cv_total_cells.mean()
    similarity_mean_cv_composition = similarity.cv_ciliate_share.mean()
    similarity_median_cv_counts = similarity.cv_total_cells.median()
    similarity_median_cv_composition = similarity.cv_ciliate_share.median()
    t1 = similarity[similarity.sample_day == 1].iloc[0]
    t3 = similarity[similarity.sample_day == 3].iloc[0]
    t31 = similarity[similarity.sample_day == 31].iloc[0]
    report = f"""# Mikrozooplanktonanalyse

## Datengrundlage

Die Auswertung wurde direkt aus `{WORKBOOK.name}` erstellt. Berücksichtigt wurden M1, M2, M3, M6, M8 und M9 mit den Probetagen T1, T2, T3, T5, T6, T7, T11, T15, T19, T23, T27 und T31. Die Behandlung erfolgte an T4; T1–T3 werden daher als Vorbehandlung und T5–T31 als Nachbehandlung behandelt.

Es wurden ausschließlich die Rohzählungen (`Count`) der taxonomischen Größenklassen verwendet. Für jede Zeile gilt:

`Zellen L⁻¹ = Count × 2 × 1000 / 50 ml = Count × 40`

Leere Count-Felder und Count = 0 wurden als kein Fund behandelt. Ciliaten umfassen genau die zehn festgelegten Kategorien von Strombidium, Strobilidium, Tintinnid, Mesodinium und Unknown Ciliate. Alle übrigen Kategorien wurden als Dinoflagellaten klassifiziert. Biomasse wurde nicht ausgewertet.

## Ergebnisse

### Genereller Verlauf und Vorbehandlung

Die Gesamtzellzahlen zeigen vor T4 unterschiedliche Richtungen: Zwischen T1 und T3 zeigen **{directions.get("Anstieg", 0)} von 6 Mesokosmen einen Anstieg** und **{directions.get("Abnahme", 0)} von 6 eine Abnahme**. Ein vollständig gemeinsamer Vorbehandlungstrend liegt somit nicht vor. Die Zeitreihen sind in `figures/01_zeitverlauf.png` dargestellt.

### Kontrollen

M3 (0 Concrete) und M6 (0 NaOH) wurden als Kontrollen verglichen. Die mittlere absolute relative Differenz der Gesamtzellzahl beträgt vor T4 **{pre_difference:.1%}** und nach T4 **{post_difference:.1%}**. Die Kontrollen sind damit als Referenz verwendbar, aber nicht gleichwertig identisch; ihre Ausgangsunterschiede müssen bei Treatment-Interpretationen berücksichtigt werden.

### Treatment-Effekte

Die Treatmentverläufe sind in `figures/02_normalisiert_T3.png` relativ zu T3 dargestellt. Die folgenden Werte sind ausdrücklich deskriptive Effekte und werden trotz fehlender Replikate berichtet. `mean_change_vs_T3_percent` ist die mittlere prozentuale Veränderung der Nachbehandlungstage gegenüber T3; `T31_cells_L` ist der Wert am letzten Probetag.

#### Gesamtzellzahl

{total_effects[["mesocosm", "mean_post_cells_L", "T31_cells_L", "mean_change_vs_T3_percent"]].to_string(index=False)}

#### Hauptgruppen

{treatment_rows}

#### Größenklassen

{size_rows}

Die Kombinationen aus Material und Dosierung werden ebenfalls direkt verglichen: 300 Concrete (M1) zeigt bei den Ciliaten eine mittlere Veränderung von {group_effects.query("mesocosm == 1 and group == 'Ciliate'").mean_change_vs_T3_percent.iloc[0]:.1f}% gegenüber T3, während 300 NaOH (M8) {group_effects.query("mesocosm == 8 and group == 'Ciliate'").mean_change_vs_T3_percent.iloc[0]:.1f}% zeigt. Bei 500 Concrete (M9) beträgt der entsprechende Wert {group_effects.query("mesocosm == 9 and group == 'Ciliate'").mean_change_vs_T3_percent.iloc[0]:.1f}%, bei 500 NaOH (M2) {group_effects.query("mesocosm == 2 and group == 'Ciliate'").mean_change_vs_T3_percent.iloc[0]:.1f}%. Diese Unterschiede sind Beobachtungsmuster und keine replizierten Treatmentmittelwerte.

Ein unabhängiger statistischer Treatmentvergleich ist nicht möglich, weil jede Kombination aus Dosis und Material nur in einem Mesokosmos vorkommt. Die deskriptiven Einzelverläufe und Effekte bleiben dennoch für die Ergebnisdarstellung relevant; Treatment und Mesokosmos müssen dabei als konfundiert bezeichnet werden.

### Zusätzliche deskriptive Tests

**AUC und Zeitpunkt des Minimums:** Die Fläche unter der Nachbehandlungskurve (T5–T31) und das Minimum der Gesamtzellzahl zeigen die integrierte Besiedlungsstärke und den Zeitpunkt der stärksten Abnahme:

{auc_rows}

**Ciliaten-Dinoflagellaten-Verhältnis:** Nach T4 lag der mittlere Ciliatenanteil bzw. das mittlere Ciliaten-Dinoflagellaten-Verhältnis je Mesokosmos bei:

{ratio_summary}

**Kontrollbasierte Treatmentabweichung:** Die Treatments wurden zusätzlich gegen die jeweils passende Kontrolle verglichen (Concrete gegen M3, NaOH gegen M6). Ein Verhältnis über 1 bedeutet höhere Zellzahlen im Treatment:

{control_summary}

**Gewinner und Verlierer einzelner Kategorien:** Kategorien mit einer mittleren Veränderung von mindestens +25 % gegenüber T3 wurden als deskriptive Gewinner, Kategorien mit höchstens −25 % als Verlierer klassifiziert. Die stärksten Beispiele sind:

Gewinner:
{winners}

Verlierer:
{losers}

**Zeitverzögerte Beziehungen:** Für Ciliaten und Dinoflagellaten wurden Korrelationen mit Verschiebungen von −4 bis +4 Probetagen berechnet. Der jeweils stärkste positive Zusammenhang je Mesokosmos war:

{lag_summary}

Diese sechs Tests dienen der Mustererkennung. Sie liefern keine unabhängigen Signifikanznachweise, können aber direkt als deskriptive Ergebnisse im Bericht verwendet werden.

### Ähnlichkeit der Mesokosmen: Zellzahlen oder Komposition?

An T1 lagen die Gesamtzellzahlen zwischen {t1.min_total_cells_L:.0f} und {t1.max_total_cells_L:.0f} Zellen L⁻¹ (CV: {t1.cv_total_cells:.1%}). Der Ciliatenanteil lag dagegen zwischen {t1.min_ciliate_share:.1%} und {t1.max_ciliate_share:.1%} (CV: {t1.cv_ciliate_share:.1%}). Die relative Komposition war an T1 somit ähnlicher als die absoluten Zellzahlen.

Von T1 bis T3 blieb dieses Muster grundsätzlich bestehen: Der mittlere CV der Gesamtzellzahl betrug {similarity[similarity.sample_day <= 3].cv_total_cells.mean():.1%}, der mittlere CV des Ciliatenanteils {similarity[similarity.sample_day <= 3].cv_ciliate_share.mean():.1%}. T2 war dabei der unähnlichste Vorbehandlungstag hinsichtlich der Komposition.

Über den gesamten Zeitraum bis T31 war die absolute Zellzahl geringfügig homogener als die Komposition (mittlerer CV: {similarity_mean_cv_counts:.1%} gegenüber {similarity_mean_cv_composition:.1%}; Median: {similarity_median_cv_counts:.1%} gegenüber {similarity_median_cv_composition:.1%}). Nach T4 nahm die Heterogenität der Komposition jedoch deutlich zu. An T31 betrug der CV der Gesamtzellzahl {t31.cv_total_cells:.1%}, während der CV des Ciliatenanteils {t31.cv_ciliate_share:.1%} erreichte; der Ciliatenanteil lag dabei zwischen {t31.min_ciliate_share:.1%} und {t31.max_ciliate_share:.1%}.

Damit waren die Mesokosmen vor der Behandlung kompositorisch ähnlicher als hinsichtlich ihrer absoluten Zellzahlen. Bis T31 entwickelten sie sich insbesondere in der Ciliaten-/Dinoflagellaten-Zusammensetzung zunehmend auseinander.

### Ciliaten, Dinoflagellaten und Größenklassen

Ciliaten und Dinoflagellaten wurden getrennt sowie als Gesamtzellzahl ausgewertet. Zusätzlich wurden die Größenklassen <30 µm und >30 µm separat aggregiert. Dadurch werden spezifische Kategorien und Unknown-Kategorien innerhalb der jeweiligen Hauptgruppe addiert, ohne Zellen doppelt zu zählen. Die häufigsten Kategorien über alle Proben sind:

{top}

### Einzelkategorien

Die vollständige Tabelle der deskriptiven Effekte jeder einzelnen Kategorie befindet sich in `microzooplankton_analysis.xlsx`, Blatt `Effekt_Kategorien`. Besonders hohe oder niedrige Werte können dort anhand der mittleren Veränderung gegenüber T3 und des T31-Wertes identifiziert werden. Die Tabelle berücksichtigt weiterhin die Regel, dass jede Zelle nur einer spezifischen Kategorie und damit genau einer Hauptgruppe zugeordnet wird.

## Datenprüfung

Die Prüfung bestätigt {len(observations.sheet.unique())} Arbeitsblätter, {observations.mesocosm.nunique()} Mesokosmen und {observations.sample_day.nunique()} Probetage. Insgesamt wurden {missing_count} Count-Zeilen mit 0 bzw. leerem Feld als kein Fund behandelt. Biomasse- oder bereits berechnete Cells/L-Spalten wurden nicht für die Ergebnisse verwendet.

## Dateien

- `microzooplankton_analysis.xlsx`: alle Rohzählungen, Aggregationen, Vorbehandlung, Kontrollen, Treatment-Normalisierung sowie deskriptive Effekte für Gesamt, Hauptgruppen, Größenklassen und Einzelkategorien.
- `figures/01_zeitverlauf.png`: Gesamtzellzahl, Ciliaten und Dinoflagellaten im Zeitverlauf.
- `figures/02_normalisiert_T3.png`: Veränderungen relativ zum letzten Vorbehandlungstag.
- `figures/03_kontrollen.png`: M3 und M6.
- `figures/04_ciliaten_groessenklassen.png`: Ciliaten nach Größe.
"""
    (RESULTS_DIR / "microzooplankton_analysis.md").write_text(report, encoding="utf-8")


def main() -> None:
    if not WORKBOOK.exists():
        raise FileNotFoundError(WORKBOOK)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    observations = load_counts()
    total = aggregate(observations, include_total=True)
    groups = aggregate(observations)
    sizes = aggregate_sizes(observations)
    trends = pre_treatment_trends(total, groups)
    normalized = normalized_changes(groups)
    effects = treatment_summary(normalized)
    controls = control_comparison(total, groups)
    categories = category_summary(observations)
    quality = quality_summary(observations)
    save_figures(total, groups, sizes)
    write_outputs(
        observations, total, groups, sizes, trends, normalized, effects, controls, categories, quality
    )
    print(f"Ergebnisse: {RESULTS_DIR}")
    print(f"Beobachtungszeilen: {len(observations)}")


if __name__ == "__main__":
    main()
