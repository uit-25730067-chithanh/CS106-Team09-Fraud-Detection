# Báo cáo Nghiệm thu — Phase 01b — Feature Engineering Enhancements

Tài liệu này tổng hợp toàn bộ các thay đổi kỹ thuật, kết quả xác minh và mô hình phân nhánh Git đã được thực hiện trong Phase 01b.

---

## 1. Nội dung đã thực hiện

### Hiện thực 5 đặc trưng mới (Feature Engineering)
Đã cập nhật logic trong file `src/preprocessing/feature_scaler.py` để tính toán 5 đặc trưng mới trên tập Train và Test trước khi thực hiện Scaling:
- **`is_drain_account`** (Binary flag): `(oldbalanceOrg > 0) & (newbalanceOrig == 0)` (cast sang `int`). Nhận diện các giao dịch rút cạn tài khoản nguồn (tín hiệu gian lận cực mạnh).
- **`hour_of_day`** (Continuous): `step % 24` (cast sang `int`). Chu kỳ thời gian theo giờ trong ngày (0–23).
- **`is_night_transaction`** (Binary flag): `hour_of_day < 6` (cast sang `int`). Đánh dấu các giao dịch đáng ngờ vào ban đêm (0h–5h).
- **`amount_to_oldbalance_ratio`** (Continuous): `amount / (oldbalanceOrg + 1e-5)` (safety constant `1e-5` để tránh division-by-zero). Tỉ lệ số tiền giao dịch trên số dư hiện tại của tài khoản nguồn.
- **`is_large_transaction`** (Binary flag): `amount > 200,000` (cast sang `int`). Giao dịch có giá trị lớn vượt ngưỡng 200k.

### Cấu hình Standard Scaling
- Đã đưa 2 continuous features mới (`hour_of_day`, `amount_to_oldbalance_ratio`) vào danh sách `SCALE_COLS` để được fit/transform qua `StandardScaler`.
- Giữ nguyên các binary flags (`is_*`) bên ngoài `SCALE_COLS` để tránh làm biến dạng tính phân tách nhị phân (0/1).

### Cập nhật Pipeline Preprocessing
- Thay đổi các assertion kiểm tra số lượng cột dữ liệu đầu ra từ `9` lên `14` cột trong file `run_preprocessing.py`.
- Thực thi toàn bộ pipeline tái tạo dữ liệu, ghi đè thành công các tập pickle dữ liệu đã qua xử lý (`X_train.pkl`, `X_test.pkl`, `y_train.pkl`, `y_test.pkl`) và bộ scaler (`models/scaler.pkl`).

---

## 2. Kết quả Xác minh Dữ liệu (Verification)

Sau khi chạy lại pipeline, dữ liệu đã được xác minh toàn vẹn qua các tiêu chí sau:

- **Kích thước Ma trận (Shapes Check):**
  - `X_train` shape: `(160000, 14)` (Tăng từ 9 lên 14 cột, dòng giữ nguyên) -> **ĐẠT**
  - `X_test` shape: `(40000, 14)` -> **ĐẠT**
- **Giá trị khuyết thiếu (NaN Check):**
  - Số lượng NaN/Null = `0` trên cả hai tập Train/Test -> **ĐẠT**
- **Tỉ lệ Nhãn (Fraud Ratios):**
  - Train set: `0.0410625` (~4.1%)
  - Test set: `0.0410750` (~4.1%)
  - Stratified split giữ nguyên phân phối nhãn của PaySim -> **ĐẠT**
- **Logic của đặc trưng `is_drain_account`:**
  - Tỉ lệ rút cạn tài khoản trong tập Fraud: **97.56%**
  - Tỉ lệ rút cạn tài khoản trong tập Normal: **42.71%**
  - Tỉ lệ rút cạn tài khoản ở các giao dịch gian lận cao gấp **2.28 lần** so với giao dịch thông thường -> **ĐẠT**

---

## 3. Khảo sát chất lượng & Khuyến nghị bổ sung (Code Review Findings)

Qua phân tích phân phối thực tế của đặc trưng `amount_to_oldbalance_ratio` trước và sau khi scaling, em phát hiện một điểm cần lưu ý:
- **Hiện tượng**: Khi tài khoản nguồn có số dư ban đầu `oldbalanceOrg` bằng 0, mẫu số cộng thêm `1e-5` khiến giá trị tỉ lệ tăng vọt (lên tới $9.24 \times 10^{12}$). 
- **Ảnh hưởng**: Sau khi đi qua Standard Scaling, giá trị max bị đẩy lên tới $120$ std, trong khi giá trị median bị nén chặt về $-0.2$. Sự phân phối lệch cực đoan (skewed) này có thể gây mất ổn định số học trong quá trình huấn luyện các mô hình Linear hoặc Neural Networks (không ảnh hưởng tới các mô hình Tree như XGBoost/LightGBM).
- **Khuyến nghị cho Phase sau**: Cân nhắc áp dụng log-transform hoặc clip trần tỉ lệ giao dịch này:
  `df["amount_to_oldbalance_ratio"] = np.log1p(df["amount"] / (df["oldbalanceOrg"] + 1e-5))`

---

## 4. Mô hình Phân nhánh Git đã áp dụng

Tuân thủ quy trình phân nhánh và bảo vệ nhánh chính:
- Toàn bộ thay đổi của Phase 01b (code, data pickle, scaler pickle, report, plans) được cam kết và đẩy lên nhánh tính năng riêng: **`feat/phase-01b-feature-engineering`**.
- Nhánh `main` từ xa (remote main) được khôi phục nguyên trạng về commit sạch `95f0ffd`.
- Các commits trên nhánh tính năng được gộp (squash) gọn gàng thành **1 commit duy nhất** (`99b502f`).
