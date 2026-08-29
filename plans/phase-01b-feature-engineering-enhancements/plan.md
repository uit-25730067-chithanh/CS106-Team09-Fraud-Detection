---
title: "Phase 01b — Feature Engineering Enhancements (Thanh)"
description: "Bổ sung 5 derived features mới vào preprocessing pipeline dựa trên ý tưởng Hôn đề xuất trong commit 95f0ffd."
status: completed
priority: P1
effort: ~2h
branch: feat/phase-01b-feature-engineering
tags: [cs106, fraud-detection, feature-engineering, preprocessing, sprint2]
created: 2026-08-29
updated: 2026-08-29
owner: Thanh (Đặng Chí Thanh — 25730067)
parent-plan: plans/fraud-detection-full-submit/plan.md
source-ideas: plans/fraud-detection-full-submit/phase-01-eda-preprocessing.md#💡-ý-tưởng-đề-xuất--cải-tiến-nâng-cao-từ-my_ideas
---

# Plan: Phase 01b — Feature Engineering Enhancements

## Mục tiêu

Từ 4 nhóm ý tưởng Hôn đề xuất trong `💡 Ý tưởng Đề xuất` (commit `95f0ffd`),
chắt lọc ra **5 features có ROI cao nhất** phù hợp scope của Thanh và implement
vào `feature_scaler.py`, cập nhật `scaler.pkl` + `.pkl` processed data.

## Phạm vi (Scope)

**IN scope — Thanh làm:**
- `is_drain_account` — binary flag
- `hour_of_day` — temporal cycle
- `is_night_transaction` — temporal flag (0h–5h)
- `amount_to_oldbalance_ratio` — amount ratio
- `is_large_transaction` — binary flag (>200,000)

**OUT scope — Không làm trong plan này:**
- `day_of_week` — ROI thấp nhất trong temporal group, skip
- Two-step chain (đã implement qua filter TRANSFER/CASH_OUT trong `data_loader.py`)
- Bất kỳ feature nào của Sơn, Cẩm, Khang, Trung

## Constraints

- Không thay đổi shape cũ (160000×9 train) — chỉ **thêm cột**, không xóa cột hiện có
- Binary features (`is_*`) KHÔNG đưa vào `SCALE_COLS` — đây là flag 0/1, scale sẽ mất ý nghĩa
- Continuous features mới (`amount_to_oldbalance_ratio`, `hour_of_day`) cần thêm vào `SCALE_COLS`
- Phải re-run `run_preprocessing.py` → overwrite `.pkl` + `scaler.pkl`
- Phải báo Sơn biết schema thay đổi trước khi Sơn bắt đầu Phase 02

## Phases

| # | Phase | Status | Est. |
|---|-------|--------|------|
| 01 | [Implement features trong `feature_scaler.py`](./phase-01-implement-features.md) | `passed` | 30 phút |
| 02 | [Re-run preprocessing → overwrite .pkl](./phase-02-rerun-preprocessing.md) | `passed` | 30 phút |
| 03 | [Code review + verify evidence](./phase-03-verify-evidence.md) | `passed` | 30 phút |
| 04 | [PR → merge → thông báo team](./phase-04-pr-merge-notify.md) | `passed` | 15 phút |
