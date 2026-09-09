"""
Smart Table Builder for UIT Academic Documents.
Features:
- Fixed printable width: 16.0 cm (matching A4 21.0cm - 3.0cm left - 2.0cm right)
- Pure black text (#000000) for all cells
- Clean neutral header shading (#F2F2F2) with thin borders
- Row protection: <w:cantSplit/> prevents awkward page breaks mid-row
- Header repetition: <w:tblHeader/> on row 0 repeats header across page breaks
- Smart cell alignment: numbers/ranges right-aligned, short codes/percentages centered, text left-aligned
- Backward compatibility: add_table, add_spacer, _is_numeric_column, _fix_layout
"""

from __future__ import annotations

import re
from typing import Callable

import docx
from docx.shared import Pt, Cm, Twips, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

COLOR_TEXT_MAIN = RGBColor(0, 0, 0)
COLOR_BG_HEADER = "F2F2F2"
COLOR_BG_ZEBRA = "FAFAFA"
COLOR_BORDER = "CCCCCC"

CONTENT_WIDTH_TWIPS = 9071


def is_numeric_or_range(val: str) -> bool:
    """Check if cell content represents numbers, ranges, percentages, or metrics."""
    cleaned = val.strip().replace('**', '').replace('*', '').replace(',', '.').replace('%', '').strip()
    if re.match(r'^-?\d+(\.\d+)?$', cleaned):
        return True
    if re.match(r'^-?\d+(\.\d+)?\s*[-–—]\s*-?\d+(\.\d+)?$', cleaned):
        return True
    if re.match(r'^\d{1,3}(\.\d{3})*(,\d+)?$', val.strip()):
        return True
    return False


def _is_numeric_column(rows: list[list[str]], col_index: int) -> bool:
    """Backward-compatible helper checking if a column consists mostly of numeric/range cells."""
    if not rows:
        return False
    matched = sum(1 for row in rows if col_index < len(row) and is_numeric_or_range(row[col_index]))
    return matched / len(rows) >= 0.6


def _fix_layout(table, col_widths: list[int]) -> None:
    """Backward-compatible column width setter."""
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            if idx < len(row.cells):
                row.cells[idx].width = Twips(width)


def add_spacer(doc: docx.Document):
    """Backward-compatible spacing paragraph."""
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.0
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    return p


def add_table(doc: docx.Document, header: list[str], rows: list[list[str]]):
    """Backward-compatible table creator returning Table Grid styled table."""
    table = doc.add_table(rows=len(rows) + 1, cols=len(header))
    try:
        table.style = "Table Grid"
    except Exception:
        pass
    for c_idx, h in enumerate(header):
        table.cell(0, c_idx).text = h
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            table.cell(r_idx + 1, c_idx).text = val
    return table


def set_cell_margins_and_border(cell, top_pt=4, bottom_pt=4, left_pt=6, right_pt=6):
    """Set inner cell padding and subtle border."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{int(top_pt * 20)}" w:type="dxa"/>'
        f'<w:bottom w:w="{int(bottom_pt * 20)}" w:type="dxa"/>'
        f'<w:left w:w="{int(left_pt * 20)}" w:type="dxa"/>'
        f'<w:right w:w="{int(right_pt * 20)}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def get_table_column_widths(
    headers: list[str],
    body_rows: list[list[str]],
    total_width_cm: float = 16.0
) -> list[float]:
    """
    Calculate smart, content-aware column widths conforming to UIT 16.0cm printable width.
    Prevents awkward word breaks on long feature names and compacts short index columns.
    """
    num_cols = len(headers)
    if num_cols <= 0:
        return []

    norm_headers = [re.sub(r'[*`_]', '', h).strip().lower() for h in headers]

    # 1. Exact preset matches for project academic tables
    # Table 4: Feature cuối & Nguồn/xử lý (Ảnh gửi kèm)
    if norm_headers == ["#", "feature cuối", "nguồn/xử lý"]:
        return [1.0, 6.0, 9.0]

    # Table 1: Thuộc tính PaySim gốc
    if norm_headers == ["thuộc tính", "kiểu/nhóm", "ý nghĩa"]:
        return [3.2, 3.0, 9.8]

    # Table 2: Loại giao dịch PaySim
    if norm_headers == ["loại giao dịch", "normal", "fraud", "tổng"]:
        return [4.0, 4.0, 3.5, 4.5]

    # Table 3: Tập dữ liệu & Fraud ratio
    if norm_headers == ["tập dữ liệu", "normal", "fraud", "tổng", "fraud ratio"]:
        return [3.8, 3.0, 2.8, 3.4, 3.0]

    # Table 5: So sánh hiệu năng mô hình (Bảng 5.2 / 5.1)
    if norm_headers == ["mô hình", "precision", "recall", "f1-score", "roc-auc", "average precision"]:
        return [5.0, 2.2, 2.2, 2.2, 2.2, 2.2]

    # Table 6: Feature Importance (Bảng 5.3 / 5.2)
    if norm_headers == ["hạng", "random forest + smotenc", "mức đóng góp", "xgboost + smotenc", "mức đóng góp"]:
        return [1.2, 4.5, 2.9, 4.5, 2.9]

    # Table 7: FP trên test & Prevalence Projection (Bảng 6.1)
    if len(norm_headers) == 6 and norm_headers[0] == "mô hình" and any("fp trên test" in nh for nh in norm_headers):
        return [4.0, 1.6, 2.3, 2.4, 2.7, 3.0]

    # Table 8: Mức độ hoàn thành các mục tiêu cụ thể (Bảng 7.1)
    if norm_headers == ["#", "mục tiêu", "kết quả", "vị trí"]:
        return [1.0, 8.5, 3.0, 3.5]

    # 2. Dynamic heuristic fallback for any other table
    col_max_lens = []
    for c in range(num_cols):
        h_len = len(headers[c].strip())
        b_len = max((len(r[c].strip()) for r in body_rows if c < len(r)), default=0)
        col_max_lens.append(max(h_len, b_len, 3))

    assigned_widths = [0.0] * num_cols
    remaining_width = total_width_cm
    remaining_cols = list(range(num_cols))

    if norm_headers[0] in ["#", "stt", "hạng", "id", "bước", "no."]:
        assigned_widths[0] = 1.0 if col_max_lens[0] <= 4 else 1.2
        remaining_width -= assigned_widths[0]
        remaining_cols.remove(0)

    total_rem_weight = sum(col_max_lens[c] for c in remaining_cols)
    if total_rem_weight <= 0:
        uniform = remaining_width / len(remaining_cols)
        for c in remaining_cols:
            assigned_widths[c] = uniform
    else:
        for c in remaining_cols:
            assigned_widths[c] = round(remaining_width * (col_max_lens[c] / total_rem_weight), 2)

        diff = round(total_width_cm - sum(assigned_widths), 2)
        assigned_widths[remaining_cols[-1]] = round(assigned_widths[remaining_cols[-1]] + diff, 2)

    return assigned_widths


def add_styled_table(
    doc: docx.Document,
    headers: list[str],
    body_rows: list[list[str]],
    caption: str | None = None,
    parse_inline_func: Callable | None = None
) -> docx.table.Table:
    """
    Construct a professional, strictly-formatted academic table conforming to UIT standards.
    Features:
    - Smart content-aware column widths preventing line wraps on identifiers
    - Zero page-split protection: rows keep_with_next dính liền với nhau và dính với caption ở dưới
    - Table caption nằm DƯỚI bảng, in nghiêng, căn giữa, chữ đen 10.5pt
    - Row cantSplit prevents page break mid-row
    - Clean neutral shading and subtle borders in 100% pure black text
    """
    num_cols = len(headers)
    num_rows = len(body_rows) + 1

    table = doc.add_table(rows=num_rows, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Smart column widths allocation
    col_widths_cm = get_table_column_widths(headers, body_rows, total_width_cm=16.0)

    # Detect column alignment heuristics
    col_alignments = []
    for c_idx in range(num_cols):
        numeric_count = 0
        total_cells = len(body_rows)
        for r in body_rows:
            if c_idx < len(r) and is_numeric_or_range(r[c_idx]):
                numeric_count += 1
        if total_cells > 0 and (numeric_count / total_cells) >= 0.6:
            col_alignments.append(WD_ALIGN_PARAGRAPH.RIGHT)
        elif headers[c_idx].strip().lower() in ["stt", "mã", "id", "#", "phase", "bước", "nhãn", "lớp"]:
            col_alignments.append(WD_ALIGN_PARAGRAPH.CENTER)
        else:
            col_alignments.append(WD_ALIGN_PARAGRAPH.LEFT)

    # Style Table Header Row (Row 0)
    hdr_row = table.rows[0]
    trPr0 = hdr_row._tr.get_or_add_trPr()
    trPr0.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    trPr0.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    for c_idx, h_text in enumerate(headers):
        cell = hdr_row.cells[c_idx]
        cell.width = Cm(col_widths_cm[c_idx])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_margins_and_border(cell, top_pt=5, bottom_pt=5, left_pt=6, right_pt=6)

        # Header Shading (clean light gray #F2F2F2, pure black text)
        tcPr = cell._tc.get_or_add_tcPr()
        tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{COLOR_BG_HEADER}"/>'))

        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        # Header row luôn dính liền với body rows (Zero page-split)
        p.paragraph_format.keep_with_next = True

        if parse_inline_func:
            parse_inline_func(p, h_text, base_font_size=10.5, is_bold=True, base_color=COLOR_TEXT_MAIN)
        else:
            r = p.add_run(h_text.strip())
            r.font.name = "Times New Roman"
            r.font.size = Pt(10.5)
            r.bold = True
            r.font.color.rgb = COLOR_TEXT_MAIN

    # Style Body Rows
    has_bottom_caption = bool(caption and caption.strip())
    for r_idx, row_data in enumerate(body_rows):
        b_row = table.rows[r_idx + 1]
        trPr = b_row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        is_zebra = (r_idx % 2 == 1)
        shd_hex = COLOR_BG_ZEBRA if is_zebra else "FFFFFF"
        is_not_last_row = (r_idx < len(body_rows) - 1)
        # Nếu có caption dưới bảng: hàng cuối cùng CŨNG dính liền với caption
        should_keep_row = is_not_last_row or has_bottom_caption

        for c_idx in range(num_cols):
            cell = b_row.cells[c_idx]
            cell.width = Cm(col_widths_cm[c_idx])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            set_cell_margins_and_border(cell, top_pt=4, bottom_pt=4, left_pt=6, right_pt=6)

            tcPr = cell._tc.get_or_add_tcPr()
            if shd_hex != "FFFFFF":
                tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{shd_hex}"/>'))

            c_text = row_data[c_idx] if c_idx < len(row_data) else ""
            p = cell.paragraphs[0]
            p.alignment = col_alignments[c_idx]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15

            if should_keep_row:
                p.paragraph_format.keep_with_next = True

            if parse_inline_func:
                parse_inline_func(p, c_text, base_font_size=10.0, base_color=COLOR_TEXT_MAIN)
            else:
                r = p.add_run(c_text.strip())
                r.font.name = "Times New Roman"
                r.font.size = Pt(10.0)
                r.font.color.rgb = COLOR_TEXT_MAIN

    # Table Borders: subtle gray borders
    tblPr = table._tbl.tblPr
    borders_xml = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="6" w:space="0" w:color="{COLOR_BORDER}"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="{COLOR_BORDER}"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="{COLOR_BORDER}"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders_xml)

    # Table Caption nằm DƯỚI bảng, in nghiêng, căn giữa (đồng nhất với Hình)
    if has_bottom_caption:
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(4)
        p_cap.paragraph_format.space_after = Pt(8)
        p_cap.paragraph_format.line_spacing = 1.15
        r_cap = p_cap.add_run(caption.strip())
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(10.5)
        r_cap.italic = True
        r_cap.bold = False
        r_cap.font.color.rgb = COLOR_TEXT_MAIN
    else:
        # Trailing spacing paragraph nếu không có caption
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(6)

    return table
