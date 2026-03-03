#!/usr/bin/env python3
"""
Erstellt zwei Visualisierungen für ein einzelnes Video:
1. First Seen: Wann erscheint jede Art zum ersten Mal?
2. MaxN: Wann wird die maximale Anzahl einer Art zur selben Zeit erreicht?

MaxN = Maximale Anzahl einer Art zum selben Frame/Zeitpunkt
"""

import os
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

# Konfiguration
CORAL_REEF_DIR = "Annotation_reports_coral_reef"
OUTPUT_DIR = "results/timeline_visualizations"
TARGET_DURATION = 3600  # ~60 Minuten

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

def find_best_video():
    """Findet ein Video mit ~60 Minuten Länge"""
    best_video = None
    best_diff = float('inf')
    
    if not os.path.exists(CORAL_REEF_DIR):
        print(f"ERROR: Verzeichnis nicht gefunden: {CORAL_REEF_DIR}")
        return None
    
    files_checked = 0
    for csv_file in os.listdir(CORAL_REEF_DIR):
        if not csv_file.endswith('.csv'):
            continue
        
        file_path = os.path.join(CORAL_REEF_DIR, csv_file)
        files_checked += 1
        
        try:
            # Finde die maximale Zeit in der gesamten Datei
            max_time = 0
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    frame_str = row.get('frames', '')
                    frame_time = extract_frame_time(frame_str)
                    if frame_time and frame_time > max_time:
                        max_time = frame_time
            
            if max_time > 0:
                diff = abs(max_time - TARGET_DURATION)
                if diff < best_diff:
                    best_diff = diff
                    best_video = {
                        'name': csv_file,
                        'path': file_path,
                        'duration': max_time
                    }
        except Exception as e:
            print(f"Fehler bei {csv_file}: {e}")
            continue
    
    print(f"DEBUG: {files_checked} Dateien überprüft")
    if best_video:
        print(f"DEBUG: Bestes Video hat {best_diff:.2f}s Abweichung von 60 Min")
    
    return best_video

def analyze_video(csv_path):
    """
    Analysiert Video für First Seen und MaxN.
    
    First Seen: Erster Zeitpunkt, an dem eine Art erscheint
    MaxN: Zeitpunkt mit der maximalen Anzahl derselben Art (gleichzeitig)
    """
    
    # Datenstrukturen
    first_seen = {}  # Art -> erste Zeit
    annotations_by_species_time = defaultdict(list)  # (Art, Frame-Zeit) -> Liste von Annotations
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                frame_str = row.get('frames', '')
                frame_time = extract_frame_time(frame_str)
                
                if frame_time is None:
                    continue
                
                label_name = row.get('label_name', '')
                family = row.get('family', '')
                
                if not label_name:
                    continue
                
                # Key für diese Art
                species_key = f"{family}|{label_name}"
                
                # First Seen
                if species_key not in first_seen:
                    first_seen[species_key] = frame_time
                
                # Sammle alle Annotations nach Art und exaktem Frame
                # Runde auf 2 Dezimalstellen um sehr nahe Zeitpunkte zusammenzufassen
                frame_rounded = round(frame_time, 2)
                annotations_by_species_time[(species_key, frame_rounded)].append(row)
        
    except Exception as e:
        print(f"Fehler beim Lesen: {e}")
        return None, None
    
    # Berechne MaxN für jede Art
    maxn_data = {}  # Art -> {'count': MaxN, 'time': Zeitpunkt}
    
    for (species_key, frame_time), annotations in annotations_by_species_time.items():
        count = len(annotations)
        
        if species_key not in maxn_data or count > maxn_data[species_key]['count']:
            maxn_data[species_key] = {
                'count': count,
                'time': frame_time
            }
    
    return first_seen, maxn_data

def create_first_seen_plot(first_seen, video_info, output_path):
    """
    Erstellt First Seen Timeline-Plot
    """
    fig, ax = plt.subplots(figsize=(16, 12))
    
    video_name = video_info['name'].replace('.csv', '')
    duration_min = seconds_to_minutes(video_info['duration'])
    
    # Sortiere nach Zeit
    sorted_species = sorted(first_seen.items(), key=lambda x: x[1])
    
    x_times = []
    y_labels = []
    colors = []
    
    # Farbpalette
    color_map = {}
    colors_palette = plt.cm.tab20(np.linspace(0, 1, 20))
    
    for idx, (species_key, time) in enumerate(sorted_species):
        x_times.append(time)
        
        # Label extrahieren
        parts = species_key.split('|')
        label = parts[1] if len(parts) > 1 else species_key
        label = label[:50] + "..." if len(label) > 50 else label
        y_labels.append(label)
        
        # Farbe nach Familie
        family = parts[0] if len(parts) > 0 else 'Unknown'
        if family not in color_map:
            color_map[family] = colors_palette[len(color_map) % len(colors_palette)]
        colors.append(color_map[family])
    
    # Plot
    y_positions = np.arange(len(x_times))
    ax.scatter(x_times, y_positions, s=200, c=colors, alpha=0.8, 
               edgecolors='black', linewidth=1.5, zorder=3)
    
    # Formatierung
    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels, fontsize=9)
    ax.set_xlabel('Video-Zeit (Minuten:Sekunden)', fontsize=14, fontweight='bold')
    ax.set_title(f'FIRST SEEN Timeline: {video_name}\n'
                 f'({duration_min} Videolänge, {len(first_seen)} verschiedene Arten/Taxa)',
                 fontsize=16, fontweight='bold', pad=20)
    
    # X-Achse formatieren
    def format_minutes(x, pos):
        return seconds_to_minutes(x) if x >= 0 else ''
    
    ax.xaxis.set_major_formatter(FuncFormatter(format_minutes))
    ax.xaxis.set_major_locator(plt.MultipleLocator(300))  # Alle 5 Minuten
    ax.xaxis.set_minor_locator(plt.MultipleLocator(60))   # Jede Minute
    
    ax.grid(True, alpha=0.3, axis='x', which='major')
    ax.grid(True, alpha=0.15, axis='x', which='minor', linestyle=':')
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Erstellt: {output_path}")
    plt.close()

def create_maxn_plot(maxn_data, video_info, output_path):
    """
    Erstellt MaxN Timeline-Plot
    """
    fig, ax = plt.subplots(figsize=(16, 12))
    
    video_name = video_info['name'].replace('.csv', '')
    duration_min = seconds_to_minutes(video_info['duration'])
    
    # Sortiere nach MaxN-Zeitpunkt
    sorted_species = sorted(maxn_data.items(), key=lambda x: x[1]['time'])
    
    x_times = []
    y_labels = []
    sizes = []
    colors = []
    
    # Farbpalette
    color_map = {}
    colors_palette = plt.cm.tab20(np.linspace(0, 1, 20))
    
    max_count = max([data['count'] for data in maxn_data.values()])
    
    for idx, (species_key, data) in enumerate(sorted_species):
        x_times.append(data['time'])
        
        # Label mit MaxN-Count
        parts = species_key.split('|')
        label = parts[1] if len(parts) > 1 else species_key
        label = label[:40] + "..." if len(label) > 40 else label
        y_labels.append(f"{label} (n={data['count']})")
        
        # Größe proportional zu MaxN
        size = 100 + (data['count'] / max_count) * 400
        sizes.append(size)
        
        # Farbe nach Familie
        family = parts[0] if len(parts) > 0 else 'Unknown'
        if family not in color_map:
            color_map[family] = colors_palette[len(color_map) % len(colors_palette)]
        colors.append(color_map[family])
    
    # Plot
    y_positions = np.arange(len(x_times))
    scatter = ax.scatter(x_times, y_positions, s=sizes, c=colors, alpha=0.7, 
                        edgecolors='black', linewidth=1.5, zorder=3)
    
    # Formatierung
    ax.set_yticks(y_positions)
    ax.set_yticklabels(y_labels, fontsize=9)
    ax.set_xlabel('Video-Zeit (Minuten:Sekunden)', fontsize=14, fontweight='bold')
    ax.set_title(f'MaxN Timeline: {video_name}\n'
                 f'({duration_min} Videolänge, Punktgröße = MaxN-Anzahl)',
                 fontsize=16, fontweight='bold', pad=20)
    
    # X-Achse formatieren
    def format_minutes(x, pos):
        return seconds_to_minutes(x) if x >= 0 else ''
    
    ax.xaxis.set_major_formatter(FuncFormatter(format_minutes))
    ax.xaxis.set_major_locator(plt.MultipleLocator(300))  # Alle 5 Minuten
    ax.xaxis.set_minor_locator(plt.MultipleLocator(60))   # Jede Minute
    
    ax.grid(True, alpha=0.3, axis='x', which='major')
    ax.grid(True, alpha=0.15, axis='x', which='minor', linestyle=':')
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Erstellt: {output_path}")
    plt.close()

def generate_summary(video_info, first_seen, maxn_data):
    """Generiert Zusammenfassungsbericht"""
    
    output_path = os.path.join(OUTPUT_DIR, 'first_seen_vs_maxn_summary.txt')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("FIRST SEEN vs. MaxN ANALYSE\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Video: {video_info['name']}\n")
        f.write(f"Dauer: {seconds_to_minutes(video_info['duration'])}\n")
        f.write(f"Verschiedene Arten/Taxa: {len(first_seen)}\n\n")
        
        f.write("KONZEPTE:\n\n")
        f.write("First Seen:\n")
        f.write("  • Zeitpunkt der ERSTEN Sichtung einer Art\n")
        f.write("  • Zeigt Kolonisations-Reihenfolge\n\n")
        
        f.write("MaxN (Maximum Number):\n")
        f.write("  • Maximale Anzahl einer Art zur SELBEN Zeit/Frame\n")
        f.write("  • Zeitpunkt, an dem diese maximale Anzahl erreicht wird\n")
        f.write("  • z.B.: Indian Half-and-Half erscheint bei Minute 1 (First Seen),\n")
        f.write("          aber MaxN von 72 Individuen wird erst bei Minute 40 erreicht\n\n")
        
        f.write("="*80 + "\n")
        f.write("ZEITLICHE VERTEILUNG\n")
        f.write("="*80 + "\n\n")
        
        # Analysiere zeitliche Muster
        first_seen_times = [t for t in first_seen.values()]
        maxn_times = [data['time'] for data in maxn_data.values()]
        
        f.write("First Seen:\n")
        f.write(f"  • Früheste: {seconds_to_minutes(min(first_seen_times))}\n")
        f.write(f"  • Späteste: {seconds_to_minutes(max(first_seen_times))}\n")
        f.write(f"  • Median: {seconds_to_minutes(np.median(first_seen_times))}\n\n")
        
        f.write("MaxN erreicht:\n")
        f.write(f"  • Früheste: {seconds_to_minutes(min(maxn_times))}\n")
        f.write(f"  • Späteste: {seconds_to_minutes(max(maxn_times))}\n")
        f.write(f"  • Median: {seconds_to_minutes(np.median(maxn_times))}\n\n")
        
        # Zeitdifferenz First Seen -> MaxN
        time_diffs = []
        for species_key in first_seen.keys():
            if species_key in maxn_data:
                diff = maxn_data[species_key]['time'] - first_seen[species_key]
                time_diffs.append(diff)
        
        f.write("Zeit von First Seen bis MaxN:\n")
        f.write(f"  • Durchschnitt: {seconds_to_minutes(np.mean(time_diffs))}\n")
        f.write(f"  • Median: {seconds_to_minutes(np.median(time_diffs))}\n")
        f.write(f"  • Minimum: {seconds_to_minutes(min(time_diffs))}\n")
        f.write(f"  • Maximum: {seconds_to_minutes(max(time_diffs))}\n\n")
        
        # Top MaxN Arten
        f.write("="*80 + "\n")
        f.write("TOP 10 MaxN ARTEN (höchste gleichzeitige Anzahl)\n")
        f.write("="*80 + "\n\n")
        
        sorted_by_maxn = sorted(maxn_data.items(), key=lambda x: x[1]['count'], reverse=True)[:10]
        for species_key, data in sorted_by_maxn:
            parts = species_key.split('|')
            label = parts[1] if len(parts) > 1 else species_key
            f_seen = first_seen.get(species_key, 0)
            time_to_maxn = data['time'] - f_seen
            
            f.write(f"{label}\n")
            f.write(f"  • MaxN: {data['count']} Individuen gleichzeitig\n")
            f.write(f"  • MaxN erreicht bei: {seconds_to_minutes(data['time'])}\n")
            f.write(f"  • First Seen bei: {seconds_to_minutes(f_seen)}\n")
            f.write(f"  • Zeit bis MaxN: {seconds_to_minutes(time_to_maxn)}\n\n")
        
        f.write("="*80 + "\n")
        f.write("INTERPRETATION\n")
        f.write("="*80 + "\n\n")
        
        f.write("Ab welcher Minute kommen wenig neue Arten dazu?\n")
        first_seen_sorted = sorted(first_seen.values())
        
        # Finde Minute, ab der < 5 neue Arten pro 10-Minuten-Fenster kommen
        for minute_threshold in range(10, 60, 5):
            new_after = sum(1 for t in first_seen_sorted if t > minute_threshold * 60)
            f.write(f"  • Nach Minute {minute_threshold}: noch {new_after} neue Arten\n")
        
        f.write("\nAb welcher Minute werden wenig neue MaxN erreicht?\n")
        maxn_sorted = sorted([data['time'] for data in maxn_data.values()])
        
        for minute_threshold in range(10, 60, 5):
            new_after = sum(1 for t in maxn_sorted if t > minute_threshold * 60)
            f.write(f"  • Nach Minute {minute_threshold}: noch {new_after} MaxN erreicht\n")
        
        f.write("\n")
    
    print(f"✓ Zusammenfassung: {output_path}")

def main():
    """Hauptfunktion"""
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("\n" + "="*80)
    print("FIRST SEEN vs. MaxN VISUALISIERUNG")
    print("="*80 + "\n")
    
    # Finde bestes Video (~60 Min)
    print("Suche Video mit ~60 Minuten Länge...")
    video_info = find_best_video()
    
    if not video_info:
        print("Kein geeignetes Video gefunden!")
        return
    
    print(f"✓ Gewählt: {video_info['name']}")
    print(f"  Länge: {seconds_to_minutes(video_info['duration'])}\n")
    
    # Analysiere Video
    print("Analysiere Video...")
    first_seen, maxn_data = analyze_video(video_info['path'])
    
    if not first_seen or not maxn_data:
        print("Fehler bei der Analyse!")
        return
    
    print(f"  • First Seen Daten: {len(first_seen)} Arten")
    print(f"  • MaxN Daten: {len(maxn_data)} Arten\n")
    
    # Erstelle Grafiken
    base_name = video_info['name'].replace('.csv', '')
    
    print("Erstelle Grafiken...")
    create_first_seen_plot(
        first_seen, 
        video_info,
        os.path.join(OUTPUT_DIR, f"{base_name}_first_seen.png")
    )
    
    create_maxn_plot(
        maxn_data,
        video_info,
        os.path.join(OUTPUT_DIR, f"{base_name}_maxn.png")
    )
    
    # Zusammenfassung
    generate_summary(video_info, first_seen, maxn_data)
    
    print("\n" + "="*80)
    print("✓ FERTIG!")
    print(f"Output: {OUTPUT_DIR}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
