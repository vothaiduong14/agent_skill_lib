#!/usr/bin/env python3
"""
Extract a PowerPoint deck into analysis-friendly Markdown.

Dependencies:
    pip install python-pptx

Optional rendering:
    LibreOffice/soffice and pdftoppm (Poppler) available on PATH.

Usage:
    python extract_pptx.py deck.pptx --out deck_extracted.md
    python extract_pptx.py deck.pptx --out deck_extracted.md --render
"""

from __future__ import annotations
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable

try:
    from pptx import Presentation
    from pptx.enum.shapes import MSO_SHAPE_TYPE
except ImportError:
    print(
        "ERROR: python-pptx is required. Install it with: pip install python-pptx",
        file=sys.stderr,
    )
    sys.exit(2)


def clean(text: str) -> str:
    return " ".join((text or "").replace("\x0b", " ").split())


def shape_bounds(shape) -> str:
    try:
        return f"x={shape.left}, y={shape.top}, w={shape.width}, h={shape.height}"
    except Exception:
        return ""


def extract_text_frame(shape) -> list[str]:
    items = []
    if not getattr(shape, "has_text_frame", False):
        return items
    for p in shape.text_frame.paragraphs:
        txt = clean(p.text)
        if not txt:
            continue
        level = getattr(p, "level", 0)
        prefix = "  " * level + "- "
        items.append(prefix + txt)
    return items


def extract_table(shape) -> list[str]:
    if not getattr(shape, "has_table", False):
        return []
    rows = []
    for row in shape.table.rows:
        cells = [clean(c.text) for c in row.cells]
        rows.append("| " + " | ".join(cells) + " |")
    if rows:
        cols = len(shape.table.columns)
        rows.insert(1, "| " + " | ".join(["---"] * cols) + " |")
    return rows


def extract_chart(shape) -> list[str]:
    if not getattr(shape, "has_chart", False):
        return []
    out = []
    chart = shape.chart
    try:
        title = clean(chart.chart_title.text_frame.text) if chart.has_title else ""
    except Exception:
        title = ""
    out.append(f"- Chart type: {getattr(chart, 'chart_type', 'unknown')}")
    if title:
        out.append(f"- Chart title: {title}")

    try:
        for idx, series in enumerate(chart.series, start=1):
            name = clean(str(series.name))
            vals = []
            try:
                vals = list(series.values)
            except Exception:
                pass
            out.append(f"- Series {idx}: {name or '(unnamed)'}")
            if vals:
                out.append(f"  - Values: {vals}")
    except Exception as exc:
        out.append(f"- Chart details unavailable: {exc}")
    return out


def extract_notes(slide) -> list[str]:
    try:
        notes_slide = slide.notes_slide
    except Exception:
        return []
    items = []
    try:
        for shape in notes_slide.shapes:
            if getattr(shape, "has_text_frame", False):
                txt = clean(shape.text)
                # Exclude placeholders that only contain slide number/date artifacts.
                if txt and not txt.isdigit():
                    items.append(txt)
    except Exception:
        pass
    # de-duplicate while preserving order
    seen = set()
    return [x for x in items if not (x in seen or seen.add(x))]


def render_slides(pptx_path: Path, render_dir: Path) -> list[Path]:
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    pdftoppm = shutil.which("pdftoppm")
    if not soffice or not pdftoppm:
        print(
            "WARNING: --render requested but LibreOffice/soffice and/or pdftoppm "
            "were not found. Continuing without slide images.",
            file=sys.stderr,
        )
        return []

    render_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        cmd = [
            soffice, "--headless", "--convert-to", "pdf",
            "--outdir", str(tmp), str(pptx_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"WARNING: LibreOffice rendering failed: {result.stderr}", file=sys.stderr)
            return []

        pdfs = list(tmp.glob("*.pdf"))
        if not pdfs:
            print("WARNING: No PDF produced during rendering.", file=sys.stderr)
            return []

        prefix = render_dir / "slide"
        result = subprocess.run(
            [pdftoppm, "-png", "-r", "144", str(pdfs[0]), str(prefix)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"WARNING: pdftoppm failed: {result.stderr}", file=sys.stderr)
            return []

    return sorted(render_dir.glob("slide-*.png"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pptx", type=Path)
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--render", action="store_true")
    args = ap.parse_args()

    if not args.pptx.exists():
        print(f"ERROR: file not found: {args.pptx}", file=sys.stderr)
        return 2

    out = args.out or args.pptx.with_name(args.pptx.stem + "_extracted.md")
    prs = Presentation(str(args.pptx))

    images = []
    render_dir = out.parent / (args.pptx.stem + "_slides")
    if args.render:
        images = render_slides(args.pptx, render_dir)

    lines = [
        f"# PowerPoint extraction — {args.pptx.name}",
        "",
        f"- Slides: {len(prs.slides)}",
        f"- Source: `{args.pptx}`",
        "",
        "> Extraction preserves text/tables/chart metadata where available. "
        "Visual layout still needs image inspection for diagrams and design-heavy slides.",
        "",
    ]

    for idx, slide in enumerate(prs.slides, start=1):
        title = ""
        try:
            if slide.shapes.title:
                title = clean(slide.shapes.title.text)
        except Exception:
            pass

        lines += [f"## Slide {idx}" + (f" — {title}" if title else ""), ""]

        if idx <= len(images):
            rel = os.path.relpath(images[idx-1], out.parent)
            lines += [f"**Rendered image:** `{rel}`", ""]

        for sidx, shape in enumerate(slide.shapes, start=1):
            sname = clean(getattr(shape, "name", "")) or f"Shape {sidx}"
            stype = getattr(shape, "shape_type", "unknown")
            bounds = shape_bounds(shape)

            text_items = extract_text_frame(shape)
            table_items = extract_table(shape)
            chart_items = extract_chart(shape)

            if text_items:
                lines += [f"### Text — {sname}", f"_Position: {bounds}_", ""]
                lines += text_items + [""]

            if table_items:
                lines += [f"### Table — {sname}", f"_Position: {bounds}_", ""]
                lines += table_items + [""]

            if chart_items:
                lines += [f"### Chart — {sname}", f"_Position: {bounds}_", ""]
                lines += chart_items + [""]

            try:
                if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                    lines += [
                        f"### Image — {sname}",
                        f"_Position: {bounds}_",
                        "- Picture present; inspect rendered slide for meaning.",
                        "",
                    ]
            except Exception:
                pass

        notes = extract_notes(slide)
        if notes:
            lines += ["### Existing speaker notes", ""]
            for note in notes:
                lines.append(f"- {note}")
            lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote: {out}")
    if images:
        print(f"Rendered {len(images)} slide image(s) to: {render_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
