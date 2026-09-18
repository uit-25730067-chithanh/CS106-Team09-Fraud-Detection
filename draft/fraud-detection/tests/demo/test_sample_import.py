"""Tests for user-imported demo samples."""

from __future__ import annotations

import json

import pytest

from demo.sample_import import parse_sample_file


VALID_SAMPLE = {
    "type": "TRANSFER",
    "step": 120,
    "amount": 250000,
    "oldbalanceOrg": 1000000,
    "newbalanceOrig": 750000,
    "oldbalanceDest": 500000,
    "newbalanceDest": 750000,
    "isFraud": 0,
}


def test_parse_json_sample_with_paysim_columns():
    samples = parse_sample_file("demo.json", json.dumps(VALID_SAMPLE).encode())

    assert samples[0]["transaction"]["transaction_type"] == "TRANSFER"
    assert samples[0]["transaction"]["amount"] == 250000
    assert samples[0]["true_label"] == 0


def test_parse_csv_sample_with_app_columns():
    csv_content = (
        "transaction_type,step,amount,old_balance_origin,new_balance_origin,"
        "old_balance_destination,new_balance_destination,true_label\n"
        "CASH_OUT,435,1143937.73,1143937.73,0,0,0,1\n"
    ).encode()

    samples = parse_sample_file("cases.csv", csv_content)

    assert samples[0]["transaction"]["step"] == 435
    assert samples[0]["true_label"] == 1


def test_reject_invalid_sample_schema():
    with pytest.raises(ValueError, match="Thiếu trường bắt buộc"):
        parse_sample_file("invalid.json", b'{"type":"TRANSFER"}')
