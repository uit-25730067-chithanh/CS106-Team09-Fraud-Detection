"""Word table builder with fixed column widths, alignment, and repeating headers."""

from __future__ import annotations

import re

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.shared import Pt, Twips

from .markdown_parser import add_runs, clean_markdown_symbols

# Bề rộng vùng in: khổ A4 11906 twips trừ lề trái 1701 và lề phải 1134.
CONTENT_WIDTH_TWIPS = 9071
NARROW_HEADERS = frozenset({"#", "STT", "Hạng"})
NARROW_WIDTH_TWIPS = 700
TABLE_FONT_PT = 9.5


def _column_widths(header: list[str], rows: list[list[str]]) -> list[int]:
    """Chia bề rộng theo độ dài nội dung, cột số thứ tự giữ hẹp cố định."""
    weights = []
    for column in range(len(header)):
        cells = [header[column]] + [row[column] for row in rows if column < len(row)]
        weights.append(max(len(clean_markdown_symbols(cell)) for cell in cells))

    narrow = header[0] in NARROW_HEADERS
    available = CONTENT_WIDTH_TWIPS - (NARROW_WIDTH_TWIPS if narrow else 0)
    scalable = weights[1:] if narrow else weights
    total = sum(scalable) or 1
    widths = [round(available * weight / total) for weight in scalable]
    return ([NARROW_WIDTH_TWIPS] + widths) if narrow else widths


def _is_numeric_column(rows: list[list[str]], column: int) -> bool:
    cells = [row[column] for row in rows if column < len(row)]
    if not cells:
        return False
    numeric = sum(
        bool(re.fullmatch(r"[\d.,%\s+–—-]+", clean_markdown_symbols(cell).strip("*")))
        for cell in cells
    )
    return numeric >= max(1, round(0.6 * len(cells)))


def add_spacer(document):
    """Đệm mỏng sau bảng: đủ tách khỏi đoạn kế tiếp, không tạo dòng trống thừa."""
    spacer = document.add_paragraph()
    spacer.paragraph_format.space_before = Pt(0)
    spacer.paragraph_format.space_after = Pt(0)
    spacer.paragraph_format.line_spacing = 1.0
    spacer.add_run().font.size = Pt(6)
    return spacer


def _repeat_header(table) -> None:
    """Lặp lại hàng tiêu đề khi bảng bị tách sang trang sau."""
    header_pr = table.rows[0]._tr.get_or_add_trPr()
    header_pr.append(header_pr.makeelement(qn("w:tblHeader"), {qn("w:val"): "true"}))
    for row in table.rows:
        row_pr = row._tr.get_or_add_trPr()
        row_pr.append(row_pr.makeelement(qn("w:cantSplit"), {}))


def _fix_layout(table, widths: list[int]) -> None:
    """Khoá bề rộng cột."""
    table.autofit = False
    for column, width in zip(table.columns, widths):
        column.width = Twips(width)


def add_table(document, header: list[str], rows: list[list[str]]):
    """Thêm bảng vào tài liệu Word với style Table Grid và căn chỉnh tự động."""
    table = document.add_table(rows=1 + len(rows), cols=len(header))
    # Dùng style name "Table Grid" thay vì style_id "TableGrid" để tránh cảnh báo deprecation
    table.style = "Table Grid"

    widths = _column_widths(header, rows)
    _fix_layout(table, widths)
    _repeat_header(table)

    narrow_first = header[0] in NARROW_HEADERS
    alignments = [
        WD_ALIGN_PARAGRAPH.CENTER if narrow_first else WD_ALIGN_PARAGRAPH.LEFT
    ] + [
        WD_ALIGN_PARAGRAPH.CENTER if _is_numeric_column(rows, column) else WD_ALIGN_PARAGRAPH.LEFT
        for column in range(1, len(header))
    ]

    for column, title in enumerate(header):
        cell = table.cell(0, column)
        cell.width = Twips(widths[column])
        paragraph = cell.paragraphs[0]
        paragraph.alignment = alignments[column]
        add_runs(paragraph, title, bold=True, size_pt=TABLE_FONT_PT)

    for row_index, row in enumerate(rows, start=1):
        for column in range(len(header)):
            cell = table.cell(row_index, column)
            cell.width = Twips(widths[column])
            paragraph = cell.paragraphs[0]
            paragraph.alignment = alignments[column]
            add_runs(
                paragraph,
                row[column] if column < len(row) else "",
                size_pt=TABLE_FONT_PT,
            )

    return table
