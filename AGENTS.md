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

## Current State (2026-08-29)

| Component | Status |
|-----------|--------|
| Project scaffold | ✅ Done — folder structure + docs created |
| `src/utils/` | ✅ Done — helpers.py, constants, set_seeds() |
| `src/preprocessing/` | ✅ Done — data_loader, feature_scaler (14 features: 5 derived + 2 error balances + 1 OHE), data_splitter |
| Notebooks | ✅ `01_eda.ipynb` hoàn chỉnh và đã execute |
| Dataset (`paysim.csv`) | ✅ Downloaded và đã verify shape (6,362,620 × 11) |
| Processed splits | ✅ X_train/X_test/y_train/y_test.pkl (shape: 160k/40k × 14) |
| `models/scaler.pkl` | ✅ Fitted StandardScaler lưu sẵn |
| Demo UI | 🟡 Phase 06 `pending` — UI shell Revision 7.7 đã xác minh ở cấp code, AppTest và local runtime. Có System/Sáng/Tối, 3 quick presets và 3 góc nhìn giao dịch; còn browser/pixel QA, model integration, figures và demo clip |
| Báo cáo & Slide | ✅ Nháp Chương 1, 2, 3 Word/PDF (Duy) & Slide PPT 9 slides PPTX/PDF (Hôn) đã hoàn tất tại `reports/` |
| Docs | ✅ 4 files: overview, roadmap, architecture, code-standards |

> **Verdict: Phase 00, 01 & 01b PASSED. Báo cáo nháp Sprint 2 (Word/PDF) & Slide PPT nháp (9 slides) hoàn tất. Sẵn sàng bàn giao Sơn (Phase 02).**

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

### Sơn — Bắt đầu Phase 02
1. `git pull` trên branch `main` (dữ liệu `X_train.pkl` đã có 14 features)
2. Load `data/processed/X_train.pkl` và `y_train.pkl`
3. Apply SMOTE và ADASYN (chỉ trên train set)
   - *Lưu ý*: Với các cờ nhị phân (`is_drain_account`, `is_night_transaction`, `is_large_transaction`, `type_TRANSFER`), cân nhắc dùng `SMOTENC` hoặc làm tròn `np.round()` sau khi oversampling để bảo toàn giá trị 0/1.
4. Xem chi tiết: `plans/fraud-detection-full-submit/phase-02-imbalance-handling.md`

### Khang
1. Viết `src/evaluation/metrics_calculator.py` (template — không cần data)
2. Viết `src/evaluation/plot_roc_curve.py` template

### Trung
1. ✅ Hoàn thành UI shell Revision 7.7: form PaySim, safe-preview, System/Sáng/Tối, 3 quick presets và 3 góc nhìn giao dịch
2. ✅ Xác minh AppTest `0 exceptions`, local root/health `200` và không hiển thị kết quả mô hình giả
3. ⏳ Click và review pixel System/Sáng/Tối
4. ⏳ Nhận artifacts Phase 04–05, tích hợp inference/figures thật và quay demo clip

### Duy — DONE SPRINT 2 DRAFT ✅
1. ✅ Đã viết xong Chương 1, 2, 3 trong `reports/report-source.md` và `[Nhom9]_BaoCao...docx` (đã merge `main`)
2. ⏳ Chuẩn bị viết Chương 4 (Methodology) ở Sprint 3

### Hôn — DONE SPRINT 2 PPT DRAFT ✅
1. ✅ Đã thiết kế template và hoàn thành 9 slides PPT mở đầu (`[Nhom9]_Slide_FraudDetection_Hon.pptx/.pdf`)
2. ⏳ Chuẩn bị tiếp nhận số liệu kết quả (Khang) và screenshot Demo (Trung) ở Sprint 4 để hoàn thiện slide kết quả.
