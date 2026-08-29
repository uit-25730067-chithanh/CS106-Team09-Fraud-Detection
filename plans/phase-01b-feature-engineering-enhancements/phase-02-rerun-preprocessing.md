# Phase 02 — Re-run Preprocessing → Overwrite .pkl

**Parent plan:** [plan.md](./plan.md)
**Depends on:** [Phase 01 — Implement Features](./phase-01-implement-features.md) — PASSED
**Next phase:** [Phase 03 — Verify Evidence](./phase-03-verify-evidence.md)

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

Chạy lại pipeline tiền xử lý bằng script `run_preprocessing.py` để áp dụng các thay đổi trong `feature_scaler.py` lên bộ dữ liệu, ghi đè các file pickle cũ.

Files bị ghi đè:
- `data/processed/X_train.pkl`
- `data/processed/X_test.pkl`
- `models/scaler.pkl`

## Implementation Steps

1. Kích hoạt môi trường ảo `.venv` trong thư mục `draft/fraud-detection`.
2. Thực thi script `run_preprocessing.py`.
3. Kiểm tra xem các file mới đã được ghi đè thành công hay chưa.

---

## Checklist

- [x] Môi trường ảo Python đã được kích hoạt.
- [x] Chạy thành công script `run_preprocessing.py` không có exception.
- [x] Kiểm tra thời gian sửa đổi (Modified time) của các file `.pkl` và `.pkl` trong `models/` đã được cập nhật mới.

## Success Criteria

| Criterion | Expected | Evidence |
|-----------|---------|---------|
| Script Execution | Kết thúc với exit code 0 | `python run_preprocessing.py` output |
| Output files creation | Ghi đè thành công `X_train.pkl`, `X_test.pkl` và `scaler.pkl` | Kiểm tra sự tồn tại và mtime của file |

## Evidence Section *(điền sau khi làm)*

```text
Execution Output:
=== Phase 01: Preprocessing Pipeline ===
Loading raw data from: data/raw/paysim.csv
Dataset Stats: {'shape': (200000, 11), 'n_fraud': 8213, 'n_normal': 191787, 'fraud_ratio': 0.041065, 'missing_values': 0}
Initial split shapes - X_train: (160000, 10), X_test: (40000, 10)
Processed shapes - X_train_scaled: (160000, 14), X_test_scaled: (40000, 14)
Saved processed file: data/processed/X_train.pkl
Saved processed file: data/processed/X_test.pkl
Saved processed file: data/processed/y_train.pkl
Saved processed file: data/processed/y_test.pkl
Saved fitted scaler -> models/scaler.pkl

=== Verification ===
y_train fraud ratio: 0.041063
y_test fraud ratio: 0.041075
[🎉] Pipeline executed successfully and verified!
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Thiếu raw data `paysim.csv` | Thấp | High | Đảm bảo `data/raw/paysim.csv` đã được tải và đặt đúng chỗ |
| OOM (Out of Memory) | Thấp | Medium | Hàm load_data đã downsample còn ~200k dòng nên rất nhẹ |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ Hoàn thành

```text
Hoàn thành: 29/08/2026
Người thực hiện: Thanh
Kết quả thực tế:
- Đã chạy thành công run_preprocessing.py.
- Ghi đè thành công X_train.pkl, X_test.pkl, y_train.pkl, y_test.pkl và models/scaler.pkl.
- Verification checks đã passed hoàn toàn.
Issues gặp phải:
- Không có.
```

## Commit

```bash
# Ở phase này chỉ chạy tạo data, không commit data thô, chỉ add data/processed và models/scaler.pkl
git add draft/fraud-detection/data/processed/X_train.pkl \
        draft/fraud-detection/data/processed/X_test.pkl \
        draft/fraud-detection/models/scaler.pkl
```
