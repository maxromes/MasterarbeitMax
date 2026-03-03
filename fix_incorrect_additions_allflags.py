import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ALL_FLAGS_ROOT = ROOT / "normalized_reports" / "all_with_flags"

# Finde WIRKLICH betroffene Dateien mit included_47min=FALSE
correct_chromis_files = set()
correct_halfnhalf_files = set()

for area in ["Annotation_reports_coral_reef", "Annotation_reports_Nursery"]:
    area_path = ALL_FLAGS_ROOT / area
    if not area_path.exists():
        continue
    
    for csv_file in area_path.glob("*.csv"):
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                included = row.get('included_47min', '').strip()
                label = row.get('label_name', '').strip()
                
                if included == 'FALSE':
                    if label == 'Genus Chromis':
                        correct_chromis_files.add(csv_file.name)
                    elif label == 'Indian Half-and-Half (Pycnochromis dimidiatus)':
                        correct_halfnhalf_files.add(csv_file.name)

print(f"Korrekte Dateien mit Genus Chromis nach 47min: {len(correct_chromis_files)}")
print(f"Korrekte Dateien mit Indian Half-and-Half nach 47min: {len(correct_halfnhalf_files)}")

# Entferne falsche Eintragungen aus all_with_flags
files_fixed = 0
incorrect_entries_removed = 0

for area in ["Annotation_reports_coral_reef", "Annotation_reports_Nursery"]:
    area_path = ALL_FLAGS_ROOT / area
    if not area_path.exists():
        continue
    
    for csv_file in sorted(area_path.glob("*.csv")):
        filename = csv_file.name
        
        # Überprüfe, ob diese Datei korrekt hätte modifiziert werden sollen
        should_have_chromis = filename in correct_chromis_files
        should_have_halfnhalf = filename in correct_halfnhalf_files
        
        # Lese Datei
        with open(csv_file, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows = list(reader)
        
        # Filtere falsche Einträge
        cleaned_rows = []
        removed = 0
        
        for row in rows:
            vid = row.get('video_annotation_label_id', '')
            label = row.get('label_name', '')
            
            # Entferne 999000001 wenn Chromis nicht hätte hinzugefügt werden sollen
            if vid == '999000001' and not should_have_chromis:
                print(f"  REMOVE: {filename} - Genus Chromis (nicht berechtigt)")
                removed += 1
                continue
            
            # Entferne 999000002 wenn Half-and-Half nicht hätte hinzugefügt werden sollen
            if vid == '999000002' and not should_have_halfnhalf:
                print(f"  REMOVE: {filename} - Indian Half-and-Half (nicht berechtigt)")
                removed += 1
                continue
            
            cleaned_rows.append(row)
        
        if removed > 0:
            # Schreibe zurück
            with open(csv_file, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(cleaned_rows)
            
            files_fixed += 1
            incorrect_entries_removed += removed

print(f"\n✓ Betroffene all_with_flags Dateien korrigiert: {files_fixed}")
print(f"✓ Falsch hinzugefügte Einträge entfernt: {incorrect_entries_removed}")
