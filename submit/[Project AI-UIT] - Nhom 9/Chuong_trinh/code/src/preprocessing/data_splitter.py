"""Stratified train/test split for imbalanced PaySim data."""
import pandas as pd
import pickle
from pathlib import Path
from sklearn.model_selection import train_test_split
from src.utils import RANDOM_STATE, TEST_SIZE, DATA_PROCESSED_DIR, get_project_root


def split_data(
    df: pd.DataFrame,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
    save: bool = False,
) -> tuple:
    """
    Stratified split on isFraud column.
    Saves raw splits to data/processed/ if save=True (warning: this will overwrite scaled data).

    Returns: (X_train, X_test, y_train, y_test)
    """
    X = df.drop("isFraud", axis=1)
    y = df["isFraud"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,  # CRITICAL for imbalanced data
    )

    if save:
        import os
        proj_root = get_project_root()
        processed_dir = os.path.join(proj_root, DATA_PROCESSED_DIR)
        Path(processed_dir).mkdir(parents=True, exist_ok=True)
        for name, obj in [
            ("X_train", X_train),
            ("X_test", X_test),
            ("y_train", y_train),
            ("y_test", y_test),
        ]:
            with open(os.path.join(processed_dir, f"{name}.pkl"), "wb") as f:
                pickle.dump(obj, f)
        print(f"Saved splits to {processed_dir}/")

    return X_train, X_test, y_train, y_test
