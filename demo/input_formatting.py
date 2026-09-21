"""Display-only PaySim time mapping and Vietnamese monetary input parsing."""

from datetime import datetime, timedelta
from decimal import Decimal
import re


# PaySim has no calendar dates. Keep hour == step % 24, as in training.
SIMULATION_START = datetime(2026, 1, 1)
MIN_STEP = 1
MAX_STEP = 744


def step_to_datetime(step: int) -> datetime:
    if not MIN_STEP <= step <= MAX_STEP or int(step) != step:
        raise ValueError("Step phải là số nguyên từ 1 đến 744.")
    return SIMULATION_START + timedelta(hours=int(step))


def datetime_to_step(value: datetime) -> int:
    if value.tzinfo is not None:
        raise ValueError("Dùng ngày giờ mô phỏng, không kèm múi giờ.")
    hours = (value - SIMULATION_START).total_seconds() / 3600
    if not MIN_STEP <= hours <= MAX_STEP or not hours.is_integer():
        raise ValueError("Chọn giờ tròn từ 01/01/2026 01:00 đến 01/02/2026 00:00.")
    return int(hours)


def format_currency(value: float) -> str:
    """Group thousands with dots and retain up to two decimal places."""
    integer, fraction = f"{value:,.2f}".split(".")
    fraction = fraction.rstrip("0")
    return integer.replace(",", ".") + (f",{fraction}" if fraction else "")


def parse_currency(value: str) -> float:
    """Accept ungrouped digits or strict Vietnamese thousands/decimal notation."""
    value = value.strip()
    if not re.fullmatch(r"(?:\d+|\d{1,3}(?:\.\d{3})+)(?:,\d{1,2})?", value):
        raise ValueError("Nhập số không âm: 250000 hoặc 250.000; phần lẻ dùng dấu phẩy, ví dụ 1.143.937,73.")
    amount = Decimal(value.replace(".", "").replace(",", "."))
    if amount > Decimal("999999999999.99"):
        raise ValueError("Số tiền tối đa là 999.999.999.999,99.")
    return float(amount)
