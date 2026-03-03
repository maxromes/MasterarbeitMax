#!/usr/bin/env python3
"""
Detaillierte Validierung der cut_47min Dateien.
Prüft:
- Taxonomische Hierarchie Konsistenz
- Label-Name vs. Familie/Gattung/Art
- Anomalien und Besonderheiten
"""

import csv
from pathlib import Path
from collections import defaultdict

def validate_taxa_consistency(filepath):
    """Detaillierte Taxa-Validierung."""
    issues = []
    stats = {
        'filename': filepath.name,
        'total': 0,
        'genus_level': 0,  # "Genus X" Einträge
        'family_level': 0,  # nur Familie, keine Art
        'full_taxa': 0,    # Familie + Gattung + Art
        'inconsistencies': 0,
        'unique_families': set(),
        'unique_genera': set(),
    }
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader, start=2):
            stats['total'] += 1
            
            label = row.get('label_name', '').strip()
            family = row.get('family', '').strip()
            genus = row.get('genus', '').strip()
            species = row.get('species', '').strip()
            
            if family:
                stats['unique_families'].add(family)
            if genus:
                stats['unique_genera'].add(genus)
            
            # Klassifizifiere Einträge
            if label.startswith('Genus '):
                stats['genus_level'] += 1
            elif family and not genus and not species:
                stats['family_level'] += 1
            elif family and genus and species:
                stats['full_taxa'] += 1
            
            # Prüfe auf Inkonsistenzen
            # Wenn Full-Taxa Entry, sollte Species im Label vorkommen
            if family and genus and species:
                if species not in label and family not in label:
                    stats['inconsistencies'] += 1
                    if stats['inconsistencies'] <= 2:
                        issues.append(f"    Zeile {i}: '{label}' | {genus} | {species}")
    
    return stats, issues

# Hauptlogik
cut_47min_path = Path('normalized_reports/cut_47min')
all_files = sorted(cut_47min_path.rglob('*.csv'))

print("\n" + "=" * 90)
print("TAXONOMISCHE VALIDIERUNG - CUT_47MIN")
print("=" * 90)

family_count = defaultdict(int)
genus_count = defaultdict(int)
pattern_summary = defaultdict(int)

for filepath in all_files:
    stats, issues = validate_taxa_consistency(filepath)
    
    pattern_summary['genus_level'] += stats['genus_level']
    pattern_summary['family_level'] += stats['family_level']
    pattern_summary['full_taxa'] += stats['full_taxa']
    
    for fam in stats['unique_families']:
        family_count[fam] += stats['total']
    for gen in stats['unique_genera']:
        genus_count[gen] += stats['total']
    
    # Nur Dateien mit Besonderheiten anzeigen
    if stats['genus_level'] > 0 or stats['family_level'] > 0 or issues:
        print(f"\n{filepath.parent.name}/{stats['filename']}")
        print(f"  Total: {stats['total']} | Genus-Level: {stats['genus_level']} | " +
              f"Family-Level: {stats['family_level']} | Full-Taxa: {stats['full_taxa']}")
        if issues:
            print(f"  ⚠️  Mögliche Inkonsistenzen:")
            for issue in issues:
                print(issue)

print("\n" + "=" * 90)
print("GLOBAL SUMMARY")
print("=" * 90)
print(f"Genus-Level Einträge (z.B. 'Genus Chromis'): {pattern_summary['genus_level']}")
print(f"Family-Level Einträge (z.B. nur 'Labridae'): {pattern_summary['family_level']}")
print(f"Full-Taxa Einträge (Familie + Gattung + Art): {pattern_summary['full_taxa']}")
print(f"\nTotal Unique Families: {len(family_count)}")
print(f"Total Unique Genera: {len(genus_count)}")

# Top Families
print("\n📊 Top 10 Families:")
for fam, count in sorted(family_count.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {fam}: ~{count} Vorkommen")

print("\n✓ Validierung abgeschlossen")
