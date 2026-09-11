# Mikrozooplankton Gran Canaria 2026

Eigenstaendiges Analyseprojekt fuer das Mikrozooplankton-Experiment auf Gran Canaria 2026.

## Projektstruktur

- `data/raw/`: unveraenderte Rohdaten, insbesondere Excel-Dateien
- `data/processed/`: aufbereitete Tabellen
- `scripts/`: ausfuehrbare Analyseskripte
- `src/mikrozooplankton_gran_canaria_2026/`: wiederverwendbare Python-Funktionen
- `results/`: Tabellen und Berichte
- `results/figures/`: Abbildungen
- `docs/`: Methodik und Projektdokumentation

## Start

```bash
cd /workspaces/Mikrozooplankton_Gran_Canaria_2026
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Lege die Excel-Rohdatei anschliessend unter `data/raw/` ab. Der erwartete Dateiname ist in `src/mikrozooplankton_gran_canaria_2026/config.py` zentral hinterlegt.

## Erste Analyse

```bash
python scripts/analyse_excel.py
```

Das Skript prueft die Excel-Arbeitsblaetter, schreibt eine strukturierte Uebersicht nach `results/excel_uebersicht.csv` und veraendert die Rohdatei nicht.

Die konkrete statistische Auswertung wird erst festgelegt, sobald Aufbau und Variablen der Excel-Datei bekannt sind.
