# Phase 02: Kế Hoạch Tinh Chỉnh Slide Báo Cáo Chuyên Sâu (`.pptx` & `.pdf`)

## 1. Context Links
- Parent Plan: [plan.md](plan.md)
- Slide Generator Script: [generate_cs106_style_slides_vn.js](../../draft/fraud-detection/slide/generate_cs106_style_slides_vn.js)
- Output Slide PDF: [[Nhom9]_Slide_FraudDetection.pdf](../../submit/CS106_F31_CN2%20-%20Nhom%209/Bao_cao/%5BNhom9%5D_Slide_FraudDetection.pdf)
- Research Synthesis: [teacher-critique-synthesis.md](research/teacher-critique-synthesis.md)

---

## 2. Overview
- **Ngày lập**: 2026-09-26
- **Mục tiêu**: Tinh chỉnh toàn diện nội dung, cấu trúc và luận điểm học thuật trong 21 trang Slide, chuyển hóa bài thuyết trình thành một công trình nghiên cứu chuẩn mực, giải quyết toàn bộ các "góc chết" mà giảng viên có thể chất vấn.
- **Thời lượng dự kiến**: ~60 phút.
- **Mức độ ưu tiên**: P1.
- **Trạng thái**: Completed.

---

## 3. Danh Mục Chi Tiết Các Slide Đã Tinh Chỉnh

```text
SLIDE ĐIỀU CHỈNH               NỘI DUNG THỐNG NHẤT & CHUẨN HÓA THỰC TẾ
─────────────                  ──────────────────────────────────────
Slide 08 (Feature Eng.)   ──►  14 Thuộc tính miền cốt lõi (Kế toán kép, Cờ vét sạch, Chu kỳ giờ)
Slide 11 (Leak-Free)      ──►  Lưu ý học thuật: Phòng thủ Temporal Split & tham chiếu Mục 3.6.4
Slide 15 (Benchmark)      ──►  Quy chiếu tỷ lệ gốc 0.129%: RF Precision 98.01% (26 FP / 1M GD)
Slide 16 (Confusion Mtx)  ──►  Ma trận nhầm lẫn 3 mô hình, nhấn mạnh tỷ lệ báo động giả cực thấp
Slide 17 (Feature Imp.)   ──►  Bổ sung thực nghiệm Ablation No-Balance: F1 sụp đổ còn 71.16%
Slide 18 (Autoencoder)    ──►  Định vị lớp phòng vệ Defense-in-Depth phát hiện dị biệt không cần nhãn
Slide 20 (Demo & Roadmap) ──►  Tổng kết đóng góp, demo Streamlit (XGBoost/Autoencoder) & 3 hướng đi
Slide 21 (Q&A / End)      ──►  Căn giữa thông điệp cảm ơn, link repo unbold màu trắng thanh lịch
```

---

### Chi Tiết Cụ Thể Từng Slide:

#### 1. Slide 08: Kỹ Thuật Đặc Trưng: 14 Thuộc Tính Miền Cốt Lõi
- **Tựa đề**: `Kỹ thuật Đặc trưng: 14 Thuộc tính Miền Cốt lõi` (Loại bỏ các thuật ngữ quá hàn lâm như "Biểu diễn Tri thức / Knowledge Representation" theo thống nhất, giữ ngôn ngữ kỹ thuật ngân hàng thực tiễn).
- **Nội dung chuẩn hóa**:
  - *Sai lệch Số dư Nguồn (Delta Orig)*: `errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig` (Nguyên lý kế toán kép).
  - *Sai lệch Số dư Đích (Delta Dest)*: `errorBalanceDest = oldbalanceDest + amount - newbalanceDest`.
  - *Cờ Vét sạch & Chu kỳ Giờ*: `drain_flag` (rút cạn tài khoản về 0) và `hour / is_overnight` (tấn công tự động ban đêm).
  - *Bảng chú giải biến & Đúc kết Feature Importance*: Nêu rõ 2 biến số dư chiếm 97.1% Gain và lưu ý rủi ro simulator artifact (Mục 3.6.2).

#### 2. Slide 11: Kiến Trúc Pipeline ML & Phòng Thủ Rủi Ro Rò Rỉ Thời Gian
- **Tựa đề**: `Kiến trúc Pipeline Machine Learning & Đảm bảo Tính Toàn vẹn Dữ liệu`.
- **Nội dung chuẩn hóa**:
  - Tại nguyên tắc chống rò rỉ: Bổ sung ghi chú học thuật: `Giới hạn chuỗi thời gian: Phân tầng giữ tỷ lệ 0.13% fraud; rủi ro temporal split được phân tích chi tiết tại Mục 3.6.4 Báo cáo.`
  - Thể hiện tư duy phản biện khoa học, chủ động giải trình hạn chế dữ liệu mô phỏng.

#### 3. Slide 15: Kết Quả Thực Nghiệm & Quy Chiếu Tỷ Lệ Gốc (Prevalence = 0.129%)
- **Nội dung chuẩn hóa**:
  - Tích hợp trực tiếp vào khối Quy chiếu Tỷ lệ Gốc: `RF đạt Precision 98.01% (CI 95%: 89.85% - 99.95%), chỉ 26 ca báo động giả trên 1.000.000 GD hợp lệ.`
  - Nêu rõ sự đánh đổi: Autoencoder trên tỷ lệ gốc có Precision rơi xuống `1.83% (~52.022 FP / 1M GD)` do thiếu nhãn giám sát, chỉ phù hợp làm lớp cảnh báo dị biệt thứ cấp.

#### 4. Slide 16: Phân Tích Ma Trận Nhầm Lẫn & Chi Phí Vận Hành Đánh Đổi Sai Số
- **Nội dung chuẩn hóa**:
  - Trình bày 3 thẻ đối chiếu chi tiết kết hợp góc nhìn chi phí vận hành thực tế:
    - *Random Forest*: FP: 1, FN: 8 (~26 FP / 1M GD quy chiếu gốc), triệt tiêu chi phí điều tra thủ công báo động giả.
    - *XGBoost*: FP: 4, FN: 8 (~104 FP / 1M GD), độ trễ cỡ nửa mili-giây (CPU), tối ưu chi phí hạ tầng sản xuất thời gian thực.
    - *Deep Autoencoder*: TP: 1,236, FP: 1,998 (~52k FP / 1M GD), chi phí xác minh cao, chỉ phù hợp làm màng lọc an toàn thứ cấp chuyên sâu.

#### 5. Slide 17: Phân Tích Đóng Góp Đặc Trưng & Minh Chứng Thực Nghiệm Ablation
- **Nội dung chuẩn hóa**:
  - Bảng tỷ trọng Gain: `errorBalanceOrig` (49.9%), `newbalanceOrig` (47.2%), `amount` (0.5%), `hour/overnight` (0.03%).
  - Tích hợp đầy đủ cả 2 thực nghiệm Ablation (Phase 01):
    - *Ablation No-Balance*: Bỏ nhóm số dư khiến F1 sụp đổ còn 71.16% (ca bỏ sót tăng vọt từ 8 lên 472 ca, Mục 3.6.2).
    - *Ablation Pruning*: Cắt tỉa `is_night_transaction` (0% gain) & biến phụ giúp giảm độ trễ, giữ nguyên 100% F1.

#### 6. Slide 18: Định Vị Vai Trò Autoencoder (Zero-Day Out-of-Distribution Anomaly)
- **Nội dung chuẩn hóa**:
  - Khẳng định vai trò: Chiến lược Defense-in-Depth - lớp phòng thủ thứ cấp phát hiện tấn công Zero-Day ngoài phân phối (Out-of-Distribution Anomaly).
  - Học không giám sát: Mạng Autoencoder huấn luyện 100% không nhãn trên luồng tiền hợp lệ, không phụ thuộc vào tri thức tấn công quá khứ.
  - Điểm cắt chọn 95th (τ = 0.0455): F1 đạt 0.5064 trên Validation; Recall 75.2%, Precision 38.2% trên Test độc lập.

#### 7. Slide 20 & 21: Demo Streamlit, Lộ Trình Nghiên Cứu & Kết Thúc
- **Slide 20**:
  - *Demo Streamlit & Đóng góp Cốt lõi*: Nêu rõ 3 kịch bản kiểm thử (GD hợp lệ, Tấn công vét sạch Drain, Tẩu tán số dư lớn); kiến trúc Dual-Model; nguyên tắc chống rò rỉ và ablation số dư.
  - *Lộ trình Nghiên cứu*: Bổ sung Lộ trình Time-Series Split (kiểm định drift chuỗi thời gian 31 ngày Mục 3.6.4), Graph Neural Networks (GNN GraphSAGE), và Streaming Kafka/Flink + XAI (SHAP).
- **Slide 21**: Căn giữa thông điệp cảm ơn trang trọng; link GitHub repo công khai định dạng màu trắng, không in đậm; trích dẫn 4 tài liệu chuẩn IEEE.

---

## 4. Implementation Steps
1. **Chỉnh sửa script JavaScript**: Tinh chỉnh mã nguồn `generate_cs106_style_slides_vn.js` chuẩn hóa layout và cập nhật đầy đủ các kết quả học thuật.
2. **Biên dịch Presentation**: Sinh file PPTX `[Nhom9]_Slide_FraudDetection_Academic_VN.pptx`.
3. **Chuyển đổi sang PDF**: Xuất bản PDF `[Nhom9]_Slide_FraudDetection.pdf` vector chất lượng cao qua Microsoft PowerPoint AppleScript.
4. **Kiểm tra trực quan layout**: Đảm bảo không tràn khung, không gãy từ tiếng Việt, căn giữa câu cảm ơn và đủ 21 trang.

---

## 5. Todo List
- [x] Tinh chỉnh Slide 08: 14 thuộc tính miền cốt lõi, kế toán kép, cờ vét sạch, chu kỳ giờ (giữ chuẩn kỹ thuật ngân hàng thực tiễn).
- [x] Bổ sung ghi chú phòng vệ Temporal Split tại Slide 11.
- [x] Tích hợp số liệu quy chiếu tỷ lệ gốc 0.129% (RF Precision 98.01% CI 95% [89.85%, 99.95%], 26 FP / 1M GD; AE 1.83%) vào Slide 15.
- [x] Trình bày ma trận nhầm lẫn 3 mô hình kết hợp góc nhìn chi phí vận hành tại Slide 16.
- [x] Bổ sung minh chứng Ablation Study (No-Balance F1 71.16% & Pruning biến 0% gain) vào Slide 17.
- [x] Chuẩn hóa định vị Autoencoder Zero-Day Out-of-Distribution Anomaly & Defense-in-Depth tại Slide 18.
- [x] Tích hợp 3 kịch bản Demo Streamlit và Lộ trình Time-Series Split tại Slide 20.
- [x] Căn giữa câu cảm ơn và định dạng link repo màu trắng unbold tại Slide 21.
- [x] Sửa lỗi co giãn cột bảng biểu tránh gãy từ tiếng Việt và sửa lỗi đè shape.
- [x] Biên dịch PPTX và xuất bản PDF chuẩn 21 trang không lỗi layout.

---

## 6. Success Criteria & Evidence
- File PDF `assignments/Final/draft/fraud-detection/slide/[Nhom9]_Slide_FraudDetection.pdf` đạt chuẩn 21 trang.
- Toàn bộ nội dung bám sát thảo luận thực tiễn, loại bỏ thuật ngữ sáo rỗng/hàn lâm không cần thiết.
- Layout và bảng biểu sạch sẽ, không tràn chữ, không lệch khung.

---

## 7. Risk Assessment & Mitigations
- **Rủi ro**: Thêm nội dung vào Slide 15 và 17 có thể gây tràn khung (text overflow).
  - *Biện pháp*: Giữ cấu trúc 2 cột cân đối, điều chỉnh font size từ 9.0 xuống 8.3pt và dùng margin tối thiểu [2, 4, 2, 4].
- **Rủi ro**: Xuất PDF qua Node.js có thể bị lỗi font tiếng Việt.
  - *Biện pháp*: Tiếp tục sử dụng `pptxgenjs` để sinh PPTX chuẩn UTF-8, sau đó dùng Microsoft Word AppleScript để render PDF hoàn hảo.

---

## 8. Next Steps
Chuyển sang [Phase 03](phase-03-report-comprehensive-revision.md) để cập nhật Báo cáo nghiên cứu.
