# Kịch bản Demo UI Phase 06

**Owner:** Phạm Thành Trung · **Thời lượng mục tiêu:** 2–3 phút

## Chuẩn bị

1. Chạy từ `draft/fraud-detection`:

   ```powershell
   py -3.14 -m streamlit run demo/app.py
   ```

2. Xác nhận `http://localhost:8501/_stcore/health` trả `ok`.
3. Chỉ quay màn hình Hiệu năng sau khi có đủ:
   - `reports/model_comparison.csv`
   - `reports/figures/roc_curves_all.png`
   - `reports/figures/pr_curves_all.png`
   - Ba file `confusion_matrix_*.png`

## Luồng trình bày

### Nhập thời gian và tiền tệ

- Chọn trực tiếp **Ngày** và **Giờ** giao dịch trong khoảng thời gian mô phỏng; giao diện chỉ nhận giờ tròn.
- PaySim không có ngày lịch gốc, vì vậy ngày giờ trên giao diện là mốc mô phỏng và được quy đổi ngầm sang đặc trưng thời gian mà model yêu cầu.
- Số tiền và bốn ô số dư tự phân tách hàng nghìn khi rời ô nhập: `250000` → `250.000`. Phần lẻ dùng dấu phẩy, ví dụ `1.143.937,73`; đơn vị là tiền mô phỏng PaySim.
- Nhấn **Phân tích giao dịch** để chạy model. Đổi ngày giờ hoặc định dạng tiền không tự tạo dự đoán mới. Lịch sử hiển thị ngày giờ mô phỏng; CSV giữ số tiền dạng số để tái sử dụng.

### Kịch bản ghi hình

| Thời gian | Thao tác | Nội dung nói |
|-----------|----------|--------------|
| 00:00–00:20 | Mở trang Phân tích giao dịch | Giới thiệu PaySim, 14 đặc trưng và XGBoost-SMOTE đang được triển khai |
| 00:20–00:35 | Mở nút Giao diện | Chuyển nhanh Tối → Sáng → System để chứng minh theme hoạt động |
| 00:35–01:00 | Chọn mẫu “Hợp lệ — dự đoán đúng” | Phân tích số tiền, số dư và kết quả rủi ro thấp; đối chiếu nhãn X_test |
| 01:00–01:30 | Chọn mẫu “Gian lận — phát hiện đúng” | Trình bày xác suất, nhãn nghi vấn gian lận và Risk Meter |
| 01:30–02:05 | Mở Hiệu năng mô hình | Trình bày bảng Precision, Recall, F1, ROC-AUC, PR-AUC và các figures Phase 05 |
| 02:05–02:25 | Mở Hồ sơ dự án | Tóm tắt pipeline, SMOTE/ADASYN chỉ áp dụng trên train và test set được giữ nguyên |
| 02:25–02:40 | Quay lại Phân tích giao dịch | Kết luận demo dùng model/artifact thật và không dựng số liệu giả |

## Evidence cần lưu

- `screenshots/dashboard-dark.png`
- `screenshots/dashboard-light.png`
- `screenshots/prediction-legitimate.png`
- `screenshots/prediction-fraud.png`
- `screenshots/model-performance.png`
- Video MP4: `fraud-shield-demo.mp4`

Không chụp hoặc quay placeholder Phase 05 làm kết quả chính thức.
