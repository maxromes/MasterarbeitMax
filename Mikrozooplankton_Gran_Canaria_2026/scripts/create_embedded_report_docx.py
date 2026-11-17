from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt


PROJECT_DIR = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_DIR / "results" / "report_documents"
SOURCE = REPORT_DIR / "mikrozooplankton_phytoplankton_bericht.md"
OUTPUT = REPORT_DIR / "mikrozooplankton_phytoplankton_bericht.docx"


def add_markdown_paragraph(document: Document, line: str) -> None:
    if not line.strip():
        return
    heading = re.match(r"^(#{1,3})\s+(.+)$", line)
    if heading:
        level = len(heading.group(1))
        document.add_heading(heading.group(2).strip(), level=level)
        return
    if line.startswith("> "):
        paragraph = document.add_paragraph(style="Intense Quote")
        paragraph.add_run(line[2:])
        return
    paragraph = document.add_paragraph()
    parts = re.split(r"(\*\*.*?\*\*|`.*?`)", line)
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            paragraph.add_run(part[2:-2]).bold = True
        elif part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            run.font.name = "Courier New"
        else:
            paragraph.add_run(part)


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    document = Document()
    section = document.sections[0]
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.9)
    section.right_margin = Inches(0.9)
    styles = document.styles
    styles["Normal"].font.name = "Arial"
    styles["Normal"].font.size = Pt(10.5)

    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        image = re.match(r"^!\[[^\]]*\]\(([^)]+)\)$", line)
        if image:
            image_path = (SOURCE.parent / image.group(1)).resolve()
            if not image_path.exists():
                raise FileNotFoundError(image_path)
            paragraph = document.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.add_run().add_picture(str(image_path), width=Inches(6.3))
            continue
        add_markdown_paragraph(document, line)

    document.save(OUTPUT)
    print(f"Erstellt: {OUTPUT}")


if __name__ == "__main__":
    main()
