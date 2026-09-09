"""Phase 07: Dựng bản Word của báo cáo từ `reports/report-source.md`.

Script giữ đúng định dạng đã chốt ở Sprint 2 bằng cách dùng
`reports/_report_template.docx` làm khuôn: template chỉ chứa styles, header,
footer, khổ giấy A4 và lề, phần thân hoàn toàn rỗng. Nhờ vậy mỗi lần source
thay đổi chỉ cần chạy lại script, không phải chỉnh tay trong Word.

Mục lục được sinh tự động từ các heading cấp 1 và cấp 2. Số trang lấy từ
`reports/_toc_pages.json`. Tệp đó do `sync_toc_pages.py` đọc ngược từ bản PDF
đã xuất, nên quy trình đầy đủ là: dựng DOCX, xuất PDF, đồng bộ số trang, dựng
lại DOCX rồi xuất PDF lần cuối.

Cách dùng:
    python build_report.py

Author: Vũ Văn Duy (Modularized for Sprint 3 PM Audit)
"""

import json
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.reporting import build_document, collect_toc_entries, parse_markdown

REPORTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
SOURCE_MD = os.path.join(REPORTS_DIR, "report-source.md")
TEMPLATE = os.path.join(REPORTS_DIR, "_report_template.docx")
TOC_PAGES = os.path.join(REPORTS_DIR, "_toc_pages.json")
OUTPUT = os.path.join(REPORTS_DIR, "[Nhom9]_BaoCao_FraudDetection_Sprint3_Duy.docx")
FINAL_OUTPUT = os.path.join(REPORTS_DIR, "[Nhom9]_BaoCao_FraudDetection.docx")


def build(blocks: list[dict], pages: dict[str, int]):
    """Wrapper tương thích ngược gọi hàm dựng tài liệu từ module reporting."""
    return build_document(blocks, pages, template_path=TEMPLATE, reports_dir=REPORTS_DIR)


def main() -> None:
    print("=== Phase 07: Dựng bản Word từ report-source.md ===")

    with open(SOURCE_MD, encoding="utf-8") as f:
        blocks = parse_markdown(f.read())

    pages: dict[str, int] = {}
    if os.path.exists(TOC_PAGES):
        with open(TOC_PAGES, encoding="utf-8") as f:
            pages = json.load(f)
        print(f"Đã nạp số trang mục lục: {len(pages)} mục")
    else:
        print("Chưa có _toc_pages.json — mục lục sẽ để trống số trang")

    document = build(blocks, pages)
    document.save(OUTPUT)
    document.save(FINAL_OUTPUT)

    counts = {
        "paragraphs": len(document.paragraphs),
        "tables": len(document.tables),
        "toc entries": len(collect_toc_entries(blocks)),
    }
    print("Saved -> reports/" + os.path.basename(OUTPUT))
    print("Saved -> reports/" + os.path.basename(FINAL_OUTPUT))
    print("  " + " | ".join(f"{key}: {value}" for key, value in counts.items()))

    sprint3_pdf = os.path.join(REPORTS_DIR, "[Nhom9]_BaoCao_FraudDetection_Sprint3_Duy.pdf")
    final_pdf = os.path.join(REPORTS_DIR, "[Nhom9]_BaoCao_FraudDetection.pdf")
    if os.path.exists(sprint3_pdf):
        import shutil
        shutil.copy2(sprint3_pdf, final_pdf)
        print("Synced -> reports/" + os.path.basename(final_pdf))


if __name__ == "__main__":
    main()
