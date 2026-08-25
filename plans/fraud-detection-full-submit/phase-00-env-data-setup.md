# Phase 00 — Environment & Data Setup

**Parent plan:** [plan.md](./plan.md)  
**Next phase:** [Phase 01 — EDA & Preprocessing](./phase-01-eda-preprocessing.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Thanh** |
| Priority | P0 — Blocker cho toàn bộ pipeline |
| Status | `pending` |
| Review | ⬜ Not reviewed |
| Estimated effort | 30 phút |
| Sprint | Sprint 1 |

## Context

Project scaffold đã có sẵn tại `draft/fraud-detection/`. Cần:
1. Cài venv + dependencies
2. Tải dataset `creditcard.csv` từ Kaggle
3. Verify toàn bộ imports work

## Requirements

- Python 3.10+
- `data/raw/creditcard.csv` phải có mặt (284,807 rows × 31 cols)
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
├── data/raw/                 ← Đặt creditcard.csv vào đây
│   └── DOWNLOAD_DATA_HERE.txt
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
# Option A: Kaggle CLI (khuyên dùng)
pip install kaggle
kaggle datasets download mlg-ulb/creditcardfraud
unzip creditcardfraud.zip -d data/raw/
rm creditcardfraud.zip

# Option B: Manual
# Truy cập: https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
# Tải creditcard.csv → đặt vào data/raw/
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
DATA_RAW_PATH = "data/raw/creditcard.csv"
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

df = pd.read_csv("data/raw/creditcard.csv")
print(f"Dataset shape: {df.shape}")  # Expected: (284807, 31)
print(f"Fraud ratio: {df['Class'].mean():.4f}")  # Expected: ~0.0017
```

## Checklist

- [ ] `python -m venv .venv` tạo được venv
- [ ] `pip install -r requirements.txt` không error
- [ ] `data/raw/creditcard.csv` có mặt, size ~150MB
- [ ] `df.shape == (284807, 31)` ✅
- [ ] `df['Class'].mean() ≈ 0.0017` ✅
- [ ] `src/utils/helpers.py` có `RANDOM_STATE`, `set_seeds()`, `get_project_root()`
- [ ] Tất cả imports (pandas, sklearn, xgboost, imblearn, tensorflow) không lỗi
- [ ] `.gitignore` exclude `*.csv` và `.venv/`

## Success Criteria

| Criterion | Evidence |
|-----------|---------|
| Dataset loaded | `df.shape == (284807, 31)` |
| Fraud ratio correct | `df['Class'].mean() ≈ 0.001727` |
| All imports work | No ImportError |
| Utils module works | `from src.utils import RANDOM_STATE` works |

## Evidence Section *(điền sau khi làm)*

```
df.shape      = ________________
fraud_ratio   = ________________
sklearn ver   = ________________
xgboost ver   = ________________
tf ver        = ________________
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| tensorflow conflict (numpy) | Medium | Medium | Pin `numpy<2.0`, use `tensorflow-macos` on M-series |
| Kaggle auth fail | Low | Low | Manual download fallback |
| Disk space | Low | Low | CSV ~150MB, ensure ≥500MB free |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa hoàn thành — điền vào sau khi tất cả checklist PASSED

```
Hoàn thành: __/__/2026
Người thực hiện: Thanh
Kết quả thực tế:
- ...
Issues gặp phải:
- ...
```

## Commit

```bash
git add src/utils/ data/raw/.gitkeep
git commit -m "feat(phase00): env setup, utils helpers, dataset verified"
```
