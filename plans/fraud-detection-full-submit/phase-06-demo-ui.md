# Phase 06 — Demo UI (Streamlit)

**Owner:** Phạm Thành Trung

**Status:** `pending`

**Updated:** 02/09/2026

**Dependencies:** Phase 04 (model artifacts) và Phase 05 (model comparison/figures)

## Mục tiêu

Xây dựng giao diện Streamlit để nhập một giao dịch PaySim, trực quan hóa tín hiệu đầu vào và trình bày kết quả mô hình khi artifacts thật được bàn giao.

## Phạm vi của Trung

| Hạng mục | Trạng thái | Kết quả hiện tại |
|----------|------------|------------------|
| Wireframe và nhận diện UI | ✅ Hoàn thành | Signal Universe, custom logo, System/Sáng/Tối, responsive layout |
| Form giao dịch | ✅ Hoàn thành | Đủ 7 trường PaySim, validation và 4 quick presets |
| Trực quan dữ liệu đầu vào | ✅ Hoàn thành | Bản đồ tín hiệu, Dòng tiền, Sai lệch số dư và biểu đồ phân bố nhãn thật |
| Inference fail-closed | ✅ Hoàn thành | Không suy đoán kết quả nếu model/scaler/schema lỗi |
| Theme switcher | 🟡 Đã triển khai | Lưu theme native v2 của Streamlit; chờ click và pixel QA System/Sáng/Tối |
| Model inference | ✅ Hoàn thành checkpoint | XGBoost-SMOTE JSON + scaler, 14-feature contract, probability và nhãn thật |
| Model results/figures | ⏳ Chờ | Cần comparison table và figures từ Phase 05 |
| Demo evidence | ⏳ Chờ | Cần screenshot hiện tại và demo clip sau khi tích hợp model |

## Deliverables

```text
draft/fraud-detection/demo/
├── app.py
├── inference.py
├── requirements-demo.txt
├── .streamlit/config.toml
├── WIREFRAME.md
├── assets/
└── screenshots/
```

## Trạng thái tích hợp model

- Đã tải `models/xgb_smote.json` và `models/scaler.pkl` bằng cache resource.
- Đã tái tạo đúng thứ tự 14 đặc trưng từ payload PaySim trước khi inference.
- Đã trả xác suất và nhãn phân loại theo ngưỡng do người dùng chọn.
- Đã khóa fail-closed khi thiếu artifact hoặc sai schema; không tạo kết quả giả.
- XGBoost-SMOTE là model triển khai hiện tại, chờ kết luận chính thức từ Phase 05.

## Evidence đã xác minh

| Kiểm tra | Kết quả | Giới hạn xác nhận |
|----------|---------|-------------------|
| Python compile và dependencies | `py_compile` đạt; `pip check` không có dependency hỏng | Môi trường local Python 3.14 |
| App regression | 9 luồng AppTest, `0 exceptions` | Form mặc định + 4 presets + ngưỡng tùy chỉnh + 3 màn hình sidebar |
| Inference contract | `6 passed` | Feature order 14 cột; 4 preset và phân loại theo ngưỡng |
| Xác suất preset | `0,00%`; `0,70%`; `16,67%`; `100,00%` | Kết quả local từ XGBoost-SMOTE, làm tròn 2 chữ số trên UI |
| Browser QA | Môi trường hiện tại báo không có browser khả dụng ngày 02/09/2026 | Chưa xác nhận pixel hoặc click theme trên trình duyệt thật |
| Runtime | Streamlit khởi động tại `localhost:8501` ngày 02/09/2026 | Local runtime tại thời điểm kiểm tra |

## Acceptance Criteria

- [x] App khởi động không lỗi.
- [x] Form và safe-preview hoạt động với dữ liệu đầu vào.
- [x] Không tạo kết quả mô hình giả.
- [x] Có ba chế độ System/Sáng/Tối và không hiện menu native góc phải.
- [ ] Click và pixel QA System/Sáng/Tối trên trình duyệt.
- [x] Model thật trả nhãn và probability.
- [ ] Comparison table và model figures hiển thị đúng.
- [ ] Screenshot hiện tại và demo clip được lưu trong thư mục demo.

## Cách chạy

Từ `draft/fraud-detection`:

```powershell
py -3.14 -m pip install -r demo/requirements-demo.txt
py -3.14 -m streamlit run demo/app.py
```

## Việc tiếp theo của Trung

1. Click và review System/Sáng/Tối khi có browser QA.
2. Nhận comparison table/figures và quyết định model chính thức từ Phase 05.
3. Chụp screenshot và quay demo clip.

## Rủi ro và kiểm soát

| Rủi ro | Kiểm soát |
|--------|-----------|
| Model hoặc schema đầu vào không khớp | Chỉ tích hợp sau khi xác nhận feature order, scaler và model contract |
| Theme thay đổi khi nâng Streamlit | Giữ phiên bản tối thiểu đã kiểm tra và chạy lại browser QA sau khi nâng |
| Tài liệu vượt quá trạng thái thực tế | Giữ Phase 06 `pending` cho đến khi đủ model, figures và demo evidence |

## Tuân thủ quy tắc project

- Chỉ cập nhật công việc của Phạm Thành Trung/Phase 06.
- Phase chưa hoàn thành nên không đổi trạng thái sang `passed`.
- Không cập nhật `Final/README.md` vì trạng thái Sprint chung chưa thay đổi.
- Không tạo hoặc thay đổi artifacts dữ liệu/model.
- Chưa stage hoặc commit vì chưa có yêu cầu.

## Kết luận

XGBoost-SMOTE và scaler thật đã được tích hợp theo contract 14 đặc trưng, có kiểm thử inference và fail-closed. Phase 06 vẫn `pending` do còn browser QA, figures Phase 05, screenshot và demo clip.
