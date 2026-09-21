"""Tests for the separated confusion-matrix component visualization."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.evaluation.plot_confusion_components import plot_confusion_components


Y_TRUE = [0, 0, 0, 0, 1, 1, 1, 1]
MODEL_PREDICTIONS = {
    # Một FP, một FN.
    "RF-SMOTENC": [0, 0, 0, 1, 0, 1, 1, 1],
    # Cảnh báo nhầm nhiều hơn hẳn, tạo khoảng cách bậc độ lớn ở panel FP.
    "Autoencoder": [1, 1, 1, 1, 0, 0, 1, 1],
}


def test_plots_four_components_and_saves_figure(tmp_path: Path) -> None:
    figure = plot_confusion_components(MODEL_PREDICTIONS, Y_TRUE, output_dir=tmp_path)

    assert (tmp_path / "confusion_matrix_components.png").is_file()
    assert len(figure.axes) == 4
    assert [axis.get_title() for axis in figure.axes] == [
        "True Negative (TN)",
        "False Positive (FP)",
        "False Negative (FN)",
        "True Positive (TP)",
    ]


def test_bar_heights_match_confusion_counts(tmp_path: Path) -> None:
    figure = plot_confusion_components(MODEL_PREDICTIONS, Y_TRUE, output_dir=tmp_path)

    heights = {
        axis.get_title(): [bar.get_height() for bar in axis.containers[0]]
        for axis in figure.axes
    }

    assert heights["True Negative (TN)"] == [3, 0]
    assert heights["False Positive (FP)"] == [1, 4]
    assert heights["False Negative (FN)"] == [1, 2]
    assert heights["True Positive (TP)"] == [3, 2]


def test_error_panels_use_log_scale_only_when_spread_is_wide(tmp_path: Path) -> None:
    wide = {"A": [0, 0, 0, 0, 0, 1, 1, 1], "B": [1, 1, 1, 1, 1, 1, 1, 1]}
    figure = plot_confusion_components(wide, Y_TRUE, output_dir=tmp_path)
    scales = {axis.get_title(): axis.get_yscale() for axis in figure.axes}

    # FP chênh 0 và 4 nên còn giá trị 0, giữ thang tuyến tính.
    assert scales["False Positive (FP)"] == "linear"
    # FN chênh 1 và 0 nên cũng tuyến tính, còn TN/TP luôn tuyến tính.
    assert scales["True Negative (TN)"] == "linear"
    assert scales["True Positive (TP)"] == "linear"


def test_log_scale_applies_to_error_panel_with_large_spread(tmp_path: Path) -> None:
    y_true = [0] * 100 + [1] * 10
    spread = {
        "Tốt": [0] * 100 + [1] * 10,
        "Kém": [1] * 60 + [0] * 40 + [1] * 10,
    }
    spread["Tốt"] = [0] * 99 + [1] + [1] * 10  # đúng 1 FP

    figure = plot_confusion_components(spread, y_true, output_dir=tmp_path)
    scales = {axis.get_title(): axis.get_yscale() for axis in figure.axes}

    assert scales["False Positive (FP)"] == "log"
    assert scales["True Negative (TN)"] == "linear"


def test_can_skip_file_output(tmp_path: Path) -> None:
    plot_confusion_components(MODEL_PREDICTIONS, Y_TRUE, save=False, output_dir=tmp_path)

    assert list(tmp_path.iterdir()) == []


def test_rejects_empty_models_dict(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="at least one model"):
        plot_confusion_components({}, Y_TRUE, save=False, output_dir=tmp_path)


def test_rejects_prediction_length_mismatch(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="same number of samples"):
        plot_confusion_components(
            {"Sai độ dài": [0, 1]}, Y_TRUE, save=False, output_dir=tmp_path
        )
