#!/usr/bin/env python3
"""
Manuell ein split video auf 47 Minuten zuschneiden,
aber Genus Chromis und Indian Half-and-Half behalten
"""
import csv
import sys
from pathlib import Path

def process_split_video(input_file, cutoff_id, output_file):
    """
    Filtert Annotations basierend auf video_annotation_label_id
    Behält alle <= cutoff_id und alle Genus Chromis/Indian Half-and-Half
    """
    kept_rows = []
    removed_rows = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        
        for row in reader:
            video_id = int(row['video_annotation_label_id'])
            label_name = row['label_name']
            
            # Behalte wenn:
            # 1. ID <= cutoff_id ODER
            # 2. Species enthält "Genus Chromis" oder "Indian Half-and-Half"
            if video_id <= cutoff_id or 'Genus Chromis' in label_name or 'Indian Half-and-Half' in label_name:
                kept_rows.append(row)
            else:
                removed_rows.append(row)
    
    # Schreibe Output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(kept_rows)
    
    return len(kept_rows), len(removed_rows)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: python manual_split_video_cutoff.py <input_file> <cutoff_id> <output_file>")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    cutoff_id = int(sys.argv[2])
    output_file = Path(sys.argv[3])
    
    kept, removed = process_split_video(input_file, cutoff_id, output_file)
    
    print(f"✓ {input_file.name}")
    print(f"  Behalten: {kept} Zeilen (inkl. Header)")
    print(f"  Entfernt: {removed} Zeilen")
    print(f"  Gespeichert: {output_file}")
