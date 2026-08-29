"""Feature engineering, encoding and scaling for PaySim dataset."""
import pandas as pd
from sklearn.preprocessing import StandardScaler

SCALE_COLS = ["amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest", "step", "hour_of_day", "amount_to_oldbalance_ratio"]


def scale_features(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, StandardScaler]:
    """
    1. Thực hiện Feature Engineering (errorBalanceOrig, errorBalanceDest và 5 features mới).
    2. One-Hot Encoding cho cột type.
    3. Fit StandardScaler trên train set, transform cả train và test.
    4. Drop các cột không dùng: nameOrig, nameDest, isFlaggedFraud (độ phủ quá thấp).

    Returns: (X_train_processed, X_test_processed, fitted_scaler)
    """
    X_train = X_train.copy()
    X_test = X_test.copy()

    # ─── 1. Feature Engineering ──────────────────────────────────────────────
    for df in [X_train, X_test]:
        df["is_drain_account"] = ((df["oldbalanceOrg"] > 0) & (df["newbalanceOrig"] == 0)).astype(int)
        df["hour_of_day"] = (df["step"] % 24).astype(int)
        df["is_night_transaction"] = (df["hour_of_day"] < 6).astype(int)
        df["amount_to_oldbalance_ratio"] = df["amount"] / (df["oldbalanceOrg"] + 1e-5)
        df["is_large_transaction"] = (df["amount"] > 200000).astype(int)

    X_train["errorBalanceOrig"] = X_train["oldbalanceOrg"] - X_train["amount"] - X_train["newbalanceOrig"]
    X_train["errorBalanceDest"] = X_train["oldbalanceDest"] + X_train["amount"] - X_train["newbalanceDest"]
    X_test["errorBalanceOrig"] = X_test["oldbalanceOrg"] - X_test["amount"] - X_test["newbalanceOrig"]
    X_test["errorBalanceDest"] = X_test["oldbalanceDest"] + X_test["amount"] - X_test["newbalanceDest"]

    # ─── 2. Encoding ──────────────────────────────────────────────────────────
    X_train = pd.get_dummies(X_train, columns=["type"], drop_first=True)
    X_test = pd.get_dummies(X_test, columns=["type"], drop_first=True)

    # Align columns in case some categories are missing in test set
    X_train, X_test = X_train.align(X_test, join="left", axis=1, fill_value=0)

    # ─── 3. Scaling ───────────────────────────────────────────────────────────
    cols_to_scale = SCALE_COLS + ["errorBalanceOrig", "errorBalanceDest"]
    scaler = StandardScaler()
    X_train[cols_to_scale] = scaler.fit_transform(X_train[cols_to_scale])
    X_test[cols_to_scale] = scaler.transform(X_test[cols_to_scale])

    # ─── 4. Drop IDs and Unused Columns ───────────────────────────────────────
    drop_cols = ["nameOrig", "nameDest", "isFlaggedFraud"]
    X_train = X_train.drop(columns=[c for c in drop_cols if c in X_train.columns], errors="ignore")
    X_test = X_test.drop(columns=[c for c in drop_cols if c in X_test.columns], errors="ignore")

    return X_train, X_test, scaler
