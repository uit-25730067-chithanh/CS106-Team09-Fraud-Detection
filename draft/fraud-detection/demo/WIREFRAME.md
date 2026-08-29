# Wireframe — Fraud Shield Demo

**Owner:** Phạm Thành Trung

**Revision:** 7.7

**Purpose:** Đặc tả bố cục và nguyên tắc hiển thị của Demo UI

## Bố cục

```text
┌─ Sidebar ──────────────┬─ Main workspace ───────────────────────┐
│ Logo + project status │ Header + trạng thái dữ liệu/model       │
│ Pipeline progress     │                                        │
│ Motion control       │ Phân tích | Hiệu năng | Hồ sơ           │
│                      │                                        │
│ [Giao diện]          │ Quick presets                           │
│ System/Sáng/Tối      │ Form giao dịch | Preview trực quan      │
└──────────────────────┴────────────────────────────────────────┘
```

## Khu vực chính

1. **Phân tích giao dịch:** Form 7 trường PaySim, 3 quick presets, validation và payload.
2. **Preview trực quan:** Bản đồ tín hiệu, Dòng tiền và Sai lệch số dư.
3. **Hiệu năng mô hình:** Phân bố nhãn thật; chừa vị trí cho comparison table và figures từ Phase 05.
4. **Hồ sơ dự án:** Dataset, mô hình, metrics và tiến độ pipeline.

## Theme

| Chế độ | Đặc điểm |
|--------|----------|
| System | Theo thiết lập giao diện của hệ điều hành |
| Sáng | Nền pastel sáng, tương phản rõ khi trình chiếu |
| Tối | Nền indigo sâu, điểm nhấn violet–cyan |

Nút **Giao diện** được ghim ở góc trái dưới. Ba lựa chọn dùng icon, active state và ARIA phù hợp. Theme được lưu bằng cơ chế native của Streamlit; toolbar tối giản và không hiển thị menu ba chấm góc phải.

## Nguyên tắc thiết kế

- Visual hierarchy rõ: trạng thái → thao tác → preview → thông tin hỗ trợ.
- Responsive trên màn hình demo và tự xuống hàng khi chiều rộng giảm.
- Material icons, card bo góc và màu nhấn thống nhất với logo.
- Chuyển động có thể tắt và không làm thay đổi dữ liệu hoặc model state.
- Biểu đồ có tooltip, chú thích và khoảng đệm an toàn.
- Không hiển thị nhãn hoặc xác suất gian lận giả khi chưa có model thật.
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
