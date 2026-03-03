import csv
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent
NORMALIZED_ROOT = ROOT / "normalized_reports" / "all_with_flags"
OUTPUT_CSV = ROOT / "lists" / "last_annotation_before_47min.csv"
OUTPUT_MD = ROOT / "lists" / "last_annotation_before_47min.md"

TARGET_SECONDS = 47 * 60


def format_seconds(sec: float) -> str:
    """Format seconds as MM:SS.ss"""
    minutes = int(sec // 60)
    seconds = sec % 60
    return f"{minutes:02d}:{seconds:06.3f}"


def process_file(file_path: Path, area: str) -> dict:
    """Extract last annotation before 47min and first after from a normalized file."""
    last_before = None
    first_after = None
    
    with file_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time_max = row.get("time_sec_local_max", "").strip()
            included = row.get("included_47min", "").strip()
            
            if time_max:
                try:
                    time_val = float(time_max)
                    if included == "TRUE":
                        last_before = {
                            "time_sec": time_val,
                            "species": row.get("species", "").strip(),
                            "label_name": row.get("label_name", "").strip()
                        }
                    elif included == "FALSE" and first_after is None:
                        first_after = {
                            "time_sec": time_val,
                            "species": row.get("species", "").strip(),
                            "label_name": row.get("label_name", "").strip()
                        }
                except (ValueError, TypeError):
                    pass
    
    return {
        "filename": file_path.name,
        "area": area,
        "last_annotation_sec": last_before["time_sec"] if last_before else None,
        "last_annotation_time": format_seconds(last_before["time_sec"]) if last_before else "",
        "last_annotation_species": last_before["species"] if last_before else "",
        "last_annotation_label": last_before["label_name"] if last_before else "",
        "first_excluded_sec": first_after["time_sec"] if first_after else None,
        "first_excluded_time": format_seconds(first_after["time_sec"]) if first_after else "",
        "gap_to_47min_sec": (TARGET_SECONDS - last_before["time_sec"]) if last_before else None,
    }


def main() -> None:
    results = []
    
    for area_dir in sorted(NORMALIZED_ROOT.iterdir()):
        if area_dir.is_dir():
            area = area_dir.name
            for file_path in sorted(area_dir.glob("*.csv")):
                result = process_file(file_path, area)
                results.append(result)
    
    # Write CSV
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "filename",
            "area",
            "last_annotation_sec",
            "last_annotation_time",
            "gap_to_47min_sec",
            "first_excluded_sec",
            "first_excluded_time",
            "last_annotation_species",
            "last_annotation_label",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            writer.writerow({
                "filename": result["filename"],
                "area": result["area"],
                "last_annotation_sec": f"{result['last_annotation_sec']:.3f}" if result["last_annotation_sec"] else "",
                "last_annotation_time": result["last_annotation_time"],
                "gap_to_47min_sec": f"{result['gap_to_47min_sec']:.3f}" if result["gap_to_47min_sec"] else "",
                "first_excluded_sec": f"{result['first_excluded_sec']:.3f}" if result["first_excluded_sec"] else "",
                "first_excluded_time": result["first_excluded_time"],
                "last_annotation_species": result["last_annotation_species"],
                "last_annotation_label": result["last_annotation_label"],
            })
    
    # Write Markdown
    with OUTPUT_MD.open("w", encoding="utf-8") as f:
        f.write("# Letzte Annotation vor 47 Minuten - Übersicht zur manuellen Prüfung\n\n")
        f.write(f"**Ziel:** 47:00 Minuten = {TARGET_SECONDS} Sekunden\n\n")
        f.write("Diese Liste zeigt für jede Datei die letzte eingeschlossene Annotation vor der 47-Minuten-Grenze.\n\n")
        f.write("---\n\n")
        
        # Group by area
        areas = {}
        for result in results:
            area = result["area"]
            if area not in areas:
                areas[area] = []
            areas[area].append(result)
        
        for area in sorted(areas.keys()):
            f.write(f"## {area}\n\n")
            f.write("| Dateiname | Letzte Annotation | Zeit | Lücke zu 47min | Erste ausgeschlossen | Art/Label |\n")
            f.write("|-----------|-------------------|------|----------------|---------------------|------------|\n")
            
            for result in areas[area]:
                gap = f"{result['gap_to_47min_sec']:.1f}s" if result["gap_to_47min_sec"] is not None else "-"
                excluded = result["first_excluded_time"] if result["first_excluded_time"] else "-"
                species = result["last_annotation_species"] or result["last_annotation_label"][:30]
                last_sec = f"{result['last_annotation_sec']:.1f}s" if result['last_annotation_sec'] else "-"
                
                f.write(
                    f"| {result['filename']} "
                    f"| {last_sec} "
                    f"| {result['last_annotation_time']} "
                    f"| {gap} "
                    f"| {excluded} "
                    f"| {species} |\n"
                )
            f.write("\n")
        
        # Summary statistics
        f.write("---\n\n")
        f.write("## Zusammenfassung\n\n")
        
        gaps = [r["gap_to_47min_sec"] for r in results if r["gap_to_47min_sec"] is not None]
        if gaps:
            f.write(f"- **Dateien gesamt:** {len(results)}\n")
            f.write(f"- **Kleinste Lücke:** {min(gaps):.1f} Sekunden\n")
            f.write(f"- **Größte Lücke:** {max(gaps):.1f} Sekunden\n")
            f.write(f"- **Durchschnittliche Lücke:** {sum(gaps)/len(gaps):.1f} Sekunden\n")
            
            # Files close to 47min (within 60 seconds)
            close_files = [r for r in results if r["gap_to_47min_sec"] is not None and r["gap_to_47min_sec"] < 60]
            if close_files:
                f.write(f"\n### Dateien nahe an 47min (< 60s Lücke):\n")
                for r in close_files:
                    f.write(f"- {r['filename']}: {r['last_annotation_time']} (Lücke: {r['gap_to_47min_sec']:.1f}s)\n")
    
    print(f"Processed {len(results)} files")
    print(f"CSV output: {OUTPUT_CSV}")
    print(f"Markdown output: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
