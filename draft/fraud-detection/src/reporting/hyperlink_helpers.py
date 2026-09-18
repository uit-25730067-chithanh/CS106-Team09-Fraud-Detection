"""Shared hyperlink and bookmark helpers for UIT Academic Documents.

Centralized XML generation for internal bookmark hyperlinks, external web
hyperlinks, bookmark anchors, and dynamic page-number fields.  Both
``report_builder`` and ``toc_generator`` import from here to avoid
duplicated OpenXML construction code.
"""

from __future__ import annotations

import logging

import docx
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import RGBColor

logger = logging.getLogger(__name__)

# Canonical colour constants shared across the reporting package.
COLOR_TEXT_MAIN = RGBColor(0, 0, 0)
COLOR_HEX_BLACK = "000000"


def _escape_xml(text: str) -> str:
    """Escape characters that are invalid inside XML attribute/text nodes."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _run_content_xml(text: str) -> str:
    """Dựng phần nội dung của một run, biến ký tự tab thành phần tử ``<w:tab/>``.

    Ký tự tab nằm thẳng trong ``<w:t>`` không phải là tab theo lược đồ OOXML.
    Word bỏ qua nó nên số trang trong mục lục không nhảy sang mốc tab và mất
    hoàn toàn dãy dấu chấm dẫn. Một số trình xem khác như Pages lại hiển thị
    được, vì vậy lỗi này không lộ ra khi kiểm tra trên bản PDF xuất từ Pages.
    """

    parts = []
    for index, chunk in enumerate(text.split("\t")):
        if index:
            parts.append("<w:tab/>")
        if chunk:
            parts.append(f'<w:t xml:space="preserve">{_escape_xml(chunk)}</w:t>')
    return "".join(parts)


def add_bookmark(paragraph, name: str, bookmark_id: int) -> None:
    """Add a bookmark anchor around a paragraph for internal hyperlink jumping."""
    bm_start = parse_xml(
        f'<w:bookmarkStart {nsdecls("w")} w:id="{bookmark_id}" w:name="{name}"/>'
    )
    bm_end = parse_xml(
        f'<w:bookmarkEnd {nsdecls("w")} w:id="{bookmark_id}"/>'
    )
    paragraph._p.append(bm_start)
    paragraph._p.append(bm_end)


def add_page_number_field(run) -> None:
    """Add a dynamic PAGE number field to a footer run."""
    fld1 = parse_xml(r'<w:fldChar %s w:fldCharType="begin"/>' % nsdecls("w"))
    instr = parse_xml(
        r'<w:instrText %s xml:space="preserve"> PAGE </w:instrText>'
        % nsdecls("w")
    )
    fld2 = parse_xml(r'<w:fldChar %s w:fldCharType="separate"/>' % nsdecls("w"))
    fld3 = parse_xml(r'<w:fldChar %s w:fldCharType="end"/>' % nsdecls("w"))
    run._r.append(fld1)
    run._r.append(instr)
    run._r.append(fld2)
    run._r.append(fld3)


def add_internal_hyperlink(
    paragraph,
    target_anchor: str,
    text: str,
    font_name: str = "Times New Roman",
    font_size: float = 13.0,
    is_bold: bool = False,
    is_italic: bool = False,
    color_hex: str = "000000",
) -> None:
    """Add an internal clickable hyperlink run targeting a bookmark anchor.

    This is the single canonical implementation used by both the TOC
    generator (``build_toc_section``) and the body section builder
    (in-text citation links).
    """
    hl = parse_xml(f'<w:hyperlink {nsdecls("w")} w:anchor="{target_anchor}"/>')
    r = parse_xml(
        f'<w:r {nsdecls("w")}>'
        f"<w:rPr>"
        f'<w:rFonts w:ascii="{font_name}" w:hAnsi="{font_name}"/>'
        f'<w:sz w:val="{int(font_size * 2)}"/>'
        f'{"<w:b/>" if is_bold else ""}'
        f'{"<w:i/>" if is_italic else ""}'
        f'<w:color w:val="{color_hex}"/>'
        f"</w:rPr>"
        f"{_run_content_xml(text)}"
        f"</w:r>"
    )
    hl.append(r)
    paragraph._p.append(hl)


def add_external_hyperlink(
    paragraph,
    url: str,
    text: str | None = None,
    font_name: str = "Times New Roman",
    font_size: float = 12.0,
    is_bold: bool = False,
    is_italic: bool = False,
    color_hex: str = "000000",
    is_underline: bool = True,
) -> None:
    """Add an external clickable web hyperlink in pure black."""
    if text is None:
        text = url
    escaped_text = _escape_xml(text)
    part = paragraph.part
    r_id = part.relate_to(
        url, docx.opc.constants.RELATIONSHIP_TYPE.HYPERLINK, is_external=True
    )

    w_ns = nsdecls("w")
    r_ns = nsdecls("r")
    hl = parse_xml(f'<w:hyperlink {w_ns} {r_ns} r:id="{r_id}"/>')
    bold_tag = "<w:b/>" if is_bold else ""
    italic_tag = "<w:i/>" if is_italic else ""
    u_tag = '<w:u w:val="single"/>' if is_underline else ""
    r = parse_xml(
        f"<w:r {w_ns}>"
        f"<w:rPr>"
        f'<w:rFonts w:ascii="{font_name}" w:hAnsi="{font_name}"/>'
        f'<w:sz w:val="{int(font_size * 2)}"/>'
        f"{bold_tag}"
        f"{italic_tag}"
        f'<w:color w:val="{color_hex}"/>'
        f"{u_tag}"
        f"</w:rPr>"
        f'<w:t xml:space="preserve">{escaped_text}</w:t>'
        f"</w:r>"
    )
    hl.append(r)
    paragraph._p.append(hl)
