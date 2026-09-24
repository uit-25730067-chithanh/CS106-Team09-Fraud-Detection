---
title: "CS106 Final — Fraud Detection Full Implementation to Submit"
description: "End-to-end implementation plan: từ code rỗng đến bản nộp hoàn chỉnh, chia theo phase độc lập có validation gate"
status: completed
priority: P1
effort: ~40h (7 người)
branch: main
tags: [cs106, fraud-detection, academic, python, ml, submit]
created: 2026-08-24
updated: 2026-09-20
sprints: 4 sprints | Sprint review mỗi tối Thứ 6 | Bắt đầu 25/8 | Deadline 18/9

---

# Plan: CS106 Final — Fraud Detection Full Submit

## Mục tiêu

Từ skeleton ban đầu (docs + structure, không có code) → bản nộp hoàn chỉnh:
`CS106_F31_CN2 - Nhom 9.zip` với đủ: code, notebooks, báo cáo Word, PPT, demo.

## Sprint Timeline

| Sprint | Thời gian | Mục tiêu chính | Sprint Review |
|--------|----------|---------------|---------------|
| **Sprint 1** | 25/8 – 28/8 | Setup repo + Scaffold, phân chia công việc | Tối Thứ 6 28/8 |
| **Sprint 2** | 28/8 – 4/9 | Tải dữ liệu, EDA, Preprocessing, Phân tích imbalance. Mã nguồn đánh giá mẫu & UI shell | Tối Thứ 6 4/9 |
| **Sprint 3** | 4/9 – 11/9 | Xử lý imbalance (SMOTE/ADASYN), Modeling (RF, XGBoost, Autoencoder). Viết Methodology, hoàn thành 6/6 notebooks & Evaluation | Tối Thứ 6 11/9 |
| **Sprint 4** | 11/9 – 18/9 | Demo UI screenshots & clip, hoàn thiện báo cáo Word/PPT, diễn tập thuyết trình, đóng gói nộp bài | Deadline 18/9 |

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
| 05 | [Evaluation & Comparison](./phase-05-evaluation-comparison.md) | Khang | Sprint 2–4* | `passed` ✅ | 4/4 scripts done; notebook 06 chạy Restart&Run All sạch; `model_comparison.csv` + 7 figures xuất xong, khớp ch5_metrics_recomputed.csv |
| 06 | [Demo UI](./phase-06-demo-ui.md) | Trung | Sprint 2–4* | `passed` ✅ | Streamlit Web UI, quy trình 4 bước, import CSV/JSON, inference XGBoost, 3 themes, comparison/9 figures, 5 screenshots chuẩn hóa & kịch bản demo |
| 07 | [Report & PPT](./phase-07-report-ppt.md) | Duy + Hôn | Sprint 2–4* | `passed` ✅ | Word/PDF Tóm tắt + Chương 1–7 ✅ 32 trang (Duy), khớp 100% Phase 05; PPT 21 slides học thuật & Kịch bản toàn team đã duyệt chính thức |
| 08 | [Submit Package](./phase-08-submit-package.md) | Hôn | Sprint 4 | `passed` ✅ | Chuẩn bị gói nộp bài CS106_F31_CN2 - Nhom 9 (47 deliverables sạch, an toàn Git) |

> \* Phase 05–07 có **Early Start Tasks** bắt đầu từ Sprint 2. Xem chi tiết trong từng file.
>
> **Phase 06 — Trung — hoàn tất 19/09/2026:** Hoàn tất toàn bộ giao diện Streamlit UI tương tác, quy trình phân tích 4 bước, hộp chọn và nhập mẫu CSV/JSON, XGBoost-SMOTE inference, mapping datetime PaySim, định dạng tiền VNĐ, comparison CSV + 9 figures, 3 themes; 5 screenshots chuẩn hóa, video demo clip ngoại tuyến tại Google Drive; toàn bộ tests pass. Phase 06 chính thức PASSED.
>
> **Phase 07 — Duy & Hôn — hoàn tất 15/09/2026:** Báo cáo Word & PDF 32 trang chuẩn cấu trúc UIT khớp 100% số liệu thực nghiệm Phase 05; bộ Slide học thuật 21 trang và kịch bản thuyết trình toàn team 7 người đã duyệt chính thức.
>
> **Phase 08 — Hôn & Team — hoàn tất 20/09/2026:** Hoàn tất đóng gói toàn diện theo đúng chuẩn UIT: tạo `Danh_sach_nhom.xlsx` (7 thành viên), trích xuất 5 screenshots từ video demo, viết `HUONG_DAN_SU_DUNG.docx`, chuẩn bị cấu trúc `submit/CS106_F31_CN2 - Nhom 9/` (47 deliverables sạch) an toàn đưa lên Git repo.
>
> **PM Audit & Final Verdict — Hôn — 20/09/2026:** Toàn bộ 9/9 phases (100%) đã chính thức **PASSED**. Đầy đủ 6/6 notebooks chạy sạch 100%, 116 tests pass. Nhóm 9 đã hoàn thành xuất sắc toàn bộ yêu cầu đồ án môn học trước hạn chót.


## Git Convention

- Làm riêng → 1 commit gộp cuối mỗi phase: `feat(phaseXX): <description>`
- Không commit: `data/raw/*.csv`, `.venv/`, `__pycache__/`, `*.pkl > 50MB`

## Validation Rules (áp dụng cho mọi phase)

Một phase được coi là **PASSED** khi:
1. ✅ Tất cả checklist items trong phase file được tick
2. ✅ Evidence section điền đầy đủ (output thực tế, không phải expected)
3. ✅ Summary section viết dựa trên code đã làm (không phải plan)
4. ❌ Nếu bất kỳ item nào FAIL → phase chưa passed, không chuyển tiếp
