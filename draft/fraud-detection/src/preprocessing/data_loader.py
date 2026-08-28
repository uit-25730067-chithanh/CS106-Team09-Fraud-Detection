"""Load, filter and validate the PaySim dataset."""
import pandas as pd
from pathlib import Path


def load_data(path: str = "data/raw/paysim.csv") -> pd.DataFrame:
    """
    Load CSV, filter for TRANSFER/CASH_OUT, and downsample to ~200k rows
    while preserving all fraud cases.
    """
    p = Path(path)
    if not p.exists():
        # Fallback to checking from project root if relative path is context-dependent
        # but the standard path is data/raw/paysim.csv
        raise FileNotFoundError(
            f"Dataset not found at {path}. "
            "Download from: https://www.kaggle.com/datasets/ealaxi/paysim1"
        )

    # Load và lọc loại giao dịch
    df = pd.read_csv(p)
    df = df[df["type"].isin(["TRANSFER", "CASH_OUT"])].reset_index(drop=True)

    # Stratified downsampling
    fraud_df = df[df["isFraud"] == 1]
    normal_df = df[df["isFraud"] == 0]

    # Downsample normal_df để đạt tổng kích thước ~200,000 dòng
    # Clamp để tránh n_normal_samples âm hoặc vượt số mẫu normal có sẵn
    n_fraud = len(fraud_df)
    if n_fraud >= 200000:
        raise ValueError(
            f"Số fraud ({n_fraud}) vượt mục tiêu downsample 200,000. "
            "Kiểm tra lại bộ lọc hoặc tăng ngưỡng mục tiêu."
        )
    n_normal_samples = min(200000 - n_fraud, len(normal_df))
    normal_sampled = normal_df.sample(n=n_normal_samples, random_state=42)

    # Gộp lại và shuffle
    df_downsampled = pd.concat([fraud_df, normal_sampled])
    df_downsampled = df_downsampled.sample(frac=1.0, random_state=42).reset_index(drop=True)

    return df_downsampled


def validate_data(df: pd.DataFrame) -> dict:
    """Validate dataset integrity. Returns summary dict."""
    assert df["isFraud"].nunique() == 2, "isFraud column must have 2 unique values"
    assert df.isnull().sum().sum() == 0, "Dataset has missing values"

    n_fraud = df["isFraud"].sum()
    fraud_ratio = df["isFraud"].mean()

    return {
        "shape": df.shape,
        "n_fraud": int(n_fraud),
        "n_normal": int(len(df) - n_fraud),
        "fraud_ratio": round(fraud_ratio, 6),
        "missing_values": int(df.isnull().sum().sum()),
    }
