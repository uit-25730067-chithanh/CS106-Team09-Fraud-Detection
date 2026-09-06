"""DOCX report document assembler using template, parsed blocks, and TOC pages."""

from __future__ import annotations

import os
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.shared import Twips

from .docx_table_builder import add_spacer, add_table
from .markdown_parser import add_runs, clean_markdown_symbols
from .toc_generator import add_toc, collect_toc_entries

FIGURE_WIDTH_TWIPS = 8600
REFERENCE_HANGING_TWIPS = 567


def build_document(
    blocks: list[dict],
    pages: dict[str, int],
    template_path: str,
    reports_dir: str,
) -> Document:
    """Dựng file Word hoàn chỉnh từ các block phân tích và khuôn template."""
    document = Document(template_path)
    entries = collect_toc_entries(blocks)
    cover_done = False
    cover_h1_done = False

    for index, block in enumerate(blocks):
        kind = block["type"]

        if kind == "pagebreak":
            document.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            if not cover_done:
                add_toc(document, entries, pages)
                document.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
                cover_done = True
            continue

        if kind == "h1":
            if not cover_h1_done:
                paragraph = document.add_paragraph(
                    clean_markdown_symbols(block["text"]), style="CoverTitle"
                )
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cover_h1_done = True
            else:
                document.add_paragraph(
                    clean_markdown_symbols(block["text"]), style="Heading 1"
                )
            continue

        if kind in ("h2", "h3"):
            document.add_paragraph(
                clean_markdown_symbols(block["text"]),
                style="Heading 2" if kind == "h2" else "Heading 3",
            )
            continue

        if kind == "note":
            paragraph = document.add_paragraph(style="ReportNote")
            add_runs(paragraph, block["text"])
            continue

        if kind == "caption":
            paragraph = document.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.keep_with_next = True
            add_runs(paragraph, block["text"], bold=True)
            continue

        if kind == "table":
            add_table(document, block["header"], block["rows"])
            add_spacer(document)
            continue

        if kind == "image":
            path = os.path.join(reports_dir, block["path"])
            picture = document.add_paragraph()
            picture.alignment = WD_ALIGN_PARAGRAPH.CENTER
            picture.add_run().add_picture(path, width=Twips(FIGURE_WIDTH_TWIPS))
            caption = document.add_paragraph()
            caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
            caption.add_run(clean_markdown_symbols(block["caption"])).italic = True
            continue

        if kind in ("bullet", "number"):
            paragraph = document.add_paragraph(
                style="List Bullet" if kind == "bullet" else "List Number"
            )
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            add_runs(paragraph, block["text"])
            continue

        style = "CoverMeta" if not cover_done else "ReportBody"
        paragraph = document.add_paragraph(style=style)
        if not cover_done:
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif re.match(r"^\[\d+\]\s", block["text"]):
            paragraph.paragraph_format.left_indent = Twips(REFERENCE_HANGING_TWIPS)
            paragraph.paragraph_format.first_line_indent = Twips(-REFERENCE_HANGING_TWIPS)
            # Căn đều làm giãn ký tự ở dòng chứa DOI dài không ngắt được.
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        add_runs(paragraph, block["text"])

    return document
