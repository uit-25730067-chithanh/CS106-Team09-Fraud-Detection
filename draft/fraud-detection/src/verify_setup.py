"""Verification script for Phase 00 - Environment & Data Setup."""
import sys
import os

# Add src to python path to check import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def verify_imports():
    print("=== Checking Library Imports ===")
    libraries = [
        ("pandas", "pd"),
        ("numpy", "np"),
        ("sklearn", "sklearn"),
        ("xgboost", "xgboost"),
        ("imblearn", "imblearn"),
        ("tensorflow", "tensorflow"),
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("shap", "shap"),
    ]
    all_ok = True
    for lib_name, short_name in libraries:
        try:
            lib = __import__(lib_name)
            version = getattr(lib, "__version__", "unknown")
            print(f"[✅] {lib_name:<12} version: {version}")
        except ImportError as e:
            print(f"[❌] {lib_name:<12} failed to import. Error: {e}")
            all_ok = False
    return all_ok

def verify_utils():
    print("\n=== Checking Project Utilities ===")
    try:
        from src.utils import RANDOM_STATE, TEST_SIZE, DATA_RAW_PATH, set_seeds, get_project_root
        print(f"[✅] RANDOM_STATE: {RANDOM_STATE}")
        print(f"[✅] TEST_SIZE: {TEST_SIZE}")
        print(f"[✅] DATA_RAW_PATH: {DATA_RAW_PATH}")
        print(f"[✅] get_project_root(): {get_project_root()}")
        
        # Test seeding
        set_seeds(RANDOM_STATE)
        print("[✅] set_seeds() works without error")
        return True
    except Exception as e:
        print(f"[❌] Failed to import or test utilities. Error: {e}")
        return False

def verify_dataset():
    print("\n=== Checking Dataset paysim.csv ===")
    from src.utils import DATA_RAW_PATH
    
    # Resolve absolute path based on project root
    from src.utils import get_project_root
    proj_root = get_project_root()
    csv_path = os.path.join(proj_root, DATA_RAW_PATH)
    
    if not os.path.exists(csv_path):
        print(f"[⚠️] Dataset not found at: {csv_path}")
        print("    Please download the Paysim dataset from Kaggle:")
        print("    https://www.kaggle.com/datasets/ealaxi/paysim1")
        print("    Then rename the csv file to 'paysim.csv' and place it in 'data/raw/'")
        return False
    
    try:
        import pandas as pd
        print(f"Loading dataset from {csv_path}...")
        df = pd.read_csv(csv_path)
        print(f"[✅] Dataset loaded successfully")
        print(f"[✅] Shape: {df.shape} (Expected: (6362620, 11))")
        
        fraud_ratio = df['isFraud'].mean()
        print(f"[✅] Fraud ratio: {fraud_ratio:.6f} (Expected: ~0.00129)")
        
        if df.shape == (6362620, 11):
            return True
        else:
            print(f"[❌] Shape mismatch: {df.shape}")
            return False
    except Exception as e:
        print(f"[❌] Failed to read or process dataset. Error: {e}")
        return False

if __name__ == "__main__":
    imports_ok = verify_imports()
    utils_ok = verify_utils()
    dataset_ok = verify_dataset()
    
    print("\n=== Summary ===")
    if imports_ok and utils_ok:
        if dataset_ok:
            print("[🎉] All checks PASSED! Environment and data are fully set up.")
            sys.exit(0)
        else:
            print("[⚠️] Environment and utilities are ready, but the dataset is missing or incorrect.")
            print("    Please follow instructions above to set up the dataset.")
            sys.exit(1)
    else:
        print("[❌] Setup verification failed. Please check logs above.")
        sys.exit(2)
