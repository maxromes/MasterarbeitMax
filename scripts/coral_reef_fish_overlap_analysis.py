#!/usr/bin/env python3
"""
Coral Reef Fish Overlap & Bait Specificity Analysis
Analysiert Fischarten-Überschneidungen und Köder-Spezifität
für Milimani und Utumbi getrennt mit zusammengefassten Ködern pro Site
"""

from pathlib import Path
from collections import defaultdict
import re

import pandas as pd
import numpy as np


def parse_filename(filename: str) -> dict:
    """Parse metadata from filename like 20241025-milimani-mackerel-c10.csv"""
    stem = filename.replace(".csv", "")
    parts = stem.split("-")
    
    date = parts[0] if parts else "unknown"
    site = parts[1].lower() if len(parts) > 1 else "unknown"
    bait = "unknown"
    
    if len(parts) > 2:
        bait = parts[2]
        if len(parts) > 3 and re.match(r"^c\d+$", parts[3]):
            pass
        else:
            bait = "-".join(parts[2:])
    
    # Normalize site names
    site = "milimani" if "milimani" in site else "utumbi" if "utumbi" in site else site
    
    return {
        "date": date,
        "site": site,
        "bait": bait.lower(),
        "filename": filename
    }


def extract_species(df: pd.DataFrame) -> set:
    """Extract all species names from a dataframe"""
    species_set = set()
    
    # Try multiple taxonomic levels
    for col in ["species", "genus", "family"]:
        if col in df.columns:
            species_set.update(df[col].dropna().unique())
    
    # Clean up
    species_set.discard("nan")
    species_set = {str(s).strip() for s in species_set if str(s).strip() and str(s) != ""}
    
    return species_set


def main():
    report_dir = Path("Annotation_reports_coral_reef")
    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)
    
    # Dictionary to store fish species by Site + Bait
    site_bait_fishes = {}
    
    # Dictionary to track which files contribute to each site-bait combo
    site_bait_files = defaultdict(list)
    
    # Collect all data
    print("="*70)
    print("CORAL REEF FISH OVERLAP & BAIT SPECIFICITY ANALYSIS")
    print("="*70)
    print("\nProcessing files...\n")
    
    all_files = sorted(report_dir.glob("*.csv"))
    
    for file_path in all_files:
        meta = parse_filename(file_path.name)
        site = meta["site"]
        bait = meta["bait"]
        
        try:
            data = pd.read_csv(file_path)
            unique_species = extract_species(data)
            
            # Store under site-bait combination
            key = (site, bait)
            if key not in site_bait_fishes:
                site_bait_fishes[key] = set()
            site_bait_fishes[key].update(unique_species)
            
            site_bait_files[key].append({
                "filename": file_path.name,
                "species_count": len(unique_species),
                "observation_count": len(data)
            })
            
            print(f"  ✓ {file_path.name}")
            print(f"    → {site.upper()} | {bait.upper()} | {len(unique_species)} species")
            
        except Exception as e:
            print(f"  ✗ {file_path.name}: {e}")
    
    # ===== CREATE MASTER TABLE: Site + Bait Overview =====
    
    print("\n" + "="*70)
    print("OVERVIEW: Site + Bait Combinations")
    print("="*70 + "\n")
    
    overview_data = []
    site_bait_keys = sorted(site_bait_fishes.keys())
    
    for site, bait in site_bait_keys:
        fishes = site_bait_fishes[(site, bait)]
        files = site_bait_files[(site, bait)]
        
        overview_data.append({
            "site": site.upper(),
            "bait": bait.upper(),
            "files_count": len(files),
            "total_species": len(fishes),
            "sample_observations": sum(f["observation_count"] for f in files),
            "file_details": "; ".join([f"{f['filename']}" for f in files])
        })
    
    overview_df = pd.DataFrame(overview_data)
    overview_df.to_csv(out_dir / "coral_reef_site_bait_overview.csv", index=False)
    print(overview_df[["site", "bait", "files_count", "total_species", "sample_observations"]].to_string(index=False))
    print("\n✓ Saved: coral_reef_site_bait_overview.csv\n")
    
    # ===== SEPARATE ANALYSIS FOR EACH SITE =====
    
    sites = ["milimani", "utumbi"]
    
    for site in sites:
        print("="*70)
        print(f"DETAILED ANALYSIS: {site.upper()}")
        print("="*70 + "\n")
        
        # Get all baits for this site
        site_baits = {bait: fishes for (s, bait), fishes in site_bait_fishes.items() if s == site}
        bait_list = sorted(site_baits.keys())
        
        if not bait_list:
            print(f"  No data for {site}")
            continue
        
        print(f"Baits found: {', '.join([b.upper() for b in bait_list])}\n")
        
        # Create fish species table for this site
        species_table_data = []
        all_species_on_site = set()
        
        for bait in bait_list:
            all_species_on_site.update(site_baits[bait])
        
        for sp in sorted(all_species_on_site):
            row = {
                "species": sp,
                "baits": ""
            }
            
            bait_presence = []
            for bait in bait_list:
                if sp in site_baits[bait]:
                    bait_presence.append(bait.upper())
            
            row["baits"] = ", ".join(bait_presence) if bait_presence else "—"
            species_table_data.append(row)
        
        species_df = pd.DataFrame(species_table_data)
        species_df = species_df.sort_values("species")
        
        filename = f"coral_reef_{site}_fish_by_bait.csv"
        species_df.to_csv(out_dir / filename, index=False)
        print(f"Fish species for {site.upper()} ({len(species_df)} total):")
        if len(species_df) <= 30:
            print(species_df.to_string(index=False))
        else:
            print(species_df.head(15).to_string(index=False))
            print(f"  ... and {len(species_df) - 15} more species ...")
        print(f"\n✓ Saved: {filename}\n")
        
        # Overlap analysis: which fish appear in multiple baits at this site?
        print(f"\nOverlap Analysis for {site.upper()}:")
        print("-" * 50)
        
        overlap_data = []
        for sp in sorted(all_species_on_site):
            baits_with_species = [bait for bait in bait_list if sp in site_baits[bait]]
            overlap_count = len(baits_with_species)
            
            specificity_label = "ubiquitous" if overlap_count >= 3 else (
                "multi-bait" if overlap_count == 2 else "bait-specific"
            )
            
            overlap_data.append({
                "species": sp,
                "baits_count": overlap_count,
                "baits": ", ".join([b.upper() for b in baits_with_species]),
                "specificity": specificity_label
            })
        
        overlap_df = pd.DataFrame(overlap_data)
        overlap_df = overlap_df.sort_values("baits_count", ascending=False)
        
        filename = f"coral_reef_{site}_fish_overlap.csv"
        overlap_df.to_csv(out_dir / filename, index=False)
        print(overlap_df.to_string(index=False))
        print(f"\n✓ Saved: {filename}\n")
        
        # Summary statistics for this site
        ubiquitous = sum(1 for row in overlap_data if row["specificity"] == "ubiquitous")
        multi_bait = sum(1 for row in overlap_data if row["specificity"] == "multi-bait")
        specific = sum(1 for row in overlap_data if row["specificity"] == "bait-specific")
        
        print(f"\nSummary for {site.upper()}:")
        print(f"  Total species: {len(all_species_on_site)}")
        print(f"  Ubiquitous (3+ baits): {ubiquitous}")
        print(f"  Multi-bait (2 baits): {multi_bait}")
        print(f"  Bait-specific (1 bait): {specific}\n")
    
    # ===== CROSS-SITE COMPARISON =====
    
    print("="*70)
    print("CROSS-SITE COMPARISON (Same Bait Type)")
    print("="*70 + "\n")
    
    # Find common baits across sites
    milimani_baits = {bait for (s, bait) in site_bait_fishes.keys() if s == "milimani"}
    utumbi_baits = {bait for (s, bait) in site_bait_fishes.keys() if s == "utumbi"}
    common_baits = milimani_baits & utumbi_baits
    
    if common_baits:
        print(f"Common baits across sites: {', '.join(sorted([b.upper() for b in common_baits]))}\n")
        
        cross_site_data = []
        for bait in sorted(common_baits):
            milimani_fish = site_bait_fishes[("milimani", bait)]
            utumbi_fish = site_bait_fishes[("utumbi", bait)]
            
            overlap_fish = milimani_fish & utumbi_fish
            only_milimani = milimani_fish - utumbi_fish
            only_utumbi = utumbi_fish - milimani_fish
            
            cross_site_data.append({
                "bait": bait.upper(),
                "milimani_species": len(milimani_fish),
                "utumbi_species": len(utumbi_fish),
                "overlap_species": len(overlap_fish),
                "overlap_percentage": round(100 * len(overlap_fish) / max(len(milimani_fish), len(utumbi_fish)), 1),
                "milimani_only": len(only_milimani),
                "utumbi_only": len(only_utumbi)
            })
            
            print(f"Bait: {bait.upper()}")
            print(f"  Milimani: {len(milimani_fish)} species | Utumbi: {len(utumbi_fish)} species")
            print(f"  Overlap: {len(overlap_fish)} species ({round(100*len(overlap_fish)/max(len(milimani_fish), len(utumbi_fish)), 1)}%)")
            print(f"  Milimani-only: {len(only_milimani)} | Utumbi-only: {len(only_utumbi)}\n")
        
        cross_site_df = pd.DataFrame(cross_site_data)
        cross_site_df.to_csv(out_dir / "coral_reef_cross_site_comparison.csv", index=False)
        print("\nCross-site Comparison Table:")
        print(cross_site_df.to_string(index=False))
        print(f"\n✓ Saved: coral_reef_cross_site_comparison.csv\n")
    else:
        print("No common baits across sites.\n")
    
    # ===== BAIT SPECIFICITY ANALYSIS =====
    
    print("="*70)
    print("BAIT SPECIFICITY ANALYSIS (All Sites Combined)")
    print("="*70 + "\n")
    
    bait_specificity_data = []
    all_baits = {bait for (s, bait) in site_bait_fishes.keys()}
    
    for bait in sorted(all_baits):
        # Get all fish for this bait across all sites
        bait_fish_all_sites = set()
        bait_sites = set()
        
        for (s, b), fishes in site_bait_fishes.items():
            if b == bait:
                bait_fish_all_sites.update(fishes)
                bait_sites.add(s.upper())
        
        bait_specificity_data.append({
            "bait": bait.upper(),
            "total_species": len(bait_fish_all_sites),
            "sites": ", ".join(sorted(bait_sites)),
            "site_count": len(bait_sites)
        })
    
    bait_spec_df = pd.DataFrame(bait_specificity_data)
    bait_spec_df = bait_spec_df.sort_values("total_species", ascending=False)
    bait_spec_df.to_csv(out_dir / "coral_reef_bait_summary.csv", index=False)
    print("Bait Summary (Species caught per bait):")
    print(bait_spec_df.to_string(index=False))
    print(f"\n✓ Saved: coral_reef_bait_summary.csv\n")
    
    print("="*70)
    print("ANALYSIS COMPLETED")
    print("="*70)


if __name__ == "__main__":
    main()
