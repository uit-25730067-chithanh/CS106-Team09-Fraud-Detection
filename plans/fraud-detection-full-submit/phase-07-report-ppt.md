# Phase 07 — Báo cáo Word + PPT

**Parent plan:** [plan.md](./plan.md)  
**Depends on:** [Phase 05](./phase-05-evaluation-comparison.md) — PASSED *(chỉ phần Results & Discussion + điền số vào PPT — Sprint 4)*  
**Early Start:** ~70% Word + PPT skeleton có thể viết từ **Sprint 2** — không cần kết quả  
**Parallel with:** [Phase 06](./phase-06-demo-ui.md)  
**Next phase:** [Phase 08 — Submit Package](./phase-08-submit-package.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Duy** (Word) + **Hôn** (PPT) |
| Priority | P0 — Required for submission |
| Status | `pending` |
| Review | ⬜ Not reviewed |
| Estimated effort | 4–6 giờ tổng (2 người) |
| Sprint | Sprint 2–3 (phần không cần kết quả), Sprint 4 (Results & Hoàn thiện) |

## ⚡ Early Start Tasks — Duy + Hôn bắt đầu từ Sprint 2

> **Duy:** ~70% báo cáo không cần số kết quả. Viết ngay từ Sprint 2, điền Results sau Sprint 4.
> **Hôn:** Template + slides non-technical bắt đầu ngay từ Sprint 2. Điền số sau Sprint 4.

### Duy — Báo cáo Word
| Task | Sprint | Ghi chú | Trạng thái |
|------|--------|---------|------------|
| Viết Introduction + Problem Statement | Sprint 2 | Không cần code | ✅ Hoàn thành |
| Viết Dataset Description (Kaggle stats) | Sprint 2 | Dùng đề bài, Kaggle, PaySim paper và evidence Phase 01 | ✅ Hoàn thành |
| Viết Methodology (thuật toán + preprocessing + imbalance) | Sprint 3 | Không cần kết quả | 🔲 Chưa bắt đầu |
| Viết Results & Discussion (điền số từ Khang) | Sprint 4 | Cần output Phase 05 | 🔲 Chưa bắt đầu |
| Viết Conclusion + References | Sprint 4 | Draft trước, hoàn thiện sau | 🔲 Chưa bắt đầu |
| Format Word + Abstract + kiểm tra citation | Sprint 4 | | 🔲 Chưa bắt đầu |

#### Evidence Early Start — Duy, Sprint 2 (29/08/2026)

- Branch riêng: `docs/vu-van-duy-sprint2-report`.
- Source có thể review bằng Git: `draft/fraud-detection/reports/report-source.md`.
- Word draft: `draft/fraud-detection/reports/[Nhom9]_BaoCao_FraudDetection_Sprint2_Duy.docx`.
- Phạm vi đã viết: Chương 1 — Giới thiệu; Chương 2 — Phát biểu bài toán; Chương 3 — Mô tả dữ liệu.
- Evidence sử dụng: đề bài CS106, notebook EDA, Phase 01, PaySim paper và Kaggle data card.
- Kiểm tra thực tế: citation validator PASS; DOCX package validation PASS; 131 paragraphs, 5 tables, đủ heading Chương 1–3.
- Giới hạn xác minh: chưa render PDF vì máy không có LibreOffice/Pages; cần mở Word và cập nhật trường mục lục khi review thủ công.
- Phase 07 tổng thể vẫn `pending`; Methodology, Results, Discussion, Conclusion và Abstract chờ Sprint 3–4.

### Hôn — PPT
| Task | Sprint | Ghi chú | Trạng thái |
|------|--------|----------|------------|
| Thiết kế template PPT (theme, layout, màu, font) | Sprint 2 | Chuẩn phong cách UIT & Financial AI | ✅ Hoàn thành |
| Điền slides: Title, Team, Giới thiệu bài toán, Dataset, EDA (Slides 1–5) | Sprint 2 | Khớp dữ liệu PaySim và EDA | ✅ Hoàn thành |
| Điền slides: Pipeline, Preprocessing 14 features, Imbalance & Models (Slides 6–9) | Sprint 2–3 | Sơ đồ data flow chống leakage, 14 features, RF/XGB/AE | ✅ Hoàn thành |
| Điền slides: Kết quả, ROC, Confusion Matrix (Slides 10–12) | Sprint 3 | Số liệu thực nghiệm RF, XGBoost, Autoencoder | ✅ Hoàn thành |
| Điền slide Demo & Tổng kết (Slides 13–15) | Sprint 3 | Demo Streamlit, Hướng phát triển, Q&A | ✅ Hoàn thành |
| Hoàn thiện PPT + kiểm tra timing (15 slides) | Sprint 3 | Khớp 100% metrics thực tế | ✅ Hoàn thành |

#### Evidence Hoàn thiện Slides — Hôn (01/09/2026)

- Google Slides thiết kế gốc: [Google Slides Link](https://docs.google.com/presentation/d/1GEibG9p26vu57G15NdChx8SQrG0zTD50LZBwpIXPU58/edit?usp=sharing).
- File artifacts lưu trữ tại repo:
  - `draft/fraud-detection/reports/[Nhom9]_Slide_FraudDetection_Hon.pptx` (1.41 MB)
  - `draft/fraud-detection/reports/[Nhom9]_Slide_FraudDetection_Hon.pdf` (4.91 MB)
- Số lượng slide: **15 slides** hoàn chỉnh (Bìa, Mục lục, Đặt vấn đề & Thách thức, Dữ liệu PaySim, EDA Discoveries, Kiến trúc Pipeline, Tiền xử lý 14 features, Xử lý mất cân bằng, 3 Mô hình RF/XGB/AE, Tiêu chí đánh giá, Bảng so sánh đa tiêu chí, Ma trận nhầm lẫn & Feature Importance, Live Demo Streamlit, Tổng kết & Hướng phát triển, Q&A & Cảm ơn).
- Nội dung xác minh: Đầy đủ 15 slides, tích hợp 100% metrics thực tế từ Phase 03–04, hình ảnh trực quan và phân tích nghiệp vụ sâu sắc.
- Tài liệu bổ trợ (PR #13): Đã tích hợp bộ slide học thuật 24 trang song ngữ EN-VN (`draft/fraud-detection/slide/`) kèm bộ biểu đồ 300 DPI phục vụ làm tài liệu tham khảo và backup Q&A.

## Context

Duy viết báo cáo Word theo chuẩn Scientific Report. Hôn làm PPT cho buổi báo cáo. Cả 2 dùng kết quả từ Phase 05 (metrics, figures, comparison table).

## Requirements

**Word (Duy):**
- Scientific Report format (theo yêu cầu đề)
- Minimum sections: Abstract, Introduction, Dataset, Method, Results, Conclusion, References
- Chèn figures từ `reports/figures/`
- Chèn bảng so sánh từ `reports/model_comparison.csv`

**PPT (Hôn):**
- ~10–15 slides
- Slide kết quả phải có bảng so sánh và ít nhất 1 chart
- Thời lượng trình bày ước tính 10–15 phút

## Key Insights

- Hình ảnh: copy từ `reports/figures/*.png` (đã có sẵn, độ phân giải 150 DPI)
- Abstract: viết sau cùng khi có kết quả đầy đủ

## 💡 Ý tưởng Đề xuất & Cải tiến Nâng cao (từ MY_IDEAS)

1. **Điểm nhấn mở đầu: Sự thất bại của Rule cổ điển (`isFlaggedFraud`):**
   * Đưa số liệu thực chứng lên Slide 2 và Chương 1: Cờ cố định của ngân hàng cũ (chỉ flag khi `TRANSFER > 200,000`) chỉ bắt được **16 / 8,213 vụ** ($\approx \mathbf{0.19\%}$).
   * *Mục tiêu:* Tạo lập luận đanh thép và thuyết phục về lý do ngân hàng bắt buộc phải chuyển dịch sang AI/Machine Learning.
2. **Phản biện học thuật sâu sắc (Threats to Validity — Đã có trong Chương 3.6):**
   * **Prevalence Shift:** Tỷ lệ gian lận trong tập test sau downsample là $4.1\%$ (so với $0.13\%$ thực tế), do đó Precision đo được sẽ cao hơn môi trường thực $\rightarrow$ giải thích cách hiệu chỉnh ngưỡng xác suất khi triển khai thực tế.
   * **Simulator Artifacts:** Dữ liệu PaySim là dữ liệu mô phỏng, cần thảo luận việc các biến `errorBalance` có thể phản ánh cơ chế cập nhật của phần mềm giả lập bên cạnh hành vi con người.
   * **Temporal Leakage vs Random Split:** Thảo luận về sự khác biệt giữa Stratified Random Split và Time-based Split theo chuỗi thời gian `step`.
3. **Cấu trúc Slide thuyết trình 12 trang đạt chuẩn Rubric tối đa:**
   * Phân bổ thời lượng 10–15 phút chuẩn chỉ: 4 Slide đầu đặt vấn đề & Data $\rightarrow$ 3 Slide Pipeline & Modeling $\rightarrow$ 3 Slide Kết quả & Demo $\rightarrow$ 2 Slide Phản biện học thuật & Q&A.

## Related Files

```
draft/fraud-detection/
└── reports/
    ├── [Nhom9]_BaoCao_FraudDetection.docx    ← OUTPUT (Duy)
    ├── [Nhom9]_PPT_FraudDetection.pptx        ← OUTPUT (Hôn)
    ├── model_comparison.csv                   ← Input từ Phase 05
    └── figures/                               ← Input từ Phase 05
        ├── roc_curves_all.png
        ├── pr_curves_all.png
        ├── confusion_matrix_*.png
        └── ...
```

## Implementation Steps

### Báo cáo Word (Duy)

**Outline chuẩn Scientific Report:**

```
Title: Hệ thống Phát hiện Giao dịch Tài chính Bất thường
       và Nghi vấn Gian lận (Đề tài 7)
       
Group: Nhóm 9 — CS106, UIT

─────────────────────────────────────
1. TÓM TẮT (Abstract)                     [~150 words, viết sau cùng]
─────────────────────────────────────
2. GIỚI THIỆU (Introduction)
   2.1. Bối cảnh và tầm quan trọng
   2.2. Vấn đề nghiên cứu
   2.3. Mục tiêu đề tài
   2.4. Phạm vi nghiên cứu

3. DỮ LIỆU (Dataset)
   3.1. Mô tả dataset (Kaggle PaySim Mobile Money)
   3.2. Thống kê mô tả (shape, features, missing values, downsampling)
   3.3. Phân tích mất cân bằng (chart từ EDA)
   
4. PHƯƠNG PHÁP (Methodology)
   4.1. Tiền xử lý dữ liệu
        - Feature scaling (StandardScaler) & Encoding (One-Hot Encoding)
        - Stratified Downsampling và lọc giao dịch
        - Train/Test split (stratified 80/20)
   4.2. Xử lý mất cân bằng
        - SMOTE
        - ADASYN
        - So sánh trước/sau
   4.3. Mô hình học máy
        4.3.1. Random Forest
        4.3.2. XGBoost
        4.3.3. Autoencoder (Anomaly Detection)
   4.4. Metrics đánh giá
        - Lý do không dùng Accuracy
        - Precision, Recall, F1-Score, ROC-AUC

5. KẾT QUẢ (Results)
   5.1. Bảng so sánh hiệu năng (model_comparison.csv)
   5.2. ROC Curves (roc_curves_all.png)
   5.3. Precision-Recall Curves (pr_curves_all.png)
   5.4. Confusion Matrices
   5.5. Feature Importance (RF và XGBoost)

6. THẢO LUẬN (Discussion)
   6.1. Phân tích kết quả
   6.2. So sánh SMOTE vs ADASYN
   6.3. Hạn chế của nghiên cứu

7. KẾT LUẬN (Conclusion)
   7.1. Kết luận chính
   7.2. Đề xuất hướng phát triển

8. TÀI LIỆU THAM KHẢO (References)
   - Kaggle dataset citation
   - scikit-learn, xgboost, keras papers/docs
   - SMOTE original paper (Chawla et al. 2002)
   - ADASYN paper (He et al. 2008)
```

**Lưu ý format:**
- Font: Times New Roman 12pt (body), 14pt (headings)
- Page margins: 2.5cm all sides
- Line spacing: 1.5
- Figures: caption bên dưới, "Hình X: ..."
- Tables: caption bên trên, "Bảng X: ..."

### PPT Slides (Hôn)

```
Slide 1: Title Slide
  - Tên đề tài, môn học, nhóm, thành viên

Slide 2: Giới thiệu bài toán
  - Fraud detection là gì?
  - Thách thức chính (imbalanced data)

Slide 3: Dataset
  - Stats: ~200,000 transactions (downsampled), ~4.1% fraud
  - Chart: Class distribution (isFraud)

Slide 4: Pipeline Overview
  - Flow chart: Data → Preprocessing → Models → Evaluation

Slide 5: Tiền xử lý & Xử lý imbalance
  - StandardScaler cho balances/amount, OHE type
  - Downsampling & Feature Engineering (errorBalance)
  - SMOTE vs ADASYN: before/after distribution

Slide 6: Mô hình Random Forest
  - Architecture, best params, training time

Slide 7: Mô hình XGBoost
  - Architecture, best params, so sánh nhanh với RF

Slide 8: Mô hình Autoencoder
  - Architecture diagram
  - Reconstruction error approach

Slide 9: Kết quả tổng hợp
  - Bảng so sánh (dạng table đẹp)
  - Highlight best model

Slide 10: ROC Curves & Confusion Matrices
  - roc_curves_all.png
  - Best model confusion matrix

Slide 11: Demo
  - Screenshot từ Streamlit app

Slide 12: Kết luận & Đề xuất
  - Best model recommendation
  - Hạn chế + hướng phát triển

Slide 13: Q&A + Cảm ơn
```

## Checklist

**Word (Duy):**
- [ ] File Word được lưu: `reports/[Nhom9]_BaoCao_FraudDetection.docx`
- [ ] Có đủ 8 sections chính (TT → GTTK → ... → TLTK)
- [ ] Bảng so sánh models được chèn (từ Phase 05)
- [ ] Ít nhất 3 figures được chèn (ROC curves, confusion matrix, ...)
- [ ] Tài liệu tham khảo có ≥ 5 nguồn
- [ ] Abstract viết sau khi có kết quả (không phải plan)
- [ ] Đọc lại pass 1 lần trước khi commit

**PPT (Hôn):**
- [ ] File PPT được lưu: `reports/[Nhom9]_PPT_FraudDetection.pptx`
- [ ] Có đủ 12–15 slides
- [ ] Slide kết quả có bảng so sánh models
- [ ] Slide kết quả có ít nhất 1 chart (ROC hoặc confusion matrix)
- [ ] Slide demo có screenshot từ app
- [ ] Font size body ≥ 18pt (readable từ xa)
- [ ] Consistent design theme (không dùng quá nhiều màu)

## Success Criteria

| Criterion | Expected | Evidence |
|-----------|---------|---------|
| Word file exists | .docx saved | ___________ |
| PPT file exists | .pptx saved | ___________ |
| Word has sections | 8 sections | ___________ |
| PPT slide count | 12–15 slides | ___________ |
| Metrics in Word | correct values from Phase 05 | ___________ |

## Evidence Section *(điền sau khi làm)*

```
Word file: reports/[Nhom9]_BaoCao_FraudDetection.docx
  - Pages: ____
  - Figures inserted: ____ figures
  - Tables: ____ tables
  
PPT file: reports/[Nhom9]_PPT_FraudDetection.pptx
  - Slides: ____
  - Estimated time: ____ phút
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Metrics in report ≠ actual results | Medium | High | Copy directly from Phase 05 evidence section |
| Figures not displaying in Word | Low | Low | Insert as PNG, not linked |
| PPT too long/short | Low | Medium | Practice timing — target 10–15 min |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa hoàn thành

```
Hoàn thành: __/__/2026
Duy: Word ____pages, ____figures
Hôn: PPT ____slides, ____min estimated
Kết quả best model ghi trong báo cáo: ____________________
```

## Commit

```bash
git add reports/
git commit -m "feat(phase07): scientific report (Word) + presentation slides (PPT)"
```
