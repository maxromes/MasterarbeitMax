#!/usr/bin/env python3
"""
Erstellt Zeitachsen-Grafiken aus Rohdaten-Annotations.
Zeigt den zeitlichen Verlauf der neuen Annotations bei Videos.
"""

import os
import csv
import json
from pathlib import Path
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import numpy as np
import pandas as pd
from datetime import datetime

# Konfiguration
CORAL_REEF_DIR = "Annotation_reports_coral_reef"
MAX_VIDEO_DURATION = 3600  # 60 Minuten in Sekunden
MIN_ANNOTATIONS = 50  # Mindestens 50 Annotations für sinnvoll Visualisierung
OUTPUT_DIR = "results/timeline_visualizations"

def extract_frame_time(frame_str):
    """Extrahiert die Zeitwert aus frame string z.B. '[123.456]'"""
    try:
        return float(frame_str.strip('[]'))
    except (ValueError, TypeError):
        return None

def seconds_to_minutes(seconds):
    """Konvertiert Sekunden zu Minuten:Sekunden Format"""
    if seconds is None:
        return None
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"

def get_video_info(csv_path):
    """Liest Video-Informationen aus CSV"""
    annotations = []
    species_seen = {}  # Trackt first seen time für jede Art
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                frame_str = row.get('frames', '')
                frame_time = extract_frame_time(frame_str)
                
                if frame_time is None:
                    continue
                    
                species = row.get('species', '')
                label_name = row.get('label_name', '')
                
                annotations.append({
                    'time': frame_time,
                    'species': species,
                    'label_name': label_name,
                    'genus': row.get('genus', '')
                })
                
                # Tracke first seen für jede Art
                key = f"{row.get('family', '')}|{label_name}"
                if key not in species_seen or frame_time < species_seen[key]['time']:
                    species_seen[key] = {
                        'time': frame_time,
                        'species': species,
                        'label_name': label_name
                    }
        
        return {
            'annotations': sorted(annotations, key=lambda x: x['time']),
            'first_seen': species_seen,
            'max_time': max([a['time'] for a in annotations]) if annotations else 0,
            'total_annotations': len(annotations)
        }
    except Exception as e:
        print(f"Fehler beim Lesen {csv_path}: {e}")
        return None

def find_videos_to_visualize():
    """Findet lange Videos mit kontinuierlichen Zeiten"""
    videos = []
    
    if not os.path.exists(CORAL_REEF_DIR):
        print(f"Verzeichnis nicht gefunden: {CORAL_REEF_DIR}")
        return []
    
    for csv_file in sorted(os.listdir(CORAL_REEF_DIR)):
        if not csv_file.endswith('.csv'):
            continue
        
        file_path = os.path.join(CORAL_REEF_DIR, csv_file)
        info = get_video_info(file_path)
        
        if info is None or info['total_annotations'] < MIN_ANNOTATIONS:
            continue
        
        # Filter: Videos bis 60 Min mit genug Annotations
        if info['max_time'] <= MAX_VIDEO_DURATION:
            videos.append({
                'name': csv_file,
                'path': file_path,
                'duration': info['max_time'],
                'annotations': info['annotations'],
                'first_seen': info['first_seen'],
                'total_annotations': info['total_annotations']
            })
    
    # Sortiere after duration
    videos.sort(key=lambda x: x['duration'], reverse=True)
    return videos

def create_timeline_plot(video_info, output_path):
    """
    Erstellt ein Timeline-Plot: Wann erste Annotation einer Art erscheint.
    """
    fig, ax = plt.subplots(figsize=(16, 10))
    
    video_name = video_info['name'].replace('.csv', '')
    duration_min = seconds_to_minutes(video_info['duration'])
    
    # Extrahiere first-seen Daten
    first_seen_list = sorted(
        video_info['first_seen'].items(),
        key=lambda x: x[1]['time']
    )
    
    x_times = []
    y_labels = []
    colors = []
    
    # Farbschema basierend auf Familie
    color_map = {}
    colors_palette = plt.cm.Set3(np.linspace(0, 1, 30))
    
    for idx, (key, data) in enumerate(first_seen_list):
        x_times.append(data['time'])
        label = data['label_name'][:30] + "..." if len(data['label_name']) > 30 else data['label_name']
        y_labels.append(label)
        
        # Farbiere nach Genus
        genus = key.split('|')[0]
        if genus not in color_map:
            color_map[genus] = colors_palette[len(color_map) % len(colors_palette)]
        colors.append(color_map[genus])
    
    # Plot als horizontales Punktdiagramm
    y_positions = np.arange(len(x_times))
    ax.scatter(x_times, y_positions, s=150, c=colors, alpha=0.7, edgecolors='black', linewidth=0.5)
    
    # Formatierung
    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels, fontsize=9)
    ax.set_xlabel('Video-Zeit (Sekunden)', fontsize=12, fontweight='bold')
    ax.set_title(f'First Seen Timeline: {video_name}\n({duration_min}, {len(first_seen_list)} verschiedene Arten)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # X-Achse: Zeit in Minuten
    def format_minutes(x, pos):
        return seconds_to_minutes(x) if x >= 0 else ''
    
    ax.xaxis.set_major_formatter(FuncFormatter(format_minutes))
    ax.xaxis.set_major_locator(plt.MultipleLocator(300))  # Alle 5 Minuten
    
    ax.grid(True, alpha=0.3, axis='x')
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Erstellt: {output_path}")
    plt.close()

def create_cumulative_plot(video_info, output_path):
    """
    Erstellt ein kumulatives Plot: Wie viele verschiedene Arten wurden bis zur Zeit T gesehen?
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    video_name = video_info['name'].replace('.csv', '')
    duration_min = seconds_to_minutes(video_info['duration'])
    
    # Sortiere Annotations nach Zeit
    sorted_annotations = sorted(video_info['annotations'], key=lambda x: x['time'])
    
    # Tracke unique species über Zeit
    unique_species = set()
    x_times = [0]
    y_counts = [0]
    
    for ann in sorted_annotations:
        species_key = f"{ann['genus']}|{ann['species']}"
        
        if species_key not in unique_species:
            unique_species.add(species_key)
            x_times.append(ann['time'])
            y_counts.append(len(unique_species))
    
    # Plotte
    ax.plot(x_times, y_counts, marker='o', linestyle='-', linewidth=2.5, 
            markersize=4, color='#2E86AB', label='Kumulative neue Arten')
    ax.fill_between(x_times, y_counts, alpha=0.3, color='#2E86AB')
    
    # Formatierung
    ax.set_xlabel('Video-Zeit (Minuten)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Anzahl unterschiedlicher Arten (kumulativ)', fontsize=12, fontweight='bold')
    ax.set_title(f'Kumulative Artenentdeckung: {video_name}\n({duration_min}, {video_info["total_annotations"]} Annotations insgesamt)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # X-Achse in Minuten
    def format_minutes(x, pos):
        return seconds_to_minutes(x)
    
    ax.xaxis.set_major_formatter(FuncFormatter(format_minutes))
    ax.xaxis.set_major_locator(plt.MultipleLocator(300))
    
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Erstellt: {output_path}")
    plt.close()

def create_density_plot(video_info, output_path):
    """
    Erstellt ein Densität-Plot: Wie dicht sind die Annotations über die Zeit verteilt?
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    video_name = video_info['name'].replace('.csv', '')
    duration_min = seconds_to_minutes(video_info['duration'])
    
    # Binne Annotations in 1-Minuten-Intervallen
    bin_size = 60  # 1 Minute
    bins = {}
    
    for ann in video_info['annotations']:
        bin_idx = int(ann['time'] // bin_size)
        bins[bin_idx] = bins.get(bin_idx, 0) + 1
    
    # Erstelle kontinuierliche Daten
    max_bin = int(video_info['duration'] // bin_size) + 1
    x_times = [i * bin_size for i in range(max_bin + 1)]
    y_counts = [bins.get(i, 0) for i in range(max_bin + 1)]
    
    # Plotte als Balkendiagramm
    ax.bar([t/60 for t in x_times[:-1]], y_counts[:-1], width=0.9, 
           color='#A23B72', alpha=0.7, edgecolor='black', linewidth=0.5)
    
    # Formatierung
    ax.set_xlabel('Video-Zeit (Minuten)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Anzahl Annotations pro Minute', fontsize=12, fontweight='bold')
    ax.set_title(f'Annotations-Dichte über Zeit: {video_name}\n({duration_min}, {video_info["total_annotations"]} Annotations insgesamt)', 
                 fontsize=14, fontweight='bold', pad=20)
    
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Erstellt: {output_path}")
    plt.close()

def generate_summary_report(videos):
    """Erstellt einen zusammenfassenden Bericht über alle Videos"""
    report_path = os.path.join(OUTPUT_DIR, "timeline_summary.txt")
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("TIMELINE VISUALISIERUNGEN - ZUSAMMENFASSUNG\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Analysierte Videos: {len(videos)}\n")
        f.write(f"Kriterien: max. 60 Min, min. 50 Annotations, kontinuierliche Zeitmessungen\n\n")
        
        for idx, video in enumerate(videos, 1):
            f.write(f"{idx}. {video['name']}\n")
            f.write(f"   Länge: {seconds_to_minutes(video['duration'])}\n")
            f.write(f"   Annotations: {video['total_annotations']}\n")
            f.write(f"   Verschiedene Arten: {len(video['first_seen'])}\n")
            f.write(f"   Grafiken: first_seen_timeline, cumulative, density\n\n")
    
    print(f"✓ Zusammenfassung: {report_path}")

def main():
    """Hauptfunktion"""
    # Erstelle Output-Verzeichnis
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("\n" + "=" * 60)
    print("TIMELINE VISUALISIERUNGEN ERSTELLEN")
    print("=" * 60 + "\n")
    
    # Finde Videos
    print("Suche Videos...")
    videos = find_videos_to_visualize()
    
    if not videos:
        print(f"Keine Videos gefunden (min. {MIN_ANNOTATIONS} Annotations pro Video)")
        return
    
    print(f"Gefunden: {len(videos)} Videos für Visualisierung\n")
    
    # Generiere Grafiken für jedes Video
    for video in videos:
        print(f"\nVerarbeite: {video['name']}")
        print(f"  - Länge: {seconds_to_minutes(video['duration'])}")
        print(f"  - Annotations: {video['total_annotations']}")
        print(f"  - Arten (first seen): {len(video['first_seen'])}")
        
        base_name = video['name'].replace('.csv', '')
        
        # Timeline der first-seen Annotations
        create_timeline_plot(
            video,
            os.path.join(OUTPUT_DIR, f"{base_name}_01_first_seen_timeline.png")
        )
        
        # Kumulatives Artenentdeckung-Plot
        create_cumulative_plot(
            video,
            os.path.join(OUTPUT_DIR, f"{base_name}_02_cumulative_species.png")
        )
        
        # Annotations-Dichte-Plot
        create_density_plot(
            video,
            os.path.join(OUTPUT_DIR, f"{base_name}_03_annotation_density.png")
        )
    
    # Erstelle Zusammenfassung
    generate_summary_report(videos)
    
    print("\n" + "=" * 60)
    print(f"✓ FERTIG! {len(videos) * 3} Grafiken erstellt.")
    print(f"Output-Verzeichnis: {OUTPUT_DIR}")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    main()
