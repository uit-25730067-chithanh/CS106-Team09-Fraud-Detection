"""Time mapping must preserve model hours; monetary input must be unambiguous."""

from datetime import datetime, timedelta
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "demo"))
from input_formatting import (
    SIMULATION_START, step_to_datetime, datetime_to_step,
    format_currency, parse_currency,
)


def test_all_simulation_hours_round_trip_without_off_by_one():
    for step in range(1, 745):
        value = step_to_datetime(step)
        assert datetime_to_step(value) == step
        assert value.hour == step % 24
    assert step_to_datetime(24) == datetime(2026, 1, 2)
    assert step_to_datetime(744) == datetime(2026, 2, 1)


@pytest.mark.parametrize("hours", [0, 0.5, 1.5, 744.5, 745])
def test_invalid_simulation_time_is_rejected(hours):
    with pytest.raises(ValueError):
        datetime_to_step(SIMULATION_START + timedelta(hours=hours))


@pytest.mark.parametrize("text,value,formatted", [
    ("250000", 250000.0, "250.000"),
    ("1.143.937,73", 1143937.73, "1.143.937,73"),
    ("0", 0.0, "0"),
    ("0,01", 0.01, "0,01"),
    (" 1000,50 ", 1000.5, "1.000,5"),
])
def test_money_parse_and_display(text, value, formatted):
    assert parse_currency(text) == value
    assert format_currency(value) == formatted
    assert parse_currency(formatted) == value


@pytest.mark.parametrize("text", ["", "NaN", "inf", "-1", "1e6", "1.23", "1,000.50", "1,234", "1..000", "1000000000000"])
def test_invalid_money_is_rejected(text):
    with pytest.raises(ValueError):
        parse_currency(text)
