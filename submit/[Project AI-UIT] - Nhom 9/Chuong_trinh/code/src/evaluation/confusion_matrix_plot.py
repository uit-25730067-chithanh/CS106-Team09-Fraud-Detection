"""Confusion matrix heatmap visualization for a single model."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from matplotlib.figure import Figure
from sklearn.metrics import confusion_matrix


FIGURES_DIR = Path(__file__).resolve().parents[2] / "reports" / "figures"


def _validate_lengths(y_true: Any, y_pred: Any) -> None:
    if len(y_true) != len(y_pred):
        raise ValueError("y_true and y_pred must have the same number of samples")


def _slug(model_name: str) -> str:
    return model_name.lower().replace(" ", "_")


def _create_figure(show: bool) -> tuple[Figure, Any]:
    if show:
        import matplotlib.pyplot as plt

        return plt.subplots(figsize=(6, 5))

    figure = Figure(figsize=(6, 5))
    return figure, figure.subplots()


def plot_confusion_matrix(
    y_true: Any,
    y_pred: Any,
    model_name: str = "Model",
    save: bool = True,
    output_dir: str | Path = FIGURES_DIR,
    show: bool = True,
) -> Figure:
    """Plot one model's confusion matrix as an annotated heatmap."""

    _validate_lengths(y_true, y_pred)

    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

    figure, axis = _create_figure(show)
    image = axis.imshow(cm, cmap="Blues")
    figure.colorbar(image, ax=axis)

    labels = ["Normal", "Fraud"]
    axis.set_xticks([0, 1], labels=labels)
    axis.set_yticks([0, 1], labels=labels)
    axis.set_xlabel("Predicted")
    axis.set_ylabel("Actual")
    axis.set_title(f"Confusion Matrix - {model_name}")

    threshold = cm.max() / 2 if cm.max() else 0
    for row in range(cm.shape[0]):
        for col in range(cm.shape[1]):
            axis.text(
                col,
                row,
                format(cm[row, col], "d"),
                ha="center",
                va="center",
                color="white" if cm[row, col] > threshold else "black",
            )

    figure.tight_layout()

    if save:
        output_path = Path(output_dir) / f"confusion_matrix_{_slug(model_name)}.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=150, bbox_inches="tight")

    import matplotlib.pyplot as plt

    if show:
        plt.show()
    plt.close(figure)

    return figure
