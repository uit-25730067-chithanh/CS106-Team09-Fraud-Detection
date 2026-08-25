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

- Input: `data/raw/creditcard.csv`
- Output: `data/processed/X_train.pkl`, `X_test.pkl`, `y_train.pkl`, `y_test.pkl`
- Scaling chỉ fit trên train set, transform cả train và test
- Split: stratified 80/20, `random_state=42`
- Không apply SMOTE ở phase này (Phase 02 làm)

## Key Insights

- Features V1–V28 đã PCA-transformed → không cần thêm feature engineering
- `Amount` và `Time` chưa scale → cần StandardScaler
- Class imbalance: 284,315 normal vs 492 fraud (~0.17%) → stratified split bắt buộc
- `Time` ít meaningful → có thể drop hoặc giữ (ghi chú trong notebook)

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
"""Load and validate the credit card fraud dataset."""
import pandas as pd
from pathlib import Path

def load_data(path: str = "data/raw/creditcard.csv") -> pd.DataFrame:
    """Load CSV and return DataFrame. Raises FileNotFoundError if missing."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(
            f"Dataset not found at {path}. "
            "Download from: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud"
        )
    df = pd.read_csv(p)
    return df

def validate_data(df: pd.DataFrame) -> dict:
    """Validate dataset integrity. Returns summary dict."""
    assert df.shape == (284807, 31), f"Unexpected shape: {df.shape}"
    assert df["Class"].nunique() == 2, "Class column must have 2 unique values"
    assert df.isnull().sum().sum() == 0, "Dataset has missing values"
    
    n_fraud = df["Class"].sum()
    fraud_ratio = df["Class"].mean()
    
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
"""Feature scaling — StandardScaler on Amount and Time columns."""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

SCALE_COLS = ["Amount", "Time"]

def scale_features(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, StandardScaler]:
    """
    Fit StandardScaler on train, transform both train and test.
    Prevents data leakage — scaler never sees test distribution.
    
    Returns: (X_train_scaled, X_test_scaled, fitted_scaler)
    """
    scaler = StandardScaler()
    
    X_train = X_train.copy()
    X_test = X_test.copy()
    
    X_train[SCALE_COLS] = scaler.fit_transform(X_train[SCALE_COLS])
    X_test[SCALE_COLS] = scaler.transform(X_test[SCALE_COLS])
    
    return X_train, X_test, scaler
```

### Step 4 — `src/preprocessing/data_splitter.py`

```python
"""Stratified train/test split for imbalanced fraud data."""
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
    Stratified split on Class column.
    Saves processed splits to data/processed/ if save=True.
    
    Returns: (X_train, X_test, y_train, y_test)
    """
    X = df.drop("Class", axis=1)
    y = df["Class"]
    
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
## 1. Load Data
## 2. Basic Info (shape, dtypes, describe)
## 3. Missing Values Analysis
## 4. Target Distribution (Class imbalance visualization)
## 5. Feature Distributions (Amount, Time histograms)
## 6. Correlation Matrix (heatmap)
## 7. Fraud vs Normal comparison (boxplots V1-V28 top features)
## 8. Preprocessing Pipeline (gọi scripts từ src/)
## 9. Verify Split (check class ratio maintained)
## 10. Kết luận / Observations
```

**Key visualizations cần có:**
- Pie chart / bar chart: Class distribution (0 vs 1)
- Histogram: `Amount` distribution (fraud vs normal)
- Histogram: `Time` distribution
- Heatmap: Correlation matrix top features
- Boxplots: Top 5 V-features có correlation cao với Class

### Step 6 — Run & Save Processed Data

```python
# Chạy ở cuối notebook
import os
import pickle
from src.preprocessing.data_loader import load_data, validate_data
from src.preprocessing.feature_scaler import scale_features
from src.preprocessing.data_splitter import split_data
from src.utils import DATA_PROCESSED_DIR

# 1. Load và validate
df = load_data()
stats = validate_data(df)
print("Dataset Stats:", stats)

# 2. Split (không tự động save vì chưa scale)
X_train, X_test, y_train, y_test = split_data(df, save=False)

# 3. Scale các cột Amount, Time
X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

# 4. Lưu processed data (đã scale)
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
- [ ] Verify split ratio: `y_train.mean() ≈ y_test.mean() ≈ 0.0017` (stratified OK)
- [ ] `notebooks/01_eda.ipynb` chạy được Restart & Run All không lỗi
- [ ] EDA notebook có ít nhất 5 visualizations
- [ ] Heatmap correlation matrix có mặt
- [ ] Class distribution chart có mặt
- [ ] Fraud vs Normal comparison có mặt

## Success Criteria

| Criterion | Expected | Evidence |
|-----------|---------|---------|
| X_train shape | (227845, 30) | ___________ |
| X_test shape | (56962, 30) | ___________ |
| y_train fraud ratio | ≈ 0.001727 | ___________ |
| y_test fraud ratio | ≈ 0.001727 | ___________ |
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
| Memory error with 284K rows | Low | Medium | Use chunked loading or pandas dtype optimization |

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
