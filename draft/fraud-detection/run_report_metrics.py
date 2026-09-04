"""Phase 07: Tính lại toàn bộ chỉ số của Chương 5 từ artifact dự đoán đã lưu.

Script phục vụ phần báo cáo. Nó KHÔNG huấn luyện lại mô hình mà chỉ đọc nhãn
thật và các tệp dự đoán đã lưu, rồi gọi ``compute_metrics`` để mọi con số trong
Chương 5 đều truy được về một nguồn duy nhất.

Đầu ra:
  - ``reports/ch5_metrics_recomputed.csv`` — bảng chỉ số của 5 biến thể mô hình.
  - ``reports/figures/confusion_matrix_components.png`` — Hình 5.1.
  - ``reports/figures/feature_importance_comparison.png`` — Hình 5.2.
  - Bản in kiểm tra chồng lấn tập False Negative giữa các mô hình.

Bảng này là bằng chứng cho bản nháp báo cáo. Bảng so sánh chính thức
(``reports/model_comparison.csv``) thuộc Phase 05 và sẽ thay thế bảng này.

Author: Vũ Văn Duy
"""
import csv
import os
import pickle
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

from src.evaluation import compute_metrics, print_metrics
from src.evaluation.plot_confusion_components import plot_confusion_components
from src.evaluation.plot_feature_importance import plot_feature_importance
from src.utils import get_project_root, DATA_PROCESSED_DIR

REPORTS_DIR = "reports"
OUTPUT_CSV = "ch5_metrics_recomputed.csv"
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


def _load(path: str):
    with open(path, "rb") as f:
        return pickle.load(f)


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


def report_false_negative_overlap(y_true: np.ndarray, predictions: dict[str, dict]) -> None:
    """In phần giao và phần hợp của các tập False Negative giữa các mô hình."""
    fn_sets = {
        name: set(np.where((y_true == 1) & (np.asarray(pred["y_pred"]).astype(int) == 0))[0])
        for name, pred in predictions.items()
    }
    supervised = [name for name in fn_sets if name != "Autoencoder"]
    intersection = set.intersection(*(fn_sets[name] for name in supervised))
    union = set.union(*(fn_sets[name] for name in supervised))

    print("\n=== Chồng lấn False Negative ===")
    for name, indices in fn_sets.items():
        print(f"  {name}: {len(indices)} FN")
    print(f"  Bốn mô hình học có giám sát — giao: {len(intersection)} | hợp: {len(union)}")
    print(f"  Autoencoder bỏ sót {len(intersection & fn_sets['Autoencoder'])}/{len(intersection)} "
          "giao dịch trong phần giao đó")


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
    report_false_negative_overlap(y_test, predictions)


if __name__ == "__main__":
    main()
