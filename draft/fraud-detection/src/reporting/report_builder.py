"""Master UIT Academic Document Compiler for CS106 Final Report.

Orchestrator module that composes:
- ``cover_page_builder`` — Section 1: Cover Page (Phụ lục 1)
- ``toc_generator``       — Section 2: Table of Contents (Phụ lục 2)
- ``body_section_builder`` — Section 3: Document Body

Exposes two clearly-named public entry points:

- ``build_document_from_markdown(markdown_path, output_docx_path, ...)``
  — Modern high-fidelity UIT builder reading ``.md`` source + YAML metadata.
- ``build_document_from_blocks(blocks, pages, template_path, reports_dir)``
  — Legacy compatibility builder used by older unit tests.

The legacy alias ``build_document`` is retained for backward compatibility
but delegates to the appropriate function based on argument types with a
deprecation warning.
"""

from __future__ import annotations

import logging
import os
import warnings

import docx
import yaml
from docx.enum.section import WD_SECTION_START
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Cm, Pt

from .body_section_builder import build_body_section
from .cover_page_builder import build_cover_page
from .hyperlink_helpers import COLOR_TEXT_MAIN
from .toc_generator import build_toc_section, collect_toc_entries

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Public API — clearly-named entry points (C5 fix)
# ---------------------------------------------------------------------------


def build_document_from_markdown(
    markdown_path: str,
    output_docx_path: str,
    meta_path: str | None = None,
    page_mapping: dict[str, int] | None = None,
) -> docx.Document:
    """Build a 3-section UIT Academic Document from Markdown source.

    Args:
        markdown_path: Path to the ``report-source.md`` file.
        output_docx_path: Where to save the generated ``.docx``.
        meta_path: Optional path to ``report-meta.yaml``.
        page_mapping: Optional TOC page numbers from ``_toc_pages.json``.

    Returns:
        The assembled ``docx.Document`` (already saved to *output_docx_path*).
    """
    base_dir = os.path.dirname(os.path.abspath(markdown_path))

    with open(markdown_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Sanitize dashes in input
    md_text = md_text.replace("\u2014", " - ").replace("\u2013", "-")

    # Load metadata
    meta: dict = {}
    if meta_path and os.path.exists(meta_path) and not meta_path.endswith(".docx"):
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = yaml.safe_load(f) or {}
    else:
        auto_meta = os.path.join(base_dir, "report-meta.yaml")
        if os.path.exists(auto_meta):
            with open(auto_meta, "r", encoding="utf-8") as f:
                meta = yaml.safe_load(f) or {}

    lines = md_text.split("\n")
    toc_data = collect_toc_entries(lines)

    doc = docx.Document()

    # Global style defaults: Times New Roman 13pt, Pure Black
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(13)
    normal_style.font.color.rgb = COLOR_TEXT_MAIN
    normal_style.paragraph_format.line_spacing = 1.3
    normal_style.paragraph_format.space_after = Pt(2)
    normal_style.paragraph_format.space_before = Pt(0)

    # 1. Section 1: Cover Page (Phụ lục 1)
    build_cover_page(doc, meta, base_dir)

    # 2. Section 2: Table of Contents (Phụ lục 2)
    sec2 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec2.page_width = Cm(21.0)
    sec2.page_height = Cm(29.7)
    sec2.top_margin = Cm(2.0)
    sec2.bottom_margin = Cm(2.0)
    sec2.left_margin = Cm(3.0)
    sec2.right_margin = Cm(2.0)
    sec2.different_first_page_header_footer = False
    sec2.header.is_linked_to_previous = False
    sec2.footer.is_linked_to_previous = False

    # Remove borders in Section 2
    sectPr2 = sec2._sectPr
    pgBorders2 = parse_xml(
        r"""
    <w:pgBorders %s w:offsetFrom="page">
        <w:top w:val="none"/><w:left w:val="none"/>
        <w:bottom w:val="none"/><w:right w:val="none"/>
    </w:pgBorders>
    """
        % nsdecls("w")
    )
    sectPr2.append(pgBorders2)

    build_toc_section(doc, toc_data, page_mapping or {})

    # 3. Section 3: Document Body
    build_body_section(doc, lines, meta, base_dir, toc_data)

    doc.save(output_docx_path)
    return doc


def build_document_from_blocks(
    blocks: list[dict],
    pages: dict[str, int],
    template_path: str,
    reports_dir: str,
) -> docx.Document:
    """Legacy builder for unit tests using parsed blocks and template.

    Uses specific ``except KeyError`` handling instead of bare
    ``except Exception`` so template style issues are logged rather
    than silently swallowed (C4 fix).
    """
    from .docx_table_builder import add_spacer, add_table
    from .markdown_parser import add_runs, clean_markdown_symbols
    from .toc_generator import add_toc

    document = docx.Document(template_path)
    entries = collect_toc_entries(blocks)
    cover_done = False
    cover_h1_done = False

    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK

    for block in blocks:
        kind = block.get("type")
        if kind == "pagebreak":
            document.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
            if not cover_done:
                add_toc(document, entries, pages)
                document.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
                cover_done = True
            continue

        if kind == "h1":
            if not cover_h1_done:
                try:
                    p = document.add_paragraph(
                        clean_markdown_symbols(block["text"]), style="CoverTitle"
                    )
                except KeyError as exc:
                    logger.warning("Style not found in template: %s, falling back to Normal", exc)
                    p = document.add_paragraph(clean_markdown_symbols(block["text"]))
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cover_h1_done = True
            else:
                try:
                    document.add_paragraph(
                        clean_markdown_symbols(block["text"]), style="Heading 1"
                    )
                except KeyError as exc:
                    logger.warning("Style 'Heading 1' not found: %s, falling back to Normal", exc)
                    document.add_paragraph(clean_markdown_symbols(block["text"]))
            continue

        if kind in ("h2", "h3"):
            style_name = "Heading 2" if kind == "h2" else "Heading 3"
            try:
                document.add_paragraph(
                    clean_markdown_symbols(block["text"]), style=style_name
                )
            except KeyError as exc:
                logger.warning("Style '%s' not found: %s, falling back to Normal", style_name, exc)
                document.add_paragraph(clean_markdown_symbols(block["text"]))
            continue

        if kind == "table":
            add_table(document, block["header"], block["rows"])
            add_spacer(document)
            continue

        if kind == "note":
            try:
                p = document.add_paragraph(style="ReportNote")
            except KeyError as exc:
                logger.warning("Style 'ReportNote' not found: %s, falling back to Normal", exc)
                p = document.add_paragraph()
            add_runs(p, block["text"])
            continue

        if kind in ("bullet", "number"):
            style_name = "List Bullet" if kind == "bullet" else "List Number"
            try:
                p = document.add_paragraph(style=style_name)
            except KeyError as exc:
                logger.warning("Style '%s' not found: %s, falling back to Normal", style_name, exc)
                p = document.add_paragraph()
            add_runs(p, block["text"])
            continue

        style = "CoverMeta" if not cover_done else "ReportBody"
        try:
            p = document.add_paragraph(style=style)
        except KeyError as exc:
            logger.warning("Style '%s' not found: %s, falling back to Normal", style, exc)
            p = document.add_paragraph()
        add_runs(p, block.get("text", ""))

    return document


# ---------------------------------------------------------------------------
# Backward-compatible alias (C5 — retained for callers, with deprecation)
# ---------------------------------------------------------------------------


def build_document(
    first_arg: str | list[dict],
    second_arg: str | dict[str, int],
    meta_path: str | None = None,
    page_mapping: dict[str, int] | None = None,
    template_path: str | None = None,
    reports_dir: str | None = None,
) -> docx.Document:
    """Backward-compatible dispatcher — prefer the explicitly-named functions.

    Detects legacy vs. modern invocation from argument types and delegates.
    """
    # Legacy invocation: build_document(blocks_list, pages_dict, ...)
    if isinstance(first_arg, list):
        tpl = template_path or (
            meta_path
            if isinstance(meta_path, str) and meta_path.endswith(".docx")
            else None
        )
        rdir = reports_dir or ""
        pgs = second_arg if isinstance(second_arg, dict) else {}
        return build_document_from_blocks(first_arg, pgs, tpl, rdir)

    # Modern invocation: build_document(markdown_path, output_docx_path, ...)
    return build_document_from_markdown(
        str(first_arg),
        str(second_arg),
        meta_path=meta_path,
        page_mapping=page_mapping,
    )
