import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ALL_FLAGS_ROOT = ROOT / "normalized_reports" / "all_with_flags"

# Read affected files
with open('/tmp/chromis_files.txt', 'r') as f:
    chromis_files = set(line.strip() for line in f if line.strip())

with open('/tmp/halfnhalf_files.txt', 'r') as f:
    halfnhalf_files = set(line.strip() for line in f if line.strip())

# Template annotations at second 1
GENUS_CHROMIS_TEMPLATE = {
    'video_annotation_label_id': '999000001',
    'label_name': 'Genus Chromis',
    'label_hierarchy': 'Small Ovals - Damselfishes > Damselfishes (Pomacentridae) > Genus Chromis',
    'unspecific': 'Small Ovals - Damselfishes',
    'family': 'Pomacentridae',
    'genus': 'Genus Chromis',
    'species': '',
    'interested': '',
    'feeding': '',
    'frames': '[1.0]',
    'time_sec_local': '[1.0]',
    'time_sec_local_first': '1.0',
    'time_sec_local_last': '1.0',
    'time_sec_local_max': '1.0',
    'included_47min': 'TRUE',
    'is_short_control_nursery': 'FALSE',
    'is_split_video': 'FALSE',
    'frames_kept_47min': '[1.0]',
    'frame_count_raw': '1',
    'frame_count_kept_47min': '1'
}

INDIAN_HALFNHALF_TEMPLATE = {
    'video_annotation_label_id': '999000002',
    'label_name': 'Indian Half-and-Half (Pycnochromis dimidiatus)',
    'label_hierarchy': 'Small Ovals - Damselfishes > Damselfishes (Pomacentridae) > Indian Half-and-Half (Pycnochromis dimidiatus)',
    'unspecific': 'Small Ovals - Damselfishes',
    'family': 'Pomacentridae',
    'genus': 'Pycnochromis',
    'species': 'Indian Half-and-Half (Pycnochromis dimidiatus)',
    'interested': '',
    'feeding': '',
    'frames': '[1.0]',
    'time_sec_local': '[1.0]',
    'time_sec_local_first': '1.0',
    'time_sec_local_last': '1.0',
    'time_sec_local_max': '1.0',
    'included_47min': 'TRUE',
    'is_short_control_nursery': 'FALSE',
    'is_split_video': 'FALSE',
    'frames_kept_47min': '[1.0]',
    'frame_count_raw': '1',
    'frame_count_kept_47min': '1'
}

files_modified = 0
annotations_added = 0

# Process each area
for area in ["Annotation_reports_coral_reef", "Annotation_reports_Nursery"]:
    area_path = ALL_FLAGS_ROOT / area
    if not area_path.exists():
        continue
    
    for csv_file in sorted(area_path.glob("*.csv")):
        filename = csv_file.name
        
        # Check if this file needs Genus Chromis or Indian Half-and-Half
        needs_chromis = filename in chromis_files
        needs_halfnhalf = filename in halfnhalf_files
        
        if not needs_chromis and not needs_halfnhalf:
            continue
        
        # Read existing data
        with open(csv_file, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames
            rows = list(reader)
        
        # Check if already added (ID 999000001 or 999000002)
        existing_ids = {row.get('video_annotation_label_id', '') for row in rows}
        if '999000001' in existing_ids and '999000002' in existing_ids:
            continue
        
        # Add annotations at the beginning
        new_rows = []
        added_this_file = 0
        
        if needs_chromis and '999000001' not in existing_ids:
            new_row = GENUS_CHROMIS_TEMPLATE.copy()
            if rows:
                new_row['is_short_control_nursery'] = rows[0].get('is_short_control_nursery', 'FALSE')
                new_row['is_split_video'] = rows[0].get('is_split_video', 'FALSE')
            new_rows.append(new_row)
            added_this_file += 1
        
        if needs_halfnhalf and '999000002' not in existing_ids:
            new_row = INDIAN_HALFNHALF_TEMPLATE.copy()
            if rows:
                new_row['is_short_control_nursery'] = rows[0].get('is_short_control_nursery', 'FALSE')
                new_row['is_split_video'] = rows[0].get('is_split_video', 'FALSE')
            new_rows.append(new_row)
            added_this_file += 1
        
        if added_this_file == 0:
            continue
        
        # Combine new rows with existing rows
        all_rows = new_rows + rows
        
        # Write back
        with open(csv_file, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_rows)
        
        files_modified += 1
        annotations_added += added_this_file
        print(f"✓ {filename}: +{added_this_file}")

print(f"\n✓ Modified {files_modified} files in all_with_flags")
print(f"✓ Added {annotations_added} annotations at second 1")
