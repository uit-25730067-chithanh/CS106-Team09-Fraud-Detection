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
# Trang bìa và các trang mục lục (trang 1-3) không được tính là nơi tiêu đề xuất hiện.
BODY_STARTS_AT_PAGE = 4


def find_heading_pages(pdf_path: str, entries: list[dict]) -> dict[str, int]:
    pages: dict[str, int] = {}
    with pymupdf.open(pdf_path) as document:
        for entry in entries:
            # Quét từ trang thân bài (trang 4) trở đi để không bị trùng với chính mục lục
            for page_number in range(BODY_STARTS_AT_PAGE - 1, document.page_count):
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
