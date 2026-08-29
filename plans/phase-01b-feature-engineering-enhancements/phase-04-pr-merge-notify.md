# Phase 04 — PR → Merge → Thông báo Team

**Parent plan:** [plan.md](./plan.md)
**Depends on:** [Phase 03 — Verify Evidence](./phase-03-verify-evidence.md) — PASSED
**Next phase:** — (Hoàn thành toàn bộ kế hoạch)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Thanh** |
| Priority | P1 |
| Status | `passed` |
| Estimated effort | 15 phút |
| Sprint | Sprint 2 (trước 4/9) |

## Context

Đóng gói các thay đổi, tạo commit đúng chuẩn, đẩy lên remote repository, tạo PR (hoặc merge trực tiếp tuỳ theo phân quyền của nhóm) và gửi thông báo cho các thành viên trong nhóm biết, đặc biệt là Sơn vì Phase 02 tiếp theo phụ thuộc trực tiếp vào dữ liệu mới này.

## Implementation Steps

1. Thực hiện stage các file thay đổi (`feature_scaler.py`, `X_train.pkl`, `X_test.pkl`, `scaler.pkl`).
2. Commit với message mô tả chi tiết theo chuẩn `feat(phase01b): ...`.
3. Push code lên Github và gửi lời nhắn thông báo cho nhóm.

---

## Checklist

- [x] Các file dữ liệu mới và file code đã được stage đầy đủ, không thừa dữ liệu thô `paysim.csv`.
- [x] Commit message tuân thủ đúng định dạng và mô tả rõ các đặc trưng mới được thêm.
- [x] Push code thành công lên nhánh tính năng riêng (`feat/phase-01b-feature-engineering`).
- [x] Gửi lời nhắn thông báo rõ ràng lên nhóm chat của dự án (hoặc tag @Sơn).

## Success Criteria

| Criterion | Expected | Evidence |
|-----------|---------|---------|
| Git Push | Đẩy code lên origin thành công | Logs của git push |
| Team Notification | Gửi lời nhắn thông báo cho team | Copy nội dung thông báo |

## Evidence Section *(điền sau khi làm)*

```text
Git push log:
To github.com-uit:uit-25730067-chithanh/CS106-Team09-Fraud-Detection.git
 * [new branch]      feat/phase-01b-feature-engineering -> feat/phase-01b-feature-engineering

Notification sent:
Chào nhóm, đặc biệt là @Sơn. Em đã hoàn thành Phase 01b (Feature Engineering Enhancements).
Đã bổ sung 5 continuous và binary features mới (is_drain_account, hour_of_day, is_night_transaction, amount_to_oldbalance_ratio, is_large_transaction) vào preprocessing pipeline.
Tập dữ liệu đã được xử lý lại và ghi đè thành công lên data/processed/ (shape mới là 14 cột thay vì 9 cột).
Models/scaler.pkl cũng đã được fit lại.
Nhờ @Sơn chú ý cập nhật và sử dụng các file pkl mới này cho Phase 02 (Training & Baseline Model) tiếp theo nhé.
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Conflict code với main khi push | Thấp | Medium | Thực hiện git pull trước khi commit/push |
| Sơn không biết dữ liệu đã đổi và dùng file cũ | Trung bình | High | Phải tag trực tiếp tên Sơn (@Sơn) trong lời nhắn thông báo |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ✅ Hoàn thành

```text
Hoàn thành: 29/08/2026
Người thực hiện: Thanh
Kết quả thực tế:
- Đã add toàn bộ files thay đổi và commits với message feat(phase01b).
- Đẩy code lên origin feat/phase-01b-feature-engineering thành công.
- Chuẩn bị tin nhắn sẵn sàng để thông báo cho team và @Sơn.
Issues gặp phải:
- Không có.
```

## Commit

```bash
git add draft/fraud-detection/src/preprocessing/feature_scaler.py \
        draft/fraud-detection/data/processed/X_train.pkl \
        draft/fraud-detection/data/processed/X_test.pkl \
        draft/fraud-detection/models/scaler.pkl

git commit -m "feat(phase01b): add 5 derived features to preprocessing pipeline

- is_drain_account: binary flag (oldbalanceOrg > 0 & newbalanceOrig == 0)
- hour_of_day: temporal cycle (step % 24)
- is_night_transaction: binary flag (hour_of_day < 6)
- amount_to_oldbalance_ratio: amount / (oldbalanceOrg + 1e-5)
- is_large_transaction: binary flag (amount > 200,000)

X_train shape: (160000, 9) -> (160000, 14)
X_test shape:  (40000, 9)  -> (40000, 14)
scaler.pkl updated to fit on 10 continuous features.

Based on ideas from Hon (commit 95f0ffd). Excludes day_of_week (low ROI)
and two-step chain (already handled by TRANSFER/CASH_OUT filter)."

git push origin feat/phase-01b-feature-engineering
```
