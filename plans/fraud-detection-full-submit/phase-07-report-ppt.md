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
| Task | Sprint | Ghi chú |
|------|--------|----------|
| Viết Introduction + Problem Statement | Sprint 2 | Không cần code |
| Viết Dataset Description (Kaggle stats) | Sprint 2 | Chỉ cần đọc README |
| Viết Methodology (thuật toán + preprocessing + imbalance) | Sprint 3 | Không cần kết quả |
| Viết Results & Discussion (điền số từ Khang) | Sprint 4 | Cần output Phase 05 |
| Viết Conclusion + References | Sprint 4 | Draft trước, hoàn thiện sau |
| Format Word + Abstract + kiểm tra citation | Sprint 4 | |

### Hôn — PPT
| Task | Sprint | Ghi chú |
|------|--------|----------|
| Thiết kế template PPT (theme, layout, màu, font) | Sprint 2 | Không cần code |
| Điền slides: Title, Team, Giới thiệu bài toán, Dataset | Sprint 2 | |
| Điền slides: Pipeline, Preprocessing, Modeling (RF/XGB/AE) | Sprint 3 | |
| Điền slides: Kết quả, ROC, Confusion Matrix (điền số từ Khang) | Sprint 4 | Cần output Phase 05 |
| Điền slide Demo (screenshot từ Trung) | Sprint 4 | Cần screenshot từ Trung |
| Hoàn thiện PPT + kiểm tra timing | Sprint 4 | |

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

- Lấy tất cả metrics từ Phase 05 evidence section (không nhớ lại, không đoán)
- Hình ảnh: copy từ `reports/figures/*.png` (đã có sẵn, độ phân giải 150 DPI)
- Abstract: viết sau cùng khi có kết quả đầy đủ

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
