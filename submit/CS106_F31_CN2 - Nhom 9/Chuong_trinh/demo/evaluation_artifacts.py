"""Validated Phase 05 artifacts consumed by the Streamlit demo."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import pandas as pd


COMPARISON_COLUMNS = (
    "model",
    "precision",
    "recall",
    "f1_score",
    "roc_auc",
    "pr_auc",
)

_COLUMN_ALIASES = {
    "model": ("model", "model_name"),
    "precision": ("precision", "precision_fraud"),
    "recall": ("recall", "recall_fraud"),
    "f1_score": ("f1_score", "f1", "f1_fraud"),
    "roc_auc": ("roc_auc", "auc"),
    "pr_auc": ("pr_auc", "average_precision", "ap"),
}


@dataclass(frozen=True)
class EvaluationFigure:
    """One expected evaluation figure and its UI metadata."""

    key: str
    filename: str
    title: str
    caption: str
    category: str


EVALUATION_FIGURES = (
    EvaluationFigure(
        "roc",
        "roc_curves_all.png",
        "ROC của 5 biến thể",
        "So sánh khả năng phân biệt giao dịch hợp lệ và gian lận của 5 biến thể.",
        "curves",
    ),
    EvaluationFigure(
        "pr",
        "pr_curves_all.png",
        "Precision–Recall của 5 biến thể",
        "Thể hiện đánh đổi Precision–Recall của 5 biến thể trên dữ liệu mất cân bằng.",
        "curves",
    ),
    EvaluationFigure(
        "feature_importance",
        "feature_importance_comparison.png",
        "Mức đóng góp của đặc trưng",
        "So sánh vai trò của 14 đặc trưng trong Random Forest và XGBoost.",
        "importance",
    ),
    EvaluationFigure(
        "confusion_rf_smotenc",
        "confusion_matrix_rf-smotenc.png",
        "Random Forest + SMOTENC",
        "Random Forest huấn luyện với SMOTENC, đánh giá trên test set nguyên bản.",
        "confusion",
    ),
    EvaluationFigure(
        "confusion_xgb_smotenc",
        "confusion_matrix_xgb-smotenc.png",
        "XGBoost + SMOTENC",
        "XGBoost huấn luyện với SMOTENC, đánh giá trên test set nguyên bản.",
        "confusion",
    ),
    EvaluationFigure(
        "confusion_rf_adasyn",
        "confusion_matrix_rf-adasyn.png",
        "Random Forest + ADASYN",
        "Random Forest huấn luyện với ADASYN, đánh giá trên test set nguyên bản.",
        "confusion",
    ),
    EvaluationFigure(
        "confusion_xgb_adasyn",
        "confusion_matrix_xgb-adasyn.png",
        "XGBoost + ADASYN",
        "XGBoost huấn luyện với ADASYN, đánh giá trên test set nguyên bản.",
        "confusion",
    ),
    EvaluationFigure(
        "confusion_autoencoder",
        "confusion_matrix_autoencoder.png",
        "Autoencoder",
        "Số dự đoán đúng và sai của Autoencoder trên test set.",
        "confusion",
    ),
    EvaluationFigure(
        "confusion_components",
        "confusion_matrix_components.png",
        "So sánh TP, FP, FN của 5 biến thể",
        "Tổng hợp trực quan các dự đoán đúng và sai trên cùng tập kiểm thử.",
        "components",
    ),
)


def _normalize_column_name(value: object) -> str:
    """Return a stable snake_case representation for a CSV header."""

    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", str(value).lower())).strip("_")


def load_model_comparison(path: Path) -> pd.DataFrame:
    """Load and validate the official three-model comparison CSV.

    The Phase 05 template converts snake_case headers to title case before
    export. This loader accepts both representations and exposes one stable
    contract to the UI. Metric values must remain probabilities in [0, 1].
    """

    if not path.is_file():
        raise FileNotFoundError(f"Chưa có bảng so sánh Phase 05: {path}")

    source = pd.read_csv(path)
    normalized_headers = {
        _normalize_column_name(column): column for column in source.columns
    }
    selected_columns: dict[str, object] = {}
    missing_columns: list[str] = []

    for canonical_name, aliases in _COLUMN_ALIASES.items():
        source_column = next(
            (
                normalized_headers[alias]
                for alias in aliases
                if alias in normalized_headers
            ),
            None,
        )
        if source_column is None:
            missing_columns.append(canonical_name)
        else:
            selected_columns[canonical_name] = source_column

    if missing_columns:
        raise ValueError(
            "Bảng so sánh thiếu cột bắt buộc: " + ", ".join(missing_columns)
        )

    comparison = pd.DataFrame(
        {
            canonical_name: source[source_column]
            for canonical_name, source_column in selected_columns.items()
        }
    )
    comparison["model"] = comparison["model"].astype("string").str.strip()
    if comparison["model"].isna().any() or (comparison["model"] == "").any():
        raise ValueError("Bảng so sánh có tên mô hình rỗng.")
    if comparison["model"].duplicated().any():
        raise ValueError("Bảng so sánh có tên mô hình trùng nhau.")
    if len(comparison) < 3:
        raise ValueError("Bảng so sánh phải có ít nhất ba mô hình.")

    for column in COMPARISON_COLUMNS[1:]:
        comparison[column] = pd.to_numeric(comparison[column], errors="coerce")
        if comparison[column].isna().any():
            raise ValueError(f"Cột {column} chứa giá trị không phải số.")
        if not comparison[column].between(0.0, 1.0, inclusive="both").all():
            raise ValueError(f"Cột {column} phải nằm trong khoảng [0, 1].")

    return comparison.loc[:, COMPARISON_COLUMNS].sort_values(
        "f1_score",
        ascending=False,
        ignore_index=True,
    )


def find_evaluation_figures(figures_dir: Path) -> dict[str, Path]:
    """Return only expected Phase 05 PNG files that currently exist."""

    return {
        figure.key: figures_dir / figure.filename
        for figure in EVALUATION_FIGURES
        if (figures_dir / figure.filename).is_file()
    }


def missing_evaluation_figures(figures_dir: Path) -> tuple[str, ...]:
    """List expected filenames still missing from the Phase 05 output."""

    return tuple(
        figure.filename
        for figure in EVALUATION_FIGURES
        if not (figures_dir / figure.filename).is_file()
    )
