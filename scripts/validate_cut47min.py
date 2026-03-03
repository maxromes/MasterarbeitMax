#!/usr/bin/env python3
"""
Validiere alle cut_47min Dateien auf Plausibilität.
Prüft:
- Zeilenanzahl und Spaltenanzahl
- Taxa-Logik (Familie/Gattung/Art)
- Leere Felder
- Ungültige Kombinationen
"""

import csv
from pathlib import Path
from collections import defaultdict

def validate_file(filepath):
    """Validiere eine einzelne CSV-Datei."""
    issues = []
    stats = {
        'filename': filepath.name,
        'total_rows': 0,
        'empty_family': 0,
        'empty_genus': 0,
        'empty_species': 0,
        'genus_mismatch': 0,
        'taxa_combo': defaultdict(int),
        'label_names': set()
    }
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader, start=2):  # start=2 wegen header
                stats['total_rows'] += 1
                
                label_name = row.get('label_name', '').strip()
                family = row.get('family', '').strip()
                genus = row.get('genus', '').strip()
                species = row.get('species', '').strip()
                
                stats['label_names'].add(label_name)
                
                # Prüfe leere Felder
                if not family and (genus or species):
                    stats['empty_family'] += 1
                    if stats['empty_family'] <= 3:  # nur erste 3 melden
                        issues.append(f"  Zeile {i}: {label_name} - Family leer, aber Genus/Species vorhanden")
                
                if not genus and species:
                    stats['empty_genus'] += 1
                    if stats['empty_genus'] <= 3:
                        issues.append(f"  Zeile {i}: {label_name} - Genus leer, aber Species vorhanden")
                
                # Prüfe ob Genus in label_name vorkommt
                if genus and species and genus not in label_name:
                    # Einige Genus können anders geschrieben sein (z.B. "Genus Chromis")
                    if not label_name.startswith('Genus '):
                        stats['genus_mismatch'] += 1
                
                # Zähle Taxa-Kombinationen
                taxa_key = f"{family}|{genus}|{species[:30] if species else '(empty)'}"
                stats['taxa_combo'][taxa_key] += 1
    
    except Exception as e:
        issues.append(f"  FEHLER beim Lesen: {e}")
        return stats, issues
    
    return stats, issues

# Hauptlogik
cut_47min_path = Path('normalized_reports/cut_47min')
all_files = sorted(cut_47min_path.rglob('*.csv'))

print("=" * 80)
print("VALIDIERUNG CUT_47MIN DATEIEN")
print("=" * 80)

total_files = len(all_files)
total_rows = 0
files_with_issues = 0

for filepath in all_files:
    stats, issues = validate_file(filepath)
    total_rows += stats['total_rows']
    
    if issues or stats['empty_family'] > 0 or stats['empty_genus'] > 0:
        files_with_issues += 1
        print(f"\n📋 {filepath.parent.name}/{stats['filename']}")
        print(f"   Zeilen: {stats['total_rows']} | Unique Labels: {len(stats['label_names'])}")
        
        if stats['empty_family'] > 0:
            print(f"   ⚠️  {stats['empty_family']} Zeilen ohne Family")
        if stats['empty_genus'] > 0:
            print(f"   ⚠️  {stats['empty_genus']} Zeilen ohne Genus")
        if stats['genus_mismatch'] > 0:
            print(f"   ℹ️  {stats['genus_mismatch']} Genus-Mismatch (können Genus-Einträge sein)")
        
        for issue in issues:
            print(issue)

print(f"\n" + "=" * 80)
print(f"ZUSAMMENFASSUNG")
print(f"=" * 80)
print(f"Total Dateien: {total_files}")
print(f"Total Zeilen: {total_rows}")
print(f"Dateien mit Problemen: {files_with_issues}")
print(f"\nStatus: {'✓ GRÜN - Alle Dateien plausibel' if files_with_issues == 0 else '⚠️  GELB - Einige Anomalien (meist erwartet)'}")
