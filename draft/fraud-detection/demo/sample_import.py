"""Parse small CSV/JSON transaction samples for the Streamlit demo."""

from __future__ import annotations

import io
import json
from pathlib import Path
from typing import Any

import pandas as pd


FIELD_ALIASES = {
    "transaction_type": ("transaction_type", "type"),
    "step": ("step",),
    "amount": ("amount",),
    "old_balance_origin": ("old_balance_origin", "oldbalanceOrg"),
    "new_balance_origin": ("new_balance_origin", "newbalanceOrig"),
    "old_balance_destination": ("old_balance_destination", "oldbalanceDest"),
    "new_balance_destination": ("new_balance_destination", "newbalanceDest"),
}
LABEL_ALIASES = ("true_label", "isFraud", "label")
MAX_IMPORTED_SAMPLES = 50


def _pick(row: dict[str, Any], aliases: tuple[str, ...], field: str) -> Any:
    for alias in aliases:
        if alias in row and not pd.isna(row[alias]):
            return row[alias]
    raise ValueError(f"Thiếu trường bắt buộc: {field}")


def _as_number(value: Any, field: str) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field} phải là số") from error
    if number < 0:
        raise ValueError(f"{field} không được âm")
    return number


def _normalize_row(row: dict[str, Any], index: int, source_name: str) -> dict[str, Any]:
    transaction_type = str(
        _pick(row, FIELD_ALIASES["transaction_type"], "type")
    ).strip().upper()
    if transaction_type not in {"TRANSFER", "CASH_OUT"}:
        raise ValueError("type chỉ nhận TRANSFER hoặc CASH_OUT")

    step_number = _as_number(_pick(row, FIELD_ALIASES["step"], "step"), "step")
    if not step_number.is_integer() or not 1 <= step_number <= 744:
        raise ValueError("step phải là số nguyên từ 1 đến 744")

    transaction = {
        "transaction_type": transaction_type,
        "step": int(step_number),
    }
    for field in (
        "amount",
        "old_balance_origin",
        "new_balance_origin",
        "old_balance_destination",
        "new_balance_destination",
    ):
        transaction[field] = _as_number(
            _pick(row, FIELD_ALIASES[field], field),
            field,
        )

    true_label = None
    for alias in LABEL_ALIASES:
        if alias in row and not pd.isna(row[alias]):
            label_number = _as_number(row[alias], alias)
            if not label_number.is_integer() or int(label_number) not in {0, 1}:
                raise ValueError(f"{alias} chỉ nhận 0 hoặc 1")
            true_label = int(label_number)
            break

    fallback_title = f"{Path(source_name).stem} · Mẫu {index + 1}"
    title = str(row.get("name") or row.get("title") or fallback_title).strip()
    return {
        "title": title[:80],
        "description": str(
            row.get("description")
            or f"Mẫu import từ {source_name}, dòng {index + 1}."
        )[:180],
        "transaction": transaction,
        "true_label": true_label,
    }


def parse_sample_file(filename: str, content: bytes) -> list[dict[str, Any]]:
    """Return validated transactions from a small CSV or JSON file."""

    suffix = Path(filename).suffix.lower()
    if suffix == ".csv":
        try:
            rows = pd.read_csv(io.BytesIO(content)).to_dict(orient="records")
        except Exception as error:
            raise ValueError("Không đọc được file CSV") from error
    elif suffix == ".json":
        try:
            payload = json.loads(content.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError("Không đọc được file JSON") from error
        if isinstance(payload, dict) and isinstance(payload.get("samples"), list):
            payload = payload["samples"]
        rows = payload if isinstance(payload, list) else [payload]
        if not all(isinstance(row, dict) for row in rows):
            raise ValueError("JSON phải là một object hoặc danh sách object")
    else:
        raise ValueError("Chỉ hỗ trợ file CSV hoặc JSON")

    if not rows:
        raise ValueError("File không có mẫu giao dịch")
    if len(rows) > MAX_IMPORTED_SAMPLES:
        raise ValueError(f"Mỗi lần chỉ import tối đa {MAX_IMPORTED_SAMPLES} mẫu")

    return [
        _normalize_row(dict(row), index, filename)
        for index, row in enumerate(rows)
    ]
