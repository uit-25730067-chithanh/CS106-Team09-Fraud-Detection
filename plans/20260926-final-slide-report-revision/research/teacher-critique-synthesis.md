# Nghiên Cứu & Tổng Hợp: Triết Lý Đánh Giá Của Giảng Viên (PGS.TS. Nguyễn Đình Hiển)

**Khóa học**: CS106 - Trí tuệ Nhân tạo (HK3/HK4 2026)  
**Nguồn dữ liệu**: Transcript & Báo cáo Buổi 10 (Báo cáo Cuối kỳ Đợt 1)  
**Đối tượng thụ hưởng**: Nhóm 09 (PaySim Financial Fraud Detection)

---

## 1. Bản Đồ 3 Trụ Cột Đánh Giá Cốt Lõi

Qua khảo sát toàn bộ các lượt chất vấn của thầy Hiển với các nhóm trong Buổi 10:

```text
               HỆ QUY CHIẾU PHẢN BIỆN (PGS.TS. NGUYỄN ĐÌNH HIỂN)
                                    │
    ┌───────────────────────────────┼───────────────────────────────┐
    ▼                               ▼                               ▼
[Trụ cột 1: Empirical Proof]    [Trụ cột 2: Anti-Leakage & Reality] [Trụ cột 3: Knowledge Rep.]
- Đo đếm có số liệu đối chứng.  - Cảnh báo bẫy Look-ahead bias.     - Phản đối "chạy mô hình mù".
- Bắt buộc có Ablation Study    - Cảnh báo bẫy Random Split chuỗi   - Đưa tri thức thực tế vào
  (thử tăng/giảm đặc trưng).      thời gian tài chính.                đặc trưng (môn CS106).
- Thử nghiệm nhiều giải pháp    - Phản đối khoe điểm F1/Acc 99.7%   - Biến số liệu thô thành quy
  rồi mới kết luận mô hình.       trên tập lệch lớp đã downsample.    luật nghiệp vụ có ngữ nghĩa.
```

---

## 2. Đối Chiếu Thực Trạng Nhóm 09 & Điểm Hở Học Thuật

### Trụ cột 1: Thực nghiệm đối chứng & Thử nghiệm loại suy (Ablation Study)
- **Tình huống thực tế lớp học**: Thầy chất vấn Nhóm 5 về việc loại bỏ đặc trưng. Nhóm 5 đã chứng minh thử bỏ 4 biến và thấy Recall sụt giảm, thầy khen ngợi việc có số liệu minh chứng trước khi chọn.
- **Hiện trạng Nhóm 09**: Nhóm phát hiện 2 biến số dư chiếm tới 97.11% Feature Gain trên XGBoost, nhưng trong báo cáo lại ghi *"thí nghiệm loại bỏ nhóm số dư nằm ngoài phạm vi đồ án"*.
- **Rủi ro phản biện**: Hội đồng sẽ chất vấn: *"Tại sao biết rủi ro Simulator Artifact mà không chạy một thực nghiệm loại bỏ 2 biến này để xem baseline thực sự là bao nhiêu?"*

### Trụ cột 2: Chống rò rỉ dữ liệu (Anti-Leakage) & Phòng vệ chuỗi thời gian
- **Tình huống thực tế lớp học**: Thầy cảnh báo Nhóm 11 về việc chia dữ liệu tài chính ngẫu nhiên gây Look-ahead bias và ảo tưởng điểm số.
- **Hiện trạng Nhóm 09**: Dữ liệu PaySim có cột `step` (thời gian 31 ngày). Nhóm chia Stratified Random Split 80/20. Trên Slide 11, nhóm giật tít *"Chuẩn Leak-Free tuyệt đối"*.
- **Rủi ro phản biện**: Thầy có thể bắt lỗi: *"Tại sao dữ liệu có thuộc tính thời gian lại chia ngẫu nhiên mà dám khẳng định Leak-Free 100%?"*
- **Giải pháp**: Nhóm phải phân định rõ ràng trên Slide: Đạt chuẩn Leak-Free về mặt Preprocessing/Scaler/Resampling; còn giới hạn Temporal Split đã được nhóm chủ động mổ xẻ tại Mục 3.6.4 của Báo cáo.

### Trụ cột 3: Biểu diễn tri thức thực tế (Knowledge Representation)
- **Tình huống thực tế lớp học**: Thầy phê bình Nhóm 10/14 (Dự báo giá nhà) chỉ làm trên dữ liệu thô, thiếu thông số tiện ích, và nhấn mạnh: *"Cái đó mình học gọi là Biểu diễn tri thức (Knowledge Representation), đưa tri thức thực tế vào thì hệ thống mới sát thực tế hơn."*
- **Hiện trạng Nhóm 09**: Nhóm dùng thuật ngữ thuần Data Science: "Feature Engineering", "Domain Features", xuất hiện đúng 0 lần thuật ngữ "Biểu diễn tri thức".
- **Cơ hội ăn điểm**: Re-frame 14 đặc trưng thành sản phẩm của quá trình **Biểu diễn tri thức nghiệp vụ kế toán kép (Double-Entry Bookkeeping)** và quy luật dòng tiền ngân hàng.

---

## 3. Kết Luận Định Hướng Chỉnh Sửa

1. **Thực hiện ngay một thực nghiệm Ablation định lượng**: Chạy script huấn luyện XGBoost/Random Forest khi loại bỏ 2 biến số dư và khi prune các biến có Gain ≈ 0 (như `is_night_transaction`), ghi nhận bảng số liệu minh chứng 100% khách quan.
2. **Tách biệt 2 Plan song song**:
   - **Plan Slide**: Tối ưu hóa tính trực quan, đưa Bảng quy chiếu Prevalence gốc (0.129%), bổ sung nhãn Biểu diễn tri thức, thêm ghi chú phòng thủ rủi ro Temporal Split.
   - **Plan Report**: Nâng cấp học thuật 6 chương, bổ sung lý thuyết Biểu diễn tri thức, tích hợp kết quả thực nghiệm Ablation, giải trình sâu sắc về Autoencoder Unsupervised Zero-Day.
