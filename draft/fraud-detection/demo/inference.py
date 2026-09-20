"""Inference contract shared by the Streamlit demo and automated tests."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

import pandas as pd
from xgboost import XGBClassifier


MODEL_FEATURES = (
    "step",
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "is_drain_account",
    "hour_of_day",
    "is_night_transaction",
    "amount_to_oldbalance_ratio",
    "is_large_transaction",
    "errorBalanceOrig",
    "errorBalanceDest",
    "type_TRANSFER",
)

SCALED_FEATURES = (
    "amount",
    "oldbalanceOrg",
    "newbalanceOrig",
    "oldbalanceDest",
    "newbalanceDest",
    "step",
    "hour_of_day",
    "amount_to_oldbalance_ratio",
    "errorBalanceOrig",
    "errorBalanceDest",
)


@dataclass(frozen=True)
class FeatureTrace:
    """Exact feature values before and after the scaler for one prediction."""

    raw_values: tuple[float, ...]
    model_values: tuple[float, ...]


@dataclass(frozen=True)
class PredictionResult:
    """One fraud-classification result returned by the deployed model."""

    label: int
    fraud_probability: float
    threshold: float = 0.5
    model_name: str = "XGBoost-SMOTE"
    feature_trace: FeatureTrace | None = None


def load_xgboost_model(path: Path) -> XGBClassifier:
    """Load the Phase 04 XGBoost JSON artifact."""

    if not path.exists():
        raise FileNotFoundError(f"Không tìm thấy model: {path}")

    model = XGBClassifier()
    model.load_model(path)
    return model


def build_model_features(values: Mapping[str, object], scaler: object) -> pd.DataFrame:
    """Reproduce the exact Phase 01 feature engineering for one transaction."""

    _, features = _build_feature_frames(values, scaler)
    return features


def _build_feature_frames(
    values: Mapping[str, object], scaler: object,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Keep the original feature row alongside the exact model input."""

    transaction_type = str(values["transaction_type"])
    if transaction_type not in {"TRANSFER", "CASH_OUT"}:
        raise ValueError(f"Loại giao dịch không được hỗ trợ: {transaction_type}")

    step = int(values["step"])
    amount = float(values["amount"])
    old_origin = float(values["old_balance_origin"])
    new_origin = float(values["new_balance_origin"])
    old_destination = float(values["old_balance_destination"])
    new_destination = float(values["new_balance_destination"])
    hour_of_day = step % 24

    row = {
        "step": step,
        "amount": amount,
        "oldbalanceOrg": old_origin,
        "newbalanceOrig": new_origin,
        "oldbalanceDest": old_destination,
        "newbalanceDest": new_destination,
        "is_drain_account": int(old_origin > 0 and new_origin == 0),
        "hour_of_day": hour_of_day,
        "is_night_transaction": int(hour_of_day < 6),
        "amount_to_oldbalance_ratio": amount / (old_origin + 1e-5),
        "is_large_transaction": int(amount > 200_000),
        "errorBalanceOrig": old_origin - amount - new_origin,
        "errorBalanceDest": old_destination + amount - new_destination,
        "type_TRANSFER": int(transaction_type == "TRANSFER"),
    }
    # All model inputs are numeric. Casting before assignment also avoids the
    # strict pandas dtype error when standardized floats replace raw integers.
    features = pd.DataFrame([row], columns=MODEL_FEATURES).astype(float)

    scaler_features = tuple(getattr(scaler, "feature_names_in_", SCALED_FEATURES))
    if scaler_features != SCALED_FEATURES:
        raise ValueError(
            "Scaler không khớp contract 10 đặc trưng của Phase 01: "
            f"{scaler_features}"
        )

    raw_features = features.copy()
    features.loc[:, list(SCALED_FEATURES)] = scaler.transform(
        features.loc[:, list(SCALED_FEATURES)]
    )
    return raw_features, features


def reconstruct_transaction_input(
    processed_row: Mapping[str, object],
    scaler: object,
) -> dict[str, object]:
    """Reconstruct the seven raw PaySim fields from one processed test row.

    This is used only for labelled demo examples. The model continues to score
    the processed test set independently; ``isFraud`` is never an input.
    """

    missing = [feature for feature in MODEL_FEATURES if feature not in processed_row]
    if missing:
        raise ValueError(f"Thiếu đặc trưng trong mẫu test: {missing}")

    scaler_features = tuple(getattr(scaler, "feature_names_in_", SCALED_FEATURES))
    if scaler_features != SCALED_FEATURES:
        raise ValueError(
            "Scaler không khớp contract 10 đặc trưng của Phase 01: "
            f"{scaler_features}"
        )

    scaled_values = pd.DataFrame(
        [[float(processed_row[feature]) for feature in SCALED_FEATURES]],
        columns=SCALED_FEATURES,
    )
    raw_values = dict(
        zip(SCALED_FEATURES, scaler.inverse_transform(scaled_values)[0])
    )
    return {
        "transaction_type": (
            "TRANSFER" if float(processed_row["type_TRANSFER"]) >= 0.5 else "CASH_OUT"
        ),
        "step": int(round(float(raw_values["step"]))),
        "amount": float(raw_values["amount"]),
        "old_balance_origin": float(raw_values["oldbalanceOrg"]),
        "new_balance_origin": float(raw_values["newbalanceOrig"]),
        "old_balance_destination": float(raw_values["oldbalanceDest"]),
        "new_balance_destination": float(raw_values["newbalanceDest"]),
    }


def predict_transaction(
    values: Mapping[str, object],
    scaler: object,
    model: XGBClassifier,
    threshold: float = 0.5,
) -> PredictionResult:
    """Return a real probability and thresholded class for one transaction."""

    model_features = tuple(model.get_booster().feature_names or ())
    if model_features and model_features != MODEL_FEATURES:
        raise ValueError(
            "Model không khớp contract 14 đặc trưng của demo: "
            f"{model_features}"
        )

    raw_features, features = _build_feature_frames(values, scaler)
    fraud_probability = float(model.predict_proba(features)[0, 1])
    return PredictionResult(
        label=int(fraud_probability >= threshold),
        fraud_probability=fraud_probability,
        threshold=threshold,
        feature_trace=FeatureTrace(
            raw_values=tuple(float(value) for value in raw_features.iloc[0]),
            model_values=tuple(float(value) for value in features.iloc[0]),
        ),
    )
