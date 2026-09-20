"""Regression tests for the Phase 06 demo inference contract."""

from __future__ import annotations

import pickle
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEMO_DIR = PROJECT_ROOT / "demo"
if str(DEMO_DIR) not in sys.path:
    sys.path.insert(0, str(DEMO_DIR))

from inference import (
    MODEL_FEATURES,
    SCALED_FEATURES,
    build_model_features,
    load_xgboost_model,
    predict_transaction,
    reconstruct_transaction_input,
)


@pytest.fixture(scope="module")
def inference_assets():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with (PROJECT_ROOT / "models" / "scaler.pkl").open("rb") as scaler_file:
            scaler = pickle.load(scaler_file)
    model = load_xgboost_model(PROJECT_ROOT / "models" / "xgb_smote.json")
    return scaler, model


SCENARIOS = {
    "safe_demo": {
        "transaction_type": "TRANSFER",
        "step": 120,
        "amount": 250_000.0,
        "old_balance_origin": 1_000_000.0,
        "new_balance_origin": 750_000.0,
        "old_balance_destination": 500_000.0,
        "new_balance_destination": 750_000.0,
    },
    "watchlist": {
        "transaction_type": "TRANSFER",
        "step": 720,
        "amount": 2_500_000.0,
        "old_balance_origin": 3_000_000.0,
        "new_balance_origin": 500_000.0,
        "old_balance_destination": 500_000.0,
        "new_balance_destination": 3_000_000.0,
    },
    "high_risk_demo": {
        "transaction_type": "CASH_OUT",
        "step": 70,
        "amount": 2_000_000.0,
        "old_balance_origin": 1_600_000.0,
        "new_balance_origin": 0.0,
        "old_balance_destination": 2_000_000.0,
        "new_balance_destination": 4_000_000.0,
    },
    "balanced": {
        "transaction_type": "TRANSFER",
        "step": 120,
        "amount": 250_000.0,
        "old_balance_origin": 1_000_000.0,
        "new_balance_origin": 750_000.0,
        "old_balance_destination": 500_000.0,
        "new_balance_destination": 750_000.0,
    },
    "mismatch": {
        "transaction_type": "TRANSFER",
        "step": 410,
        "amount": 300_000.0,
        "old_balance_origin": 800_000.0,
        "new_balance_origin": 620_000.0,
        "old_balance_destination": 200_000.0,
        "new_balance_destination": 430_000.0,
    },
    "large": {
        "transaction_type": "CASH_OUT",
        "step": 720,
        "amount": 2_500_000.0,
        "old_balance_origin": 3_000_000.0,
        "new_balance_origin": 500_000.0,
        "old_balance_destination": 10_000_000.0,
        "new_balance_destination": 12_500_000.0,
    },
    "drain": {
        "transaction_type": "TRANSFER",
        "step": 435,
        "amount": 1_143_937.73,
        "old_balance_origin": 1_143_937.73,
        "new_balance_origin": 0.0,
        "old_balance_destination": 0.0,
        "new_balance_destination": 0.0,
    },
}


def test_feature_contract_matches_xgboost(inference_assets):
    scaler, model = inference_assets
    features = build_model_features(SCENARIOS["balanced"], scaler)

    assert tuple(features.columns) == MODEL_FEATURES
    assert tuple(model.get_booster().feature_names) == MODEL_FEATURES
    assert features.shape == (1, 14)


@pytest.mark.parametrize(
    ("scenario", "expected_label"),
    [
        ("safe_demo", 0),
        ("watchlist", 0),
        ("high_risk_demo", 1),
        ("balanced", 0),
        ("mismatch", 0),
        ("large", 0),
        ("drain", 1),
    ],
)
def test_presets_return_real_model_predictions(
    inference_assets,
    scenario: str,
    expected_label: int,
):
    scaler, model = inference_assets
    result = predict_transaction(SCENARIOS[scenario], scaler, model)

    assert result.label == expected_label
    assert 0.0 <= result.fraud_probability <= 1.0


def test_custom_threshold_changes_classification(inference_assets):
    scaler, model = inference_assets

    default_result = predict_transaction(SCENARIOS["watchlist"], scaler, model)
    sensitive_result = predict_transaction(
        SCENARIOS["watchlist"],
        scaler,
        model,
        threshold=0.2,
    )

    assert default_result.label == 0
    assert 0.2 <= default_result.fraud_probability < 0.5
    assert sensitive_result.label == 1
    assert sensitive_result.fraud_probability == default_result.fraud_probability


def test_high_risk_demo_is_large_and_stays_in_explainable_probability_band(
    inference_assets,
):
    scaler, model = inference_assets
    scenario = SCENARIOS["high_risk_demo"]

    result = predict_transaction(scenario, scaler, model)
    features = build_model_features(scenario, scaler)

    assert features.iloc[0]["is_large_transaction"] == 1
    assert result.label == 1
    assert 0.85 <= result.fraud_probability <= 0.90


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_feature_trace_captures_actual_scaler_and_model_input(inference_assets, monkeypatch, scenario):
    scaler, model = inference_assets
    captured = {}
    original_transform = scaler.transform
    original_predict = model.predict_proba

    def capture_transform(values):
        captured["raw"] = values.copy()
        return original_transform(values)

    def capture_prediction(values):
        captured["model"] = values.copy()
        return original_predict(values)

    monkeypatch.setattr(scaler, "transform", capture_transform)
    monkeypatch.setattr(model, "predict_proba", capture_prediction)
    result = predict_transaction(SCENARIOS[scenario], scaler, model)

    assert result.feature_trace is not None
    np.testing.assert_array_equal(result.feature_trace.model_values, captured["model"].iloc[0])
    raw = pd.Series(result.feature_trace.raw_values, index=MODEL_FEATURES)
    np.testing.assert_array_equal(raw.loc[list(SCALED_FEATURES)], captured["raw"].iloc[0])
    binary_features = [name for name in MODEL_FEATURES if name not in SCALED_FEATURES]
    assert set(raw[binary_features]) <= {0, 1}
    np.testing.assert_array_equal(raw[binary_features], captured["model"].iloc[0][binary_features])


def test_processed_test_row_can_be_reconstructed_for_demo(inference_assets):
    scaler, _ = inference_assets
    X_test = pd.read_pickle(PROJECT_ROOT / "data" / "processed" / "X_test.pkl")
    processed_row = X_test.iloc[0]

    raw_transaction = reconstruct_transaction_input(processed_row, scaler)
    rebuilt = build_model_features(raw_transaction, scaler).iloc[0]

    assert raw_transaction["transaction_type"] in {"TRANSFER", "CASH_OUT"}
    assert np.allclose(
        rebuilt.loc[list(MODEL_FEATURES)].to_numpy(dtype=float),
        processed_row.loc[list(MODEL_FEATURES)].to_numpy(dtype=float),
        rtol=1e-7,
        atol=1e-7,
    )
