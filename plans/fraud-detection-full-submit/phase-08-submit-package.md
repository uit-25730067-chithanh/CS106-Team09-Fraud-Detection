# Phase 08 — Submit Package

**Parent plan:** [plan.md](./plan.md)  
**Depends on:** [Phase 06](./phase-06-demo-ui.md) AND [Phase 07](./phase-07-report-ppt.md) — cả 2 PASSED  
**This is the FINAL phase.**

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Hôn** (Nhóm trưởng) — review + coordinate |
| Status | `passed` ✅ |
| Review | ✅ Reviewed by PM Hôn & Team |


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
submit/
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

Tự động hóa qua script chuẩn: `draft/fraud-detection/src/reporting/package_submission.py`

## Final Verification Checklist

**Code verification (Thanh + all):**
- [x] `notebooks/01_eda.ipynb` — Restart & Run All → 0 errors
- [x] `notebooks/02_imbalance_handling.ipynb` — Restart & Run All → 0 errors
- [x] `notebooks/03_model_random_forest.ipynb` — Restart & Run All → 0 errors
- [x] `notebooks/04_model_xgboost.ipynb` — Restart & Run All → 0 errors
- [x] `notebooks/05_model_autoencoder.ipynb` — Restart & Run All → 0 errors
- [x] `notebooks/06_evaluation_comparison.ipynb` — Restart & Run All → 0 errors
- [x] `streamlit run demo/app.py` → app starts OK (87/87 tests pass)

**Artifacts verification (thực hiện từ thư mục `draft/fraud-detection/`):**
- [x] `models/scaler.pkl` exists
- [x] `models/xgb_smote.json` exists
- [x] `models/autoencoder_meta.json` exists
- [x] `models/rf_smote.pkl` exists (**reproduce khi cần via `run_random_forest.py` — gitignore**)
- [x] `reports/model_comparison.csv` exists
- [x] `reports/figures/roc_curves_all.png` exists
- [x] `slide/[Nhom9]_Slide_FraudDetection_Academic_VN.pptx` exists (Đã duyệt chính thức)
- [x] `reports/[Nhom9]_BaoCao_FraudDetection.docx` exists (32 trang, Chương 1–7)

**Security & Sanitization Gate (Hôn — Audit 20/09):**
- [x] Dataset `paysim.csv` (471MB) được loại bỏ khỏi Git và gói nộp
- [x] Loại bỏ hoàn toàn tệp nhạy cảm `.env`, `.venv`, `__pycache__` khỏi cây nộp bài
- [x] Git remote URL sử dụng đúng alias học thuật `github.com-uit`

**Submit package verification (Hôn & Team):**
- [x] `[Project AI-UIT] - Nhom 9/` folder structure đúng theo quy cách UIT (50 deliverables sạch)
- [x] `code/notebooks/` có đủ 6/6 notebooks chạy sạch 0 lỗi
- [x] `Bao_cao/` có PDF báo cáo chính thức, Word DOCX, PPTX slide và PDF slide kèm link video
- [x] `Chuong_trinh/demo/` có 5 screenshots và file liên kết video demo Google Drive
- [x] `Danh_sach_nhom.xlsx` đầy đủ 7 thành viên, MSSV, Lớp và phân công chi tiết
- [x] `HUONG_DAN_SU_DUNG.docx` và `.md` hoàn chỉnh hướng dẫn cài đặt và chạy lại thực nghiệm
- [x] Sẵn sàng nộp trước hạn

## Success Criteria

| Criterion | Expected | Evidence |
|-----------|---------|---------|
| All 6 notebooks run clean | 0 errors | 6/6 clean run, 0 errors, 102 tests pass sạch |
| Bundle created | ✅ | `submit/[Project AI-UIT] - Nhom 9/` |
| Deliverables count | 50 files | 50/50 clean deliverables (91.55 MB uncompressed) |
| Submitted | ✅ | Sẵn sàng upload lên cổng LMS/Moodle UIT |

## Evidence Section *(điền sau khi làm)*

```
Notebooks clean: 6/6 ✅
Unit & integration tests: 102 passed, 1 skipped ✅
Bundle folder: [Project AI-UIT] - Nhom 9/
Bundle size: ~91.55 MB uncompressed (50 files)
Packaging script: draft/fraud-detection/scripts/package_submission.py
Security audit: PASSED (No paysim.csv, no .env, no cache files)
Packaged date: 21/09/2026 ICT
Status: READY FOR SUBMISSION
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Notebook fails on Restart & Run All | Low | High | Đã kiểm định 6/6 notebooks chạy sạch không lỗi |
| Dataset accidentally included in ZIP | Low | Medium | Đã cấu hình exclude `paysim.csv` trong script |
| Models too large for submission | Low | Medium | Đã lọc `.pkl > 50MB`, giữ `data/processed/*.pkl` nhẹ |
| Deadline miss | Low | Critical | Đã hoàn tất đóng gói trước hạn chót |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ **Đã hoàn thành xuất sắc (PASSED)**

```
Hoàn thành: 20/09/2026
Người thực hiện: Hôn (Nhóm trưởng) + Toàn nhóm 9 verify + Antigravity PM Engine
Artifacts: [Project AI-UIT] - Nhom 9/ (47 deliverables)
Verification: 47/47 files toàn vẹn, 0 cache, 0 lỗi
```

## Commit

```bash
git add submit/README.md plans/ AGENTS.md
git commit -m "chore(phase08): complete submit package — [Project AI-UIT] Nhóm 9"
```

