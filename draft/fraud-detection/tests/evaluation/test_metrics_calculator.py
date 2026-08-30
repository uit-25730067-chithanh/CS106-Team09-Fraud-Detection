"""Tests for fraud-detection classification metrics."""

from __future__ import annotations

import pytest

from src.evaluation.metrics_calculator import compute_metrics, print_metrics


def test_compute_metrics_returns_hand_checked_fraud_metrics() -> None:
    metrics = compute_metrics(
        y_true=[0, 0, 1, 1],
        y_pred=[0, 1, 1, 0],
        y_prob=[0.1, 0.8, 0.9, 0.2],
        model_name="Dummy Model",
    )

    assert metrics == {
        "model": "Dummy Model",
        "precision_fraud": 0.5,
        "recall_fraud": 0.5,
        "f1_fraud": 0.5,
        "roc_auc": 0.75,
        "pr_auc": 0.8333,
    }


def test_compute_metrics_handles_no_predicted_fraud() -> None:
    metrics = compute_metrics(
        y_true=[0, 0, 1, 1],
        y_pred=[0, 0, 0, 0],
        y_prob=[0.1, 0.2, 0.8, 0.9],
    )

    assert metrics["precision_fraud"] == 0.0
    assert metrics["recall_fraud"] == 0.0
    assert metrics["f1_fraud"] == 0.0
    assert metrics["roc_auc"] == 1.0
    assert metrics["pr_auc"] == 1.0


def test_compute_metrics_rejects_mismatched_lengths() -> None:
    with pytest.raises(ValueError, match="same number of samples"):
        compute_metrics(
            y_true=[0, 1],
            y_pred=[0],
            y_prob=[0.1, 0.9],
        )


def test_print_metrics_formats_a_readable_summary(capsys: pytest.CaptureFixture[str]) -> None:
    print_metrics(
        {
            "model": "Dummy Model",
            "precision_fraud": 0.5,
            "recall_fraud": 0.25,
            "f1_fraud": 0.3333,
            "roc_auc": 0.75,
            "pr_auc": 0.625,
        }
    )

    output = capsys.readouterr().out
    assert "Dummy Model" in output
    assert "Precision (Fraud): 0.5000" in output
    assert "Recall    (Fraud): 0.2500" in output
    assert "F1-Score  (Fraud): 0.3333" in output
    assert "ROC-AUC          : 0.7500" in output
    assert "PR-AUC           : 0.6250" in output
