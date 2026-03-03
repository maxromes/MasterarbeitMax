import ast
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import List

ROOT = Path(__file__).resolve().parent
INPUT_DIRS = [
    ROOT / "Annotation_reports_coral_reef",
    ROOT / "Annotation_reports_Nursery",
]
OUTPUT_ROOT = ROOT / "normalized_reports"
OUT_ALL = OUTPUT_ROOT / "all_with_flags"
OUT_CUT = OUTPUT_ROOT / "cut_47min"
SUMMARY_FILE = OUTPUT_ROOT / "normalization_summary.csv"

TARGET_SECONDS = 47 * 60
SHORT_VIDEO_NAME = "20240108-nursery-control.csv"
# Split videos with time resets - to be processed manually
SPLIT_VIDEO_NAMES = {
    "20240516-utumbi-mackerel.csv",
    "20240515-milimani-mackerel.csv",
    "20240108-nursery-control.csv",
    "20240106-nursery-mackerel.csv",
    "20240223-nursery-mackerel.csv",
    "20241126-nursery-mackerel.csv",
    "20251212-nursery-mackerel.csv",
}


@dataclass
class FileSummary:
    filename: str
    area: str
    rows_total: int
    rows_kept_47min: int
    rows_removed_after_47min: int
    frame_values_total: int
    frame_values_kept_47min: int
    max_original_seconds: float
    is_short_control_nursery: bool
    is_split_video: bool


def parse_frame_values(raw: str) -> List[float]:
    if raw is None:
        return []
    text = raw.strip()
    if not text:
        return []

    try:
        value = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        return []

    if isinstance(value, (int, float)):
        return [float(value)]
    if isinstance(value, list):
        result: List[float] = []
        for item in value:
            if isinstance(item, (int, float)):
                result.append(float(item))
        return result
    return []


def format_frame_list(values: List[float]) -> str:
    return "[" + ",".join(f"{v:.6f}" for v in values) + "]"


def process_file(input_path: Path, area: str) -> FileSummary:
    """Process file: copy split videos unchanged, normalize continuous videos to 47min."""
    out_all_path = OUT_ALL / area / input_path.name
    out_cut_path = OUT_CUT / area / input_path.name
    out_all_path.parent.mkdir(parents=True, exist_ok=True)
    out_cut_path.parent.mkdir(parents=True, exist_ok=True)

    is_short_control_nursery = input_path.name == SHORT_VIDEO_NAME
    is_split_video = input_path.name in SPLIT_VIDEO_NAMES
    
    # For split videos: copy unchanged, mark for manual processing
    if is_split_video:
        import shutil
        shutil.copy2(input_path, out_all_path)
        shutil.copy2(input_path, out_cut_path)
        
        # Count rows for summary
        with input_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            total_rows = len(rows)
        
        return FileSummary(
            filename=input_path.name,
            area=area,
            rows_total=total_rows,
            rows_kept_47min=total_rows,  # All kept for manual processing
            rows_removed_after_47min=0,
            frame_values_total=total_rows,
            frame_values_kept_47min=total_rows,
            max_original_seconds=0.0,  # Not calculated for split videos
            is_short_control_nursery=is_short_control_nursery,
            is_split_video=True,
        )

    # Process continuous (non-split) videos with 47min cutoff
    with input_path.open("r", encoding="utf-8", newline="") as infile:
        reader = csv.DictReader(infile)
        original_fields = reader.fieldnames or []
        extra_fields = [
            "time_sec_local",
            "time_sec_local_first",
            "time_sec_local_last",
            "time_sec_local_max",
            "included_47min",
            "is_short_control_nursery",
            "is_split_video",
            "frames_kept_47min",
            "frame_count_raw",
            "frame_count_kept_47min",
        ]
        out_fields = original_fields + [f for f in extra_fields if f not in original_fields]

        with out_all_path.open("w", encoding="utf-8", newline="") as out_all, out_cut_path.open(
            "w", encoding="utf-8", newline=""
        ) as out_cut:
            writer_all = csv.DictWriter(out_all, fieldnames=out_fields)
            writer_cut = csv.DictWriter(out_cut, fieldnames=out_fields)
            writer_all.writeheader()
            writer_cut.writeheader()

            rows_total = 0
            rows_kept = 0
            frame_values_total = 0
            frame_values_kept = 0
            max_original = 0.0

            for row in reader:
                rows_total += 1
                local_values = parse_frame_values(row.get("frames", ""))
                frame_values_total += len(local_values)
                if local_values:
                    max_original = max(max_original, max(local_values))

                kept_values = [v for v in local_values if v <= TARGET_SECONDS]
                frame_values_kept += len(kept_values)
                included = len(kept_values) > 0
                if included:
                    rows_kept += 1

                row_out = dict(row)
                row_out["time_sec_local"] = format_frame_list(local_values)
                row_out["time_sec_local_first"] = f"{local_values[0]:.6f}" if local_values else ""
                row_out["time_sec_local_last"] = f"{local_values[-1]:.6f}" if local_values else ""
                row_out["time_sec_local_max"] = f"{max(local_values):.6f}" if local_values else ""
                row_out["included_47min"] = "TRUE" if included else "FALSE"
                row_out["is_short_control_nursery"] = "TRUE" if is_short_control_nursery else "FALSE"
                row_out["is_split_video"] = "FALSE"
                row_out["frames_kept_47min"] = format_frame_list(kept_values)
                row_out["frame_count_raw"] = str(len(local_values))
                row_out["frame_count_kept_47min"] = str(len(kept_values))

                writer_all.writerow(row_out)
                if included:
                    writer_cut.writerow(row_out)

    return FileSummary(
        filename=input_path.name,
        area=area,
        rows_total=rows_total,
        rows_kept_47min=rows_kept,
        rows_removed_after_47min=rows_total - rows_kept,
        frame_values_total=frame_values_total,
        frame_values_kept_47min=frame_values_kept,
        max_original_seconds=max_original,
        is_short_control_nursery=is_short_control_nursery,
        is_split_video=False,
    )


def main() -> None:
    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)

    summaries: List[FileSummary] = []
    for input_dir in INPUT_DIRS:
        area = input_dir.name
        files = sorted(input_dir.glob("*.csv"))
        for file_path in files:
            summaries.append(process_file(file_path, area))

    with SUMMARY_FILE.open("w", encoding="utf-8", newline="") as summary_out:
        fieldnames = [
            "filename",
            "area",
            "rows_total",
            "rows_kept_47min",
            "rows_removed_after_47min",
            "frame_values_total",
            "frame_values_kept_47min",
            "max_original_seconds",
            "is_short_control_nursery",
            "is_split_video",
        ]
        writer = csv.DictWriter(summary_out, fieldnames=fieldnames)
        writer.writeheader()
        for item in summaries:
            writer.writerow(
                {
                    "filename": item.filename,
                    "area": item.area,
                    "rows_total": item.rows_total,
                    "rows_kept_47min": item.rows_kept_47min,
                    "rows_removed_after_47min": item.rows_removed_after_47min,
                    "frame_values_total": item.frame_values_total,
                    "frame_values_kept_47min": item.frame_values_kept_47min,
                    "max_original_seconds": f"{item.max_original_seconds:.6f}",
                    "is_short_control_nursery": "TRUE" if item.is_short_control_nursery else "FALSE",
                    "is_split_video": "TRUE" if item.is_split_video else "FALSE",
                }
            )

    split_count = sum(1 for s in summaries if s.is_split_video)
    normalized_count = len(summaries) - split_count
    
    print(f"Processed files: {len(summaries)}")
    print(f"  - Split videos (copied for manual processing): {split_count}")
    print(f"  - Continuous videos (normalized to 47min): {normalized_count}")
    print(f"Output (all rows): {OUT_ALL}")
    print(f"Output (cut <=47min): {OUT_CUT}")
    print(f"Summary: {SUMMARY_FILE}")


if __name__ == "__main__":
    main()
