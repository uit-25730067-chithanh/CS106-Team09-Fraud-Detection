# Phase 01 — Implement Features trong `feature_scaler.py`

**Parent plan:** [plan.md](./plan.md)
**Depends on:** Phase 01 (EDA & Preprocessing) — `passed` ✅
**Next phase:** [Phase 02 — Re-run Preprocessing](./phase-02-rerun-preprocessing.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Thanh** |
| Priority | P1 |
| Status | `passed` |
| Estimated effort | 30 phút |
| Sprint | Sprint 2 (trước 4/9) |

## Context

File cần sửa: [`draft/fraud-detection/src/preprocessing/feature_scaler.py`](../../draft/fraud-detection/src/preprocessing/feature_scaler.py)

**Logic cần thêm — trước bước Scaling (Step 3):**

| Feature mới | Loại | Vào SCALE_COLS? | Công thức |
|------------|------|----------------|-----------|
| `is_drain_account` | Binary flag | ❌ KHÔNG | `(oldbalanceOrg > 0) & (newbalanceOrig == 0)` |
| `hour_of_day` | Continuous (0–23) | ✅ CÓ | `step % 24` |
| `is_night_transaction` | Binary flag | ❌ KHÔNG | `hour_of_day < 6` |
| `amount_to_oldbalance_ratio` | Continuous | ✅ CÓ | `amount / (oldbalanceOrg + 1e-5)` |
| `is_large_transaction` | Binary flag | ❌ KHÔNG | `amount > 200_000` |

## Key Insights

- `is_drain_account` là signal mạnh nhất — trong PaySim, gần như mọi fraud TRANSFER đều drain account nguồn.
- `is_night_transaction` dùng `hour_of_day < 6` thay vì `.isin()` để tối ưu tốc độ xử lý.
- `amount_to_oldbalance_ratio` cần `+ 1e-5` để tránh division-by-zero khi `oldbalanceOrg = 0`.
- Binary features (`is_*`) KHÔNG đưa vào `SCALE_COLS` để tránh mất tính phân tách nhị phân (0/1).

## Implementation Steps

1. Cập nhật `SCALE_COLS` constant ở đầu file để gộp các continuous features mới.
2. Thêm logic tính toán 5 features mới trong vòng lặp `for df in [X_train, X_test]` trước bước scaling.
3. Cập nhật docstring của hàm `scale_features`.

---

## Checklist

- [x] `SCALE_COLS` đã được cập nhật đúng các biến continuous (bao gồm `hour_of_day`, `amount_to_oldbalance_ratio`).
- [x] Logic tính toán `is_drain_account` sử dụng đúng kiểu `int` (`astype(int)`).
- [x] Logic tính toán `hour_of_day` và `is_night_transaction` đã được viết và ép kiểu về `int`.
- [x] Logic tính toán `amount_to_oldbalance_ratio` có hằng số an toàn `1e-5`.
- [x] Logic tính toán `is_large_transaction` sử dụng ngưỡng `200000` và ép kiểu `int`.
- [x] File `feature_scaler.py` compile không có lỗi cú pháp.

## Success Criteria

| Criterion | Expected | Evidence |
|-----------|---------|---------|
| Syntax Check | Python compile thành công | `python -m py_compile ...` không lỗi |
| SCALE_COLS list | Chỉ chứa continuous features | Checked in code |
| Astype safety | Tất cả các flag binary được lưu dưới dạng `int` (0/1) | Checked in code |

## Evidence Section *(điền sau khi làm)*

```text
Syntax compile: OK
SCALE_COLS updated: ["amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest", "step", "hour_of_day", "amount_to_oldbalance_ratio"]
Binary column types: int (using .astype(int))
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Scale nhầm các cột binary | Thấp | High | Review kỹ danh sách `SCALE_COLS` trước khi chạy |
| Division by zero ở tỉ lệ amount | Cao | Medium | Đã thêm `1e-5` ở mẫu số |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ Hoàn thành

```text
Hoàn thành: 29/08/2026
Người thực hiện: Thanh
Kết quả thực tế:
- Đã thêm thành công 5 features (is_drain_account, hour_of_day, is_night_transaction, amount_to_oldbalance_ratio, is_large_transaction) vào feature_scaler.py.
- SCALE_COLS đã được gộp các continuous features mới.
- Cập nhật assertions trong run_preprocessing.py để nhận diện 14 cột.
Issues gặp phải:
- Không có.
```

## Commit

```bash
# Chỉ add code file, không add data trong phase này
git add draft/fraud-detection/src/preprocessing/feature_scaler.py
```
