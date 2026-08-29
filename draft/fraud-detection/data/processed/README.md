# Dữ liệu đã xử lý — `data/processed/`

> **Dành cho tất cả thành viên nhóm — kể cả người không lập trình.**

---

## Các file trong thư mục này là gì?

| File | Kích thước | Nội dung |
|------|-----------|---------|
| `X_train.pkl` | ~18 MB | **Features (đặc trưng) tập huấn luyện** — 160,000 giao dịch × 14 thuộc tính, đã được chuẩn hóa và mã hóa |
| `X_test.pkl` | ~4.5 MB | **Features tập kiểm tra** — 40,000 giao dịch × 14 thuộc tính |
| `y_train.pkl` | ~3.8 MB | **Nhãn tập huấn luyện** — 160,000 giá trị (0 = bình thường, 1 = gian lận) |
| `y_test.pkl` | ~1 MB | **Nhãn tập kiểm tra** — 40,000 giá trị |

> **`.pkl`** là định dạng file nhị phân của Python (pickle). Không mở bằng Excel hay Word — chỉ đọc được bằng Python.

---

## Dữ liệu này đến từ đâu?

### Sơ đồ luồng xử lý dữ liệu

```
 ┌─────────────────────────────────────────────────────────────────┐
 │  📥 NGUỒN: paysim.csv  (6,362,620 giao dịch — ~500MB)          │
 │  Tải từ Kaggle. KHÔNG commit lên git (quá nặng)                │
 └───────────────────────────┬─────────────────────────────────────┘
                             │
                    [ data_loader.py ]
                             │
              ┌──────────────▼──────────────┐
              │   LỌC loại giao dịch        │
              │   Chỉ giữ: TRANSFER &       │
              │   CASH_OUT (fraud chỉ xảy   │
              │   ra ở 2 loại này)          │
              └──────────────┬──────────────┘
                             │
              ┌──────────────▼──────────────┐
              │   DOWNSAMPLE xuống ~200,000 │
              │   Giữ TOÀN BỘ 8,213 fraud  │
              │   Lấy ngẫu nhiên normal     │
              └──────────────┬──────────────┘
                             │
                   [ data_splitter.py ]
                             │
              ┌──────────────▼──────────────┐
              │   CHIA TẬP (Stratified)     │
              │   80% Train — 20% Test      │
              │   Tỷ lệ fraud giữ đều nhau  │
              └──────┬───────────────┬──────┘
                     │               │
               [TRAIN SET]     [TEST SET]
               160,000 dòng    40,000 dòng
                     │               │
                    [ feature_scaler.py ]
                     │               │
         ┌───────────▼───┐   ┌───────▼───────┐
         │ Feature       │   │ Feature       │
         │ Engineering   │   │ Engineering   │
         │ (tạo 7 cột    │   │ (tạo 7 cột    │
         │ đặc trưng mới)│   │ đặc trưng mới)│
         │               │   │               │
         │ StandardScaler│   │ .transform()  │
         │ .fit_transform│   │ CHỈ transform │
         │ (FIT Ở ĐÂY)   │   │ KHÔNG fit lại │
         └───────┬───────┘   └───────┬───────┘
                 │                   │
                 ▼                   ▼
    ┌────────────────────┐  ┌────────────────────┐
    │  X_train.pkl ✅    │  │  X_test.pkl  ✅    │
    │  y_train.pkl ✅    │  │  y_test.pkl  ✅    │
    │  (160,000 × 14)    │  │  (40,000 × 14)     │
    └────────────────────┘  └────────────────────┘
              +
    ┌────────────────────┐
    │  scaler.pkl  ✅    │  ← Dùng khi predict giao dịch mới
    │  (models/)         │    trong Demo UI
    └────────────────────┘

  ✅ = Đã commit lên git. Chỉ cần git pull là có ngay.
```

### Bước xử lý chi tiết

```
paysim.csv (6.36 triệu giao dịch, ~500MB)
    │
    ├── Lọc: Chỉ giữ giao dịch TRANSFER và CASH_OUT
    │         (Fraud chỉ xảy ra ở 2 loại này)
    │
    ├── Downsampling: Giảm xuống ~200,000 dòng
    │         (Giữ toàn bộ 8,213 mẫu gian lận)
    │
    ├── Tạo 7 đặc trưng mới (Phase 01 + Phase 01b):
    │     errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig
    │     errorBalanceDest = oldbalanceDest + amount - newbalanceDest
    │     is_drain_account = (oldbalanceOrg > 0) & (newbalanceOrig == 0)
    │     hour_of_day = step % 24
    │     is_night_transaction = hour_of_day < 6
    │     amount_to_oldbalance_ratio = amount / (oldbalanceOrg + 1e-5)
    │     is_large_transaction = amount > 200,000
    │
    ├── Chia tập: 80% train / 20% test (stratified — giữ nguyên tỷ lệ fraud)
    │
    └── Chuẩn hóa: StandardScaler fit trên train, transform cả 2 tập
```

---

## 14 thuộc tính (cột) trong X_train / X_test

| # | Tên cột | Ý nghĩa | Loại & Xử lý |
|---|---------|---------|--------------|
| 1 | `step` | Thời điểm giao dịch (giờ giả lập) | Số liên tục — Đã scale |
| 2 | `amount` | Số tiền giao dịch | Số liên tục — Đã scale |
| 3 | `oldbalanceOrg` | Số dư nguồn trước giao dịch | Số liên tục — Đã scale |
| 4 | `newbalanceOrig` | Số dư nguồn sau giao dịch | Số liên tục — Đã scale |
| 5 | `oldbalanceDest` | Số dư đích trước giao dịch | Số liên tục — Đã scale |
| 6 | `newbalanceDest` | Số dư đích sau giao dịch | Số liên tục — Đã scale |
| 7 | `is_drain_account` | **[Tạo mới 01b]** Rút cạn tài khoản nguồn | Cờ nhị phân (0/1) |
| 8 | `hour_of_day` | **[Tạo mới 01b]** Giờ giao dịch trong ngày (0–23) | Số liên tục — Đã scale |
| 9 | `is_night_transaction` | **[Tạo mới 01b]** Giao dịch ban đêm (0h–5h) | Cờ nhị phân (0/1) |
| 10 | `amount_to_oldbalance_ratio` | **[Tạo mới 01b]** Tỉ lệ tiền gửi / số dư gốc | Số liên tục — Đã scale |
| 11 | `is_large_transaction` | **[Tạo mới 01b]** Giao dịch lớn (> 200k) | Cờ nhị phân (0/1) |
| 12 | `errorBalanceOrig` | **[Tạo mới 01]** Chênh lệch số dư nguồn | Số liên tục — Đã scale |
| 13 | `errorBalanceDest` | **[Tạo mới 01]** Chênh lệch số dư đích | Số liên tục — Đã scale |
| 14 | `type_TRANSFER` | Loại giao dịch (1=TRANSFER, 0=CASH_OUT) | One-Hot Encoding (0/1) |

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

print(X_train.shape)   # → (160000, 14)
print(y_train.mean())  # → ~0.041 (tỷ lệ fraud)
```

> ⚠️ **QUAN TRỌNG:**
> 1. Chỉ apply SMOTE/ADASYN trên `X_train`/`y_train`. **Không được** dùng trên `X_test`/`y_test`.
> 2. Các cờ nhị phân (`is_drain_account`, `is_night_transaction`, `is_large_transaction`, `type_TRANSFER`) nên được xử lý bằng `SMOTENC` hoặc làm tròn nhị phân `np.round()` sau khi oversample để bảo toàn dạng giá trị 0/1.

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
