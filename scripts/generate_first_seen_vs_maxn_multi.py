#!/usr/bin/env python3
"""
Erstellt First Seen vs. MaxN Visualisierungen für mehrere Videos im Vergleich.
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
NUM_VIDEOS = 5  # Anzahl Videos für Vergleich

def extract_frame_time(frame_str):
    """Extrahiert die Zeitwert aus frame string"""
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

def find_best_videos():
    """Findet mehrere Videos mit ~60 Minuten Länge"""
    videos = []
    
    if not os.path.exists(CORAL_REEF_DIR):
        print(f"ERROR: Verzeichnis nicht gefunden: {CORAL_REEF_DIR}")
        return []
    
    for csv_file in os.listdir(CORAL_REEF_DIR):
        if not csv_file.endswith('.csv'):
            continue
        
        file_path = os.path.join(CORAL_REEF_DIR, csv_file)
        
        try:
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
                videos.append({
                    'name': csv_file,
                    'path': file_path,
                    'duration': max_time,
                    'diff': diff
                })
        except Exception as e:
            continue
    
    videos.sort(key=lambda x: x['diff'])
    best_videos = videos[:NUM_VIDEOS]
    
    print(f"✓ {len(best_videos)} Videos ausgewählt\n")
    return best_videos

def analyze_video(csv_path):
    """Analysiert Video für First Seen und MaxN"""
    first_seen = {}
    annotations_by_species_time = defaultdict(list)
    
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
                
                species_key = f"{family}|{label_name}"
                
                if species_key not in first_seen:
                    first_seen[species_key] = frame_time
                
                frame_rounded = round(frame_time, 2)
                annotations_by_species_time[(species_key, frame_rounded)].append(row)
        
    except Exception as e:
        print(f"Fehler beim Lesen: {e}")
        return None, None
    
    maxn_data = {}
    
    for (species_key, frame_time), annotations in annotations_by_species_time.items():
        count = len(annotations)
        
        if species_key not in maxn_data or count > maxn_data[species_key]['count']:
            maxn_data[species_key] = {
                'count': count,
                'time': frame_time
            }
    
    return first_seen, maxn_data

def create_multi_first_seen_plot(videos_data, output_path):
    """Erstellt First Seen Plot für mehrere Videos"""
    
    fig, ax = plt.subplots(figsize=(18, 14))
    
    # Farbpalette für Videos
    video_colors = plt.cm.Set2(np.linspace(0, 1, len(videos_data)))
    markers = ['o', 's', '^', 'D', 'v', 'P', '*', 'X']
    
    max_duration = max([v['duration'] for v in videos_data])
    
    all_species_times = []
    
    # Sammle alle First Seen Zeiten für alle Videos
    for video_idx, video_data in enumerate(videos_data):
        first_seen = video_data['first_seen']
        video_name = video_data['name'].replace('.csv', '').replace('20241', '')[:20]
        
        for species_key, time in first_seen.items():
            parts = species_key.split('|')
            label = parts[1] if len(parts) > 1 else species_key
            all_species_times.append((time, video_idx, label, video_name))
    
    # Sortiere nach Zeit
    all_species_times.sort(key=lambda x: x[0])
    
    # Gruppiere nach Zeitfenstern (1-Minuten-Bins)
    time_bins = defaultdict(lambda: defaultdict(int))
    for time, video_idx, label, video_name in all_species_times:
        bin_idx = int(time // 60)  # 1-Minuten-Bins
        time_bins[bin_idx][video_idx] += 1
    
    # Plotte kumulative Kurven
    for video_idx, (video_data, color) in enumerate(zip(videos_data, video_colors)):
        first_seen = video_data['first_seen']
        video_name = video_data['name'].replace('.csv', '').replace('20241', '')[:25]
        
        times = sorted(first_seen.values())
        cumulative = list(range(1, len(times) + 1))
        
        # Füge Start- und Endpunkt hinzu
        times_plot = [0] + times + [max_duration]
        cumulative_plot = [0] + cumulative + [cumulative[-1]]
        
        ax.plot(times_plot, cumulative_plot, 
                color=color, linewidth=3, alpha=0.8,
                marker=markers[video_idx % len(markers)],
                markersize=8, markevery=max(1, len(times) // 15),
                label=f'{video_name} ({len(first_seen)} Arten)')
    
    # Formatierung
    ax.set_xlabel('Video-Zeit (Minuten)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Kumulative Anzahl neuer Arten (First Seen)', fontsize=14, fontweight='bold')
    ax.set_title(f'First Seen Vergleich: {len(videos_data)} Videos (~60 Min)\n'
                 f'Wann erscheinen neue Arten zum ersten Mal?',
                 fontsize=16, fontweight='bold', pad=20)
    
    def format_minutes(x, pos):
        return str(int(x // 60))
    
    ax.xaxis.set_major_formatter(FuncFormatter(format_minutes))
    ax.xaxis.set_major_locator(plt.MultipleLocator(600))  # Alle 10 Minuten
    
    ax.grid(True, alpha=0.3)
    ax.legend(loc='lower right', fontsize=10, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Erstellt: {output_path}")
    plt.close()

def create_multi_maxn_plot(videos_data, output_path):
    """Erstellt MaxN Plot für mehrere Videos"""
    
    fig, ax = plt.subplots(figsize=(18, 14))
    
    video_colors = plt.cm.Set2(np.linspace(0, 1, len(videos_data)))
    markers = ['o', 's', '^', 'D', 'v', 'P', '*', 'X']
    
    max_duration = max([v['duration'] for v in videos_data])
    
    # Plotte kumulative MaxN-Kurven
    for video_idx, (video_data, color) in enumerate(zip(videos_data, video_colors)):
        maxn_data = video_data['maxn_data']
        video_name = video_data['name'].replace('.csv', '').replace('20241', '')[:25]
        
        times = sorted([data['time'] for data in maxn_data.values()])
        cumulative = list(range(1, len(times) + 1))
        
        times_plot = [0] + times + [max_duration]
        cumulative_plot = [0] + cumulative + [cumulative[-1]]
        
        ax.plot(times_plot, cumulative_plot, 
                color=color, linewidth=3, alpha=0.8,
                marker=markers[video_idx % len(markers)],
                markersize=8, markevery=max(1, len(times) // 15),
                label=f'{video_name} ({len(maxn_data)} MaxN)')
    
    # Formatierung
    ax.set_xlabel('Video-Zeit (Minuten)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Kumulative Anzahl MaxN erreicht', fontsize=14, fontweight='bold')
    ax.set_title(f'MaxN Vergleich: {len(videos_data)} Videos (~60 Min)\n'
                 f'Wann werden maximale Artenzahlen erreicht?',
                 fontsize=16, fontweight='bold', pad=20)
    
    def format_minutes(x, pos):
        return str(int(x // 60))
    
    ax.xaxis.set_major_formatter(FuncFormatter(format_minutes))
    ax.xaxis.set_major_locator(plt.MultipleLocator(600))
    
    ax.grid(True, alpha=0.3)
    ax.legend(loc='lower right', fontsize=10, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"✓ Erstellt: {output_path}")
    plt.close()

def generate_summary(videos_data):
    """Generiert Zusammenfassungsbericht"""
    
    output_path = os.path.join(OUTPUT_DIR, 'multi_video_summary.txt')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("FIRST SEEN vs. MaxN - MULTI-VIDEO VERGLEICH\n")
        f.write("="*80 + "\n\n")
        
        f.write(f"Anzahl Videos: {len(videos_data)}\n")
        f.write(f"Ziel-Länge: ~60 Minuten\n\n")
        
        f.write("VIDEOS:\n\n")
        for idx, video_data in enumerate(videos_data, 1):
            f.write(f"{idx}. {video_data['name']}\n")
            f.write(f"   Länge: {seconds_to_minutes(video_data['duration'])}\n")
            f.write(f"   First Seen: {len(video_data['first_seen'])} Arten\n")
            f.write(f"   MaxN Ereignisse: {len(video_data['maxn_data'])}\n")
            
            # Median-Zeiten
            fs_times = sorted(video_data['first_seen'].values())
            maxn_times = sorted([d['time'] for d in video_data['maxn_data'].values()])
            
            if fs_times:
                fs_median = np.median(fs_times)
                f.write(f"   First Seen Median: {seconds_to_minutes(fs_median)}\n")
            
            if maxn_times:
                maxn_median = np.median(maxn_times)
                f.write(f"   MaxN Median: {seconds_to_minutes(maxn_median)}\n")
            
            f.write("\n")
        
        f.write("="*80 + "\n")
        f.write("INTERPRETATION\n")
        f.write("="*80 + "\n\n")
        
        f.write("Grafik 1 - First Seen:\n")
        f.write("  • Zeigt kumulative Kurven: Wie schnell werden neue Arten entdeckt?\n")
        f.write("  • Steile Kurven = Viele Arten erscheinen früh\n")
        f.write("  • Flache Kurven am Ende = Sättigung erreicht\n\n")
        
        f.write("Grafik 2 - MaxN:\n")
        f.write("  • Zeigt kumulative Kurven: Wann werden MaxN-Werte erreicht?\n")
        f.write("  • Höhere Kurven = Mehr verschiedene Schwarm-Maxima\n")
        f.write("  • MaxN dauert oft länger als First Seen\n\n")
        
        f.write("Vergleiche zwischen Videos:\n")
        f.write("  • Unterschiedliche Standorte oder Köder?\n")
        f.write("  • Ähnliche Kolonisations-Muster erkennbar?\n")
        f.write("  • Zeitliche Variabilität in der Artenentdeckung\n\n")
    
    print(f"✓ Zusammenfassung: {output_path}")

def main():
    """Hauptfunktion"""
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("\n" + "="*80)
    print("FIRST SEEN vs. MaxN - MULTI-VIDEO VISUALISIERUNG")
    print("="*80 + "\n")
    
    # Finde beste Videos
    print("Suche Videos mit ~60 Minuten Länge...")
    videos_list = find_best_videos()
    
    if len(videos_list) < 2:
        print("Nicht genug Videos gefunden!")
        return
    
    # Analysiere alle Videos
    videos_data = []
    for video in videos_list:
        print(f"Analysiere: {video['name']} ({seconds_to_minutes(video['duration'])})")
        first_seen, maxn_data = analyze_video(video['path'])
        
        if first_seen and maxn_data:
            videos_data.append({
                'name': video['name'],
                'path': video['path'],
                'duration': video['duration'],
                'first_seen': first_seen,
                'maxn_data': maxn_data
            })
            print(f"  ✓ {len(first_seen)} Arten, {len(maxn_data)} MaxN\n")
    
    if not videos_data:
        print("Keine gültigen Video-Daten!")
        return
    
    # Erstelle Grafiken
    print("Erstelle Grafiken...\n")
    
    create_multi_first_seen_plot(
        videos_data,
        os.path.join(OUTPUT_DIR, "multi_video_first_seen.png")
    )
    
    create_multi_maxn_plot(
        videos_data,
        os.path.join(OUTPUT_DIR, "multi_video_maxn.png")
    )
    
    # Zusammenfassung
    generate_summary(videos_data)
    
    print("\n" + "="*80)
    print("✓ FERTIG!")
    print(f"Output: {OUTPUT_DIR}")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
