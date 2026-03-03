#!/usr/bin/env python3
"""
Species Richness Analysis for Annotation Reports
Analysiert die Artenvielfalt in allen Annotation-Dateien
"""

import pandas as pd
import os
from pathlib import Path
from scipy.stats import mannwhitneyu

def calculate_species_richness(file_path, file_name):
    """Berechnet die Species Richness für eine Datei"""
    # Daten einlesen
    data = pd.read_csv(file_path)
    
    # Eindeutige Arten zählen
    unique_species = data['label_name'].nunique()
    
    # Gesamtanzahl der Beobachtungen
    total_observations = len(data)
    
    # Arten mit Häufigkeit
    species_counts = data.groupby(['label_name', 'label_hierarchy']).size().reset_index(name='count')
    species_counts = species_counts.sort_values('count', ascending=False)
    
    return {
        'file_name': file_name,
        'species_richness': unique_species,
        'total_observations': total_observations,
        'species_counts': species_counts
    }

def main():
    # Alle CSV-Dateien im Annotation_reports Ordner finden
    annotation_dir = Path("Annotation_reports")
    csv_files = list(annotation_dir.glob("*.csv"))
    
    # Species Richness für alle Dateien berechnen
    results_list = []
    for file in csv_files:
        file_name = file.name
        print(f"Analysiere: {file_name}")
        result = calculate_species_richness(file, file_name)
        results_list.append(result)
    
    # Zusammenfassung erstellen
    summary_data = []
    for res in results_list:
        summary_data.append({
            'file_name': res['file_name'],
            'species_richness': res['species_richness'],
            'total_observations': res['total_observations']
        })
    
    summary_df = pd.DataFrame(summary_data)
    
    # Standort und Köder aus Dateinamen extrahieren
    summary_df['location'] = summary_df['file_name'].apply(
        lambda x: 'Utumbi' if 'utumbi' in x.lower() else 'Milimani'
    )
    summary_df['date'] = summary_df['file_name'].str.extract(r'^(\d+)-')[0]
    summary_df['bait_info'] = summary_df['file_name'].str.extract(r'-c\d+-(.+)-ganz\.csv$')[0]
    summary_df['observations_per_species'] = (
        summary_df['total_observations'] / summary_df['species_richness']
    ).round(2)
    
    # Sortieren nach Species Richness
    summary_df = summary_df.sort_values('species_richness', ascending=False)
    
    # Ergebnisse ausgeben
    print("\n=== SPECIES RICHNESS VERGLEICH ===\n")
    print(summary_df.to_string(index=False))
    
    # Detaillierte Artenlisten für jede Datei
    print("\n\n=== DETAILLIERTE ARTENLISTEN ===\n")
    for res in results_list:
        print(f"\n--- {res['file_name']} ---")
        print(f"Species Richness: {res['species_richness']}")
        print(f"Gesamtbeobachtungen: {res['total_observations']}\n")
        print("Top 10 häufigste Arten:")
        print(res['species_counts'].head(10).to_string(index=False))
        print()
    
    # Ergebnisse in CSV speichern
    output_file = "results/species_richness_comparison.csv"
    os.makedirs("results", exist_ok=True)
    summary_df.to_csv(output_file, index=False)
    print(f"\nErgebnisse gespeichert in: {output_file}")
    
    # Zusätzliche detaillierte Artenliste mit allen Arten pro Datei
    detailed_species_list = []
    for res in results_list:
        species_df = res['species_counts'].copy()
        species_df['file_name'] = res['file_name']
        detailed_species_list.append(species_df)
    
    detailed_df = pd.concat(detailed_species_list, ignore_index=True)
    detailed_output_file = "results/species_richness_detailed.csv"
    detailed_df.to_csv(detailed_output_file, index=False)
    print(f"Detaillierte Artenliste gespeichert in: {detailed_output_file}")
    
    # ===== STATISTISCHE SIGNIFIKANZTESTS =====
    
    print("\n\n===== STATISTISCHE SIGNIFIKANZTESTS =====\n")
    
    significance_results = []
    
    # Vergleich zwischen Standorten (Milimani vs Utumbi)
    milimani_richness = summary_df[summary_df['location'] == 'Milimani']['species_richness'].values
    utumbi_richness = summary_df[summary_df['location'] == 'Utumbi']['species_richness'].values
    
    if len(milimani_richness) > 0 and len(utumbi_richness) > 0:
        u_stat, p_value = mannwhitneyu(milimani_richness, utumbi_richness)
        print(f"Milimani vs Utumbi (Species Richness):")
        print(f"  n_Milimani: {len(milimani_richness)}")
        print(f"  n_Utumbi: {len(utumbi_richness)}")
        print(f"  Test: Mann-Whitney U")
        print(f"  Statistic: {u_stat:.4f}")
        print(f"  p-value: {p_value:.6f}")
        print(f"  Significant (α=0.05): {'Yes' if p_value < 0.05 else 'No'}\n")
        
        significance_results.append({
            'comparison': 'Milimani vs Utumbi',
            'n_group1': len(milimani_richness),
            'n_group2': len(utumbi_richness),
            'test': 'Mann-Whitney U',
            'statistic': f"{u_stat:.4f}",
            'p_value': f"{p_value:.6f}",
            'significant_alpha_005': 'Yes' if p_value < 0.05 else 'No',
            'mean_group1': f"{milimani_richness.mean():.2f}",
            'mean_group2': f"{utumbi_richness.mean():.2f}"
        })
    
    # Speichere Signifikanz-Ergebnisse
    stats_df = pd.DataFrame(significance_results)
    stats_output_file = "results/species_richness_statistical_tests.csv"
    stats_df.to_csv(stats_output_file, index=False)
    print(f"Signifikanz-Tests gespeichert in: {stats_output_file}")

if __name__ == "__main__":
    main()
