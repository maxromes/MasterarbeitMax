from __future__ import annotations

import re
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_DIR = Path(__file__).resolve().parents[1]
WORKBOOK = PROJECT_DIR / "MicroZP_Gran_Canaria_2026_MaxRomes_AntoniaKirner (1).xlsx"
PROTOCOL_WORKBOOK = PROJECT_DIR / "MicroZP_Kosmos_GC_2026_Max_Romes.xlsx"
RESULTS_DIR = PROJECT_DIR / "results" / "microzooplankton_overview"
FIGURES_DIR = RESULTS_DIR / "figures"
SELECTED_MESOCOSMS = {1, 2, 3, 6, 8, 9}
CILIATE_GENERA = {"Strombidium", "Strobilidium", "Tintinnid", "Mesodinium"}


def parse_sheet_metadata(sheet_name: str) -> tuple[int, int] | None:
    match = re.search(r"_M(\d+)_T(\d+)_", sheet_name)
    if match is None:
        return None
    mesocosm, day = map(int, match.groups())
    if mesocosm not in SELECTED_MESOCOSMS:
        return None
    return mesocosm, day


def load_ciliate_data() -> pd.DataFrame:
    workbook = pd.ExcelFile(WORKBOOK)
    records: list[dict[str, object]] = []
    for sheet_name in workbook.sheet_names[2:]:
        metadata = parse_sheet_metadata(sheet_name)
        if metadata is None:
            continue
        mesocosm, day = metadata
        frame = pd.read_excel(WORKBOOK, sheet_name=sheet_name)
        if "Taxa" in frame.columns:
            ciliate_mask = frame["Taxa"].astype("string").str.casefold().eq("ciliate")
        elif "Genus" in frame.columns:
            # Later worksheets omit the Taxa column; their ciliate genera are
            # retained and are unambiguous against the dinoflagellate genera.
            ciliate_mask = frame["Genus"].isin(CILIATE_GENERA)
        else:
            raise ValueError(f"Keine Taxonomie-Spalte in {sheet_name}.")
        ciliate = frame.loc[ciliate_mask].copy()
        if ciliate.empty:
            records.append(
                {
                    "mesocosm": mesocosm,
                    "sample_day": day,
                    "sheet": sheet_name,
                    "ciliate_cells_L": 0.0,
                    "ciliate_biomass_ugC_L": 0.0,
                    "small_cells_L": 0.0,
                    "large_cells_L": 0.0,
                    "weighted_mean_volume_um3": float("nan"),
                    "ciliate_taxa": 0,
                }
            )
            continue

        cells = pd.to_numeric(ciliate["Cells_L"], errors="coerce").fillna(0)
        biomass = pd.to_numeric(ciliate["Biomass_µgC/L"], errors="coerce").fillna(0)
        volume = pd.to_numeric(ciliate["MeanV_µm3"], errors="coerce")
        size_class = ciliate["Species_SizeClass"].astype("string")
        total_cells = cells.sum()
        weighted_volume = (
            (cells * volume.fillna(0)).sum() / total_cells
            if total_cells > 0
            else float("nan")
        )
        records.append(
            {
                "mesocosm": mesocosm,
                "sample_day": day,
                "sheet": sheet_name,
                "ciliate_cells_L": total_cells,
                "ciliate_biomass_ugC_L": biomass.sum(),
                "small_cells_L": cells.where(size_class.str.contains("<30", na=False), 0).sum(),
                "large_cells_L": cells.where(size_class.str.contains(">30", na=False), 0).sum(),
                "weighted_mean_volume_um3": weighted_volume,
                "ciliate_taxa": int(ciliate["Species_SizeClass"].dropna().nunique()),
            }
        )

    data = pd.DataFrame(records).sort_values(["mesocosm", "sample_day"])
    if len(data) != len(SELECTED_MESOCOSMS) * 12:
        raise ValueError(
            f"Erwartet wurden 72 ausgewertete Proben, gefunden wurden {len(data)}."
        )
    return data


def load_metadata() -> pd.DataFrame:
    main = pd.read_excel(WORKBOOK, sheet_name="MainTable")
    main = main.loc[main["Mesocosm"].isin(SELECTED_MESOCOSMS)].copy()
    main["mesocosm"] = main["Mesocosm"].astype(int)
    protocol = pd.read_excel(PROTOCOL_WORKBOOK, sheet_name="Protocol", header=None)
    protocol_treatments = {
        int(str(protocol.iloc[1, column]).removeprefix("M")): str(protocol.iloc[0, column])
        for column in range(protocol.shape[1])
        if str(protocol.iloc[1, column]).startswith("M")
        and pd.notna(protocol.iloc[0, column])
    }
    main["treatment"] = main["mesocosm"].map(protocol_treatments)
    metadata = (
        main.loc[main["Day"].isin([1, 5, 9, 17, 33]), ["mesocosm", "Day", "treatment", "Mineral"]]
        .rename(columns={"Day": "sample_day"})
        .sort_values(["mesocosm", "sample_day"])
    )
    return metadata


def add_labels(data: pd.DataFrame, metadata: pd.DataFrame) -> pd.DataFrame:
    treatment = (
        metadata[["mesocosm", "treatment", "Mineral"]]
        .drop_duplicates()
    )
    return data.merge(treatment, on="mesocosm", how="left", validate="many_to_one")


def make_overview(data: pd.DataFrame) -> pd.DataFrame:
    return (
        data.groupby(["mesocosm", "treatment", "Mineral"], as_index=False)
        .agg(
            n_samples=("sample_day", "size"),
            sample_days=("sample_day", lambda values: ", ".join(map(str, values))),
            source_sheets=("sheet", lambda values: " | ".join(values)),
        )
        .sort_values("mesocosm")
    )


def line_plot(
    data: pd.DataFrame,
    y: str,
    ylabel: str,
    filename: str,
    log_scale: bool = False,
) -> None:
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=data,
        x="sample_day",
        y=y,
        hue="treatment",
        style="mesocosm",
        markers=True,
        dashes=False,
        linewidth=1.8,
        palette="tab10",
    )
    plt.xlabel("Probetag")
    plt.ylabel(ylabel)
    if log_scale:
        plt.yscale("log")
    plt.title(ylabel + " der sechs ausgewerteten Mesokosmen")
    plt.grid(alpha=0.25)
    plt.legend(title="Treatment / Mesokosmos", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / filename, dpi=300)
    plt.close()


def make_figures(data: pd.DataFrame, metadata: pd.DataFrame) -> None:
    sns.set_theme(style="whitegrid", context="notebook")
    line_plot(
        data,
        "ciliate_cells_L",
        "Ciliatenkonzentration (Zellen L$^{-1}$)",
        "01_ciliate_cells_over_time.png",
        log_scale=True,
    )
    line_plot(
        data,
        "ciliate_biomass_ugC_L",
        "Ciliatenbiomasse (µg C L$^{-1}$)",
        "02_ciliate_biomass_over_time.png",
        log_scale=True,
    )
    line_plot(
        data,
        "weighted_mean_volume_um3",
        "Zellvolumen, zellzahl-gewichtetes Mittel (µm³)",
        "03_ciliate_mean_size_over_time.png",
        log_scale=True,
    )

    size = data.melt(
        id_vars=["mesocosm", "sample_day", "treatment"],
        value_vars=["small_cells_L", "large_cells_L"],
        var_name="size_class",
        value_name="cells_L",
    )
    size["size_class"] = size["size_class"].map(
        {"small_cells_L": "<30 µm", "large_cells_L": ">30 µm"}
    )
    plt.figure(figsize=(10, 6))
    sns.lineplot(
        data=size,
        x="sample_day",
        y="cells_L",
        hue="size_class",
        style="mesocosm",
        markers=True,
        dashes=False,
        linewidth=1.5,
    )
    plt.yscale("log")
    plt.xlabel("Probetag")
    plt.ylabel("Ciliatenkonzentration (Zellen L$^{-1}$)")
    plt.title("Ciliaten-Größenklassen im Zeitverlauf")
    plt.grid(alpha=0.25)
    plt.legend(title="Größenklasse / Mesokosmos", bbox_to_anchor=(1.02, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "04_ciliate_size_classes_over_time.png", dpi=300)
    plt.close()

def main() -> None:
    if not WORKBOOK.exists():
        raise FileNotFoundError(f"Excel-Datei nicht gefunden: {WORKBOOK}")
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    metadata = load_metadata()
    data = add_labels(load_ciliate_data(), metadata)
    make_overview(data).to_csv(RESULTS_DIR / "microzooplankton_overview.csv", index=False)

    print(f"Ausgewertete Proben: {len(data)}")
    print(f"Mesokosmen: {sorted(data['mesocosm'].unique())}")
    print(f"Ergebnisse: {RESULTS_DIR}")


if __name__ == "__main__":
    main()
