# Phase 02 — Imbalance Handling (SMOTE / ADASYN)

**Parent plan:** [plan.md](./plan.md)  
**Depends on:** [Phase 01](./phase-01-eda-preprocessing.md) — PASSED (processed splits available)  
**Next phase:** [Phase 03 — Random Forest](./phase-03-model-random-forest.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Sơn** |
| Priority | P0 — Yêu cầu cho modeling |
| Status | `pending` |
| Review | ⬜ Not reviewed |
| Estimated effort | 1–2 giờ |
| Sprint | Sprint 3 |

## Context

Phase 01 đã tạo `data/processed/X_train.pkl` và `y_train.pkl` (imbalanced).  
Phase này apply SMOTE và ADASYN **chỉ trên train set** để tạo balanced version.

> **CRITICAL:** Test set KHÔNG được touch — phải giữ nguyên distribution thực tế để evaluation có ý nghĩa.

## Requirements

- Input: `data/processed/X_train.pkl`, `y_train.pkl`
- Output:
  - `data/processed/X_train_smote.pkl`, `y_train_smote.pkl`
  - `data/processed/X_train_adasyn.pkl`, `y_train_adasyn.pkl`
- So sánh class distribution trước/sau cho cả 2 phương pháp
- Lưu logs/stats vào report

## Key Insights

- SMOTE: synthetic oversampling — tạo điểm mới nội suy giữa các minority samples
- ADASYN: adaptive — tập trung vào các vùng khó classify hơn
- Nên thử cả 2, so sánh ở Phase 05 để xem cái nào cho model tốt hơn
- Sau SMOTE/ADASYN: `y_train.value_counts()` sẽ ~50/50 hoặc theo ratio đặt

## Related Files

```
draft/fraud-detection/
├── notebooks/
│   └── 02_imbalance_handling.ipynb    ← [TẠO MỚI]
├── src/preprocessing/
│   └── imbalance_handler.py           ← [TẠO MỚI]
└── data/processed/
    ├── X_train_smote.pkl              ← OUTPUT
    ├── y_train_smote.pkl              ← OUTPUT
    ├── X_train_adasyn.pkl             ← OUTPUT
    └── y_train_adasyn.pkl             ← OUTPUT
```

## Implementation Steps

### Step 1 — `src/preprocessing/imbalance_handler.py`

```python
"""SMOTE and ADASYN implementations for handling class imbalance."""
import pickle
import numpy as np
import pandas as pd
from pathlib import Path
from imblearn.over_sampling import SMOTE, ADASYN
from src.utils import RANDOM_STATE, DATA_PROCESSED_DIR


def apply_smote(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    sampling_strategy: float = 0.5,
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Apply SMOTE to oversample minority class.
    
    sampling_strategy=0.5 means minority:majority = 1:2 after resampling.
    Does NOT modify test set — call only on train data.
    """
    smote = SMOTE(
        sampling_strategy=sampling_strategy,
        random_state=random_state,
        n_jobs=-1,
    )
    X_res, y_res = smote.fit_resample(X_train, y_train)
    return pd.DataFrame(X_res, columns=X_train.columns), pd.Series(y_res)


def apply_adasyn(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    sampling_strategy: float = 0.5,
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Apply ADASYN to oversample minority class (adaptive density).
    """
    adasyn = ADASYN(
        sampling_strategy=sampling_strategy,
        random_state=random_state,
        n_jobs=-1,
    )
    X_res, y_res = adasyn.fit_resample(X_train, y_train)
    return pd.DataFrame(X_res, columns=X_train.columns), pd.Series(y_res)


def save_resampled(
    X: pd.DataFrame,
    y: pd.Series,
    method: str,  # "smote" or "adasyn"
    out_dir: str = DATA_PROCESSED_DIR,
) -> None:
    """Persist resampled train data as pickle files."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    for name, obj in [(f"X_train_{method}", X), (f"y_train_{method}", y)]:
        with open(f"{out_dir}/{name}.pkl", "wb") as f:
            pickle.dump(obj, f)
    print(f"Saved {method} resampled data → {out_dir}/")


def report_class_distribution(
    y_original: pd.Series,
    y_smote: pd.Series,
    y_adasyn: pd.Series,
) -> pd.DataFrame:
    """Print and return class distribution comparison."""
    rows = []
    for name, y in [("Original", y_original), ("SMOTE", y_smote), ("ADASYN", y_adasyn)]:
        counts = y.value_counts().sort_index()
        rows.append({
            "Method": name,
            "Normal (0)": counts.get(0, 0),
            "Fraud (1)": counts.get(1, 0),
            "Total": len(y),
            "Fraud %": f"{y.mean()*100:.2f}%",
        })
    return pd.DataFrame(rows)
```

### Step 2 — `notebooks/02_imbalance_handling.ipynb`

```
## 0. Imports & Setup
## 1. Load Processed Data (từ data/processed/)
## 2. Original Class Distribution (bar chart)
## 3. Apply SMOTE
   - Distribution sau SMOTE (bar chart)
   - So sánh trước/sau
## 4. Apply ADASYN
   - Distribution sau ADASYN (bar chart)
   - So sánh trước/sau
## 5. Summary Table (Original vs SMOTE vs ADASYN)
## 6. Save Resampled Data
## 7. Kết luận
```

**Key code trong notebook:**

```python
import pickle
import pandas as pd
from src.preprocessing.imbalance_handler import apply_smote, apply_adasyn, save_resampled, report_class_distribution

# Load train data
with open("data/processed/X_train.pkl", "rb") as f: X_train = pickle.load(f)
with open("data/processed/y_train.pkl", "rb") as f: y_train = pickle.load(f)

# Apply both methods
X_smote, y_smote = apply_smote(X_train, y_train)
X_adasyn, y_adasyn = apply_adasyn(X_train, y_train)

# Save
save_resampled(X_smote, y_smote, "smote")
save_resampled(X_adasyn, y_adasyn, "adasyn")

# Report
df_report = report_class_distribution(y_train, y_smote, y_adasyn)
print(df_report.to_string(index=False))
```

## Checklist

- [ ] `src/preprocessing/imbalance_handler.py` tạo xong với `apply_smote()`, `apply_adasyn()`, `save_resampled()`, `report_class_distribution()`
- [ ] SMOTE chỉ apply trên X_train (KHÔNG phải X_test)
- [ ] ADASYN chỉ apply trên X_train (KHÔNG phải X_test)
- [ ] `data/processed/X_train_smote.pkl` tồn tại
- [ ] `data/processed/y_train_smote.pkl` tồn tại
- [ ] `data/processed/X_train_adasyn.pkl` tồn tại
- [ ] `data/processed/y_train_adasyn.pkl` tồn tại
- [ ] `y_train_smote.mean()` > `y_train.mean()` (imbalance đã được xử lý)
- [ ] `y_train_adasyn.mean()` > `y_train.mean()`
- [ ] Notebook `02_imbalance_handling.ipynb` chạy clean
- [ ] Summary table (Original vs SMOTE vs ADASYN) có trong notebook

## Success Criteria

| Criterion | Expected | Evidence |
|-----------|---------|---------|
| y_train_smote fraud % | ~33% (sampling_strategy=0.5) | ___________ |
| y_train_adasyn fraud % | ~33% | ___________ |
| Test set untouched | y_test.mean() ≈ 0.0017 | ___________ |
| 4 new pkl files created | ✅ | ___________ |

## Evidence Section *(điền sau khi làm)*

```
Original y_train fraud ratio = ________________
After SMOTE  y_train ratio   = ________________
After ADASYN y_train ratio   = ________________
y_test.mean() (unchanged)    = ________________
SMOTE X_train_smote.shape    = ________________
ADASYN X_train_adasyn.shape  = ________________
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| SMOTE OOM (large synthetic) | Low | Medium | Use sampling_strategy=0.1 if memory issue |
| ADASYN neighbors fail (sparse fraud) | Low | Low | Fallback to SMOTE only |
| Data leakage (apply on test) | Low but catastrophic | Critical | Code review gate before next phase |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa hoàn thành

```
Hoàn thành: __/__/2026
Người thực hiện: Sơn
Kết quả thực tế:
- SMOTE: Original ... → Resampled ...
- ADASYN: Original ... → Resampled ...
Issues gặp phải:
- ...
```

## Commit

```bash
git add src/preprocessing/imbalance-handler.py notebooks/02_imbalance_handling.ipynb data/processed/
git commit -m "feat(phase02): SMOTE + ADASYN imbalance handling, resampled data saved"
```
