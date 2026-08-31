"""Phase 03: Train and evaluate Random Forest models.

Trains RF on both SMOTE and ADASYN datasets with hyperparameter tuning,
evaluates on test set, generates feature importance analysis, and saves
all artifacts (models, predictions, reports).

Author: Hoàng Cao Sơn
"""
import sys
import os

# Fix Windows console encoding for emoji
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pickle
import numpy as np
from src.utils import set_seeds, get_project_root, DATA_PROCESSED_DIR, RANDOM_STATE
from src.models.random_forest_model import (
    train_random_forest,
    predict,
    evaluate_model,
    get_feature_importance,
    save_model,
    save_predictions,
    save_feature_importance,
    save_model_summary,
)


def main():
    set_seeds(RANDOM_STATE)
    proj_root = get_project_root()
    processed_dir = os.path.join(proj_root, DATA_PROCESSED_DIR)

    # ─── 1. Load data ────────────────────────────────────────────────────────
    print("=" * 60)
    print("  Phase 03: Random Forest Model Training & Evaluation")
    print("=" * 60)

    # Load test set (common for both evaluations)
    with open(os.path.join(processed_dir, "X_test.pkl"), "rb") as f:
        X_test = pickle.load(f)
    with open(os.path.join(processed_dir, "y_test.pkl"), "rb") as f:
        y_test = pickle.load(f)
    print(f"\n📥 Test set: X={X_test.shape}, y={y_test.shape}")
    print(f"   Test fraud ratio: {y_test.mean():.6f}")

    feature_names = list(X_test.columns)

    # ═══════════════════════════════════════════════════════════════════════
    # PART A: Random Forest on SMOTE data
    # ═══════════════════════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("  PART A: Random Forest on SMOTE data")
    print(f"{'='*60}")

    with open(os.path.join(processed_dir, "X_train_smote.pkl"), "rb") as f:
        X_smote = pickle.load(f)
    with open(os.path.join(processed_dir, "y_train_smote.pkl"), "rb") as f:
        y_smote = pickle.load(f)
    print(f"📥 SMOTE train: X={X_smote.shape}, y={y_smote.shape}")

    # Train with tuning
    rf_smote, info_smote = train_random_forest(
        X_smote, y_smote,
        tune=True,
        n_iter=50,
        cv=5,
        scoring="f1",
    )

    # Predict & evaluate
    y_pred_smote, y_prob_smote = predict(rf_smote, X_test)
    metrics_smote = evaluate_model(y_test, y_pred_smote, y_prob_smote, "RF-SMOTE")

    # Feature importance
    fi_smote = get_feature_importance(rf_smote, feature_names, top_n=14)
    print("\n📊 Feature Importance (RF-SMOTE):")
    print(fi_smote.to_string(index=False))

    # Save artifacts
    save_model(rf_smote, "rf_smote")
    save_predictions(y_pred_smote, y_prob_smote, "rf_smote_predictions")
    save_feature_importance(fi_smote, "rf_smote_feature_importance")
    save_model_summary(metrics_smote, info_smote, "rf_smote_summary")

    # ═══════════════════════════════════════════════════════════════════════
    # PART B: Random Forest on ADASYN data
    # ═══════════════════════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("  PART B: Random Forest on ADASYN data")
    print(f"{'='*60}")

    with open(os.path.join(processed_dir, "X_train_adasyn.pkl"), "rb") as f:
        X_adasyn = pickle.load(f)
    with open(os.path.join(processed_dir, "y_train_adasyn.pkl"), "rb") as f:
        y_adasyn = pickle.load(f)
    print(f"📥 ADASYN train: X={X_adasyn.shape}, y={y_adasyn.shape}")

    # Train with tuning
    rf_adasyn, info_adasyn = train_random_forest(
        X_adasyn, y_adasyn,
        tune=True,
        n_iter=50,
        cv=5,
        scoring="f1",
    )

    # Predict & evaluate
    y_pred_adasyn, y_prob_adasyn = predict(rf_adasyn, X_test)
    metrics_adasyn = evaluate_model(y_test, y_pred_adasyn, y_prob_adasyn, "RF-ADASYN")

    # Feature importance
    fi_adasyn = get_feature_importance(rf_adasyn, feature_names, top_n=14)
    print("\n📊 Feature Importance (RF-ADASYN):")
    print(fi_adasyn.to_string(index=False))

    # Save artifacts
    save_model(rf_adasyn, "rf_adasyn")
    save_predictions(y_pred_adasyn, y_prob_adasyn, "rf_adasyn_predictions")
    save_feature_importance(fi_adasyn, "rf_adasyn_feature_importance")
    save_model_summary(metrics_adasyn, info_adasyn, "rf_adasyn_summary")

    # ═══════════════════════════════════════════════════════════════════════
    # COMPARISON
    # ═══════════════════════════════════════════════════════════════════════
    print(f"\n{'='*60}")
    print("  COMPARISON: RF-SMOTE vs RF-ADASYN")
    print(f"{'='*60}")

    import pandas as pd
    comparison = pd.DataFrame([
        {
            "Model": "RF-SMOTE",
            "F1-Score": metrics_smote["f1_score"],
            "Precision": metrics_smote["precision"],
            "Recall": metrics_smote["recall"],
            "ROC-AUC": metrics_smote["roc_auc"],
            "Train Time (s)": info_smote["training_time_seconds"],
        },
        {
            "Model": "RF-ADASYN",
            "F1-Score": metrics_adasyn["f1_score"],
            "Precision": metrics_adasyn["precision"],
            "Recall": metrics_adasyn["recall"],
            "ROC-AUC": metrics_adasyn["roc_auc"],
            "Train Time (s)": info_adasyn["training_time_seconds"],
        },
    ])
    print(comparison.to_string(index=False))

    # Save combined predictions for downstream (Khang's evaluation)
    combined_preds = {
        "rf_smote": {"y_pred": y_pred_smote, "y_prob": y_prob_smote},
        "rf_adasyn": {"y_pred": y_pred_adasyn, "y_prob": y_prob_adasyn},
    }
    reports_dir = os.path.join(proj_root, "reports")
    with open(os.path.join(reports_dir, "rf_predictions.pkl"), "wb") as f:
        pickle.dump(combined_preds, f)
    print(f"\n📊 Combined predictions saved: reports/rf_predictions.pkl")

    # Success criteria check
    print(f"\n{'='*60}")
    print("  SUCCESS CRITERIA CHECK")
    print(f"{'='*60}")

    checks = [
        ("RF-SMOTE F1 > 0.75", metrics_smote["f1_score"] > 0.75),
        ("RF-SMOTE AUC > 0.90", metrics_smote["roc_auc"] > 0.90),
        ("RF-ADASYN F1 > 0.75", metrics_adasyn["f1_score"] > 0.75),
        ("RF-ADASYN AUC > 0.90", metrics_adasyn["roc_auc"] > 0.90),
    ]
    all_pass = True
    for name, passed in checks:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}  {name}")
        if not passed:
            all_pass = False

    if all_pass:
        print(f"\n  🎉 ALL SUCCESS CRITERIA MET!")
    else:
        print(f"\n  ⚠️ Some criteria not met — review results above.")

    print(f"\n{'='*60}")
    print("  ✅ Phase 03 COMPLETE")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
