"""Phase 02: Run imbalance handling pipeline.

Loads processed train data, applies SMOTE & ADASYN, validates binary
feature integrity, saves 4 .pkl files, and prints distribution report.

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
from src.preprocessing.imbalance_handler import (
    apply_smote,
    apply_adasyn,
    report_class_distribution,
    save_resampled,
    validate_binary_integrity,
)


def main():
    set_seeds(RANDOM_STATE)
    proj_root = get_project_root()
    processed_dir = os.path.join(proj_root, DATA_PROCESSED_DIR)

    # ─── 1. Load data ────────────────────────────────────────────────────────
    print("=" * 60)
    print("  Phase 02: Imbalance Handling (SMOTE & ADASYN)")
    print("=" * 60)

    with open(os.path.join(processed_dir, "X_train.pkl"), "rb") as f:
        X_train = pickle.load(f)
    with open(os.path.join(processed_dir, "y_train.pkl"), "rb") as f:
        y_train = pickle.load(f)

    print(f"\n📥 Loaded X_train: {X_train.shape}")
    print(f"📥 Loaded y_train: {y_train.shape}")
    print(f"   Fraud ratio: {y_train.mean():.6f} ({y_train.sum()} fraud / {len(y_train)} total)")

    # ─── 2. Apply SMOTE (SMOTENC) ────────────────────────────────────────────
    print(f"\n{'─'*50}")
    print("🔄 Applying SMOTENC (sampling_strategy=0.5)...")
    X_smote, y_smote = apply_smote(X_train, y_train, sampling_strategy=0.5)
    print(f"   Output shape: X={X_smote.shape}, y={y_smote.shape}")
    print(f"   Fraud ratio: {y_smote.mean():.6f} ({y_smote.sum()} / {len(y_smote)})")

    # ─── 3. Apply ADASYN ─────────────────────────────────────────────────────
    print(f"\n{'─'*50}")
    print("🔄 Applying ADASYN (sampling_strategy=0.5)...")
    X_adasyn, y_adasyn = apply_adasyn(X_train, y_train, sampling_strategy=0.5)
    print(f"   Output shape: X={X_adasyn.shape}, y={y_adasyn.shape}")
    print(f"   Fraud ratio: {y_adasyn.mean():.6f} ({y_adasyn.sum()} / {len(y_adasyn)})")

    # ─── 4. Validate binary integrity ─────────────────────────────────────────
    print(f"\n{'─'*50}")
    print("🔎 Validating binary feature integrity...")
    for name, X in [("SMOTE", X_smote), ("ADASYN", X_adasyn)]:
        integrity = validate_binary_integrity(X)
        all_ok = all(integrity.values())
        status = "✅ PASS" if all_ok else "❌ FAIL"
        print(f"   {name}: {status} — {integrity}")

    # ─── 5. Distribution report ───────────────────────────────────────────────
    print(f"\n{'─'*50}")
    print("📊 Class Distribution Report:")
    report = report_class_distribution(y_train, y_smote, y_adasyn)
    print(report.to_string(index=False))

    # ─── 6. Save resampled data ──────────────────────────────────────────────
    print(f"\n{'─'*50}")
    save_resampled(X_smote, y_smote, "smote")
    save_resampled(X_adasyn, y_adasyn, "adasyn")

    # ─── 7. Verify test set is untouched ──────────────────────────────────────
    print(f"\n{'─'*50}")
    print("🛡️ Verifying test set integrity...")
    with open(os.path.join(processed_dir, "y_test.pkl"), "rb") as f:
        y_test = pickle.load(f)
    test_ratio = y_test.mean()
    print(f"   y_test fraud ratio: {test_ratio:.6f} (expected ~0.041065)")
    assert abs(test_ratio - 0.041065) < 0.001, f"Test set contaminated! Ratio: {test_ratio}"
    print("   ✅ Test set is untouched.")

    print(f"\n{'='*60}")
    print("  ✅ Phase 02 COMPLETE — 4 .pkl files saved")
    print("=" * 60)


if __name__ == "__main__":
    main()
