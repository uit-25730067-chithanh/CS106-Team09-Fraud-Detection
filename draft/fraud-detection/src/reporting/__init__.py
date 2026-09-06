"""Reporting helpers for building DOCX reports from Markdown source."""

from .docx_table_builder import add_spacer, add_table
from .markdown_parser import add_runs, clean_markdown_symbols, parse_markdown
from .report_builder import build_document
from .toc_generator import add_toc, collect_toc_entries

__all__ = [
    "parse_markdown",
    "clean_markdown_symbols",
    "add_runs",
    "add_table",
    "add_spacer",
    "collect_toc_entries",
    "add_toc",
    "build_document",
]
