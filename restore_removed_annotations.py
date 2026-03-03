import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CUT_47MIN_ROOT = ROOT / "normalized_reports" / "cut_47min"
ALL_FLAGS_ROOT = ROOT / "normalized_reports" / "all_with_flags"

# Dateien mit entfernten Annotationen und ihren Arten
correct_files = {
    "20241105-milimani-ulva_salad.csv": ("chromis", "halfnhalf"),
    "20241111-utumbi-control.csv": ("chromis", "halfnhalf"),
    "20241124-utumbi-mackerel.csv": ("chromis",),
    "20241129-utumbi-sargassum.csv": ("chromis",),
    "20241210-milimani-fischmix.csv": ("chromis",),
    "20241112-utumbi-ulva_gutweed.csv": ("halfnhalf",),
}

total_added = 0
files_processed = 0

for filename, species_to_include in correct_files.items():
    print(f"\nProcessing {filename}...")
    
    # Finde in welchem Bereich die Datei ist
    for area in ["Annotation_reports_coral_reef", "Annotation_reports_Nursery"]:
        all_flags_file = ALL_FLAGS_ROOT / area / filename
        cut_file = CUT_47MIN_ROOT / area / filename
        
        if not all_flags_file.exists():
            continue
        
        # Lese all_with_flags
        with open(all_flags_file, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            all_flags_rows = list(reader)
        
        # Filtere entfernte Zeilen (included_47min=FALSE)
        removed_rows = []
        for row in all_flags_rows:
            if row.get('included_47min') == 'FALSE':
                label = row.get('label_name', '').strip()
                if label == 'Genus Chromis' and "chromis" in species_to_include:
                    removed_rows.append(row)
                elif label == 'Indian Half-and-Half (Pycnochromis dimidiatus)' and "halfnhalf" in species_to_include:
                    removed_rows.append(row)
        
        if not removed_rows:
            continue
        
        # Lese cut_47min
        with open(cut_file, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            cut_rows = list(reader)
        
        # Entferne die 999000001 und 999000002 Platzhalter (falls vorhanden)
        cut_rows = [r for r in cut_rows if r.get('video_annotation_label_id', '') not in ('999000001', '999000002')]
        
        # Kombiniere: entfernte Zeilen + enthaltene Zeilen
        combined_rows = removed_rows + cut_rows
        
        # Sortiere nach time_sec_local_max
        try:
            combined_rows.sort(key=lambda r: float(r.get('time_sec_local_max', '0')))
        except:
            pass
        
        # Schreibe zurück
        with open(cut_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(combined_rows)
        
        print(f"  ✓ {len(removed_rows)} entfernte Zeilen hinzugefügt")
        total_added += len(removed_rows)
        files_processed += 1
        break

print(f"\n✓ {files_processed} Dateien verarbeitet")
print(f"✓ Gesamt: {total_added} entfernte Zeilen zu cut_47min hinzugefügt")
