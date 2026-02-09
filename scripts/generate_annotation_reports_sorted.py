#!/usr/bin/env python3
"""Generate a markdown list of annotation report files sorted by filename."""

from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
OUTPUT_FILE = BASE_DIR / "data" / "annotation_reports_sorted.md"
FOLDERS = [
    "Annotation_reports_coral_reef",
    "Annotation_reports_Nursery",
]


def list_sorted(folder: Path) -> list[str]:
    return sorted(p.name for p in folder.iterdir() if p.is_file() and p.suffix.lower() == ".csv")


def main() -> None:
    lines = ["# Annotation reports (sorted)", ""]

    for folder_name in FOLDERS:
        folder = BASE_DIR / folder_name
        lines.append(f"## {folder_name}")
        lines.append("")

        for name in list_sorted(folder):
            lines.append(f"- {name}")

        lines.append("")

    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
