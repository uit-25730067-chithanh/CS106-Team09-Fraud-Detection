# Phase 08 — Submit Package

**Parent plan:** [plan.md](./plan.md)  
**Depends on:** [Phase 06](./phase-06-demo-ui.md) AND [Phase 07](./phase-07-report-ppt.md) — cả 2 PASSED  
**This is the FINAL phase.**

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Hôn** (Nhóm trưởng) — review + coordinate |
| Priority | P0 — Final gate |
| Status | `pending` |
| Review | ⬜ Not reviewed |
| Estimated effort | 1–2 giờ |
| Sprint | Sprint 4 |

## Context

Phase cuối: gộp tất cả, final verification, đóng gói ZIP, nộp bài. Hôn chịu trách nhiệm coordinate mọi người commit xong trước khi đóng gói.

## Requirements

- Tất cả notebooks phải **Restart & Run All** không error
- Tên file nộp: `[Project AI-UIT] - Nhom 9.zip`
- Cấu trúc submit package đúng theo quy định

- `Restart & Run All` quan trọng — tránh trường hợp notebook chạy được vì có cached variables
- Không commit dataset `paysim.csv` vào git (>100MB)
- Cần kiểm tra artifacts tại `draft/fraud-detection/models/` (`scaler.pkl`, `xgb_smote.json`, `autoencoder_meta.json`) tồn tại trước khi đóng gói
- ⚠️ RF models (`draft/fraud-detection/models/rf_smote.pkl`, `rf_adasyn.pkl`) bị gitignore — cần reproduce hoặc share offline

## 💡 Ý tưởng Đề xuất & Cải tiến Nâng cao (từ MY_IDEAS)

1. **Kiểm tra tính toàn vẹn đa nền tảng (Cross-Platform Reproduction):**
   * Đảm bảo pipeline và notebooks chạy độc lập từ file `data/processed/*.pkl` mà không cần tải lại tập thô 500MB `paysim.csv`.
2. **Đồng bộ hóa 4 sản phẩm giao nộp (Deliverables Audit):**
   * **Báo cáo Word:** Khớp 100% số liệu với bảng `reports/model_comparison.csv` và ảnh biểu đồ trong `reports/figures/`.
   * **Slide PPT:** Trình bày rõ nét các điểm nhấn: Anti-leakage, Feature engineering, So sánh đa trường phái, Explainable AI (SHAP) và Threats to validity.
   * **Mã nguồn:** Thư mục `src/` modular, sạch sẽ, notebooks chạy không còn warning.
   * **Demo UI:** Cung cấp đầy đủ hướng dẫn chạy Streamlit và video/ảnh chụp màn hình minh họa.

## Pre-Commit Verification

Trước khi mỗi người commit phần cuối, kiểm tra:

```bash
# Verify không có untracked sensitive files
git status
# Verify .gitignore đang hoạt động
git check-ignore data/raw/paysim.csv  # phải bị ignore
```

## Final Git Flow

```bash
# Step 1: Mỗi người commit phần của mình (đã làm ở phase trước)
# Step 2: Gộp (nếu dùng branches)
git merge feat/phase03-rf
git merge feat/phase04-xgb-autoencoder
# ...

# Step 3: Final commit với summary
git add .
git commit -m "feat: complete fraud detection pipeline — ready for submission"

# Step 4: Tag release
git tag -a v1.0 -m "CS106 Final Submission — Nhóm 9"
git push origin main --tags
```

## Submit Package Structure

```
Final/submit/
└── [Project AI-UIT] - Nhom 9/
    ├── code/
    │   ├── src/
    │   │   ├── preprocessing/
    │   │   ├── models/
    │   │   ├── evaluation/
    │   │   └── utils/
    │   ├── notebooks/
    │   │   ├── 01_eda.ipynb
    │   │   ├── 02_imbalance_handling.ipynb
    │   │   ├── 03_model_random_forest.ipynb
    │   │   ├── 04_model_xgboost.ipynb
    │   │   ├── 05_model_autoencoder.ipynb
    │   │   └── 06_evaluation_comparison.ipynb
    │   ├── demo/
    │   │   └── app.py
    │   └── requirements.txt
    ├── report/
    │   └── [Nhom9]_BaoCao_FraudDetection.docx
    ├── slides/
    │   └── [Nhom9]_PPT_FraudDetection.pptx
    └── demo/
        └── screenshots/ (or demo_clip.mp4)
```

## Packaging Script

```bash
# Tạo submit directory
SUBMIT_DIR="submit/[Project AI-UIT] - Nhom 9"
mkdir -p "$SUBMIT_DIR/code" "$SUBMIT_DIR/report" "$SUBMIT_DIR/slides" "$SUBMIT_DIR/demo"

# Copy code (exclude data/raw and .venv)
cp -r draft/fraud-detection/src "$SUBMIT_DIR/code/"
cp -r draft/fraud-detection/notebooks "$SUBMIT_DIR/code/"
cp -r draft/fraud-detection/demo "$SUBMIT_DIR/code/"
cp draft/fraud-detection/requirements.txt "$SUBMIT_DIR/code/"

# Copy reports & slides
cp draft/fraud-detection/reports/*.docx "$SUBMIT_DIR/report/"
cp draft/fraud-detection/slide/*.pptx "$SUBMIT_DIR/slides/"  # slide chính thức (đang xem xét)
cp -r draft/fraud-detection/demo/screenshots "$SUBMIT_DIR/demo/"

# Create ZIP
cd submit
zip -r "[Project AI-UIT] - Nhom 9.zip" "[Project AI-UIT] - Nhom 9/"
echo "ZIP created: [Project AI-UIT] - Nhom 9.zip"
```

## Final Verification Checklist

**Code verification (Thanh + all):**
- [x] `notebooks/01_eda.ipynb` — Restart & Run All → 0 errors
- [x] `notebooks/02_imbalance_handling.ipynb` — Restart & Run All → 0 errors
- [x] `notebooks/03_model_random_forest.ipynb` — Restart & Run All → 0 errors
- [x] `notebooks/04_model_xgboost.ipynb` — Restart & Run All → 0 errors
- [x] `notebooks/05_model_autoencoder.ipynb` — Restart & Run All → 0 errors
- [x] `notebooks/06_evaluation_comparison.ipynb` — Restart & Run All → 0 errors
- [x] `streamlit run demo/app.py` → app starts OK (74 tests pass)

**Artifacts verification (thực hiện từ thư mục `draft/fraud-detection/`):**
- [x] `models/scaler.pkl` exists
- [x] `models/xgb_smote.json` exists
- [x] `models/autoencoder_meta.json` exists
- [ ] `models/rf_smote.pkl` exists (**reproduce khi cần via `run_random_forest.py` — gitignore**)
- [x] `reports/model_comparison.csv` exists
- [x] `reports/figures/roc_curves_all.png` exists
- [x] `slide/[Nhom9]_Slide_FraudDetection_Academic_VN.pptx` exists (Đã duyệt chính thức)
- [ ] `reports/[Nhom9]_BaoCao_FraudDetection.docx` exists (Đang xuất bản cuối từ `report-source.md`)

**Security & Sanitization Gate (Hôn — Audit 09/09):**
- [x] Dataset `paysim.csv` (470MB) được loại bỏ khỏi Git và gói nộp ZIP
- [ ] Loại bỏ tệp nhạy cảm `.env` (chứa KAGGLE_API_TOKEN) khỏi cây nộp bài
- [x] Git remote URL sử dụng đúng alias học thuật `github.com-uit`

**Submit package verification (Hôn):**
- [ ] `[Project AI-UIT] - Nhom 9/` folder structure đúng
- [x] `code/notebooks/` có đủ 6/6 notebooks
- [ ] `report/` có Word file bản nộp chính thức
- [x] `slides/` có PPT file chính thức 21 slide
- [ ] `demo/` có screenshots hoặc clip
- [ ] ZIP tạo thành công: `[Project AI-UIT] - Nhom 9.zip`
- [ ] ZIP size hợp lý (< 500MB, loại bỏ paysim.csv)
- [ ] Test unzip và kiểm tra nội dung
- [ ] Nộp đúng hạn (trước 18/9/2026)

## Success Criteria

| Criterion | Expected | Evidence |
|-----------|---------|---------|
| All 6 notebooks run clean | 0 errors | ___________ |
| ZIP created | ✅ | ___________ |
| ZIP size | < 500MB | ___________ |
| Submitted | ✅ | ___________ |

## Evidence Section *(điền sau khi làm)*

```
Notebooks clean: 6/6 ✅/❌
ZIP filename: [Project AI-UIT] - Nhom 9.zip
ZIP size: ____ MB
Submit date: __/__/2026 __:__ ICT
Submit link/confirmation: ____________________
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Notebook fails on Restart & Run All | Medium | High | Fix errors before packaging |
| Dataset accidentally included in ZIP | Low | Medium | Verify ZIP size, check .gitignore |
| Models too large for submission | Low | Medium | Exclude large .h5 if > 50MB; note in README |
| Deadline miss | Low | Critical | Submit 1 day early as buffer |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa hoàn thành

```
Hoàn thành: __/__/2026
Người thực hiện: Hôn (+ toàn nhóm verify)
Submitted at: __:__ ICT __/__/2026
Confirmation: ____________________
```

## Commit

```bash
git add Final/submit/
git commit -m "chore(phase08): final submit package ready — [Project AI-UIT] Nhóm 9"
git tag -a v1.0 -m "CS106 Final Submission"
```
