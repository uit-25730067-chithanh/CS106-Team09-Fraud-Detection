# Phase 03 — Modeling: Random Forest

**Parent plan:** [plan.md](./plan.md)  
**Depends on:** [Phase 02](./phase-02-imbalance-handling.md) — PASSED  
**Parallel with:** [Phase 04](./phase-04-model-xgboost-autoencoder.md)  
**Next phase:** [Phase 05 — Evaluation](./phase-05-evaluation-comparison.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Sơn** |
| Priority | P0 — Required model (baseline bắt buộc) |
| Status | `passed` ✅ |
| Review | ✅ Evidence-based |
| Estimated effort | 2–3 giờ |
| Sprint | Sprint 3 |

## Context

Random Forest là model baseline bắt buộc của đề. Sơn train RF với cả SMOTE và ADASYN data để so sánh, lưu model artifacts, và output predictions cho Phase 05.

## Requirements

- Train RF với SMOTE data (primary)
- Train RF với ADASYN data (secondary, để so sánh)
- Hyperparameter tuning bằng GridSearchCV hoặc RandomizedSearchCV
- Lưu model artifacts: `models/rf_smote.pkl`, `models/rf_adasyn.pkl`
- Lưu predictions: `reports/rf_predictions.pkl`

## Key Insights

- RF robust với imbalanced data ngay cả không dùng SMOTE (class_weight='balanced' option)
- `n_estimators=100–200` là good starting point
- Evaluation PHẢI dùng F1-Score và ROC-AUC, không phải Accuracy

## 💡 Ý tưởng Đề xuất & Cải tiến Nâng cao (từ MY_IDEAS)

1. **Thử nghiệm `class_weight='balanced_subsample'`:**
   * Thay vì chỉ dùng `class_weight='balanced'` cố định toàn cục, thử nghiệm `'balanced_subsample'` để tự động tính toán lại trọng số cân bằng lớp trên từng cây con (bootstrap sample), giúp Random Forest học tốt hơn các đặc trưng vi mô của nhóm thiểu số.
2. **Khai thác Feature Importance chuyên sâu:**
   * Trích xuất và trực quan hóa bảng xếp hạng độ quan trọng của đặc trưng (MDI / Permutation Importance).
   * Kiểm chứng xem 2 biến sai số `errorBalanceOrig`, `errorBalanceDest` có lọt vào Top 3 thuộc tính đóng góp lớn nhất vào quyết định phân loại hay không.
3. **Kiểm soát độ sâu để chống học vẹt (Anti-Overfitting Tuning):**
   * Do dữ liệu sau SMOTE có thể chứa các điểm ngoại lai nội suy, cần ràng buộc chặt chẽ `max_depth` (khoảng 15–20), `min_samples_split >= 10` và `min_samples_leaf >= 4` để cây không bị overfit vào dữ liệu nhân tạo.

## Related Files

```
draft/fraud-detection/
├── notebooks/
│   └── 03_model_random_forest.ipynb    ← [TẠO MỚI]
├── src/models/
│   ├── __init__.py                      ← [TẠO MỚI]
│   └── random_forest_model.py          ← [TẠO MỚI]
└── reports/
    ├── rf_predictions.pkl              ← OUTPUT
    ├── rf_feature_importance.csv       ← OUTPUT
    └── rf_model_summary.txt            ← OUTPUT
```

**Saved model artifacts (nên lưu riêng thư mục `models/`):**
```
draft/fraud-detection/
└── models/                    ← [TẠO MỚI thư mục]
    ├── rf_smote.pkl
    └── rf_adasyn.pkl
```

## Implementation Steps

### Step 1 — `src/models/__init__.py`

```python
from .random_forest_model import train_random_forest, load_model, predict

__all__ = ["train_random_forest", "load_model", "predict"]
```

### Step 2 — `src/models/random_forest_model.py`

```python
"""Random Forest Classifier for fraud detection."""
import pickle
import time
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from src.utils import RANDOM_STATE

MODEL_DIR = "models"


def train_random_forest(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    tune: bool = True,
    random_state: int = RANDOM_STATE,
) -> tuple[RandomForestClassifier, dict]:
    """
    Train Random Forest with optional hyperparameter tuning.
    Returns: (fitted_model, training_info_dict)
    """
    Path(MODEL_DIR).mkdir(exist_ok=True)
    start = time.time()
    
    if tune:
        # Giảm n_estimators để tuning nhanh hơn; không dùng class_weight='balanced' trên dữ liệu đã SMOTE
        param_grid = {
            "n_estimators": [50, 100, 150],
            "max_depth": [None, 10, 20],
            "min_samples_split": [2, 5],
        }
        base_rf = RandomForestClassifier(random_state=random_state, n_jobs=-1)
        search = RandomizedSearchCV(
            base_rf, param_grid,
            n_iter=8,  # Giảm bớt số iteration để chạy nhanh hơn
            cv=3,
            scoring="f1",   # Dùng F1-Score làm metric tối ưu
            random_state=random_state,
            n_jobs=-1,
            verbose=1,
        )
        search.fit(X_train, y_train)
        model = search.best_estimator_
        best_params = search.best_params_
    else:
        # Khi train mặc định trên dữ liệu SMOTE/ADASYN, không cần class_weight='balanced'
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=random_state,
            n_jobs=-1,
        )
        model.fit(X_train, y_train)
        best_params = model.get_params()
    
    elapsed = time.time() - start
    info = {
        "best_params": best_params,
        "training_time_sec": round(elapsed, 2),
        "n_features": X_train.shape[1],
        "train_samples": len(X_train),
    }
    return model, info


def save_model(model: RandomForestClassifier, name: str) -> str:
    """Save model to models/{name}.pkl. Returns path."""
    path = f"{MODEL_DIR}/{name}.pkl"
    with open(path, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved → {path}")
    return path


def load_model(name: str) -> RandomForestClassifier:
    """Load model from models/{name}.pkl."""
    path = f"{MODEL_DIR}/{name}.pkl"
    with open(path, "rb") as f:
        return pickle.load(f)


def predict(model: RandomForestClassifier, X_test: pd.DataFrame) -> dict:
    """Return predictions dict with y_pred and y_prob."""
    return {
        "y_pred": model.predict(X_test),
        "y_prob": model.predict_proba(X_test)[:, 1],
    }


def get_feature_importance(
    model: RandomForestClassifier,
    feature_names: list,
    top_n: int = 15,
) -> pd.DataFrame:
    """Return top N feature importances as DataFrame."""
    df = pd.DataFrame({
        "feature": feature_names,
        "importance": model.feature_importances_,
    }).sort_values("importance", ascending=False).head(top_n)
    return df
```

### Step 3 — `notebooks/03_model_random_forest.ipynb`

```
## 0. Imports & Setup (RANDOM_STATE = 42)
## 1. Load Processed Data
   - X_train (from data/processed/ — unbalanced original)
   - X_train_smote (SMOTE version)
   - X_train_adasyn (ADASYN version)
   - X_test, y_test (giữ nguyên, không SMOTE)
## 2. Train RF on SMOTE data (primary)
   - RandomizedSearchCV tuning
   - Best params
   - Training time
## 3. Train RF on ADASYN data (comparison)
   - Same tuning
## 4. Feature Importance Plot (top 15 features)
## 5. Quick Evaluation on Test Set
   - F1-Score, Precision, Recall, ROC-AUC
   - Confusion Matrix visualization
## 6. Save Models & Predictions
## 7. Kết luận
```

### Step 4 — Verify & Quick Test

```python
# Sau khi train, verify:
from sklearn.metrics import f1_score, roc_auc_score

preds = predict(rf_smote, X_test)
f1 = f1_score(y_test, preds["y_pred"])
auc = roc_auc_score(y_test, preds["y_prob"])
print(f"RF (SMOTE) → F1: {f1:.4f}, AUC: {auc:.4f}")
# Expected: F1 > 0.80, AUC > 0.95 (fraud detection baseline)
```

## Checklist

- [x] `src/models/__init__.py` tạo xong
- [x] `src/models/random_forest_model.py` tạo xong với đủ functions
- [x] `models/` directory tạo xong
- [x] RF trained với SMOTE data — F1=0.9973, AUC=0.9994
- [x] RF trained với ADASYN data — F1=0.9966, AUC=0.9992
- [x] `models/rf_smote.pkl` tồn tại và loadable — 9.2 MB
- [x] `models/rf_adasyn.pkl` tồn tại và loadable — 32.3 MB
- [x] `reports/rf_predictions.pkl` lưu `y_pred` và `y_prob` cho cả 2 models
- [x] Feature importance có trong output — errorBalanceOrig #1 (41-47%)
- [x] RF (SMOTE) F1-Score trên test set > 0.75 — **0.9973** ✅
- [x] RF (SMOTE) ROC-AUC trên test set > 0.90 — **0.9994** ✅
- [ ] Notebook `03_model_random_forest.ipynb` chạy clean — ⏳ tạo sau
- [x] Training time được ghi nhận — SMOTE: 1187.7s, ADASYN: 1167.5s

## Success Criteria

| Criterion | Minimum | Evidence |
|-----------|---------|---------|
| RF F1-Score (test, SMOTE) | > 0.75 | **0.9973** ✅ |
| RF ROC-AUC (test, SMOTE) | > 0.90 | **0.9994** ✅ |
| RF F1-Score (test, ADASYN) | > 0.75 | **0.9966** ✅ |
| RF ROC-AUC (test, ADASYN) | > 0.90 | **0.9992** ✅ |
| Model file loadable | ✅ | rf_smote.pkl (9.2 MB), rf_adasyn.pkl (32.3 MB) ✅ |
| Training time recorded | any value | SMOTE: 1187.7s, ADASYN: 1167.5s ✅ |

> Note: Cả 2 models đều vượt xa ngưỡng tối thiểu. RF-SMOTE nhỉnh hơn nhẹ so với RF-ADASYN.

## Evidence Section

```
RF SMOTE  — F1: 0.9973  AUC: 0.9994  Precision: 0.9994  Recall: 0.9951  Training time: 1187.7s
RF ADASYN — F1: 0.9966  AUC: 0.9992  Precision: 0.9982  Recall: 0.9951  Training time: 1167.5s

Best params (SMOTE):  n_estimators=200, max_depth=20, min_samples_split=2, min_samples_leaf=1,
                      max_features=sqrt, class_weight=balanced_subsample
Best params (ADASYN): n_estimators=500, max_depth=20, min_samples_split=2, min_samples_leaf=1,
                      max_features=sqrt, class_weight=balanced_subsample
Best CV F1 (SMOTE):  0.9993
Best CV F1 (ADASYN): 0.9964

Confusion Matrix (RF-SMOTE):   TN=38,356  FP=1   FN=8  TP=1,635
Confusion Matrix (RF-ADASYN):  TN=38,354  FP=3   FN=8  TP=1,635

Feature Importance Top 5 (RF-SMOTE):
  #1 errorBalanceOrig         = 0.4110
  #2 oldbalanceOrg            = 0.1606
  #3 is_drain_account         = 0.1090
  #4 newbalanceDest            = 0.0595
  #5 amount_to_oldbalance_ratio = 0.0519

Model sizes:
  rf_smote.pkl  = 9.2 MB  (< 50MB → có thể commit)
  rf_adasyn.pkl = 32.3 MB (< 50MB → có thể commit)
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation | Kết quả |
|------|-----------|--------|------------|---------|
| RF slow on 230K SMOTE samples | Medium | Low | Use n_jobs=-1, reduce n_iter | ✅ 1187.7s (~20 min) — chấp nhận được |
| F1 < 0.75 | Low | High | Adjust decision threshold | ✅ F1=0.9973 — vượt xa ngưỡng |
| Memory OOM during SearchCV | Low | Medium | Use RandomizedSearchCV with n_iter=50 | ✅ Không gặp |

## Phase Summary

> ✅ **PASSED — Hoàn thành ngày 31/08/2026**

```
Hoàn thành: 31/08/2026
Người thực hiện: Hoàng Cao Sơn
Kết quả thực tế:
- RF SMOTE:  F1=0.9973  AUC=0.9994  Precision=0.9994  Recall=0.9951
- RF ADASYN: F1=0.9966  AUC=0.9992  Precision=0.9982  Recall=0.9951
- Best params: n_estimators=200, max_depth=20, max_features=sqrt, class_weight=balanced_subsample
- Feature #1: errorBalanceOrig (41.1%)  Feature #2: oldbalanceOrg (16.1%)
- Model sizes: rf_smote.pkl=9.2MB, rf_adasyn.pkl=32.3MB (cả 2 < 50MB)
- RandomizedSearchCV: n_iter=50, cv=5, scoring=f1 cho cả 2 datasets
Issues gặp phải:
- Training time dài (~40 min tổng cả 2 models) do n_iter=50, cv=5 trên ~230k mẫu
- Windows console encoding → đã fix bằng sys.stdout.reconfigure(encoding='utf-8')
```

## Commit

```bash
git add src/models/ run_random_forest.py models/ reports/
git commit -m "feat(phase03): Random Forest model trained + tuned, artifacts saved"
```
