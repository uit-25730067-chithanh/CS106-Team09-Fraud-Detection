"""UIT Cover Page Builder (Phụ lục 1) for CS106 Final Report.

Constructs the first section of the academic document with:
- Ornate triple black border frame
- University headers (VNU-HCM / UIT / Department)
- Centered UIT logo (3.0 cm)
- Course info, topic title
- Instructor and 7-student roster table
- Date and location footer

All text in 100% Pure Black (#000000).
"""

from __future__ import annotations

import logging
import os

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Cm, Pt

from .hyperlink_helpers import COLOR_TEXT_MAIN

logger = logging.getLogger(__name__)


def build_cover_page(doc: docx.Document, meta: dict, base_dir: str) -> None:
    """Build official UIT Cover Page (Phụ lục 1)."""
    sec1 = doc.sections[0]
    sec1.page_width = Cm(21.0)
    sec1.page_height = Cm(29.7)
    sec1.top_margin = Cm(2.0)
    sec1.bottom_margin = Cm(2.0)
    sec1.left_margin = Cm(2.5)
    sec1.right_margin = Cm(2.5)
    sec1.different_first_page_header_footer = False
    sec1.header.is_linked_to_previous = False
    sec1.footer.is_linked_to_previous = False

    # 1. Ornate triple border in Pure Black (#000000)
    sectPr1 = sec1._sectPr
    pgBorders1 = parse_xml(
        r"""
    <w:pgBorders %s w:offsetFrom="page">
        <w:top w:val="triple" w:sz="18" w:space="20" w:color="000000"/>
        <w:left w:val="triple" w:sz="18" w:space="20" w:color="000000"/>
        <w:bottom w:val="triple" w:sz="18" w:space="20" w:color="000000"/>
        <w:right w:val="triple" w:sz="18" w:space="20" w:color="000000"/>
    </w:pgBorders>
    """
        % nsdecls("w")
    )
    sectPr1.append(pgBorders1)

    # 2. University Header
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.15

    uni_lines = [
        meta.get("university", "ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH"),
        meta.get("school", "TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN"),
    ]
    dept = meta.get("department", "KHOA KHOA HỌC MÁY TÍNH")
    if dept:
        uni_lines.append(dept)

    r_uni = p.add_run("\n".join(uni_lines))
    r_uni.font.name = "Times New Roman"
    r_uni.font.size = Pt(12)
    r_uni.bold = True
    r_uni.font.color.rgb = COLOR_TEXT_MAIN

    # 3. Decorative Divider -o0o-
    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(2)
    p_div.paragraph_format.space_after = Pt(6)
    r_div = p_div.add_run("-o0o-")
    r_div.font.name = "Times New Roman"
    r_div.font.size = Pt(11)
    r_div.bold = True
    r_div.font.color.rgb = COLOR_TEXT_MAIN

    # 4. Centered UIT Logo (3.0 cm width) — relative paths only (C1 fix)
    logo_path = meta.get("logo_path")
    if logo_path and not os.path.isabs(logo_path):
        logo_path = os.path.join(base_dir, logo_path)

    if not logo_path or not os.path.exists(logo_path):
        # Search only within the project tree — no hardcoded absolute paths
        relative_candidates = [
            os.path.join(base_dir, "images", "uit-logo.png"),
            os.path.join(base_dir, "..", "..", ".agents", "skills", "academic-report", "assets", "uit-logo.png"),
        ]
        logo_path = None
        for c in relative_candidates:
            resolved = os.path.normpath(c)
            if os.path.exists(resolved):
                logo_path = resolved
                break
        if logo_path is None:
            logger.warning(
                "UIT logo not found in any candidate path. "
                "Set 'logo_path' in report-meta.yaml or place uit-logo.png in reports/images/."
            )

    if logo_path and os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_before = Pt(2)
        p_logo.paragraph_format.space_after = Pt(8)
        r_logo = p_logo.add_run()
        r_logo.add_picture(logo_path, width=Cm(3.0))

    # 5. Document Title
    p_doc = doc.add_paragraph()
    p_doc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_doc.paragraph_format.space_before = Pt(6)
    p_doc.paragraph_format.space_after = Pt(3)
    r_doc = p_doc.add_run(meta.get("document_title", "BÁO CÁO ĐỒ ÁN MÔN HỌC"))
    r_doc.font.name = "Times New Roman"
    r_doc.font.size = Pt(16)
    r_doc.bold = True
    r_doc.font.color.rgb = COLOR_TEXT_MAIN

    # 6. Course Info
    c_name = meta.get("course_name", "TRÍ TUỆ NHÂN TẠO")
    c_code = meta.get("course_code", "CS106")
    p_c = doc.add_paragraph()
    p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_c.paragraph_format.space_before = Pt(0)
    p_c.paragraph_format.space_after = Pt(12)
    r_c = p_c.add_run(f"MÔN HỌC: {c_name} ({c_code})".upper())
    r_c.font.name = "Times New Roman"
    r_c.font.size = Pt(13)
    r_c.bold = True
    r_c.font.color.rgb = COLOR_TEXT_MAIN

    # 7. Topic Title
    p_top_label = doc.add_paragraph()
    p_top_label.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top_label.paragraph_format.space_before = Pt(4)
    p_top_label.paragraph_format.space_after = Pt(2)
    top_label_text = meta.get("topic_label", "ĐỀ TÀI SỐ 7:")
    r_top_lbl = p_top_label.add_run(top_label_text)
    r_top_lbl.font.name = "Times New Roman"
    r_top_lbl.font.size = Pt(13)
    r_top_lbl.bold = True
    r_top_lbl.font.color.rgb = COLOR_TEXT_MAIN

    p_top_val = doc.add_paragraph()
    p_top_val.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top_val.paragraph_format.space_before = Pt(0)
    p_top_val.paragraph_format.space_after = Pt(16)
    p_top_val.paragraph_format.line_spacing = 1.25
    topic_text = meta.get(
        "topic",
        "HỆ THỐNG PHÁT HIỆN GIAO DỊCH TÀI CHÍNH BẤT THƯỜNG VÀ NGHI VẤN GIAN LẬN",
    )
    r_top_val = p_top_val.add_run(topic_text.upper())
    r_top_val.font.name = "Times New Roman"
    r_top_val.font.size = Pt(13.5)
    r_top_val.bold = True
    r_top_val.font.color.rgb = COLOR_TEXT_MAIN

    # 8. Roster & Instructor Block (Single centered 1-column layout)
    _build_roster_block(doc, meta)

    # 9. Bottom Date & Location
    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_before = Pt(20)
    p_date.paragraph_format.space_after = Pt(0)
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_date = p_date.add_run(
        meta.get("date", "TP. HỒ CHÍ MINH - THÁNG 09/2026")
    )
    r_date.font.name = "Times New Roman"
    r_date.font.size = Pt(12)
    r_date.bold = True
    r_date.font.color.rgb = COLOR_TEXT_MAIN


def _build_roster_block(doc: docx.Document, meta: dict) -> None:
    """Build the instructor + student roster table on the cover page (2-column balanced layout)."""
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Set column widths: Left (GVHD) 5.8cm, Right (SVTH) 9.2cm = 15.0cm
    col_widths = [Cm(5.8), Cm(9.2)]
    for i, col in enumerate(table.columns):
        col.width = col_widths[i]

    # Remove cell borders and set top vertical alignment
    for i, w in enumerate(col_widths):
        c = table.cell(0, i)
        c.width = w
        tcPr = c._tc.get_or_add_tcPr()
        borders_xml = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:top w:val="none"/><w:left w:val="none"/>'
            f'<w:bottom w:val="none"/><w:right w:val="none"/>'
            f"</w:tcBorders>"
        )
        tcPr.append(borders_xml)
        valign_xml = parse_xml(f'<w:vAlign {nsdecls("w")} w:val="top"/>')
        tcPr.append(valign_xml)

    # 1. Left Cell: Instructor
    cell_gv = table.cell(0, 0)
    p_gv = cell_gv.paragraphs[0]
    p_gv.paragraph_format.space_before = Pt(4)
    p_gv.paragraph_format.space_after = Pt(2)
    p_gv.paragraph_format.line_spacing = 1.15
    r_gvh = p_gv.add_run("GIẢNG VIÊN HƯỚNG DẪN:")
    r_gvh.font.name = "Times New Roman"
    r_gvh.font.size = Pt(11.5)
    r_gvh.bold = True
    r_gvh.font.color.rgb = COLOR_TEXT_MAIN

    p_gvn = cell_gv.add_paragraph()
    p_gvn.paragraph_format.space_before = Pt(2)
    p_gvn.paragraph_format.space_after = Pt(4)
    p_gvn.paragraph_format.line_spacing = 1.15
    inst = meta.get("instructor", {})
    inst_name = inst.get("name", "Nguyễn Đình Hiển") if isinstance(inst, dict) else str(inst)
    inst_title = inst.get("title", "PGS.TS.") if isinstance(inst, dict) else ""
    r_gvn = p_gvn.add_run(f"{inst_title} {inst_name}".strip())
    r_gvn.font.name = "Times New Roman"
    r_gvn.font.size = Pt(12)
    r_gvn.bold = True
    r_gvn.font.color.rgb = COLOR_TEXT_MAIN

    # 2. Right Cell: Student Group
    cell_sv = table.cell(0, 1)
    p_svh = cell_sv.paragraphs[0]
    p_svh.paragraph_format.space_before = Pt(4)
    p_svh.paragraph_format.space_after = Pt(2)
    p_svh.paragraph_format.line_spacing = 1.15
    r_svh = p_svh.add_run("NHÓM SINH VIÊN THỰC HIỆN:")
    r_svh.font.name = "Times New Roman"
    r_svh.font.size = Pt(11.5)
    r_svh.bold = True
    r_svh.font.color.rgb = COLOR_TEXT_MAIN

    group_name = meta.get("group_name", "Nhóm 09")
    class_id = meta.get("class_id", "CS106.F31.CN2.TTNT")
    p_grp = cell_sv.add_paragraph()
    p_grp.paragraph_format.space_before = Pt(0)
    p_grp.paragraph_format.space_after = Pt(4)
    p_grp.paragraph_format.line_spacing = 1.15
    r_grp = p_grp.add_run(f"{group_name} - Lớp: {class_id}")
    r_grp.font.name = "Times New Roman"
    r_grp.font.size = Pt(11.0)
    r_grp.bold = True
    r_grp.font.color.rgb = COLOR_TEXT_MAIN

    # Student list
    p_sts = cell_sv.add_paragraph()
    p_sts.paragraph_format.space_before = Pt(0)
    p_sts.paragraph_format.space_after = Pt(4)
    p_sts.paragraph_format.line_spacing = 1.25

    students = meta.get("students", [])
    for idx, st in enumerate(students, 1):
        s_name = st.get("name", "")
        s_id = st.get("student_id", "")
        s_role = st.get("role", "")

        extra_info = []
        if s_role and "trưởng nhóm" in s_role.lower():
            extra_info.append(s_role)
        extra_str = f" ({', '.join(extra_info)})" if extra_info else ""

        line_str = f"{idx}. {s_name} - {s_id}{extra_str}"
        if idx < len(students):
            line_str += "\n"

        r_st = p_sts.add_run(line_str)
        r_st.font.name = "Times New Roman"
        r_st.font.size = Pt(11.0)
        r_st.bold = "trưởng nhóm" in s_role.lower()
        r_st.font.color.rgb = COLOR_TEXT_MAIN
