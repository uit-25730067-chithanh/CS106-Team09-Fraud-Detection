"""High-level regression test for the three Phase 06 workspaces."""

from __future__ import annotations

import tomllib
from pathlib import Path

import pytest

pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
APP_PATH = PROJECT_ROOT / "demo" / "app.py"


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
