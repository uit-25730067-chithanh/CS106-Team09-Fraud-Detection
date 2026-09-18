"""
Script chuyển đổi Huong_dan_su_dung.md thành Huong_dan_su_dung.docx chuẩn định dạng.
"""
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_guide_docx(md_path: Path, output_docx: Path):
    doc = docx.Document()

    # Set normal style font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    # Page margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG CHƯƠNG TRÌNH\nĐỒ ÁN TRÍ TUỆ NHÂN TẠO (CS106)")
    run_title.font.name = 'Times New Roman'
    run_title.font.size = Pt(16)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("Đề tài #7: Hệ thống phát hiện giao dịch tài chính bất thường và nghi vấn gian lận\nNhóm 09 — Trường ĐH Công nghệ Thông tin, ĐHQG-HCM")
    run_sub.font.name = 'Times New Roman'
    run_sub.font.size = Pt(12)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    doc.add_paragraph("GitHub Repository: https://github.com/uit-25730067-chithanh/CS106-Team09-Fraud-Detection")

    # Section 1
    h1 = doc.add_heading("1. Yêu cầu Môi trường & Cài đặt", level=1)
    h1.style.font.name = 'Times New Roman'
    h1.style.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    doc.add_paragraph("Chương trình được phát triển và kiểm thử ổn định trên hệ điều hành Windows / Linux / macOS với Python 3.10 trở lên.")
    doc.add_paragraph("Bước 1: Tạo và kích hoạt môi trường ảo (Khuyến nghị):\n"
                      "  python -m venv .venv\n"
                      "  .venv\\Scripts\\Activate.ps1   (trên Windows PowerShell)\n"
                      "  source .venv/bin/activate    (trên Linux / macOS)")
    
    doc.add_paragraph("Bước 2: Cài đặt các thư viện phụ thuộc:\n"
                      "  pip install --upgrade pip\n"
                      "  pip install -r requirements.txt")

    # Section 2
    h2 = doc.add_heading("2. Cấu trúc Mã nguồn & Hoạt động các Module", level=1)
    h2.style.font.name = 'Times New Roman'
    h2.style.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    modules = [
        ("src/preprocessing/data_loader.py", "Lọc tập TRANSFER & CASH_OUT, lấy mẫu phân tầng 200.000 dòng từ 6.36 triệu giao dịch PaySim."),
        ("src/preprocessing/data_splitter.py", "Chia tách tập Train/Test theo tỷ lệ 80/20 phân tầng (Stratified Split), bảo toàn tỷ lệ gian lận."),
        ("src/preprocessing/feature_scaler.py", "Tạo 14 đặc trưng (bổ sung 5 derived features: tỷ lệ số dư, số tiền chuyển sạch tài khoản...), chuẩn hóa StandardScaler chỉ fit trên tập Train (chống rò rỉ dữ liệu)."),
        ("src/preprocessing/imbalance_handler.py", "Áp dụng kỹ thuật SMOTENC (bảo toàn biến nhị phân) và ADASYN chỉ trên tập huấn luyện để cân bằng mẫu."),
        ("src/models/random_forest_model.py", "Huấn luyện Random Forest, dò siêu tham số RandomizedSearchCV, trích xuất Feature Importance."),
        ("src/models/xgboost_model.py", "Huấn luyện Gradient Boosting XGBoost siêu nhanh (41.6s), lưu file native JSON dung lượng 410 KB."),
        ("src/models/autoencoder_model.py", "Mô hình Mạng nơ-ron Autoencoder phát hiện bất thường không giám sát dựa trên Reconstruction MSE."),
        ("src/evaluation/metrics_calculator.py", "Tính toán F1, ROC-AUC, PR-AUC, Precision, Recall."),
        ("src/evaluation/model_comparator.py", "Bảng tổng hợp so sánh chéo 5 biến thể mô hình (xuất báo cáo và đồ thị)."),
        ("demo/app.py", "Giao diện Web trực quan Streamlit UI, hỗ trợ kiểm tra thời gian thực, giao diện Sáng/Tối, định dạng VNĐ và Risk Meter.")
    ]

    t_mod = doc.add_table(rows=1, cols=2)
    t_mod.style = 'Table Grid'
    hdr_cells = t_mod.rows[0].cells
    hdr_cells[0].text = "Module / File"
    hdr_cells[1].text = "Mô tả Hoạt động và Chức năng"
    for cell in hdr_cells:
        set_cell_background(cell, "1F497D")
        for p in cell.paragraphs:
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for path_str, desc in modules:
        row_cells = t_mod.add_row().cells
        row_cells[0].text = path_str
        row_cells[1].text = desc
        for cell in row_cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(10.5)

    # Section 3
    h3 = doc.add_heading("3. Hướng dẫn Chạy Thử nghiệm", level=1)
    h3.style.font.name = 'Times New Roman'
    h3.style.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    doc.add_paragraph("3.1. Khởi chạy Giao diện Demo Streamlit (Khuyến nghị):\n"
                      "Từ thư mục mã nguồn chạy lệnh:\n"
                      "  streamlit run demo/app.py\n"
                      "Trình duyệt sẽ tự động mở tại http://localhost:8501 để tương tác trực tiếp.")

    doc.add_paragraph("3.2. Chạy 6 Notebooks Thực nghiệm Jupyter:\n"
                      "Mở Jupyter Lab / Notebooks và chạy lần lượt từ 01_eda.ipynb đến 06_evaluation_comparison.ipynb. Tất cả đều đã được lưu sẵn kết quả biểu đồ.")

    doc.add_paragraph("3.3. Chạy Kiểm thử Tự động (Tests):\n"
                      "  pytest tests/\n"
                      "Hệ thống đạt 100% tỷ lệ pass (74 tests pass).")

    # Section 4: Summary Table
    h4 = doc.add_heading("4. Bảng Tổng hợp Kết quả Thực nghiệm", level=1)
    h4.style.font.name = 'Times New Roman'
    h4.style.font.color.rgb = RGBColor(0x1F, 0x49, 0x7D)

    results = [
        ("Random Forest", "SMOTENC", "0.9973", "0.9994", "0.9981", "~180s"),
        ("Random Forest", "ADASYN", "0.9966", "0.9992", "0.9974", "~195s"),
        ("XGBoost (Được chọn)", "SMOTENC", "0.9963", "0.9993", "0.9978", "41.6s"),
        ("XGBoost", "ADASYN", "0.9954", "0.9994", "0.9975", "45.2s"),
        ("Autoencoder", "Normal Only", "0.5074", "0.9318", "0.4421", "~90s")
    ]

    t_res = doc.add_table(rows=1, cols=6)
    t_res.style = 'Table Grid'
    res_hdr = t_res.rows[0].cells
    cols = ["Mô hình", "Kỹ thuật", "F1-Score", "ROC-AUC", "PR-AUC", "Thời gian train"]
    for idx, cname in enumerate(cols):
        res_hdr[idx].text = cname
        set_cell_background(res_hdr[idx], "1F497D")
        for p in res_hdr[idx].paragraphs:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.bold = True
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for m, k, f1, auc, pr, t in results:
        r_cells = t_res.add_row().cells
        r_cells[0].text = m
        r_cells[1].text = k
        r_cells[2].text = f1
        r_cells[3].text = auc
        r_cells[4].text = pr
        r_cells[5].text = t
        for idx, cell in enumerate(r_cells):
            for p in cell.paragraphs:
                if idx >= 1:
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(10.5)

    output_docx.parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_docx)
    print(f"[OK] Da tao docx tai: {output_docx}")

if __name__ == "__main__":
    src_md = Path("draft/fraud-detection/docs/Huong_dan_su_dung.md")
    dest_docx = Path("draft/fraud-detection/docs/Huong_dan_su_dung.docx")
    create_guide_docx(src_md, dest_docx)
