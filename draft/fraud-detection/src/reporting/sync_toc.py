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


def normalize_text_for_search(text: str) -> str:
    """Normalize text by removing all markers, punctuation, whitespace for robust matching."""
    return re.sub(r'[*_`#\s–—\.\-:,;()\[\]/]+', '', text).lower()


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

    # Detect body start (first page after cover & TOC where Section 3 body text begins)
    first_body_pdf_page = 0
    for p_idx in range(total_pages):
        text = page_texts[p_idx]
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        # Skip cover page (index 0) and pages with TOC dot leaders or "MỤC LỤC" header
        if p_idx == 0 or any("...." in l or "…" in l for l in lines) or "MỤC LỤC" in text:
            continue
        # The first page after cover and TOC is page 1 of Section 3 (Body)
        first_body_pdf_page = p_idx
        break

    if first_body_pdf_page == 0 and total_pages > 3:
        first_body_pdf_page = 3  # Default fallback if TOC is 2 pages (0=cover, 1=toc1, 2=toc2)

    print(f"[*] Detected body start at PDF page index {first_body_pdf_page + 1} (Page 1 of body)")

    mapping: dict[str, int] = {}
    current_search_page = first_body_pdf_page
    norm_page_texts = [normalize_text_for_search(t) for t in page_texts]

    for entry in toc_entries:
        raw_title = entry["text"]
        norm_query = normalize_text_for_search(raw_title)

        # Extract numbering prefix if present (e.g. 'CHƯƠNG 2', '2.1', '3.6.2')
        m_num = re.match(r"^(chương\s*\d+|\d+(?:\.\d+)+)", raw_title, re.IGNORECASE)
        sec_prefix = m_num.group(1).lower() if m_num else None

        found_page = None

        # 1. Forward search from current_search_page
        for p_idx in range(current_search_page, total_pages):
            lines = [l.strip() for l in page_texts[p_idx].split("\n") if l.strip()]
            if any("...." in l or "…" in l for l in lines):
                continue

            # Exact normalized substring match
            if norm_query in norm_page_texts[p_idx]:
                found_page = (p_idx - first_body_pdf_page) + 1
                current_search_page = p_idx
                break

            # Heading line starting with section number
            if sec_prefix and any(l.lower().startswith(sec_prefix) for l in lines):
                found_page = (p_idx - first_body_pdf_page) + 1
                current_search_page = p_idx
                break

        # 2. Fallback scan from body start if not found forward
        if found_page is None:
            for p_idx in range(first_body_pdf_page, total_pages):
                lines = [l.strip() for l in page_texts[p_idx].split("\n") if l.strip()]
                if any("...." in l or "…" in l for l in lines):
                    continue
                if norm_query in norm_page_texts[p_idx]:
                    found_page = (p_idx - first_body_pdf_page) + 1
                    break
                if sec_prefix and any(l.lower().startswith(sec_prefix) for l in lines):
                    found_page = (p_idx - first_body_pdf_page) + 1
                    break

        if found_page is not None:
            mapping[raw_title] = max(1, found_page)
        else:
            last_page = max(mapping.values()) if mapping else 1
            mapping[raw_title] = last_page

    doc.close()
    return mapping
