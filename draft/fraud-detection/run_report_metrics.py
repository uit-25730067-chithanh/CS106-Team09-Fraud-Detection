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
from scipy.stats import beta
from sklearn.metrics import confusion_matrix

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
# Tỷ lệ gian lận của PaySim trước khi downsampling: 8.213 / 6.362.620.
ORIGINAL_PREVALENCE = 8213 / 6362620
PROJECTION_CSV = "ch6_prevalence_projection.csv"
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


def _clopper_pearson(successes: int, trials: int, alpha: float = 0.05) -> tuple[float, float]:
    """Khoảng tin cậy chính xác cho một tỷ lệ nhị thức."""

    lower = beta.ppf(alpha / 2, successes, trials - successes + 1) if successes else 0.0
    upper = beta.ppf(1 - alpha / 2, successes + 1, trials - successes) if successes < trials else 1.0
    return float(lower), float(upper)


def _precision_at(prevalence: float, tpr: float, fpr: float) -> float:
    """Precision suy ra từ TPR và FPR ở một tỷ lệ dương tính cho trước."""

    denominator = prevalence * tpr + (1 - prevalence) * fpr
    return prevalence * tpr / denominator if denominator else float("nan")


def project_to_original_prevalence(y_true, predictions: dict[str, dict]) -> list[dict]:
    """Quy chiếu Precision về tỷ lệ gian lận gốc của PaySim.

    Downsampling chỉ lấy mẫu ngẫu nhiên lớp bình thường nên không làm đổi phân
    bố có điều kiện của từng lớp. TPR và FPR đo trên tập kiểm tra vì thế vẫn
    dùng được cho phân bố gốc, chỉ Precision là phụ thuộc tỷ lệ lớp.
    """

    rows = []
    for name, pred in predictions.items():
        tn, fp, fn, tp = confusion_matrix(
            y_true, np.asarray(pred["y_pred"]).astype(int), labels=[0, 1]
        ).ravel()
        tpr, negatives = tp / (tp + fn), fp + tn
        fpr = fp / negatives
        fpr_low, fpr_high = _clopper_pearson(int(fp), int(negatives))

        rows.append({
            "model": name,
            "tpr": round(tpr, 4),
            "false_positives": int(fp),
            "fpr": f"{fpr:.3e}",
            "precision_test": round(tp / (tp + fp), 4),
            "precision_original": round(_precision_at(ORIGINAL_PREVALENCE, tpr, fpr), 4),
            "precision_original_low": round(_precision_at(ORIGINAL_PREVALENCE, tpr, fpr_high), 4),
            "precision_original_high": round(_precision_at(ORIGINAL_PREVALENCE, tpr, fpr_low), 4),
            "false_alarms_per_million": round((1 - ORIGINAL_PREVALENCE) * fpr * 1e6),
        })
    return rows


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

    projection = project_to_original_prevalence(y_test, predictions)
    projection_path = os.path.join(reports_dir, PROJECTION_CSV)
    with open(projection_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(projection[0].keys()))
        writer.writeheader()
        writer.writerows(projection)
    print(f"Saved prevalence projection -> {REPORTS_DIR}/{PROJECTION_CSV}")

    print(f"\n=== Hiệu năng quy chiếu về tỷ lệ gian lận gốc ({ORIGINAL_PREVALENCE:.6%}) ===")
    for row in projection:
        print(f"  {row['model']:<24} FP={row['false_positives']:>4} | "
              f"Precision {row['precision_test']:.4f} → {row['precision_original']:.4f} "
              f"(KTC 95%: {row['precision_original_low']:.4f}–{row['precision_original_high']:.4f}) | "
              f"{row['false_alarms_per_million']:,} cảnh báo nhầm mỗi triệu giao dịch")

    report_false_negative_overlap(y_test, predictions)


if __name__ == "__main__":
    main()
