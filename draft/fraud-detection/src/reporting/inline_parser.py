"""Inline Markdown-to-DOCX formatter for UIT Academic Documents.

Parses bold, italic, code, citations ``[n]``, markdown web links, and bare
URLs inside a single paragraph, emitting properly styled runs via
``python-docx``.  All output text is guaranteed 100% pure black (#000000).
"""

from __future__ import annotations

import re

from docx.shared import Pt, RGBColor

from .hyperlink_helpers import (
    COLOR_TEXT_MAIN,
    add_external_hyperlink,
    add_internal_hyperlink,
)


def parse_inline_formatting(
    paragraph,
    text: str,
    base_font_name: str = "Times New Roman",
    base_font_size: float = 13.0,
    is_italic: bool = False,
    is_bold: bool = False,
    base_color: RGBColor | None = None,
) -> None:
    """Parse inline markdown formatting and append styled runs to *paragraph*.

    Handles: ``***bold-italic***``, ``**bold**``, ``*italic*``, ``` `code` ```,
    ``[n]`` citation links, ``[text](url)`` web links, bare ``https://`` URLs.

    Em dash v\u00e0 en dash \u0111\u01b0\u1ee3c gi\u1eef nguy\u00ean. Times New Roman c\u00f3 \u0111\u1ee7 hai glyph n\u00e0y v\u00e0
    quy \u01b0\u1edbc h\u1ecdc thu\u1eadt d\u00f9ng en dash cho kho\u1ea3ng gi\u00e1 tr\u1ecb (``pp. 90\u2013113``) c\u00f9ng t\u00ean
    gh\u00e9p c\u1ee7a hai t\u00e1c gi\u1ea3 (``Clopper\u2013Pearson``, ``Precision\u2013Recall``), n\u00ean thay
    ch\u00fang b\u1eb1ng hyphen l\u00e0m sai ch\u00ednh t\u1ea3 tr\u00ecnh b\u00e0y.
    """
    token_pattern = re.compile(
        r"(\*\*\*[^*]+\*\*\*|\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|\[\d+\]|\[[^\]]+\]\(https?://[^\)]+\)|https?://[^\s)\]]+)"
    )
    tokens = token_pattern.split(text)

    for token in tokens:
        if not token:
            continue

        # Markdown Web Link: [Anchor](URL)
        md_link_m = re.match(r"^\[([^\]]+)\]\((https?://[^\)]+)\)$", token)
        if md_link_m:
            add_external_hyperlink(
                paragraph,
                md_link_m.group(2),
                text=md_link_m.group(1),
                font_name=base_font_name,
                font_size=base_font_size,
                is_bold=is_bold,
                is_italic=is_italic,
                color_hex="000000",
                is_underline=True,
            )
            continue

        # Direct Web URL
        if re.match(r"^https?://[^\s)\]]+$", token):
            add_external_hyperlink(
                paragraph,
                token,
                text=token,
                font_name=base_font_name,
                font_size=base_font_size,
                is_bold=is_bold,
                is_italic=is_italic,
                color_hex="000000",
                is_underline=True,
            )
            continue

        # Citation [n] -> Clickable link to Bibliography anchor ref_n
        cit_m = re.match(r"^\[(\d+)\]$", token)
        if cit_m:
            ref_id = cit_m.group(1)
            add_internal_hyperlink(
                paragraph,
                f"ref_{ref_id}",
                f"[{ref_id}]",
                font_name=base_font_name,
                font_size=base_font_size,
                is_bold=True,
                color_hex="000000",
            )
            continue

        # Bold-Italic
        if token.startswith("***") and token.endswith("***") and len(token) >= 6:
            r = paragraph.add_run(token[3:-3])
            r.font.name = base_font_name
            r.font.size = Pt(base_font_size)
            r.bold = True
            r.italic = True
            r.font.color.rgb = COLOR_TEXT_MAIN
        # Bold
        elif token.startswith("**") and token.endswith("**") and len(token) >= 4:
            r = paragraph.add_run(token[2:-2])
            r.font.name = base_font_name
            r.font.size = Pt(base_font_size)
            r.bold = True
            r.italic = is_italic
            r.font.color.rgb = COLOR_TEXT_MAIN
        # Italic
        elif token.startswith("*") and token.endswith("*") and len(token) >= 2:
            r = paragraph.add_run(token[1:-1])
            r.font.name = base_font_name
            r.font.size = Pt(base_font_size)
            r.bold = is_bold
            r.italic = True
            r.font.color.rgb = COLOR_TEXT_MAIN
        # Monospace code (Courier New, pure black)
        elif token.startswith("`") and token.endswith("`") and len(token) >= 2:
            r = paragraph.add_run(token[1:-1])
            r.font.name = "Courier New"
            r.font.size = Pt(base_font_size - 0.5)
            r.bold = is_bold
            r.italic = is_italic
            r.font.color.rgb = COLOR_TEXT_MAIN
        else:
            r = paragraph.add_run(token)
            r.font.name = base_font_name
            r.font.size = Pt(base_font_size)
            r.bold = is_bold
            r.italic = is_italic
            r.font.color.rgb = COLOR_TEXT_MAIN
