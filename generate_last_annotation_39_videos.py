import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NORMALIZED_ROOT = ROOT / "normalized_reports" / "cut_47min"
OUTPUT_CSV = ROOT / "lists" / "last_annotation_39_cut_videos.csv"
OUTPUT_MD = ROOT / "lists" / "last_annotation_39_cut_videos.md"

SPLIT_VIDEOS = {
    "20240516-utumbi-mackerel.csv",
    "20240515-milimani-mackerel.csv",
    "20240108-nursery-control.csv",
    "20240106-nursery-mackerel.csv",
    "20240223-nursery-mackerel.csv",
    "20241126-nursery-mackerel.csv",
    "20251212-nursery-mackerel.csv",
}


def format_seconds(sec: float) -> str:
    """Format seconds as MM:SS.ss"""
    minutes = int(sec // 60)
    seconds = sec % 60
    return f"{minutes:02d}:{seconds:06.3f}"


def get_last_annotation(file_path: Path, area: str) -> dict:
    """Get the last annotation from a cut_47min file."""
    last_row = None
    
    with file_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            last_row = row
    
    if last_row is None:
        return {
            "filename": file_path.name,
            "area": area,
            "last_time_sec": None,
            "last_time_formatted": "",
            "species": "",
            "label_name": "",
        }
    
    time_sec = None
    time_max = last_row.get("time_sec_local_max", "").strip()
    if time_max:
        try:
            time_sec = float(time_max)
        except (ValueError, TypeError):
            pass
    
    return {
        "filename": file_path.name,
        "area": area,
        "last_time_sec": time_sec,
        "last_time_formatted": format_seconds(time_sec) if time_sec else "",
        "species": last_row.get("species", "").strip(),
        "label_name": last_row.get("label_name", "").strip(),
    }


def main() -> None:
    results = []
    
    for area_dir in sorted(NORMALIZED_ROOT.iterdir()):
        if area_dir.is_dir():
            area = area_dir.name
            for file_path in sorted(area_dir.glob("*.csv")):
                # Skip split videos
                if file_path.name in SPLIT_VIDEOS:
                    continue
                
                result = get_last_annotation(file_path, area)
                results.append(result)
    
    # Write CSV
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV.open("w", encoding="utf-8", newline="") as f:
        fieldnames = [
            "filename",
            "area",
            "last_time_sec",
            "last_time_formatted",
            "species",
            "label_name",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            writer.writerow({
                "filename": result["filename"],
                "area": result["area"],
                "last_time_sec": f"{result['last_time_sec']:.6f}" if result["last_time_sec"] else "",
                "last_time_formatted": result["last_time_formatted"],
                "species": result["species"],
                "label_name": result["label_name"],
            })
    
    # Write Markdown
    with OUTPUT_MD.open("w", encoding="utf-8") as f:
        f.write("# Letzte Annotation der 39 gekürzten Videos\n\n")
        f.write("Diese Liste zeigt die **letzte beibehaltene Annotation** für jedes der 39 kontinuierlichen Videos nach dem 47-Minuten-Cut.\n\n")
        f.write("*(Die 7 Split-Videos sind nicht enthalten, da sie manuell verarbeitet werden.)*\n\n")
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
            f.write("| # | Dateiname | Letzte Annotation (Zeit) | Sekunden | Art/Label |\n")
            f.write("|---|-----------|--------------------------|----------|------------|\n")
            
            for idx, result in enumerate(areas[area], 1):
                species = result["species"] or result["label_name"][:40]
                time_str = result["last_time_formatted"] if result["last_time_formatted"] else "-"
                sec_str = f"{result['last_time_sec']:.1f}s" if result["last_time_sec"] else "-"
                
                f.write(
                    f"| {idx} "
                    f"| {result['filename']} "
                    f"| {time_str} "
                    f"| {sec_str} "
                    f"| {species} |\n"
                )
            f.write("\n")
        
        # Summary statistics
        f.write("---\n\n")
        f.write("## Zusammenfassung\n\n")
        
        valid_times = [r["last_time_sec"] for r in results if r["last_time_sec"] is not None]
        if valid_times:
            f.write(f"- **Videos gekürzt:** {len(results)}\n")
            f.write(f"- **Kürzeste letzte Annotation:** {format_seconds(min(valid_times))} ({min(valid_times):.1f}s)\n")
            f.write(f"- **Längste letzte Annotation:** {format_seconds(max(valid_times))} ({max(valid_times):.1f}s)\n")
            f.write(f"- **Durchschnitt:** {format_seconds(sum(valid_times)/len(valid_times))} ({sum(valid_times)/len(valid_times):.1f}s)\n")
            
            # Annotations close to 47min (> 45min = 2700s)
            close = [r for r in results if r["last_time_sec"] and r["last_time_sec"] > 2700]
            if close:
                f.write(f"\n### Videos mit letzter Annotation > 45 Minuten (sehr nah an 47min):\n")
                for r in sorted(close, key=lambda x: x["last_time_sec"] or 0, reverse=True):
                    f.write(f"- **{r['filename']}**: {r['last_time_formatted']} ({r['last_time_sec']:.1f}s)\n")
    
    print(f"Processed {len(results)} cut (continuous) videos")
    print(f"CSV output: {OUTPUT_CSV}")
    print(f"Markdown output: {OUTPUT_MD}")


if __name__ == "__main__":
    main()
