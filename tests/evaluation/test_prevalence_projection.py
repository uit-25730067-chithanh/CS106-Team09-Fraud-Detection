"""Tests for prevalence projection and false negative overlap analysis."""

from __future__ import annotations

import numpy as np
import pytest

from src.evaluation.prevalence_projection import (
    ORIGINAL_PREVALENCE,
    clopper_pearson,
    precision_at,
    project_to_original_prevalence,
    report_false_negative_overlap,
)


def test_clopper_pearson_exact_intervals() -> None:
    # 0 successes in 100 trials -> lower bound must be 0.0
    lower, upper = clopper_pearson(0, 100)
    assert lower == 0.0
    assert 0.0 < upper < 0.05

    # 100 successes in 100 trials -> upper bound must be 1.0
    lower, upper = clopper_pearson(100, 100)
    assert 0.95 < lower < 1.0
    assert upper == 1.0

    # 50 in 100 trials -> symmetric around 0.5
    lower, upper = clopper_pearson(50, 100)
    assert lower < 0.5 < upper
    assert pytest.approx(0.5 - lower, abs=1e-4) == upper - 0.5


def test_clopper_pearson_invalid_inputs() -> None:
    with pytest.raises(ValueError, match="phải lớn hơn 0"):
        clopper_pearson(0, 0)
    with pytest.raises(ValueError, match="nằm trong"):
        clopper_pearson(10, 5)


def test_precision_at_known_values() -> None:
    # Perfect classifier: tpr=1, fpr=0 -> precision=1
    assert precision_at(0.01, 1.0, 0.0) == 1.0

    # Random guessing: tpr=0.5, fpr=0.5 -> precision=prevalence
    assert precision_at(0.05, 0.5, 0.5) == pytest.approx(0.05)


def test_project_to_original_prevalence_computes_expected_structure() -> None:
    y_true = np.array([0] * 90 + [1] * 10)
    predictions = {
        "TestModel": {
            "y_pred": [0] * 89 + [1] + [1] * 9 + [0],  # 1 FP, 1 FN, 9 TP, 89 TN
            "y_prob": [0.1] * 100,
        }
    }

    rows = project_to_original_prevalence(y_true, predictions, prevalence=ORIGINAL_PREVALENCE)
    assert len(rows) == 1
    row = rows[0]
    assert row["model"] == "TestModel"
    assert row["false_positives"] == 1
    assert row["tpr"] == 0.9
    assert "precision_original" in row
    assert "precision_original_low" in row
    assert "precision_original_high" in row
    assert row["precision_original_low"] <= row["precision_original"] <= row["precision_original_high"]


def test_report_false_negative_overlap_runs_without_error(capsys: pytest.CaptureFixture) -> None:
    y_true = np.array([1, 1, 1, 0, 0])
    predictions = {
        "M1": {"y_pred": [1, 1, 0, 0, 0]},  # FN at index 2
        "M2": {"y_pred": [1, 1, 0, 0, 0]},  # FN at index 2
        "Autoencoder": {"y_pred": [1, 0, 0, 0, 0]},  # FN at 1, 2
    }

    report_false_negative_overlap(y_true, predictions)
    captured = capsys.readouterr().out
    assert "Chồng lấn False Negative" in captured
    assert "M1: 1 FN" in captured
