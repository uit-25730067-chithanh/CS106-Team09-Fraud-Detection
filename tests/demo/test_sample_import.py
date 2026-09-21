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


def test_reject_nan_and_infinity():
    nan_sample = dict(VALID_SAMPLE, amount="NaN")
    with pytest.raises(ValueError, match="amount không hợp lệ"):
        parse_sample_file("nan.json", json.dumps(nan_sample).encode())

    inf_sample = dict(VALID_SAMPLE, amount="inf")
    with pytest.raises(ValueError, match="amount không hợp lệ"):
        parse_sample_file("inf.json", json.dumps(inf_sample).encode())


def test_reject_negative_values():
    neg_sample = dict(VALID_SAMPLE, amount=-100)
    with pytest.raises(ValueError, match="amount không được âm"):
        parse_sample_file("neg.json", json.dumps(neg_sample).encode())


def test_reject_out_of_range_and_non_integer_step():
    with pytest.raises(ValueError, match="step phải là số nguyên"):
        parse_sample_file("step0.json", json.dumps(dict(VALID_SAMPLE, step=0)).encode())

    with pytest.raises(ValueError, match="step phải là số nguyên"):
        parse_sample_file("step745.json", json.dumps(dict(VALID_SAMPLE, step=745)).encode())

    with pytest.raises(ValueError, match="step phải là số nguyên"):
        parse_sample_file("step_float.json", json.dumps(dict(VALID_SAMPLE, step=1.5)).encode())


def test_reject_unsupported_transaction_type():
    with pytest.raises(ValueError, match="type chỉ nhận TRANSFER hoặc CASH_OUT"):
        parse_sample_file("debit.json", json.dumps(dict(VALID_SAMPLE, type="DEBIT")).encode())


def test_reject_unsupported_file_extension():
    with pytest.raises(ValueError, match="Chỉ hỗ trợ file CSV hoặc JSON"):
        parse_sample_file("demo.txt", b"hello world")


def test_reject_invalid_true_label():
    with pytest.raises(ValueError, match="isFraud chỉ nhận 0 hoặc 1"):
        parse_sample_file("label.json", json.dumps(dict(VALID_SAMPLE, isFraud=2)).encode())


def test_reject_exceeding_max_samples():
    many_samples = [VALID_SAMPLE] * 51
    with pytest.raises(ValueError, match="tối đa 50 mẫu"):
        parse_sample_file("many.json", json.dumps(many_samples).encode())


def test_empty_sample_file():
    with pytest.raises(ValueError, match="File không có mẫu giao dịch"):
        parse_sample_file("empty.json", b"[]")


def test_empty_or_whitespace_title_falls_back():
    sample_empty_title = dict(VALID_SAMPLE, name="   ")
    samples = parse_sample_file("cases.json", json.dumps(sample_empty_title).encode())
    assert samples[0]["title"] == "cases · Mẫu 1"
