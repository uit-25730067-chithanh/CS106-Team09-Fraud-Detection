# Phase 00 — Environment & Data Setup

**Parent plan:** [plan.md](./plan.md)  
**Next phase:** [Phase 01 — EDA & Preprocessing](./phase-01-eda-preprocessing.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Thanh** |
| Priority | P0 — Blocker cho toàn bộ pipeline |
| Status | `completed` |
| Review | ⬜ Not reviewed |
| Estimated effort | 30 phút |
| Sprint | Sprint 1 |

## Context

Project scaffold đã có sẵn tại `draft/fraud-detection/`. Cần:
1. Cài venv + dependencies
2. Tải dataset `paysim.csv` từ Kaggle (và đổi tên từ file log gốc)
3. Verify toàn bộ imports work

## Requirements

- Python 3.10+
- `data/raw/paysim.csv` phải có mặt (6,362,620 rows × 11 cols)
- Tất cả packages trong `requirements.txt` cài được
- `RANDOM_STATE = 42` set trong mọi script

## Key Insights

- Dataset ~150MB → không commit git (đã có trong `.gitignore`)
- `tensorflow` có thể conflict với numpy version → pin numpy<2.0 nếu cần
- macOS M1/M2: dùng `tensorflow-macos` thay `tensorflow` nếu cần

## Related Files

```
draft/fraud-detection/
├── requirements.txt          ← Install target
├── .gitignore                ← Verify csv excluded
├── data/raw/                 ← Đặt paysim.csv vào đây
│   └── .gitkeep
└── src/utils/
    ├── __init__.py
    └── helpers.py            ← Tạo constants + helpers cơ bản
```

## Implementation Steps

### Step 1 — Setup Virtual Environment

```bash
cd draft/fraud-detection
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
pip install --upgrade pip
pip install -r requirements.txt
```

> ⚠️ Nếu `tensorflow` fail trên Apple Silicon: thay bằng `tensorflow-macos` và `tensorflow-metal`

### Step 2 — Download Dataset

```bash
# Option A: Kaggle CLI
pip install kaggle
kaggle datasets download ealaxi/paysim1
unzip paysim1.zip -d data/raw/
mv data/raw/PS_20174392719_1491204439457_log.csv data/raw/paysim.csv
rm paysim1.zip

# Option B: Manual
# Truy cập: https://www.kaggle.com/datasets/ealaxi/paysim1
# Tải file log .csv → đổi tên thành paysim.csv -> đặt vào data/raw/
```

### Step 3 — Create Utility Files

**`src/utils/helpers.py`** — constants và helpers dùng chung:

```python
"""Shared constants and utility helpers for the fraud detection project."""
import numpy as np
import random

# ─── Constants ────────────────────────────────────────────────────────────────
RANDOM_STATE = 42
TEST_SIZE = 0.2
DATA_RAW_PATH = "data/raw/paysim.csv"
DATA_PROCESSED_DIR = "data/processed"

# ─── Reproducibility ──────────────────────────────────────────────────────────

def set_seeds(seed: int = RANDOM_STATE) -> None:
    """Set all random seeds for reproducibility."""
    np.random.seed(seed)
    random.seed(seed)

# ─── Path helpers ─────────────────────────────────────────────────────────────

def get_project_root() -> str:
    """Return the project root directory (fraud-detection/)."""
    import os
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

**`src/utils/__init__.py`** — expose public API:

```python
from .helpers import RANDOM_STATE, TEST_SIZE, DATA_RAW_PATH, DATA_PROCESSED_DIR, set_seeds, get_project_root

__all__ = [
    "RANDOM_STATE",
    "TEST_SIZE",
    "DATA_RAW_PATH",
    "DATA_PROCESSED_DIR",
    "set_seeds",
    "get_project_root",
]
```

### Step 4 — Verify Installation

```python
# Chạy trong Python REPL hoặc notebook cell
import pandas as pd
import numpy as np
import sklearn
import xgboost
import imblearn
import tensorflow
import matplotlib
import seaborn
print("All imports OK")
print(f"Pandas: {pd.__version__}")
print(f"Sklearn: {sklearn.__version__}")
print(f"XGBoost: {xgboost.__version__}")

df = pd.read_csv("data/raw/paysim.csv")
print(f"Dataset shape: {df.shape}")  # Expected: (6362620, 11)
print(f"Fraud ratio: {df['isFraud'].mean():.6f}")  # Expected: ~0.00129
```

## Checklist

- [x] `python -m venv .venv` tạo được venv
- [x] `pip install -r requirements.txt` không error
- [x] `data/raw/paysim.csv` có mặt, size ~500MB
- [x] `df.shape == (6362620, 11)` ✅
- [x] `df['isFraud'].mean() ≈ 0.00129` ✅
- [x] `src/utils/helpers.py` có `RANDOM_STATE`, `set_seeds()`, `get_project_root()`
- [x] Tất cả imports (pandas, sklearn, xgboost, imblearn, tensorflow) không lỗi
- [x] `.gitignore` exclude `*.csv` và `.venv/`

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| Dataset loaded | `df.shape == (6362620, 11)` (Passed) |
| Fraud ratio correct | `df['isFraud'].mean() ≈ 0.00129` (Passed) |
| All imports work | Verified using `verify_setup.py` |
| Utils module works | `from src.utils import RANDOM_STATE` works |

## Evidence Section *(điền sau khi làm)*

```
df.shape      = (6362620, 11)
fraud_ratio   = 0.001291
sklearn ver   = 1.9.0
xgboost ver   = 3.4.1
tf ver        = 2.21.0
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| tensorflow conflict (numpy) | Medium | Medium | Pin `numpy<2.0`, use `tensorflow-macos` on M-series (Resolved by pinning numpy<2.0.0) |
| Kaggle auth fail | Low | Low | Manual download fallback (Resolved by configuring access_token and downloading via Kaggle CLI) |
| Disk space | Low | Low | CSV ~500MB, ensure ≥1GB free |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ Hoàn thành hoàn toàn — Đã hoàn thành phần cài đặt môi trường ảo, utilities và dataset.

```
Hoàn thành setup env: 28/08/2026
Người thực hiện: Thanh
Kết quả thực tế:
- Đã tạo venv, nâng cấp pip và cài đặt thành công mọi packages trong requirements.txt.
- Sửa requirements.txt để pin numpy < 2.0.0 tránh xung đột với tensorflow.
- Tạo files utils helpers và init hoạt động tốt.
- Tải dataset tự động thành công thông qua Kaggle CLI sau khi cấu hình access_token.
- Viết file test tự động src/verify_setup.py chạy thành công 100% cho phần package imports, utilities, và dataset validation (Shape: (6362620, 11), Fraud ratio: 0.001291).
```

## Commit

```bash
git add src/utils/ data/raw/.gitkeep src/verify_setup.py requirements.txt plans/fraud-detection-full-submit/phase-00-env-data-setup.md
git commit -m "feat(phase00): env setup, utils helpers, dataset verified"
```
