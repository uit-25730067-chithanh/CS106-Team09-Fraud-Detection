# Phase 03: Kế Hoạch Hoàn Thiện Toàn Diện Báo Cáo Học Thuật UIT (`.md` / `.docx` / `.pdf`)

## 1. Context Links
- Parent Plan: [plan.md](plan.md)
- Markdown Source File: [report-source.md](../../draft/fraud-detection/reports/report-source.md)
- Report Metadata Config: [report-meta.yaml](../../draft/fraud-detection/reports/report-meta.yaml)
- Build & Verification Script: [build_report.py](../../draft/fraud-detection/build_report.py)
- Reporting Modules:
  - Cover Page: [cover_page_builder.py](../../draft/fraud-detection/src/reporting/cover_page_builder.py)
  - TOC Generator: [toc_generator.py](../../draft/fraud-detection/src/reporting/toc_generator.py)
  - Inline Parser: [inline_parser.py](../../draft/fraud-detection/src/reporting/inline_parser.py)
  - Hyperlink Helpers: [hyperlink_helpers.py](../../draft/fraud-detection/src/reporting/hyperlink_helpers.py)
- Research Synthesis: [teacher-critique-synthesis.md](research/teacher-critique-synthesis.md)

---

## 2. Overview & Decisions Log
- **Ngày cập nhật**: 2026-09-26
- **Mục tiêu**: Tái cấu trúc và nâng cấp toàn diện bản thảo báo cáo khoa học `report-source.md` và pipeline biên dịch OpenXML theo đúng chuẩn học thuật UIT (Phụ lục 1, Phụ lục 2, Nghị định 30/2020/NĐ-CP). Khắc phục triệt để các lỗi kỹ thuật và thiếu sót chuẩn mực được phát hiện qua đợt tổng duyệt phản biện (--hard).
- **Quyết định đã thống nhất với Trưởng nhóm (2026-09-26)**:
  1. **Định dạng trích dẫn nội dòng**: Chuyển hẳn sang dạng **số mũ Superscript `[1]`** (font ~9.5pt, không in đậm, màu đen, tích hợp thẻ OpenXML `<w:vertAlign w:val="superscript"/>`, liên kết tương tác nhảy tới anchor tài liệu).
  2. **Mã lớp học phần chính thức**: `CS106.F31.CN2.TTNT`.
  3. **Phương án thực hiện**: Phê duyệt **Phương án 1** (Tái cấu trúc toàn diện từ mã nguồn sinh OpenXML, văn bản Markdown nguồn đến quy trình biên dịch kép và kiểm định link thực tế).
- **Thời lượng dự kiến**: ~90 phút.
- **Mức độ ưu tiên**: P1.
- **Trạng thái**: `Completed` (Đã hoàn tất toàn bộ 7 hạng mục nâng cấp).

---

## 3. Danh Mục Các Hạng Mục Nâng Cấp Chi Tiết (Work Breakdown Structure)

```text
HẠNG MỤC                      TRỌNG TÂM KỸ THUẬT VÀ NỘI DUNG NÂNG CẤP
────────                      ───────────────────────────────────────
1. Metadata & Bìa UIT         ──► Cập nhật lớp `CS106.F31.CN2.TTNT`, chia bảng 2 cột GVHD (35%) vs SVTH (65%), viền nhã nhặn.
2. Sửa Tab Stop Mục lục       ──► Xóa phép trừ `indent_cm`, cố định tab stop tại 15.8cm cho cả 3 cấp; sửa regex bắt trọn H3.
3. Trích Dẫn & Sửa Link 404   ──► Cắt tỉa dấu chấm kết câu khỏi URL/DOI; chuyển trích dẫn sang số mũ Superscript `[n]`.
4. Cấu Trúc Học Thuật Chuẩn   ──► Bổ sung Cam kết liêm chính, Bảng phân công nhóm, Abstract tiếng Anh, Từ viết tắt.
5. Cải Tổ Danh Mục TLTK       ──► Bỏ code nội bộ khỏi References; thêm 4 bài báo Việt Nam uy tín (Ngân hàng, Tree-based, NHNN).
6. Bổ Sung Phụ Lục (Appendix) ──► Phụ lục A (Mã nguồn & Notebooks); Phụ lục B (Môi trường); Phụ lục C (Ảnh Demo Streamlit).
7. Tái Biên Dịch & Kiểm Định  ──► Chạy build_report.py 2 chiều; quét PyMuPDF đo độ lệch tab = 0 và kiểm tra HTTP 100% link sống.
```

---

### Chi Tiết Kỹ Thuật Từng Hạng Mục:

### Hạng Mục 1: Tái Cấu Trúc Trang Bìa Chuẩn UIT (Phụ Lục 1)
- **Tệp can thiệp**: `report-meta.yaml`, `src/reporting/cover_page_builder.py`.
- **Nội dung thực hiện**:
  1. Cập nhật `course_code` và bổ sung thông tin lớp học phần `class_id: "CS106.F31.CN2.TTNT"`.
  2. Thay thế khối bảng 1 cột dồn cục hiện tại bằng **Bảng 2 cột cân xứng** (`cols=2`, tỷ lệ 35% - 65% trên tổng bề rộng 15.0 cm, không viền):
     - **Cột trái (35%)**:
       - `GIẢNG VIÊN HƯỚNG DẪN:` (Times New Roman 11.5pt Bold)
       - `PGS.TS. Nguyễn Đình Hiển` (Times New Roman 12pt Bold)
     - **Cột phải (65%)**:
       - `NHÓM SINH VIÊN THỰC HIỆN:` (Times New Roman 11.5pt Bold)
       - `Nhóm 9 - Lớp: CS106.F31.CN2.TTNT` (Times New Roman 11pt Bold Italic)
       - Danh sách 7 sinh viên (11pt Regular, tên Trưởng nhóm Bold) kèm đầy đủ MSSV và vai trò phân công.
  3. Căn chỉnh khoảng cách: Tăng `space_before` cho tên đề tài để cân đối không gian nửa trên và nửa dưới, xóa bỏ text `-o0o-` thô sơ hoặc thay bằng vạch kẻ phân đoạn trang nhã.

### Hạng Mục 2: Khắc Phục Lỗi Tab Stop Xộc Xệch Trong Mục Lục
- **Tệp can thiệp**: `src/reporting/toc_generator.py`.
- **Nguyên nhân cốt lõi**: Trong Word OOXML, vị trí `tab_stop` được đo từ lề trái trang giấy, việc script trừ đi `indent_cm` khiến tab stop của H1 (15.8cm), H2 (15.2cm), H3 (14.6cm) bị lệch bậc thang.
- **Nội dung thực hiện**:
  1. Sửa công thức: Đặt `tab_position_cm = CONTENT_WIDTH_CM - TOC_TAB_SAFETY_CM` (cố định `15.8 cm` cho mọi cấp tiêu đề 1, 2, 3).
  2. Đảm bảo toàn bộ ký tự dot-leader `...` và số trang dóng thẳng hàng tăm tắp ở mép phải.
  3. Sửa hàm `collect_toc_entries`: Nới rộng regex nhận diện H3 để bắt toàn bộ các tiểu mục có trong báo cáo, đảm bảo có bookmark anchor tương ứng để click nhảy chính xác.

### Hạng Mục 3: Chuẩn Hóa Trích Dẫn Nội Dòng Số Mũ & Khắc Phục Lỗi Link 404
- **Tệp can thiệp**: `src/reporting/inline_parser.py`, `src/reporting/hyperlink_helpers.py`.
- **Nội dung thực hiện**:
  1. **Số mũ Superscript `[n]`**:
     - Cập nhật hàm `add_internal_hyperlink`: Thêm tham số `is_superscript=True` để chèn phần tử OpenXML `<w:vertAlign w:val="superscript"/>` vào thẻ `<w:rPr>`.
     - Đặt font size của số trích dẫn về `9.5 pt`, `is_bold=False`, màu đen (`#000000`).
     - Giữ nguyên anchor trỏ tới bookmark `ref_{n}` trong danh mục tài liệu tham khảo.
  2. **Khắc phục lỗi Regex nuốt dấu chấm cuối câu**:
     - Cải tiến regex nhận diện URL/DOI: Tách riêng dấu chấm kết câu `.`, dấu phẩy `,`, dấu ngoặc đơn `)` ở cuối chuỗi URL trước khi đóng gói thẻ `<w:hyperlink>`.
     - Loại bỏ triệt để tình trạng link sinh ra có dạng `https://doi.org/...007.` gây lỗi `404 Not Found`.

### Hạng Mục 4: Bổ Sung Các Thành Phần Chuẩn Mực Báo Cáo Học Thuật UIT
- **Tệp can thiệp**: `reports/report-source.md`.
- **Nội dung thực hiện**:
  1. **Lời cảm ơn (Acknowledgements)**: Bày tỏ sự tri ân chân thành đến PGS.TS. Nguyễn Đình Hiển, Bộ môn Khoa học Máy tính và Trường ĐH Công nghệ Thông tin.
  2. **Cam kết liêm chính học thuật (Academic Integrity Pledge)**: Bản tuyên thệ chính thức cam đoan không đạo văn, trung thực trong nghiên cứu và thực nghiệm theo quy chế của UIT.
  3. **Bảng phân công nhiệm vụ và tỷ lệ đóng góp**: Bảng phân định rõ ràng trách nhiệm của cả 7 thành viên (Họ tên, MSSV, Nhiệm vụ chính, Tỷ lệ đóng góp % đạt 100%, Ký tên xác nhận).
  4. **Tóm tắt song ngữ (Bilingual Abstract)**: Bổ sung phần `ABSTRACT` tiếng Anh chuẩn thuật ngữ quốc tế (Machine Learning, PaySim, Ablation Study, Imbalanced Data, Double-entry Bookkeeping rules).
  5. **Danh mục từ viết tắt (List of Abbreviations)**: Bảng tra cứu toàn bộ thuật ngữ xuất hiện dày đặc trong bài: EDA, SMOTE, ADASYN, RF, XGB, AE, ROC-AUC, PR-AUC, TP, FP, TN, FN, FPR, TPR, F1, GNN...

### Hạng Mục 5: Cải Tổ Toàn Diện Danh Mục Tài Liệu Tham Khảo (References)
- **Tệp can thiệp**: `reports/report-source.md`.
- **Nội dung thực hiện**:
  1. **Loại bỏ hoàn toàn** mục *"Tài liệu nội bộ của dự án"* (các tệp notebook, script, README) ra khỏi Danh mục Tài liệu tham khảo.
  2. **Chuẩn hóa danh mục tài liệu quốc tế**: Kiểm tra và làm sạch toàn bộ DOI của các bài báo [1]-[8], đảm bảo liên kết sạch và truy cập tức thì.
  3. **Bổ sung 4 công trình nghiên cứu và quy định pháp lý tại Việt Nam**:
     - *Ngô Thuỳ Linh, Nguyễn Dương Hùng (2024)*, "Phát hiện gian lận thẻ tín dụng sử dụng mô hình học sâu Autoencoder kết hợp thuật toán Isolation Forest", *Tạp chí Kinh tế - Luật và Ngân hàng*.
     - *Nguyễn Thị Mai Trang và cộng sự (2024)*, "Ứng dụng các thuật toán học máy Tree-based (Random Forest, XGBoost) trong nhận diện gian lận giao dịch thanh toán điện tử", *Tạp chí Khoa học Thương mại*.
     - *Nghiên cứu ứng dụng học máy không giám sát trong giám sát giao dịch bất thường*, *Tạp chí Ngân hàng* (2021).
     - *Ngân hàng Nhà nước Việt Nam (2023)*, Quyết định số 2345/QĐ-NHNN về triển khai các giải pháp an toàn, bảo mật trong thanh toán trực tuyến và thanh toán thẻ ngân hàng.

### Hạng Mục 6: Xây Dựng Hệ Thống Phụ Lục Chuyên Sâu (Appendices)
- **Tệp can thiệp**: `reports/report-source.md`, `src/reporting/body_section_builder.py`.
- **Nội dung thực hiện**:
  1. **Phụ lục A: Cấu trúc mã nguồn và Tài nguyên thực nghiệm**: Quy hoạch lại toàn bộ các notebook (`01_eda.ipynb`, `02_imbalance_handling.ipynb`, `03_model_random_forest.ipynb`...), mã nguồn module `src/`, và các file kết quả CSV.
  2. **Phụ lục B: Cấu hình môi trường phần cứng và Thư viện thực thi**: Chi tiết thông số máy trạm huấn luyện, phiên bản Python, Scikit-learn, XGBoost, PyTorch/TensorFlow, Imbalanced-learn.
  3. **Phụ lục C: Minh họa giao diện ứng dụng Web Demo (Streamlit)**: Ảnh chụp màn hình và kịch bản kiểm thử giao diện phát hiện gian lận thời gian thực.

### Hạng Mục 7: Tái Biên Dịch & Kiểm Định Tự Động Kép
- **Tệp can thiệp**: `build_report.py`, `reports/[Nhom9]_Report_FraudDetection.docx`, `reports/[Nhom9]_Report_FraudDetection.pdf`.
- **Nội dung thực hiện**:
  1. Chạy biên dịch 2 lượt đồng bộ số trang PyMuPDF.
  2. Chạy kịch bản tự động kiểm tra:
     - Đo tọa độ số trang Mục lục: Chênh lệch x giữa các dòng phải bằng 0.
     - Quét toàn bộ URL/DOI trong PDF bằng HTTP HEAD/GET request: Tỷ lệ link sống đạt 100% (mã 200/202).
  3. Đồng bộ sản phẩm chính thức sang thư mục nộp bài `submit/report/`.

---

## 4. Implementation Steps & Verification Protocol

1. **Step 1: Cập nhật mã nguồn sinh OpenXML**:
   - Chỉnh sửa `hyperlink_helpers.py` và `inline_parser.py` (superscript + regex URL).
   - Chỉnh sửa `toc_generator.py` (cố định tab stop 15.8cm).
   - Chỉnh sửa `cover_page_builder.py` (bảng 2 cột cân đối) và `report-meta.yaml` (`CS106.F31.CN2.TTNT`).
2. **Step 2: Cập nhật văn bản nguồn `report-source.md`**:
   - Thêm Lời cảm ơn, Cam kết liêm chính, Bảng phân công 7 thành viên, Abstract tiếng Anh, Bảng từ viết tắt.
   - Làm sạch mục Tài liệu tham khảo và thêm 4 tài liệu Việt Nam.
   - Thêm Phụ lục A, B, C ở cuối tài liệu.
3. **Step 3: Biên dịch kép và đồng bộ số trang**:
   - Chạy `python3 build_report.py` để xuất Word và PDF qua AppleScript.
4. **Step 4: Kiểm định thực nghiệm tự động**:
   - Viết scratch script kiểm tra tọa độ cột số trang Mục lục trong PDF.
   - Quét HTTP mã phản hồi của toàn bộ URL để đảm bảo 0 link chết.

---

## 5. Todo Checklist

- [x] Cập nhật `report-meta.yaml` bổ sung `class_id: "CS106.F31.CN2.TTNT"`.
- [x] Sửa `cover_page_builder.py`: Dựng bảng 2 cột GVHD vs SVTH, căn chỉnh khoảng cách bìa.
- [x] Sửa `toc_generator.py`: Khóa cứng tab stop tại 15.8cm, sửa regex H3.
- [x] Sửa `inline_parser.py` & `hyperlink_helpers.py`: Hỗ trợ superscript `[n]` và tách dấu chấm khỏi URL.
- [x] Cập nhật `report-source.md`:
  - [x] Thêm Lời cảm ơn và Cam kết liêm chính học thuật.
  - [x] Thêm Bảng phân công nhiệm vụ và tỷ lệ hoàn thành của 7 thành viên.
  - [x] Thêm Tóm tắt tiếng Anh (ABSTRACT).
  - [x] Thêm Danh mục từ viết tắt.
  - [x] Loại bỏ code nội bộ khỏi TLTK, thêm 4 bài báo Việt Nam uy tín.
  - [x] Thêm Phụ lục A, B, C (Mã nguồn, Môi trường, Web Demo).
- [x] Thực hiện biên dịch kép và xuất PDF chuẩn qua Word AppleScript.
- [x] Chạy script kiểm định: Đo độ thẳng hàng Mục lục (diff=0.0pt) và quét HTTP 100% link sống (0 lỗi 404).
- [x] Đồng bộ bản Word và PDF hoàn chỉnh sang thư mục `submit/report/` và `submit/CS106_F31_CN2 - Nhom 9/Bao_cao/`.

---

## 6. Success Criteria & Evidence

- Bìa báo cáo hiển thị trang trọng, chia 2 cột rõ ràng, có lớp `CS106.F31.CN2.TTNT`.
- Mục lục thẳng tắp 100% (kiểm tra bằng PyMuPDF không còn hiện tượng thụt thò bậc thang).
- Số trích dẫn trong bài hiển thị dạng số mũ Superscript `[n]` nhỏ gọn, click nhảy chính xác đến tài liệu tham khảo.
- 100% link DOI và website trong danh mục tài liệu tham khảo hoạt động tốt (HTTP 200/202, không còn lỗi 404 dấu chấm).
- Báo cáo có đầy đủ Cam kết liêm chính học thuật, Bảng phân công nhóm và Danh mục từ viết tắt theo chuẩn UIT.
- Bản Word và PDF được đồng bộ nhất quán sang `submit/report/`.
