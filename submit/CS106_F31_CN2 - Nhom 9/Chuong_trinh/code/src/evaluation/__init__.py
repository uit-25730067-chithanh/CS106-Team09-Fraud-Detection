"""Evaluation helpers for fraud detection models."""

from .confusion_matrix_plot import plot_confusion_matrix
from .metrics_calculator import compute_metrics, print_metrics
from .model_comparator import compare_models, save_comparison
from .plot_confusion_components import plot_confusion_components
from .plot_roc_curve import plot_pr_curves, plot_roc_curves
from .prevalence_projection import (
    ORIGINAL_PREVALENCE,
    clopper_pearson,
    precision_at,
    project_to_original_prevalence,
    report_false_negative_overlap,
)

__all__ = [
    "compute_metrics",
    "print_metrics",
    "plot_roc_curves",
    "plot_confusion_components",
    "plot_confusion_matrix",
    "plot_pr_curves",
    "compare_models",
    "save_comparison",
    "ORIGINAL_PREVALENCE",
    "clopper_pearson",
    "precision_at",
    "project_to_original_prevalence",
    "report_false_negative_overlap",
]

