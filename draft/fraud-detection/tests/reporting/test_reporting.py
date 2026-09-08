"""Unit tests for the modularized reporting pipeline."""

import pytest

docx = pytest.importorskip("docx")
Document = docx.Document

from src.reporting.docx_table_builder import add_spacer, add_table
from src.reporting.markdown_parser import add_runs, clean_markdown_symbols, parse_markdown
from src.reporting.toc_generator import collect_toc_entries


def test_clean_markdown_symbols() -> None:
    assert clean_markdown_symbols("`code` with $math$") == "code with math"
    assert clean_markdown_symbols("`amount_to_oldbalance_ratio`") == "amount_to_oldbalance_ratio"


def test_parse_markdown_blocks() -> None:
    md_text = """
# Tiêu đề 1

Đoạn văn thường với **in đậm**.

| Cột 1 | Cột 2 |
|---|---|
| A | B |

- Mục 1
- Mục 2

---
"""
    blocks = parse_markdown(md_text)
    types = [b["type"] for b in blocks]
    assert "h1" in types
    assert "para" in types
    assert "table" in types
    assert "bullet" in types
    assert "pagebreak" in types


def test_collect_toc_entries() -> None:
    blocks = [
        {"type": "h1", "text": "Bìa Báo Cáo"},
        {"type": "h1", "text": "CHƯƠNG 1. GIỚI THIỆU"},
        {"type": "h2", "text": "1.1. Bối cảnh"},
        {"type": "h2", "text": "Mục không đánh số"},
        {"type": "h3", "text": "1.1.1. Chi tiết"},
    ]
    entries = collect_toc_entries(blocks)
    assert len(entries) == 2
    assert entries[0] == {"text": "CHƯƠNG 1. GIỚI THIỆU", "level": 1}
    assert entries[1] == {"text": "1.1. Bối cảnh", "level": 2}


def test_add_table_and_runs() -> None:
    doc = Document()
    p = doc.add_paragraph()
    add_runs(p, "Văn bản **đậm** thường")
    assert len(p.runs) == 3
    assert p.runs[1].bold is True

    table = add_table(doc, ["STT", "Tên"], [["1", "Thử nghiệm"]])
    assert len(table.rows) == 2
    assert len(table.columns) == 2
    assert table.style.name == "Table Grid"

    spacer = add_spacer(doc)
    assert spacer.paragraph_format.line_spacing == 1.0


def test_is_numeric_column_with_unicode_dashes() -> None:
    from src.reporting.docx_table_builder import _is_numeric_column

    rows = [
        ["Random Forest", "0,8985 – 0,9995"],
        ["XGBoost", "0,8281 — 0,9784"],
        ["Autoencoder", "0,0176 - 0,0191"],
    ]
    assert not _is_numeric_column(rows, 0)
    assert _is_numeric_column(rows, 1)


def test_build_document_smoke(tmp_path) -> None:
    from build_report import REPORTS_DIR, TEMPLATE
    from src.reporting.report_builder import build_document

    blocks = [
        {"type": "h1", "text": "Tiêu Đề Bìa Test"},
        {"type": "para", "text": "Tác giả: Nhóm 9"},
        {"type": "pagebreak"},
        {"type": "h1", "text": "CHƯƠNG 1. GIỚI THIỆU"},
        {"type": "para", "text": "Nội dung kiểm thử báo cáo."},
        {"type": "table", "header": ["#", "Chỉ số", "Giá trị"], "rows": [["1", "F1", "0,99"]]},
    ]
    pages = {"CHƯƠNG 1. GIỚI THIỆU": 4}
    doc = build_document(blocks, pages, template_path=TEMPLATE, reports_dir=REPORTS_DIR)
    out_file = tmp_path / "smoke_report.docx"
    doc.save(str(out_file))

    assert out_file.exists()
    assert out_file.stat().st_size > 0

