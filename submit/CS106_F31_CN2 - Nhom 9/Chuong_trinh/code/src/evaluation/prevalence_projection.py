"""Prevalence projection and false negative overlap analysis for model evaluation."""

from __future__ import annotations

import numpy as np
from scipy.stats import beta
from sklearn.metrics import confusion_matrix

# Tỷ lệ gian lận của PaySim trước khi downsampling: 8.213 / 6.362.620.
ORIGINAL_PREVALENCE = 8213 / 6362620


def clopper_pearson(successes: int, trials: int, alpha: float = 0.05) -> tuple[float, float]:
    """Khoảng tin cậy chính xác cho một tỷ lệ nhị thức."""
    if trials <= 0:
        raise ValueError("Số phép thử trials phải lớn hơn 0")
    if successes < 0 or successes > trials:
        raise ValueError("Số thành công successes phải nằm trong [0, trials]")

    lower = beta.ppf(alpha / 2, successes, trials - successes + 1) if successes else 0.0
    upper = beta.ppf(1 - alpha / 2, successes + 1, trials - successes) if successes < trials else 1.0
    return float(lower), float(upper)


def precision_at(prevalence: float, tpr: float, fpr: float) -> float:
    """Precision suy ra từ TPR và FPR ở một tỷ lệ dương tính cho trước."""
    if not (0.0 <= prevalence <= 1.0):
        raise ValueError("prevalence phải nằm trong [0, 1]")
    if not (0.0 <= tpr <= 1.0) or not (0.0 <= fpr <= 1.0):
        raise ValueError("tpr và fpr phải nằm trong [0, 1]")

    denominator = prevalence * tpr + (1 - prevalence) * fpr
    return prevalence * tpr / denominator if denominator > 0 else float("nan")


def project_to_original_prevalence(
    y_true: np.ndarray | list[int],
    predictions: dict[str, dict],
    prevalence: float = ORIGINAL_PREVALENCE,
) -> list[dict]:
    """Quy chiếu Precision về tỷ lệ gian lận gốc của PaySim.

    Downsampling chỉ lấy mẫu ngẫu nhiên lớp bình thường nên không làm đổi phân
    bố có điều kiện của từng lớp. TPR và FPR đo trên tập kiểm tra vì thế vẫn
    dùng được cho phân bố gốc, chỉ Precision là phụ thuộc tỷ lệ lớp.
    """
    y_true_arr = np.asarray(y_true).astype(int)
    rows = []

    for name, pred in predictions.items():
        y_pred = np.asarray(pred["y_pred"]).astype(int)
        tn, fp, fn, tp = confusion_matrix(y_true_arr, y_pred, labels=[0, 1]).ravel()
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        negatives = fp + tn
        fpr = fp / negatives if negatives > 0 else 0.0
        fpr_low, fpr_high = clopper_pearson(int(fp), int(negatives))

        rows.append({
            "model": name,
            "tpr": round(tpr, 4),
            "false_positives": int(fp),
            "fpr": f"{fpr:.3e}",
            "precision_test": round(tp / (tp + fp), 4) if (tp + fp) > 0 else 0.0,
            "precision_original": round(precision_at(prevalence, tpr, fpr), 4),
            "precision_original_low": round(precision_at(prevalence, tpr, fpr_high), 4),
            "precision_original_high": round(precision_at(prevalence, tpr, fpr_low), 4),
            "false_alarms_per_million": round((1 - prevalence) * fpr * 1e6),
        })
    return rows


def report_false_negative_overlap(y_true: np.ndarray, predictions: dict[str, dict]) -> None:
    """In phần giao và phần hợp của các tập False Negative giữa các mô hình."""
    y_true_arr = np.asarray(y_true).astype(int)
    fn_sets = {
        name: set(np.where((y_true_arr == 1) & (np.asarray(pred["y_pred"]).astype(int) == 0))[0])
        for name, pred in predictions.items()
    }
    supervised = [name for name in fn_sets if name != "Autoencoder"]
    intersection = set.intersection(*(fn_sets[name] for name in supervised)) if supervised else set()
    union = set.union(*(fn_sets[name] for name in supervised)) if supervised else set()

    print("\n=== Chồng lấn False Negative ===")
    for name, indices in fn_sets.items():
        print(f"  {name}: {len(indices)} FN")
    if supervised:
        print(f"  Bốn mô hình học có giám sát — giao: {len(intersection)} | hợp: {len(union)}")
    if "Autoencoder" in fn_sets and intersection:
        print(
            f"  Autoencoder bỏ sót {len(intersection & fn_sets['Autoencoder'])}/{len(intersection)} "
            "giao dịch trong phần giao đó"
        )
