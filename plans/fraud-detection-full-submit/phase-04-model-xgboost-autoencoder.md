# Phase 04 — Modeling: XGBoost + Autoencoder

**Parent plan:** [plan.md](./plan.md)  
**Depends on:** [Phase 02](./phase-02-imbalance-handling.md) — PASSED  
**Parallel with:** [Phase 03](./phase-03-model-random-forest.md) (Sơn làm RF song song)  
**Next phase:** [Phase 05 — Evaluation](./phase-05-evaluation-comparison.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Cẩm** |
| Priority | P0 (XGBoost required) + P1 (Autoencoder bonus) |
| Status | `pending` |
| Review | ⬜ Not reviewed |
| Estimated effort | 3–4 giờ |
| Sprint | Sprint 3 |

## Context

Cẩm implement 2 models song song với Sơn (Phase 03):
- **XGBoost**: supervised classifier, required, compare vs RF
- **Autoencoder**: anomaly detection via reconstruction error, bonus points

Cẩm cũng save tất cả processed data artifacts chuẩn.

## Requirements

- XGBoost: train với SMOTE data, hyperparameter tuning, save model
- Autoencoder: train trên NORMAL transactions only (anomaly detection paradigm)
- Lưu đầy đủ: model artifacts, predictions, reconstruction errors
- Không commit `*.h5` > 50MB

## Key Insights

**XGBoost:**
- `scale_pos_weight = n_negative/n_positive` để handle imbalance thêm
- `eval_metric="aucpr"` thay vì "auc" — tốt hơn cho imbalanced
- `early_stopping_rounds=10` để tránh overfit

**Autoencoder:**
- Train ONLY trên normal transactions (Class=0)
- Fraud detection: reconstruction error cao → likely fraud
- Threshold: chọn percentile của reconstruction error trên validation set
- Framework: Keras functional API hoặc Sequential

## Related Files

```
draft/fraud-detection/
├── notebooks/
│   ├── 04_model_xgboost.ipynb          ← [TẠO MỚI]
│   └── 05_model_autoencoder.ipynb      ← [TẠO MỚI]
├── src/models/
│   ├── xgboost_model.py                ← [TẠO MỚI]
│   └── autoencoder_model.py            ← [TẠO MỚI]
└── models/
    ├── xgb_smote.pkl                   ← OUTPUT (XGBoost)
    ├── autoencoder.h5                  ← OUTPUT (Keras model)
    └── autoencoder_threshold.txt       ← OUTPUT (threshold value)
```

## Implementation Steps

### Step 1 — `src/models/xgboost_model.py`

```python
"""XGBoost Classifier for fraud detection."""
import pickle
import time
import numpy as np
import pandas as pd
from pathlib import Path
import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV
from src.utils import RANDOM_STATE

MODEL_DIR = "models"


def train_xgboost(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_val: pd.DataFrame = None,
    y_val: pd.Series = None,
    tune: bool = True,
    use_scale_pos_weight: bool = False,  # Mặc định False nếu đã dùng SMOTE/ADASYN để tránh trùng lặp trọng số
    random_state: int = RANDOM_STATE,
) -> tuple[xgb.XGBClassifier, dict]:
    """
    Train XGBoost with optional hyperparameter tuning.
    scale_pos_weight handles remaining class imbalance.
    """
    Path(MODEL_DIR).mkdir(exist_ok=True)
    start = time.time()
    
    # Compute class weight ratio if needed
    if use_scale_pos_weight:
        n_neg = (y_train == 0).sum()
        n_pos = (y_train == 1).sum()
        scale_pos_weight = n_neg / n_pos
    else:
        scale_pos_weight = 1.0
    
    if tune:
        # Tuning grid nhẹ hơn để tránh tốn thời gian chạy
        param_grid = {
            "n_estimators": [50, 100, 150],
            "max_depth": [4, 6],
            "learning_rate": [0.05, 0.1],
            "subsample": [0.8, 1.0],
            "colsample_bytree": [0.8, 1.0],
        }
        base_xgb = xgb.XGBClassifier(
            scale_pos_weight=scale_pos_weight,
            eval_metric="aucpr",
            random_state=random_state,
            n_jobs=-1,
            verbosity=0,
        )
        search = RandomizedSearchCV(
            base_xgb, param_grid,
            n_iter=6,  # Giảm bớt số iteration
            cv=3,
            scoring="f1",
            random_state=random_state,
            n_jobs=-1,
            verbose=1,
        )
        search.fit(X_train, y_train)
        model = search.best_estimator_
        best_params = search.best_params_
    else:
        model = xgb.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.05,
            scale_pos_weight=scale_pos_weight,
            eval_metric="aucpr",
            random_state=random_state,
            n_jobs=-1,
        )
        model.fit(X_train, y_train)
        best_params = model.get_params()
    
    elapsed = time.time() - start
    info = {"best_params": best_params, "training_time_sec": round(elapsed, 2)}
    return model, info


def save_xgb_model(model: xgb.XGBClassifier, name: str = "xgb_smote") -> str:
    """Save XGBoost model as pickle."""
    path = f"{MODEL_DIR}/{name}.pkl"
    with open(path, "wb") as f:
        pickle.dump(model, f)
    print(f"XGBoost saved → {path}")
    return path


def predict_xgb(model: xgb.XGBClassifier, X_test: pd.DataFrame) -> dict:
    return {
        "y_pred": model.predict(X_test),
        "y_prob": model.predict_proba(X_test)[:, 1],
    }
```

### Step 2 — `src/models/autoencoder_model.py`

```python
"""Autoencoder for anomaly-based fraud detection using Keras."""
import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from tensorflow import keras
from tensorflow.keras import layers
from src.utils import RANDOM_STATE

MODEL_DIR = "models"


def build_autoencoder(input_dim: int) -> keras.Model:
    """Build symmetric autoencoder. Input → compress → reconstruct."""
    keras.utils.set_random_seed(RANDOM_STATE)
    
    # Encoder
    inputs = keras.Input(shape=(input_dim,))
    encoded = layers.Dense(16, activation="relu")(inputs)
    encoded = layers.Dense(8, activation="relu")(encoded)
    bottleneck = layers.Dense(4, activation="relu")(encoded)
    
    # Decoder
    decoded = layers.Dense(8, activation="relu")(bottleneck)
    decoded = layers.Dense(16, activation="relu")(decoded)
    outputs = layers.Dense(input_dim, activation="linear")(decoded)
    
    model = keras.Model(inputs, outputs, name="fraud_autoencoder")
    model.compile(optimizer="adam", loss="mse")
    return model


def train_autoencoder(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    epochs: int = 30,
    batch_size: int = 256,
    validation_split: float = 0.1,
) -> tuple[keras.Model, keras.callbacks.History]:
    """
    Train autoencoder on NORMAL (Class=0) transactions only.
    Fraud detection: high reconstruction error = anomaly.
    """
    # Train ONLY on normal transactions
    X_normal = X_train[y_train == 0].values
    
    model = build_autoencoder(input_dim=X_normal.shape[1])
    
    callbacks = [
        keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=5, restore_best_weights=True
        )
    ]
    
    history = model.fit(
        X_normal, X_normal,  # reconstruction task: input = output
        epochs=epochs,
        batch_size=batch_size,
        validation_split=validation_split,
        callbacks=callbacks,
        verbose=1,
    )
    return model, history


def compute_reconstruction_error(
    model: keras.Model,
    X: np.ndarray | pd.DataFrame,
) -> np.ndarray:
    """Compute MSE reconstruction error per sample."""
    if isinstance(X, pd.DataFrame):
        X = X.values
    reconstructed = model.predict(X, verbose=0)
    mse = np.mean(np.power(X - reconstructed, 2), axis=1)
    return mse


def find_threshold(
    recon_errors_normal: np.ndarray,
    percentile: float = 99.9,  # Nâng từ 95 lên 99.9 để giảm thiểu tỉ lệ báo động giả (FPR)
) -> float:
    """
    Threshold at percentile of normal reconstruction errors.
    Samples with error > threshold are classified as fraud.
    """
    threshold = np.percentile(recon_errors_normal, percentile)
    print(f"Threshold (p{percentile:.2f}%): {threshold:.6f}")
    return threshold


def predict_autoencoder(
    model: keras.Model,
    X_test: pd.DataFrame,
    threshold: float,
) -> dict:
    """Classify as fraud (1) if reconstruction error > threshold."""
    errors = compute_reconstruction_error(model, X_test)
    y_pred = (errors > threshold).astype(int)
    return {
        "y_pred": y_pred,
        "y_prob": errors,  # error score as "fraud probability"
        "reconstruction_errors": errors,
    }


def save_autoencoder(model: keras.Model, threshold: float) -> None:
    """Save model (.h5) and threshold (.txt)."""
    Path(MODEL_DIR).mkdir(exist_ok=True)
    model.save(f"{MODEL_DIR}/autoencoder.h5")
    with open(f"{MODEL_DIR}/autoencoder_threshold.txt", "w") as f:
        f.write(str(threshold))
    print(f"Autoencoder saved → {MODEL_DIR}/autoencoder.h5")
```

### Step 3 — `notebooks/04_model_xgboost.ipynb`

```
## 0. Imports & Setup
## 1. Load SMOTE Data
## 2. Train XGBoost (with RandomizedSearchCV)
## 3. Feature Importance Plot (XGBoost built-in)
## 4. Quick Evaluation (F1, AUC on test set)
## 5. Compare with RF (summary table — will expand in Phase 05)
## 6. Save XGBoost Model
## 7. Kết luận
```

### Step 4 — `notebooks/05_model_autoencoder.ipynb`

```
## 0. Imports & Setup
## 1. Load Data (normal transactions for training)
## 2. Build & Train Autoencoder
   - Architecture summary (model.summary())
   - Loss curve (train vs val)
## 3. Compute Reconstruction Errors
   - Normal vs Fraud distribution of errors (histogram)
## 4. Find Threshold (99.9th percentile)
## 5. Predict & Evaluate
   - Confusion Matrix
   - F1, Precision, Recall, AUC
## 6. Save Model & Threshold
## 7. Kết luận
   - Nhận xét về anomaly detection approach
```

## Checklist

**XGBoost:**
- [ ] `src/models/xgboost_model.py` tạo xong
- [ ] XGBoost trained với SMOTE data
- [ ] `models/xgb_smote.pkl` tồn tại và loadable
- [ ] XGBoost F1-Score trên test > 0.75
- [ ] XGBoost ROC-AUC trên test > 0.93
- [ ] Feature importance plot trong notebook
- [ ] Notebook `04_model_xgboost.ipynb` chạy clean

**Autoencoder:**
- [ ] `src/models/autoencoder_model.py` tạo xong
- [ ] Autoencoder trained CHỈ trên normal transactions (Class=0)
- [ ] `models/autoencoder.h5` tồn tại
- [ ] `models/autoencoder_threshold.txt` chứa threshold value
- [ ] Reconstruction error distribution plot có trong notebook
- [ ] Autoencoder Recall trên fraud > 0.60 (acceptable for bonus)
- [ ] Notebook `05_model_autoencoder.ipynb` chạy clean

## Success Criteria

| Model | Criterion | Minimum | Evidence |
|-------|-----------|---------|---------|
| XGBoost | F1-Score | > 0.75 | ___________ |
| XGBoost | ROC-AUC | > 0.93 | ___________ |
| Autoencoder | Recall (fraud) | > 0.60 | ___________ |
| Both | Model artifacts | loadable | ___________ |

## Evidence Section *(điền sau khi làm)*

```
XGBoost SMOTE — F1: ____  AUC: ____  Training time: ____s
Best XGB params: ____________________
Autoencoder threshold: ____________________
Autoencoder Recall: ____  Precision: ____
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Autoencoder threshold too sensitive | Medium | Medium | Try percentile 90, 95, 99; pick best F1 |
| TF/Keras version conflict | Medium | Medium | Use tf-keras package or pin tensorflow version |
| autoencoder.h5 too large to commit | Low | Low | Ensure < 50MB; use .gitignore if needed |
| XGBoost underperforms RF | Low | Low | This is expected comparison data, not failure |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa hoàn thành

```
Hoàn thành: __/__/2026
Người thực hiện: Cẩm
Kết quả thực tế:
- XGBoost: F1=... AUC=...
- Autoencoder: Recall=... Threshold=...
Issues gặp phải:
- ...
```

## Commit

```bash
git add src/models/xgboost-model.py src/models/autoencoder-model.py \
        notebooks/04_model_xgboost.ipynb notebooks/05_model_autoencoder.ipynb \
        models/
git commit -m "feat(phase04): XGBoost + Autoencoder models trained and saved"
```
