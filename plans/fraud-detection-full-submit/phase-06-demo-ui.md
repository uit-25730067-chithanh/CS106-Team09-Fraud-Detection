# Phase 06 — Demo UI (Streamlit)

**Owner:** Phạm Thành Trung

**Status:** `pending`

**Updated:** 05/09/2026

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
| Theme switcher | ✅ Hoàn thành | Browser QA đã xác nhận System/Sáng/Tối, mặc định Tối và chuyển theme không reload trang |
| Model inference | ✅ Hoàn thành checkpoint | XGBoost-SMOTE JSON + scaler, 14-feature contract, probability và nhãn thật |
| Mẫu kiểm thử có nhãn | ✅ Hoàn thành | Nạp mẫu từ X_test, đối chiếu nhãn thật với dự đoán và thể hiện đúng/sai |
| Model results/figures | 🟡 Adapter hoàn thành | Đã validate/render CSV + 5 figures; chờ artifacts chính thức từ Phase 05 |
| Demo evidence | 🟡 Đã có kịch bản | Quy ước 5 screenshots + clip 2–3 phút; chờ artifacts Phase 05 để ghi hình bản cuối |

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
- Màn hình Hiệu năng tự đọc `model_comparison.csv` và 5 figures đúng contract Phase 05.
- CSV sai schema, thiếu mô hình hoặc metric ngoài `[0, 1]` bị chặn fail-closed.
- UI giữ placeholder trung thực khi Phase 05 chưa bàn giao artifacts.
- Kịch bản quay demo 2–3 phút và quy ước tên evidence đã được chuẩn hóa.

## Evidence đã xác minh

| Kiểm tra | Kết quả | Giới hạn xác nhận |
|----------|---------|-------------------|
| Python compile và dependencies | `py_compile` đạt; `pip check` không có dependency hỏng | Môi trường local Python 3.14 |
| Demo test suite | `13 passed` | Inference, artifact contract và regression cho 3 màn hình |
| Toàn bộ test hiện có | `21 passed` | Chạy từ `draft/fraud-detection` trên Python 3.14 |
| Streamlit AppTest | `0 exceptions` | Phân tích giao dịch, Hiệu năng mô hình và Lịch sử phân tích |
| Phase 05 adapter | PASS với fixture | Nhận schema title-case/snake_case, sort F1, validate 3 models × 5 metrics và dò 5 PNG |
| Xác suất preset | `0,00%`; `0,70%`; `16,67%`; `100,00%` | Kết quả local từ XGBoost-SMOTE, làm tròn 2 chữ số trên UI |
| Browser QA | PASS System/Sáng/Tối ngày 05/09/2026 | Kiểm tra trực quan và thao tác bằng Playwright; 0 browser errors, mặc định Tối, chuyển theme không reload trang |
| Runtime | Health endpoint trả `ok` tại `localhost:8501` ngày 05/09/2026 | Local runtime tại thời điểm kiểm tra |

## Acceptance Criteria

- [x] App khởi động không lỗi.
- [x] Form và safe-preview hoạt động với dữ liệu đầu vào.
- [x] Không tạo kết quả mô hình giả.
- [x] Có ba chế độ System/Sáng/Tối và không hiện menu native góc phải.
- [ ] Click và pixel QA System/Sáng/Tối trên trình duyệt.
- [x] Model thật trả nhãn và probability.
- [x] UI có adapter fail-closed để nhận comparison CSV và 5 figures Phase 05.
- [x] Browser QA System/Sáng/Tối, theme mặc định Tối và chuyển theme không reload.
- [ ] Comparison table và model figures hiển thị đúng.
- [ ] Screenshot hiện tại và demo clip được lưu trong thư mục demo.

## Cách chạy

Từ `draft/fraud-detection`:

```powershell
py -3.14 -m pip install -r demo/requirements-demo.txt
py -3.14 -m streamlit run demo/app.py
```

## Việc tiếp theo của Trung

1. Nhận comparison table/figures và kết luận model chính thức từ Phase 05; adapter UI đã sẵn sàng.
2. Render và QA lại màn hình Hiệu năng sau khi nhận artifacts chính thức.
3. Chụp screenshots hiện tại và quay demo clip.

## Rủi ro và kiểm soát

| Rủi ro | Kiểm soát |
|--------|-----------|
| Model hoặc schema đầu vào không khớp | Validate feature order, scaler, CSV metrics và tên figures trước khi hiển thị |
| Theme thay đổi khi nâng Streamlit | Giữ phiên bản tối thiểu đã kiểm tra và chạy lại browser QA sau khi nâng |
| Tài liệu vượt quá trạng thái thực tế | Giữ Phase 06 `pending` cho đến khi đủ model, figures và demo evidence |

## Tuân thủ quy tắc project

- Chỉ cập nhật công việc của Phạm Thành Trung/Phase 06.
- Phase chưa hoàn thành nên không đổi trạng thái sang `passed`.
- Không cập nhật `Final/README.md` vì trạng thái Sprint chung chưa thay đổi.
- Không tạo hoặc thay đổi artifacts dữ liệu/model.
- Checkpoint tích hợp model đã được commit trên branch Phase 06.

## Kết luận

Phần Phase 06 tự chủ đã hoàn tất: UI, XGBoost inference, mẫu test có nhãn, adapter kết quả Phase 05 và Browser QA đều đã có evidence. Phase vẫn `pending` do chưa có artifacts chính thức Phase 05, screenshots hiện tại và demo clip.
