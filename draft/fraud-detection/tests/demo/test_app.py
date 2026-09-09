"""High-level regression test for the three Phase 06 workspaces."""

from __future__ import annotations

from pathlib import Path
from datetime import date, time

import pytest

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore[no-redef]

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_PATH = PROJECT_ROOT / "demo" / "app.py"


@pytest.fixture(autouse=True)
def isolate_persistent_history(monkeypatch, tmp_path):
    monkeypatch.setenv(
        "FRAUD_SHIELD_HISTORY_DB",
        str(tmp_path / "analysis_history.sqlite3"),
    )


def test_theme_config_is_loaded_from_documented_project_root():
    config_path = PROJECT_ROOT / ".streamlit" / "config.toml"

    with config_path.open("rb") as config_file:
        config = tomllib.load(config_file)

    assert config["theme"]["base"] == "dark"
    assert config["client"]["toolbarMode"] == "minimal"
    assert not (PROJECT_ROOT / "demo" / ".streamlit" / "config.toml").exists()


def test_primary_workspaces_render_without_exceptions():
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()

    assert not app.exception
    assert app.title[0].value == "Bản đồ tín hiệu giao dịch"

    app.button(key="nav_results").click().run()
    assert not app.exception
    assert app.session_state["active_view"] == "results"
    assert "Hiệu năng và mức sẵn sàng" in [item.value for item in app.subheader]

    app.button(key="nav_history").click().run()
    assert not app.exception
    assert app.session_state["active_view"] == "history"
    assert "Lịch sử phân tích" in [item.value for item in app.subheader]
    assert any(
        "Chưa có giao dịch nào" in item.value
        for item in app.markdown
    )


def test_performance_workspace_renders_all_figures_and_sampling_variants():
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    app.button(key="nav_results").click().run()

    assert not app.exception
    assert len(app.image) == 8  # Seven evaluation figures plus the sidebar logo.
    assert any("Đặc trưng quyết định mô hình" in item.value for item in app.markdown)
    assert any("So sánh TP, FP, FN của 5 biến thể" in item.value for item in app.markdown)
    assert any("Random Forest + SMOTENC" in item.value for item in app.markdown)
    assert any("XGBoost + SMOTENC" in item.value for item in app.markdown)

    app.button_group(key="confusion_sampling_method").set_value("ADASYN").run()

    assert not app.exception
    assert app.session_state["confusion_sampling_method"] == "ADASYN"
    assert any("Random Forest + ADASYN" in item.value for item in app.markdown)
    assert any("XGBoost + ADASYN" in item.value for item in app.markdown)
def test_threshold_slider_switches_visual_mode_at_boundaries():
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    slider = app.slider(key="decision_threshold_percent")
    assert slider.min == 10
    assert slider.max == 90
    assert slider.step == 1

    for threshold, expected_badge in (
        (35, "Ưu tiên phát hiện"),
        (40, "Cân bằng"),
        (60, "Cân bằng"),
        (65, "Giảm cảnh báo nhầm"),
    ):
        slider.set_value(threshold).run()
        assert not app.exception
        assert app.session_state["decision_threshold_percent"] == threshold
        assert any(expected_badge in item.value for item in app.markdown)
        slider = app.slider(key="decision_threshold_percent")


def test_datetime_and_money_submit_preserve_payload():
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    assert len(app.number_input) == 1
    app.date_input(key="transaction_date_input").set_value(date(2026, 1, 3)).run()
    app.time_input(key="transaction_time_input").set_value(time(5)).run()
    assert app.session_state["transaction_step_input"] == 53
    app.number_input(key="transaction_step_input").set_value(200).run()
    assert app.date_input(key="transaction_date_input").value == date(2026, 1, 9)
    assert app.time_input(key="transaction_time_input").value == time(8)
    app.text_input(key="transaction_amount_input_text").set_value("1143937,73").run()
    assert app.text_input(key="transaction_amount_input_text").value == "1.143.937,73"

    assert not app.button(key="analyze_transaction").disabled

    app.button(key="analyze_transaction").click().run()
    assert not app.exception
    assert app.session_state["last_transaction"]["step"] == 200
    assert app.session_state["last_transaction"]["amount"] == 1143937.73
    assert app.text_input(key="transaction_amount_input_text").value == "1.143.937,73"


def test_history_survives_new_app_session_and_renders_history_workspace():
    first_session = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    first_session.button(key="analyze_transaction").click().run()
    assert len(first_session.session_state["analysis_history"]) == 1

    restarted_session = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    assert len(restarted_session.session_state["analysis_history"]) == 1
    restarted_session.button(key="nav_history").click().run()
    assert not restarted_session.exception
    assert restarted_session.download_button[0].label == "Tải lịch sử CSV"


def test_invalid_input_blocks_analysis_and_recovers():
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    app.text_input(key="old_balance_origin_text").set_value("1..000").run()
    assert app.button(key="analyze_transaction").disabled
    app.text_input(key="old_balance_origin_text").set_value("1000000").run()
    assert not app.button(key="analyze_transaction").disabled
    app.time_input(key="transaction_time_input").set_value(time(0, 30)).run()
    assert app.button(key="analyze_transaction").disabled
    app.time_input(key="transaction_time_input").set_value(time(1)).run()
    assert not app.button(key="analyze_transaction").disabled
    assert not app.exception


def test_presets_and_labeled_cases_keep_exact_values_in_datetime_mode():
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    for preset in ("balanced", "mismatch", "large", "drain"):
        app.pills(key="preset_selector").set_value(preset).run()
        assert not app.exception
        before = dict(app.session_state["last_transaction"])
        app.button(key="analyze_transaction").click().run()
        assert not app.exception
        assert app.session_state["last_transaction"] == before
    selector = app.selectbox(key="test_case_selector")
    for index in range(len(selector.options)):
        app.selectbox(key="test_case_selector").select_index(index).run()
        assert not app.exception
        before = dict(app.session_state["last_transaction"])
        app.button(key="analyze_transaction").click().run()
        assert not app.exception
        assert app.session_state["last_transaction"] == before
    app.button(key="nav_history").click().run()
    assert not app.exception
    assert len(app.session_state["analysis_history"]) == len(selector.options) + 4
    assert app.download_button[0].label == "Tải lịch sử CSV"
    app.button(key="nav_prediction").click().run()
    assert not app.exception
    assert app.session_state["transaction_step_input"] == before["step"]
    assert app.session_state["transaction_amount_input"] == before["amount"]
