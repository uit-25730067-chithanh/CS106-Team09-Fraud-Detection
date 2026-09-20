# Wireframe — Fraud Shield Demo

**Owner:** Phạm Thành Trung

**Purpose:** Đặc tả bố cục và nguyên tắc hiển thị của Demo UI

## Bố cục

```text
┌─ Sidebar thu gọn được ─┬─ Main workspace ──────────────────────┐
│ Logo + Fraud Shield    │ Nội dung của màn hình đang chọn       │
│                        │                                       │
│ Phân tích giao dịch    │ Phân tích: header + preset + form     │
│ Hiệu năng mô hình      │ Hiệu năng: dataset + model metrics    │
│ Hồ sơ dự án            │ Hồ sơ: thông tin + pipeline           │
│ Kịch bản nhanh (Pills) │                                       │
│                        │                                       │
│ [Giao diện]            │ Không lặp lại tab điều hướng ngang    │
└────────────────────────┴───────────────────────────────────────┘
```

## Khu vực chính

1. **Phân tích giao dịch:** Form 7 trường PaySim, 4 quick presets, validation, payload và inference thật.
2. **Preview trực quan:** Bản đồ tín hiệu, Dòng tiền và Sai lệch số dư.
   - Hero có ngưỡng cảnh báo tương tác 10–90%, thay hoàn toàn khối trang trí trạng thái model.
   - Risk Meter là điểm nhấn đầu tiên sau dự đoán, dùng thang xanh–cam–đỏ, một nhãn xác suất nổi, vạch ngưỡng không chữ và các mốc 0–25–50–75–100%.
3. **Hiệu năng mô hình:** Phân bố nhãn thật; chừa vị trí cho comparison table và figures từ Phase 05.
4. **Hồ sơ dự án:** Dataset, mô hình, metrics và tiến độ pipeline.
5. **Quy trình phân tích 4 bước:** Trực quan hóa hành trình xử lý từ kiểm tra đầu vào, trích xuất đặc trưng, chuẩn hóa dữ liệu đến tính toán xác suất qua XGBoost; tích hợp modal chi tiết từng bước.
6. **Hộp thoại chọn dữ liệu mẫu (Sample Picker Dialog):** Modal cho phép chọn kịch bản mẫu hoặc tải tệp CSV/JSON ngoại vi, điền vào form trước và chỉ suy luận khi người dùng nhấn "Phân tích giao dịch".

Sidebar giữ điều hướng chính, bốn kịch bản nhanh theo ngữ cảnh và nút giao diện. Cụm kịch bản chỉ xuất hiện ở màn hình Phân tích giao dịch; lựa chọn được giữ khi chuyển màn hình. Brand header, active state có vạch nhấn, hover nhẹ và model status card tạo phân cấp rõ mà không lấn át nội dung.

## Theme

| Chế độ | Đặc điểm |
|--------|----------|
| System | Theo thiết lập giao diện của hệ điều hành |
| Sáng | Nền pastel sáng, tương phản rõ khi trình chiếu |
| Tối | Nền indigo sâu, điểm nhấn violet–cyan |

Nút **Giao diện** nằm cuối sidebar. Ba lựa chọn dùng icon, active state và ARIA phù hợp. Theme được lưu bằng cơ chế native của Streamlit; toolbar tối giản và không hiển thị menu ba chấm góc phải.

## Nguyên tắc thiết kế

- Visual hierarchy rõ: trạng thái → thao tác → preview → thông tin hỗ trợ.
- Responsive trên màn hình demo và tự xuống hàng khi chiều rộng giảm.
- Material icons, card bo góc và màu nhấn thống nhất với logo.
- Chuyển động có thể tắt và không làm thay đổi dữ liệu hoặc model state.
- Biểu đồ có tooltip, chú thích và khoảng đệm an toàn.
- Chỉ hiển thị nhãn và xác suất khi XGBoost/scaler chạy thành công; lỗi phải fail-closed.
- Bản đồ tín hiệu và data-quality score chỉ mô tả đầu vào, không phải kết quả inference.

## Nguồn dữ liệu trực quan

| Visual | Nguồn | Ranh giới |
|--------|-------|-----------|
| Phân bố nhãn | `y_train.pkl`, `y_test.pkl` | Mô tả dataset, không phải metric model |
| Bản đồ tín hiệu | Giao dịch vừa nhập | Không phải fraud score |
| Dòng tiền | Số dư nguồn/đích trước và sau | Không dự đoán gian lận |
| Sai lệch số dư | Sai lệch tính từ payload | Chỉ kiểm tra tính nhất quán đầu vào |

## Trạng thái bàn giao

Wireframe đã được hiện thực trong `demo/app.py`. Tiến độ, evidence và phần còn lại được quản lý tại `plans/fraud-detection-full-submit/phase-06-demo-ui.md`.
