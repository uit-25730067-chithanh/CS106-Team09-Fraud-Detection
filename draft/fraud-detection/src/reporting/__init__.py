"""Reporting helpers for building high-fidelity UIT Academic Reports."""

from .docx_table_builder import add_styled_table
from .hyperlink_helpers import (
    COLOR_HEX_BLACK,
    COLOR_TEXT_MAIN,
    add_bookmark,
    add_external_hyperlink,
    add_internal_hyperlink,
    add_page_number_field,
)
from .pdf_exporter import export_docx_to_pdf
from .report_builder import (
    build_document,
    build_document_from_blocks,
    build_document_from_markdown,
)
from .toc_generator import build_toc_section, collect_toc_entries

__all__ = [
    # Modern API (C5 — clearly-named functions)
    "build_document_from_markdown",
    "build_document_from_blocks",
    # Legacy alias
    "build_document",
    # Submodule re-exports
    "export_docx_to_pdf",
    "collect_toc_entries",
    "build_toc_section",
    "add_styled_table",
    # Shared helpers
    "add_internal_hyperlink",
    "add_external_hyperlink",
    "add_bookmark",
    "add_page_number_field",
    "COLOR_TEXT_MAIN",
    "COLOR_HEX_BLACK",
]
