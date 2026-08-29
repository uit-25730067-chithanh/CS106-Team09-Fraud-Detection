# Phase 03 — Code Review + Verify Evidence

**Parent plan:** [plan.md](./plan.md)
**Depends on:** [Phase 02 — Re-run Preprocessing](./phase-02-rerun-preprocessing.md) — PASSED
**Next phase:** [Phase 04 — PR → Merge → Notify](./phase-04-pr-merge-notify.md)

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

Chạy sanity check script để đảm bảo tính toàn vẹn của dữ liệu sau khi thêm các đặc trưng mới. Đảm bảo shape đạt (160000, 14), không có giá trị NaN, tỉ lệ fraud không thay đổi và các đặc trưng nhị phân hoạt động đúng logic.

## Verification Steps

1. Viết hoặc thực thi script Python để kiểm tra nhanh.
2. Xác minh tỉ lệ phân phối class `isFraud` được giữ nguyên (~0.041).
3. Kiểm tra độ tương quan của `is_drain_account` đối với nhãn fraud (sanity check logic nghiệp vụ).

---

## Checklist

- [x] Viết script hoặc notebook kiểm tra dữ liệu đầu ra.
- [x] Xác minh số lượng cột của `X_train` và `X_test` đúng là `14`.
- [x] Xác minh không có giá trị NaN hoặc Null xuất hiện sau biến đổi.
- [x] Xác minh các cột binary (`is_large_transaction`, `is_drain_account`, `is_night_transaction`) chỉ nhận giá trị `0` hoặc `1`.
- [x] Kiểm tra giá trị trung bình (mean) của `is_drain_account` trên tập fraud lớn hơn nhiều so với tập normal.

## Success Criteria

| Criterion | Expected | Evidence |
|-----------|---------|---------|
| Matrix Shapes | Train shape (160000, 14), Test shape (40000, 14) | Output shape check |
| Integrity Check | NaN count = 0 | Null values sum check |
| Target Consistency | Tỉ lệ fraud của Train và Test xấp xỉ nhau (~0.041) | Mean check |
| Feature Logic | `is_drain_account` trên tập fraud >> tập normal | Tỉ lệ kiểm tra logic |

## Evidence Section *(điền sau khi làm)*

```text
Shapes Check:
- X_train: (160000, 14)
- X_test: (40000, 14)

NaN / Null Count: 0

Fraud ratios:
- Train set: 0.0410625
- Test set: 0.041075

is_drain_account validation:
- Fraud group mean: 0.975647
- Normal group mean: 0.427061
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Tỉ lệ fraud bị lệch do sampling lỗi | Thấp | High | Sử dụng stratified split với `stratify=y` và seed cố định |
| Leakage thông tin từ Test sang Train | Thấp | High | StandardScaler chỉ dùng `fit_transform` trên Train và `transform` trên Test |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ Hoàn thành

```text
Hoàn thành: 29/08/2026
Người thực hiện: Thanh
Kết quả thực tế:
- Đã xác minh thành công số lượng cột là 14 (bao gồm 5 features mới).
- Không có NaN/Null value nào.
- Tỉ lệ class isFraud đạt đúng yêu cầu (~0.041).
- is_drain_account trên tập fraud (97.56%) lớn hơn rất nhiều so với tập normal (42.71%).
Issues gặp phải:
- Không có.
```

## Commit

```bash
# Không có thay đổi file code trong phase này, chỉ là chạy verify
```
