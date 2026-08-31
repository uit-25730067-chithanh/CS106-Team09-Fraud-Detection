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
| Status | `passed` ✅ |
| Review | ✅ Evidence-based |
| Estimated effort | 3–4 giờ |
| Sprint | Sprint 3 |

> ⚠️ **Sai khác triển khai (có chủ đích):**
> - **Autoencoder dùng `sklearn.neural_network.MLPRegressor`** thay cho Keras/TensorFlow.
>   Máy phát triển chạy **Python 3.14**, chưa có bản TensorFlow nào (`pip`: *No matching
>   distribution*). Kiến trúc giữ nguyên 16→8→4→8→16 (bottleneck 4), Adam + early stopping.
>   Model lưu `models/autoencoder.pkl` (+ `autoencoder_threshold.txt`, `autoencoder_meta.json`)
>   thay cho `.h5`.
> - **Deliverable chính là `run_xgboost.py` + `run_autoencoder.py`** (theo pattern
>   `run_random_forest.py` của Sơn). Notebook `04_*`/`05_*` là bản wrapper mỏng gọi lại
>   `src/models/` để lên báo cáo.

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
- Train ONLY trên normal transactions (isFraud=0)
- Fraud detection: reconstruction error cao → likely fraud
- Threshold: chọn percentile của reconstruction error trên validation set
- Framework: Keras functional API hoặc Sequential

## 💡 Ý tưởng Đề xuất & Cải tiến Nâng cao (từ MY_IDEAS)

1. **Tối ưu hóa Hyperparameter XGBoost bằng Optuna (Bayesian Optimization):**
   * Thay vì GridSearchCV duyệt lưới thô sơ, sử dụng **Optuna** để tìm kiếm siêu tham số tối ưu thông minh: `learning_rate` ($0.01 \rightarrow 0.2$), `max_depth` ($4 \rightarrow 10$), `subsample` ($0.6 \rightarrow 1.0$), `colsample_bytree` ($0.6 \rightarrow 1.0$) và `scale_pos_weight`.
2. **Autoencoder — Deep Anomaly Detection (Zero-shot Fraud):**
   * Chỉ huấn luyện mạng nơ-ron Autoencoder trên giao dịch **Bình thường (Class 0)**.
   * Khi gặp gian lận, mô hình không tái tạo tốt $\rightarrow$ **Reconstruction Loss (MSE)** tăng vọt.
   * Thử nghiệm các ngưỡng phân định khác nhau: 95th, 99th và 99.5th percentile của tập validation bình thường để tối ưu hóa F1-score.
3. **🌟 Đột phá học thuật — Kiến trúc Lai (Hybrid Stacking Ensemble):**
   * Trích xuất điểm số `reconstruction_error` từ Autoencoder và đưa vào làm **1 feature bổ sung** cho tập dữ liệu huấn luyện của XGBoost.
   * *Ý nghĩa:* Giúp mô hình cây quyết định (XGBoost) kết hợp được cả thông tin quan hệ phi tuyến dạng nơ-ron từ Autoencoder, nâng cao khả năng phân loại vượt bậc.

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
    Train autoencoder on NORMAL (isFraud=0) transactions only.
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
- [x] `src/models/xgboost_model.py` tạo xong
- [x] XGBoost trained với SMOTE data (+ ADASYN để so sánh)
- [x] `models/xgb_smote.pkl` tồn tại và loadable (0.41 MB) + bản `.json` native
- [x] XGBoost F1-Score trên test > 0.75 — **0.9963** ✅
- [x] XGBoost ROC-AUC trên test > 0.93 — **0.9993** ✅
- [x] Feature importance plot (notebook `04_*` §3) + CSV `reports/xgb_smote_feature_importance.csv`
- [x] Notebook `04_model_xgboost.ipynb` chạy clean — đã execute bằng `jupyter nbconvert`,
      output + biểu đồ nhúng sẵn (0 lỗi)

**Autoencoder:**
- [x] `src/models/autoencoder_model.py` tạo xong (MLPRegressor — xem ghi chú sai khác)
- [x] Autoencoder trained CHỈ trên normal transactions (isFraud=0) — 122,744 dòng
- [x] `models/autoencoder.pkl` tồn tại (thay `.h5`) + `autoencoder_meta.json`
- [x] `models/autoencoder_threshold.txt` chứa threshold value — `0.045456`
- [x] Reconstruction error distribution plot (notebook `05_*` §3)
- [x] Autoencoder Recall trên fraud > 0.60 — **0.7523** ✅ (200 epoch)
- [x] Notebook `05_model_autoencoder.ipynb` chạy clean — đã execute bằng `jupyter nbconvert`,
      2 biểu đồ (loss curve + phân bố recon error) nhúng sẵn (0 lỗi)

## Success Criteria

| Model | Criterion | Minimum | Evidence |
|-------|-----------|---------|---------|
| XGBoost | F1-Score | > 0.75 | **0.9963** (SMOTE) / 0.9954 (ADASYN) ✅ |
| XGBoost | ROC-AUC | > 0.93 | **0.9993** (SMOTE) / 0.9994 (ADASYN) ✅ |
| Autoencoder | Recall (fraud) | > 0.60 | **0.7523** ✅ |
| Both | Model artifacts | loadable | `xgb_smote.pkl` 0.41MB, `xgb_adasyn.pkl` 0.50MB, `autoencoder.pkl` 22KB ✅ |

## Evidence Section

```
XGBoost SMOTE  — F1: 0.9963  AUC: 0.9993  Precision: 0.9976  Recall: 0.9951  Training time: 45.9s
XGBoost ADASYN — F1: 0.9954  AUC: 0.9994  Precision: 0.9957  Recall: 0.9951  Training time: 43.5s
Best XGB params (SMOTE):  n_estimators=300, max_depth=8, learning_rate=0.2, subsample=0.85,
                          colsample_bytree=1.0, min_child_weight=3, gamma=0.1
Best CV F1 (SMOTE): 0.9994   |   RandomizedSearchCV: n_iter=20, cv=3, scoring=f1
scale_pos_weight = 1.0 (dữ liệu đã cân bằng bằng SMOTE/ADASYN — không nhân đôi trọng số)

Confusion Matrix (XGB-SMOTE):  TN=38,353  FP=4   FN=8  TP=1,635

XGB Feature Importance Top 3 (SMOTE): errorBalanceOrig=0.499, newbalanceOrig=0.472, errorBalanceDest=0.010

Autoencoder (MLPRegressor 16-8-4-8-16, train trên 122,744 giao dịch normal, 200 epoch)
  threshold (p95 validation, ưu tiên recall≥0.60) = 0.045456
  Test — Recall: 0.7523  Precision: 0.3822  F1: 0.5069  ROC-AUC: 0.9318
  Confusion Matrix:  TN=36,359  FP=1,998  FN=407  TP=1,236
  Threshold sweep (validation): p90 R=0.85/P=0.27 · p95 R=0.74/P=0.39 · p99 R=0.47/P=0.67

Artifacts:
  models/xgb_smote.pkl (0.41MB) + xgb_smote.json      models/xgb_adasyn.pkl (0.50MB) + xgb_adasyn.json
  models/autoencoder.pkl (19KB) + autoencoder_threshold.txt + autoencoder_meta.json
  reports/xgb_{smote,adasyn}_summary.txt, xgb_{smote,adasyn}_feature_importance.csv
  reports/xgb_predictions.pkl, xgb_{smote,adasyn}_predictions.pkl
  reports/autoencoder_summary.txt, autoencoder_predictions.pkl, autoencoder_recon_errors.pkl
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Autoencoder threshold too sensitive | Medium | Medium | Try percentile 90, 95, 99; pick best F1 |
| TF/Keras version conflict | Medium | Medium | Use tf-keras package or pin tensorflow version |
| autoencoder.h5 too large to commit | Low | Low | Ensure < 50MB; use .gitignore if needed |
| XGBoost underperforms RF | Low | Low | This is expected comparison data, not failure |

## Phase Summary

> ✅ **PASSED — Hoàn thành ngày 31/08/2026**

```
Hoàn thành: 31/08/2026
Người thực hiện: Mỷ Cẩm
Kết quả thực tế:
- XGBoost SMOTE:  F1=0.9963  AUC=0.9993  Precision=0.9976  Recall=0.9951  (45.9s)
- XGBoost ADASYN: F1=0.9954  AUC=0.9994  Precision=0.9957  Recall=0.9951  (43.5s)
  → ngang Random Forest (RF-SMOTE F1=0.9973), nhưng train nhanh hơn ~25x (46s vs ~1188s)
- Autoencoder: Recall(fraud)=0.7523  Precision=0.3822  F1=0.5069  AUC=0.9318
  Threshold=0.045456 (p95 validation), train 200 epoch trên 122,744 giao dịch normal
- Feature quan trọng nhất (XGB & RF đồng thuận): errorBalanceOrig
Issues gặp phải:
- TensorFlow/Keras KHÔNG có bản cho Python 3.14 → Autoencoder chuyển sang sklearn
  MLPRegressor (cùng kiến trúc), lưu .pkl thay .h5. API giữ nguyên cho Phase 05.
- Ban đầu máy chưa có jupyter → đã `pip install jupyter nbconvert ipykernel` (OK trên
  Python 3.14) và execute cả 2 notebook bằng `jupyter nbconvert --execute` (0 lỗi).
- Windows console cp1252 + emoji trong log → `run_*.py` gọi `sys.stdout.reconfigure`,
  notebook guard bằng `hasattr`, và `src/models/{xgboost,autoencoder}_model.py` có helper
  `_log()` tự fallback sang ASCII khi UnicodeEncodeError.
- Autoencoder precision thấp (~0.38) — đúng bản chất anomaly detection thuần; đây là
  phần bonus (P1), không phải model chính.
```

## Bàn giao cho Phase 05 (Khang)

- `reports/xgb_predictions.pkl` — dict `{"xgb_smote": {y_pred, y_prob}, "xgb_adasyn": {...}}`
  (cùng format `rf_predictions.pkl`).
- `reports/autoencoder_predictions.pkl` — `{y_pred, y_prob}` với `y_prob` = reconstruction error.
- `reports/autoencoder_recon_errors.pkl` — `{reconstruction_errors, y_test}` để vẽ phân bố.
- Import chung: `from src.models import train_xgboost, load_xgb_model, load_autoencoder, ...`

## Commit

`models/*.pkl` bị `.gitignore` (dễ vỡ cross-version, trùng với `.json`). Model chia sẻ
qua git bằng **bản `.json` native của XGBoost** + threshold/meta — Trung load thẳng cho
Streamlit, Khang dùng cho Phase 05. Chi tiết quyết định: xem comment trong `.gitignore`.

```bash
cd <repo-root>
git add draft/fraud-detection/src/models/ \
        draft/fraud-detection/run_xgboost.py draft/fraud-detection/run_autoencoder.py \
        draft/fraud-detection/notebooks/04_model_xgboost.ipynb \
        draft/fraud-detection/notebooks/05_model_autoencoder.ipynb \
        draft/fraud-detection/reports/xgb_*.txt draft/fraud-detection/reports/xgb_*.csv \
        draft/fraud-detection/reports/xgb_predictions.pkl \
        draft/fraud-detection/reports/autoencoder_predictions.pkl \
        draft/fraud-detection/reports/autoencoder_recon_errors.pkl \
        draft/fraud-detection/reports/autoencoder_summary.txt \
        draft/fraud-detection/models/xgb_smote.json draft/fraud-detection/models/xgb_adasyn.json \
        draft/fraud-detection/models/autoencoder_threshold.txt draft/fraud-detection/models/autoencoder_meta.json \
        draft/fraud-detection/.gitignore draft/fraud-detection/requirements.txt \
        draft/fraud-detection/docs/project-roadmap.md \
        plans/fraud-detection-full-submit/
git commit -m "feat(phase04): XGBoost + Autoencoder models trained and saved"
```

> `models/xgb_smote.pkl` / `autoencoder.pkl` cố tình KHÔNG add (đã .gitignore). Ai cần
> object Python nguyên bản thì chạy lại `python run_xgboost.py` / `run_autoencoder.py`.
