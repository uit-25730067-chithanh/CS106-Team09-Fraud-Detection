"""Table of contents collection and page-number layout for DOCX report."""

from __future__ import annotations

import re

from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.shared import Pt, Twips

from .docx_table_builder import CONTENT_WIDTH_TWIPS, _fix_layout
from .markdown_parser import clean_markdown_symbols

TOC_FIRST_PAGE_ROWS = 20
TOC_PAGE_COLUMN_TWIPS = 648


def collect_toc_entries(blocks: list[dict]) -> list[dict]:
    """Mục lục gồm tiêu đề chương và các mục đánh số dạng x.y.

    Bỏ qua tiêu đề bìa (block đầu tiên), heading cấp 3 và các mục không đánh số
    trong phần tài liệu tham khảo.
    """
    entries = []
    for index, block in enumerate(blocks):
        if index == 0 or block["type"] not in ("h1", "h2"):
            continue
        if block["type"] == "h2" and not re.match(r"^\d+\.\d+\.", block["text"]):
            continue
        entries.append({
            "text": block["text"],
            "level": 1 if block["type"] == "h1" else 2,
        })
    return entries


def add_toc(document, entries: list[dict], pages: dict[str, int]) -> None:
    """Chèn bảng mục lục chia làm 2 phần (trang 1 và trang tiếp theo)."""
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
        _fix_layout(
            table,
            [CONTENT_WIDTH_TWIPS - TOC_PAGE_COLUMN_TWIPS, TOC_PAGE_COLUMN_TWIPS],
        )
        for row_index, entry in enumerate(chunk):
            label_cell, page_cell = table.cell(row_index, 0), table.cell(row_index, 1)
            label_cell.width = Twips(CONTENT_WIDTH_TWIPS - TOC_PAGE_COLUMN_TWIPS)
            page_cell.width = Twips(TOC_PAGE_COLUMN_TWIPS)

            label = label_cell.paragraphs[0]
            label.alignment = WD_ALIGN_PARAGRAPH.LEFT
            if entry["level"] == 2:
                label.paragraph_format.left_indent = Twips(280)
            run = label.add_run(clean_markdown_symbols(entry["text"]))
            run.bold = entry["level"] == 1
            run.font.size = Pt(11)

            page = page_cell.paragraphs[0]
            page.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            number = pages.get(entry["text"])
            page_run = page.add_run(str(number) if number else "")
            page_run.bold = entry["level"] == 1
            page_run.font.size = Pt(11)
