"""Separate confusion-matrix component visualizations for model comparison."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from matplotlib.figure import Figure
from sklearn.metrics import confusion_matrix


FIGURES_DIR = Path(__file__).resolve().parents[2] / "reports" / "figures"
_COMPONENTS = (
    ("TN", "True Negative"),
    ("FP", "False Positive"),
    ("FN", "False Negative"),
    ("TP", "True Positive"),
)
_DISPLAY_LABELS = {
    "RF-SMOTENC": "RF\nSMOTENC",
    "RF-ADASYN": "RF\nADASYN",
    "XGB-SMOTENC": "XGB\nSMOTENC",
    "XGB-ADASYN": "XGB\nADASYN",
    "Autoencoder": "Autoencoder",
}
# Panel lỗi có thể lệch tới ba bậc độ lớn (ví dụ FP: 1 và 1.998). Trên thang
# tuyến tính các cột nhỏ bị dí sát trục và không còn so sánh được với nhau.
_ERROR_COMPONENTS = ("FP", "FN")
_LOG_SCALE_SPREAD = 20


def _needs_log_scale(key: str, values: list[int]) -> bool:
    """Chỉ chuyển sang thang log cho panel lỗi khi khoảng giá trị quá rộng."""

    if key not in _ERROR_COMPONENTS or min(values) <= 0:
        return False
    return max(values) / min(values) >= _LOG_SCALE_SPREAD


def plot_confusion_components(
    models_dict: dict[str, Any],
    y_true: Any,
    save: bool = True,
    output_dir: str | Path = FIGURES_DIR,
) -> Figure:
    """Plot TN, FP, FN, and TP separately so each component keeps a readable scale."""

    if not models_dict:
        raise ValueError("models_dict must contain at least one model")

    expected_length = len(y_true)
    component_values: dict[str, list[int]] = {key: [] for key, _ in _COMPONENTS}
    for model_name, y_pred in models_dict.items():
        if len(y_pred) != expected_length:
            raise ValueError(
                f"Predictions for {model_name!r} must have the same number of samples as y_true"
            )
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
        for key, value in zip(component_values, (tn, fp, fn, tp)):
            component_values[key].append(int(value))

    figure = Figure(figsize=(12, 8))
    axes = figure.subplots(2, 2)
    model_names = list(models_dict)
    display_names = [_DISPLAY_LABELS.get(name, name) for name in model_names]
    colors = ("#2F6690", "#D97706", "#C2413B", "#2E7D32")

    for axis, (key, full_name), color in zip(axes.flat, _COMPONENTS, colors):
        values = component_values[key]
        bars = axis.bar(display_names, values, color=color, width=0.68)
        axis.set_title(f"{full_name} ({key})", fontweight="bold")
        axis.set_xlabel("Mô hình")
        axis.grid(axis="y", alpha=0.25, linestyle="--")
        axis.tick_params(axis="x", labelrotation=0, labelsize=9, pad=3)
        if _needs_log_scale(key, values):
            axis.set_yscale("log")
            axis.set_ylim(0.5, max(values) * 4)
            axis.set_ylabel("Số giao dịch (thang log)")
        else:
            axis.set_ylim(0, max(values) * 1.18 if max(values) else 1)
            axis.set_ylabel("Số giao dịch")
        axis.bar_label(bars, labels=[f"{value:,}".replace(",", ".") for value in values], padding=3)

    figure.suptitle(
        "So sánh các thành phần ma trận nhầm lẫn theo mô hình",
        fontsize=15,
        fontweight="bold",
    )
    figure.tight_layout(rect=(0, 0, 1, 0.95))

    if save:
        output_path = Path(output_dir) / "confusion_matrix_components.png"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(output_path, dpi=300, bbox_inches="tight")

    return figure
