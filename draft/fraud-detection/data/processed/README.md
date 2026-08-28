# Dữ liệu đã xử lý — `data/processed/`

> **Dành cho tất cả thành viên nhóm — kể cả người không lập trình.**

---

## Các file trong thư mục này là gì?

| File | Kích thước | Nội dung |
|------|-----------|---------|
| `X_train.pkl` | ~12 MB | **Features (đặc trưng) tập huấn luyện** — 160,000 giao dịch × 9 thuộc tính, đã được chuẩn hóa và mã hóa |
| `X_test.pkl` | ~3 MB | **Features tập kiểm tra** — 40,000 giao dịch × 9 thuộc tính |
| `y_train.pkl` | ~4 MB | **Nhãn tập huấn luyện** — 160,000 giá trị (0 = bình thường, 1 = gian lận) |
| `y_test.pkl` | ~1 MB | **Nhãn tập kiểm tra** — 40,000 giá trị |

> **`.pkl`** là định dạng file nhị phân của Python (pickle). Không mở bằng Excel hay Word — chỉ đọc được bằng Python.

---

## Dữ liệu này đến từ đâu?

```
paysim.csv (6.36 triệu giao dịch, ~500MB)
    │
    ├── Lọc: Chỉ giữ giao dịch TRANSFER và CASH_OUT
    │         (Fraud chỉ xảy ra ở 2 loại này)
    │
    ├── Downsampling: Giảm xuống ~200,000 dòng
    │         (Giữ toàn bộ 8,213 mẫu gian lận)
    │
    ├── Tạo thêm 2 đặc trưng mới:
    │     errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig
    │     errorBalanceDest = oldbalanceDest + amount - newbalanceDest
    │
    ├── Chia tập: 80% train / 20% test (stratified — giữ nguyên tỷ lệ fraud)
    │
    └── Chuẩn hóa: StandardScaler fit trên train, transform cả 2 tập
```

---

## 9 thuộc tính (cột) trong X_train / X_test

| # | Tên cột | Ý nghĩa | Đã xử lý? |
|---|---------|---------|-----------|
| 1 | `step` | Thời điểm giao dịch (giờ) | Đã scale |
| 2 | `amount` | Số tiền giao dịch | Đã scale |
| 3 | `oldbalanceOrg` | Số dư nguồn trước giao dịch | Đã scale |
| 4 | `newbalanceOrig` | Số dư nguồn sau giao dịch | Đã scale |
| 5 | `oldbalanceDest` | Số dư đích trước giao dịch | Đã scale |
| 6 | `newbalanceDest` | Số dư đích sau giao dịch | Đã scale |
| 7 | `errorBalanceOrig` | **[Tạo mới]** Chênh lệch số dư nguồn | Đã scale |
| 8 | `errorBalanceDest` | **[Tạo mới]** Chênh lệch số dư đích | Đã scale |
| 9 | `type_TRANSFER` | Loại giao dịch (1=TRANSFER, 0=CASH_OUT) | One-Hot Encoding |

> Các cột đã bị **loại bỏ**: `nameOrig`, `nameDest` (ID tài khoản — không có giá trị dự báo), `isFlaggedFraud` (chỉ có 16 giao dịch được gắn cờ trong 6.36M — quá thưa thớt)

---

## Số liệu thực tế sau xử lý

| Chỉ số | Giá trị |
|--------|---------|
| Tổng sau downsample | 200,000 giao dịch |
| Tập train (80%) | 160,000 giao dịch |
| Tập test (20%) | 40,000 giao dịch |
| Số giao dịch gian lận trong train | ~6,570 (~4.1%) |
| Số giao dịch gian lận trong test | ~1,643 (~4.1%) |
| Tỷ lệ fraud giữ nguyên (stratified) | `y_train.mean() ≈ y_test.mean() ≈ 0.041` |

---

## Dành cho Sơn (Phase 02 — SMOTE/ADASYN)

```python
import pickle

with open("data/processed/X_train.pkl", "rb") as f:
    X_train = pickle.load(f)
with open("data/processed/y_train.pkl", "rb") as f:
    y_train = pickle.load(f)

print(X_train.shape)   # → (160000, 9)
print(y_train.mean())  # → ~0.041 (tỷ lệ fraud)
```

> ⚠️ **QUAN TRỌNG:** Chỉ apply SMOTE/ADASYN trên `X_train`/`y_train`. **Không được** dùng trên `X_test`/`y_test`.

---

## Dành cho Trung (Demo UI)

```python
import pickle

# Load scaler đã được fit sẵn (trong models/)
with open("models/scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

# Khi user nhập giao dịch mới → tính errorBalance trước → rồi scale
new_tx = {...}  # dict chứa thông tin giao dịch
new_tx["errorBalanceOrig"] = new_tx["oldbalanceOrg"] - new_tx["amount"] - new_tx["newbalanceOrig"]
new_tx["errorBalanceDest"] = new_tx["oldbalanceDest"] + new_tx["amount"] - new_tx["newbalanceDest"]
# Sau đó scale và predict
```

---

## Không cần chạy lại preprocessing nếu...

Các file `.pkl` đã có trong git. Chỉ cần `git pull` là đủ. **Không cần** cài venv hay chạy script để có dữ liệu này.

Nếu muốn **tạo lại từ đầu** (cần có `paysim.csv`):
```bash
cd draft/fraud-detection
source .venv/bin/activate
python run_preprocessing.py
```

---

*Tạo bởi: Đặng Chí Thanh — Phase 01 EDA & Preprocessing — 28/08/2026*
