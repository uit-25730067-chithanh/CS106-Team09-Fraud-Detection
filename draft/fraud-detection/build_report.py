"""
Phase 07: Biên dịch Báo cáo Đồ án CS106 theo Chuẩn Học thuật UIT.
Bao gồm:
- Trang bìa chuẩn Phụ lục 1: hoa văn khung viền đen triple border, logo UIT, đề tài, GVHD PGS.TS. Nguyễn Đình Hiển, 7 sinh viên Nhóm 9.
- Mục lục chuẩn Phụ lục 2: tab dot-leader và liên kết tương tác (clickable hyperlinks) nhảy đến từng chương/mục.
- Thân bài: lề 2-2-3-2 cm (gáy sách 3.0cm), Times New Roman 13pt, 1.3 line spacing, 100% chữ đen (#000000).
- Trích dẫn [1]-[8] tương tác: click nhảy trực tiếp đến danh mục tài liệu tham khảo.
- Tự động hóa đồng bộ số trang hai chiều (2-way PyMuPDF TOC sync) và xuất PDF chuẩn qua Microsoft Word AppleScript.
"""

from __future__ import annotations

import json
import os
import shutil
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.reporting.docx_table_builder import add_styled_table
from src.reporting.pdf_exporter import export_docx_to_pdf
from src.reporting.report_builder import build_document
from src.reporting.sync_toc import extract_toc_page_mapping
from src.reporting.toc_generator import collect_toc_entries

REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
SOURCE_MD = os.path.join(REPORTS_DIR, "report-source.md")
META_YAML = os.path.join(REPORTS_DIR, "report-meta.yaml")
TOC_PAGES = os.path.join(REPORTS_DIR, "_toc_pages.json")
TEMPLATE = os.path.join(REPORTS_DIR, "_report_template.docx")

OUTPUT_DOCX = os.path.join(REPORTS_DIR, "[Nhom9]_BaoCao_FraudDetection.docx")
OUTPUT_PDF = os.path.join(REPORTS_DIR, "[Nhom9]_BaoCao_FraudDetection.pdf")


def main() -> None:
    print("=== Phase 07: Dựng bản Word & PDF Báo cáo theo Chuẩn Học thuật UIT ===")

    # 1. Đọc số trang mục lục đã lưu (nếu có)
    pages: dict[str, int] = {}
    if os.path.exists(TOC_PAGES):
        try:
            with open(TOC_PAGES, encoding="utf-8") as f:
                pages = json.load(f)
            print(f"[*] Đã nạp số trang mục lục hiện có: {len(pages)} mục")
        except Exception as e:
            print(f"[!] Không đọc được {TOC_PAGES}: {e}")

    # 2. Biên dịch DOCX lượt 1
    print("[*] Đang biên dịch bản Word (DOCX)...")
    doc = build_document(SOURCE_MD, OUTPUT_DOCX, meta_path=META_YAML, page_mapping=pages)
    print(f"[✓] Đã tạo DOCX: reports/{os.path.basename(OUTPUT_DOCX)}")

    # 3. Xuất PDF lượt 1 để đo số trang thực tế
    print("[*] Đang xuất PDF qua Microsoft Word để đồng bộ số trang...")
    pdf_ok = export_docx_to_pdf(OUTPUT_DOCX, OUTPUT_PDF)

    if pdf_ok:
        print(f"[✓] Đã xuất PDF: reports/{os.path.basename(OUTPUT_PDF)}")

        # 4. Trích xuất số trang chính xác qua PyMuPDF
        print("[*] Đang quét số trang từng chương/mục qua PyMuPDF...")
        with open(SOURCE_MD, encoding="utf-8") as f:
            lines = f.read().splitlines()
        toc_entries = collect_toc_entries(lines)

        try:
            new_mapping = extract_toc_page_mapping(OUTPUT_PDF, toc_entries)
            with open(TOC_PAGES, "w", encoding="utf-8") as f:
                json.dump(new_mapping, f, ensure_ascii=False, indent=2)
            print(f"[✓] Đã đồng bộ {len(new_mapping)} mục vào reports/_toc_pages.json")

            # 5. Tái biên dịch DOCX với số trang chuẩn
            print("[*] Tái biên dịch DOCX với số trang mục lục khớp 100%...")
            doc = build_document(SOURCE_MD, OUTPUT_DOCX, meta_path=META_YAML, page_mapping=new_mapping)

            # 6. Tái xuất PDF lần cuối
            print("[*] Xuất bản PDF chính thức lần cuối...")
            export_docx_to_pdf(OUTPUT_DOCX, OUTPUT_PDF)
            print(f"[✓] Hoàn tất xuất bản PDF chính thức: reports/{os.path.basename(OUTPUT_PDF)}")
        except Exception as e:
            print(f"[!] Lỗi trong quá trình đồng bộ số trang: {e}")

    # 7. Đồng bộ sang thư mục submit nếu có
    submit_report_dir = os.path.abspath(os.path.join(REPORTS_DIR, "..", "..", "submit", "report"))
    if os.path.exists(submit_report_dir):
        shutil.copy2(OUTPUT_DOCX, os.path.join(submit_report_dir, os.path.basename(OUTPUT_DOCX)))
        if os.path.exists(OUTPUT_PDF):
            shutil.copy2(OUTPUT_PDF, os.path.join(submit_report_dir, os.path.basename(OUTPUT_PDF)))
        print(f"[✓] Đã đồng bộ sang submit/report/{os.path.basename(OUTPUT_DOCX)}")

    print("\n=== Tổng kết báo cáo ===")
    print(f"- Số đoạn văn (Paragraphs): {len(doc.paragraphs)}")
    print(f"- Số bảng biểu (Tables): {len(doc.tables)}")
    print(f"- DOCX size: {os.path.getsize(OUTPUT_DOCX) / 1024:.1f} KB")
    if os.path.exists(OUTPUT_PDF):
        print(f"- PDF size: {os.path.getsize(OUTPUT_PDF) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
