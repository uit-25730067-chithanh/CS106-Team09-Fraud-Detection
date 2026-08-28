# AGENTS.md — CS106 Final Project Context

> Agent context file. Cung cấp ngữ cảnh cho AI assistants làm việc với project này.

---

## Project Identity

- **Course:** CS106 — Trí tuệ Nhân tạo, UIT ĐHQG-HCM
- **Assignment:** Final — Đề tài #7 (Fraud Detection)
- **Group:** Nhóm 9, 7 thành viên

---

## Directory Layout

```
Final/
├── docs/              ← PDF đề bài gốc từ GV
├── draft/
│   └── fraud-detection/    ← Working project (đang phát triển)
│       ├── src/            ← Python scripts (CHƯA CÓ CODE)
│       │   ├── preprocessing/   # data_loader, feature_scaler, data_splitter, imbalance_handler
│       │   ├── models/          # random_forest_model, xgboost_model, autoencoder_model
│       │   ├── evaluation/      # metrics_calculator, plot_roc_curve, confusion_matrix_plot, model_comparator
│       │   └── utils/           # helpers, constants
│       ├── notebooks/      ← Jupyter notebooks (CHƯA CÓ)
│       ├── data/raw/       ← paysim.csv (CHƯA TẢI)
│       ├── data/processed/ ← Output từ preprocessing pipeline
│       ├── docs/           ← Tài liệu kỹ thuật (đã có 4 file)
│       ├── reports/        ← Kết quả (trống)
│       ├── demo/           ← Streamlit UI (trống)
│       └── requirements.txt
└── submit/            ← Bản nộp cuối (trống cho đến khi nộp bài)
```

---

## Current State (2026-08-25)

| Component | Status |
|-----------|--------|
| Project scaffold | ✅ Done — folder structure (with `.gitkeep`) + docs created |
| `src/` Python files | ❌ Empty — directories created but no `.py` files |
| Notebooks | ❌ Empty — directory created but no `.ipynb` files |
| Dataset (`paysim.csv`) | ❌ Not downloaded yet |
| Docs | ✅ 4 files: overview, roadmap, architecture, code-standards |

> **Verdict: ~20% complete.** Planning & scaffold done, implementation not started.

---

## Conventions (follow these when writing code)

- **Files:** snake_case cho file Python (`data_loader.py`, `random_forest_model.py`), kebab-case cho các loại file khác
- **Functions/Variables:** snake_case — `load_data()`, `X_train`, `y_test`
- **Classes:** PascalCase — `FraudDetector`, `DataPreprocessor`
- **Constants:** UPPER_SNAKE_CASE — `RANDOM_STATE = 42`, `TEST_SIZE = 0.2`
- **Random seed:** Always set `RANDOM_STATE = 42`
- **Git:** Do NOT commit `data/raw/paysim.csv` (>100MB)

---

## Pipeline Overview

```
paysim.csv
  → [data_loader.py]        Load & validate CSV
  → [feature_scaler.py]     StandardScaler on numericals, OHE on categorical Type, and Downsampling
  → [data_splitter.py]      Stratified 80/20 split
  → [imbalance_handler.py]  SMOTE/ADASYN on train only (no leakage)
  → [random_forest_model.py / xgboost_model.py / autoencoder_model.py]
  → [metrics_calculator.py] F1, ROC-AUC, Precision, Recall
  → [model_comparator.py]   Cross-model comparison table
```

**Key design decisions:**
1. SMOTE/ADASYN only on TRAIN set — never touch test set
2. Stratified split — maintain fraud ratio in both splits
3. Do NOT use Accuracy as primary metric (imbalanced data)
4. Each model gets its own notebook — avoid merge conflicts

---

## Data

| Field | Value |
|-------|-------|
| Source | Kaggle: `ealaxi/paysim1` |
| Shape | 6,362,620 rows × 11 cols (Downsampled to ~200k rows) |
| Features | step, type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest |
| Label | isFraud (0=normal, 1=fraud) |
| Fraud ratio | ~0.13% (8,213 fraud / 6.36M total) |

---

## Team & Responsibilities

> 📌 **Chi tiết tasks theo phase:** [project-roadmap.md](./draft/fraud-detection/docs/project-roadmap.md)

### 🔵 Nhóm Preprocessing & Modeling

| Member | Task chính | Sprint |
|--------|-----------|--------|
| **Đặng Chí Thanh** | EDA, Preprocessing, Feature Engineering | Sprint 2 |
| **Hoàng Cao Sơn** | Imbalance Analysis, SMOTE/ADASYN, Random Forest | Sprint 2–3 |
| **Bùi Thị Mỷ Cẩm** | XGBoost, Autoencoder, Lưu models (.pkl/.h5) | Sprint 3 |

### 🟡 Nhóm Đánh giá, Báo cáo & Demo

| Member | Task chính | Bắt đầu song song | Phụ thuộc đầu ra từ mô hình |
|--------|-----------|------------------|----------|
| **Trần Hoàng Hôn** | PM + PPT template + Nộp bài | ✅ PPT template | ⏳ Số liệu kết quả |
| **Nguyễn Duy Khang** | Viết evaluation scripts + Chạy metrics | ✅ Viết scripts | ⏳ Chạy sau Sprint 3 |
| **Vũ Văn Duy** | Báo cáo Word (Intro+Method ngay, Results sau) | ✅ ~70% ngay | ⏳ Results |
| **Phạm Thành Trung** | Demo UI shell + Kết nối model | ✅ UI shell ngay | ⏳ `.pkl` từ Cẩm |

Pipeline dữ liệu có sự tuần tự giữa các thành viên phụ trách mô hình để đảm bảo tính nhất quán.

---

## Submission Format

Final package name: `[Project AI-UIT] - Nhom 9.zip`

Contents:
```
[Project AI-UIT] - Nhom 9/
├── code/          ← src/ + notebooks/
├── report/        ← Word document
├── slides/        ← PPT
└── demo/          ← Clip/screenshot demo
```

Place in `Final/submit/` before zipping.

---

## Next Actions (bắt đầu Sprint 2 - 28/08)

### Thanh
1. Download dataset: https://www.kaggle.com/datasets/ealaxi/paysim1 → `draft/fraud-detection/data/raw/paysim.csv`
2. Setup venv: `cd draft/fraud-detection && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
3. Start EDA: Create `notebooks/01_eda.ipynb`
4. Implement preprocessing scripts in `src/preprocessing/`

### Khang
1. Viết `src/evaluation/metrics-calculator.py` (template — không cần data)
2. Viết `src/evaluation/plot-roc-curve.py` template

### Trung
1. Thiết kế wireframe UI → bắt đầu Streamlit form nhập liệu

### Duy
1. Mở Word → viết phần Introduction + Problem Statement

### Hôn
1. Tạo file PPT → chọn theme → thiết kế layout template
