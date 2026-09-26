#!/usr/bin/env python3
"""
Phase 01: Script thực nghiệm Ablation Study & Feature Pruning cho Đồ án CS106 Nhóm 09.
Khảo sát 3 kịch bản trên mô hình XGBoost (SMOTENC train, clean test 40.000 mẫu):
1. Full_14: Đầy đủ 14 đặc trưng (Baseline).
2. Pruned_12: Cắt bỏ 2 đặc trưng có Gain xấp xỉ 0 (is_night_transaction, is_large_transaction).
3. No_Balance_6: Loại bỏ toàn bộ 8 đặc trưng số dư, chỉ giữ lại 6 đặc trưng giao dịch thuần túy.

Kết quả xuất ra:
- reports/ablation_study_results.csv
- reports/ablation_study_summary.txt
"""

import os
import time
import pickle
import numpy as np
import pandas as pd
from xgboost import XGBClassifier
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

os.makedirs(REPORTS_DIR, exist_ok=True)

# 1. Nạp dữ liệu
print("[*] Đang nạp dữ liệu train/test đã xử lý...")
with open(os.path.join(DATA_DIR, "X_train_smote.pkl"), "rb") as f:
    X_train_full = pickle.load(f)
with open(os.path.join(DATA_DIR, "y_train_smote.pkl"), "rb") as f:
    y_train = pickle.load(f)

with open(os.path.join(DATA_DIR, "X_test.pkl"), "rb") as f:
    X_test_full = pickle.load(f)
with open(os.path.join(DATA_DIR, "y_test.pkl"), "rb") as f:
    y_test = pickle.load(f)

print(f"[✓] X_train shape: {X_train_full.shape}, X_test shape: {X_test_full.shape}")

# 2. Định nghĩa các tập đặc trưng
features_full = list(X_train_full.columns)
features_pruned = [c for c in features_full if c not in ["is_night_transaction", "is_large_transaction"]]
features_no_balance = ["step", "amount", "hour_of_day", "is_night_transaction", "is_large_transaction", "type_TRANSFER"]

scenarios = [
    {
        "name": "Full_14_Baseline",
        "description": "Toàn bộ 14 đặc trưng chuẩn",
        "features": features_full,
    },
    {
        "name": "Pruned_12_Optimized",
        "description": "Cắt bỏ 2 đặc trưng Gain ≈ 0 (is_night, is_large)",
        "features": features_pruned,
    },
    {
        "name": "No_Balance_6_Ablation",
        "description": "Loại bỏ toàn bộ 8 đặc trưng số dư (chỉ giữ 6 biến giao dịch)",
        "features": features_no_balance,
    },
]

# Siêu tham số tối ưu chuẩn của nhóm
xgb_params = {
    "n_estimators": 300,
    "max_depth": 8,
    "learning_rate": 0.2,
    "subsample": 0.85,
    "colsample_bytree": 1.0,
    "min_child_weight": 3,
    "gamma": 0.1,
    "scale_pos_weight": 1.0,
    "tree_method": "hist",
    "eval_metric": "aucpr",
    "random_state": 42,
    "n_jobs": -1,
}

results = []
summary_lines = [
    "=" * 70,
    "BÁO CÁO THỰC NGHIỆM ABLATION STUDY & FEATURE PRUNING (CS106 - NHÓM 09)",
    "=" * 70,
    f"Thời điểm thực nghiệm: {time.strftime('%Y-%m-%d %H:%M:%S')}",
    f"Tập huấn luyện (SMOTE): {len(X_train_full):,} dòng",
    f"Tập kiểm thử độc lập:  {len(X_test_full):,} dòng (1.643 gian lận / 38.357 hợp lệ)",
    "-" * 70,
]

for sc in scenarios:
    name = sc["name"]
    cols = sc["features"]
    n_feats = len(cols)
    print(f"\n---> Đang chạy kịch bản: {name} ({n_feats} đặc trưng)...")

    X_tr = X_train_full[cols]
    X_te = X_test_full[cols]

    # Huấn luyện
    t0 = time.time()
    clf = XGBClassifier(**xgb_params)
    clf.fit(X_tr, y_train)
    train_time = time.time() - t0

    # Dự đoán & đo độ trễ suy luận
    t1 = time.time()
    y_pred = clf.predict(X_te)
    y_prob = clf.predict_proba(X_te)[:, 1]
    infer_time_total = time.time() - t1
    infer_latency_ms = (infer_time_total / len(X_te)) * 1000.0

    # Tính toán các chỉ số
    cm = confusion_matrix(y_test, y_pred)
    tn, fp, fn, tp = cm.ravel()
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    pr_auc = average_precision_score(y_test, y_prob)

    # Quy chiếu prevalence gốc (0.129082%)
    p_real = 0.00129082
    fpr = fp / (tn + fp)
    tpr = rec
    prec_projected = (tpr * p_real) / (tpr * p_real + fpr * (1.0 - p_real))
    fp_per_million = int(round(fpr * 1_000_000))

    res_item = {
        "Scenario": name,
        "Num_Features": n_feats,
        "Train_Time_s": round(train_time, 2),
        "Inference_Latency_us": round(infer_latency_ms * 1000, 2),
        "TP": int(tp),
        "FP": int(fp),
        "FN": int(fn),
        "TN": int(tn),
        "Precision_Test": round(prec, 4),
        "Recall_Test": round(rec, 4),
        "F1_Score_Test": round(f1, 4),
        "ROC_AUC": round(roc_auc, 4),
        "PR_AUC": round(pr_auc, 4),
        "Precision_Projected_Real": round(prec_projected, 4),
        "FP_Per_Million": fp_per_million,
    }
    results.append(res_item)

    summary_lines.append(
        f"[{name}] ({n_feats} feats | Train: {train_time:.2f}s | Latency: {infer_latency_ms*1000:.1f}µs/mẫu):\n"
        f"  - Confusion Matrix: TP={tp}, FP={fp}, FN={fn}, TN={tn}\n"
        f"  - Precision: {prec:.4f} | Recall: {rec:.4f} | F1-Score: {f1:.4f}\n"
        f"  - ROC-AUC:   {roc_auc:.4f} | PR-AUC: {pr_auc:.4f}\n"
        f"  - Quy chiếu tỷ lệ gốc 0.129%: Precision={prec_projected:.4f} (~{fp_per_million} FP/triệu GD)\n"
    )
    print(f"    [✓] Hoàn tất: F1 = {f1:.4f}, Recall = {rec:.4f}, Precision = {prec:.4f}, FP = {fp}")

# 3. Xuất file kết quả
df_results = pd.DataFrame(results)
csv_out = os.path.join(REPORTS_DIR, "ablation_study_results.csv")
df_results.to_csv(csv_out, index=False, encoding="utf-8")
print(f"\n[✓] Đã lưu bảng kết quả: {csv_out}")

txt_out = os.path.join(REPORTS_DIR, "ablation_study_summary.txt")
with open(txt_out, "w", encoding="utf-8") as f:
    f.write("\n".join(summary_lines) + "\n")
print(f"[✓] Đã lưu tóm tắt phân tích: {txt_out}")

print("\n" + "\n".join(summary_lines))
