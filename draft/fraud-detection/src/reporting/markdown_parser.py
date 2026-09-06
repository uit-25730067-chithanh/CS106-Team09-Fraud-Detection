"""Markdown parsing and inline run formatting for DOCX report generation."""

from __future__ import annotations

import re

from docx.shared import Pt


def _split_row(line: str) -> list[str]:
    """Tách các ô trong một hàng bảng Markdown."""
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def parse_markdown(text: str) -> list[dict]:
    """Chuyển Markdown của báo cáo thành danh sách block đơn giản."""
    lines = text.splitlines()
    blocks: list[dict] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        if stripped == "---":
            blocks.append({"type": "pagebreak"})
            index += 1
            continue

        heading = re.match(r"^(#{1,3})\s+(.*)$", stripped)
        if heading:
            blocks.append({
                "type": f"h{len(heading.group(1))}",
                "text": heading.group(2).strip(),
            })
            index += 1
            continue

        image = re.match(r"^!\[(.*?)\]\((.*?)\)$", stripped)
        if image:
            blocks.append({
                "type": "image",
                "caption": image.group(1).strip(),
                "path": image.group(2).strip(),
            })
            index += 1
            continue

        if stripped.startswith("|") and index + 1 < len(lines) and re.match(
            r"^\|[\s:|-]+\|$", lines[index + 1].strip()
        ):
            header = _split_row(stripped)
            index += 2
            rows = []
            while index < len(lines) and lines[index].strip().startswith("|"):
                rows.append(_split_row(lines[index].strip()))
                index += 1
            blocks.append({"type": "table", "header": header, "rows": rows})
            continue

        if stripped.startswith("> "):
            note = [stripped[2:].strip()]
            index += 1
            while index < len(lines) and lines[index].strip().startswith("> "):
                note.append(lines[index].strip()[2:].strip())
                index += 1
            blocks.append({"type": "note", "text": " ".join(note)})
            continue

        if stripped.startswith("- "):
            blocks.append({"type": "bullet", "text": stripped[2:].strip()})
            index += 1
            continue

        numbered = re.match(r"^\d+\.\s+(.*)$", stripped)
        if numbered:
            blocks.append({"type": "number", "text": numbered.group(1).strip()})
            index += 1
            continue

        if re.match(r"^\*\*.*\*\*$", stripped):
            blocks.append({"type": "caption", "text": stripped.strip("*").strip()})
            index += 1
            continue

        blocks.append({"type": "para", "text": stripped})
        index += 1

    return blocks


def clean_markdown_symbols(text: str) -> str:
    """Bỏ ký hiệu Markdown mà bản Word không hiển thị (backtick, ký hiệu toán)."""
    text = text.replace("`", "")
    return re.sub(r"\$(.+?)\$", r"\1", text)


def add_runs(paragraph, text: str, bold: bool = False, size_pt: float | None = None):
    """Ghi text vào paragraph, tách phần **in đậm** thành run riêng."""
    for segment in re.split(r"(\*\*.+?\*\*)", clean_markdown_symbols(text)):
        if not segment:
            continue
        run = paragraph.add_run(segment.strip("*") if segment.startswith("**") else segment)
        run.bold = bold or segment.startswith("**")
        if size_pt is not None:
            run.font.size = Pt(size_pt)
    return paragraph
