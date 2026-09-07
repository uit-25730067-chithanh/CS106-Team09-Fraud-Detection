"""Tests for cross-model performance comparison table."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.evaluation.model_comparator import compare_models, save_comparison


METRICS_LIST = [
    {
        "model": "RF",
        "precision_fraud": 0.99,
        "recall_fraud": 0.95,
        "f1_fraud": 0.97,
        "roc_auc": 0.999,
        "pr_auc": 0.99,
    },
    {
        "model": "XGB",
        "precision_fraud": 0.98,
        "recall_fraud": 0.99,
        "f1_fraud": 0.985,
        "roc_auc": 0.9993,
        "pr_auc": 0.98,
    },
]


def test_compare_models_sorts_by_f1_descending() -> None:
    df = compare_models(METRICS_LIST)

    assert df["Model"].tolist() == ["XGB", "RF"]


def test_compare_models_renames_columns_for_readability() -> None:
    df = compare_models(METRICS_LIST)

    assert list(df.columns) == [
        "Model",
        "Precision Fraud",
        "Recall Fraud",
        "F1 Fraud",
        "Roc Auc",
        "Pr Auc",
    ]


def test_save_comparison_writes_a_csv(tmp_path: Path) -> None:
    df = compare_models(METRICS_LIST)
    output_path = tmp_path / "model_comparison.csv"

    save_comparison(df, path=output_path)

    saved = pd.read_csv(output_path)
    assert saved["Model"].tolist() == ["XGB", "RF"]
