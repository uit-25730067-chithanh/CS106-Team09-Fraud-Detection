"""Phase 04 (Part 1): Train and evaluate XGBoost models.

Trains XGBoost on SMOTE (primary) and ADASYN (comparison) datasets with
hyperparameter tuning, evaluates on the held-out test set, generates feature
importance, and saves all artifacts (model, predictions, reports).

Author: Mỷ Cẩm
"""
import os
import sys

# Fix Windows console encoding for emoji
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pickle

import pandas as pd

from src.utils import set_seeds, get_project_root, DATA_PROCESSED_DIR, RANDOM_STATE
from src.models.xgboost_model import (
    train_xgboost,
    predict,
    evaluate_model,
    get_feature_importance,
    save_model,
    save_predictions,
    save_feature_importance,
    save_model_summary,
)

# n_iter/cv nhỏ để chạy nhanh trên CPU; tăng lên nếu muốn tuning kỹ hơn.
N_ITER = int(os.environ.get("XGB_N_ITER", "20"))
CV = int(os.environ.get("XGB_CV", "3"))


def _load(processed_dir: str, name: str):
    with open(os.path.join(processed_dir, f"{name}.pkl"), "rb") as f:
        return pickle.load(f)


def run_one(tag: str, X_train, y_train, X_test, y_test, feature_names) -> tuple[dict, dict, dict]:
    print(f"\n{'='*60}\n  XGBoost on {tag.upper()} data\n{'='*60}")
    print(f"📥 {tag} train: X={X_train.shape}, y={y_train.shape}")

    model, info = train_xgboost(
        X_train, y_train,
        tune=True, n_iter=N_ITER, cv=CV, scoring="f1",
    )

    y_pred, y_prob = predict(model, X_test)
    metrics = evaluate_model(y_test, y_pred, y_prob, f"XGB-{tag.upper()}")

    fi = get_feature_importance(model, feature_names, top_n=14)
    print(f"\n📊 Feature Importance (XGB-{tag.upper()}):")
    print(fi.to_string(index=False))

    save_model(model, f"xgb_{tag}")
    save_predictions(y_pred, y_prob, f"xgb_{tag}_predictions")
    save_feature_importance(fi, f"xgb_{tag}_feature_importance")
    save_model_summary(metrics, info, f"xgb_{tag}_summary")

    return metrics, info, {"y_pred": y_pred, "y_prob": y_prob}


def main():
    set_seeds(RANDOM_STATE)
    proj_root = get_project_root()
    processed_dir = os.path.join(proj_root, DATA_PROCESSED_DIR)
    reports_dir = os.path.join(proj_root, "reports")

    print("=" * 60)
    print("  Phase 04: XGBoost Model Training & Evaluation")
    print("=" * 60)

    X_test = _load(processed_dir, "X_test")
    y_test = _load(processed_dir, "y_test")
    feature_names = list(X_test.columns)
    print(f"\n📥 Test set: X={X_test.shape}  fraud ratio={y_test.mean():.6f}")

    results = {}
    combined_preds = {}
    for tag in ("smote", "adasyn"):
        X_tr = _load(processed_dir, f"X_train_{tag}")
        y_tr = _load(processed_dir, f"y_train_{tag}")
        metrics, info, preds = run_one(tag, X_tr, y_tr, X_test, y_test, feature_names)
        results[tag] = (metrics, info)
        combined_preds[f"xgb_{tag}"] = preds

    # ─── Comparison table ───────────────────────────────────────────────────
    print(f"\n{'='*60}\n  COMPARISON: XGB-SMOTE vs XGB-ADASYN\n{'='*60}")
    comparison = pd.DataFrame([
        {
            "Model": f"XGB-{tag.upper()}",
            "F1-Score": results[tag][0]["f1_score"],
            "Precision": results[tag][0]["precision"],
            "Recall": results[tag][0]["recall"],
            "ROC-AUC": results[tag][0]["roc_auc"],
            "Train Time (s)": results[tag][1]["training_time_seconds"],
        }
        for tag in ("smote", "adasyn")
    ])
    print(comparison.to_string(index=False))

    with open(os.path.join(reports_dir, "xgb_predictions.pkl"), "wb") as f:
        pickle.dump(combined_preds, f)
    print("\n📊 Combined predictions saved: reports/xgb_predictions.pkl")

    # ─── Success criteria (theo phase-04 doc) ──────────────────────────────
    print(f"\n{'='*60}\n  SUCCESS CRITERIA CHECK\n{'='*60}")
    m = results["smote"][0]
    checks = [
        ("XGB-SMOTE F1 > 0.75", m["f1_score"] > 0.75),
        ("XGB-SMOTE ROC-AUC > 0.93", m["roc_auc"] > 0.93),
    ]
    all_pass = True
    for name, passed in checks:
        print(f"  {'✅ PASS' if passed else '❌ FAIL'}  {name}")
        all_pass &= passed
    print("\n  🎉 ALL SUCCESS CRITERIA MET!" if all_pass
          else "\n  ⚠️ Some criteria not met — review results above.")

    print(f"\n{'='*60}\n  ✅ Phase 04 (XGBoost) COMPLETE\n{'='*60}")


if __name__ == "__main__":
    main()
