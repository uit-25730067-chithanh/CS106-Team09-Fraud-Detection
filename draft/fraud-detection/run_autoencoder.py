"""Phase 04 (Part 2): Train and evaluate the Autoencoder (anomaly detection).

Huấn luyện autoencoder CHỈ trên giao dịch bình thường của tập train GỐC
(trước SMOTE — SMOTE không phù hợp cho anomaly detection). Chọn ngưỡng
reconstruction-error theo F1 trên một phần validation tách từ train, rồi
đánh giá trên tập test.

Author: Mỷ Cẩm
"""
import os
import sys

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pickle

import numpy as np
from sklearn.model_selection import train_test_split

from src.utils import set_seeds, get_project_root, DATA_PROCESSED_DIR, RANDOM_STATE
from src.models.random_forest_model import evaluate_model, save_predictions
from src.models.autoencoder_model import (
    train_autoencoder,
    select_threshold_by_f1,
    predict_autoencoder,
    save_autoencoder,
    save_autoencoder_summary,
)

EPOCHS = int(os.environ.get("AE_EPOCHS", "200"))


def _load(processed_dir: str, name: str):
    with open(os.path.join(processed_dir, f"{name}.pkl"), "rb") as f:
        return pickle.load(f)


def main():
    set_seeds(RANDOM_STATE)
    proj_root = get_project_root()
    processed_dir = os.path.join(proj_root, DATA_PROCESSED_DIR)
    reports_dir = os.path.join(proj_root, "reports")

    print("=" * 60)
    print("  Phase 04: Autoencoder (Anomaly Detection) Training & Evaluation")
    print("=" * 60)

    # Train GỐC (chưa SMOTE) — giữ đúng phân phối normal/fraud thực.
    X_train_full = _load(processed_dir, "X_train")
    y_train_full = _load(processed_dir, "y_train")
    X_test = _load(processed_dir, "X_test")
    y_test = _load(processed_dir, "y_test")
    print(f"\n📥 Train gốc: X={X_train_full.shape}  fraud={int(y_train_full.sum())}")
    print(f"📥 Test:      X={X_test.shape}  fraud={int(y_test.sum())}")

    # Tách validation (stratify để giữ đủ mẫu fraud cho việc chọn ngưỡng).
    X_tr, X_val, y_tr, y_val = train_test_split(
        X_train_full, y_train_full,
        test_size=0.2, random_state=RANDOM_STATE, stratify=y_train_full,
    )
    print(f"   → fit={X_tr.shape[0]:,} | validation={X_val.shape[0]:,} "
          f"(fraud val={int(np.asarray(y_val).sum())})")

    # ─── Train ─────────────────────────────────────────────────────────────
    model, history = train_autoencoder(X_tr, y_tr, epochs=EPOCHS, random_state=RANDOM_STATE)

    # ─── Chọn ngưỡng trên validation ─────────────────────────────────────
    # Ưu tiên recall ≥ 0.60 (mục tiêu bonus của phase-04), trong đó lấy F1 tốt nhất.
    threshold, thr_table = select_threshold_by_f1(
        model, X_val, y_val,
        percentiles=(80.0, 85.0, 90.0, 95.0, 99.0, 99.5, 99.9),
        min_recall=0.60,
    )

    # ─── Đánh giá trên test ───────────────────────────────────────────────
    out = predict_autoencoder(model, X_test, threshold)
    metrics = evaluate_model(y_test, out["y_pred"], out["y_prob"], "Autoencoder")

    # ─── Lưu artifacts ───────────────────────────────────────────────────
    save_autoencoder(model, threshold, name="autoencoder", history=history)
    save_predictions(out["y_pred"], out["y_prob"], "autoencoder_predictions")
    save_autoencoder_summary(metrics, history, threshold, thr_table, "autoencoder_summary")

    with open(os.path.join(reports_dir, "autoencoder_recon_errors.pkl"), "wb") as f:
        pickle.dump(
            {"reconstruction_errors": out["reconstruction_errors"], "y_test": np.asarray(y_test)},
            f,
        )
    print("📊 Reconstruction errors saved: reports/autoencoder_recon_errors.pkl")

    # ─── Success criteria (bonus target: Recall fraud > 0.60) ─────────────
    print(f"\n{'='*60}\n  SUCCESS CRITERIA CHECK\n{'='*60}")
    passed = metrics["recall"] > 0.60
    print(f"  {'✅ PASS' if passed else '❌ FAIL'}  Autoencoder Recall(fraud) > 0.60 "
          f"(actual={metrics['recall']})")
    print("\n  ℹ️ Autoencoder là điểm cộng (bonus) — precision thấp là bình thường "
          "với anomaly detection thuần.")

    print(f"\n{'='*60}\n  ✅ Phase 04 (Autoencoder) COMPLETE\n{'='*60}")


if __name__ == "__main__":
    main()
