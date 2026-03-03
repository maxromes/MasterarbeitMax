#!/usr/bin/env python3
"""
Reduziere cut_47min Dateien auf die 10 Rohdaten-Spalten.
Behält alle Zeilen, entfernt nur die Extra-Berechnungsspalten.
"""

import csv
import os
from pathlib import Path

# Spalten die behalten werden (die ersten 10)
KEEP_COLUMNS = [
    'video_annotation_label_id',
    'label_name',
    'label_hierarchy',
    'unspecific',
    'family',
    'genus',
    'species',
    'interested',
    'feeding',
    'frames'
]

def reduce_file(input_file, output_file):
    """Reduziere eine CSV-Datei auf die 10 Rohdaten-Spalten."""
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        # Schreibe mit nur den gewünschten Spalten
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=KEEP_COLUMNS)
            writer.writeheader()
            
            kept_count = 0
            for row in reader:
                # Erstelle neue Row mit nur den gewünschten Spalten
                new_row = {col: row.get(col, '') for col in KEEP_COLUMNS}
                writer.writerow(new_row)
                kept_count += 1
    
    return kept_count

# Verarbeite alle Dateien
cut_47min_path = Path('normalized_reports/cut_47min')

for csv_file in cut_47min_path.rglob('*.csv'):
    try:
        count = reduce_file(csv_file, csv_file)
        print(f"✓ {csv_file.name} - {count} Zeilen behalten, auf 10 Spalten reduziert")
    except Exception as e:
        print(f"✗ {csv_file.name} - Fehler: {e}")

print("\n✓ Alle Dateien verarbeitet!")
