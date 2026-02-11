#!/usr/bin/env python3
"""
Species richness comparison for coral reef annotation reports.
Creates per-bait plots and summary tables.
"""

from __future__ import annotations

from pathlib import Path
import re

import numpy as np
import pandas as pd


def parse_filename(file_name: str) -> dict:
    """Parse metadata from filename like 20241025-milimani-mackerel-c10.csv."""
    stem = file_name.replace(".csv", "")
    parts = stem.split("-")
    date = parts[0] if parts else "unknown"
    site = parts[1] if len(parts) > 1 else "unknown"

    bait = "unknown"
    camera = ""
    if len(parts) > 2:
        bait = parts[2]
        if len(parts) > 3:
            if re.match(r"^c\d+$", parts[3]):
                camera = parts[3]
            else:
                # If bait itself includes a dash, join remaining parts.
                bait = "-".join(parts[2:])
    return {"date": date, "site": site, "bait": bait, "camera": camera}


def collect_richness(report_dir: Path) -> pd.DataFrame:
    rows = []
    for file_path in sorted(report_dir.glob("*.csv")):
        data = pd.read_csv(file_path)
        richness = data["label_name"].nunique()
        meta = parse_filename(file_path.name)
        rows.append(
            {
                "file_name": file_path.name,
                "date": meta["date"],
                "site": meta["site"],
                "bait": meta["bait"],
                "camera": meta["camera"],
                "species_richness": richness,
            }
        )
    return pd.DataFrame(rows)


def _svg_header(width: int, height: int) -> str:
    return (
        f"<svg xmlns='http://www.w3.org/2000/svg' width='{width}' height='{height}' "
        f"viewBox='0 0 {width} {height}'>\n"
    )


def _svg_footer() -> str:
    return "</svg>\n"


def _svg_text(x: float, y: float, text: str, size: int = 12, anchor: str = "middle") -> str:
    safe_text = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    return (
        f"<text x='{x}' y='{y}' font-size='{size}' text-anchor='{anchor}' "
        f"font-family='DejaVu Sans, Arial, sans-serif'>{safe_text}</text>\n"
    )


def _scale(value: float, vmin: float, vmax: float, out_min: float, out_max: float) -> float:
    if vmax == vmin:
        return (out_min + out_max) / 2
    return out_min + (value - vmin) * (out_max - out_min) / (vmax - vmin)


def _box_stats(values: np.ndarray) -> dict:
    q1 = float(np.percentile(values, 25))
    q3 = float(np.percentile(values, 75))
    median = float(np.median(values))
    iqr = q3 - q1
    lower = float(np.min(values[values >= q1 - 1.5 * iqr]))
    upper = float(np.max(values[values <= q3 + 1.5 * iqr]))
    return {"q1": q1, "q3": q3, "median": median, "lower": lower, "upper": upper}


def plot_richness_by_bait(df: pd.DataFrame, out_path: Path) -> None:
    bait_order = (
        df.groupby("bait")["species_richness"].mean().sort_values(ascending=False).index.tolist()
    )
    data_by_bait = [df.loc[df["bait"] == b, "species_richness"].values for b in bait_order]

    width, height = 900, 500
    margin = dict(left=70, right=20, top=50, bottom=100)
    plot_w = width - margin["left"] - margin["right"]
    plot_h = height - margin["top"] - margin["bottom"]

    y_values = df["species_richness"].values
    y_min = max(0, float(np.min(y_values)) - 1)
    y_max = float(np.max(y_values)) + 1

    svg = [_svg_header(width, height)]
    svg.append(_svg_text(width / 2, 28, "Species richness per bait (coral reef reports)", size=16))

    # Axes
    x0 = margin["left"]
    y0 = margin["top"] + plot_h
    x1 = margin["left"] + plot_w
    y1 = margin["top"]
    svg.append(f"<line x1='{x0}' y1='{y0}' x2='{x1}' y2='{y0}' stroke='#2b2b2b'/>\n")
    svg.append(f"<line x1='{x0}' y1='{y0}' x2='{x0}' y2='{y1}' stroke='#2b2b2b'/>\n")

    # Y ticks
    for tick in np.linspace(y_min, y_max, 5):
        y = _scale(tick, y_min, y_max, y0, y1)
        svg.append(f"<line x1='{x0-4}' y1='{y}' x2='{x0}' y2='{y}' stroke='#2b2b2b'/>\n")
        svg.append(_svg_text(x0 - 8, y + 4, f"{tick:.0f}", size=11, anchor="end"))

    # Boxes and points
    rng = np.random.default_rng(42)
    for i, bait in enumerate(bait_order):
        values = data_by_bait[i]
        stats = _box_stats(values)
        x_center = x0 + (i + 0.5) * (plot_w / len(bait_order))
        box_width = plot_w / len(bait_order) * 0.45

        y_q1 = _scale(stats["q1"], y_min, y_max, y0, y1)
        y_q3 = _scale(stats["q3"], y_min, y_max, y0, y1)
        y_med = _scale(stats["median"], y_min, y_max, y0, y1)
        y_low = _scale(stats["lower"], y_min, y_max, y0, y1)
        y_up = _scale(stats["upper"], y_min, y_max, y0, y1)

        svg.append(
            f"<rect x='{x_center - box_width/2}' y='{y_q3}' width='{box_width}' "
            f"height='{y_q1 - y_q3}' fill='#b3cde3' stroke='#2b2b2b'/>\n"
        )
        svg.append(f"<line x1='{x_center - box_width/2}' y1='{y_med}' "
                   f"x2='{x_center + box_width/2}' y2='{y_med}' stroke='#2b2b2b'/>\n")
        svg.append(f"<line x1='{x_center}' y1='{y_q3}' x2='{x_center}' y2='{y_up}' "
                   f"stroke='#2b2b2b'/>\n")
        svg.append(f"<line x1='{x_center}' y1='{y_q1}' x2='{x_center}' y2='{y_low}' "
                   f"stroke='#2b2b2b'/>\n")
        svg.append(f"<line x1='{x_center - box_width/4}' y1='{y_up}' "
                   f"x2='{x_center + box_width/4}' y2='{y_up}' stroke='#2b2b2b'/>\n")
        svg.append(f"<line x1='{x_center - box_width/4}' y1='{y_low}' "
                   f"x2='{x_center + box_width/4}' y2='{y_low}' stroke='#2b2b2b'/>\n")

        jitter = rng.normal(0, box_width * 0.15, size=len(values))
        for value, j in zip(values, jitter):
            y = _scale(value, y_min, y_max, y0, y1)
            svg.append(
                f"<circle cx='{x_center + j}' cy='{y}' r='3' fill='#1f78b4' opacity='0.8'/>\n"
            )

        # X labels
        svg.append(
            f"<g transform='translate({x_center},{y0 + 30}) rotate(-30)'>"
            f"<text font-size='11' text-anchor='end' font-family='DejaVu Sans, Arial, sans-serif'>{bait}</text>"
            "</g>\n"
        )

    svg.append(_svg_text(width / 2, height - 10, "Bait", size=12))
    svg.append(
        f"<g transform='translate(18,{height/2}) rotate(-90)'>"
        f"<text font-size='12' text-anchor='middle' font-family='DejaVu Sans, Arial, sans-serif'>Species richness</text>"
        "</g>\n"
    )
    svg.append(_svg_footer())

    out_path.write_text("".join(svg), encoding="utf-8")


def plot_mean_by_bait_and_site(df: pd.DataFrame, out_path: Path) -> None:
    summary = (
        df.groupby(["bait", "site"])["species_richness"]
        .agg(["mean", "std", "count"])
        .reset_index()
    )

    bait_order = summary.groupby("bait")["mean"].mean().sort_values(ascending=False).index.tolist()
    sites = sorted(summary["site"].unique().tolist())
    colors = {"milimani": "#4daf4a", "utumbi": "#984ea3"}

    width, height = 900, 500
    margin = dict(left=70, right=20, top=50, bottom=100)
    plot_w = width - margin["left"] - margin["right"]
    plot_h = height - margin["top"] - margin["bottom"]

    max_mean = float(summary["mean"].max()) if not summary.empty else 1
    max_std = float(summary["std"].fillna(0).max()) if not summary.empty else 0
    y_min = 0
    y_max = max_mean + max_std + 1

    svg = [_svg_header(width, height)]
    svg.append(_svg_text(width / 2, 28, "Mean species richness by bait and site", size=16))

    x0 = margin["left"]
    y0 = margin["top"] + plot_h
    x1 = margin["left"] + plot_w
    y1 = margin["top"]
    svg.append(f"<line x1='{x0}' y1='{y0}' x2='{x1}' y2='{y0}' stroke='#2b2b2b'/>\n")
    svg.append(f"<line x1='{x0}' y1='{y0}' x2='{x0}' y2='{y1}' stroke='#2b2b2b'/>\n")

    for tick in np.linspace(y_min, y_max, 5):
        y = _scale(tick, y_min, y_max, y0, y1)
        svg.append(f"<line x1='{x0-4}' y1='{y}' x2='{x0}' y2='{y}' stroke='#2b2b2b'/>\n")
        svg.append(_svg_text(x0 - 8, y + 4, f"{tick:.0f}", size=11, anchor="end"))

    group_width = plot_w / len(bait_order)
    bar_width = group_width / max(len(sites), 1) * 0.7

    for i, bait in enumerate(bait_order):
        group_x = x0 + i * group_width
        for j, site in enumerate(sites):
            row = summary[(summary["bait"] == bait) & (summary["site"] == site)]
            if row.empty:
                continue
            mean_val = float(row["mean"].iloc[0])
            std_val = float(row["std"].fillna(0).iloc[0])
            bar_x = group_x + (j + 0.15) * (group_width / max(len(sites), 1))
            bar_y = _scale(mean_val, y_min, y_max, y0, y1)
            bar_h = y0 - bar_y

            svg.append(
                f"<rect x='{bar_x}' y='{bar_y}' width='{bar_width}' height='{bar_h}' "
                f"fill='{colors.get(site, '#a6cee3')}' opacity='0.85'/>\n"
            )

            err_top = _scale(mean_val + std_val, y_min, y_max, y0, y1)
            err_bottom = _scale(max(mean_val - std_val, y_min), y_min, y_max, y0, y1)
            center_x = bar_x + bar_width / 2
            svg.append(f"<line x1='{center_x}' y1='{err_top}' x2='{center_x}' y2='{err_bottom}' "
                       f"stroke='#2b2b2b'/>\n")
            svg.append(f"<line x1='{center_x - 4}' y1='{err_top}' x2='{center_x + 4}' y2='{err_top}' "
                       f"stroke='#2b2b2b'/>\n")
            svg.append(f"<line x1='{center_x - 4}' y1='{err_bottom}' x2='{center_x + 4}' y2='{err_bottom}' "
                       f"stroke='#2b2b2b'/>\n")

        label_x = group_x + group_width / 2
        svg.append(
            f"<g transform='translate({label_x},{y0 + 30}) rotate(-30)'>"
            f"<text font-size='11' text-anchor='end' font-family='DejaVu Sans, Arial, sans-serif'>{bait}</text>"
            "</g>\n"
        )

    svg.append(_svg_text(width / 2, height - 10, "Bait", size=12))
    svg.append(
        f"<g transform='translate(18,{height/2}) rotate(-90)'>"
        f"<text font-size='12' text-anchor='middle' font-family='DejaVu Sans, Arial, sans-serif'>Mean species richness</text>"
        "</g>\n"
    )

    # Legend
    legend_x = width - margin["right"] - 120
    legend_y = margin["top"] + 10
    for idx, site in enumerate(sites):
        y = legend_y + idx * 18
        svg.append(
            f"<rect x='{legend_x}' y='{y - 10}' width='12' height='12' fill='{colors.get(site, '#a6cee3')}'/>\n"
        )
        svg.append(_svg_text(legend_x + 18, y, site, size=12, anchor="start"))

    svg.append(_svg_footer())

    out_path.write_text("".join(svg), encoding="utf-8")


if __name__ == "__main__":
    report_dir = Path("Annotation_reports_coral_reef")
    out_dir = Path("results")
    fig_dir = out_dir / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    df = collect_richness(report_dir)
    df.to_csv(out_dir / "species_richness_coral_reef.csv", index=False)

    bait_summary = (
        df.groupby("bait")["species_richness"]
        .agg(["count", "mean", "std", "min", "max"])
        .reset_index()
        .sort_values("mean", ascending=False)
    )
    bait_summary.to_csv(out_dir / "species_richness_coral_reef_by_bait.csv", index=False)

    plot_richness_by_bait(df, fig_dir / "species_richness_by_bait.svg")
    plot_mean_by_bait_and_site(df, fig_dir / "species_richness_by_bait_site.svg")
