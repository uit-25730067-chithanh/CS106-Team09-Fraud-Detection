"""Feature importance visualization comparing the two supervised models."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from matplotlib.figure import Figure


FIGURES_DIR = Path(__file__).resolve().parents[2] / "reports" / "figures"

# Nhóm đặc trưng dẫn xuất từ số dư tài khoản. Data card của PaySim khuyến cáo
# không dùng các cột số dư để phát hiện gian lận, nên phần đóng góp của nhóm này
# là con số cần đọc được ngay trên hình.
BALANCE_FEATURES = frozenset({
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "errorBalanceOrig",
    "errorBalanceDest",
    "is_drain_account",
    "amount_to_oldbalance_ratio",
})

_BALANCE_COLOR = "#C2413B"
_OTHER_COLOR = "#2F6690"

# Hình được chèn vào bản Word theo bề rộng trang (khoảng 15 cm). Tỷ lệ càng
# ngang thì chữ càng bị thu nhỏ khi ép về bề rộng đó, nên khung giữ gần vuông
# và cỡ chữ đặt lớn hơn mặc định của matplotlib.
_FIGSIZE = (9.5, 6.4)
_TICK_FONT_PT = 11
_VALUE_FONT_PT = 9.5
_TITLE_FONT_PT = 13
_AXIS_FONT_PT = 11


def _share_of_balance_group(importances: Mapping[str, float]) -> float:
    total = sum(importances.values())
    if total <= 0:
        raise ValueError("Tổng mức đóng góp phải lớn hơn 0")
    return sum(v for k, v in importances.items() if k in BALANCE_FEATURES) / total


def plot_feature_importance(
    importances_by_model: Mapping[str, Mapping[str, float]],
    save: bool = True,
    output_dir: str | Path = FIGURES_DIR,
) -> Figure:
    """Vẽ mức đóng góp đặc trưng của từng mô hình trên một panel riêng.

    Mỗi panel là một thang đo khác nhau (Gini với Random Forest, gain với
    XGBoost) nên không dùng chung trục. Màu phân biệt nhóm đặc trưng số dư với
    phần còn lại, và tỷ lệ đóng góp của nhóm đó được ghi ngay trên panel.
    """

    if not importances_by_model:
        raise ValueError("importances_by_model must contain at least one model")

    model_names = list(importances_by_model)
    figure = Figure(figsize=_FIGSIZE)
    axes = figure.subplots(1, len(model_names), squeeze=False)[0]

    for axis, name in zip(axes, model_names):
        importances = importances_by_model[name]
        if not importances:
            raise ValueError(f"Mô hình {name!r} không có dữ liệu mức đóng góp")

        # Kiểm tra trước khi vẽ để không để lại panel dở dang khi dữ liệu sai.
        share = _share_of_balance_group(importances)

        ordered = sorted(importances.items(), key=lambda item: item[1])
        labels = [feature for feature, _ in ordered]
        values = [value for _, value in ordered]
        colors = [
            _BALANCE_COLOR if feature in BALANCE_FEATURES else _OTHER_COLOR
            for feature in labels
        ]

        bars = axis.barh(labels, values, color=colors, height=0.72)
        axis.set_title(name, fontweight="bold", fontsize=_TITLE_FONT_PT)
        axis.set_xlabel("Mức đóng góp", fontsize=_AXIS_FONT_PT)
        axis.set_xlim(0, max(values) * 1.28)
        # Chừa một khoảng trống dưới thanh cuối để dòng chú thích tỷ lệ không
        # đè lên nhãn giá trị của đặc trưng nhỏ nhất.
        axis.set_ylim(-1.6, len(values) - 0.4)
        axis.grid(axis="x", alpha=0.25, linestyle="--")
        axis.tick_params(axis="y", labelsize=_TICK_FONT_PT)
        axis.tick_params(axis="x", labelsize=_AXIS_FONT_PT - 1)
        axis.bar_label(
            bars,
            labels=[f"{value:.4f}".replace(".", ",") for value in values],
            padding=3,
            fontsize=_VALUE_FONT_PT,
        )

        axis.text(
            0.97,
            0.04,
            f"Nhóm đặc trưng số dư: {share:.2%}".replace(".", ","),
            transform=axis.transAxes,
            ha="right",
            va="bottom",
            fontsize=_VALUE_FONT_PT + 0.5,
            color=_BALANCE_COLOR,
            fontweight="bold",
        )

    handles = [
        figure.add_subplot(111, visible=False).barh([0], [0], color=color)
        for color in (_BALANCE_COLOR, _OTHER_COLOR)
    ]
    figure.legend(
        handles,
        ["Đặc trưng dẫn xuất từ số dư", "Đặc trưng khác"],
        loc="lower center",
        ncols=2,
        frameon=False,
        fontsize=_AXIS_FONT_PT,
        bbox_to_anchor=(0.5, -0.01),
    )
    figure.tight_layout(rect=(0, 0.05, 1, 1))

    if save:
        output_path = Path(output_dir) / "feature_importance_comparison.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=300, bbox_inches="tight")

    return figure
