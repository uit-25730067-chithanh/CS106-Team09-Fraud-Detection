"""Tests for the feature importance comparison visualization."""

from __future__ import annotations

from pathlib import Path

import pytest

from src.evaluation.plot_feature_importance import (
    BALANCE_FEATURES,
    plot_feature_importance,
)


# Nhóm số dư chiếm 0,75 trên tổng 1,00 để phần trăm chú thích dễ kiểm chứng.
IMPORTANCES = {
    "Mô hình A": {
        "errorBalanceOrig": 0.50,
        "oldbalanceOrg": 0.25,
        "amount": 0.15,
        "step": 0.10,
    },
    "Mô hình B": {
        "newbalanceOrig": 0.60,
        "hour_of_day": 0.40,
    },
}


def test_one_panel_per_model_and_saves_figure(tmp_path: Path) -> None:
    figure = plot_feature_importance(IMPORTANCES, output_dir=tmp_path)

    assert (tmp_path / "feature_importance_comparison.png").is_file()
    # Hai panel dữ liệu cộng với một axes ẩn chỉ dùng để dựng chú giải.
    data_axes = [axis for axis in figure.axes if axis.get_visible()]
    assert len(data_axes) == 2
    assert [axis.get_title() for axis in data_axes] == ["Mô hình A", "Mô hình B"]


def test_bars_sorted_ascending_within_each_panel(tmp_path: Path) -> None:
    figure = plot_feature_importance(IMPORTANCES, output_dir=tmp_path)
    panel = [axis for axis in figure.axes if axis.get_title() == "Mô hình A"][0]

    widths = [bar.get_width() for bar in panel.containers[0]]
    assert widths == sorted(widths)
    assert widths[-1] == pytest.approx(0.50)


def test_balance_features_use_a_distinct_colour(tmp_path: Path) -> None:
    figure = plot_feature_importance(IMPORTANCES, output_dir=tmp_path)
    panel = [axis for axis in figure.axes if axis.get_title() == "Mô hình A"][0]

    labels = [label.get_text() for label in panel.get_yticklabels()]
    colours = [bar.get_facecolor() for bar in panel.containers[0]]
    by_label = dict(zip(labels, colours))

    assert by_label["errorBalanceOrig"] == by_label["oldbalanceOrg"]
    assert by_label["amount"] == by_label["step"]
    assert by_label["errorBalanceOrig"] != by_label["amount"]


def test_annotates_share_of_balance_group(tmp_path: Path) -> None:
    figure = plot_feature_importance(IMPORTANCES, output_dir=tmp_path)
    panel = [axis for axis in figure.axes if axis.get_title() == "Mô hình A"][0]

    notes = [text.get_text() for text in panel.texts if "số dư" in text.get_text()]
    assert notes == ["Nhóm đặc trưng số dư: 75,00%"]


def test_balance_group_covers_every_balance_derived_feature() -> None:
    assert "amount_to_oldbalance_ratio" in BALANCE_FEATURES
    assert "is_drain_account" in BALANCE_FEATURES
    assert "amount" not in BALANCE_FEATURES
    assert "type_TRANSFER" not in BALANCE_FEATURES


def test_can_skip_file_output(tmp_path: Path) -> None:
    plot_feature_importance(IMPORTANCES, save=False, output_dir=tmp_path)

    assert list(tmp_path.iterdir()) == []


def test_rejects_empty_input(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="at least one model"):
        plot_feature_importance({}, save=False, output_dir=tmp_path)

    with pytest.raises(ValueError, match="không có dữ liệu"):
        plot_feature_importance({"Rỗng": {}}, save=False, output_dir=tmp_path)


def test_rejects_zero_total_importance(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="lớn hơn 0"):
        plot_feature_importance(
            {"Bằng không": {"amount": 0.0, "step": 0.0}},
            save=False,
            output_dir=tmp_path,
        )
