"""ROC and Precision-Recall curve visualizations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from matplotlib.figure import Figure
from sklearn.metrics import (
    average_precision_score,
    precision_recall_curve,
    roc_auc_score,
    roc_curve,
)


FIGURES_DIR = Path(__file__).resolve().parents[2] / "reports" / "figures"


def _validate_inputs(models_dict: dict[str, Any], y_true: Any) -> None:
    if not models_dict:
        raise ValueError("models_dict must contain at least one model")

    expected_length = len(y_true)
    for model_name, scores in models_dict.items():
        if len(scores) != expected_length:
            raise ValueError(
                f"Scores for {model_name!r} must have the same number of samples as y_true"
            )


def _create_figure(show: bool) -> tuple[Figure, Any]:
    if show:
        import matplotlib.pyplot as plt

        return plt.subplots(figsize=(8, 6))

    figure = Figure(figsize=(8, 6))
    return figure, figure.subplots()


def plot_roc_curves(
    models_dict: dict[str, Any],
    y_true: Any,
    save: bool = True,
    output_dir: str | Path = FIGURES_DIR,
    show: bool = True,
) -> Figure:
    """Plot all model ROC curves on one figure and optionally save it."""

    _validate_inputs(models_dict, y_true)
    figure, axis = _create_figure(show)

    for model_name, y_prob in models_dict.items():
        false_positive_rate, true_positive_rate, _ = roc_curve(y_true, y_prob)
        roc_auc = roc_auc_score(y_true, y_prob)
        axis.plot(
            false_positive_rate,
            true_positive_rate,
            linewidth=2,
            label=f"{model_name} (AUC = {roc_auc:.4f})",
        )

    axis.plot([0, 1], [0, 1], "k--", linewidth=1, label="Random")
    axis.set_xlabel("False Positive Rate")
    axis.set_ylabel("True Positive Rate")
    axis.set_title("ROC Curves - All Models")
    axis.legend(loc="lower right")
    axis.grid(alpha=0.3)
    figure.tight_layout()

    if save:
        output_path = Path(output_dir) / "roc_curves_all.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=150, bbox_inches="tight")

    if show:
        import matplotlib.pyplot as plt

        plt.show()

    return figure


def plot_pr_curves(
    models_dict: dict[str, Any],
    y_true: Any,
    save: bool = True,
    output_dir: str | Path = FIGURES_DIR,
    show: bool = True,
) -> Figure:
    """Plot all model Precision-Recall curves and optionally save them."""

    _validate_inputs(models_dict, y_true)
    figure, axis = _create_figure(show)

    for model_name, y_prob in models_dict.items():
        precision, recall, _ = precision_recall_curve(y_true, y_prob)
        pr_auc = average_precision_score(y_true, y_prob)
        axis.plot(
            recall,
            precision,
            linewidth=2,
            label=f"{model_name} (PR-AUC = {pr_auc:.4f})",
        )

    axis.set_xlabel("Recall")
    axis.set_ylabel("Precision")
    axis.set_title("Precision-Recall Curves - All Models")
    axis.legend(loc="upper right")
    axis.grid(alpha=0.3)
    figure.tight_layout()

    if save:
        output_path = Path(output_dir) / "pr_curves_all.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=150, bbox_inches="tight")

    if show:
        import matplotlib.pyplot as plt

        plt.show()

    return figure
