#!/usr/bin/env python3
"""
Coral Reef Fish Overlap & Bait Specificity Visualizations
Erstellt übersichtliche Grafiken für Fish-Overlap und Bait-Spezifität
"""

from pathlib import Path
import re
from collections import defaultdict

import pandas as pd
import numpy as np


def parse_filename(filename: str) -> dict:
    """Parse metadata from filename"""
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
    
    site = "milimani" if "milimani" in site else "utumbi" if "utumbi" in site else site
    
    return {
        "date": date,
        "site": site,
        "bait": bait.lower(),
        "filename": filename
    }


def get_species_name(row: pd.Series) -> str:
    """Extract highest taxonomic level"""
    for col in ["species", "genus", "family", "unspecific"]:
        value = str(row.get(col, "")).strip()
        if value and value != "nan" and value != "":
            return value
    return "unidentified"


def svg_header(width: int, height: int) -> str:
    return f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' viewBox='0 0 {width} {height}'>\n"


def svg_footer() -> str:
    return "</svg>\n"


def svg_text(x: float, y: float, text: str, size: int = 12, anchor: str = "middle", bold: bool = False) -> str:
    safe_text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    weight = "bold" if bold else "normal"
    return f"<text x='{x}' y='{y}' font-size='{size}' font-weight='{weight}' text-anchor='{anchor}' font-family='DejaVu Sans, Arial' fill='#2b2b2b'>{safe_text}</text>\n"


def svg_rect(x: float, y: float, width: float, height: float, fill: str = "#b3cde3", stroke: str = "#2b2b2b") -> str:
    return f"<rect x='{x}' y='{y}' width='{width}' height='{height}' fill='{fill}' stroke='{stroke}'/>\n"


def svg_line(x1: float, y1: float, x2: float, y2: float, stroke: str = "#2b2b2b", width: str = "1") -> str:
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{stroke}' stroke-width='{width}'/>\n"


def create_bait_specificity_chart(site: str, out_path: Path):
    """Create bar chart showing fish species count per bait"""
    
    report_dir = Path("Annotation_reports_coral_reef")
    site_bait_count = defaultdict(int)
    
    for file_path in report_dir.glob("*.csv"):
        meta = parse_filename(file_path.name)
        if meta["site"] != site:
            continue
        
        try:
            data = pd.read_csv(file_path)
            data["species_name"] = data.apply(get_species_name, axis=1)
            unique_species = set(data["species_name"].unique())
            unique_species.discard("unidentified")
            
            bait = meta["bait"]
            site_bait_count[bait] = max(site_bait_count[bait], len(unique_species))
        except:
            pass
    
    if not site_bait_count:
        return
    
    baits = sorted(site_bait_count.keys())
    counts = [site_bait_count[b] for b in baits]
    
    width, height = 900, 500
    margin = dict(left=100, right=20, top=60, bottom=150)
    plot_w = width - margin["left"] - margin["right"]
    plot_h = height - margin["top"] - margin["bottom"]
    
    max_count = max(counts) if counts else 1
    y_max = max_count + 3
    
    colors = ["#1f78b4", "#33a02c", "#e31a1c", "#ff7f00", "#6a3d9a", "#a6cee3", "#fb9a99", "#fdbf6f"]
    
    svg = [svg_header(width, height)]
    svg.append(svg_text(width / 2, 35, f"Fish Species per Bait Type - {site.upper()}", size=18, bold=True))
    
    # Axes
    x0 = margin["left"]
    y0 = margin["top"] + plot_h
    x1 = width - margin["right"]
    y1 = margin["top"]
    
    svg.append(svg_line(x0, y0, x1, y0, stroke="#2b2b2b", width="2"))
    svg.append(svg_line(x0, y0, x0, y1, stroke="#2b2b2b", width="2"))
    
    # Y-axis ticks and labels
    for tick in np.linspace(0, y_max, 6):
        y = y0 - (tick / y_max) * plot_h
        svg.append(svg_line(x0 - 5, y, x0, y, stroke="#2b2b2b"))
        svg.append(svg_text(x0 - 10, y + 4, str(int(tick)), size=11, anchor="end"))
    
    # Y-axis label
    svg.append(f"<g transform='translate(25,{height/2}) rotate(-90)'><text font-size='12' text-anchor='middle' font-family='DejaVu Sans'>Species Count</text></g>\n")
    
    # Bars
    bar_width = plot_w / (len(baits) * 1.3)
    
    for i, (bait, count) in enumerate(zip(baits, counts)):
        x = x0 + (i + 0.3) * (plot_w / len(baits))
        bar_height = (count / y_max) * plot_h
        y = y0 - bar_height
        
        color = colors[i % len(colors)]
        svg.append(svg_rect(x, y, bar_width, bar_height, fill=color))
        svg.append(svg_text(x + bar_width / 2, y - 10, str(count), size=11, bold=True))
        
        # X-axis label
        svg.append(f"<g transform='translate({x + bar_width/2},{y0 + 20}) rotate(-30)'><text font-size='11' text-anchor='end' font-family='DejaVu Sans'>{bait.upper()}</text></g>\n")
    
    svg.append(svg_text(width / 2, height - 20, "Bait Type", size=12))
    svg.append(svg_footer())
    
    out_path.write_text("".join(svg), encoding="utf-8")


def create_overlap_pie_chart(site: str, overlap_stats: dict, out_path: Path):
    """Create pie chart for fish specificity distribution"""
    
    ubiquitous = overlap_stats.get("ubiquitous", 0)
    multi_bait = overlap_stats.get("multi-bait", 0)
    specific = overlap_stats.get("bait-specific", 0)
    
    total = ubiquitous + multi_bait + specific
    if total == 0:
        return
    
    width, height = 600, 500
    cx, cy = width / 2, height / 2 - 30
    radius = 120
    
    colors = {
        "ubiquitous": "#1f78b4",
        "multi-bait": "#33a02c",
        "bait-specific": "#e31a1c"
    }
    
    data = [
        ("Ubiquitous (3+ baits)", ubiquitous, colors["ubiquitous"]),
        ("Multi-bait (2 baits)", multi_bait, colors["multi-bait"]),
        ("Bait-specific (1 bait)", specific, colors["bait-specific"])
    ]
    
    svg = [svg_header(width, height)]
    svg.append(svg_text(width / 2, 30, f"Fish Specificity Distribution - {site.upper()}", size=16, bold=True))
    
    current_angle = 0
    for label, count, color in data:
        angle_size = (count / total) * 360
        
        # Draw slice (simplified pie chart)
        svg.append(f"<circle cx='{cx}' cy='{cy}' r='{radius}' fill='none' stroke='{color}' stroke-width='25' opacity='0.7' "
                  f"stroke-dasharray='{radius * np.pi * angle_size / 180:.1f} {radius * np.pi * 2:.1f}' "
                  f"transform='rotate({current_angle} {cx} {cy})'/>\n")
        
        current_angle += angle_size
    
    # Legend
    legend_x = width - 280
    legend_y = 80
    for i, (label, count, color) in enumerate(data):
        y = legend_y + i * 35
        svg.append(svg_rect(legend_x, y - 10, 15, 15, fill=color, stroke="#2b2b2b"))
        svg.append(svg_text(legend_x + 25, y, f"{label}: {count} ({round(100*count/total, 1)}%)", 
                           size=11, anchor="start"))
    
    svg.append(svg_footer())
    out_path.write_text("".join(svg), encoding="utf-8")


def create_cross_site_comparison_chart(out_path: Path):
    """Create bar chart comparing species overlap between sites"""
    
    report_dir = Path("Annotation_reports_coral_reef")
    site_bait_fish = defaultdict(lambda: defaultdict(set))
    
    # Collect data
    for file_path in report_dir.glob("*.csv"):
        meta = parse_filename(file_path.name)
        
        try:
            data = pd.read_csv(file_path)
            data["species_name"] = data.apply(get_species_name, axis=1)
            unique_species = set(data["species_name"].unique())
            unique_species.discard("unidentified")
            
            site_bait_fish[meta["site"]][meta["bait"]].update(unique_species)
        except:
            pass
    
    # Find common baits
    milimani_baits = set(site_bait_fish["milimani"].keys())
    utumbi_baits = set(site_bait_fish["utumbi"].keys())
    common_baits = sorted(milimani_baits & utumbi_baits)
    
    if not common_baits:
        return
    
    width, height = 900, 500
    margin = dict(left=80, right=20, top=60, bottom=150)
    plot_w = width - margin["left"] - margin["right"]
    plot_h = height - margin["top"] - margin["bottom"]
    
    x0, y0 = margin["left"], margin["top"] + plot_h
    
    svg = [svg_header(width, height)]
    svg.append(svg_text(width / 2, 35, "Fish Species Overlap Between Sites (Same Bait)", size=16, bold=True))
    
    # Axes
    svg.append(svg_line(x0, y0, width - margin["right"], y0, stroke="#2b2b2b", width="2"))
    svg.append(svg_line(x0, y0, x0, margin["top"], stroke="#2b2b2b", width="2"))
    
    # Y-axis
    max_val = 25
    for tick in np.linspace(0, max_val, 6):
        y = y0 - (tick / max_val) * plot_h
        svg.append(svg_line(x0 - 5, y, x0, y))
        svg.append(svg_text(x0 - 10, y + 4, str(int(tick)), size=10, anchor="end"))
    
    svg.append(svg_text(25, height / 2, "Species Count", size=11, anchor="middle"))
    
    # Draw bars grouped by bait
    bar_width = plot_w / (len(common_baits) * 3.2)
    colors_bars = ["#4daf4a", "#984ea3"]  # Milimani, Utumbi
    
    for i, bait in enumerate(common_baits):
        x_base = x0 + (i + 0.3) * (plot_w / len(common_baits))
        
        milimani_count = len(site_bait_fish["milimani"][bait])
        utumbi_count = len(site_bait_fish["utumbi"][bait])
        
        # Milimani bar
        bar_height = (milimani_count / max_val) * plot_h
        svg.append(svg_rect(x_base, y0 - bar_height, bar_width, bar_height, fill=colors_bars[0]))
        
        # Utumbi bar
        x_base2 = x_base + bar_width + 3
        bar_height2 = (utumbi_count / max_val) * plot_h
        svg.append(svg_rect(x_base2, y0 - bar_height2, bar_width, bar_height2, fill=colors_bars[1]))
        
        # Label
        label_x = x_base + bar_width
        svg.append(f"<g transform='translate({label_x},{y0 + 25}) rotate(-30)'><text font-size='10' text-anchor='end' font-family='DejaVu Sans'>{bait.upper()}</text></g>\n")
    
    # Legend
    legend_x, legend_y = width - 200, 80
    svg.append(svg_rect(legend_x, legend_y - 10, 12, 12, fill=colors_bars[0]))
    svg.append(svg_text(legend_x + 18, legend_y, "Milimani", size=11, anchor="start"))
    svg.append(svg_rect(legend_x, legend_y + 20, 12, 12, fill=colors_bars[1]))
    svg.append(svg_text(legend_x + 18, legend_y + 25, "Utumbi", size=11, anchor="start"))
    
    svg.append(svg_text(width / 2, height - 20, "Bait Type", size=12))
    svg.append(svg_footer())
    
    out_path.write_text("".join(svg), encoding="utf-8")


def main():
    out_dir = Path("results")
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    
    print("\n" + "="*70)
    print("GENERATING VISUALIZATIONS")
    print("="*70 + "\n")
    
    # 1. Bait specificity charts
    for site in ["milimani", "utumbi"]:
        print(f"Creating bait specificity chart for {site}...")
        create_bait_specificity_chart(site, fig_dir / f"coral_reef_{site}_bait_species.svg")
        print(f"  ✓ coral_reef_{site}_bait_species.svg\n")
    
    # 2. Overlap pie charts (need to read CSV files to get stats)
    print("Analyzing overlap statistics...")
    for site in ["milimani", "utumbi"]:
        csv_path = out_dir / f"coral_reef_{site}_fish_overlap.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path)
            overlap_stats = {
                "ubiquitous": len(df[df["specificity"] == "ubiquitous"]),
                "multi-bait": len(df[df["specificity"] == "multi-bait"]),
                "bait-specific": len(df[df["specificity"] == "bait-specific"])
            }
            print(f"Creating overlap pie chart for {site}...")
            create_overlap_pie_chart(site, overlap_stats, fig_dir / f"coral_reef_{site}_fish_specificity.svg")
            print(f"  ✓ coral_reef_{site}_fish_specificity.svg\n")
    
    # 3. Cross-site comparison
    print("Creating cross-site comparison chart...")
    create_cross_site_comparison_chart(fig_dir / "coral_reef_cross_site_comparison.svg")
    print("  ✓ coral_reef_cross_site_comparison.svg\n")
    
    print("="*70)
    print("VISUALIZATIONS COMPLETED")
    print("="*70)


if __name__ == "__main__":
    main()
