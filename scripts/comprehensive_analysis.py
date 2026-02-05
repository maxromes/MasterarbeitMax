#!/usr/bin/env python3
"""
Umfassende Analyse: Species Richness + MaxN + Vergleichskennzahlen
Kombiniert alle Annotation Reports (Coral Reef + Nursery)
Erstellt große Vergleichstabelle mit Species Richness, MaxN und statistischen Kennzahlen
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import entropy
from collections import Counter

# ===== 1. FUNKTIONEN DEFINIEREN =====

def calculate_shannon_index(species_list):
    """Berechnet Shannon Diversity Index"""
    if len(species_list) == 0:
        return 0
    counts = Counter(species_list)
    total = sum(counts.values())
    proportions = [count / total for count in counts.values()]
    return entropy(proportions)

def calculate_simpson_index(species_list):
    """Berechnet Simpson Diversity Index"""
    if len(species_list) == 0:
        return 0
    counts = Counter(species_list)
    total = sum(counts.values())
    proportions = [count / total for count in counts.values()]
    return 1 - sum(p**2 for p in proportions)

def calculate_pielou_evenness(species_list):
    """Berechnet Pielou's Evenness Index (J)"""
    unique_species = len(set(species_list))
    if unique_species <= 1:
        return 0
    shannon = calculate_shannon_index(species_list)
    return shannon / np.log(unique_species)

def calculate_comprehensive_stats(file_path, file_name, area_type):
    """Berechnet comprehensive Statistics für eine Datei"""
    try:
        # Daten einlesen
        data = pd.read_csv(file_path)
        
        if len(data) == 0:
            print(f"Warnung: Datei leer - {file_name}")
            return None
        
        # Basic Statistics
        unique_species = data['label_name'].nunique()
        total_observations = len(data)
        
        # MaxN Berechnung: Höchste Anzahl einer Art in einem Frame
        maxn_by_species = data.groupby(['label_name', 'frames']).size().reset_index(name='count')
        overall_maxn = maxn_by_species['count'].max()
        
        # Beobachtungen pro Art
        observations_per_species = data.groupby('label_name').size()
        obs_per_species_mean = observations_per_species.mean()
        obs_per_species_sd = observations_per_species.std()
        
        # Diversity Indices
        species_list = data['label_name'].tolist()
        shannon_h = calculate_shannon_index(species_list)
        simpson_d = calculate_simpson_index(species_list)
        pielou_j = calculate_pielou_evenness(species_list)
        
        # Anzahl der Frames im Video
        unique_frames = data['frames'].nunique()
        
        # Top 3 häufigste Arten
        top_species = observations_per_species.nlargest(3).index.tolist()
        top_species_str = ", ".join(top_species[:3])
        
        # Informationen aus Dateinamen extrahieren
        location = "Utumbi" if "utumbi" in file_name.lower() else "Milimani"
        date_str = file_name.split('-')[0]
        
        # Datum formatieren (DDMMJJJJ -> DD.MM.JJJJ)
        if len(date_str) == 8 and date_str.isdigit():
            date_formatted = f"{date_str[0:2]}.{date_str[2:4]}.{date_str[4:8]}"
        else:
            date_formatted = date_str
        
        # Köder/Bait Information
        import re
        match = re.search(r'-c\d+-(.+?)-ganz\.csv$', file_name.lower())
        if match:
            bait_info = match.group(1)
        else:
            match = re.search(r'-(.+?)-ganz\.csv$', file_name.lower())
            bait_info = match.group(1) if match else "unknown"
        
        # Ergebnis als Dictionary
        result = {
            'file_name': file_name,
            'area_type': area_type,
            'location': location,
            'date': date_formatted,
            'bait_type': bait_info,
            'species_richness': unique_species,
            'total_observations': total_observations,
            'maxn_overall': overall_maxn,
            'obs_per_species_mean': round(obs_per_species_mean, 2),
            'obs_per_species_sd': round(obs_per_species_sd, 2),
            'shannon_h': round(shannon_h, 3),
            'simpson_d': round(simpson_d, 3),
            'pielou_j': round(pielou_j, 3),
            'unique_frames': unique_frames,
            'obs_per_frame': round(total_observations / unique_frames, 2),
            'top_3_species': top_species_str
        }
        
        return result
        
    except Exception as e:
        print(f"Fehler bei Datei: {file_name} - {str(e)}")
        return None

# ===== 2. ALLE DATEIEN SAMMELN UND ANALYSIEREN =====

print("\n===== ANALYSIERE ALLE ANNOTATION REPORTS =====\n")

coral_reef_dir = Path("Annotation_reports_coral_reef")
nursery_dir = Path("Annotation_reports_Nursery")

# Finde alle CSV-Dateien
coral_reef_files = list(coral_reef_dir.glob("*.csv"))
nursery_files = list(nursery_dir.glob("*.csv"))

print(f"Coral Reef Dateien gefunden: {len(coral_reef_files)}")
print(f"Nursery Dateien gefunden: {len(nursery_files)}\n")

all_results = []

# Analysiere Coral Reef
print("Analysiere Coral Reef Dateien...")
for file in sorted(coral_reef_files):
    file_name = file.name
    print(f"  - {file_name}")
    result = calculate_comprehensive_stats(str(file), file_name, "Coral Reef")
    if result:
        all_results.append(result)

# Analysiere Nursery
print("\nAnalysiere Nursery Dateien...")
for file in sorted(nursery_files):
    file_name = file.name
    print(f"  - {file_name}")
    result = calculate_comprehensive_stats(str(file), file_name, "Nursery")
    if result:
        all_results.append(result)

# ===== 3. ERSTELLE HAUPTTABELLE =====

comprehensive_df = pd.DataFrame(all_results)

# Sortiere nach Species Richness (absteigend)
comprehensive_df = comprehensive_df.sort_values('species_richness', ascending=False).reset_index(drop=True)

# ===== 4. ERGEBNISSE ANZEIGEN =====

print("\n\n===== UMFASSENDE VERGLEICHSTABELLE =====\n")
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
print(comprehensive_df.to_string())

# ===== 5. STATISTIKEN NACH BEREICH =====

print("\n\n===== STATISTIKEN NACH BEREICH =====\n")

stats_by_area = comprehensive_df.groupby('area_type').agg({
    'file_name': 'count',
    'species_richness': ['mean', 'std', 'min', 'max'],
    'maxn_overall': ['mean', 'std'],
    'total_observations': 'sum',
    'shannon_h': 'mean',
    'pielou_j': 'mean'
}).round(2)

stats_by_area.columns = ['anzahl_dateien', 'richness_mean', 'richness_sd', 'richness_min', 
                         'richness_max', 'maxn_mean', 'maxn_sd', 'observations_total', 
                         'shannon_mean', 'evennes_mean']
print(stats_by_area)

# ===== 6. STATISTIKEN NACH STANDORT =====

print("\n\n===== STATISTIKEN NACH STANDORT =====\n")

stats_by_location = comprehensive_df.groupby(['location', 'area_type']).agg({
    'file_name': 'count',
    'species_richness': ['mean', 'std'],
    'maxn_overall': 'mean',
    'total_observations': 'sum',
    'shannon_h': 'mean'
}).round(2)

stats_by_location.columns = ['anzahl_dateien', 'richness_mean', 'richness_sd', 
                              'maxn_mean', 'observations_total', 'shannon_mean']
print(stats_by_location)

# ===== 7. TOP KÖDERTYPEN =====

print("\n\n===== TOP KÖDERTYPEN (Bait Types) =====\n")

bait_stats = comprehensive_df.groupby('bait_type').agg({
    'file_name': 'count',
    'species_richness': ['mean', 'std'],
    'maxn_overall': 'mean',
    'total_observations': 'mean',
    'shannon_h': 'mean'
}).round(2)

bait_stats.columns = ['anzahl_videos', 'richness_mean', 'richness_sd', 
                      'maxn_mean', 'obs_mean', 'shannon_mean']
bait_stats = bait_stats.sort_values('richness_mean', ascending=False)
print(bait_stats)

# ===== 8. SPEICHERE ERGEBNISSE =====

output_dir = Path("results")
output_dir.mkdir(exist_ok=True)

# Haupttabelle
comprehensive_df.to_csv(output_dir / "comprehensive_analysis_table.csv", index=False)
print("\n\nHaupttabelle gespeichert: results/comprehensive_analysis_table.csv")

# Bereichs-Statistiken
stats_by_area.to_csv(output_dir / "statistics_by_area.csv")
print("Bereichs-Statistiken gespeichert: results/statistics_by_area.csv")

# Standort-Statistiken
stats_by_location.to_csv(output_dir / "statistics_by_location.csv")
print("Standort-Statistiken gespeichert: results/statistics_by_location.csv")

# Köder-Statistiken
bait_stats.to_csv(output_dir / "statistics_by_bait.csv")
print("Köder-Statistiken gespeichert: results/statistics_by_bait.csv")

print("\n===== ANALYSE ABGESCHLOSSEN =====\n")
