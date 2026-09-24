"""
Module chuyển đổi SCRIPT_THUYET_TRINH_TOAN_TEAM_CS106.md thành SCRIPT_THUYET_TRINH_TOAN_TEAM_CS106.docx
theo chuẩn uu:docx-stylist (Master Template Pattern), đảm bảo 100% sạch dấu LaTeX/Backticks,
định dạng học thuật UIT chuẩn mực, bảng biểu chuyên nghiệp, căn lề và typography tối ưu.
"""
from pathlib import Path
import re
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

# --- XML UTILITIES ---

def set_cell_background(cell, fill_hex):
    """Đặt màu nền cho cell trong bảng."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Đặt lề trong (padding) cho ô bảng tính theo dxa (1 pt = 20 dxa)."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for margin_name, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{margin_name}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_row_cant_split(row):
    """Ngăn hàng bảng bị gãy đôi khi sang trang."""
    trPr = row._element.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

def set_table_header_repeat(row):
    """Lặp lại tiêu đề bảng khi bảng kéo dài qua trang mới."""
    trPr = row._element.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

def set_blockquote_borders(paragraph):
    """Thêm đường viền bên trái cho blockquote kiểu Callout chuẩn Word."""
    pPr = paragraph._element.get_or_add_pPr()
    pBdr = parse_xml(
        f'<w:pBdr {nsdecls("w")}>'
        f'  <w:left w:val="single" w:sz="24" w:space="12" w:color="1F497D"/>'
        f'</w:pBdr>'
    )
    pPr.append(pBdr)

# --- INLINE MARKDOWN TOKENIZER ---

def tokenize_inline(text, parent_italic=False, parent_bold=False):
    """
    Tách chuỗi markdown thành các đoạn tuple (text, is_bold, is_italic, is_code).
    Xử lý sạch dấu backtick, ký hiệu latex, markdown nested bold/italic,
    và bảo vệ các định danh biến số có gạch dưới (drain_flag, is_overnight, v.v.).
    """
    text = text.strip()
    if not text:
        return []

    # 1. Nhận diện chỉ dẫn thoại đặc biệt dạng _(...)_ hoặc *(...)*
    if (text.startswith("_(") and text.endswith(")_")) or (text.startswith("*(") and text.endswith(")*")):
        text = "(" + text[2:-2].strip() + ")"
        parent_italic = True
    elif (text.startswith("*\"") and text.endswith("\"*")) or (text.startswith("*\"") and text.endswith("\"*.")):
        has_dot = text.endswith(".")
        text = "\"" + text[2:-2 if not has_dot else -3].strip() + "\"" + ("." if has_dot else "")
        parent_italic = True

    # 2. Regex tách token inline:
    # Nhóm 1: `code` (sạch dấu backtick)
    # Nhóm 2: ***bold-italic*** hoặc **_bold-italic_**
    # Nhóm 3: **bold**
    # Nhóm 4: *"italic quote"*
    # Nhóm 5: *italic* (biên từ an toàn)
    # Nhóm 6: _italic_ (biên từ an toàn, không dính vào biến có underscore)
    token_pattern = re.compile(
        r"(`[^`]+`)"                                    # Group 1: code
        r"|(\*\*\*[^*]+\*\*\*|\*\*_[^_]+_\*\*)"          # Group 2: bold-italic
        r"|(\*\*[^*]+\*\*)"                             # Group 3: bold
        r"|(\*\"[^\"]+\"\*)"                            # Group 4: italic quote *"..."*
        r"|((?<!\w)\*[^*\n]+?\*(?!\w))"                 # Group 5: italic *
        r"|((?<!\w)_[^_\n]+?_(?!\w))"                   # Group 6: italic _
    )

    tokens = []
    last_end = 0

    for match in token_pattern.finditer(text):
        start, end = match.span()
        if start > last_end:
            raw = text[last_end:start]
            if raw:
                tokens.append((raw, parent_bold, parent_italic, False))

        g_code, g_bi, g_b, g_iq, g_i_star, g_i_under = match.groups()
        if g_code:
            inner = g_code[1:-1]  # Loại bỏ dấu backtick triệt để
            tokens.append((inner, True if parent_bold else False, parent_italic, True))
        elif g_bi:
            inner = g_bi[3:-3]
            tokens.append((inner, True, True, False))
        elif g_b:
            inner = g_b[2:-2]
            tokens.append((inner, True, parent_italic, False))
        elif g_iq:
            inner = "\"" + g_iq[2:-2] + "\""
            tokens.append((inner, parent_bold, True, False))
        elif g_i_star:
            inner = g_i_star[1:-1]
            tokens.append((inner, parent_bold, True, False))
        elif g_i_under:
            inner = g_i_under[1:-1]
            tokens.append((inner, parent_bold, True, False))

        last_end = end

    if last_end < len(text):
        raw = text[last_end:]
        if raw:
            tokens.append((raw, parent_bold, parent_italic, False))

    return tokens

def add_formatted_runs_to_paragraph(paragraph, text, font_name="Times New Roman", font_size=Pt(11), default_color=None, is_blockquote=False):
    """Thêm các text runs đã được định dạng vào paragraph."""
    tokens = tokenize_inline(text)
    for snippet, is_bold, is_italic, is_code in tokens:
        run = paragraph.add_run(snippet)
        run.bold = is_bold
        run.italic = is_italic
        run.font.name = font_name

        if font_size:
            run.font.size = font_size

        if is_code:
            run.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)  # Highlight màu navy trang nhã
            run.bold = True
        elif default_color:
            run.font.color.rgb = default_color
        elif is_blockquote:
            run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        else:
            run.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

# --- CONVERTER ENGINE (MASTER TEMPLATE PATTERN) ---

def convert_script_md_to_docx(md_path: Path, docx_path: Path, template_path: Path = None):
    """
    Chuyển đổi file MD sang DOCX bằng cách áp dụng Master Template Pattern (uu:docx-stylist).
    Kế thừa metadata, margins, headers/footers và styles có sẵn trong template.
    """
    if template_path and template_path.exists():
        print(f"[uu:docx-stylist] Nạp Master Template: {template_path.name}")
        doc = docx.Document(str(template_path))
        # 1. Dọn dẹp nội dung mẫu cũ nhưng giữ nguyên styles, margins và section properties
        for table in list(doc.tables):
            table._element.getparent().remove(table._element)
        for p in list(doc.paragraphs):
            p._element.getparent().remove(p._element)
    else:
        print("[uu:docx-stylist] Khởi tạo tài liệu mới theo chuẩn UIT academic.")
        doc = docx.Document()
        for section in doc.sections:
            section.top_margin = Inches(0.98)     # 2.5 cm
            section.bottom_margin = Inches(0.98)  # 2.5 cm
            section.left_margin = Inches(1.18)    # 3.0 cm
            section.right_margin = Inches(0.79)   # 2.0 cm

    # Cập nhật Header & Footer chuẩn bài báo cáo
    for section in doc.sections:
        header = section.header
        if header.paragraphs:
            hp = header.paragraphs[0]
            hp.text = "CS106 — Kịch bản thuyết trình Đồ án Final | Nhóm 09 (PaySim Fraud Detection)"
            hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            for r in hp.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(8.5)
                r.font.italic = True
                r.font.color.rgb = RGBColor(0x7F, 0x7F, 0x7F)

    with md_path.open("r", encoding="utf-8") as f:
        lines = f.readlines()

    in_table = False
    table_rows = []

    for line in lines:
        line_str = line.rstrip("\r\n")
        stripped = line_str.strip()

        # 1. Xử lý Bảng biểu (Markdown Table)
        if stripped.startswith("|") and stripped.endswith("|"):
            # Bỏ qua dòng kẻ phân cách |:---|---|
            if re.match(r"^\|[\s\-:|]+\|$", stripped):
                continue
            cols = [c.strip() for c in stripped[1:-1].split("|")]
            table_rows.append(cols)
            in_table = True
            continue
        else:
            if in_table and table_rows:
                # Kết thúc bảng -> Render Table ra Word
                num_cols = max(len(r) for r in table_rows)
                t = doc.add_table(rows=0, cols=num_cols)
                t.style = "Table Grid"
                t.alignment = WD_TABLE_ALIGNMENT.CENTER

                # Độ rộng tương đối cho bảng thời lượng (10 cột)
                col_widths = [
                    Inches(0.4),  # STT
                    Inches(1.0),  # Thành viên
                    Inches(0.9),  # Slide
                    Inches(0.9),  # Tình trạng
                    Inches(1.8),  # Nội dung
                    Inches(0.8),  # Target
                    Inches(0.8),  # Script time
                    Inches(0.8),  # Dry-run
                    Inches(0.8),  # Chênh lệch
                    Inches(1.8)   # Khuyến nghị
                ]

                is_header = True
                for r_idx, row_data in enumerate(table_rows):
                    row = t.add_row()
                    set_row_cant_split(row)
                    if is_header:
                        set_table_header_repeat(row)

                    for c_idx, cell_value in enumerate(row_data):
                        if c_idx < num_cols:
                            cell = row.cells[c_idx]
                            if c_idx < len(col_widths):
                                cell.width = col_widths[c_idx]

                            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

                            p = cell.paragraphs[0]
                            p.paragraph_format.space_before = Pt(2)
                            p.paragraph_format.space_after = Pt(2)
                            p.paragraph_format.line_spacing = 1.05

                            if is_header:
                                set_cell_background(cell, "1F497D")  # Navy chuẩn
                                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                add_formatted_runs_to_paragraph(
                                    p, cell_value,
                                    font_size=Pt(9.5),
                                    default_color=RGBColor(0xFF, 0xFF, 0xFF)
                                )
                                for r in p.runs:
                                    r.bold = True
                            else:
                                if r_idx % 2 == 1:
                                    set_cell_background(cell, "F2F5F9")  # Zebra stripe nhẹ
                                if c_idx in (0, 2, 5, 6, 7, 8):
                                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                                else:
                                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT

                                add_formatted_runs_to_paragraph(
                                    p, cell_value,
                                    font_size=Pt(9),
                                    default_color=RGBColor(0x22, 0x22, 0x22)
                                )

                    is_header = False

                # Thêm khoảng đệm sau bảng
                post_p = doc.add_paragraph()
                post_p.paragraph_format.space_before = Pt(4)
                post_p.paragraph_format.space_after = Pt(4)
                table_rows = []
                in_table = False

        if not stripped:
            continue

        # 2. Xử lý Đường kẻ ngang (Horizontal Rule)
        if stripped in ("---", "***", "___"):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.space_after = Pt(6)
            continue

        # 3. Xử lý Tiêu đề (Headings)
        if stripped.startswith("# "):
            h = doc.add_paragraph()
            h.alignment = WD_ALIGN_PARAGRAPH.CENTER
            h.paragraph_format.space_before = Pt(14)
            h.paragraph_format.space_after = Pt(8)
            add_formatted_runs_to_paragraph(
                h, stripped[2:],
                font_size=Pt(16),
                default_color=RGBColor(0x1F, 0x49, 0x7D)
            )
            for r in h.runs:
                r.bold = True
            continue

        if stripped.startswith("## "):
            h = doc.add_paragraph()
            h.paragraph_format.space_before = Pt(12)
            h.paragraph_format.space_after = Pt(5)
            add_formatted_runs_to_paragraph(
                h, stripped[3:],
                font_size=Pt(13.5),
                default_color=RGBColor(0x1F, 0x49, 0x7D)
            )
            for r in h.runs:
                r.bold = True
            continue

        if stripped.startswith("### "):
            h = doc.add_paragraph()
            h.paragraph_format.space_before = Pt(9)
            h.paragraph_format.space_after = Pt(3)
            add_formatted_runs_to_paragraph(
                h, stripped[4:],
                font_size=Pt(12),
                default_color=RGBColor(0x2E, 0x75, 0xB6)
            )
            for r in h.runs:
                r.bold = True
            continue

        if stripped.startswith("#### "):
            h = doc.add_paragraph()
            h.paragraph_format.space_before = Pt(7)
            h.paragraph_format.space_after = Pt(2)
            add_formatted_runs_to_paragraph(
                h, stripped[5:],
                font_size=Pt(11),
                default_color=RGBColor(0x33, 0x33, 0x33)
            )
            for r in h.runs:
                r.bold = True
            continue

        # 4. Xử lý Trích dẫn / Callout (Blockquotes)
        if stripped.startswith(">"):
            # Bỏ ký tự > và khoảng trắng đầu
            raw_inside = stripped[1:].strip()
            if not raw_inside:
                # Dòng > trống, bỏ qua không tạo đoạn rỗng
                continue

            # Kiểm tra xem có phải danh sách gạch đầu dòng bên trong blockquote không
            if raw_inside.startswith("- ") or raw_inside.startswith("* "):
                p = doc.add_paragraph(style="List Bullet")
                p.paragraph_format.left_indent = Inches(0.5)
                p.paragraph_format.space_before = Pt(1.5)
                p.paragraph_format.space_after = Pt(1.5)
                p.paragraph_format.line_spacing = 1.15
                add_formatted_runs_to_paragraph(p, raw_inside[2:], font_size=Pt(10.5), is_blockquote=True)
                continue

            m_num = re.match(r"^(\d+)\.\s+(.*)$", raw_inside)
            if m_num:
                p = doc.add_paragraph(style="List Number")
                p.paragraph_format.left_indent = Inches(0.5)
                p.paragraph_format.space_before = Pt(1.5)
                p.paragraph_format.space_after = Pt(1.5)
                p.paragraph_format.line_spacing = 1.15
                add_formatted_runs_to_paragraph(p, m_num.group(2), font_size=Pt(10.5), is_blockquote=True)
                continue

            # Đoạn blockquote thông thường
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.35)
            p.paragraph_format.right_indent = Inches(0.2)
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.15
            set_blockquote_borders(p)
            add_formatted_runs_to_paragraph(p, raw_inside, font_size=Pt(10.5), is_blockquote=True)
            continue

        # 5. Xử lý Danh sách không thứ tự (Bullet Lists)
        if stripped.startswith("- ") or stripped.startswith("* "):
            p = doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            add_formatted_runs_to_paragraph(p, stripped[2:], font_size=Pt(11))
            continue

        # 6. Xử lý Danh sách có thứ tự (Numbered Lists)
        m_num = re.match(r"^(\d+)\.\s+(.*)$", stripped)
        if m_num:
            p = doc.add_paragraph(style="List Number")
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.line_spacing = 1.15
            add_formatted_runs_to_paragraph(p, m_num.group(2), font_size=Pt(11))
            continue

        # 7. Đoạn văn chuẩn (Normal Paragraph)
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        add_formatted_runs_to_paragraph(p, stripped, font_size=Pt(11))

    docx_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(docx_path))
    print(f"[uu:docx-stylist] Xuất tài liệu thành công: {docx_path}")

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[2]
    md_file = base_dir / "slide" / "scripts" / "SCRIPT_THUYET_TRINH_TOAN_TEAM_CS106.md"
    docx_file = base_dir / "slide" / "scripts" / "SCRIPT_THUYET_TRINH_TOAN_TEAM_CS106.docx"
    template_file = base_dir / "reports" / "_report_template.docx"

    convert_script_md_to_docx(md_file, docx_file, template_file)
