# Phase 06 — Demo UI (Streamlit)

**Owner:** Phạm Thành Trung

**Status:** `pending`

**Updated:** 29/08/2026

**Dependencies:** Phase 04 (model artifacts) và Phase 05 (model comparison/figures)

## Mục tiêu

Xây dựng giao diện Streamlit để nhập một giao dịch PaySim, trực quan hóa tín hiệu đầu vào và trình bày kết quả mô hình khi artifacts thật được bàn giao.

## Phạm vi của Trung

| Hạng mục | Trạng thái | Kết quả hiện tại |
|----------|------------|------------------|
| Wireframe và nhận diện UI | ✅ Hoàn thành | Signal Universe, custom logo, System/Sáng/Tối, responsive layout |
| Form giao dịch | ✅ Hoàn thành | Đủ 7 trường PaySim, validation và 3 quick presets |
| Trực quan dữ liệu đầu vào | ✅ Hoàn thành | Bản đồ tín hiệu, Dòng tiền, Sai lệch số dư và biểu đồ phân bố nhãn thật |
| Safe-preview | ✅ Hoàn thành | Không hiển thị nhãn hoặc xác suất gian lận giả khi chưa có model |
| Theme switcher | 🟡 Đã triển khai | Lưu theme native v2 của Streamlit; chờ click và pixel QA System/Sáng/Tối |
| Model inference | ⏳ Chờ | Cần model được chọn từ Phase 04–05 |
| Model results/figures | ⏳ Chờ | Cần comparison table và figures từ Phase 05 |
| Demo evidence | ⏳ Chờ | Cần screenshot hiện tại và demo clip sau khi tích hợp model |

## Deliverables

```text
draft/fraud-detection/demo/
├── app.py
├── requirements-demo.txt
├── .streamlit/config.toml
├── WIREFRAME.md
├── assets/
└── screenshots/
```

## Trạng thái Revision 7.7

- Nút **Giao diện** nằm gọn ở góc trái dưới và mở ba lựa chọn System/Sáng/Tối.
- Theme được ghi trực tiếp theo cơ chế lưu native v2 của Streamlit rồi reload; không phụ thuộc menu DOM.
- Toolbar dùng chế độ `minimal`, không hiển thị menu ba chấm góc phải.
- Ba biểu đồ preview có vùng vẽ và khoảng đệm an toàn.
- Giao diện tiếp tục khóa inference cho đến khi có model thật.

## 💡 Ý tưởng Đề xuất & Cải tiến Nâng cao (từ MY_IDEAS)

1. **Thanh trượt điều chỉnh ngưỡng quyết định linh hoạt (Threshold Slider $0.1 \rightarrow 0.9$):**
   * Cho phép chuyên viên tài chính kéo thanh trượt `st.slider` để thay đổi Decision Threshold.
   * Hiển thị biểu đồ tương tác thời gian thực: Khi hạ ngưỡng (ví dụ từ $0.5 \rightarrow 0.2$), tỷ lệ phát hiện gian lận (Recall) tăng lên bao nhiêu vs số lượng cảnh báo nhầm (False Positive) tăng bao nhiêu.
2. **Minh bạch hóa AI với SHAP (Explainable AI Waterfall Plot):**
   * Khi tích hợp model thật (XGBoost/RF), tích hợp biểu đồ **SHAP** để giải thích cho từng giao dịch: *"Tại sao giao dịch này bị gắn cờ là gian lận?"* (Ví dụ: `errorBalanceOrig` đóng góp +45% rủi ro, `amount` đóng góp +30%, `hour_of_day=2h` đóng góp +15%).
3. **Mô phỏng dòng giao dịch thời gian thực (Real-time Transaction Simulation):**
   * Bổ sung chế độ Stream simulation tự động đẩy các giao dịch mẫu từ tập test set theo chu kỳ 1 giây/giao dịch, tự động kích hoạt hiệu ứng còi/chuông cảnh báo khi phát hiện giao dịch có xác suất gian lận cao.

## Evidence đã xác minh

| Kiểm tra | Kết quả | Giới hạn xác nhận |
|----------|---------|-------------------|
| Python compile và dependencies | `py_compile` đạt; `pip check` không có dependency hỏng | Môi trường local Python 3.14 |
| App regression | 4 luồng AppTest, `0 exceptions` | Presets, form, motion và preview |
| Theme implementation | Direct native-theme storage; legacy menu bridge đã loại bỏ; toolbar `minimal` | Chưa thay thế click/pixel QA trên trình duyệt |
| Runtime | Root `200`; health `200 ok` ngày 29/08/2026 | Local runtime tại thời điểm kiểm tra |
| Visual safety | Contrast và spacing của 3 preview đạt kiểm tra hiện có | Cần ảnh Revision 7.7 để duyệt cuối |

## Acceptance Criteria

- [x] App khởi động không lỗi.
- [x] Form và safe-preview hoạt động với dữ liệu đầu vào.
- [x] Không tạo kết quả mô hình giả.
- [x] Có ba chế độ System/Sáng/Tối và không hiện menu native góc phải.
- [ ] Click và pixel QA System/Sáng/Tối trên trình duyệt.
- [ ] Model thật trả nhãn và probability.
- [ ] Comparison table và model figures hiển thị đúng.
- [ ] Screenshot hiện tại và demo clip được lưu trong thư mục demo.

## Cách chạy

Từ `draft/fraud-detection`:

```powershell
py -3.14 -m pip install -r demo/requirements-demo.txt
py -3.14 -m streamlit run demo/app.py
```

## Việc tiếp theo của Trung

1. Click và review pixel Revision 7.7 ở System/Sáng/Tối.
2. Nhận model/comparison artifacts từ Phase 04–05 và tích hợp inference thật.
3. Kiểm tra luồng nhập → dự đoán → giải thích kết quả.
4. Chụp screenshot và quay demo clip.

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

UI shell Revision 7.7 đã sẵn sàng cho bước browser QA và tích hợp model. Phase 06 vẫn `pending` cho đến khi hoàn tất inference thật, figures và demo evidence.
