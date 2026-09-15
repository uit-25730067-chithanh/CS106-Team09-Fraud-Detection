"""Persistent analysis history must survive connections and support cleanup."""

from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "demo"))
from history_store import (
    clear_analysis_history,
    delete_analysis,
    load_analysis_history,
    save_analysis,
)


def analysis_entry(amount: float, label: int = 0) -> dict[str, object]:
    return {
        "created_at": "2026-09-09T10:30:00+07:00",
        "transaction_type": "TRANSFER",
        "step": 120,
        "amount": amount,
        "fraud_probability": 0.82 if label else 0.08,
        "threshold": 0.5,
        "label": label,
        "quality_warnings": 0,
    }


def test_history_survives_new_database_connections(tmp_path):
    database_path = tmp_path / "history.sqlite3"

    first_id = save_analysis(database_path, analysis_entry(100_000))
    second_id = save_analysis(database_path, analysis_entry(900_000, label=1))

    assert [row["sequence"] for row in load_analysis_history(database_path)] == [
        first_id,
        second_id,
    ]
    assert load_analysis_history(database_path)[-1]["label"] == 1


def test_delete_one_then_clear_all_history(tmp_path):
    database_path = tmp_path / "history.sqlite3"
    first_id = save_analysis(database_path, analysis_entry(100_000))
    save_analysis(database_path, analysis_entry(900_000, label=1))

    assert delete_analysis(database_path, first_id)
    assert len(load_analysis_history(database_path)) == 1
    assert clear_analysis_history(database_path) == 1
    assert load_analysis_history(database_path) == []


def test_history_limit_must_be_positive(tmp_path):
    with pytest.raises(ValueError):
        load_analysis_history(tmp_path / "history.sqlite3", limit=0)


def test_history_keeps_only_the_latest_250_entries(tmp_path):
    database_path = tmp_path / "history.sqlite3"
    for amount in range(251):
        save_analysis(database_path, analysis_entry(float(amount)))

    history = load_analysis_history(database_path)
    assert len(history) == 250
    assert history[0]["amount"] == 1.0
    assert history[-1]["amount"] == 250.0
