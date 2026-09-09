# Phase 06 — Demo UI (Streamlit)

**Owner:** Phạm Thành Trung

**Status:** `pending`

**Updated:** 09/09/2026

**Dependencies:** Phase 04 (model artifacts) và Phase 05 (model comparison/figures)

## Mục tiêu

Xây dựng giao diện Streamlit để nhập một giao dịch PaySim, trực quan hóa tín hiệu đầu vào và trình bày kết quả mô hình khi artifacts thật được bàn giao.

## Phạm vi của Trung

| Hạng mục | Trạng thái | Kết quả hiện tại |
|----------|------------|------------------|
| Wireframe và nhận diện UI | ✅ Hoàn thành | Signal Universe, custom logo, System/Sáng/Tối, responsive layout |
| Form giao dịch | ✅ Hoàn thành | Đủ 7 trường PaySim, validation, 4 quick presets, định dạng tiền VNĐ & mapping thời gian (PR #27) |
| Trực quan dữ liệu đầu vào | ✅ Hoàn thành | Bản đồ tín hiệu, Dòng tiền, Sai lệch số dư và biểu đồ phân bố nhãn thật |
| Inference fail-closed | ✅ Hoàn thành | Không suy đoán kết quả nếu model/scaler/schema lỗi |
| Theme switcher | ✅ Hoàn thành | Browser QA đã xác nhận System/Sáng/Tối, mặc định Tối và chuyển theme không reload trang |
| Model inference | ✅ Hoàn thành checkpoint | XGBoost-SMOTE JSON + scaler, 14-feature contract, probability và nhãn thật |
| Mẫu kiểm thử có nhãn | ✅ Hoàn thành | Nạp mẫu từ X_test, đối chiếu nhãn thật với dự đoán và thể hiện đúng/sai |
| Model results/figures | ✅ Hoàn thành | Đã render comparison CSV + 9 biểu đồ độc lập; có chuyển SMOTENC/ADASYN, Feature Importance và so sánh TP/FP/FN |
| Demo evidence | 🟡 Đang hoàn thiện | Đã chuẩn hóa `demo/DEMO-SCRIPT.md` và Browser QA bố cục mới đạt; còn lưu 5 screenshots và quay clip 2–3 phút |

## Deliverables

```text
draft/fraud-detection/
├── .streamlit/config.toml
└── demo/
    ├── app.py
    ├── DEMO-SCRIPT.md
    ├── evaluation_artifacts.py
    ├── inference.py
    ├── requirements-demo.txt
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
- Màn hình Hiệu năng tự đọc `model_comparison.csv` và 9 biểu đồ độc lập đúng contract Phase 05/báo cáo.
- Ma trận Random Forest/XGBoost chuyển được giữa `SMOTENC • Chính thức` và `ADASYN • Đối chứng`; Autoencoder hiển thị riêng.
- Đã bổ sung `feature_importance_comparison.png` và `confusion_matrix_components.png`.
- CSV sai schema, thiếu mô hình hoặc metric ngoài `[0, 1]` bị chặn fail-closed.
- UI giữ placeholder trung thực khi Phase 05 chưa bàn giao artifacts.
- Kịch bản quay demo 2–3 phút và quy ước tên evidence đã được chuẩn hóa.

## Evidence đã xác minh

| Kiểm tra | Kết quả | Giới hạn xác nhận |
|----------|---------|-------------------|
| Python compile và dependencies | `py_compile` đạt; `pip check` không có dependency hỏng | Môi trường local Python 3.14 |
| Demo test suite | `45 passed` | Inference, artifact contract, chuyển SMOTENC/ADASYN, lịch sử SQLite và regression cho 3 màn hình |
| Toàn bộ test hiện có | `87 passed` | Chạy từ repository trên Python 3.14 ngày 09/09/2026 |
| Streamlit AppTest | `0 exceptions` | Hiển thị 7 hình trong một chế độ (9 artifact tổng), chuyển ADASYN và giữ Autoencoder |
| Phase 05 adapter | PASS với artifact thật | Validate 5 biến thể × 5 metrics và dò đủ 9 PNG độc lập |
| Xác suất preset | `0,00%`; `0,70%`; `16,67%`; `100,00%` | Kết quả local từ XGBoost-SMOTE, làm tròn 2 chữ số trên UI |
| Browser QA | PASS System/Sáng/Tối ngày 05/09/2026 | Kiểm tra trực quan và thao tác bằng Playwright; 0 browser errors, mặc định Tối, chuyển theme không reload trang |
| Runtime | Health endpoint trả `ok` tại `localhost:8501` ngày 09/09/2026 | Browser QA bố cục Hiệu năng và Lịch sử mới đạt trên giao diện Sáng/Tối; 0 console errors |

## Acceptance Criteria

- [x] App khởi động không lỗi.
- [x] Form và safe-preview hoạt động với dữ liệu đầu vào.
- [x] Không tạo kết quả mô hình giả.
- [x] Có ba chế độ System/Sáng/Tối và không hiện menu native góc phải.
- [x] Click và pixel QA bố cục mới trên System/Sáng/Tối.
- [x] Model thật trả nhãn và probability.
- [x] UI có adapter fail-closed để nhận comparison CSV và 9 figures Phase 05/báo cáo.
- [x] Browser QA System/Sáng/Tối, theme mặc định Tối và chuyển theme không reload.
- [x] Comparison table và model figures hiển thị đúng qua AppTest, gồm SMOTENC/ADASYN, Feature Importance và TP/FP/FN.
- [ ] Lưu đủ 5 screenshots và demo clip 2–3 phút trong thư mục `demo/`.

## Cách chạy

Từ `draft/fraud-detection`:

```powershell
py -3.14 -m pip install -r demo/requirements-demo.txt
py -3.14 -m streamlit run demo/app.py
```

## Việc tiếp theo của Trung

1. Chụp 5 ảnh screenshots UI (System, Sáng, Tối, Form nhập liệu, Hiệu năng mô hình) và lưu vào `demo/screenshots/`.
2. Quay video demo clip 2–3 phút theo `demo/DEMO-SCRIPT.md`.
3. Hoàn tất đóng gói Phase 06 và chuyển trạng thái sang `passed`.

## Rủi ro và kiểm soát

| Rủi ro | Kiểm soát |
|--------|-----------|
| Model hoặc schema đầu vào không khớp | Validate feature order, scaler, CSV metrics và tên figures trước khi hiển thị |
| Theme thay đổi khi nâng Streamlit | Giữ phiên bản tối thiểu đã kiểm tra và chạy lại browser QA sau khi nâng |
| Tài liệu vượt quá trạng thái thực tế | Giữ Phase 06 `pending` cho đến khi đủ screenshots và demo clip |

## Tuân thủ quy tắc project

- Chỉ cập nhật công việc của Phạm Thành Trung/Phase 06.
- Phase chưa hoàn thành nên không đổi trạng thái sang `passed`.
- Checkpoint tích hợp model và cải tiến UX đã được commit trên main.

## Kết luận

Phần chức năng của Phase 06 đã hoàn tất: UI, XGBoost inference, mẫu test có nhãn, mapping datetime PaySim, định dạng tiền VNĐ, comparison/9 figures, lịch sử SQLite và Browser QA bố cục mới. Phase vẫn giữ trạng thái `pending` cho đến khi bổ sung đủ 5 screenshots và video clip demo.
