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
    overview = next(item.value for item in app.table if "F1-score" in item.value.columns)
    interactive = next(item.value for item in app.dataframe if "f1_score" in item.value.columns)
    assert overview.shape == (5, 6)
    assert overview["F1-score"].tolist() == interactive["f1_score"].tolist()
    assert overview["Mô hình"].tolist() == interactive["model"].tolist()

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
    history = restarted_session.session_state["analysis_history"]
    summary_cards = list(restarted_session.metric)[:4]
    assert [card.label for card in summary_cards] == [
        "Đã phân tích", "Cảnh báo rủi ro", "Xác suất trung bình", "Lần gần nhất",
    ]
    assert [card.value for card in summary_cards] == [
        "1",
        str(history[0]["label"]),
        f"{history[0]['fraud_probability']:.2%}",
        f"{history[0]['fraud_probability']:.2%}",
    ]
    assert all(card.delta for card in summary_cards)


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
    app.button(key="open_sample_picker").click().run()
    sample_options = app.selectbox(key="sample_selector").options
    assert sample_options == [
        ":material/verified_user: Mô phỏng · Hợp lệ — dòng tiền cân đối",
        ":material/visibility: Mô phỏng · Cần lưu ý — chưa vượt ngưỡng",
        ":material/gpp_maybe: Mô phỏng · Nghi vấn gian lận — vượt ngưỡng",
    ]
    sample_count = len(sample_options)
    for index in range(sample_count):
        app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
        app.slider(key="decision_threshold_percent").set_value(10).run()
        assert app.session_state["decision_threshold_percent"] == 10
        app.button(key="open_sample_picker").click().run()
        assert app.session_state["decision_threshold_percent"] == 50
        app.selectbox(key="sample_selector").select_index(index)
        app.button(key="choose_sample").click().run()
        assert not app.exception
        assert app.session_state["decision_threshold_percent"] == 50
        assert app.session_state["last_transaction"] is None
        before = {
            "transaction_type": app.session_state["transaction_type_input"],
            "step": app.session_state["transaction_step_input"],
            "amount": app.session_state["transaction_amount_input"],
            "old_balance_origin": app.session_state["old_balance_origin"],
            "new_balance_origin": app.session_state["new_balance_origin"],
            "old_balance_destination": app.session_state["old_balance_destination"],
            "new_balance_destination": app.session_state["new_balance_destination"],
        }
        if index == 0:
            assert before["old_balance_origin"] >= before["amount"]
            assert abs(
                before["old_balance_origin"]
                - before["amount"]
                - before["new_balance_origin"]
            ) <= 0.05
            assert abs(
                before["old_balance_destination"]
                + before["amount"]
                - before["new_balance_destination"]
            ) <= 0.05
        app.button(key="analyze_transaction").click().run()
        assert not app.exception
        assert app.session_state["last_transaction"] == before
    app.button(key="nav_history").click().run()
    assert not app.exception
    assert len(app.session_state["analysis_history"]) == sample_count
    assert app.download_button[0].label == "Tải lịch sử CSV"
    app.button(key="nav_prediction").click().run()
    assert not app.exception
    assert app.session_state["transaction_step_input"] == before["step"]
    assert app.session_state["transaction_amount_input"] == before["amount"]


def pipeline_html(app):
    return next(
        element.proto.body for element in app.get("html")
        if 'id="analysis-pipeline-overview"' in element.proto.body
    )


def test_pipeline_tracks_current_input_and_threshold_without_saving_again():
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    assert 'data-state="idle"' in pipeline_html(app)
    assert any(item.value == "Quy trình phân tích" for item in app.subheader)
    assert all(app.button(key=f"pipeline_open_{index}").disabled for index in range(1, 5))
    assert any("Nhập thông tin và chọn Phân tích giao dịch" in item.value for item in app.caption)
    app.button(key="open_sample_picker").click().run()
    app.selectbox(key="sample_selector").select_index(0)
    app.button(key="choose_sample").click().run()
    assert app.session_state["last_transaction"] is None
    assert 'data-state="idle"' in pipeline_html(app)

    app.button(key="analyze_transaction").click().run()
    assert not app.exception
    assert 'data-state="complete"' in pipeline_html(app)
    assert any(item.value == "Quy trình phân tích" for item in app.subheader)
    assert "4/4 bước hoàn tất" not in pipeline_html(app)
    assert "Chọn một bước để khám phá cách xử lý." not in pipeline_html(app)
    for color, label in (
        ("violet", "7 trường đầu vào"),
        ("blue", "14 đặc trưng"),
        ("green", "1 dự đoán"),
    ):
        assert any(
            f":{color}-badge[" in item.value and label in item.value
            for item in app.markdown
        )
    assert all(not app.button(key=f"pipeline_open_{index}").disabled for index in range(1, 5))

    app.slider(key="decision_threshold_percent").set_value(70).run()
    assert 'data-state="complete"' in pipeline_html(app)
    assert any("Ngưỡng 70%" in item.value for item in app.caption)

    app.text_input(key="transaction_amount_input_text").set_value("300000").run()
    assert 'data-state="edited"' in pipeline_html(app)
    assert all(app.button(key=f"pipeline_open_{index}").disabled for index in range(1, 5))

    app.text_input(key="transaction_amount_input_text").set_value("1..000").run()
    assert 'data-state="invalid"' in pipeline_html(app)
    assert "4/4 bước hoàn tất" not in pipeline_html(app)
    assert app.button(key="analyze_transaction").disabled
    assert len(app.session_state["analysis_history"]) == 1
    assert not app.exception


def test_pipeline_does_not_claim_completion_when_inference_fails(monkeypatch):
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()

    def unavailable_model(*args, **kwargs):
        raise ValueError("Model unavailable for this test")

    monkeypatch.setattr("inference.predict_transaction", unavailable_model)
    app.button(key="analyze_transaction").click().run()
    assert not app.exception
    assert 'data-state="unavailable"' in pipeline_html(app)
    assert "4/4 bước hoàn tất" not in pipeline_html(app)
    assert any("Chờ dự đoán" in item.value for item in app.markdown)
    assert not any("1 dự đoán" in item.value for item in app.markdown)
    assert all(app.button(key=f"pipeline_open_{index}").disabled for index in range(1, 5))
    assert not app.session_state["analysis_history"]


@pytest.mark.parametrize("step", [1, 2, 3, 4])
def test_pipeline_opens_real_step_details_without_adding_history(step):
    app = AppTest.from_file(str(APP_PATH), default_timeout=30).run()
    app.button(key="analyze_transaction").click().run()
    app.button(key=f"pipeline_open_{step}").click().run()

    assert not app.exception
    assert app.session_state["pipeline_detail_step"] == step
    assert any(item.value.startswith(f"{step:02} · ") for item in app.subheader)
    assert len(app.session_state["analysis_history"]) == 1
    if step == 1:
        assert app.table[0].value.shape == (7, 2)
    elif step == 2:
        feature_table = next(
            item.value for item in app.table if "Trường mô hình" in item.value.columns
        )
        assert feature_table.shape == (14, 5)
        assert (feature_table["Xử lý"] == "StandardScaler").sum() == 10
    elif step == 3:
        assert {item.label for item in app.metric} >= {"Xác suất hợp lệ", "Xác suất gian lận"}
    else:
        assert app.table[0].value.shape == (2, 2)
