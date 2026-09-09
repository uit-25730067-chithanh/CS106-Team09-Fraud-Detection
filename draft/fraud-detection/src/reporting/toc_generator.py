"""
Table of Contents Generator for UIT Academic Documents.
Features:
- Conforms strictly to UIT Phụ lục 2 (Mục lục dot-leader).
- Paragraphs with right-aligned tab stop at 16.0cm and dot leader (WD_TAB_LEADER.DOTS).
- Interactive internal hyperlinks (<w:hyperlink w:anchor="...">) jumping directly to section bookmarks.
- 100% Pure Black text (#000000) for all entries and page numbers.
- Two-tier typography: Level 1 bold 12pt, Level 2 regular 11.5pt with 0.6cm indent.
- Backward-compatible add_toc and collect_toc_entries.
"""

from __future__ import annotations

import re
import docx
from docx.shared import Pt, Cm, Twips, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER, WD_BREAK
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

COLOR_TEXT_MAIN = RGBColor(0, 0, 0)
COLOR_HEX_BLACK = "000000"
TOC_FIRST_PAGE_ROWS = 20
TOC_PAGE_COLUMN_TWIPS = 648
CONTENT_WIDTH_TWIPS = 9071


def add_hyperlink_run(
    paragraph,
    target_anchor: str,
    text: str,
    font_name="Times New Roman",
    font_size=12.0,
    is_bold=False,
    is_italic=False,
    color_hex="000000"
) -> None:
    """Add an internal clickable hyperlink run targeting a bookmark anchor in pure black."""
    escaped_text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    hl = parse_xml(f'<w:hyperlink {nsdecls("w")} w:anchor="{target_anchor}"/>')
    r = parse_xml(
        f'<w:r {nsdecls("w")}>'
        f'<w:rPr>'
        f'<w:rFonts w:ascii="{font_name}" w:hAnsi="{font_name}"/>'
        f'<w:sz w:val="{int(font_size * 2)}"/>'
        f'{"<w:b/>" if is_bold else ""}'
        f'{"<w:i/>" if is_italic else ""}'
        f'<w:color w:val="{color_hex}"/>'
        f'</w:rPr>'
        f'<w:t xml:space="preserve">{escaped_text}</w:t>'
        f'</w:r>'
    )
    hl.append(r)
    paragraph._p.append(hl)


def collect_toc_entries(blocks: list[dict] | list[str]) -> list[dict]:
    """
    Collect TOC entries from markdown headings or legacy parsed blocks.
    """
    entries = []
    h1_count = 0
    h2_count = 0
    h3_count = 0

    # If list of raw markdown strings
    if blocks and isinstance(blocks[0], str):
        for line in blocks:
            stripped = line.strip()
            if stripped.startswith('# '):
                t = stripped[2:].strip()
                if "TIỂU LUẬN" in t.upper() or "BÁO CÁO" in t.upper() or "BÌA" in t.upper():
                    continue
                h1_count += 1
                entries.append({
                    "text": t,
                    "level": 1,
                    "anchor": f"bm_h1_{h1_count}"
                })
            elif stripped.startswith('## '):
                t = stripped[3:].strip()
                h2_count += 1
                entries.append({
                    "text": t,
                    "level": 2,
                    "anchor": f"bm_h2_{h2_count}"
                })
            elif stripped.startswith('### '):
                t = stripped[4:].strip()
                if re.match(r'^\d+\.\d+\.\d+\.', t):
                    h3_count += 1
                    entries.append({
                        "text": t,
                        "level": 3,
                        "anchor": f"bm_h3_{h3_count}"
                    })
        return entries

    # If list of legacy dict blocks
    first_h1_skipped = False
    for b in blocks:
        kind = b.get("type")
        text = b.get("text", "").strip()
        if kind == "h1":
            if not first_h1_skipped or "BÌA" in text.upper():
                first_h1_skipped = True
                continue
            entries.append({"text": text, "level": 1})
        elif kind == "h2":
            if not re.match(r"^\d+\.\d+\.", text):
                continue
            entries.append({"text": text, "level": 2})

    return entries


def add_toc(document, entries: list[dict], pages: dict[str, int]) -> None:
    """Backward-compatible table-based add_toc."""
    chunks = [entries[:TOC_FIRST_PAGE_ROWS], entries[TOC_FIRST_PAGE_ROWS:]]
    for chunk_index, chunk in enumerate(chunks):
        if not chunk:
            continue
        if chunk_index:
            document.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        document.add_paragraph(
            "MỤC LỤC (TIẾP THEO)" if chunk_index else "MỤC LỤC",
            style="Heading 1",
        )

        table = document.add_table(rows=len(chunk), cols=2)
        from .docx_table_builder import _fix_layout
        _fix_layout(table, [CONTENT_WIDTH_TWIPS - TOC_PAGE_COLUMN_TWIPS, TOC_PAGE_COLUMN_TWIPS])
        for row_index, entry in enumerate(chunk):
            label_cell, page_cell = table.cell(row_index, 0), table.cell(row_index, 1)
            label_cell.width = Twips(CONTENT_WIDTH_TWIPS - TOC_PAGE_COLUMN_TWIPS)
            page_cell.width = Twips(TOC_PAGE_COLUMN_TWIPS)

            label = label_cell.paragraphs[0]
            label.alignment = WD_ALIGN_PARAGRAPH.LEFT
            if entry["level"] == 2:
                label.paragraph_format.left_indent = Twips(280)
            run = label.add_run(entry["text"])
            run.bold = entry["level"] == 1
            run.font.size = Pt(11)

            page = page_cell.paragraphs[0]
            page.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            number = pages.get(entry["text"])
            page_run = page.add_run(str(number) if number else "")
            page_run.bold = entry["level"] == 1
            page_run.font.size = Pt(11)


def build_toc_section(
    doc: docx.Document,
    toc_entries: list[dict],
    page_mapping: dict[str, int]
) -> None:
    """
    Build the official Table of Contents (Phụ lục 2) in Section 2.
    """
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(14)
    p_title.paragraph_format.space_after = Pt(12)
    p_title.paragraph_format.line_spacing = 1.15
    r_t = p_title.add_run("MỤC LỤC")
    r_t.font.name = "Times New Roman"
    r_t.font.size = Pt(14)
    r_t.bold = True
    r_t.font.color.rgb = COLOR_TEXT_MAIN

    for entry in toc_entries:
        title = entry["text"].strip()
        level = entry["level"]
        anchor = entry.get("anchor")
        page_num = page_mapping.get(title, "")

        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before = Pt(3 if level == 1 else 1)
        p_toc.paragraph_format.space_after = Pt(2)
        p_toc.paragraph_format.line_spacing = 1.25

        if level == 2:
            p_toc.paragraph_format.left_indent = Cm(0.6)
        elif level == 3:
            p_toc.paragraph_format.left_indent = Cm(1.2)

        tab_stops = p_toc.paragraph_format.tab_stops
        tab_stops.add_tab_stop(Cm(16.0), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

        is_bold = (level == 1)
        font_sz = 12.0 if level == 1 else 11.5

        if anchor:
            add_hyperlink_run(
                p_toc, anchor, title,
                font_name="Times New Roman", font_size=font_sz,
                is_bold=is_bold, color_hex=COLOR_HEX_BLACK
            )
            add_hyperlink_run(
                p_toc, anchor, f"\t{page_num}",
                font_name="Times New Roman", font_size=font_sz,
                is_bold=is_bold, color_hex=COLOR_HEX_BLACK
            )
        else:
            r_entry = p_toc.add_run(title)
            r_entry.font.name = "Times New Roman"
            r_entry.font.size = Pt(font_sz)
            r_entry.bold = is_bold
            r_entry.font.color.rgb = COLOR_TEXT_MAIN

            r_p = p_toc.add_run(f"\t{page_num}")
            r_p.font.name = "Times New Roman"
            r_p.font.size = Pt(font_sz)
            r_p.bold = is_bold
            r_p.font.color.rgb = COLOR_TEXT_MAIN
