# Kịch bản quay Demo UI — 3 phút

**Người trình bày:** Phạm Thành Trung · **Thời lượng:** 03:00

**Sản phẩm:** Fraud Shield — Hệ thống phát hiện giao dịch tài chính bất thường

## Chuẩn bị trước khi quay

1. Chạy app từ `draft/fraud-detection`:

   ```powershell
   py -3.14 -m streamlit run demo/app.py
   ```

2. Mở `http://localhost:8501`, đặt cửa sổ ở 1920 × 1080 và zoom trình duyệt khoảng 90–100%.
3. Giữ giao diện **Tối** khi bắt đầu; kiểm tra ba màn hình **Phân tích giao dịch**, **Hiệu năng mô hình** và **Lịch sử phân tích** đều mở được.
4. Trong **Dữ liệu mẫu**, xác nhận có ba mức mô phỏng:
   - **Hợp lệ — dòng tiền cân đối**
   - **Cần lưu ý — chưa vượt ngưỡng**
   - **Nghi vấn gian lận — vượt ngưỡng**
5. Không quay thông báo lỗi, dữ liệu placeholder hoặc thao tác chờ tải trang.

## Kịch bản ghi hình và lời thoại

| Thời gian | Thao tác trên màn hình | Lời thoại đề xuất |
|-----------|-------------------------|-------------------|
| **00:00–00:18** | Mở màn hình **Phân tích giao dịch**, để toàn cảnh giao diện Tối. | “Xin chào thầy và các bạn. Em là Phạm Thành Trung, thành viên Nhóm 9. Đây là Fraud Shield, hệ thống phát hiện giao dịch tài chính bất thường trên PaySim, bộ dữ liệu mô phỏng giao dịch Mobile Money.” |
| **00:18–00:32** | Mở nút **Giao diện** ở cuối sidebar; bấm **Sáng**, sau đó trở lại **Tối**. | “Hệ thống hỗ trợ ba chế độ hiển thị gồm System, Sáng và Tối. Người dùng có thể chuyển giao diện trực tiếp mà không cần tải lại trang.” |
| **00:32–00:52** | Chỉ lần lượt vào ngày, giờ, step, loại giao dịch và các ô tiền/số dư. | “Tại đây, người dùng chọn chuyển khoản hoặc rút tiền, rồi nhập số tiền và các số dư liên quan. Ngày giờ và step tự động quy đổi qua lại; step là số giờ kể từ đầu mô phỏng PaySim. Giá trị tiền được phân tách hàng nghìn để dễ kiểm tra.” |
| **00:52–01:14** | Chọn **Hợp lệ — dòng tiền cân đối** trong **Dữ liệu mẫu**, rồi bấm **Phân tích giao dịch**. Cuộn nhẹ tới kết quả. | “Em chọn một giao dịch mô phỏng có dòng tiền cân đối. Sau khi nhấn Phân tích giao dịch, hệ thống tạo 14 đặc trưng, đưa vào XGBoost và trả về mức rủi ro thấp.” |
| **01:14–01:42** | Chọn **Nghi vấn gian lận — vượt ngưỡng**, bấm **Phân tích giao dịch**; dừng ở thẻ **RỦI RO CAO** và thanh xác suất. | “Tiếp theo là một tình huống mô phỏng đáng ngờ: giao dịch rút 2 triệu đơn vị, vượt số dư nguồn 1,6 triệu và đưa tài khoản về 0. Model trả xác suất khoảng 88 phần trăm nên hệ thống gắn cờ để rà soát. Đây là dự đoán rủi ro, không phải kết luận pháp lý rằng giao dịch chắc chắn gian lận.” |
| **01:42–01:58** | Lướt qua ba chế độ **Tín hiệu**, **Dòng tiền**, **Số dư**. | “Ba góc nhìn giúp giải thích đầu vào. Tín hiệu thể hiện mức độ nổi bật của từng yếu tố; Dòng tiền mô tả tiền di chuyển giữa hai tài khoản; Số dư làm rõ chênh lệch trước và sau giao dịch.” |
| **01:58–02:34** | Bấm **Hiệu năng mô hình**. Chỉ bảng so sánh, ROC/PR và Feature Importance; tại **Ma trận nhầm lẫn**, chuyển **SMOTENC** sang **ADASYN**. | “Màn hình Hiệu năng so sánh năm biến thể mô hình. Precision là tỷ lệ cảnh báo chính xác; Recall là khả năng tìm ra giao dịch gian lận; F1-score cân bằng hai chỉ số này. ROC-AUC và PR-AUC đánh giá khả năng phân biệt tổng thể. Các biểu đồ thể hiện đường cong đánh giá, đặc trưng quan trọng, ma trận nhầm lẫn và các ca dự đoán đúng hoặc sai. SMOTENC và ADASYN là hai cách cân bằng tập huấn luyện khi gian lận chiếm tỷ lệ rất thấp.” |
| **02:34–02:52** | Bấm **Lịch sử phân tích**; chỉ các KPI, biểu đồ, bộ lọc và bảng. Bấm thử **Cảnh báo**, rồi trở về **Tất cả**. | “Kết quả được lưu cục bộ bằng SQLite nên vẫn còn sau khi khởi động lại ứng dụng. Người dùng có thể xem thống kê, lọc cảnh báo, tải CSV và xóa riêng từng giao dịch.” |
| **02:52–03:00** | Trở về **Phân tích giao dịch**, dừng ở kết quả gian lận hoặc toàn cảnh dashboard. | “Fraud Shield hoàn chỉnh luồng nhập dữ liệu, dự đoán bằng mô hình thật, giải thích kết quả, đánh giá hiệu năng và quản lý lịch sử. Em xin cảm ơn thầy và các bạn.” |

## Điểm cần nhấn mạnh khi nói

- Ba đầu vào demo là **tình huống mô phỏng**; xác suất hiển thị được tính trực tiếp bằng model thật, không chỉnh tay.
- SMOTE/ADASYN chỉ áp dụng trên tập train; tập test được giữ nguyên để đánh giá.
- Đánh giá tập trung vào Precision, Recall, F1-score, ROC-AUC và PR-AUC.
- Ngày giờ trên UI là mốc mô phỏng được quy đổi sang `step` của PaySim, không phải thời gian lịch gốc của dataset.
- Lịch sử SQLite là dữ liệu cục bộ trên máy chạy app, không tự chia sẻ sang máy khác.

## Evidence cần lưu

- `screenshots/dashboard-dark.png`
- `screenshots/dashboard-light.png`
- `screenshots/prediction-legitimate.png`
- `screenshots/prediction-fraud.png`
- `screenshots/model-performance.png`
- Video: `fraud-shield-demo.mp4`

## Phương án rút gọn nếu vượt thời gian

- Không đọc tên toàn bộ năm mô hình; chỉ nói “năm biến thể mô hình”.
- Chỉ chuyển SMOTENC → ADASYN một lần, không cuộn hết từng ma trận.
- Ở Lịch sử phân tích, chỉ giới thiệu SQLite, bộ lọc và xóa từng dòng; không tải CSV trong lúc quay.
