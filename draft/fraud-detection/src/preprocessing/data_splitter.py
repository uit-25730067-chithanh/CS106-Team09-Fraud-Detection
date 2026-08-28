"""Stratified train/test split for imbalanced PaySim data."""
import pandas as pd
import pickle
from pathlib import Path
from sklearn.model_selection import train_test_split
from src.utils import RANDOM_STATE, TEST_SIZE, DATA_PROCESSED_DIR


def split_data(
    df: pd.DataFrame,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
    save: bool = True,
) -> tuple:
    """
    Stratified split on isFraud column.
    Saves processed splits to data/processed/ if save=True.

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
        Path(DATA_PROCESSED_DIR).mkdir(parents=True, exist_ok=True)
        for name, obj in [
            ("X_train", X_train),
            ("X_test", X_test),
            ("y_train", y_train),
            ("y_test", y_test),
        ]:
            with open(f"{DATA_PROCESSED_DIR}/{name}.pkl", "wb") as f:
                pickle.dump(obj, f)
        print(f"Saved splits to {DATA_PROCESSED_DIR}/")

    return X_train, X_test, y_train, y_test
