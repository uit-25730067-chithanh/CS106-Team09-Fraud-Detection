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
| Status | `pending` |
| Review | ⬜ Not reviewed |
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
- Feature importance từ RF có thể reveal top fraud indicators
- Evaluation PHẢI dùng F1-Score và ROC-AUC, không phải Accuracy

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

- [ ] `src/models/__init__.py` tạo xong
- [ ] `src/models/random_forest_model.py` tạo xong với đủ functions
- [ ] `models/` directory tạo xong
- [ ] RF trained với SMOTE data
- [ ] RF trained với ADASYN data
- [ ] `models/rf_smote.pkl` tồn tại và loadable
- [ ] `models/rf_adasyn.pkl` tồn tại và loadable
- [ ] `reports/rf_predictions.pkl` lưu `y_pred` và `y_prob`
- [ ] Feature importance plot có trong notebook
- [ ] RF (SMOTE) F1-Score trên test set > 0.75
- [ ] RF (SMOTE) ROC-AUC trên test set > 0.90
- [ ] Notebook chạy Restart & Run All không lỗi
- [ ] Training time được ghi nhận (evidence)

## Success Criteria

| Criterion | Minimum | Evidence |
|-----------|---------|---------|
| RF F1-Score (test, SMOTE) | > 0.75 | ___________ |
| RF ROC-AUC (test, SMOTE) | > 0.90 | ___________ |
| Model file loadable | ✅ | ___________ |
| Training time recorded | any value | ___________ |

> Note: Threshold 0.75 F1 là minimum acceptable. Nếu < 0.75, cần điều chỉnh threshold hoặc re-tune.

## Evidence Section *(điền sau khi làm)*

```
RF SMOTE  — F1: ____  AUC: ____  Training time: ____s
RF ADASYN — F1: ____  AUC: ____  Training time: ____s
Best params (SMOTE): ____________________
Feature #1: ____________________
Feature #2: ____________________
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| RF slow on 300K SMOTE samples | Medium | Low | Use n_jobs=-1, reduce n_iter in search |
| F1 < 0.75 | Low | High | Adjust decision threshold (0.3–0.4 instead of 0.5) |
| Memory OOM during GridSearch | Low | Medium | Use RandomizedSearchCV with n_iter=10 |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa hoàn thành

```
Hoàn thành: __/__/2026
Người thực hiện: Sơn
Kết quả thực tế:
- RF SMOTE: F1=... AUC=...
- RF ADASYN: F1=... AUC=...
- Best params: ...
Issues gặp phải:
- ...
```

## Commit

```bash
git add src/models/ notebooks/03_model_random_forest.ipynb models/ reports/
git commit -m "feat(phase03): Random Forest model trained + tuned, artifacts saved"
```
