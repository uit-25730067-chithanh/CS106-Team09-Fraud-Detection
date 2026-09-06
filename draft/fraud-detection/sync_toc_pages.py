"""Phase 07: Đọc số trang thật của từng mục từ bản PDF đã xuất.

Mục lục trong bản Word là bảng tĩnh nên số trang phải lấy ngược từ PDF. Script
mở PDF, tìm vị trí đầu tiên của mỗi tiêu đề trong phần thân rồi ghi ra
`reports/_toc_pages.json` để `build_report.py` dựng lại mục lục có số trang.

Quy trình đầy đủ:
    python build_report.py        # lần 1, mục lục chưa có số trang
    <xuất PDF từ bản Word>
    python sync_toc_pages.py      # đọc số trang từ PDF
    python build_report.py        # lần 2, mục lục đã có số trang
    <xuất PDF lần cuối>

Author: Vũ Văn Duy
"""
import json
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

import pymupdf

from build_report import SOURCE_MD, TOC_PAGES, collect_toc_entries, parse_markdown

REPORTS_DIR = os.path.dirname(TOC_PAGES)
PDF_PATH = os.path.join(REPORTS_DIR, "[Nhom9]_BaoCao_FraudDetection_Sprint3_Duy.pdf")
# Mặc định trang bắt đầu phần thân nếu không tìm thấy tiêu đề Chương 1.
DEFAULT_BODY_START_PAGE = 4


def find_heading_pages(pdf_path: str, entries: list[dict]) -> dict[str, int]:
    pages: dict[str, int] = {}
    with pymupdf.open(pdf_path) as document:
        # Tự động phát hiện trang bắt đầu phần thân (Chương 1) thay vì gán cứng
        start_page = DEFAULT_BODY_START_PAGE - 1
        for page_idx in range(document.page_count):
            if document[page_idx].search_for("CHƯƠNG 1. GIỚI THIỆU", quads=False):
                start_page = page_idx
                break

        for entry in entries:
            for page_number in range(start_page, document.page_count):
                if document[page_number].search_for(entry["text"], quads=False):
                    pages[entry["text"]] = page_number + 1
                    break
    return pages


def main() -> None:
    print("=== Phase 07: Đồng bộ số trang mục lục ===")

    if not os.path.exists(PDF_PATH):
        raise SystemExit(f"Chưa có PDF để đọc: {PDF_PATH}")

    with open(SOURCE_MD, encoding="utf-8") as f:
        entries = collect_toc_entries(parse_markdown(f.read()))

    pages = find_heading_pages(PDF_PATH, entries)
    missing = [entry["text"] for entry in entries if entry["text"] not in pages]

    with open(TOC_PAGES, "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

    print(f"Đã tìm thấy {len(pages)}/{len(entries)} mục -> reports/_toc_pages.json")
    if missing:
        print("Không tìm thấy trang cho:")
        for text in missing:
            print(f"  - {text}")


if __name__ == "__main__":
    main()
