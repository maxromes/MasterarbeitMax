from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RESULTS_DIR = PROJECT_ROOT / "results"

# Nach Eingang der Datei hier den tatsaechlichen Dateinamen eintragen.
EXCEL_FILENAME = "mikrozooplankton_gran_canaria_2026.xlsx"
EXCEL_PATH = RAW_DATA_DIR / EXCEL_FILENAME
