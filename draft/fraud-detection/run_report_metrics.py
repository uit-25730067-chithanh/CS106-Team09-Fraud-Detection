"""Phase 07: Tính lại toàn bộ chỉ số của Chương 5 từ artifact dự đoán đã lưu.

Script phục vụ phần báo cáo. Nó KHÔNG huấn luyện lại mô hình mà chỉ đọc nhãn
thật và các tệp dự đoán đã lưu, rồi gọi ``compute_metrics`` để mọi con số trong
Chương 5 đều truy được về một nguồn duy nhất.

Đầu ra:
  - ``reports/ch5_metrics_recomputed.csv`` — bảng chỉ số của 5 biến thể mô hình.
  - ``reports/figures/confusion_matrix_components.png`` — Hình 5.1.
  - ``reports/figures/feature_importance_comparison.png`` — Hình 5.2.
  - ``reports/ch6_prevalence_projection.csv`` — hiệu năng quy chiếu về tỷ lệ
    gian lận gốc của PaySim, kèm khoảng tin cậy.
  - Bản in kiểm tra chồng lấn tập False Negative giữa các mô hình.

Bảng này là bằng chứng cho bản nháp báo cáo. Bảng so sánh chính thức
(``reports/model_comparison.csv``) thuộc Phase 05 và sẽ thay thế bảng này.

Author: Vũ Văn Duy (Refactored for modularity & NumPy 1.x/2.x compatibility)
"""

import csv
import os
import pickle
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

from src.evaluation import (
    ORIGINAL_PREVALENCE,
    compute_metrics,
    plot_confusion_components,
    plot_feature_importance,
    print_metrics,
    project_to_original_prevalence,
    report_false_negative_overlap,
)
from src.utils import DATA_PROCESSED_DIR, get_project_root

REPORTS_DIR = "reports"
OUTPUT_CSV = "ch5_metrics_recomputed.csv"
PROJECTION_CSV = "ch6_prevalence_projection.csv"

# Nhãn rút gọn cho Hình 5.1 và nhãn đầy đủ kèm thang đo cho Hình 5.2.
FIGURE_LABELS = {
    "Random Forest + SMOTENC": "RF-SMOTENC",
    "Random Forest + ADASYN": "RF-ADASYN",
    "XGBoost + SMOTENC": "XGB-SMOTENC",
    "XGBoost + ADASYN": "XGB-ADASYN",
    "Autoencoder": "Autoencoder",
}

IMPORTANCE_SOURCES = {
    "Random Forest + SMOTENC\n(mức giảm độ bất thuần Gini)": "rf_smote_feature_importance.csv",
    "XGBoost + SMOTENC\n(độ lợi trung bình)": "xgb_smote_feature_importance.csv",
}


class _CompatUnpickler(pickle.Unpickler):
    """Cầu nối tương thích unpickle giữa NumPy 2.x (nguồn lưu) và NumPy 1.x."""

    def find_class(self, module: str, name: str):
        if module.startswith("numpy._core"):
            module = module.replace("numpy._core", "numpy.core")
        return super().find_class(module, name)


def _load(path: str):
    with open(path, "rb") as f:
        return _CompatUnpickler(f).load()


def collect_predictions(reports_dir: str) -> dict[str, dict]:
    """Gom đầu ra dự đoán của 5 biến thể mô hình về một dict phẳng."""
    rf = _load(os.path.join(reports_dir, "rf_predictions.pkl"))
    xgb = _load(os.path.join(reports_dir, "xgb_predictions.pkl"))
    autoencoder = _load(os.path.join(reports_dir, "autoencoder_predictions.pkl"))

    return {
        "Random Forest + SMOTENC": rf["rf_smote"],
        "Random Forest + ADASYN": rf["rf_adasyn"],
        "XGBoost + SMOTENC": xgb["xgb_smote"],
        "XGBoost + ADASYN": xgb["xgb_adasyn"],
        "Autoencoder": autoencoder,
    }


def build_figures(y_true, predictions: dict[str, dict], reports_dir: str) -> None:
    """Sinh lại hai hình của Chương 5 từ cùng nguồn dữ liệu với bảng chỉ số."""
    plot_confusion_components(
        {FIGURE_LABELS[name]: pred["y_pred"] for name, pred in predictions.items()},
        y_true,
    )
    print("Saved figure -> reports/figures/confusion_matrix_components.png")

    importances = {}
    for label, filename in IMPORTANCE_SOURCES.items():
        with open(os.path.join(reports_dir, filename), encoding="utf-8") as f:
            importances[label] = {
                row["Feature"]: float(row["Importance"]) for row in csv.DictReader(f)
            }
    plot_feature_importance(importances)
    print("Saved figure -> reports/figures/feature_importance_comparison.png")


def main() -> None:
    print("=== Phase 07: Tính lại chỉ số cho Chương 5 ===")

    proj_root = get_project_root()
    reports_dir = os.path.join(proj_root, REPORTS_DIR)

    y_test = np.asarray(
        _load(os.path.join(proj_root, DATA_PROCESSED_DIR, "y_test.pkl"))
    ).astype(int)
    print(f"y_test: {y_test.shape[0]:,} giao dịch | fraud = {int(y_test.sum()):,}")

    predictions = collect_predictions(reports_dir)

    rows = []
    for name, pred in predictions.items():
        metrics = compute_metrics(y_test, pred["y_pred"], pred["y_prob"], model_name=name)
        print_metrics(metrics)
        rows.append(metrics)

    output_path = os.path.join(reports_dir, OUTPUT_CSV)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Saved recomputed metrics -> {REPORTS_DIR}/{OUTPUT_CSV}")

    build_figures(y_test, predictions, reports_dir)

    projection = project_to_original_prevalence(y_test, predictions, prevalence=ORIGINAL_PREVALENCE)
    projection_path = os.path.join(reports_dir, PROJECTION_CSV)
    with open(projection_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(projection[0].keys()))
        writer.writeheader()
        writer.writerows(projection)
    print(f"Saved prevalence projection -> {REPORTS_DIR}/{PROJECTION_CSV}")

    print(f"\n=== Hiệu năng quy chiếu về tỷ lệ gian lận gốc ({ORIGINAL_PREVALENCE:.6%}) ===")
    for row in projection:
        print(
            f"  {row['model']:<24} FP={row['false_positives']:>4} | "
            f"Precision {row['precision_test']:.4f} → {row['precision_original']:.4f} "
            f"(KTC 95%: {row['precision_original_low']:.4f}–{row['precision_original_high']:.4f}) | "
            f"{row['false_alarms_per_million']:,} cảnh báo nhầm mỗi triệu giao dịch"
        )

    report_false_negative_overlap(y_test, predictions)


if __name__ == "__main__":
    main()
