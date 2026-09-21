# Kịch bản quay Demo UI

**Người trình bày:** Phạm Thành Trung · **Thời lượng dự kiến:** 5–6 phút

**Sản phẩm:** Fraud Shield — Hệ thống phát hiện giao dịch tài chính bất thường

## Chuẩn bị trước khi quay

1. Chạy app từ thư mục gốc dự án:

   ```bash
   streamlit run demo/app.py
   ```

2. Mở `http://localhost:8501`, đặt cửa sổ ở 1920 × 1080 và zoom trình duyệt khoảng 90–100%.
3. Giữ giao diện **Tối** khi bắt đầu; kiểm tra ba màn hình **Phân tích giao dịch**, **Hiệu năng mô hình** và **Lịch sử phân tích** đều mở được.
4. Trong **Dữ liệu mẫu**, xác nhận có ba mức mô phỏng:
   - **Hợp lệ — dòng tiền cân đối**
   - **Cần lưu ý — chưa vượt ngưỡng**
   - **Nghi vấn gian lận — vượt ngưỡng**
5. Không quay thông báo lỗi, dữ liệu placeholder hoặc thao tác chờ tải trang.

## Kịch bản ghi hình và lời thoại

### 1. Mở đầu

**Thao tác:** Mở màn hình **Phân tích giao dịch** và để toàn cảnh giao diện Tối.

> Xin chào thầy và các bạn. Em tên là Phạm Thành Trung, đại diện cho Nhóm 9 trình bày phần demo của hệ thống.

### 2. Giới thiệu khu vực nhập giao dịch

**Thao tác:** Chỉ lần lượt vào loại giao dịch, ngày, giờ, step, số tiền và các trường số dư.

> Đầu tiên, đây là khu vực nhập thông tin giao dịch.
>
> Người dùng có thể nhập loại giao dịch, thời điểm thực hiện, số tiền, cùng với số dư của tài khoản trước và sau giao dịch.
>
> Sau khi nhận dữ liệu, hệ thống sẽ kiểm tra, tạo các đặc trưng cần thiết rồi mới đưa vào mô hình để phân tích.

### 3. Demo giao dịch hợp lệ

**Thao tác:**

1. Mở **Dữ liệu mẫu**.
2. Chọn **Hợp lệ — dòng tiền cân đối**.
3. Cho thấy dữ liệu mới chỉ được điền vào biểu mẫu.
4. Nhấn **Phân tích giao dịch** và cuộn đến kết quả.

> Đầu tiên, em chọn một mẫu giao dịch có dòng tiền cân đối.
>
> Sau khi chọn, hệ thống chỉ điền dữ liệu vào biểu mẫu và chưa thực hiện dự đoán. Người dùng vẫn có thể kiểm tra hoặc thay đổi thông tin trước khi phân tích.
>
> Bây giờ em nhấn “Phân tích giao dịch”.
>
> Có thể thấy mô hình trả về mức rủi ro rất thấp và giao dịch được phân loại là hợp lệ.

### 4. Demo giao dịch cần lưu ý

**Thao tác:**

1. Mở **Dữ liệu mẫu**.
2. Chọn **Cần lưu ý — chưa vượt ngưỡng**.
3. Nhấn **Phân tích giao dịch**.
4. Dừng tại mức xác suất và ngưỡng cảnh báo 50%.

> Tiếp theo, em thử một giao dịch có mức rủi ro cao hơn.
>
> Giao dịch này vẫn có dòng tiền cân đối, nhưng số tiền chiếm tỷ lệ khá lớn so với số dư tài khoản nguồn và được thực hiện vào thời điểm mô phỏng ban đêm.
>
> Sau khi phân tích, mô hình trả về xác suất gian lận khoảng 31,95%.
>
> Kết quả này vẫn chưa vượt ngưỡng cảnh báo là 50%, nên mô hình phân loại giao dịch là hợp lệ. Tuy nhiên, giao diện hiển thị mức “Cần lưu ý” để người dùng biết đây là một giao dịch nên được quan sát thêm.

### 5. Demo giao dịch nghi vấn gian lận

**Thao tác:**

1. Mở **Dữ liệu mẫu**.
2. Chọn **Nghi vấn gian lận — vượt ngưỡng**.
3. Nhấn **Phân tích giao dịch**.
4. Dừng tại nhãn **RỦI RO CAO** và thanh xác suất.

> Cuối cùng, em chọn một tình huống có nhiều dấu hiệu bất thường rõ ràng hơn.
>
> Ở đây, số tiền giao dịch lớn hơn số dư nguồn hiện có, tài khoản nguồn bị đưa về 0, đồng thời xuất hiện sai lệch trong quá trình cập nhật số dư.
>
> Sau khi phân tích, mô hình trả về xác suất rủi ro khoảng 88%.
>
> Do kết quả đã vượt ngưỡng cảnh báo 50%, hệ thống gắn cờ giao dịch là nghi vấn gian lận để ưu tiên đưa vào quá trình rà soát.

### 6. Giải thích quy trình phân tích

**Thao tác:** Tại **Quy trình phân tích**, lần lượt mở bốn bước và chỉ vào dữ liệu minh họa của từng bước.

> Ở phần Quy trình phân tích, người dùng có thể xem hệ thống xử lý một giao dịch như thế nào.
>
> Đầu tiên là kiểm tra dữ liệu đầu vào.
>
> Sau đó, hệ thống tạo các đặc trưng cần thiết từ giao dịch.
>
> Các đặc trưng số được chuẩn hóa rồi đưa vào mô hình XGBoost để tính xác suất gian lận.
>
> Cuối cùng, xác suất này được so sánh với ngưỡng cảnh báo để đưa ra kết quả phân loại.

### 7. Giới thiệu các góc nhìn trực quan

**Thao tác:** Lần lượt chuyển qua **Tín hiệu**, **Dòng tiền** và **Số dư**.

> Bên cạnh kết quả dự đoán, hệ thống còn cung cấp ba góc nhìn trực quan.
>
> Phần Tín hiệu cho biết những yếu tố đáng chú ý của giao dịch.
>
> Phần Dòng tiền giúp quan sát quá trình tiền di chuyển giữa hai tài khoản.
>
> Còn phần Số dư giúp đối chiếu giá trị trước và sau giao dịch.
>
> Nhờ đó, người dùng không chỉ nhìn thấy một con số xác suất mà còn có thêm thông tin để hiểu giao dịch.

### 8. Giới thiệu hiệu năng mô hình

**Thao tác:**

1. Bấm **Hiệu năng mô hình** trên sidebar.
2. Chỉ vào các thẻ chỉ số và bảng so sánh Random Forest, XGBoost và Autoencoder.
3. Cuộn qua biểu đồ ROC, Precision–Recall và Feature Importance.
4. Tại **Ma trận nhầm lẫn**, chuyển từ **SMOTENC** sang **ADASYN**.

> Tiếp theo là phần đánh giá hiệu năng mô hình.
>
> Ở đây, nhóm so sánh ba thuật toán gồm Random Forest, XGBoost và Autoencoder.
>
> Do dữ liệu gian lận bị mất cân bằng khá mạnh, nên thay vì chỉ dựa vào Accuracy, nhóm tập trung vào các chỉ số như Precision, Recall, F1-score, ROC-AUC và PR-AUC.
>
> Đây là các biểu đồ ROC và Precision–Recall, giúp đánh giá khả năng phân biệt giữa giao dịch hợp lệ và giao dịch gian lận.
>
> Đồng thời, ma trận nhầm lẫn giúp quan sát số giao dịch phát hiện đúng, số cảnh báo nhầm và những trường hợp gian lận bị bỏ sót.
>
> Hệ thống cũng cho phép chuyển giữa SMOTENC và ADASYN để đối chiếu kết quả của hai phương pháp xử lý mất cân bằng dữ liệu.

### 9. Giới thiệu lịch sử phân tích

**Thao tác:**

1. Bấm **Lịch sử phân tích** trên sidebar.
2. Chỉ vào các thẻ thống kê, bộ lọc và danh sách giao dịch.
3. Minh họa thao tác lọc và nút tải CSV.

> Cuối cùng là phần Lịch sử phân tích.
>
> Mỗi giao dịch sau khi được phân tích thành công sẽ được lưu lại cục bộ bằng SQLite.
>
> Người dùng có thể xem tổng số giao dịch, số cảnh báo, xác suất trung bình và kết quả gần nhất.
>
> Ngoài ra, người dùng có thể lọc lịch sử theo kết quả hoặc loại giao dịch, xóa riêng từng giao dịch và xuất lịch sử thành file CSV.

### 10. Kết thúc

**Thao tác:** Trở về màn hình **Phân tích giao dịch** và dừng ở toàn cảnh dashboard hoặc kết quả nghi vấn gian lận.

> Phần trình bày của em đến đây là kết thúc. Em xin cảm ơn thầy và các bạn.

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
- Video Demo: [Google Drive Nhóm 9 — Demo Video MP4](https://drive.google.com/file/d/1QkrP-Zl4LXTgB13U0lQkLU9hB72qkZGL/view) (nhúng link vào Slide PPT/PDF báo cáo; lưu trữ ngoại bộ để đảm bảo dung lượng repo Git luôn an toàn < 50MB)

## Phương án rút gọn nếu vượt thời gian

- Không đọc tên toàn bộ năm mô hình; chỉ nói “năm biến thể mô hình”.
- Chỉ chuyển SMOTENC → ADASYN một lần, không cuộn hết từng ma trận.
- Ở Lịch sử phân tích, chỉ giới thiệu SQLite, bộ lọc và xóa từng dòng; không tải CSV trong lúc quay.
