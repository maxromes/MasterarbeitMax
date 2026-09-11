from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from mikrozooplankton_gran_canaria_2026.config import EXCEL_PATH, RESULTS_DIR


def main() -> None:
    if not EXCEL_PATH.exists():
        raise FileNotFoundError(
            f"Keine Excel-Datei gefunden: {EXCEL_PATH}\n"
            "Bitte die Rohdatei unter data/raw/ ablegen oder EXCEL_FILENAME anpassen."
        )

    workbook = pd.ExcelFile(EXCEL_PATH)
    overview = []
    for sheet_name in workbook.sheet_names:
        frame = pd.read_excel(EXCEL_PATH, sheet_name=sheet_name)
        overview.append(
            {
                "arbeitsblatt": sheet_name,
                "zeilen": len(frame),
                "spalten": len(frame.columns),
                "spaltennamen": " | ".join(str(column) for column in frame.columns),
            }
        )

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = RESULTS_DIR / "excel_uebersicht.csv"
    pd.DataFrame(overview).to_csv(output_path, index=False)
    print(f"Excel-Datei geprueft: {EXCEL_PATH}")
    print(f"Uebersicht geschrieben: {output_path}")


if __name__ == "__main__":
    main()
