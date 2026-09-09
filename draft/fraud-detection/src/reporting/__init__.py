"""Reporting helpers for building high-fidelity UIT Academic Reports."""

from .docx_table_builder import add_styled_table
from .pdf_exporter import export_docx_to_pdf
from .report_builder import build_document
from .toc_generator import build_toc_section, collect_toc_entries

__all__ = [
    "build_document",
    "export_docx_to_pdf",
    "collect_toc_entries",
    "build_toc_section",
    "add_styled_table",
]
