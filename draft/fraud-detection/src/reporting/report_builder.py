"""
Master UIT Academic Document Compiler for CS106 Final Report.
Features:
- Section 1: Official UIT Cover Page (Phụ lục 1) with ornate triple black border,
  university headers, UIT logo (3.0 cm), course, topic, instructor & 7-student roster, and date.
- Section 2: Table of Contents (Phụ lục 2) with dot-leader tabs and active clickable hyperlinks.
- Section 3: Document Body adhering strictly to 2-2-3-2 cm margins, 1.27cm indent, 13pt Times New Roman,
  1.3 line spacing, 100% pure black text (#000000), bookmark anchors on all headings,
  active in-text citations jumping to bibliography, and external URL hyperlinks.
"""

from __future__ import annotations

import os
import re
import sys
import yaml
import json
import docx
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION_START
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

from .docx_table_builder import add_styled_table
from .toc_generator import build_toc_section, collect_toc_entries

COLOR_TEXT_MAIN = RGBColor(0, 0, 0)
COLOR_TEXT_MUTED = RGBColor(80, 80, 80)
COLOR_HEX_BLACK = "000000"


def add_bookmark(paragraph, name: str, bookmark_id: int) -> None:
    """Add a bookmark anchor around a paragraph for internal hyperlink jumping."""
    bm_start = parse_xml(f'<w:bookmarkStart {nsdecls("w")} w:id="{bookmark_id}" w:name="{name}"/>')
    bm_end = parse_xml(f'<w:bookmarkEnd {nsdecls("w")} w:id="{bookmark_id}"/>')
    paragraph._p.append(bm_start)
    paragraph._p.append(bm_end)


def add_page_number_field(run) -> None:
    """Add dynamic PAGE number field to a footer run."""
    fld1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls('w'))
    instr = parse_xml(r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>' % nsdecls('w'))
    fld2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls('w'))
    fld3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls('w'))
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)
    run._r.append(fld3)


def add_internal_hyperlink(
    paragraph,
    target_anchor: str,
    text: str,
    font_name="Times New Roman",
    font_size=13.0,
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


def add_external_hyperlink(
    paragraph,
    url: str,
    text: str | None = None,
    font_name="Times New Roman",
    font_size=12.0,
    is_bold=False,
    is_italic=False,
    color_hex="000000",
    is_underline=True
) -> None:
    """Add an external clickable web hyperlink in pure black."""
    if text is None:
        text = url
    escaped_text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
    part = paragraph.part
    r_id = part.relate_to(url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    w_ns = nsdecls('w')
    r_ns = nsdecls('r')
    hl = parse_xml(f'<w:hyperlink {w_ns} {r_ns} r:id="{r_id}"/>')
    bold_tag = "<w:b/>" if is_bold else ""
    italic_tag = "<w:i/>" if is_italic else ""
    u_tag = '<w:u w:val="single"/>' if is_underline else ""
    r = parse_xml(
        f'<w:r {w_ns}>'
        f'<w:rPr>'
        f'<w:rFonts w:ascii="{font_name}" w:hAnsi="{font_name}"/>'
        f'<w:sz w:val="{int(font_size * 2)}"/>'
        f'{bold_tag}'
        f'{italic_tag}'
        f'<w:color w:val="{color_hex}"/>'
        f'{u_tag}'
        f'</w:rPr>'
        f'<w:t xml:space="preserve">{escaped_text}</w:t>'
        f'</w:r>'
    )
    hl.append(r)
    paragraph._p.append(hl)


def parse_inline_formatting(
    paragraph,
    text: str,
    base_font_name="Times New Roman",
    base_font_size=13.0,
    is_italic=False,
    is_bold=False,
    base_color: RGBColor | None = None
) -> None:
    """
    Parse inline markdown formatting: bold, italic, code, citations, web links.
    Guarantees dash replacement and pure black text everywhere.
    """
    text = text.replace('—', ' - ').replace('–', '-')
    token_pattern = re.compile(
        r'(\*\*\*[^*]+\*\*\*|\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[\d+\]|\[[^\]]+\]\(https?://[^\)]+\)|https?://[^\s)\]]+)'
    )
    tokens = token_pattern.split(text)

    for token in tokens:
        if not token:
            continue

        # Markdown Web Link: [Anchor](URL)
        md_link_m = re.match(r'^\[([^\]]+)\]\((https?://[^\)]+)\)$', token)
        if md_link_m:
            add_external_hyperlink(
                paragraph, md_link_m.group(2), text=md_link_m.group(1),
                font_name=base_font_name, font_size=base_font_size,
                is_bold=is_bold, is_italic=is_italic, color_hex="000000", is_underline=True
            )
            continue

        # Direct Web URL
        if re.match(r'^https?://[^\s)\]]+$', token):
            add_external_hyperlink(
                paragraph, token, text=token,
                font_name=base_font_name, font_size=base_font_size,
                is_bold=is_bold, is_italic=is_italic, color_hex="000000", is_underline=True
            )
            continue

        # Citation [n] -> Clickable link to Bibliography anchor ref_n (Pure Black)
        if re.match(r'^\[(\d+)\]$', token):
            ref_id = re.match(r'^\[(\d+)\]$', token).group(1)
            add_internal_hyperlink(
                paragraph, f"ref_{ref_id}", f"[{ref_id}]",
                font_name=base_font_name, font_size=base_font_size,
                is_bold=True, color_hex="000000"
            )
            continue

        # Bold-Italic
        if token.startswith('***') and token.endswith('***') and len(token) >= 6:
            r = paragraph.add_run(token[3:-3])
            r.font.name = base_font_name
            r.font.size = Pt(base_font_size)
            r.bold = True
            r.italic = True
            r.font.color.rgb = COLOR_TEXT_MAIN
        # Bold
        elif token.startswith('**') and token.endswith('**') and len(token) >= 4:
            r = paragraph.add_run(token[2:-2])
            r.font.name = base_font_name
            r.font.size = Pt(base_font_size)
            r.bold = True
            r.italic = is_italic
            r.font.color.rgb = COLOR_TEXT_MAIN
        # Italic
        elif token.startswith('*') and token.endswith('*') and len(token) >= 2:
            r = paragraph.add_run(token[1:-1])
            r.font.name = base_font_name
            r.font.size = Pt(base_font_size)
            r.bold = is_bold
            r.italic = True
            r.font.color.rgb = COLOR_TEXT_MAIN
        # Monospace code (rendered cleanly in Courier New, pure black)
        elif token.startswith('`') and token.endswith('`') and len(token) >= 2:
            r = paragraph.add_run(token[1:-1])
            r.font.name = "Courier New"
            r.font.size = Pt(base_font_size - 0.5)
            r.bold = is_bold
            r.italic = is_italic
            r.font.color.rgb = COLOR_TEXT_MAIN
        else:
            r = paragraph.add_run(token)
            r.font.name = base_font_name
            r.font.size = Pt(base_font_size)
            r.bold = is_bold
            r.italic = is_italic
            r.font.color.rgb = COLOR_TEXT_MAIN


def build_cover_page(doc: docx.Document, meta: dict, base_dir: str) -> None:
    """
    Build official UIT Cover Page (Phụ lục 1) with ornate triple black border,
    university headers, UIT logo, topic title, instructor & student roster table.
    All text in 100% Pure Black (#000000).
    """
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
    pgBorders1 = parse_xml(r'''
    <w:pgBorders %s w:offsetFrom="page">
        <w:top w:val="triple" w:sz="18" w:space="20" w:color="000000"/>
        <w:left w:val="triple" w:sz="18" w:space="20" w:color="000000"/>
        <w:bottom w:val="triple" w:sz="18" w:space="20" w:color="000000"/>
        <w:right w:val="triple" w:sz="18" w:space="20" w:color="000000"/>
    </w:pgBorders>
    ''' % nsdecls('w'))
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

    # 4. Centered UIT Logo (3.0 cm width)
    logo_path = meta.get("logo_path")
    if logo_path and not os.path.isabs(logo_path):
        logo_path = os.path.join(base_dir, logo_path)

    if not logo_path or not os.path.exists(logo_path):
        # Fallback search
        cands = [
            os.path.join(base_dir, "images", "uit-logo.png"),
            "/Users/tcdtist/dev/uit/cs106/.agents/skills/academic-report/assets/uit-logo.png",
        ]
        for c in cands:
            if os.path.exists(c):
                logo_path = c
                break

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
    p_top_label.paragraph_format.space_before = Pt(2)
    p_top_label.paragraph_format.space_after = Pt(2)
    r_top_lbl = p_top_label.add_run("ĐỀ TÀI:")
    r_top_lbl.font.name = "Times New Roman"
    r_top_lbl.font.size = Pt(12.5)
    r_top_lbl.bold = True
    r_top_lbl.font.color.rgb = COLOR_TEXT_MAIN

    p_top_val = doc.add_paragraph()
    p_top_val.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top_val.paragraph_format.space_before = Pt(0)
    p_top_val.paragraph_format.space_after = Pt(18)
    p_top_val.paragraph_format.line_spacing = 1.25
    topic_text = meta.get("topic", "HỆ THỐNG PHÁT HIỆN GIAO DỊCH TÀI CHÍNH BẤT THƯỜNG VÀ NGHI VẤN GIAN LẬN")
    r_top_val = p_top_val.add_run(f'“{topic_text}”'.upper())
    r_top_val.font.name = "Times New Roman"
    r_top_val.font.size = Pt(13.5)
    r_top_val.bold = True
    r_top_val.font.color.rgb = COLOR_TEXT_MAIN

    # 8. Roster & Instructor Table (2 columns, borderless)
    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    for row in table.rows:
        row.cells[0].width = Cm(7.0)
        row.cells[1].width = Cm(9.0)

    # Column Headers (Row 0)
    c0 = table.cell(0, 0)
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_after = Pt(3)
    p0.paragraph_format.line_spacing = 1.15
    r0 = p0.add_run("GIẢNG VIÊN HƯỚNG DẪN:")
    r0.font.name = "Times New Roman"
    r0.font.size = Pt(11.5)
    r0.bold = True
    r0.font.color.rgb = COLOR_TEXT_MAIN

    c1 = table.cell(0, 1)
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_after = Pt(3)
    p1.paragraph_format.line_spacing = 1.15
    r1 = p1.add_run("SINH VIÊN THỰC HIỆN:")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11.5)
    r1.bold = True
    r1.font.color.rgb = COLOR_TEXT_MAIN

    # Column Details (Row 1)
    c0_body = table.cell(1, 0)
    p0_b = c0_body.paragraphs[0]
    p0_b.paragraph_format.space_after = Pt(0)
    p0_b.paragraph_format.line_spacing = 1.2

    inst = meta.get("instructor", {})
    inst_name = inst.get("name", "Nguyễn Đình Hiển") if isinstance(inst, dict) else str(inst)
    inst_title = inst.get("title", "PGS.TS.") if isinstance(inst, dict) else ""
    r0_b = p0_b.add_run(f"{inst_title} {inst_name}".strip())
    r0_b.font.name = "Times New Roman"
    r0_b.font.size = Pt(12)
    r0_b.bold = True
    r0_b.font.color.rgb = COLOR_TEXT_MAIN

    c1_body = table.cell(1, 1)
    p1_b = c1_body.paragraphs[0]
    p1_b.paragraph_format.space_after = Pt(0)
    p1_b.paragraph_format.line_spacing = 1.2

    group_name = meta.get("group_name", "Nhóm 9")
    r_grp = p1_b.add_run(f"{group_name}:\n")
    r_grp.font.name = "Times New Roman"
    r_grp.font.size = Pt(11.5)
    r_grp.bold = True
    r_grp.font.color.rgb = COLOR_TEXT_MAIN

    students = meta.get("students", [])
    for idx, st in enumerate(students, 1):
        s_name = st.get("name", "")
        s_id = st.get("student_id", "")
        s_role = st.get("role", "")
        s_class = st.get("class_id", "")

        extra_info = []
        if s_role and s_role.lower() != "thành viên":
            extra_info.append(s_role)
        if s_class:
            extra_info.append(s_class)
        extra_str = f" ({' - '.join(extra_info)})" if extra_info else ""

        line_str = f"{idx}. {s_name} - {s_id}{extra_str}"
        if idx < len(students):
            line_str += "\n"

        r_st = p1_b.add_run(line_str)
        r_st.font.name = "Times New Roman"
        r_st.font.size = Pt(11.0)
        r_st.bold = ("Trưởng nhóm" in s_role)
        r_st.font.color.rgb = COLOR_TEXT_MAIN

    # 9. Bottom Date & Location
    p_date = doc.add_paragraph()
    p_date.paragraph_format.space_before = Pt(24)
    p_date.paragraph_format.space_after = Pt(0)
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_date = p_date.add_run(meta.get("date", "TP. HỒ CHÍ MINH - THÁNG 09/2026"))
    r_date.font.name = "Times New Roman"
    r_date.font.size = Pt(12)
    r_date.bold = True
    r_date.font.color.rgb = COLOR_TEXT_MAIN


def build_body_section(
    doc: docx.Document,
    lines: list[str],
    meta: dict,
    base_dir: str,
    toc_data: list[dict]
) -> None:
    """
    Build Section 3 (Document Body) adhering to UIT standards:
    Margins: Left 3.0cm, Right 2.0cm, Top 2.0cm, Bottom 2.0cm.
    Font: Times New Roman 13pt regular, 1.3 line spacing, 1.27cm indent, Justified.
    Colors: 100% Pure Black (#000000) for all text and headings.
    Bookmarks: Matching TOC anchor IDs.
    Citations: Active internal hyperlinks jumping to Bibliography items.
    """
    sec3 = doc.add_section(WD_SECTION_START.NEW_PAGE)
    sec3.page_width = Cm(21.0)
    sec3.page_height = Cm(29.7)
    sec3.top_margin = Cm(2.0)
    sec3.bottom_margin = Cm(2.0)
    sec3.left_margin = Cm(3.0)
    sec3.right_margin = Cm(2.0)
    sec3.header_distance = Cm(1.0)
    sec3.footer_distance = Cm(1.0)
    sec3.different_first_page_header_footer = False
    sec3.header.is_linked_to_previous = False
    sec3.footer.is_linked_to_previous = False

    # Remove borders
    sectPr3 = sec3._sectPr
    pgBorders3 = parse_xml(r'''
    <w:pgBorders %s w:offsetFrom="page">
        <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>
    </w:pgBorders>
    ''' % nsdecls('w'))
    sectPr3.append(pgBorders3)

    # Page number starts at 1
    pgNumType = parse_xml(r'<w:pgNumType %s w:start="1"/>' % nsdecls('w'))
    sectPr3.append(pgNumType)

    # Header running title
    hdr_p = sec3.header.paragraphs[0]
    hdr_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    hdr_p.paragraph_format.space_after = Pt(0)
    hdr_r = hdr_p.add_run(meta.get("header_title", "Báo cáo Đồ án CS106 | Nhóm 9 - Fraud Detection"))
    hdr_r.font.name = "Times New Roman"
    hdr_r.font.size = Pt(9)
    hdr_r.italic = True
    hdr_r.font.color.rgb = COLOR_TEXT_MUTED

    # Footer page number
    ftr_p = sec3.footer.paragraphs[0]
    ftr_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    ftr_p.paragraph_format.space_after = Pt(0)
    ftr_p.paragraph_format.space_before = Pt(0)
    ftr_r = ftr_p.add_run()
    ftr_r.font.name = "Times New Roman"
    ftr_r.font.size = Pt(11)
    ftr_r.font.color.rgb = COLOR_TEXT_MAIN
    add_page_number_field(ftr_r)

    # Build title-to-anchor registry
    anchor_by_title = {item["text"].strip().lower(): item.get("anchor") for item in toc_data}

    # Skip draft metadata header if source starts with # Title / metadata table
    start_idx = 0
    for idx, line in enumerate(lines):
        if line.strip().startswith('# TÓM TẮT') or line.strip().startswith('# CHƯƠNG 1'):
            start_idx = idx
            break

    i = start_idx
    bookmark_counter = 1000

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # 1. Skip dividers, page breaks, empty lines
        if stripped in ['---', '***', '___', '\\newpage', '<br>', '<br><br>'] or not stripped:
            i += 1
            continue

        # 2. Image tag: ![alt](path)
        img_match = re.match(r'^!\[(.*?)\]\((.*?)\)$', stripped)
        if img_match:
            img_caption = img_match.group(1).strip()
            img_rel_path = img_match.group(2).strip()
            img_full = os.path.normpath(os.path.join(base_dir, img_rel_path))

            if os.path.exists(img_full):
                p_img = doc.add_paragraph()
                p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_img.paragraph_format.space_before = Pt(8)
                p_img.paragraph_format.space_after = Pt(3)
                r_img = p_img.add_run()
                r_img.add_picture(img_full, width=Cm(14.5))

                if img_caption:
                    p_cap = doc.add_paragraph()
                    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
                    p_cap.paragraph_format.space_before = Pt(2)
                    p_cap.paragraph_format.space_after = Pt(8)
                    r_cap = p_cap.add_run(img_caption)
                    r_cap.font.name = "Times New Roman"
                    r_cap.font.size = Pt(10.5)
                    r_cap.italic = True
                    r_cap.font.color.rgb = COLOR_TEXT_MAIN
            i += 1
            continue

        # 3. Figure caption standalone: *Hình X: ...*
        if re.match(r'^\*Hình\s+\d+.*\*$', stripped):
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            r_cap = p_cap.add_run(stripped[1:-1].strip())
            r_cap.font.name = "Times New Roman"
            r_cap.font.size = Pt(10.5)
            r_cap.italic = True
            r_cap.font.color.rgb = COLOR_TEXT_MAIN
            i += 1
            continue

        # 4. Heading 1: # Heading
        if line.startswith('# '):
            h_text = line[2:].strip().replace('—', ' - ').replace('–', '-')
            p_h = doc.add_paragraph()
            p_h.paragraph_format.keep_with_next = True
            p_h.paragraph_format.space_before = Pt(12)
            p_h.paragraph_format.space_after = Pt(4)
            p_h.paragraph_format.line_spacing = 1.15
            p_h.paragraph_format.first_line_indent = Cm(0)
            p_h.alignment = WD_ALIGN_PARAGRAPH.LEFT

            anchor = anchor_by_title.get(h_text.lower())
            if anchor:
                bookmark_counter += 1
                add_bookmark(p_h, anchor, bookmark_counter)

            r = p_h.add_run(h_text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(13.5)
            r.bold = True
            r.font.color.rgb = COLOR_TEXT_MAIN
            i += 1
            continue

        # 5. Heading 2: ## Heading
        if line.startswith('## '):
            h_text = line[3:].strip().replace('—', ' - ').replace('–', '-')
            p_h = doc.add_paragraph()
            p_h.paragraph_format.keep_with_next = True
            p_h.paragraph_format.space_before = Pt(8)
            p_h.paragraph_format.space_after = Pt(3)
            p_h.paragraph_format.line_spacing = 1.15
            p_h.paragraph_format.first_line_indent = Cm(0)
            p_h.alignment = WD_ALIGN_PARAGRAPH.LEFT

            anchor = anchor_by_title.get(h_text.lower())
            if anchor:
                bookmark_counter += 1
                add_bookmark(p_h, anchor, bookmark_counter)

            r = p_h.add_run(h_text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(13.0)
            r.bold = True
            r.font.color.rgb = COLOR_TEXT_MAIN
            i += 1
            continue

        # 6. Heading 3: ### Heading
        if line.startswith('### '):
            h_text = line[4:].strip().replace('—', ' - ').replace('–', '-')
            p_h = doc.add_paragraph()
            p_h.paragraph_format.keep_with_next = True
            p_h.paragraph_format.space_before = Pt(6)
            p_h.paragraph_format.space_after = Pt(2)
            p_h.paragraph_format.line_spacing = 1.15
            p_h.paragraph_format.first_line_indent = Cm(0)
            p_h.alignment = WD_ALIGN_PARAGRAPH.LEFT

            anchor = anchor_by_title.get(h_text.lower())
            if anchor:
                bookmark_counter += 1
                add_bookmark(p_h, anchor, bookmark_counter)

            r = p_h.add_run(h_text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(13.0)
            r.bold = True
            r.italic = True
            r.font.color.rgb = COLOR_TEXT_MAIN
            i += 1
            continue

        # 7. Blockquote: > ...
        if line.startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                q_text = lines[i].strip()[1:].strip()
                if q_text:
                    quote_lines.append(q_text)
                i += 1
            full_quote = " ".join(quote_lines)
            p_q = doc.add_paragraph()
            p_q.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_q.paragraph_format.left_indent = Cm(1.27)
            p_q.paragraph_format.right_indent = Cm(0.8)
            p_q.paragraph_format.space_before = Pt(3)
            p_q.paragraph_format.space_after = Pt(4)
            p_q.paragraph_format.line_spacing = 1.2
            parse_inline_formatting(p_q, full_quote, is_italic=True, base_font_size=12.0)
            continue

        # 8. List items (*, -, +, or 1.)
        list_match = re.match(r'^(\s*)([\*\-\+]|\d+\.)\s+(.*)$', line)
        if list_match:
            indent_spaces = len(list_match.group(1))
            bullet_sym = list_match.group(2)
            content = list_match.group(3)

            p_l = doc.add_paragraph()
            p_l.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            level = indent_spaces // 2
            p_l.paragraph_format.left_indent = Cm(1.27 + level * 0.4)
            p_l.paragraph_format.first_line_indent = Cm(-0.5)
            p_l.paragraph_format.space_before = Pt(1)
            p_l.paragraph_format.space_after = Pt(2)
            p_l.paragraph_format.line_spacing = 1.25

            bullet_char = "-  " if bullet_sym in ['*', '-', '+'] else f"{bullet_sym} "
            r_b = p_l.add_run(bullet_char)
            r_b.font.name = "Times New Roman"
            r_b.font.size = Pt(13)
            r_b.bold = True
            r_b.font.color.rgb = COLOR_TEXT_MAIN

            parse_inline_formatting(p_l, content)
            i += 1
            continue

        # 9. Reference / Bibliography entry: [1] Author...
        ref_match = re.match(r'^\[(\d+)\]\s+(.*)$', stripped)
        if ref_match:
            ref_num = ref_match.group(1)
            ref_body = ref_match.group(2)

            p_ref = doc.add_paragraph()
            p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p_ref.paragraph_format.left_indent = Cm(0.8)
            p_ref.paragraph_format.first_line_indent = Cm(-0.8)
            p_ref.paragraph_format.space_before = Pt(2)
            p_ref.paragraph_format.space_after = Pt(3)
            p_ref.paragraph_format.line_spacing = 1.15

            bookmark_counter += 1
            add_bookmark(p_ref, f"ref_{ref_num}", bookmark_counter)

            r_num = p_ref.add_run(f"[{ref_num}]\t")
            r_num.font.name = "Times New Roman"
            r_num.font.size = Pt(11.5)
            r_num.bold = True
            r_num.font.color.rgb = COLOR_TEXT_MAIN

            parse_inline_formatting(p_ref, ref_body, base_font_size=11.5)
            i += 1
            continue

        # 10. Markdown Table: | col1 | col2 |
        if stripped.startswith('|') and '|' in stripped[1:]:
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|') and '|' in lines[i].strip()[1:]:
                table_lines.append(lines[i].strip())
                i += 1

            rows_data = []
            for t_line in table_lines:
                if re.match(r'^\|[\s\:\-]+(\Auto|[\s\:\-\|]+)\|$', t_line):
                    continue
                raw_cells = [c.strip() for c in t_line.strip('|').split('|')]
                rows_data.append(raw_cells)

            if rows_data:
                header = rows_data[0]
                body_rows = rows_data[1:]

                cap = None
                if len(doc.paragraphs) > 0:
                    last_p_text = doc.paragraphs[-1].text.strip()
                    if last_p_text.startswith("Bảng ") or last_p_text.startswith("Table "):
                        cap = last_p_text
                        p_elem = doc.paragraphs[-1]._p
                        p_elem.getparent().remove(p_elem)

                add_styled_table(
                    doc, header, body_rows, caption=cap,
                    parse_inline_func=lambda p, txt, **kw: parse_inline_formatting(p, txt, **kw)
                )
            continue

        # 11. Standalone Table Caption: **Bảng X.Y...**
        if re.match(r'^\*\*Bảng\s+\d+.*?\*\*$', stripped):
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.keep_with_next = True
            p_cap.paragraph_format.space_before = Pt(8)
            p_cap.paragraph_format.space_after = Pt(3)
            r_cap = p_cap.add_run(stripped.strip('*').strip())
            r_cap.font.name = "Times New Roman"
            r_cap.font.size = Pt(11)
            r_cap.bold = True
            r_cap.font.color.rgb = COLOR_TEXT_MAIN
            i += 1
            continue

        # 12. Standard Body Paragraph
        p_body = doc.add_paragraph()
        p_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_body.paragraph_format.first_line_indent = Cm(1.27)
        p_body.paragraph_format.space_before = Pt(0)
        p_body.paragraph_format.space_after = Pt(2.0)
        p_body.paragraph_format.line_spacing = 1.3
        parse_inline_formatting(p_body, stripped)
        i += 1


def _legacy_build_document(blocks: list[dict], pages: dict[str, int], template_path: str, reports_dir: str) -> docx.Document:
    """Legacy compatibility builder for unit tests using parsed blocks and templates."""
    from .docx_table_builder import add_spacer, add_table
    from .markdown_parser import add_runs, clean_markdown_symbols
    from .toc_generator import add_toc, collect_toc_entries
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK

    document = docx.Document(template_path)
    entries = collect_toc_entries(blocks)
    cover_done = False
    cover_h1_done = False

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
                    p = document.add_paragraph(clean_markdown_symbols(block["text"]), style="CoverTitle")
                except Exception:
                    p = document.add_paragraph(clean_markdown_symbols(block["text"]))
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                cover_h1_done = True
            else:
                try:
                    document.add_paragraph(clean_markdown_symbols(block["text"]), style="Heading 1")
                except Exception:
                    document.add_paragraph(clean_markdown_symbols(block["text"]))
            continue

        if kind in ("h2", "h3"):
            style_name = "Heading 2" if kind == "h2" else "Heading 3"
            try:
                document.add_paragraph(clean_markdown_symbols(block["text"]), style=style_name)
            except Exception:
                document.add_paragraph(clean_markdown_symbols(block["text"]))
            continue

        if kind == "table":
            add_table(document, block["header"], block["rows"])
            add_spacer(document)
            continue

        if kind == "note":
            try:
                p = document.add_paragraph(style="ReportNote")
            except Exception:
                p = document.add_paragraph()
            add_runs(p, block["text"])
            continue

        if kind in ("bullet", "number"):
            style_name = "List Bullet" if kind == "bullet" else "List Number"
            try:
                p = document.add_paragraph(style=style_name)
            except Exception:
                p = document.add_paragraph()
            add_runs(p, block["text"])
            continue

        style = "CoverMeta" if not cover_done else "ReportBody"
        try:
            p = document.add_paragraph(style=style)
        except Exception:
            p = document.add_paragraph()
        add_runs(p, block.get("text", ""))

    return document


def build_document(
    first_arg: str | list[dict],
    second_arg: str | dict[str, int],
    meta_path: str | None = None,
    page_mapping: dict[str, int] | None = None,
    template_path: str | None = None,
    reports_dir: str | None = None
) -> docx.Document:
    """Master build procedure constructing the 3-section UIT Document or delegating to legacy builder."""
    # Legacy invocation: build_document(blocks, pages, template_path=..., reports_dir=...)
    if isinstance(first_arg, list):
        tpl = template_path or (meta_path if isinstance(meta_path, str) and meta_path.endswith(".docx") else None)
        rdir = reports_dir or ""
        pages = second_arg if isinstance(second_arg, dict) else {}
        return _legacy_build_document(first_arg, pages, tpl, rdir)

    # Modern high-fidelity UIT invocation: build_document(markdown_path, output_docx_path, meta_path, page_mapping)
    markdown_path = str(first_arg)
    output_docx_path = str(second_arg)
    base_dir = os.path.dirname(os.path.abspath(markdown_path))

    with open(markdown_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    # Sanitize dashes in input
    md_text = md_text.replace('—', ' - ').replace('–', '-')

    # Load metadata
    meta = {}
    if meta_path and os.path.exists(meta_path) and not meta_path.endswith(".docx"):
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = yaml.safe_load(f) or {}
    else:
        auto_meta = os.path.join(base_dir, "report-meta.yaml")
        if os.path.exists(auto_meta):
            with open(auto_meta, "r", encoding="utf-8") as f:
                meta = yaml.safe_load(f) or {}

    lines = md_text.split('\n')
    toc_data = collect_toc_entries(lines)

    doc = docx.Document()

    # Global style defaults: Times New Roman 13pt, Pure Black
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
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
    pgBorders2 = parse_xml(r'''
    <w:pgBorders %s w:offsetFrom="page">
        <w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/>
    </w:pgBorders>
    ''' % nsdecls('w'))
    sectPr2.append(pgBorders2)

    build_toc_section(doc, toc_data, page_mapping or {})

    # 3. Section 3: Document Body
    build_body_section(doc, lines, meta, base_dir, toc_data)

    doc.save(output_docx_path)
    return doc

