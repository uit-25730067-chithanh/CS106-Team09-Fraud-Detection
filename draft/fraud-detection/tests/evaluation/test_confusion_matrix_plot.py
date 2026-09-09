"""Tests for the per-model confusion matrix heatmap visualization."""

from __future__ import annotations

from pathlib import Path

from src.evaluation.confusion_matrix_plot import plot_confusion_matrix


Y_TRUE = [0, 0, 1, 1]
Y_PRED = [0, 1, 1, 1]


def test_plot_confusion_matrix_saves_a_heatmap_named_after_the_model(tmp_path: Path) -> None:
    figure = plot_confusion_matrix(
        Y_TRUE,
        Y_PRED,
        model_name="XGBoost SMOTE",
        output_dir=tmp_path,
        show=False,
    )

    assert (tmp_path / "confusion_matrix_xgboost_smote.png").is_file()
    assert figure.axes[0].get_title() == "Confusion Matrix - XGBoost SMOTE"


def test_plot_confusion_matrix_can_skip_file_output(tmp_path: Path) -> None:
    plot_confusion_matrix(
        Y_TRUE,
        Y_PRED,
        model_name="RF",
        save=False,
        output_dir=tmp_path,
        show=False,
    )

    assert list(tmp_path.iterdir()) == []


def test_plot_confusion_matrix_rejects_mismatched_lengths() -> None:
    import pytest

    with pytest.raises(ValueError, match="same number of samples"):
        plot_confusion_matrix([0, 1], [0], model_name="RF", show=False)


def test_plot_confusion_matrix_show_true_uses_a_pyplot_managed_figure(tmp_path: Path) -> None:
    """show=True must go through pyplot so plt.show() actually renders something."""
    import matplotlib.pyplot as plt

    plt.close("all")

    figure = plot_confusion_matrix(
        Y_TRUE,
        Y_PRED,
        model_name="RF",
        output_dir=tmp_path,
        show=True,
    )

    assert hasattr(figure, "number")


def test_plot_confusion_matrix_does_not_leak_pyplot_figures(tmp_path: Path) -> None:
    import matplotlib.pyplot as plt

    plt.close("all")

    plot_confusion_matrix(
        Y_TRUE,
        Y_PRED,
        model_name="RF",
        output_dir=tmp_path,
        show=True,
    )

    assert plt.get_fignums() == []
