"""Tests for the Phase 05 artifact contract consumed by the demo."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEMO_DIR = PROJECT_ROOT / "demo"
if str(DEMO_DIR) not in sys.path:
    sys.path.insert(0, str(DEMO_DIR))

from evaluation_artifacts import (
    EVALUATION_FIGURES,
    find_evaluation_figures,
    load_model_comparison,
    missing_evaluation_figures,
)


def comparison_rows() -> list[dict[str, object]]:
    return [
        {
            "Model": "Random Forest",
            "Precision Fraud": 0.98,
            "Recall Fraud": 0.96,
            "F1 Fraud": 0.97,
            "Roc Auc": 0.99,
            "Pr Auc": 0.98,
        },
        {
            "Model": "XGBoost",
            "Precision Fraud": 0.99,
            "Recall Fraud": 0.98,
            "F1 Fraud": 0.985,
            "Roc Auc": 0.995,
            "Pr Auc": 0.99,
        },
        {
            "Model": "Autoencoder",
            "Precision Fraud": 0.70,
            "Recall Fraud": 0.75,
            "F1 Fraud": 0.72,
            "Roc Auc": 0.93,
            "Pr Auc": 0.68,
        },
    ]


def test_comparison_loader_accepts_phase05_title_case_schema(tmp_path: Path):
    csv_path = tmp_path / "model_comparison.csv"
    pd.DataFrame(comparison_rows()).to_csv(csv_path, index=False)

    comparison = load_model_comparison(csv_path)

    assert list(comparison.columns) == [
        "model",
        "precision",
        "recall",
        "f1_score",
        "roc_auc",
        "pr_auc",
    ]
    assert comparison.iloc[0]["model"] == "XGBoost"
    assert comparison.iloc[0]["f1_score"] == pytest.approx(0.985)


def test_comparison_loader_rejects_missing_metric(tmp_path: Path):
    csv_path = tmp_path / "model_comparison.csv"
    rows = comparison_rows()
    frame = pd.DataFrame(rows).drop(columns=["Pr Auc"])
    frame.to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="pr_auc"):
        load_model_comparison(csv_path)


def test_comparison_loader_rejects_out_of_range_metric(tmp_path: Path):
    csv_path = tmp_path / "model_comparison.csv"
    rows = comparison_rows()
    rows[0]["F1 Fraud"] = 99.7
    pd.DataFrame(rows).to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        load_model_comparison(csv_path)


def test_figure_discovery_reports_present_and_missing_files(tmp_path: Path):
    available = EVALUATION_FIGURES[0]
    (tmp_path / available.filename).write_bytes(b"png")

    figures = find_evaluation_figures(tmp_path)
    missing = missing_evaluation_figures(tmp_path)

    assert figures == {available.key: tmp_path / available.filename}
    assert available.filename not in missing
    assert len(missing) == len(EVALUATION_FIGURES) - 1


def test_figure_contract_covers_all_nine_distinct_evaluation_views():
    figure_map = {figure.key: figure.filename for figure in EVALUATION_FIGURES}

    assert len(EVALUATION_FIGURES) == 9
    assert len(set(figure_map.values())) == 9
    assert figure_map["feature_importance"] == "feature_importance_comparison.png"
    assert figure_map["confusion_components"] == "confusion_matrix_components.png"
    assert figure_map["confusion_rf_smotenc"] == "confusion_matrix_rf-smotenc.png"
    assert figure_map["confusion_xgb_smotenc"] == "confusion_matrix_xgb-smotenc.png"
    assert figure_map["confusion_rf_adasyn"] == "confusion_matrix_rf-adasyn.png"
    assert figure_map["confusion_xgb_adasyn"] == "confusion_matrix_xgb-adasyn.png"
