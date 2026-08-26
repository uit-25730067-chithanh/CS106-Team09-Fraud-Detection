# Code Standards — Fraud Detection Project

## Quy ước đặt tên

- **Files**: snake_case cho các file Python (`data_loader.py`, `random_forest_model.py`), kebab-case cho các loại file khác (Markdown, Config, Directories)
- **Functions/Variables**: snake_case (`load_data()`, `X_train`, `y_test`)
- **Classes**: PascalCase (`FraudDetector`, `DataPreprocessor`)
- **Constants**: UPPER_SNAKE_CASE (`RANDOM_STATE = 42`, `TEST_SIZE = 0.2`)

## Cấu trúc Notebook

Mỗi notebook tuân theo cấu trúc:
```
# Tiêu đề notebook
## 0. Imports
## 1. Load Data
## 2. [Nội dung chính]
## 3. Kết luận / Observations
```

## Reproducibility

Luôn set random seed:
```python
import numpy as np
import random

RANDOM_STATE = 42
np.random.seed(RANDOM_STATE)
random.seed(RANDOM_STATE)
```

## Git Conventions

- Mỗi người làm trên notebook/script của mình — không sửa file người khác
- Commit message: `feat: add XGBoost training notebook` hoặc `fix: fix SMOTE overfit`
- Không commit `data/raw/paysim.csv` vào git (>100MB)

## Evaluation Checklist

Trước khi báo cáo, đảm bảo mỗi model có đủ:
- [ ] Confusion Matrix
- [ ] Precision, Recall, F1-Score (class 0 và class 1)
- [ ] ROC-AUC Score
- [ ] Thời gian training
