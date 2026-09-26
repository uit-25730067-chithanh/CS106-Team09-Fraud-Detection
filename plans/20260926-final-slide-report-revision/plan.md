---
title: "Kế Hoạch Nâng Cấp Toàn Diện Báo Cáo & Slide Đồ Án Cuối Kỳ CS106 (Nhóm 09)"
description: "Kế hoạch phản biện chuyên sâu (--hard) tinh chỉnh Slide và Báo cáo theo gu phản biện của PGS.TS. Nguyễn Đình Hiển."
status: completed
priority: P1
effort: 4.5h
branch: main
tags: [cs106, fraud-detection, report-revision, slide-revision, paysim, academic-defense]
created: 2026-09-26
---

# Kế Hoạch Nâng Cấp Toàn Diện Báo Cáo & Slide Đồ Án Cuối Kỳ CS106

Kế hoạch tối ưu hóa và hoàn thiện bài nộp chính thức của Nhóm 09 môn CS106 (Trí tuệ Nhân tạo), giải quyết triệt để các lỗ hổng học thuật được phát hiện qua buổi báo cáo đợt 1 của PGS.TS. Nguyễn Đình Hiển.

## 🧭 Lộ Trình Triển Khai (Phân Tách Độc Lập Slide & Report)

| Phase | Trọng Tâm Nhiệm Vụ | Mục Tiêu & Sản Phẩm Đầu Ra | Trạng Thái |
|:---:|---|---|:---:|
| **[Phase 01](phase-01-empirical-ablation-experiment.md)** | **Thực Nghiệm Bổ Sung (Ablation Study)** | Chạy script đối chứng loại bỏ biến số dư & prune biến 0% gain; xuất `reports/ablation_study_results.csv` | `Completed` |
| **[Phase 02](phase-02-slide-academic-refinement.md)** | **Plan Tinh Chỉnh Slide (`.pptx` / `.pdf`)** | Cập nhật `generate_cs106_style_slides_vn.js`: 14 thuộc tính miền cốt lõi Slide 8, phòng thủ Temporal Split Slide 11, quy chiếu tỷ lệ gốc Slide 15, biên dịch PDF | `Completed` |
| **[Phase 03](phase-03-report-comprehensive-revision.md)** | **Plan Hoàn Thiện Báo Cáo (`.md` / `.docx` / `.pdf`)** | Cập nhật `report-source.md` 6 chương: Chuẩn hóa thuộc tính miền kế toán kép, tích hợp kết quả Ablation thực tế, biện luận Autoencoder Zero-Day | `Completed` |
| **[Phase 04](phase-04-dual-compilation-verification.md)** | **Kiểm Định Kép & Đồng Bộ Bài Nộp** | Biên dịch Word/PDF chuẩn học thuật UIT (2-way PyMuPDF TOC sync 0 mismatches), kiểm thử trực quan Slide/Report | `Completed` |

## 🔗 Tài Liệu Tham Chiếu & Căn Cứ Học Thuật
- Báo cáo tổng hợp triết lý chấm điểm của thầy Hiển: [teacher-critique-synthesis.md](research/teacher-critique-synthesis.md)
- Báo cáo nguồn hiện tại: [report-source.md](../../draft/fraud-detection/reports/report-source.md)
- Script sinh slide hiện tại: [generate_cs106_style_slides_vn.js](../../draft/fraud-detection/slide/generate_cs106_style_slides_vn.js)
