---
title: "CS106 Final — Fraud Detection Full Implementation to Submit"
description: "End-to-end implementation plan: từ code rỗng đến bản nộp hoàn chỉnh, chia theo phase độc lập có validation gate"
status: in-progress
priority: P1
effort: ~40h (7 người)
branch: main
tags: [cs106, fraud-detection, academic, python, ml, submit]
created: 2026-08-24
updated: 2026-09-05
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
| **Sprint 4** | 11/9 – 18/9 | Evaluation, Demo UI browser QA + figures + evidence, Báo cáo & PPT hoàn thiện, Đóng gói nộp bài | Deadline 18/9 |

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
| 06 | [Demo UI](./phase-06-demo-ui.md) | Trung | Sprint 2–4* | `pending` | UI, inference, adapter Phase 05 và Browser QA đã xong; chờ artifacts chính thức + screenshots/clip |
| 07 | [Report & PPT](./phase-07-report-ppt.md) | Duy + Hôn | Sprint 2–4* | `pending` | Word/PDF Tóm tắt + Chương 1–7 ✅ 32 trang (Duy), chờ đối chiếu Phase 05; PPT: bộ slide học thuật 21 trang & Kịch bản toàn team (đang xem xét) |
| 08 | [Submit Package](./phase-08-submit-package.md) | Hôn | Sprint 4 | `pending` | Blocked by 05–07; Đã có 5/6 notebooks (chỉ còn thiếu 06 của Khang) |

> \* Phase 05–07 có **Early Start Tasks** bắt đầu từ Sprint 2. Xem chi tiết trong từng file.
>
> **Phase 06 — Trung — checkpoint 05/09/2026:** Đã hoàn tất UI, XGBoost inference, mẫu test có nhãn, adapter fail-closed cho comparison CSV + 5 figures và Browser QA System/Sáng/Tối; `13` demo tests và `21` tests toàn project đều pass. Phase vẫn `pending`; còn artifacts chính thức Phase 05, screenshots hiện tại và demo clip.
>
> **Phase 07 — Duy & Hôn — checkpoint 04/09/2026:** Duy đã hoàn thành Chương 1–7 của báo cáo. Chương 4 Phương pháp và Chương 5 Kết quả được tái tính từ prediction artifacts, Chương 6 Thảo luận bổ sung phép quy chiếu Precision về tỷ lệ gian lận gốc cùng phân tích khoảng tin cậy cho thấy khác biệt giữa bốn biến thể học có giám sát chưa đủ tin cậy để xếp hạng, Chương 7 Kết luận có Bảng 7.1 đối chiếu bảy mục tiêu của Mục 1.3.2. Bản DOCX/PDF 31 trang được sinh tự động từ `report-source.md` bằng `build_report.py`, và toàn bộ số liệu tái lập được bằng `run_report_metrics.py`. Bộ slide học thuật 21 trang cùng Kịch bản toàn team đang được xem xét làm bản chính thức. Phase vẫn `pending` chờ Phase 05 xuất comparison CSV cùng ROC/PR figures để đối chiếu, và chờ viết Abstract.
>
> **PM Audit — Hôn — 04/09/2026:** Tiến độ notebooks: Sơn đã bổ sung notebook 02 và 03 (hiện có 5/6, chỉ còn thiếu 06 của Khang). 2 scripts evaluation của Khang chưa tạo, `reports/model_comparison.csv` chưa tồn tại, RF `.pkl` bị gitignore. Tiến độ tổng thể 5/9 phases = 55.6%, đúng Sprint timeline. *Cập nhật:* `reports/figures/` đã có trên nhánh báo cáo của Duy với 2 hình dùng cho Chương 5.

## Git Convention

- Làm riêng → 1 commit gộp cuối mỗi phase: `feat(phaseXX): <description>`
- Không commit: `data/raw/*.csv`, `.venv/`, `__pycache__/`, `*.pkl > 50MB`

## Validation Rules (áp dụng cho mọi phase)

Một phase được coi là **PASSED** khi:
1. ✅ Tất cả checklist items trong phase file được tick
2. ✅ Evidence section điền đầy đủ (output thực tế, không phải expected)
3. ✅ Summary section viết dựa trên code đã làm (không phải plan)
4. ❌ Nếu bất kỳ item nào FAIL → phase chưa passed, không chuyển tiếp
