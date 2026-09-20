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
│       │   ├── preprocessing/   ✅ data_loader, feature_scaler, data_splitter, imbalance_handler
│       │   ├── models/          ✅ random_forest_model, xgboost_model, autoencoder_model
│       │   ├── evaluation/      ✅ Phase 05 passed (06/09) — 4/4 scripts: metrics_calculator, plot_roc_curve, confusion_matrix_plot, model_comparator
│       │   └── utils/           ✅ helpers.py, constants (RANDOM_STATE=42, TEST_SIZE=0.2)
│       ├── notebooks/      ← ✅ 6/6 notebooks hoàn thành (01_eda đến 06_evaluation_comparison)
│       ├── data/
│       │   ├── raw/        ← paysim.csv (✅ đã tải, KHÔNG commit git — ~500MB)
│       │   └── processed/  ← ✅ X_train/X_test/y_train/y_test.pkl + README.md (đã commit)
│       ├── models/         ← scaler + XGBoost đã commit; RF .pkl bị gitignore
│       ├── docs/           ← ✅ 4 file kỹ thuật (overview, roadmap, architecture, code-standards)
│       ├── reports/        ← ✅ Predictions + Báo cáo DOCX/PDF Chương 1–7 (32 trang) + model_comparison.csv + figures/
│       ├── slide/          ← ✅ Bộ slide học thuật 21 trang + kịch bản toàn team (PM duyệt chính thức)
│       ├── demo/           ← ✅ Streamlit UI + XGBoost inference + Quy trình 4 bước + Import mẫu + 74 tests pass + Clip Google Drive
│       ├── run_preprocessing.py  ← Script chạy lại pipeline nếu cần
│       └── requirements.txt
└── submit/            ← Bản nộp cuối (trống cho đến khi nộp bài)
```

---

## Current State (2026-09-19)

| Component | Status |
|-----------|--------|
| Project scaffold | ✅ Done — folder structure + docs created |
| `src/utils/` | ✅ Done — helpers.py, constants, set_seeds() |
| `src/preprocessing/` | ✅ Done — data_loader, feature_scaler (14 features), data_splitter, **imbalance_handler** (SMOTENC + ADASYN) |
| `src/models/` | ✅ Done — **random_forest_model.py**, **xgboost_model.py**, **autoencoder_model.py** |
| Notebooks | ✅ 6/6 notebooks hoàn thành & chạy sạch: `01_eda.ipynb`, `02_imbalance_handling.ipynb`, `03_model_random_forest.ipynb`, `04_model_xgboost.ipynb`, `05_model_autoencoder.ipynb`, `06_evaluation_comparison.ipynb` |
| Dataset (`paysim.csv`) | ✅ Downloaded và đã verify shape (6,362,620 × 11) |
| Processed splits | ✅ X_train/X_test/y_train/y_test.pkl (160k/40k × 14) + **X_train_smote/adasyn.pkl** (230k × 14) |
| `models/scaler.pkl` | ✅ Fitted StandardScaler lưu sẵn |
| Random Forest | ✅ Đã train — SMOTE F1=0.9973/AUC=0.9994; ADASYN F1=0.9966/AUC=0.9992. Hai artifact `.pkl` bị gitignore và không có sau pull |
| `models/xgb_smote.json` | ✅ XGBoost trained — F1=0.9963, AUC=0.9993 (Train time: 41.6s) |
| `models/autoencoder_meta.json` | ✅ Autoencoder trained — AUC=0.9318, Recall=0.7523 (Threshold: 0.045456) |
| Evaluation (`src/evaluation/`) | ✅ Phase 05 `passed` (PR #26 & #28) — 4/4 scripts của Khang xong (metrics_calculator.py, plot_roc_curve.py, confusion_matrix_plot.py, model_comparator.py); `notebooks/06_evaluation_comparison.ipynb` chạy sạch; `reports/model_comparison.csv` + 7 figures đã xuất, khớp 100% `ch5_metrics_recomputed.csv`. Thêm 2 scripts vẽ đồ thị báo cáo |
| Demo UI | ✅ Phase 06 `passed` — Streamlit Web UI + XGBoost-SMOTE & scaler kết nối hoàn chỉnh; bổ sung quy trình phân tích trực quan 4 bước, hộp chọn dữ liệu mẫu hỗ trợ nhập CSV/JSON an toàn, mapping thời gian PaySim, định dạng tiền VNĐ, comparison CSV + 9 figures, 3 themes; 5 screenshots chuẩn hóa, kịch bản 7 cảnh & video clip demo; tests pass |
| Báo cáo & Slide | ✅ Phase 07 `passed` (15/09) — Word: **Tóm tắt + Chương 1–7 ✅** (Duy — DOCX/PDF 32 trang chuẩn định dạng UIT, khớp 100% Phase 05). Slide: bộ học thuật 21 trang kèm Kịch bản toàn team 7 người **đã duyệt chính thức**. |
| Gói nộp bài | ✅ Phase 08 `passed` (17/09) — Đóng gói tự động `[Project AI-UIT] - Nhom 9.zip` (47.26 MB), kiểm tra toàn vẹn và bảo mật đạt 100% |
| Docs | ✅ Đầy đủ: overview, roadmap, architecture, code-standards, data guides, Huong_dan_su_dung (Word & MD), Danh sách nhóm (Excel) |

> **Verdict (19/09/2026): Phase 00–08 TOÀN BỘ PASSED (9/9 = 100%). Đồ án hoàn thành trọn vẹn trước hạn chót. Toàn bộ mã nguồn, 6/6 notebooks, báo cáo Word/PDF 32 trang, Slide học thuật 21 trang kèm kịch bản thuyết trình toàn team, giao diện demo UI tương tác và gói nộp bài ZIP [Project AI-UIT] - Nhom 9.zip đã sẵn sàng nộp chính thức.**

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
| **Vũ Văn Duy** | Báo cáo Word (Intro+Method ngay, Results sau) | ✅ Tóm tắt + Chương 1–7 | ⏳ Đối chiếu Phase 05 |
| **Phạm Thành Trung** | Demo UI shell + Kết nối model | ✅ UI + inference | ⏳ Figures/kết luận Phase 05 |

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

## Next Actions (Sprint 3 Closing & Sprint 4 Kickoff — 09/09 → 18/09)

> **⚠️ PM Audit 09/09/2026 — Checkpoint findings & Missed Items Radar (by Hôn):**
> - **Slide Deck & Script:** Bộ Slide học thuật 21 trang (`[Nhom9]_Slide_FraudDetection_Academic_VN.pptx` & `.pdf`) và Kịch bản bảo vệ toàn team 7 người (`SCRIPT_THUYET_TRINH_TOAN_TEAM_CS106.md` & `.docx`) đã được **PM chính thức phê duyệt** và **hiệu chỉnh thời lượng thực tế** dựa trên dữ liệu buổi họp diễn tập (Dry-run meeting 18/09/2026, 49m48s). Tốc độ phát biểu WPM của 7 thành viên đã được đo lường chính xác, thời lượng toàn bài được chuẩn hóa tối ưu ở mức **~23–25 phút** (thay cho ước tính cũ phi thực tế ~15 phút).
> - **Submit Package:** Đã đóng gói hoàn chỉnh `[Project AI-UIT] - Nhom 9.zip` (47.33 MB, 124 files), bao gồm slide và kịch bản thuyết trình Word/MD.

### ✅ Thanh — DONE (Phase 00 + 01 + 01b PASSED)
- EDA notebook `notebooks/01_eda.ipynb` hoàn thành (6 visualizations, run clean)
- Preprocessing pipeline: `src/preprocessing/` hiện thực 14 đặc trưng (bổ sung 5 derived features)
- Processed splits (160k/40k × 14) và scaler được lưu vào `data/processed/` & `models/`

### ✅ Sơn — DONE (Phase 02 + 03 PASSED)
- ✅ SMOTENC (SMOTE) + ADASYN áp dụng trên train set → 4 file `.pkl` đã lưu `data/processed/`
  - SMOTE: 230,145 × 14, fraud 33.33% | ADASYN: 230,411 × 14, fraud 33.41%
  - Binary features integrity: PASS (cả 4 cột 0/1)
  - Test set untouched: y_test.mean() = 0.041075
- ✅ Random Forest trained + tuned (RandomizedSearchCV n_iter=50, cv=5, scoring=f1)
  - RF-SMOTE: **F1=0.9973, AUC=0.9994**, Precision=0.9994, Recall=0.9951
  - RF-ADASYN: **F1=0.9966, AUC=0.9992**, Precision=0.9982, Recall=0.9951
  - Best params: n_estimators=200, max_depth=20, max_features=sqrt, class_weight=balanced_subsample
  - Top feature: errorBalanceOrig (41.1%)
  - Models: rf_smote.pkl (9.2 MB), rf_adasyn.pkl (32.3 MB) — gitignored trên repo, tái lập tự động qua `run_random_forest.py`
- ✅ Notebooks `02_imbalance_handling.ipynb` và `03_model_random_forest.ipynb` hoàn thành và lưu đầy đủ biểu đồ trực quan (Clean run)

### ✅ Cẩm — DONE (Phase 04 PASSED)
- ✅ Huấn luyện & Tối ưu XGBoost trên SMOTE (`F1=0.9963, AUC=0.9993`, train time 41.6s) và ADASYN (`F1=0.9954, AUC=0.9994`)
- ✅ Huấn luyện Autoencoder (MLPRegressor) trên normal data (`AUC=0.9318, Recall=0.7523`, threshold=0.045456)
- ✅ Lưu artifact models: `models/xgb_smote.json`, `models/xgb_adasyn.json`, `models/autoencoder_threshold.txt`
- ✅ Hoàn thành 2 notebooks `04_model_xgboost.ipynb` và `05_model_autoencoder.ipynb` (đầy đủ biểu đồ visual)
- ✅ Đã bàn giao predictions: `reports/xgb_predictions.pkl`, `reports/autoencoder_predictions.pkl`

### ✅ Khang — DONE (Phase 05 PASSED)
1. ✅ `src/evaluation/metrics_calculator.py` và `plot_roc_curve.py` (merged PR #7); `confusion_matrix_plot.py` và `model_comparator.py` viết bằng TDD.
2. ✅ Toàn bộ `tests/evaluation` + `tests/demo`: 74 passed, 1 skipped.
3. ✅ `notebooks/06_evaluation_comparison.ipynb` — load predictions có sẵn, chạy sạch 0 lỗi (`jupyter nbconvert --execute`).
4. ✅ Đánh giá đủ 5 biến thể: RF-SMOTENC (F1=0.9973, best model), RF-ADASYN, XGB-SMOTENC, XGB-ADASYN, Autoencoder (Recall=0.7523, Precision=0.3822).
5. ✅ Output: `reports/model_comparison.csv` + 7 figures (`roc_curves_all.png`, `pr_curves_all.png`, 5× `confusion_matrix_*.png`) — số liệu khớp 100% với `reports/ch5_metrics_recomputed.csv` (Duy).
6. ✅ Post-review fixes: alias `confusion_matrix_rf.png`/`confusion_matrix_xgb.png`; pyplot figure lifecycle sạch; cột CSV chuẩn hóa `ROC-AUC`/`PR-AUC`.

### ✅ Trung — DONE (Phase 06 PASSED)
1. ✅ Đã kết nối `models/xgb_smote.json` + `models/scaler.pkl` vào UI với contract 14 đặc trưng
2. ✅ Đã hỗ trợ hiển thị xác suất, định dạng số tiền VNĐ và mapping thời gian PaySim (PR #27)
3. ✅ Đã Browser QA System/Sáng/Tối, xác nhận theme mặc định là Tối và chuyển theme không reload trang
4. ✅ Đã tích hợp comparison + 9 figures, gồm chuyển SMOTENC/ADASYN, Feature Importance và so sánh TP/FP/FN
5. ✅ Đã Browser QA bố cục mới trên giao diện Sáng/Tối và xác nhận không còn nhãn tiến độ nội bộ
6. ✅ Đã lưu đủ 5 ảnh chụp màn hình UI chuẩn hóa vào `demo/screenshots/` và hoàn thiện kịch bản `demo/DEMO-SCRIPT.md`.

### ✅ Duy — DONE (Phase 07 PASSED)
1. ✅ Đã viết xong toàn bộ Chương 1–7 trong `report-source.md`, xuất bản DOCX/PDF 32 trang
2. ✅ Toàn bộ số liệu Chương 5 khớp 100% `reports/model_comparison.csv` của Phase 05
3. ✅ Bổ sung phân tích Clopper-Pearson 95%, quy chiếu tỷ lệ gian lận gốc (Bảng 6.1) và Bảng 7.1 đối chiếu mục tiêu
4. ✅ Đã xuất bản tự động DOCX/PDF chuẩn định dạng báo cáo UIT với tên chuẩn `[Nhom9]_BaoCao_FraudDetection.docx` phục vụ submit.

### ✅ Hôn — DONE (Phase 07 & 08 PASSED — Final Package Ready)
1. ✅ **Chính thức phê duyệt** bộ Slide học thuật 21 trang (`[Nhom9]_Slide_FraudDetection_Academic_VN.pptx` & `.pdf`) và Kịch bản bảo vệ toàn team 7 người.
2. ✅ **Xây dựng script tự động đóng gói:** `draft/fraud-detection/src/reporting/package_submission.py`.
3. ✅ **Kiểm tra bảo mật & toàn vẹn:** Loại bỏ triệt để `paysim.csv` (470MB) và `.env` token, nén thành công `[Project AI-UIT] - Nhom 9.zip` dung lượng 47.26 MB (122 files).
4. ✅ **Bổ sung tài liệu giao nộp:** `Danh sách nhóm.xlsx` (Excel chuẩn 7 thành viên), `Huong_dan_su_dung.docx`/`.md`.
5. ✅ **Sẵn sàng nộp bài:** Nhóm trưởng Hôn đại diện nộp file ZIP lên hệ thống môn học CS106 đúng hạn (trước 18/09/2026).


