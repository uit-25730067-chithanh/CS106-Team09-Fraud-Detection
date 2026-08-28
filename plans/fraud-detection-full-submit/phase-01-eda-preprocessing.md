# Phase 01 — EDA & Preprocessing

**Parent plan:** [plan.md](./plan.md)  
**Depends on:** [Phase 00](./phase-00-env-data-setup.md) — PASSED  
**Next phase:** [Phase 02 — Imbalance Handling](./phase-02-imbalance-handling.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Thanh** |
| Priority | P0 — Dependency của tất cả các mô hình |
| Status | `pending` |
| Review | ⬜ Not reviewed |
| Estimated effort | 3–4 giờ |
| Sprint | Sprint 2 |

## Context

Đây là phần quan trọng nhất của Thanh — output của phase này là:
1. Notebook EDA hoàn chỉnh (visualization, insights)
2. Script preprocessing pipeline có thể tái sử dụng
3. Dữ liệu đã split + scale được lưu vào `data/processed/`

## Requirements

- Input: `data/raw/paysim.csv`
- Output: `data/processed/X_train.pkl`, `X_test.pkl`, `y_train.pkl`, `y_test.pkl`
- Scaling chỉ fit trên train set, transform cả train và test
- Split: stratified 80/20, `random_state=42`
- Không apply SMOTE ở phase này (Phase 02 làm)

## Key Insights

- Features có ý nghĩa vật lý rõ ràng → Cần làm Feature Engineering để mô hình học tốt hơn.
- `type` là biến categorical → Cần One-Hot Encoding (OHE).
- `amount` và các biến số dư (`oldbalanceOrg`, `newbalanceOrig`, `oldbalanceDest`, `newbalanceDest`) cần StandardScaler.
- Class imbalance cực kỳ lớn: 6.36 triệu dòng, trong đó chỉ có 8,213 mẫu fraud (~0.13%). Để tránh OOM trên máy tính cá nhân, Thanh sẽ thực hiện **Stratified Downsampling**:
  1. Lọc giao dịch chỉ giữ lại `TRANSFER` và `CASH_OUT` (các loại giao dịch thực tế có xảy ra fraud).
  2. Lấy mẫu ngẫu nhiên (sampling) để rút gọn tập dữ liệu xuống khoảng **200,000 dòng**, giữ lại toàn bộ 8,213 mẫu fraud.
- `nameOrig` và `nameDest` (ID tài khoản) nên được drop trước khi đưa vào huấn luyện mô hình.

## Related Files

```
draft/fraud-detection/
├── notebooks/
│   └── 01_eda.ipynb              ← [TẠO MỚI] EDA + phân tích
├── src/preprocessing/
│   ├── __init__.py               ← [TẠO MỚI]
│   ├── data_loader.py            ← [TẠO MỚI] Load + validate
│   ├── feature_scaler.py         ← [TẠO MỚI] StandardScaler
│   └── data_splitter.py          ← [TẠO MỚI] Stratified split
└── data/processed/               ← Output directory
```

## Implementation Steps

### Step 1 — `src/preprocessing/__init__.py`

```python
from .data_loader import load_data, validate_data
from .feature_scaler import scale_features
from .data_splitter import split_data

__all__ = ["load_data", "validate_data", "scale_features", "split_data"]
```

> 💡 Note: Các file module của Python trong `src/` sử dụng `snake_case` (gạch dưới) để có thể import bình thường theo cú pháp chuẩn của Python.

### Step 2 — `src/preprocessing/data_loader.py`

```python
"""Load, filter and validate the PaySim dataset."""
import pandas as pd
from pathlib import Path

def load_data(path: str = "data/raw/paysim.csv") -> pd.DataFrame:
    """
    Load CSV, filter for TRANSFER/CASH_OUT, and downsample to ~200k rows
    while preserving all fraud cases.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. "
            "Download from: https://www.kaggle.com/datasets/ealaxi/paysim1"
        )
    
    # Load và lọc loại giao dịch
    df = pd.read_csv(p)
    df = df[df["type"].isin(["TRANSFER", "CASH_OUT"])].reset_index(drop=True)
    
    # Stratified downsampling
    fraud_df = df[df["isFraud"] == 1]
    normal_df = df[df["isFraud"] == 0]
    
    # Downsample normal_df để đạt tổng kích thước ~200,000 dòng
    # Clamp để tránh n_normal_samples âm hoặc vượt số mẫu normal có sẵn
    n_fraud = len(fraud_df)
    if n_fraud >= 200000:
        raise ValueError(
            f"Số fraud ({n_fraud}) vượt mục tiêu downsample 200,000. "
            "Kiểm tra lại bộ lọc hoặc tăng ngưỡng mục tiêu."
        )
    n_normal_samples = min(200000 - n_fraud, len(normal_df))
    normal_sampled = normal_df.sample(n=n_normal_samples, random_state=42)
    
    # Gộp lại và shuffle
    df_downsampled = pd.concat([fraud_df, normal_sampled])
    df_downsampled = df_downsampled.sample(frac=1.0, random_state=42).reset_index(drop=True)
    
    return df_downsampled

def validate_data(df: pd.DataFrame) -> dict:
    """Validate dataset integrity. Returns summary dict."""
    assert df["isFraud"].nunique() == 2, "isFraud column must have 2 unique values"
    assert df.isnull().sum().sum() == 0, "Dataset has missing values"
    
    n_fraud = df["isFraud"].sum()
    fraud_ratio = df["isFraud"].mean()
    
    return {
        "shape": df.shape,
        "n_fraud": int(n_fraud),
        "n_normal": int(len(df) - n_fraud),
        "fraud_ratio": round(fraud_ratio, 6),
        "missing_values": int(df.isnull().sum().sum()),
    }
```

### Step 3 — `src/preprocessing/feature_scaler.py`

```python
"""Feature engineering, encoding and scaling for PaySim dataset."""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

SCALE_COLS = ["amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest", "step"]

def scale_features(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, StandardScaler]:
    """
    1. Thực hiện Feature Engineering (errorBalanceOrig, errorBalanceDest).
    2. One-Hot Encoding cho cột type.
    3. Fit StandardScaler trên train set, transform cả train và test.
    4. Drop các cột ID không sử dụng (nameOrig, nameDest).
    
    Returns: (X_train_processed, X_test_processed, fitted_scaler)
    """
    X_train = X_train.copy()
    X_test = X_test.copy()
    
    # ─── 1. Feature Engineering ──────────────────────────────────────────────
    for df in [X_train, X_test]:
        df["errorBalanceOrig"] = df["oldbalanceOrg"] - df["amount"] - df["newbalanceOrig"]
        df["errorBalanceDest"] = df["oldbalanceDest"] + df["amount"] - df["newbalanceDest"]
    
    # ─── 2. Encoding ──────────────────────────────────────────────────────────
    X_train = pd.get_dummies(X_train, columns=["type"], drop_first=True)
    X_test = pd.get_dummies(X_test, columns=["type"], drop_first=True)
    
    # Align columns in case some categories are missing in test set
    X_train, X_test = X_train.align(X_test, join="left", axis=1, fill_value=0)
    
    # ─── 3. Scaling ───────────────────────────────────────────────────────────
    cols_to_scale = SCALE_COLS + ["errorBalanceOrig", "errorBalanceDest"]
    scaler = StandardScaler()
    X_train[cols_to_scale] = scaler.fit_transform(X_train[cols_to_scale])
    X_test[cols_to_scale] = scaler.transform(X_test[cols_to_scale])
    
    # ─── 4. Drop IDs ──────────────────────────────────────────────────────────
    drop_cols = ["nameOrig", "nameDest"]
    X_train = X_train.drop(columns=[c for c in drop_cols if c in X_train.columns], errors="ignore")
    X_test = X_test.drop(columns=[c for c in drop_cols if c in X_test.columns], errors="ignore")
    
    return X_train, X_test, scaler
```

### Step 4 — `src/preprocessing/data_splitter.py`

```python
"""Stratified train/test split for imbalanced PaySim data."""
import pandas as pd
import pickle
from pathlib import Path
from sklearn.model_selection import train_test_split
from src.utils import RANDOM_STATE, TEST_SIZE, DATA_PROCESSED_DIR

def split_data(
    df: pd.DataFrame,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
    save: bool = True,
) -> tuple:
    """
    Stratified split on isFraud column.
    Saves processed splits to data/processed/ if save=True.
    
    Returns: (X_train, X_test, y_train, y_test)
    """
    X = df.drop("isFraud", axis=1)
    y = df["isFraud"]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,  # CRITICAL for imbalanced data
    )
    
    if save:
        Path(DATA_PROCESSED_DIR).mkdir(parents=True, exist_ok=True)
        for name, obj in [
            ("X_train", X_train), ("X_test", X_test),
            ("y_train", y_train), ("y_test", y_test),
        ]:
            with open(f"{DATA_PROCESSED_DIR}/{name}.pkl", "wb") as f:
                pickle.dump(obj, f)
        print(f"Saved splits to {DATA_PROCESSED_DIR}/")
    
    return X_train, X_test, y_train, y_test
```

### Step 5 — `notebooks/01_eda.ipynb` Structure

Notebook phải có đủ các sections (theo code-standards.md):

```
## 0. Imports & Setup (Cần cấu hình path để import được `src`)
```python
import sys
import os
sys.path.insert(0, os.path.abspath(".."))
```
## 1. Load Data (Phải tải paysim.csv)
## 2. Basic Info (shape, dtypes, describe)
## 3. Missing Values Analysis
## 4. Target Distribution (isFraud distribution chart)
## 5. Feature Distributions (amount, step histograms, type bar chart)
## 6. Balance Analysis (so sánh oldbalance vs newbalance)
## 7. Preprocessing & Feature Engineering (tạo errorBalance, OHE type, downsampling)
## 8. Correlation Matrix (heatmap các thuộc tính đã mã hóa và tạo mới)
## 9. Preprocessing Pipeline (gọi scripts từ src/)
## 10. Verify Split (check isFraud ratio maintained)
## 11. Kết luận / Observations

**Key visualizations cần có:**
- Pie chart / bar chart: isFraud distribution (0 vs 1)
- Histogram: `amount` distribution (fraud vs normal)
- Bar chart: Tần suất giao dịch theo `type`
- Scatter/Line chart: Phân bố giao dịch gian lận theo `step` (thời gian)
- Heatmap: Correlation matrix của các numeric features + engineered features

### Step 6 — Run & Save Processed Data

```python
# Chạy ở cuối notebook
import os
import pickle
from src.preprocessing.data_loader import load_data, validate_data
from src.preprocessing.feature_scaler import scale_features
from src.preprocessing.data_splitter import split_data
from src.utils import DATA_PROCESSED_DIR

# 1. Load và validate (gồm downsampling bên trong load_data)
df = load_data()
stats = validate_data(df)
print("Dataset Stats:", stats)

# 2. Split (không tự động save vì chưa scale & encode)
X_train, X_test, y_train, y_test = split_data(df, save=False)

# 3. Scale các cột numerical và One-Hot Encode type, thêm feature mới
X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

# 4. Lưu processed data
os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
for name, obj in [
    ("X_train", X_train_scaled),
    ("X_test", X_test_scaled),
    ("y_train", y_train),
    ("y_test", y_test),
]:
    path = os.path.join(DATA_PROCESSED_DIR, f"{name}.pkl")
    with open(path, "wb") as f:
        pickle.dump(obj, f)
    print(f"Saved processed file: {path}")

# 5. Lưu fitted scaler vào models/ để Demo UI load và scale dữ liệu giao dịch mới
os.makedirs("models", exist_ok=True)
with open("models/scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)
print("Saved fitted scaler -> models/scaler.pkl")
```

> Hoặc tạo script runner riêng `run_preprocessing.py`

## Checklist

- [ ] `src/preprocessing/__init__.py` tạo xong
- [ ] `src/preprocessing/data_loader.py` — `load_data()` và `validate_data()` hoạt động
- [ ] `src/preprocessing/feature_scaler.py` — `scale_features()` fit chỉ trên train
- [ ] `src/preprocessing/data_splitter.py` — stratified split, save `.pkl`
- [ ] `data/processed/X_train.pkl` tồn tại
- [ ] `data/processed/X_test.pkl` tồn tại
- [ ] `data/processed/y_train.pkl` tồn tại
- [ ] `data/processed/y_test.pkl` tồn tại
- [ ] `models/scaler.pkl` tồn tại và loadable
- [ ] Verify split ratio: `y_train.mean() ≈ y_test.mean() ≈ 0.041` (nếu tổng downsample là 200k và có 8,213 fraud)
- [ ] `notebooks/01_eda.ipynb` chạy được Restart & Run All không lỗi
- [ ] EDA notebook có ít nhất 5 visualizations
- [ ] Heatmap correlation matrix các feature mới có mặt
- [ ] isFraud distribution chart có mặt
- [ ] Phân phối giao dịch theo type có mặt

## Success Criteria

| Criterion | Expected | Evidence |
|-----------|---------|---------|
| X_train shape | (160000, 9) | ___________ |
| X_test shape | (40000, 9) | ___________ |
| y_train fraud ratio | ≈ 0.041 | ___________ |
| y_test fraud ratio | ≈ 0.041 | ___________ |
| Notebook runs clean | 0 errors | ___________ |
| Processed files saved | 4 .pkl files | ___________ |

## Evidence Section *(điền sau khi làm)*

```
X_train.shape   = ________________
X_test.shape    = ________________
y_train mean    = ________________  (fraud ratio in train)
y_test mean     = ________________  (fraud ratio in test)
pkl files saved = X_train / X_test / y_train / y_test ✅/❌
notebook errors = ________________
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Import error (kebab filename) | Low | High | Sử dụng snake_case cho các module Python trong `src/` (đã được sửa đổi) |
| Scaler leakage (fit on all data) | Low | High | Explicitly split before scaling, then fit_transform train only |
| Memory error with 6M rows | High | High | Lọc ngay TRANSFER/CASH_OUT và downsample stratified trong load_data trước khi phân tích |

## Notes for Sơn (Phase 02)

- `data/processed/X_train.pkl` = features, đã scaled, chưa SMOTE
- `data/processed/y_train.pkl` = labels gốc (imbalanced)
- **Không** modify test set — giữ nguyên tỷ lệ thực tế

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa hoàn thành — điền vào sau khi tất cả checklist PASSED

```
Hoàn thành: __/__/2026
Người thực hiện: Thanh
Kết quả thực tế:
- X_train.shape = ...
- y_train fraud ratio = ...
- EDA insights quan trọng nhất: ...
Issues gặp phải:
- ...
```

## Commit

```bash
git add src/preprocessing/ notebooks/01_eda.ipynb data/processed/
git commit -m "feat(phase01): EDA notebook + preprocessing pipeline, processed data saved"
```
