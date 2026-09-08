"""Cross-model performance comparison table."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def compare_models(metrics_list: list[dict]) -> pd.DataFrame:
    """Build a comparison DataFrame from a list of metrics dicts, sorted by F1 descending."""

    df = pd.DataFrame(metrics_list)
    df = df.sort_values("f1_fraud", ascending=False).reset_index(drop=True)
    df.columns = [c.replace("_", " ").title() for c in df.columns]
    return df


def save_comparison(df: pd.DataFrame, path: str | Path = "reports/model_comparison.csv") -> None:
    """Save the comparison table to CSV."""

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
