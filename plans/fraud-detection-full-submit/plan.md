---
title: "CS106 Final — Fraud Detection Full Implementation to Submit"
description: "End-to-end implementation plan: từ code rỗng đến bản nộp hoàn chỉnh, chia theo phase độc lập có validation gate"
status: in-progress
priority: P1
effort: ~40h (7 người)
branch: main
tags: [cs106, fraud-detection, academic, python, ml, submit]
created: 2026-08-24
updated: 2026-09-04
sprints: 4 sprints | Sprint review mỗi tối Thứ 6 | Bắt đầu 25/8 | Deadline 18/9
---

# Plan: CS106 Final — Fraud Detection Full Submit

## Mục tiêu

Từ skeleton hiện tại (docs + structure, không có code) → bản nộp hoàn chỉnh:
`[Project AI-UIT] - Nhom 9.zip` với đủ: code, notebooks, báo cáo Word, PPT, demo.

## Sprint Timeline

| Sprint | Thời gian | Mục tiêu chính | Sprint Review |
|--------|----------|---------------|---------------|
| **Sprint 1** | 25/8 – 28/8 | Setup repo + Scaffold, phân chia công việc | Tối Thứ 6 28/8 |
| **Sprint 2** | 28/8 – 4/9 | Tải dữ liệu, EDA, Preprocessing, Phân tích imbalance. Mã nguồn đánh giá mẫu & UI shell | Tối Thứ 6 4/9 |
| **Sprint 3** | 4/9 – 11/9 | Xử lý imbalance (SMOTE/ADASYN), Modeling (RF, XGBoost, Autoencoder). Viết Methodology | Tối Thứ 6 11/9 |
| **Sprint 4** | 11/9 – 18/9 | Evaluation, Demo UI kết nối model thật, Báo cáo & PPT hoàn thiện, Đóng gói nộp bài | Deadline 18/9 |

> ⚡ Nhóm Đánh giá, Báo cáo & Demo (Khang, Trung, Duy, Hôn) bắt đầu triển khai song song từ Sprint 2.
> Phase files 05–07 có mục `Early Start Tasks` cho các thành viên thực hiện trước.

## Constraints

- Dataset: `paysim.csv` (~500MB) — phải tải thủ công từ Kaggle, không commit git, downsample khi preprocess
- Tech: Python 3.10+, scikit-learn, xgboost, imbalanced-learn, keras/tensorflow
- Mỗi người làm phần riêng → gom vào 1 commit chung
- Phase phải passed validation gate trước khi chuyển tiếp
- Tóm lược phase viết **sau khi code xong** (evidence-based, không phải plan)

## Phase Overview

| # | Phase | Owner | Sprint | Status | Gate |
|---|-------|-------|--------|--------|------|
| 00 | [Environment & Data Setup](./phase-00-env-data-setup.md) | Thanh | Sprint 1 | `passed` ✅ | Dataset loaded, venv OK, imports work |
| 01 | [EDA & Preprocessing](./phase-01-eda-preprocessing.md) | Thanh | Sprint 2 | `passed` ✅ | Notebooks chạy, processed data saved |
| 02 | [Imbalance Handling](./phase-02-imbalance-handling.md) | Sơn | Sprint 3 | `passed` ✅ | SMOTENC+ADASYN applied, 4 pkl saved, binary integrity PASS |
| 03 | [Modeling — Random Forest](./phase-03-model-random-forest.md) | Sơn | Sprint 3 | `passed` ✅ | RF-SMOTE F1=0.9973 AUC=0.9994, RF-ADASYN F1=0.9966 AUC=0.9992 (digits=4 synced) |
| 04 | [Modeling — XGBoost + Autoencoder](./phase-04-model-xgboost-autoencoder.md) | Cẩm | Sprint 3 | `passed` ✅ | XGB-SMOTE F1=0.9963/AUC=0.9993; Autoencoder Recall=0.75/AUC=0.93 (MLPRegressor — TF thiếu Python 3.14) |
| 05 | [Evaluation & Comparison](./phase-05-evaluation-comparison.md) | Khang | Sprint 2–4* | `pending` | 2/4 scripts done (PR #7 merged); còn thiếu confusion_matrix_plot.py + model_comparator.py + notebook 06 |
| 06 | [Demo UI](./phase-06-demo-ui.md) | Trung | Sprint 2–4* | `pending` | UI shell Rev 7.7 verified; chờ model integration + browser QA + screenshots/clip |
| 07 | [Report & PPT](./phase-07-report-ppt.md) | Duy + Hôn | Sprint 2–4* | `pending` | Word: Chương 1-3 ✅ (Duy) + PPT 15 slides ✅ (Hôn) + Slide học thuật 24 trang ✅ (PR #13); Chương 4-6 chưa viết |
| 08 | [Submit Package](./phase-08-submit-package.md) | Hôn | Sprint 4 | `pending` | Blocked by 05–07; ⚠️ cần 6 notebooks (hiện chỉ có 3) |

> \* Phase 05–07 có **Early Start Tasks** bắt đầu từ Sprint 2. Xem chi tiết trong từng file.
>
> **Phase 06 — Trung — checkpoint 29/08/2026:** UI shell Revision 7.7 đã được xác minh ở cấp code, AppTest và local runtime. Phase vẫn `pending`; còn browser/pixel QA, tích hợp model và figures thật, screenshot và demo clip.
>
> **Phase 07 — Duy & Hôn — checkpoint 04/09/2026:** Bản nháp Báo cáo Word Sprint 2 (Chương 1, 2, 3 + Threats to Validity) của Duy đã hoàn thành và merge vào `main`. Bộ Slide PPT chính thức (15 slides) và Slide học thuật 24 trang đã hoàn tất. Phase vẫn `pending` chờ Methodology (Chương 4 — Duy có thể viết ngay) và Results/Conclusion (Chương 5-6 — cần Phase 05).
>
> **PM Audit — Hôn — 04/09/2026:** Scout toàn bộ file tree phát hiện 17 items cần xử lý: 3 notebooks thiếu (02, 03, 06), 2 scripts evaluation chưa tạo, thư mục `reports/figures/` và `reports/model_comparison.csv` chưa tồn tại, RF `.pkl` bị gitignore, và Phase 08 checklist tham chiếu sai (`autoencoder.h5` → `autoencoder_meta.json`). Tiến độ tổng thể 5/9 phases = 55.6%, đúng Sprint timeline.

## Git Convention

- Làm riêng → 1 commit gộp cuối mỗi phase: `feat(phaseXX): <description>`
- Không commit: `data/raw/*.csv`, `.venv/`, `__pycache__/`, `*.pkl > 50MB`

## Validation Rules (áp dụng cho mọi phase)

Một phase được coi là **PASSED** khi:
1. ✅ Tất cả checklist items trong phase file được tick
2. ✅ Evidence section điền đầy đủ (output thực tế, không phải expected)
3. ✅ Summary section viết dựa trên code đã làm (không phải plan)
4. ❌ Nếu bất kỳ item nào FAIL → phase chưa passed, không chuyển tiếp
