# Phase 04: Quy Trình Biên Dịch Kép, Kiểm Định & Đồng Bộ Bài Nộp

## 1. Context Links
- Parent Plan: [plan.md](plan.md)
- Slide Generator: [generate_cs106_style_slides_vn.js](../../draft/fraud-detection/slide/generate_cs106_style_slides_vn.js)
- Report Compiler: [build_report.py](../../draft/fraud-detection/build_report.py)
- Submission Package: [submit/CS106_F31_CN2 - Nhom 9/](../../submit/CS106_F31_CN2%20-%20Nhom%209)

---

## 2. Overview
- **Ngày lập**: 2026-09-26
- **Mục tiêu**: Thực thi quy trình biên dịch tự động hóa hai chiều (2-way compilation) cho cả Slide và Báo cáo, đảm bảo 100% số trang mục lục khớp với thực tế, xuất PDF chuẩn in ấn học thuật UIT và đồng bộ trọn vẹn vào gói nộp bài chính thức.
- **Thời lượng dự kiến**: ~45 phút.
- **Mức độ ưu tiên**: P1.
- **Trạng thái**: Completed.

---

## 3. Kiến Trúc Quy Trình Biên Dịch & Kiểm Định (Dual-Track Pipeline)

```text
TRACK 1: BIÊN DỊCH SLIDE
generate_cs106_style_slides_vn.js ──► [Nhom9]_Slide.pptx ──► Word/AppleScript Export ──► [Nhom9]_Slide.pdf (21 trang tại draft/)

TRACK 2: BIÊN DỊCH BÁO CÁO (2-WAY TOC SYNC WITH BUGFIX)
report-source.md ──► DOCX Lượt 1 ──► PDF Lượt 1 ──► sync_toc.py (Khử dot-leader Mục lục) ──► _toc_pages.json ──► DOCX Lượt 2 ──► PDF Lượt 2 Chuẩn (37 trang)

TRACK 3: LƯU TRỮ VÀ BÀN GIAO BẢN THẢO
Bản xuất sắc nhất ──► draft/fraud-detection/reports/ & slide/ (submit do sinh viên tự quản lý đồng bộ)
```

---

## 4. Implementation Steps

### Bước 1: Biên dịch & Kiểm định Slide PDF
1. Chạy lệnh: `cd assignments/Final/draft/fraud-detection/slide && node generate_cs106_style_slides_vn.js`.
2. Kiểm tra output console báo tạo thành công file PPTX.
3. Xuất bản PDF bằng lệnh AppleScript qua Microsoft Word hoặc công cụ chuyển đổi chuyên dụng.
4. Kiểm định số trang qua PyMuPDF: Đúng chuẩn **21 trang**.

### Bước 2: Biên dịch & Đồng bộ Mục lục Báo cáo 2 Chiều
1. Sửa lỗi `sync_toc.py`: Tinh chỉnh cơ chế nhận diện trang bắt đầu phần thân bằng regex loại bỏ các trang có dot-leader `....` của Mục lục 2 trang, đảm bảo không nhận nhầm `7.1. Tóm tắt`.
2. Chạy lệnh: `cd assignments/Final/draft/fraud-detection && python3 build_report.py`.
3. Theo dõi log tự động hóa:
   - Nạp template `_report_template.docx`.
   - Dựng DOCX lượt 1.
   - Xuất PDF lượt 1 để đo đạc vị trí thực tế của từng heading.
   - PyMuPDF quét số trang chính xác từng chương/mục và cập nhật vào `_toc_pages.json`.
   - Tái biên dịch DOCX lượt 2 với số trang hiển thị khớp 100% và tạo liên kết tương tác (clickable bookmarks).
   - Xuất bản PDF chính thức cuối cùng.

### Bước 3: Kiểm toán Chất lượng Học thuật (Visual & Academic QA)
- Kiểm tra trang bìa chuẩn Phụ lục 1: Khung viền triple border, logo UIT, thông tin 7 thành viên, GVHD PGS.TS. Nguyễn Đình Hiển.
- Kiểm tra bảng biểu: Không bị cắt ngang dòng giữa trang, font chữ và màu sắc đồng nhất.
- Kiểm tra biểu đồ: Hình 5.1 (ROC Curves), Hình 5.2 (PR Curves), Hình 5.3 (Confusion Matrix), Hình 5.4 (Feature Importance), Hình 5.5 (Ablation Comparison) sắc nét, không bị vỡ hạt.
- Kiểm tra tài liệu tham khảo: Chuẩn IEEE [1]-[8], có liên kết nhảy trực tiếp.

### Bước 4: Lưu Trữ Bản Thảo Hoàn Thiện
- Xuất bản phẩm hoàn thiện tại:
  - `assignments/Final/draft/fraud-detection/reports/[Nhom9]_Report_FraudDetection.docx` (và `.pdf` 37 trang)
  - `assignments/Final/draft/fraud-detection/slide/[Nhom9]_Slide_FraudDetection.pdf` (21 trang)
- Lưu ý: Thư mục `submit/` do người dùng trực tiếp kiểm tra và sao chép theo nguyên tắc bảo vệ bài nộp.

---

## 5. Todo List
- [x] Chạy pipeline biên dịch Slide và xuất PDF (`[Nhom9]_Slide_FraudDetection.pdf` 21 trang trong `draft/`).
- [x] Sửa bug nhận diện trang bắt đầu phần thân trong `sync_toc.py` (loại bỏ nhận nhầm dot-leader của Mục lục 2 trang).
- [x] Chạy `build_report.py` để biên dịch Báo cáo với đồng bộ số trang PyMuPDF 2 chiều đạt 0 mismatches.
- [x] Kiểm tra số trang thực tế của Slide (21 trang) và Báo cáo (37 trang).
- [x] Kiểm tra tính toàn vẹn của file `_toc_pages.json` (69 mục khớp tuyệt đối 100%).
- [x] Xuất bản phẩm hoàn thiện tại `draft/fraud-detection/reports/[Nhom9]_Report_FraudDetection.docx` và PDF.

---

## 6. Success Criteria & Evidence
- Cả hai file báo cáo và slide hoàn thiện đều có timestamp mới nhất trong thư mục `draft/`.
- Báo cáo PDF có mục lục khớp số trang 100% (0 mismatches được xác thực bằng script PyMuPDF).
- File Word DOCX có đầy đủ mục lục tương tác, bảng biểu và biểu đồ thực nghiệm sắc nét.

---

## 7. Risk Assessment & Mitigations
- **Rủi ro**: Lỗi kết nối AppleScript khi Microsoft Word xuất PDF tự động trên macOS.
  - *Biện pháp*: Script `export_docx_to_pdf` đã tích hợp sẵn cơ chế fallback qua headless LibreOffice nếu AppleScript gặp sự cố.
- **Rủi ro**: Thêm tiểu mục Mục 5.7 làm đẩy các trang phía sau nhảy trang.
  - *Biện pháp*: Quy trình 2 lượt (2-pass) của `build_report.py` tự động đo lại toàn bộ sau khi đã chèn nội dung, triệt tiêu hoàn toàn rủi ro lệch trang.

---

## 8. Next Steps
Hoàn tất kế hoạch, tổng kết báo cáo và trình modal `ask_question` để người dùng phê duyệt trước khi kích hoạt quy trình thực thi.
