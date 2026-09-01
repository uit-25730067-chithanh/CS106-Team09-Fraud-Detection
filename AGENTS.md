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
├── AGENTS.md          ← File này — context cho AI agents
├── draft/
│   └── fraud-detection/    ← Working project
│       ├── src/            ← Python source code
│       │   ├── preprocessing/   ✅ data_loader, feature_scaler, data_splitter
│       │   ├── models/          ⏳ random_forest_model, xgboost_model, autoencoder_model
│       │   ├── evaluation/      ⏳ metrics_calculator, plot_roc_curve, model_comparator
│       │   └── utils/           ✅ helpers.py, constants (RANDOM_STATE=42, TEST_SIZE=0.2)
│       ├── notebooks/      ← Jupyter notebooks
│       │   └── 01_eda.ipynb    ✅ Hoàn thành (6 biểu đồ, run clean)
│       ├── data/
│       │   ├── raw/        ← paysim.csv (✅ đã tải, KHÔNG commit git — ~500MB)
│       │   └── processed/  ← ✅ X_train/X_test/y_train/y_test.pkl + README.md (đã commit)
│       ├── models/         ← ✅ scaler.pkl (đã commit); model lớn sẽ gitignored
│       ├── docs/           ← ✅ 4 file kỹ thuật (overview, roadmap, architecture, code-standards)
│       ├── reports/        ← Kết quả (trống — Sprint 3+)
│       ├── demo/           ← ✅ Streamlit UI shell + wireframe; ⏳ model thật
│       ├── run_preprocessing.py  ← Script chạy lại pipeline nếu cần
│       └── requirements.txt
└── submit/            ← Bản nộp cuối (trống cho đến khi nộp bài)
```

---

## Current State (2026-09-01)

| Component | Status |
|-----------|--------|
| Project scaffold | ✅ Done — folder structure + docs created |
| `src/utils/` | ✅ Done — helpers.py, constants, set_seeds() |
| `src/preprocessing/` | ✅ Done — data_loader, feature_scaler (14 features), data_splitter, **imbalance_handler** (SMOTENC + ADASYN) |
| `src/models/` | ✅ Done — **random_forest_model.py**, **xgboost_model.py**, **autoencoder_model.py** |
| Notebooks | ✅ `01_eda.ipynb`, `04_model_xgboost.ipynb`, `05_model_autoencoder.ipynb` hoàn chỉnh |
| Dataset (`paysim.csv`) | ✅ Downloaded và đã verify shape (6,362,620 × 11) |
| Processed splits | ✅ X_train/X_test/y_train/y_test.pkl (160k/40k × 14) + **X_train_smote/adasyn.pkl** (230k × 14) |
| `models/scaler.pkl` | ✅ Fitted StandardScaler lưu sẵn |
| `models/rf_smote.pkl` | ✅ RF trained — F1=0.9973, AUC=0.9994 (9.2 MB) |
| `models/rf_adasyn.pkl` | ✅ RF trained — F1=0.9966, AUC=0.9992 (32.3 MB) |
| `models/xgb_smote.json` | ✅ XGBoost trained — F1=0.9963, AUC=0.9993 (Train time: 41.6s) |
| `models/autoencoder_meta.json` | ✅ Autoencoder trained — AUC=0.9318, Recall=0.7523 (Threshold: 0.045456) |
| Evaluation (`src/evaluation/`) | 🟡 Phase 05 in progress — metrics_calculator.py & plot_roc_curve.py merged; sẵn sàng chạy cross-model evaluation |
| Demo UI | 🟡 Phase 06 `pending` — UI shell Revision 7.7 đã xác minh; sẵn sàng nạp model thật |
| Báo cáo & Slide | ✅ Nháp Chương 1, 2, 3 Word/PDF (Duy) & Slide PPT 15 slides PPTX/PDF (Hôn) đã hoàn tất |
| Docs | ✅ Đầy đủ: overview, roadmap, architecture, code-standards, data guides |

> **Verdict: Phase 00, 01, 01b, 02, 03 & 04 PASSED. Toàn bộ 3 họ mô hình (Random Forest, XGBoost, Autoencoder) đã hoàn thành xuất sắc. Sẵn sàng cho Khang (Phase 05 - Evaluation) và Trung (Phase 06 - UI Integration).**

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

## Agent Workflow — Post-Implementation Checklist

> **BẮT BUỘC cho mọi AI agent sau khi implement xong 1 phase.**
> Đây là quy trình chuẩn đã được thiết lập sau Phase 01.

### Sau khi code xong, agent phải làm theo thứ tự:

```
[1] Verify pipeline chạy đúng
    → Chạy lại script chính, kiểm tra output shape/ratio khớp Success Criteria
    → Không claim "done" nếu chưa chạy thực tế

[2] Update phase file (plans/fraud-detection-full-submit/phase-XX-*.md)
    → Điền Evidence section bằng output THỰC TẾ (không phải expected)
    → Tick [x] tất cả checklist items
    → Viết Summary sau khi code xong

[3] Update plan.md (plans/fraud-detection-full-submit/plan.md)
    → Đổi status phase vừa xong: pending → passed ✅
    → Cập nhật field updated: với ngày thực tế

[4] Update AGENTS.md (file này)
    → Cập nhật bảng Current State
    → Cập nhật Next Actions cho thành viên tiếp theo

[5] Update docs/ (nếu architecture/data thay đổi)
    → system-architecture.md: cập nhật pipeline diagram nếu có bước mới
    → project-overview-pdr.md: cập nhật số liệu nếu thay đổi

[6] Update README files (nếu cần)
    → draft/fraud-detection/README.md: cập nhật Workflow status ✔/→
    → Final/README.md: cập nhật Sprint progress

[7] Xử lý artifacts (data, models)
    → Kiểm tra file .pkl nào team cần → đảm bảo KHÔNG bị gitignore
    → Processed data (< ~50MB) → commit luôn để team dùng
    → Model lớn (> 50MB) → để trong gitignore, ghi hướng dẫn reproduce

[8] Commit
    → feat(phaseXX): <mô tả ngắn>  ← code + notebook
    → docs(phaseXX): <mô tả ngắn> ← docs/README riêng nếu nhiều thay đổi
```

### File nào phải update sau mỗi phase

| File | Khi nào cập nhật |
|------|----------------|
| `plans/.../phase-XX-*.md` | Luôn luôn — điền Evidence + Summary |
| `plans/.../plan.md` | Luôn luôn — đổi status + updated date |
| `AGENTS.md` | Luôn luôn — Current State + Next Actions |
| `draft/fraud-detection/README.md` | Khi có file mới hoặc workflow thay đổi |
| `Final/README.md` | Khi sprint status thay đổi |
| `docs/system-architecture.md` | Khi pipeline có thêm/bớt bước |
| `data/processed/README.md` | Khi có file .pkl mới được tạo ra |

### Quy tắc về .pkl và artifacts

- `data/raw/paysim.csv` → **KHÔNG bao giờ commit** (500MB)
- `data/processed/*.pkl` (splits, scaler) → **Commit luôn** nếu < 50MB
- `models/scaler.pkl` → **Commit luôn** (nhỏ, team UI cần)  
- `models/rf_*.pkl`, `models/xgboost_*.pkl` → **Gitignore** (thường > 50MB)
- Khi gitignore model lớn → ghi rõ lệnh reproduce trong phase file

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

## Next Actions (Sprint 2/3 — 28/08 → 04/09)

### ✅ Thanh — DONE (Phase 00 + 01 + 01b PASSED)
- EDA notebook `notebooks/01_eda.ipynb` hoàn thành (6 visualizations, run clean)
- Preprocessing pipeline: `src/preprocessing/` hiện thực 14 đặc trưng (bổ sung 5 derived features)
- Processed splits (160k/40k × 14) và scaler được lưu vào `data/processed/` & `models/`

### ✅ Sơn — DONE (Phase 02 + 03 PASSED) — 31/08/2026
- ✅ SMOTENC (SMOTE) + ADASYN áp dụng trên train set → 4 file `.pkl` đã lưu `data/processed/`
  - SMOTE: 230,145 × 14, fraud 33.33% | ADASYN: 230,411 × 14, fraud 33.41%
  - Binary features integrity: PASS (cả 4 cột 0/1)
  - Test set untouched: y_test.mean() = 0.041075
- ✅ Random Forest trained + tuned (RandomizedSearchCV n_iter=50, cv=5, scoring=f1)
  - RF-SMOTE: **F1=0.9973, AUC=0.9994**, Precision=0.9994, Recall=0.9951
  - RF-ADASYN: **F1=0.9966, AUC=0.9992**, Precision=0.9982, Recall=0.9951
  - Best params: n_estimators=200, max_depth=20, max_features=sqrt, class_weight=balanced_subsample
  - Top feature: errorBalanceOrig (41.1%)
  - Models: rf_smote.pkl (9.2 MB), rf_adasyn.pkl (32.3 MB)
- ⏳ Notebooks `02_imbalance_handling.ipynb` và `03_model_random_forest.ipynb` cần tạo

### ✅ Cẩm — DONE (Phase 04 PASSED) — 01/09/2026
- ✅ Huấn luyện & Tối ưu XGBoost trên SMOTE (`F1=0.9963, AUC=0.9993`, train time 41.6s) và ADASYN (`F1=0.9954, AUC=0.9994`)
- ✅ Huấn luyện Autoencoder (MLPRegressor) trên normal data (`AUC=0.9318, Recall=0.7523`, threshold=0.045456)
- ✅ Lưu artifact models: `models/xgb_smote.json`, `models/xgb_adasyn.json`, `models/autoencoder_threshold.txt`
- ✅ Hoàn thành 2 notebooks `04_model_xgboost.ipynb` và `05_model_autoencoder.ipynb` (đầy đủ biểu đồ visual)
- ✅ Đã bàn giao predictions cho Khang: `reports/xgb_predictions.pkl`, `reports/autoencoder_predictions.pkl`

### Khang — Phase 05 (Evaluation & Comparison)
1. ✅ Đã viết xong `src/evaluation/metrics_calculator.py` và `plot_roc_curve.py` (Unit tests pass 100%).
2. ✅ Đầy đủ predictions từ cả 3 mô hình đã có sẵn tại `reports/`:
   - `rf_predictions.pkl` (Random Forest)
   - `xgb_predictions.pkl` (XGBoost)
   - `autoencoder_predictions.pkl` (Autoencoder)
3. ⏳ Viết nốt `confusion_matrix_plot.py`, `model_comparator.py` và xuất bảng so sánh tổng hợp chéo (Cross-model comparison table) cùng biểu đồ ROC / PR curves so sánh 3 mô hình.

### Trung — Bắt đầu Tích hợp Model vào Demo UI (Phase 06)
1. Đã có weights mô hình: `models/xgb_smote.json` / `models/rf_smote.pkl` và `models/scaler.pkl`
2. Kết nối pipeline inference vào `demo/app.py` để dự đoán xác suất gian lận thời gian thực
3. Chụp screenshots QA và quay video demo clip

### Duy — Báo cáo Word
1. ✅ Đã viết xong Chương 1, 2, 3
2. ⏳ Viết Chương 4 (Methodology) & Chương 5 (Experimental Results): Đã có toàn bộ số liệu của cả 3 mô hình (RF, XGB, Autoencoder)

### Hôn — Slide Thuyết trình PPT
1. ✅ Đã hoàn thành 9 slides nháp mở đầu
2. ⏳ Điền bảng số liệu thực nghiệm và biểu đồ so sánh mô hình vào các slides kết quả (Slide 10-15)

