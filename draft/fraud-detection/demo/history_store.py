"""Small SQLite store for persistent demo analysis history."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping


CREATE_HISTORY_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS analysis_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    step INTEGER NOT NULL,
    amount REAL NOT NULL,
    fraud_probability REAL NOT NULL,
    threshold REAL NOT NULL,
    label INTEGER NOT NULL,
    quality_warnings INTEGER NOT NULL
)
"""
MAX_HISTORY_ENTRIES = 250


def _connect(database_path: Path) -> sqlite3.Connection:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database_path, timeout=5)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA busy_timeout = 5000")
    connection.execute(CREATE_HISTORY_TABLE_SQL)
    return connection


def load_analysis_history(
    database_path: Path,
    limit: int = MAX_HISTORY_ENTRIES,
) -> list[dict[str, Any]]:
    """Return the newest persisted analyses in chronological order."""

    if limit < 1:
        raise ValueError("limit must be at least 1")

    with _connect(database_path) as connection:
        rows = connection.execute(
            """
            SELECT id, created_at, transaction_type, step, amount,
                   fraud_probability, threshold, label, quality_warnings
            FROM analysis_history
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    return [
        {
            "sequence": int(row["id"]),
            "created_at": row["created_at"],
            "transaction_type": row["transaction_type"],
            "step": int(row["step"]),
            "amount": float(row["amount"]),
            "fraud_probability": float(row["fraud_probability"]),
            "threshold": float(row["threshold"]),
            "label": int(row["label"]),
            "quality_warnings": int(row["quality_warnings"]),
        }
        for row in reversed(rows)
    ]


def save_analysis(database_path: Path, entry: Mapping[str, Any]) -> int:
    """Persist one successful analysis and return its database identifier."""

    created_at = str(
        entry.get("created_at")
        or datetime.now().astimezone().isoformat(timespec="seconds")
    )
    with _connect(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO analysis_history (
                created_at, transaction_type, step, amount,
                fraud_probability, threshold, label, quality_warnings
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                created_at,
                str(entry["transaction_type"]),
                int(entry["step"]),
                float(entry["amount"]),
                float(entry["fraud_probability"]),
                float(entry["threshold"]),
                int(entry["label"]),
                int(entry["quality_warnings"]),
            ),
        )
        connection.execute(
            """
            DELETE FROM analysis_history
            WHERE id NOT IN (
                SELECT id FROM analysis_history ORDER BY id DESC LIMIT ?
            )
            """,
            (MAX_HISTORY_ENTRIES,),
        )
        return int(cursor.lastrowid)


def delete_analysis(database_path: Path, analysis_id: int) -> bool:
    """Delete one persisted analysis by its identifier."""

    with _connect(database_path) as connection:
        cursor = connection.execute(
            "DELETE FROM analysis_history WHERE id = ?",
            (int(analysis_id),),
        )
        return cursor.rowcount > 0


def clear_analysis_history(database_path: Path) -> int:
    """Delete all analyses and reset identifiers for a clean demo session."""

    with _connect(database_path) as connection:
        cursor = connection.execute("DELETE FROM analysis_history")
        connection.execute(
            "DELETE FROM sqlite_sequence WHERE name = 'analysis_history'"
        )
        return cursor.rowcount
