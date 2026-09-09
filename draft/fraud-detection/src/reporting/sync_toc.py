"""
Two-way TOC Page Synchronizer for UIT Academic Documents.
Scans compiled PDF using PyMuPDF (fitz) to extract the exact physical body page numbers
where chapters and headings appear, taking into account page number restarts at Section 3 (Body).
"""

from __future__ import annotations

import os
import re
import json


def clean_search_title(title: str) -> str:
    """Clean markdown markers and excessive whitespace for reliable PDF text matching."""
    text = re.sub(r'[*_`#]', '', title)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'—', ' - ', text)
    text = re.sub(r'–', '-', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_toc_page_mapping(pdf_path: str, toc_entries: list[dict]) -> dict[str, int]:
    """
    Search for each TOC entry title in the PDF and record its body-relative page number.
    Returns a dict mapping entry['text'] -> page_number (int).
    """
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    page_texts = [doc[i].get_text("text") for i in range(total_pages)]

    # Detect body start (typically where TÓM TẮT or CHƯƠNG 1 appears in body after TOC)
    first_entry_text = clean_search_title(toc_entries[0]["text"]) if toc_entries else ""
    first_body_pdf_page = 0

    for p_idx in range(total_pages):
        text = page_texts[p_idx]
        if "MỤC LỤC" in text and p_idx < 3:
            continue
        if first_entry_text and first_entry_text.lower() in text.lower():
            first_body_pdf_page = p_idx
            break

    if first_body_pdf_page == 0 and total_pages > 2:
        first_body_pdf_page = 2  # Cover is 0, TOC is 1, Body starts at index 2

    print(f"[*] Detected body start at PDF page index {first_body_pdf_page + 1} (Page 1 of body)")

    mapping: dict[str, int] = {}
    current_search_page = first_body_pdf_page

    for entry in toc_entries:
        raw_title = entry["text"]
        search_query = clean_search_title(raw_title)

        short_query = search_query
        if ":" in search_query:
            short_query = search_query.split(":")[0].strip()
        elif "." in search_query and len(search_query) > 35:
            short_query = search_query[:35].strip()

        found_page = None
        for p_idx in range(current_search_page, total_pages):
            p_text = page_texts[p_idx]
            if (search_query.lower() in p_text.lower()) or (short_query.lower() in p_text.lower()):
                found_page = (p_idx - first_body_pdf_page) + 1
                current_search_page = p_idx
                break

        if found_page is None:
            for p_idx in range(first_body_pdf_page, total_pages):
                p_text = page_texts[p_idx]
                if (search_query.lower() in p_text.lower()) or (short_query.lower() in p_text.lower()):
                    found_page = (p_idx - first_body_pdf_page) + 1
                    break

        if found_page is not None:
            mapping[raw_title] = max(1, found_page)
        else:
            last_page = max(mapping.values()) if mapping else 1
            mapping[raw_title] = last_page

    doc.close()
    return mapping
