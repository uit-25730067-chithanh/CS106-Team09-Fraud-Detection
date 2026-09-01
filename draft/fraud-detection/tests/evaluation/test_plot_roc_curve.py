"""Tests for ROC and Precision-Recall visualizations."""

from __future__ import annotations

from pathlib import Path

from src.evaluation.plot_roc_curve import plot_pr_curves, plot_roc_curves


MODEL_SCORES = {
    "Model A": [0.05, 0.25, 0.75, 0.95],
    "Model B": [0.20, 0.40, 0.60, 0.80],
}
Y_TRUE = [0, 0, 1, 1]


def test_plot_roc_curves_saves_combined_figure(tmp_path: Path) -> None:
    figure = plot_roc_curves(
        MODEL_SCORES,
        Y_TRUE,
        output_dir=tmp_path,
        show=False,
    )

    assert (tmp_path / "roc_curves_all.png").is_file()
    assert len(figure.axes) == 1
    assert len(figure.axes[0].lines) == 3  # Two models and the random baseline.


def test_plot_pr_curves_saves_combined_figure(tmp_path: Path) -> None:
    figure = plot_pr_curves(
        MODEL_SCORES,
        Y_TRUE,
        output_dir=tmp_path,
        show=False,
    )

    assert (tmp_path / "pr_curves_all.png").is_file()
    assert len(figure.axes) == 1
    assert len(figure.axes[0].lines) == 2


def test_plot_functions_can_skip_file_output(tmp_path: Path) -> None:
    plot_roc_curves(
        MODEL_SCORES,
        Y_TRUE,
        save=False,
        output_dir=tmp_path,
        show=False,
    )
    plot_pr_curves(
        MODEL_SCORES,
        Y_TRUE,
        save=False,
        output_dir=tmp_path,
        show=False,
    )

    assert list(tmp_path.iterdir()) == []
