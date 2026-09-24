"""Imbalance handling for fraud detection — SMOTE & ADASYN oversampling.

Áp dụng các kỹ thuật oversampling CHỈ trên tập huấn luyện để xử lý
mất cân bằng lớp (~4.1% fraud). Đảm bảo các cột nhị phân không bị
biến thành số thực lẻ.

Author: Hoàng Cao Sơn — Phase 02
"""
import numpy as np
import pandas as pd
import pickle
import os
from pathlib import Path

from imblearn.over_sampling import ADASYN
from imblearn.over_sampling import SMOTENC

from src.utils import RANDOM_STATE, DATA_PROCESSED_DIR, get_project_root


# ─── Binary feature columns ──────────────────────────────────────────────────
# Những cột nhị phân (0/1) cần bảo vệ khi oversampling
BINARY_FEATURES = [
    "is_drain_account",
    "is_night_transaction",
    "is_large_transaction",
    "type_TRANSFER",
]


def _get_categorical_indices(X: pd.DataFrame) -> list[int]:
    """Trả về danh sách index của các cột nhị phân/categorical trong DataFrame.

    Dùng cho SMOTENC để xử lý đúng bản chất categorical.
    """
    indices = []
    for col in BINARY_FEATURES:
        if col in X.columns:
            indices.append(X.columns.get_loc(col))
    return indices


def _round_binary_columns(X: pd.DataFrame) -> pd.DataFrame:
    """Làm tròn các cột nhị phân về 0 hoặc 1.

    ADASYN không có biến thể NC nên mẫu tổng hợp sẽ có giá trị
    thực lẻ ở các cột nhị phân → cần round() sau khi sinh mẫu.
    """
    X = X.copy()
    for col in BINARY_FEATURES:
        if col in X.columns:
            X[col] = np.round(X[col]).astype(int)
    return X


def apply_smote(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    sampling_strategy: float = 0.5,
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.Series]:
    """Áp dụng SMOTENC lên tập huấn luyện.

    Sử dụng SMOTENC (thay vì SMOTE thường) để xử lý đúng các cột
    nhị phân/categorical — không sinh số thực lẻ cho cờ 0/1.

    Parameters
    ----------
    X_train : pd.DataFrame
        Features tập huấn luyện (160,000 × 14).
    y_train : pd.Series
        Nhãn tập huấn luyện (0 = normal, 1 = fraud).
    sampling_strategy : float
        Tỷ lệ mẫu thiểu số / mẫu đa số mong muốn.
        0.5 → fraud chiếm ~33% tổng. 1.0 → fraud chiếm ~50%.
    random_state : int
        Seed để tái tạo kết quả.

    Returns
    -------
    (X_resampled, y_resampled) : tuple[pd.DataFrame, pd.Series]
    """
    cat_indices = _get_categorical_indices(X_train)

    smote = SMOTENC(
        categorical_features=cat_indices,
        sampling_strategy=sampling_strategy,
        random_state=random_state,
        k_neighbors=5,
    )

    X_res, y_res = smote.fit_resample(X_train, y_train)

    # Đảm bảo trả về DataFrame/Series với đúng column names
    X_res = pd.DataFrame(X_res, columns=X_train.columns)
    y_res = pd.Series(y_res, name=y_train.name)

    # Đảm bảo binary columns là int (SMOTENC đôi khi trả float)
    for col in BINARY_FEATURES:
        if col in X_res.columns:
            X_res[col] = X_res[col].astype(int)

    return X_res, y_res


def apply_adasyn(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    sampling_strategy: float = 0.5,
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.Series]:
    """Áp dụng ADASYN lên tập huấn luyện.

    ADASYN không có biến thể NC → sau khi sinh mẫu, các cột nhị phân
    được làm tròn (np.round) về 0/1.

    Parameters
    ----------
    X_train : pd.DataFrame
        Features tập huấn luyện.
    y_train : pd.Series
        Nhãn tập huấn luyện.
    sampling_strategy : float
        Tỷ lệ mẫu thiểu số / mẫu đa số mong muốn.
    random_state : int
        Seed để tái tạo kết quả.

    Returns
    -------
    (X_resampled, y_resampled) : tuple[pd.DataFrame, pd.Series]
    """
    adasyn = ADASYN(
        sampling_strategy=sampling_strategy,
        random_state=random_state,
        n_neighbors=5,
    )

    X_res, y_res = adasyn.fit_resample(X_train, y_train)

    # Đảm bảo trả về DataFrame/Series
    X_res = pd.DataFrame(X_res, columns=X_train.columns)
    y_res = pd.Series(y_res, name=y_train.name)

    # Làm tròn binary columns (ADASYN sinh số thực lẻ)
    X_res = _round_binary_columns(X_res)

    return X_res, y_res


def report_class_distribution(
    y_original: pd.Series,
    y_smote: pd.Series,
    y_adasyn: pd.Series,
) -> pd.DataFrame:
    """Tạo bảng so sánh phân phối lớp: Original vs SMOTE vs ADASYN.

    Returns
    -------
    pd.DataFrame
        Bảng tổng hợp với các cột: Dataset, Normal, Fraud, Total, Fraud_Ratio.
    """
    rows = []
    for name, y in [("Original", y_original), ("SMOTE", y_smote), ("ADASYN", y_adasyn)]:
        n_fraud = int(y.sum())
        n_normal = int(len(y) - n_fraud)
        total = len(y)
        ratio = y.mean()
        rows.append({
            "Dataset": name,
            "Normal": n_normal,
            "Fraud": n_fraud,
            "Total": total,
            "Fraud_Ratio": f"{ratio:.4f} ({ratio * 100:.2f}%)",
        })
    return pd.DataFrame(rows)


def save_resampled(
    X: pd.DataFrame,
    y: pd.Series,
    method: str,
    out_dir: str | None = None,
) -> dict[str, str]:
    """Lưu dữ liệu đã oversample vào file .pkl.

    Parameters
    ----------
    X : pd.DataFrame
        Features đã resample.
    y : pd.Series
        Nhãn đã resample.
    method : str
        Tên phương pháp ("smote" hoặc "adasyn").
    out_dir : str, optional
        Thư mục đầu ra. Mặc định: data/processed/ trong project root.

    Returns
    -------
    dict[str, str]
        Mapping tên file → đường dẫn tuyệt đối.
    """
    if out_dir is None:
        out_dir = os.path.join(get_project_root(), DATA_PROCESSED_DIR)

    Path(out_dir).mkdir(parents=True, exist_ok=True)

    method = method.lower()
    paths = {}

    x_path = os.path.join(out_dir, f"X_train_{method}.pkl")
    y_path = os.path.join(out_dir, f"y_train_{method}.pkl")

    with open(x_path, "wb") as f:
        pickle.dump(X, f)
    with open(y_path, "wb") as f:
        pickle.dump(y, f)

    paths[f"X_train_{method}"] = x_path
    paths[f"y_train_{method}"] = y_path

    print(f"✅ Saved {method.upper()} data:")
    print(f"   X → {x_path} ({X.shape})")
    print(f"   y → {y_path} ({y.shape})")

    return paths


def validate_binary_integrity(X: pd.DataFrame) -> dict[str, bool]:
    """Kiểm tra binary columns chỉ chứa 0 hoặc 1.

    Returns
    -------
    dict[str, bool]
        True = cột chỉ có 0/1, False = có giá trị khác.
    """
    result = {}
    for col in BINARY_FEATURES:
        if col in X.columns:
            unique_vals = set(X[col].unique())
            result[col] = unique_vals.issubset({0, 1, True, False})
    return result
