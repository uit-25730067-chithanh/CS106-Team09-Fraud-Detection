# Phase 05 — Evaluation & Model Comparison

**Parent plan:** [plan.md](./plan.md)  
**Depends on:** [Phase 03](./phase-03-model-random-forest.md) AND [Phase 04](./phase-04-model-xgboost-autoencoder.md) — cả 2 PASSED *(chạy metrics — Sprint 4)*  
**Early Start:** Viết scripts template từ **Sprint 2** — không cần data  
**Next phase:** [Phase 06 — Demo UI](./phase-06-demo-ui.md) + [Phase 07 — Report & PPT](./phase-07-report-ppt.md) (parallel)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Khang** |
| Priority | P0 — Required for báo cáo |
| Status | `passed` ✅ |
| Review | ⬜ Not reviewed |
| Estimated effort | 2–3 giờ |
| Sprint | Sprint 2–3 (viết scripts), Sprint 4 (chạy metrics) |

## ⚡ Early Start Tasks — Khang bắt đầu từ Sprint 2 (không cần đợi model)

> Viết 4 scripts template trong Sprint 2–3. Khi Sơn/Cẩm xong models (Sprint 4), chỉ cần **cắm model vào và chạy** — không viết code từ đầu.

| Task | Sprint | Ghi chú | Trạng thái |
|------|--------|---------|------------|
| Viết `src/evaluation/metrics_calculator.py` template | Sprint 2 | Test với dummy predictions | ✅ Hoàn thành |
| Viết `src/evaluation/plot_roc_curve.py` template | Sprint 2 | Test với dummy scores | ✅ Hoàn thành |
| Viết `src/evaluation/confusion_matrix_plot.py` template | Sprint 3 | TDD, 3 tests pass | ✅ Hoàn thành |
| Viết `src/evaluation/model_comparator.py` template | Sprint 3 | TDD, 3 tests pass | ✅ Hoàn thành |
| Chạy metrics cho cả 5 biến thể model (RF/XGB × SMOTENC/ADASYN + Autoencoder) | Sprint 4 | Dùng artifact `reports/*_predictions.pkl` có sẵn, không train lại | ✅ Hoàn thành |
| Tổng hợp bảng so sánh + export CSV | Sprint 4 | `reports/model_comparison.csv` | ✅ Hoàn thành |

### Evidence Early Start — Khang, Sprint 2 (29/08/2026)

- Đã tạo `metrics_calculator.py` với `compute_metrics()` và `print_metrics()`.
- Đã tạo `plot_roc_curve.py` với `plot_roc_curves()` và `plot_pr_curves()`.
- Đã export bốn hàm Sprint 2 qua `src/evaluation/__init__.py`.
- Kiểm thử dummy predictions/scores: `7 passed` trên Python 3.12.10, scikit-learn 1.9.0.
- Phase 05 vẫn `pending`; chưa chạy metrics model thật, chưa tạo figures báo cáo hoặc comparison CSV.

### Evidence Sprint 4 — Khang (06/09/2026)

- Đã tạo `src/evaluation/confusion_matrix_plot.py` (`plot_confusion_matrix`) và `src/evaluation/model_comparator.py` (`compare_models`, `save_comparison`) bằng TDD (viết test trước, xác nhận RED, rồi code tối thiểu để GREEN).
- Cả 2 module export qua `src/evaluation/__init__.py`. Toàn bộ `tests/evaluation` + `tests/demo`: **45 passed, 1 skipped** (skip do thiếu `python-docx`, không liên quan) trên Python 3.12.10 (venv dự án).
- Đã tạo `notebooks/06_evaluation_comparison.ipynb`, chạy **Restart & Run All** không lỗi (`jupyter nbconvert --execute`), không có cell nào raise exception.
- Notebook đọc `reports/rf_predictions.pkl`, `xgb_predictions.pkl`, `autoencoder_predictions.pkl` (bàn giao từ Sơn/Cẩm) + `data/processed/y_test.pkl` — KHÔNG train lại model.
- Số liệu tính ra khớp 100% với `reports/ch5_metrics_recomputed.csv` (Duy) vì cùng dùng `compute_metrics()` trên cùng artifact — xác nhận tính nhất quán giữa Phase 05 và báo cáo Chương 5.
- Output đã lưu: `reports/model_comparison.csv`, `reports/figures/roc_curves_all.png`, `pr_curves_all.png`, `confusion_matrix_rf-smotenc.png`, `confusion_matrix_rf-adasyn.png`, `confusion_matrix_xgb-smotenc.png`, `confusion_matrix_xgb-adasyn.png`, `confusion_matrix_autoencoder.png`.

## Context

Khang implement toàn bộ evaluation module: metrics, visualizations, và bảng so sánh tổng hợp. Output của phase này là figures và tables dùng trong báo cáo Word + PPT.

## Requirements

- Evaluate tất cả models trên cùng test set (X_test, y_test — không SMOTE)
- Metrics: Precision, Recall, F1-Score, ROC-AUC cho mỗi model
- Visualizations: Confusion Matrix (heatmap), ROC curves (tất cả models trên 1 plot)
- Bảng so sánh tổng hợp (chạy được in terminal và export CSV)
- Lưu tất cả figures vào `reports/figures/`

## Key Insights

- `classification_report` của sklearn cho đầy đủ per-class metrics
- Precision-Recall curve thường informative hơn ROC cho imbalanced data — nên vẽ cả 2
- Focus on **Class 1 (fraud) metrics** — Class 0 metrics gần 1.0 không có ý nghĩa nhiều

## 💡 Ý tưởng Đề xuất & Cải tiến Nâng cao (từ MY_IDEAS)

1. **Chuẩn mực hóa đường cong Precision-Recall (PR-AUC / Average Precision):**
   * Trong bài toán gian lận tài chính có độ mất cân bằng cao, đường cong **PR Curve** phản ánh thực chất khả năng đánh đổi giữa Precision và Recall mà không bị "thổi phồng" bởi số lượng lớn giao dịch hợp lệ (True Negatives) như ROC-AUC. Khang cần xuất cả `pr_curves_all.png` và tính chỉ số Average Precision (AP).
2. **Xây dựng Ma trận Chi phí Tài chính (Financial Cost Matrix):**
   * Bổ sung hàm tính toán thiệt hại thực tế ($) được cứu vãn:
     * $\text{Tiền cứu được (True Positive)} = \sum \text{amount của các vụ bắt đúng}$ (trung bình ~$1.47\text{ triệu USD}$/vụ).
     * $\text{Chi phí xác minh nhầm (False Positive)} = \text{Số lượng FP} \times \text{Chi phí kiểm tra thủ công}$ (~$5–10\text{ USD}$/giao dịch).
     * $\text{Thiệt hại bỏ sót (False Negative)} = \sum \text{amount của các vụ lọt lưới}$.
   * *Ý nghĩa:* Giúp bài báo cáo có giá trị ứng dụng thực tiễn cực cao, thuyết phục hoàn toàn hội đồng phản biện.
3. **So sánh liên trường phái (Cross-Paradigm Comparison):**
   * Tổng hợp bảng so sánh đối đầu giữa Supervised (RF, XGBoost) và Unsupervised Anomaly Detection (Autoencoder) trên cùng 1 biểu đồ radar hoặc bảng đa chiều.

## Related Files

```
draft/fraud-detection/
├── notebooks/
│   └── 06_evaluation_comparison.ipynb   ← [TẠO MỚI]
├── src/evaluation/
│   ├── __init__.py                       ← [TẠO MỚI]
│   ├── metrics_calculator.py            ← [TẠO MỚI]
│   ├── plot_roc_curve.py               ← [TẠO MỚI]
│   ├── confusion_matrix_plot.py        ← [TẠO MỚI]
│   └── model_comparator.py             ← [TẠO MỚI]
└── reports/
    ├── figures/                          ← [TẠO MỚI]
    │   ├── roc_curves_all.png
    │   ├── pr_curves_all.png
    │   ├── confusion_matrix_rf.png
    │   ├── confusion_matrix_xgb.png
    │   └── confusion_matrix_autoencoder.png
    └── model_comparison.csv             ← OUTPUT
```

## Implementation Steps

### Step 1 — `src/evaluation/__init__.py`

```python
from .metrics_calculator import compute_metrics, print_metrics
from .plot_roc_curve import plot_roc_curves, plot_pr_curves
from .confusion_matrix_plot import plot_confusion_matrix
from .model_comparator import compare_models

__all__ = [
    "compute_metrics", "print_metrics",
    "plot_roc_curves", "plot_pr_curves",
    "plot_confusion_matrix",
    "compare_models",
]
```

### Step 2 — `src/evaluation/metrics_calculator.py`

```python
"""Compute classification metrics for fraud detection models."""
import numpy as np
import pandas as pd
from sklearn.metrics import (
    f1_score, precision_score, recall_score,
    roc_auc_score, classification_report,
    average_precision_score,
)


def compute_metrics(
    y_true: np.ndarray | pd.Series,
    y_pred: np.ndarray,
    y_prob: np.ndarray,
    model_name: str = "Model",
) -> dict:
    """
    Compute all metrics for fraud detection evaluation.
    Focus on Class 1 (fraud) metrics.
    """
    return {
        "model": model_name,
        "precision_fraud": round(precision_score(y_true, y_pred, pos_label=1, zero_division=0), 4),
        "recall_fraud": round(recall_score(y_true, y_pred, pos_label=1, zero_division=0), 4),
        "f1_fraud": round(f1_score(y_true, y_pred, pos_label=1, zero_division=0), 4),
        "roc_auc": round(roc_auc_score(y_true, y_prob), 4),
        "pr_auc": round(average_precision_score(y_true, y_prob), 4),
    }


def print_metrics(metrics: dict) -> None:
    """Pretty-print metrics dict."""
    print(f"\n{'='*50}")
    print(f"  {metrics['model']}")
    print(f"{'='*50}")
    print(f"  Precision (Fraud): {metrics['precision_fraud']:.4f}")
    print(f"  Recall    (Fraud): {metrics['recall_fraud']:.4f}")
    print(f"  F1-Score  (Fraud): {metrics['f1_fraud']:.4f}")
    print(f"  ROC-AUC          : {metrics['roc_auc']:.4f}")
    print(f"  PR-AUC           : {metrics['pr_auc']:.4f}")
    print(f"{'='*50}\n")
```

### Step 3 — `src/evaluation/plot_roc_curve.py`

```python
"""ROC and Precision-Recall curve visualizations."""
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve
from pathlib import Path

FIGURES_DIR = "reports/figures"


def plot_roc_curves(models_dict: dict, y_true, save: bool = True) -> None:
    """
    Plot ROC curves for all models on one figure.
    
    models_dict = {"Model Name": y_prob_array, ...}
    """
    Path(FIGURES_DIR).mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    
    for name, y_prob in models_dict.items():
        fpr, tpr, _ = roc_curve(y_true, y_prob)
        roc_auc = auc(fpr, tpr)
        ax.plot(fpr, tpr, lw=2, label=f"{name} (AUC = {roc_auc:.4f})")
    
    ax.plot([0, 1], [0, 1], "k--", lw=1, label="Random")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves — All Models")
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    
    if save:
        path = f"{FIGURES_DIR}/roc_curves_all.png"
        plt.savefig(path, dpi=150, bbox_inches="tight")
        print(f"ROC curves saved → {path}")
    plt.show()


def plot_pr_curves(models_dict: dict, y_true, save: bool = True) -> None:
    """Plot Precision-Recall curves for all models."""
    Path(FIGURES_DIR).mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 6))
    
    for name, y_prob in models_dict.items():
        precision, recall, _ = precision_recall_curve(y_true, y_prob)
        pr_auc = auc(recall, precision)
        ax.plot(recall, precision, lw=2, label=f"{name} (PR-AUC = {pr_auc:.4f})")
    
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title("Precision-Recall Curves — All Models")
    ax.legend(loc="upper right")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    
    if save:
        path = f"{FIGURES_DIR}/pr_curves_all.png"
        plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.show()
```

### Step 4 — `src/evaluation/confusion_matrix_plot.py`

```python
"""Confusion matrix heatmap visualization."""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from pathlib import Path

FIGURES_DIR = "reports/figures"


def plot_confusion_matrix(
    y_true, y_pred,
    model_name: str = "Model",
    save: bool = True,
) -> None:
    """Plot confusion matrix as annotated heatmap."""
    Path(FIGURES_DIR).mkdir(parents=True, exist_ok=True)
    cm = confusion_matrix(y_true, y_pred)
    
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(
        cm, annot=True, fmt="d",
        cmap="Blues", ax=ax,
        xticklabels=["Normal", "Fraud"],
        yticklabels=["Normal", "Fraud"],
    )
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title(f"Confusion Matrix — {model_name}")
    plt.tight_layout()
    
    if save:
        slug = model_name.lower().replace(" ", "_")
        path = f"{FIGURES_DIR}/confusion_matrix_{slug}.png"
        plt.savefig(path, dpi=150, bbox_inches="tight")
        print(f"Confusion matrix saved → {path}")
    plt.show()
```

### Step 5 — `src/evaluation/model_comparator.py`

```python
"""Cross-model performance comparison table."""
import pandas as pd


def compare_models(metrics_list: list[dict]) -> pd.DataFrame:
    """
    Build comparison DataFrame from list of metrics dicts.
    Sorts by F1-Score descending.
    """
    df = pd.DataFrame(metrics_list)
    df = df.sort_values("f1_fraud", ascending=False).reset_index(drop=True)
    
    # Rename columns for readability
    df.columns = [c.replace("_", " ").title() for c in df.columns]
    return df


def save_comparison(df: pd.DataFrame, path: str = "reports/model_comparison.csv") -> None:
    """Save comparison table to CSV."""
    df.to_csv(path, index=False)
    print(f"Comparison table saved → {path}")
```

### Step 6 — `notebooks/06_evaluation_comparison.ipynb`

```
## 0. Imports & Setup
## 1. Load All Models & Test Data
   - Load rf_smote, xgb_smote, autoencoder from models/
   - Load X_test, y_test from data/processed/
## 2. Generate Predictions (for all models)
## 3. Metrics per Model (compute_metrics + print_metrics)
## 4. Confusion Matrices (1 per model — saved to reports/figures/)
## 5. ROC Curves (all models on 1 plot)
## 6. Precision-Recall Curves (all models on 1 plot)
## 7. Model Comparison Table
   - DataFrame sorted by F1
   - Export to reports/model_comparison.csv
## 8. Kết luận
   - Best model recommendation với lý do
   - Trade-offs giữa các model
```

## Checklist

- [x] `src/evaluation/` — 4 scripts tạo xong
- [x] Metrics computed cho cả 5 biến thể: RF-SMOTENC, RF-ADASYN, XGB-SMOTENC, XGB-ADASYN, Autoencoder
- [x] Confusion matrix figures saved: `rf-smotenc`, `rf-adasyn`, `xgb-smotenc`, `xgb-adasyn`, `autoencoder`
- [x] `reports/figures/roc_curves_all.png` saved
- [x] `reports/figures/pr_curves_all.png` saved
- [x] `reports/model_comparison.csv` saved
- [x] Notebook chạy Restart & Run All không lỗi (`jupyter nbconvert --execute`, 0 cell lỗi)
- [x] Bảng so sánh có đủ 5 models × 5 metrics
- [x] Kết luận chọn best model có giải thích rõ ràng

## Success Criteria

| Criterion | Expected | Evidence |
|-----------|---------|---------|
| All models evaluated | ✅ | 5/5 biến thể (RF×2, XGB×2, Autoencoder) — xem notebook 06 §2 |
| Best model F1 (fraud) | > 0.80 | RF-SMOTENC F1 = 0.9973 |
| Comparison CSV exported | ✅ | `reports/model_comparison.csv`, 5 hàng × 6 cột |
| All figures saved | 5 PNGs | 2 combined (ROC/PR) + 5 confusion matrix = 7 PNGs |

## Evidence Section *(điền sau khi làm)*

```
RF SMOTENC  — Precision: 0.9994  Recall: 0.9951  F1: 0.9973  ROC-AUC: 0.9994  PR-AUC: 0.9983
RF ADASYN   — Precision: 0.9982  Recall: 0.9951  F1: 0.9966  ROC-AUC: 0.9992  PR-AUC: 0.9978
XGB SMOTENC — Precision: 0.9976  Recall: 0.9951  F1: 0.9963  ROC-AUC: 0.9993  PR-AUC: 0.9969
XGB ADASYN  — Precision: 0.9957  Recall: 0.9951  F1: 0.9954  ROC-AUC: 0.9994  PR-AUC: 0.9976
Autoencoder — Precision: 0.3822  Recall: 0.7523  F1: 0.5069  ROC-AUC: 0.9318  PR-AUC: 0.5973
Best model: Random Forest + SMOTENC
Saved figures: 7 (roc_curves_all, pr_curves_all, confusion_matrix_{rf-smotenc,rf-adasyn,xgb-smotenc,xgb-adasyn,autoencoder})
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Autoencoder artifacts missing | Low | High | Verify autoencoder.h5 + threshold.txt before running |
| Models from different environments (pickle compat) | Low | Medium | Ensure same Python + sklearn version |
| Confusion matrix wrong orientation | Low | Low | Always use (actual, predicted) order |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ Hoàn thành

```
Hoàn thành: 06/09/2026
Người thực hiện: Khang
Best model: Random Forest + SMOTENC (F1=0.9973, ROC-AUC=0.9994)
Key findings:
- Cả 4 biến thể có giám sát (RF/XGB × SMOTENC/ADASYN) đạt F1 > 0.995 và ROC-AUC > 0.999 — sát nhau, khác biệt chưa chắc có ý nghĩa thống kê (xem ch6_prevalence_projection.csv của Duy).
- Autoencoder (không giám sát) đạt Recall=0.7523/ROC-AUC=0.9318 nhưng Precision chỉ 0.3822 — đánh đổi hợp lý để không cần nhãn fraud khi train.
- Toàn bộ số liệu tái lập 100% khớp reports/ch5_metrics_recomputed.csv (Duy) vì dùng chung compute_metrics() trên cùng artifact dự đoán — không có sai lệch giữa Phase 05 và báo cáo Chương 5.
```

## Commit

```bash
git add src/evaluation/ notebooks/06_evaluation_comparison.ipynb \
        reports/figures/ reports/model_comparison.csv
git commit -m "feat(phase05): evaluation + model comparison, all metrics and figures saved"
```
