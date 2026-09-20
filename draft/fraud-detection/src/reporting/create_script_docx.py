"""
Script chuyển đổi SCRIPT_THUYET_TRINH_TOAN_TEAM_CS106.md thành SCRIPT_THUYET_TRINH_TOAN_TEAM_CS106.docx
đảm bảo đồng bộ 100% nội dung với định dạng đẹp mắt, chuyên nghiệp.
"""
from pathlib import Path
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def add_styled_paragraph(doc, text, style_name='Normal', bold_prefix=None):
    p = doc.add_paragraph(style=style_name)
    # Parse bold text **text**
    parts = re.split(r'(\*\*.*?\*\*)', text)
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            run = p.add_run(part[2:-2])
            run.bold = True
        else:
            p.add_run(part)
    return p

def convert_script_md_to_docx(md_path: Path, docx_path: Path):
    doc = docx.Document()

    # Set normal style font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # Page margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    with md_path.open('r', encoding='utf-8') as f:
        lines = f.readlines()

    in_table = False
    table_rows = []

    for line in lines:
        line_str = line.rstrip('\r\n')
        stripped = line_str.strip()

        # Check table
        if stripped.startswith('|') and stripped.endswith('|'):
            # Table row
            if re.match(r'^\|[\s\-:|]+\|$', stripped):
                # Separator line
                continue
            cols = [c.strip() for c in stripped[1:-1].split('|')]
            table_rows.append(cols)
            in_table = True
            continue
        else:
            if in_table and table_rows:
                # Render table
                num_cols = max(len(r) for r in table_rows)
                t = doc.add_table(rows=0, cols=num_cols)
                t.style = 'Table Grid'
                is_header = True
                for row_data in table_rows:
                    row_cells = t.add_row().cells
                    for idx, val in enumerate(row_data):
                        if idx < num_cols:
                            row_cells[idx].text = val
                            if is_header:
                                set_cell_background(row_cells[idx], "1F497D")
                                for p in row_cells[idx].paragraphs:
                                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                    for r in p.runs:
                                        r.font.name = 'Times New Roman'
                                        r.font.bold = True
                                        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                            else:
                                for p in row_cells[idx].paragraphs:
                                    for r in p.runs:
                                        r.font.name = 'Times New Roman'
                                        r.font.size = Pt(10)
                    is_header = False
                doc.add_paragraph()
                table_rows = []
                in_table = False

        if not stripped:
            continue

        # Horizontal rule
        if stripped in ('---', '***', '___'):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(4)
            p.paragraph_format.space_after = Pt(4)
            continue

        # Headings
        if stripped.startswith('# '):
            h = doc.add_heading(level=0)
            h.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = h.add_run(stripped[2:])
            run.font.name = 'Times New Roman'
            run.font.size = Pt(16)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
            continue

        if stripped.startswith('## '):
            h = doc.add_heading(level=1)
            run = h.add_run(stripped[3:])
            run.font.name = 'Times New Roman'
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)
            continue

        if stripped.startswith('### '):
            h = doc.add_heading(level=2)
            run = h.add_run(stripped[4:])
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x2E, 0x75, 0xB6)
            continue

        if stripped.startswith('#### '):
            h = doc.add_heading(level=3)
            run = h.add_run(stripped[5:])
            run.font.name = 'Times New Roman'
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
            continue

        # Blockquote
        if stripped.startswith('> '):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.3)
            p.paragraph_format.right_indent = Inches(0.3)
            text_inside = stripped[2:]
            parts = re.split(r'(\*\*.*?\*\*)', text_inside)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    r = p.add_run(part[2:-2])
                    r.bold = True
                else:
                    r = p.add_run(part)
                r.italic = True
                r.font.name = 'Times New Roman'
                r.font.color.rgb = RGBColor(0x44, 0x44, 0x44)
            continue

        # Bullet list
        if stripped.startswith('- ') or stripped.startswith('* '):
            p = doc.add_paragraph(style='List Bullet')
            parts = re.split(r'(\*\*.*?\*\*)', stripped[2:])
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    r = p.add_run(part[2:-2])
                    r.bold = True
                else:
                    r = p.add_run(part)
                r.font.name = 'Times New Roman'
            continue

        # Numbered list
        m_num = re.match(r'^(\d+)\.\s+(.*)$', stripped)
        if m_num:
            num, text_num = m_num.groups()
            p = doc.add_paragraph(style='List Number')
            parts = re.split(r'(\*\*.*?\*\*)', text_num)
            for part in parts:
                if part.startswith('**') and part.endswith('**'):
                    r = p.add_run(part[2:-2])
                    r.bold = True
                else:
                    r = p.add_run(part)
                r.font.name = 'Times New Roman'
            continue

        # Normal paragraph
        p = doc.add_paragraph()
        parts = re.split(r'(\*\*.*?\*\*|\_.*?\_)', stripped)
        for part in parts:
            if part.startswith('**') and part.endswith('**'):
                r = p.add_run(part[2:-2])
                r.bold = True
            elif part.startswith('_') and part.endswith('_'):
                r = p.add_run(part[1:-1])
                r.italic = True
            else:
                r = p.add_run(part)
            r.font.name = 'Times New Roman'

    docx_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(docx_path))
    print("[OK] Da tao docx kich ban thuyet trinh thanh cong.")

if __name__ == '__main__':
    base_dir = Path(__file__).resolve().parents[2]
    md_file = base_dir / 'slide' / 'scripts' / 'SCRIPT_THUYET_TRINH_TOAN_TEAM_CS106.md'
    docx_file = base_dir / 'slide' / 'scripts' / 'SCRIPT_THUYET_TRINH_TOAN_TEAM_CS106.docx'
    convert_script_md_to_docx(md_file, docx_file)
