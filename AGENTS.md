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

## Current State (2026-09-04)

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
| `models/rf_smote.pkl` | ✅ RF trained — F1=0.9973, AUC=0.9994 (digits=4 chuẩn hóa từ PR #15) |
| `models/rf_adasyn.pkl` | ✅ RF trained — F1=0.9966, AUC=0.9992 (digits=4 chuẩn hóa từ PR #15) |
| `models/xgb_smote.json` | ✅ XGBoost trained — F1=0.9963, AUC=0.9993 (Train time: 41.6s) |
| `models/autoencoder_meta.json` | ✅ Autoencoder trained — AUC=0.9318, Recall=0.7523 (Threshold: 0.045456) |
| Evaluation (`src/evaluation/`) | 🟡 Phase 05 `pending` — 2/4 scripts của Khang đã merge (metrics_calculator.py + plot_roc_curve.py, PR #7); **còn thiếu** confusion_matrix_plot.py + model_comparator.py; chưa chạy cross-model evaluation; chưa có `reports/model_comparison.csv`. Duy đã thêm plot_confusion_components.py + plot_feature_importance.py phục vụ báo cáo (branch riêng) |
| Demo UI | 🟡 Phase 06 `pending` — UI shell Revision 7.7 đã xác minh (code, AppTest, local runtime); còn thiếu browser/pixel QA, model integration, comparison figures, screenshots, demo clip |
| Báo cáo & Slide | 🟡 Word: **Chương 1–6 ✅** (Duy — DOCX/PDF 28 trang, mục lục 46 mục, 2 hình, 10 bảng, sinh tự động từ source, visual QA pass, trên branch riêng); **Chương 7 và Abstract chưa viết**. PPT: 15 slides ✅ (Hôn) + Slide học thuật ✅ (PR #13). Kịch bản thuyết trình chưa hoàn thiện |
| Notebooks | ⚠️ **Thiếu 3 notebooks**: `02_imbalance_handling.ipynb` (Sơn), `03_model_random_forest.ipynb` (Sơn), `06_evaluation_comparison.ipynb` (Khang) — cần cho submit package |
| Docs | ✅ Đầy đủ: overview, roadmap, architecture, code-standards, data guides |

> **Verdict (04/09): Phase 00–04 PASSED (5/9 = 55.6%). Toàn bộ 3 họ mô hình đã hoàn thành. Đang Sprint 3: Khang cần hoàn thành Phase 05 (2 scripts + notebook 06 + chạy metrics), Trung chờ model integration, Duy đã xong Chương 1–6, còn Chương 7 (Kết luận) và Abstract. ⚠️ Sơn cần tạo 2 notebooks (02, 03) còn thiếu cho submit package.**

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
  → [data_loader.py]        Load & validate CSV + Downsampling (200k rows)
  → [data_splitter.py]      Stratified 80/20 split  ← TRƯỚC khi fit scaler
  → [feature_scaler.py]     Derived features + OHE type; StandardScaler fit trên TRAIN, transform TEST
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
| **Vũ Văn Duy** | Báo cáo Word (Intro+Method ngay, Results sau) | ✅ Chương 1–4 | ⏳ Results từ Phase 05 |
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

## Next Actions (Sprint 3 — 04/09 → 11/09)

> **⚠️ PM Audit 04/09/2026 — Checkpoint findings (by Hôn):**
> - 5/9 phases passed (55.6%); Sprint 3 đúng tiến độ.
> - **3 notebooks còn thiếu** cần tạo trước submit: `02_imbalance_handling.ipynb` (Sơn), `03_model_random_forest.ipynb` (Sơn), `06_evaluation_comparison.ipynb` (Khang).
> - RF model `.pkl` files bị gitignore, chỉ có local — team cần reproduce hoặc Sơn share offline.
> - `reports/figures/` chưa tồn tại — Khang sẽ tạo khi chạy Phase 05.
> - Phase 08 checklist cần chỉnh: `autoencoder.h5` → `autoencoder_meta.json` (dùng MLPRegressor, không Keras).

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
  - Models: rf_smote.pkl (9.2 MB), rf_adasyn.pkl (32.3 MB) — ⚠️ gitignored, local only
- ⚠️ **Notebooks `02_imbalance_handling.ipynb` và `03_model_random_forest.ipynb` CẦN TẠO trước Sprint 4** (submit package cần 6 notebooks)

### ✅ Cẩm — DONE (Phase 04 PASSED) — 01/09/2026
- ✅ Huấn luyện & Tối ưu XGBoost trên SMOTE (`F1=0.9963, AUC=0.9993`, train time 41.6s) và ADASYN (`F1=0.9954, AUC=0.9994`)
- ✅ Huấn luyện Autoencoder (MLPRegressor) trên normal data (`AUC=0.9318, Recall=0.7523`, threshold=0.045456)
- ✅ Lưu artifact models: `models/xgb_smote.json`, `models/xgb_adasyn.json`, `models/autoencoder_threshold.txt`
- ✅ Hoàn thành 2 notebooks `04_model_xgboost.ipynb` và `05_model_autoencoder.ipynb` (đầy đủ biểu đồ visual)
- ✅ Đã bàn giao predictions cho Khang: `reports/xgb_predictions.pkl`, `reports/autoencoder_predictions.pkl`

### 🔄 Khang — Phase 05 (Evaluation & Comparison) — IN PROGRESS
1. ✅ Đã viết xong `src/evaluation/metrics_calculator.py` và `plot_roc_curve.py` (Unit tests pass 100%, merged PR #7).
2. ✅ Đầy đủ predictions từ cả 3 mô hình đã có sẵn tại `reports/`:
   - `rf_predictions.pkl` (Random Forest)
   - `xgb_predictions.pkl` (XGBoost)
   - `autoencoder_predictions.pkl` (Autoencoder)
3. ⏳ **Sprint 3 TODO (ưu tiên cao):**
   - Viết `confusion_matrix_plot.py` — template có sẵn trong phase file
   - Viết `model_comparator.py` — template có sẵn trong phase file
   - Tạo `notebooks/06_evaluation_comparison.ipynb`
   - Chạy evaluation cho cả 3 mô hình → xuất `reports/figures/` + `reports/model_comparison.csv`

### 🔄 Trung — Phase 06 (Demo UI Integration) — BLOCKED on Phase 05
1. ✅ UI shell Revision 7.7 verified (code + AppTest + local runtime)
2. ⏳ Cần model weights: `models/xgb_smote.json` ✅ có sẵn + `models/scaler.pkl` ✅ có sẵn
3. ⏳ Kết nối pipeline inference vào `demo/app.py`
4. ⏳ Browser/pixel QA System/Sáng/Tối
5. ⏳ Chụp screenshots QA và quay video demo clip

### Duy — Báo cáo Word
1. ✅ Đã viết xong Chương 1–6 trên branch `docs/vu-van-duy-sprint3-methodology`
2. ✅ Toàn bộ số liệu Chương 5 tính lại được bằng `run_report_metrics.py` → `reports/ch5_metrics_recomputed.csv` (gồm Average Precision cho cả 5 biến thể) và sinh lại được 2 hình
3. ✅ Mục 5.5 trả lời câu hỏi nghiên cứu về feature importance (Bảng 5.2 + Hình 5.2): nhóm đặc trưng số dư chiếm 90,5% (RF) và 99,3% (XGB) mức đóng góp
4. ✅ DOCX/PDF sinh tự động từ `report-source.md` bằng `build_report.py` + `sync_toc_pages.py` — Sprint 4 chỉ cần sửa source rồi chạy lại
5. ✅ Chương 6 (Thảo luận) hoàn thành: trả lời 3 câu hỏi nghiên cứu, quy chiếu Precision về tỷ lệ gian lận gốc (Bảng 6.1) và chỉ ra khác biệt giữa 4 biến thể chưa đủ tin cậy thống kê. Còn chờ `model_comparison.csv` + ROC/PR curves của Phase 05 để đối chiếu lần cuối
6. ⏳ Viết Chương 7 (Kết luận và hướng phát triển) và Abstract
7. ⏳ Cần Sơn/Cẩm hỗ trợ ablation loại nhóm đặc trưng số dư — bằng chứng quyết định cho Chương 6 (xem Mục 3.6.2 và 5.5)

### 🔄 Hôn — PM + PPT — PARTIALLY BLOCKED
1. ✅ Đã hoàn thành 15 slides PPTX/PDF hoàn chỉnh với đầy đủ số liệu thực nghiệm
2. ✅ Đã tích hợp bộ Slide học thuật 24 trang song ngữ EN-VN từ PR #13
3. ✅ **PM Audit Sprint 3** hoàn thành — phát hiện 17 missed items (xem bảng trên)
4. ⏳ Chuẩn bị kịch bản thuyết trình 10–12 phút
5. ⏳ Phối hợp Trung chụp ảnh Demo UI → cập nhật Slide 13
6. ⏳ Phase 08: Đóng gói submit package (blocked by Phase 05–07)


