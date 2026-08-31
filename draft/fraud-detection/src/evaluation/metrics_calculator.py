"""Compute classification metrics for fraud detection models."""

from __future__ import annotations

from typing import Any, TypedDict

from sklearn.metrics import (
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


class EvaluationMetrics(TypedDict):
    model: str
    precision_fraud: float
    recall_fraud: float
    f1_fraud: float
    roc_auc: float
    pr_auc: float


def _validate_lengths(y_true: Any, y_pred: Any, y_prob: Any) -> None:
    lengths = (len(y_true), len(y_pred), len(y_prob))
    if len(set(lengths)) != 1:
        raise ValueError("y_true, y_pred, and y_prob must have the same number of samples")


def _ranking_metric(metric_fn: Any, y_true: Any, y_prob: Any) -> float:
    """Round a ranking metric, or return NaN when y_true has only one class."""

    if len(set(y_true)) < 2:
        return float("nan")
    return round(float(metric_fn(y_true, y_prob)), 4)


def compute_metrics(
    y_true: Any,
    y_pred: Any,
    y_prob: Any,
    model_name: str = "Model",
) -> EvaluationMetrics:
    """Return fraud-class metrics and ranking metrics for one model."""

    _validate_lengths(y_true, y_pred, y_prob)

    return {
        "model": model_name,
        "precision_fraud": round(
            float(precision_score(y_true, y_pred, pos_label=1, zero_division=0)),
            4,
        ),
        "recall_fraud": round(
            float(recall_score(y_true, y_pred, pos_label=1, zero_division=0)),
            4,
        ),
        "f1_fraud": round(
            float(f1_score(y_true, y_pred, pos_label=1, zero_division=0)),
            4,
        ),
        "roc_auc": _ranking_metric(roc_auc_score, y_true, y_prob),
        "pr_auc": _ranking_metric(average_precision_score, y_true, y_prob),
    }


def print_metrics(metrics: EvaluationMetrics) -> None:
    """Print one model's metrics in a terminal-friendly layout."""

    separator = "=" * 50
    print(f"\n{separator}")
    print(f"  {metrics['model']}")
    print(separator)
    print(f"  Precision (Fraud): {metrics['precision_fraud']:.4f}")
    print(f"  Recall    (Fraud): {metrics['recall_fraud']:.4f}")
    print(f"  F1-Score  (Fraud): {metrics['f1_fraud']:.4f}")
    print(f"  ROC-AUC          : {metrics['roc_auc']:.4f}")
    print(f"  PR-AUC           : {metrics['pr_auc']:.4f}")
    print(f"{separator}\n")
