#!/usr/bin/env python3
"""
Generate UIT Academic Huong_dan_su_dung.docx using report styling.
Clones document setup and styles from assignments/Final/draft/fraud-detection/reports/[Nhom9]_BaoCao_FraudDetection.docx
Ensures 100% Times New Roman, pure black #000000, academic booktabs tables (F2F2F2 header, CCCCCC borders),
and verified content.
"""

import os
from pathlib import Path
import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

BLACK = RGBColor(0, 0, 0)

def set_cell_margins(cell, top=60, bottom=60, left=120, right=120):
    """Set cell padding in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex="F2F2F2"):
    """Set cell background fill color."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}" w:val="clear"/>')
    tcPr.append(shd)

def apply_booktabs_borders(table, border_color="CCCCCC", top_sz="8", bottom_sz="8", inside_sz="4"):
    """Apply UIT academic booktabs style borders (horizontal only)."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="{top_sz}" w:space="0" w:color="{border_color}"/>
            <w:bottom w:val="single" w:sz="{bottom_sz}" w:space="0" w:color="{border_color}"/>
            <w:insideH w:val="single" w:sz="{inside_sz}" w:space="0" w:color="{border_color}"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_code_block(doc, code_text):
    """Add a clean monospace code paragraph block (without table)."""
    for i, line in enumerate(code_text.splitlines()):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.35)
        p.paragraph_format.space_before = Pt(2) if i == 0 else Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(line)
        r.font.name = "Courier New"
        r.font.size = Pt(9.5)
        if line.strip().startswith("#"):
            r.font.color.rgb = RGBColor(100, 100, 100)
            r.italic = True
        else:
            r.font.color.rgb = BLACK
            r.bold = True

def create_guide_docx(template_path: str, output_path: str):
    doc = docx.Document(template_path)

    # Clear existing paragraphs and tables
    for table in list(doc.tables):
        table._element.getparent().remove(table._element)
    for p in list(doc.paragraphs):
        p._element.getparent().remove(p._element)

    # Set page margins to standard A4 (18mm top/bottom, 22mm left/right)
    section = doc.sections[0]
    section.top_margin = Inches(0.70)     # ~18mm
    section.bottom_margin = Inches(0.70)  # ~18mm
    section.left_margin = Inches(0.85)    # ~22mm
    section.right_margin = Inches(0.85)   # ~22mm
    section.page_width = Inches(8.27)     # 210mm
    section.page_height = Inches(11.69)   # 297mm

    # Configure Header / Footer
    header = section.header
    header.is_linked_to_previous = False
    hp = header.paragraphs[0]
    hp.text = "Trường ĐH Công nghệ Thông tin, ĐHQG-HCM | Môn Trí tuệ Nhân tạo (CS106)"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if hp.runs:
        hp.runs[0].font.name = "Times New Roman"
        hp.runs[0].font.size = Pt(8.5)
        hp.runs[0].font.color.rgb = RGBColor(120, 120, 120)

    footer = section.footer
    footer.is_linked_to_previous = False
    fp = footer.paragraphs[0]
    fp.text = "Nhóm 09 — Hướng dẫn cài đặt và sử dụng chương trình Fraud Shield"
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if fp.runs:
        fp.runs[0].font.name = "Times New Roman"
        fp.runs[0].font.size = Pt(8.5)
        fp.runs[0].font.color.rgb = RGBColor(120, 120, 120)

    # --- 1. INSTITUTIONAL HEADER ---
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(1)
    p_inst.paragraph_format.line_spacing = 1.10
    
    r1 = p_inst.add_run("ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH\nTRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN\n")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(10.5)
    r1.font.bold = True
    r1.font.color.rgb = BLACK

    r2 = p_inst.add_run("KHOA KHOA HỌC MÁY TÍNH\n")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(10.5)
    r2.font.bold = True
    r2.font.color.rgb = BLACK

    r3 = p_inst.add_run("-o0o-")
    r3.font.name = "Times New Roman"
    r3.font.size = Pt(9.5)
    r3.font.color.rgb = BLACK

    # --- 2. DOCUMENT TITLE ---
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(2)
    p_title.paragraph_format.line_spacing = 1.15

    rt1 = p_title.add_run("HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG CHƯƠNG TRÌNH\n")
    rt1.font.name = "Times New Roman"
    rt1.font.size = Pt(14.0)
    rt1.font.bold = True
    rt1.font.color.rgb = BLACK

    rt2 = p_title.add_run("MÔN HỌC: TRÍ TUỆ NHÂN TẠO (CS106) — ĐỀ TÀI SỐ 7\n")
    rt2.font.name = "Times New Roman"
    rt2.font.size = Pt(11.5)
    rt2.font.bold = True
    rt2.font.color.rgb = BLACK

    rt3 = p_title.add_run("Hệ thống phát hiện giao dịch tài chính bất thường và nghi vấn gian lận\n")
    rt3.font.name = "Times New Roman"
    rt3.font.size = Pt(11.0)
    rt3.italic = True
    rt3.font.color.rgb = BLACK

    rt4 = p_title.add_run("Nhóm 09 — Lớp CS106.F31.CN2.TTNT — GVHD: PGS.TS. Nguyễn Đình Hiển")
    rt4.font.name = "Times New Roman"
    rt4.font.size = Pt(10.5)
    rt4.font.color.rgb = BLACK

    # Links block
    p_link = doc.add_paragraph()
    p_link.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_link.paragraph_format.space_before = Pt(2)
    p_link.paragraph_format.space_after = Pt(6)
    
    rl1 = p_link.add_run("Mã nguồn GitHub chính thức: ")
    rl1.font.name = "Times New Roman"
    rl1.font.size = Pt(9.5)
    rl1.font.bold = True
    rl1.font.color.rgb = BLACK
    
    rl2 = p_link.add_run("https://github.com/uit-25730067-chithanh/CS106-Team09-Fraud-Detection\n")
    rl2.font.name = "Times New Roman"
    rl2.font.size = Pt(9.5)
    rl2.underline = True
    rl2.font.color.rgb = BLACK

    rl3 = p_link.add_run("Video Clip Demo trực tiếp: ")
    rl3.font.name = "Times New Roman"
    rl3.font.size = Pt(9.5)
    rl3.font.bold = True
    rl3.font.color.rgb = BLACK

    rl4 = p_link.add_run("https://aceteam-uit.vercel.app/l/70vGyu")
    rl4.font.name = "Times New Roman"
    rl4.font.size = Pt(9.5)
    rl4.underline = True
    rl4.font.color.rgb = BLACK

    rl5 = p_link.add_run(" (Thời lượng chính thức: 1 phút 37 giây)")
    rl5.font.name = "Times New Roman"
    rl5.font.size = Pt(9.5)
    rl5.italic = True
    rl5.font.color.rgb = BLACK

    # --- SECTION 1 ---
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(8)
    h1.paragraph_format.space_after = Pt(4)
    h1.paragraph_format.keep_with_next = True
    r = h1.add_run("1. YÊU CẦU MÔI TRƯỜNG & CÀI ĐẶT")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13.0)
    r.font.bold = True
    r.font.color.rgb = BLACK

    p1 = doc.add_paragraph()
    p1.paragraph_format.space_before = Pt(2)
    p1.paragraph_format.space_after = Pt(4)
    p1.paragraph_format.line_spacing = 1.15
    r = p1.add_run("Chương trình được phát triển, tối ưu và kiểm thử ổn định trên hệ điều hành Windows, Linux và macOS với Python phiên bản 3.10 trở lên. Quá trình thiết lập môi trường thực nghiệm được thực hiện theo các bước tuần tự sau:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.0)
    r.font.color.rgb = BLACK

    p_step1 = doc.add_paragraph()
    p_step1.paragraph_format.space_before = Pt(4)
    p_step1.paragraph_format.space_after = Pt(2)
    p_step1.paragraph_format.keep_with_next = True
    r = p_step1.add_run("Bước 1: Khởi tạo và kích hoạt môi trường ảo (Khuyến nghị):")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.0)
    r.font.bold = True
    r.font.color.rgb = BLACK

    add_code_block(doc, "python -m venv .venv\n# Trên Windows PowerShell:  .venv\\Scripts\\Activate.ps1\n# Trên Linux / macOS:      source .venv/bin/activate")

    p_step2 = doc.add_paragraph()
    p_step2.paragraph_format.space_before = Pt(6)
    p_step2.paragraph_format.space_after = Pt(2)
    p_step2.paragraph_format.keep_with_next = True
    r = p_step2.add_run("Bước 2: Cài đặt danh mục thư viện phụ thuộc:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.0)
    r.font.bold = True
    r.font.color.rgb = BLACK

    add_code_block(doc, "pip install --upgrade pip\npip install -r requirements.txt")

    # --- SECTION 2 ---
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(12)
    h2.paragraph_format.space_after = Pt(4)
    h2.paragraph_format.keep_with_next = True
    r = h2.add_run("2. CẤU TRÚC MÃ NGUỒN VÀ CHỨC NĂNG MODULE")
    r.font.name = "Times New Roman"
    r.font.size = Pt(13.0)
    r.font.bold = True
    r.font.color.rgb = BLACK

    p2 = doc.add_paragraph()
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(4)
    p2.paragraph_format.line_spacing = 1.15
    r = p2.add_run("Toàn bộ mã nguồn giải thuật học máy và ứng dụng tương tác được tổ chức chặt chẽ theo nguyên tắc module hóa cao trong thư mục Chuong_trinh/code/src/ và Chuong_trinh/demo/:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.0)
    r.font.color.rgb = BLACK

    p_tb1_caption = doc.add_paragraph()
    p_tb1_caption.paragraph_format.space_before = Pt(4)
    p_tb1_caption.paragraph_format.space_after = Pt(3)
    p_tb1_caption.paragraph_format.keep_with_next = True
    r = p_tb1_caption.add_run("Bảng 1: Danh mục chức năng các module chính trong chương trình")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.italic = True
    r.font.bold = True
    r.font.color.rgb = BLACK

    modules_data = [
        ("src/preprocessing/data_loader.py", "Lọc hai loại giao dịch TRANSFER & CASH_OUT, lấy mẫu phân tầng 200.000 dòng từ 6.36 triệu giao dịch PaySim gốc."),
        ("src/preprocessing/data_splitter.py", "Chia tách tập Train/Test theo tỷ lệ 80/20 phân tầng (Stratified Split), bảo toàn nguyên vẹn tỷ lệ mẫu gian lận."),
        ("src/preprocessing/feature_scaler.py", "Xây dựng 14 đặc trưng (bổ sung 5 biến dẫn xuất), chuẩn hóa StandardScaler chỉ fit trên Train set để chống rò rỉ dữ liệu."),
        ("src/preprocessing/imbalance_handler.py", "Áp dụng kỹ thuật tái cân bằng SMOTENC (bảo toàn biến rời rạc) và ADASYN trên tập huấn luyện, không can thiệp tập test."),
        ("src/models/random_forest_model.py", "Huấn luyện Random Forest, tối ưu siêu tham số RandomizedSearchCV và trích xuất độ quan trọng đặc trưng (Feature Importance)."),
        ("src/models/xgboost_model.py", "Huấn luyện mô hình Gradient Boosting XGBoost tốc độ cao, hỗ trợ lưu và nạp mô hình qua định dạng native JSON (xgb_smote.json)."),
        ("src/models/autoencoder_model.py", "Xây dựng và huấn luyện Mạng nơ-ron Autoencoder phát hiện bất thường không giám sát dựa trên sai số tái tạo (Reconstruction MSE)."),
        ("src/evaluation/metrics_calculator.py", "Tính toán toàn diện các độ đo F1-Score, Precision, Recall, ROC-AUC, PR-AUC và ma trận nhầm lẫn (Confusion Matrix)."),
        ("src/evaluation/model_comparator.py", "Tổng hợp kết quả thực nghiệm, đối sánh chéo 5 biến thể mô hình và xuất biểu đồ so sánh chi tiết."),
        ("demo/app.py", "Ứng dụng Web trực quan Streamlit Fraud Shield: hỗ trợ kiểm tra thời gian thực 3 kịch bản, định dạng tiền tệ VNĐ và Risk Meter."),
    ]

    t1 = doc.add_table(rows=len(modules_data) + 1, cols=2)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_booktabs_borders(t1, border_color="CCCCCC", top_sz="8", bottom_sz="8", inside_sz="4")

    # Header
    col_widths_1 = [Inches(2.5), Inches(4.0)]
    headers_1 = ["Module / File", "Mô tả Hoạt động và Chức năng"]
    for j, h_txt in enumerate(headers_1):
        cell = t1.cell(0, j)
        cell.width = col_widths_1[j]
        set_cell_margins(cell, top=50, bottom=50, left=100, right=100)
        set_cell_shading(cell, "F2F2F2")
        cp = cell.paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_before = Pt(1)
        cp.paragraph_format.space_after = Pt(1)
        r = cp.add_run(h_txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = BLACK

    for i, (mod, desc) in enumerate(modules_data):
        row = t1.rows[i + 1]
        
        c0 = row.cells[0]
        c0.width = col_widths_1[0]
        set_cell_margins(c0, top=35, bottom=35, left=80, right=80)
        cp0 = c0.paragraphs[0]
        cp0.paragraph_format.space_before = Pt(0)
        cp0.paragraph_format.space_after = Pt(0)
        cp0.paragraph_format.line_spacing = 1.10
        r0 = cp0.add_run(mod)
        r0.font.name = "Courier New"
        r0.font.size = Pt(8.5)
        r0.font.bold = True
        r0.font.color.rgb = BLACK

        c1 = row.cells[1]
        c1.width = col_widths_1[1]
        set_cell_margins(c1, top=35, bottom=35, left=80, right=80)
        cp1 = c1.paragraphs[0]
        cp1.paragraph_format.space_before = Pt(0)
        cp1.paragraph_format.space_after = Pt(0)
        cp1.paragraph_format.line_spacing = 1.10
        r1 = cp1.add_run(desc)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(9.0)
        r1.font.color.rgb = BLACK

    # --- SECTION 3 ---
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(8)
    h3.paragraph_format.space_after = Pt(2)
    h3.paragraph_format.keep_with_next = True
    r = h3.add_run("3. HƯỚNG DẪN THỰC THI CHƯƠNG TRÌNH")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12.5)
    r.font.bold = True
    r.font.color.rgb = BLACK

    # 3.1
    h31 = doc.add_paragraph()
    h31.paragraph_format.space_before = Pt(3)
    h31.paragraph_format.space_after = Pt(1)
    h31.paragraph_format.keep_with_next = True
    r = h31.add_run("3.1. Chạy 6 Notebooks Thực nghiệm Jupyter (Phương thức Thẩm định Chính)")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.0)
    r.font.bold = True
    r.font.color.rgb = BLACK

    p31 = doc.add_paragraph()
    p31.paragraph_format.space_before = Pt(1)
    p31.paragraph_format.space_after = Pt(3)
    p31.paragraph_format.line_spacing = 1.10
    r = p31.add_run("Quý Thầy/Cô mở Jupyter Lab hoặc Visual Studio Code và thực thi lần lượt 6 cuốn sổ tay từ ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    r_c = p31.add_run("01_eda.ipynb")
    r_c.font.name = "Courier New"
    r_c.font.size = Pt(9.0)
    r_c.font.bold = True
    r_c.font.color.rgb = BLACK

    r = p31.add_run(" đến ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    r_c2 = p31.add_run("06_evaluation_comparison.ipynb")
    r_c2.font.name = "Courier New"
    r_c2.font.size = Pt(9.0)
    r_c2.font.bold = True
    r_c2.font.color.rgb = BLACK

    r = p31.add_run(" trong thư mục Chuong_trinh/code/notebooks/. Toàn bộ 6 notebooks đều đã được chạy sạch (Clean Run) và lưu sẵn toàn bộ đầu ra biểu đồ, chỉ số thực nghiệm.")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    # 3.2
    h32 = doc.add_paragraph()
    h32.paragraph_format.space_before = Pt(4)
    h32.paragraph_format.space_after = Pt(1)
    h32.paragraph_format.keep_with_next = True
    r = h32.add_run("3.2. Xem Minh chứng Video Clip Thuyết minh Demo Giao diện")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.0)
    r.font.bold = True
    r.font.color.rgb = BLACK

    p32 = doc.add_paragraph()
    p32.paragraph_format.space_before = Pt(1)
    p32.paragraph_format.space_after = Pt(3)
    p32.paragraph_format.line_spacing = 1.10
    r = p32.add_run("Quý Thầy/Cô có thể theo dõi video clip thuyết minh trực quan giao diện tương tác Streamlit Web UI (độ phân giải Full HD 1080p, thời lượng chuẩn 1 phút 37 giây do sinh viên Phạm Thành Trung trình bày) qua liên kết truy cập công khai tại tệp ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    r_link_f = p32.add_run("Chuong_trinh/demo/Link_video_demo.txt")
    r_link_f.font.name = "Courier New"
    r_link_f.font.size = Pt(9.0)
    r_link_f.font.bold = True
    r_link_f.font.color.rgb = BLACK

    r = p32.add_run(" hoặc xem tại Trang 20 trong tệp trình chiếu ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    r_slide = p32.add_run("Bao_cao/[Nhom9]_Slide_FraudDetection.pdf")
    r_slide.font.name = "Courier New"
    r_slide.font.size = Pt(9.0)
    r_slide.font.bold = True
    r_slide.font.color.rgb = BLACK

    r = p32.add_run(".")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    # 3.3
    h33 = doc.add_paragraph()
    h33.paragraph_format.space_before = Pt(4)
    h33.paragraph_format.space_after = Pt(1)
    h33.paragraph_format.keep_with_next = True
    r = h33.add_run("3.3. Khởi chạy Ứng dụng Web Demo Streamlit tại Máy Cục bộ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11.0)
    r.font.bold = True
    r.font.color.rgb = BLACK

    p33 = doc.add_paragraph()
    p33.paragraph_format.space_before = Pt(1)
    p33.paragraph_format.space_after = Pt(2)
    p33.paragraph_format.line_spacing = 1.10
    r = p33.add_run("Để trực tiếp trải nghiệm ứng dụng Web giao diện Fraud Shield bằng mô hình XGBoost-SMOTE đã huấn luyện sẵn, mở Terminal tại thư mục Chuong_trinh/ và thực hiện lệnh:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    add_code_block(doc, "cd Chuong_trinh\nstreamlit run demo/app.py")

    p33_note = doc.add_paragraph()
    p33_note.paragraph_format.space_before = Pt(3)
    p33_note.paragraph_format.space_after = Pt(3)
    p33_note.paragraph_format.line_spacing = 1.10
    r = p33_note.add_run("Hệ thống sẽ tự động khởi tạo dịch vụ Web cục bộ tại địa chỉ ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    r_url = p33_note.add_run("http://localhost:8501")
    r_url.font.name = "Courier New"
    r_url.font.size = Pt(9.0)
    r_url.font.bold = True
    r_url.font.color.rgb = BLACK

    r = p33_note.add_run(" với đầy đủ tính năng thử nghiệm trực tiếp 3 kịch bản giao dịch (Hợp lệ, Cần lưu ý, Nghi vấn gian lận).")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    # --- SECTION 4 ---
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(8)
    h4.paragraph_format.space_after = Pt(2)
    h4.paragraph_format.keep_with_next = True
    r = h4.add_run("4. BẢNG TỔNG HỢP KẾT QUẢ THỰC NGHIỆM")
    r.font.name = "Times New Roman"
    r.font.size = Pt(12.5)
    r.font.bold = True
    r.font.color.rgb = BLACK

    p4 = doc.add_paragraph()
    p4.paragraph_format.space_before = Pt(1)
    p4.paragraph_format.space_after = Pt(2)
    p4.paragraph_format.line_spacing = 1.10
    r = p4.add_run("Kết quả đối sánh thực nghiệm của 5 biến thể mô hình trên cùng tập dữ liệu kiểm tra 40.000 giao dịch PaySim được tổng hợp tại Bảng 2:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.5)
    r.font.color.rgb = BLACK

    p_tb2_caption = doc.add_paragraph()
    p_tb2_caption.paragraph_format.space_before = Pt(2)
    p_tb2_caption.paragraph_format.space_after = Pt(2)
    p_tb2_caption.paragraph_format.keep_with_next = True
    r = p_tb2_caption.add_run("Bảng 2: So sánh hiệu năng phát hiện gian lận giữa các mô hình thử nghiệm")
    r.font.name = "Times New Roman"
    r.font.size = Pt(10.0)
    r.italic = True
    r.font.bold = True
    r.font.color.rgb = BLACK

    models_data = [
        ("Random Forest", "SMOTENC", "0.9973", "0.9994", "0.9983", "1187 s"),
        ("Random Forest", "ADASYN", "0.9966", "0.9992", "0.9978", "1168 s"),
        ("XGBoost (Được chọn)", "SMOTENC", "0.9963", "0.9993", "0.9969", "57.9 s"),
        ("XGBoost", "ADASYN", "0.9954", "0.9994", "0.9976", "45.5 s"),
        ("Autoencoder", "Normal Only", "0.5069", "0.9318", "0.5973", "~90 s"),
    ]

    t2 = doc.add_table(rows=len(models_data) + 1, cols=6)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    apply_booktabs_borders(t2, border_color="CCCCCC", top_sz="8", bottom_sz="8", inside_sz="4")

    col_widths_2 = [Inches(1.8), Inches(1.3), Inches(0.85), Inches(0.85), Inches(0.85), Inches(0.85)]
    headers_2 = ["Mô hình", "Kỹ thuật Lấy mẫu", "F1-Score", "ROC-AUC", "PR-AUC", "Thời gian"]
    for j, h_txt in enumerate(headers_2):
        cell = t2.cell(0, j)
        cell.width = col_widths_2[j]
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        set_cell_shading(cell, "F2F2F2")
        cp = cell.paragraphs[0]
        cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp.paragraph_format.space_before = Pt(1)
        cp.paragraph_format.space_after = Pt(1)
        r = cp.add_run(h_txt)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.0)
        r.font.bold = True
        r.font.color.rgb = BLACK

    for i, row_data in enumerate(models_data):
        row = t2.rows[i + 1]
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = col_widths_2[j]
            set_cell_margins(cell, top=35, bottom=35, left=60, right=60)
            cp = cell.paragraphs[0]
            cp.paragraph_format.space_before = Pt(0)
            cp.paragraph_format.space_after = Pt(0)
            cp.paragraph_format.line_spacing = 1.10
            if j in (0, 1):
                cp.alignment = WD_ALIGN_PARAGRAPH.LEFT
            else:
                cp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = cp.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.0)
            if "Được chọn" in val:
                r.font.bold = True
            r.font.color.rgb = BLACK

    p_note = doc.add_paragraph()
    p_note.paragraph_format.space_before = Pt(4)
    p_note.paragraph_format.space_after = Pt(2)
    p_note.paragraph_format.line_spacing = 1.10
    r = p_note.add_run("Ghi chú: ")
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = BLACK

    r = p_note.add_run("Mô hình XGBoost kết hợp SMOTENC được lựa chọn để tích hợp vào ứng dụng Demo thực tế nhờ hiệu năng phát hiện gian lận tiệm cận Random Forest (F1-Score đạt 0.9963) nhưng thời gian huấn luyện và độ trễ suy luận nhanh hơn gấp 20 lần.")
    r.font.name = "Times New Roman"
    doc.save(output_path)
    print(f"[✓] Created clean academic DOCX at: {output_path}")

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parents[2]  # assignments/Final
    template = base_dir / "draft/fraud-detection/reports/[Nhom9]_Report_FraudDetection.docx"
    
    out_tmp = base_dir.parent.parent / "tmp/Huong_dan_su_dung.docx"
    out_tmp.parent.mkdir(parents=True, exist_ok=True)
    create_guide_docx(str(template), str(out_tmp))
