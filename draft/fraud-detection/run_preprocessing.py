"""Runner script to execute the complete preprocessing pipeline."""
import os
import pickle
import sys

# Ensure src is in python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.preprocessing.data_loader import load_data, validate_data
from src.preprocessing.feature_scaler import scale_features
from src.preprocessing.data_splitter import split_data
from src.utils import DATA_PROCESSED_DIR, DATA_RAW_PATH, get_project_root


def main():
    print("=== Phase 01: Preprocessing Pipeline ===")

    # Resolve absolute path for raw data
    proj_root = get_project_root()
    raw_path = os.path.join(proj_root, DATA_RAW_PATH)
    print(f"Loading raw data from: {DATA_RAW_PATH}")

    # 1. Load và validate (gồm downsampling bên trong load_data)
    df = load_data(raw_path)
    stats = validate_data(df)
    print("Dataset Stats:", stats)

    # 2. Split (không tự động save vì chưa scale & encode)
    X_train, X_test, y_train, y_test = split_data(df, save=False)
    print(f"Initial split shapes - X_train: {X_train.shape}, X_test: {X_test.shape}")

    # 3. Scale các cột numerical và One-Hot Encode type, thêm feature mới
    X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)
    print(f"Processed shapes - X_train_scaled: {X_train_scaled.shape}, X_test_scaled: {X_test_scaled.shape}")

    # 4. Lưu processed data
    processed_dir = os.path.join(proj_root, DATA_PROCESSED_DIR)
    os.makedirs(processed_dir, exist_ok=True)
    for name, obj in [
        ("X_train", X_train_scaled),
        ("X_test", X_test_scaled),
        ("y_train", y_train),
        ("y_test", y_test),
    ]:
        path = os.path.join(processed_dir, f"{name}.pkl")
        with open(path, "wb") as f:
            pickle.dump(obj, f)
        print(f"Saved processed file: {DATA_PROCESSED_DIR}/{name}.pkl")

    # 5. Lưu fitted scaler vào models/ để Demo UI
    models_dir = os.path.join(proj_root, "models")
    os.makedirs(models_dir, exist_ok=True)
    scaler_path = os.path.join(models_dir, "scaler.pkl")
    with open(scaler_path, "wb") as f:
        pickle.dump(scaler, f)
    print("Saved fitted scaler -> models/scaler.pkl")

    # Verification checks according to success criteria
    print("\n=== Verification ===")
    print(f"y_train fraud ratio: {y_train.mean():.6f}")
    print(f"y_test fraud ratio: {y_test.mean():.6f}")
    assert X_train_scaled.shape == (160000, 14), f"X_train shape mismatch: {X_train_scaled.shape}"
    assert X_test_scaled.shape == (40000, 14), f"X_test shape mismatch: {X_test_scaled.shape}"
    assert abs(y_train.mean() - 0.041065) < 1e-4, f"y_train fraud ratio unexpected: {y_train.mean()}"
    assert abs(y_test.mean() - 0.041065) < 1e-4, f"y_test fraud ratio unexpected: {y_test.mean()}"
    print("[🎉] Pipeline executed successfully and verified!")


if __name__ == "__main__":
    main()
