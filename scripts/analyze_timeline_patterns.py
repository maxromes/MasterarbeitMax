#!/usr/bin/env python3
"""
Analyse der Timeline-Visualisierungen - Statistiken und Muster
"""

import os
import csv
from collections import defaultdict

def extract_frame_time(frame_str):
    try:
        return float(frame_str.strip('[]'))
    except:
        return None

def analyze_species_patterns():
    """Analysiert Patterns in der Artenverteilung"""
    
    coral_reef_dir = "Annotation_reports_coral_reef"
    
    # Metriken
    first_appearance_times = defaultdict(list)
    species_counts = defaultdict(int)
    
    print("\n" + "="*70)
    print("DETAILLIERTE TIMELINE-ANALYSE")
    print("="*70 + "\n")
    
    # Analysiere alle Videos
    for csv_file in sorted(os.listdir(coral_reef_dir)):
        if not csv_file.endswith('.csv'):
            continue
        
        file_path = os.path.join(coral_reef_dir, csv_file)
        first_seen_species = {}
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    frame_time = extract_frame_time(row.get('frames', ''))
                    if frame_time is None:
                        continue
                    
                    label = row.get('label_name', '')
                    family = row.get('family', '')
                    
                    key = f"{family}|{label}"
                    if key not in first_seen_species:
                        first_seen_species[key] = frame_time
        except Exception as e:
            print(f"Fehler in {csv_file}: {e}")
            continue
        
        # Erfasse Metriken
        for (family_label, first_time) in first_seen_species.items():
            minutes = int(first_time // 60)
            species_counts[minutes] += 1
            first_appearance_times[minutes].append((family_label, first_time))
    
    # Bericht
    print("ERSTE ARTENERSCHEINUNGEN PRO VIDEO-MINUTE:\n")
    for minute in sorted(species_counts.keys()):
        print(f"Minute {minute:2d}: {species_counts[minute]:3d} erste Sichtungen")
    
    print("\n" + "="*70)
    print("HÄUFIGSTE ERSCHEINUNGSMUSTER")
    print("="*70)
    
    # Finde Trends
    early_species = {}  # Arten, die in der ersten Hälfte erscheinen
    late_species = {}   # Arten, die in der zweiten Hälfte erscheinen
    
    for minute in first_appearance_times:
        for family_label, first_time in first_appearance_times[minute]:
            species = family_label.split('|')[1] if '|' in family_label else family_label
            
            if minute < 30:  # Erste 30 Minuten
                early_species[species] = early_species.get(species, 0) + 1
            else:  # Nach 30 Minuten
                late_species[species] = late_species.get(species, 0) + 1
    
    print("\nARTEN, DIE HÄ UIG FRÜH ERSCHEINEN (in < 30min):")
    sorted_early = sorted(early_species.items(), key=lambda x: x[1], reverse=True)[:10]
    for species, count in sorted_early:
        print(f"  • {species}: {count} Videos")
    
    print("\nARTEN, DIE HÄ UIG SPÄT ERSCHEINEN (in > 30min):")
    sorted_late = sorted(late_species.items(), key=lambda x: x[1], reverse=True)[:10]
    for species, count in sorted_late:
        print(f"  • {species}: {count} Videos")
    
    return first_appearance_times

def generate_analysis_report(output_file="results/timeline_analysis.txt"):
    """Generiert einen detaillierten Analysebericht"""
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("TIMELINE VISUALISIERUNGEN - DETAILLIERTE ANALYSE\n")
        f.write("="*70 + "\n\n")
        
        f.write("INTERPRETATION DER VISUALISIERUNGEN:\n\n")
        
        f.write("1. FIRST SEEN TIMELINE\n")
        f.write("   • Zeigt: Zeitpunkt der ERSTEN Sichtung jeder Fischart\n")
        f.write("   • Anwendung: Identifiziert Colonisations-Verlauf und Ankauf-Hierarchie\n")
        f.write("   • Muster zu suchen:\n")
        f.write("     - Clustered starts: Viele Arten erscheinen gleichzeitig\n")
        f.write("     - Sequential pattern: Arten erscheinen nacheinander\n")
        f.write("     - Late bloomers: Arten, die erst nach 40+ Minuten kommen\n\n")
        
        f.write("2. KUMULATIVE SPECIES PLOT\n")
        f.write("   • Zeigt: Gesamtzahl unterschiedlicher Arten über Zeit\n")
        f.write("   • Anwendung: Messung der Biodiversitäts-Akkumulation\n")
        f.write("   • Wichtige Metriken:\n")
        f.write("     - Initiale Steigung: Wie schnell werden Arten identifiziert?\n")
        f.write("     - Inflection point: Wann verlangsamt sich die Entdeckung?\n")
        f.write("     - Sättigung: Wie viele Arten insgesamt?\n\n")
        
        f.write("3. ANNOTATIONS-DICHTE\n")
        f.write("   • Zeigt: Annotations-Häufigkeit pro Videonominute\n")
        f.write("   • Anwendung: Identifiziert zeitliche Hotspots\n")
        f.write("   • Interpretation:\n")
        f.write("     - Hohe Dichte: Viel Fischaktivität oder Bodeninteraktion\n")
        f.write("     - Niedrige Dichte: Leere Phasen oder schnelle Übergänge\n\n")
        
        f.write("FORSCHUNGSFRAGEN, DIE BEANTWORTET WERDEN KÖNNEN:\n\n")
        f.write("1. Köder-Spezifität:\n")
        f.write("   Erscheinen bestimmte Arten früher auf Fischmix als auf Sargassum?\n\n")
        
        f.write("2. Standort-Unterschiede (Milimani vs. Utumbi):\n")
        f.write("   Unterscheiden sich die Kolonialisierungsmuster zwischen Standorten?\n\n")
        
        f.write("3. Ökologische Hierarchie:\n")
        f.write("   Welche Arten sind dominant (erscheinen früh)?\n")
        f.write("   Welche sind subdominant (erscheinen später)?\n\n")
        
        f.write("4. Temporale Belastung (Temporal Robustness):\n")
        f.write("   Wie konsistent sind die Muster über verschiedene Videos?\n\n")
        
        f.write("STATISTISCHE ANALYSEN (EMPFOHLEN):\n\n")
        f.write("1. Korrelation zwischen Ködern und Species First Appearance Times\n")
        f.write("2. Mann-Whitney U Test für Standortunterschiede\n")
        f.write("3. Clusteranalyse der First Appearance Patterns\n")
        f.write("4. Regression: Wie schnell wächst die kumulative Artenzahl?\n\n")
        
        f.write("="*70 + "\n")
    
    print(f"✓ Analysebericht erstellt: {output_file}")

if __name__ == "__main__":
    analyze_species_patterns()
    generate_analysis_report()
    print("\n✓ Alle Analysen abgeschlossen!")
