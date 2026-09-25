"""Streamlit UI shell for the CS106 fraud-detection project.

Run from ``draft/fraud-detection`` with::

    streamlit run demo/app.py

The Phase 06 version validates a transaction, reproduces the Phase 01 feature
contract and returns a real XGBoost fraud probability from the Phase 04 model.
"""

from __future__ import annotations

import os
import pickle
import re
import sqlite3
import sys
import warnings
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


DEMO_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = DEMO_DIR.parent
HISTORY_DATABASE_PATH = Path(
    os.environ.get(
        "FRAUD_SHIELD_HISTORY_DB",
        DEMO_DIR / ".data" / "analysis_history.sqlite3",
    )
)
DEFAULT_DECISION_THRESHOLD_PERCENT = 50
if str(DEMO_DIR) not in sys.path:
    sys.path.insert(0, str(DEMO_DIR))
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from src.utils import load_pickle_compat
except Exception:
    def load_pickle_compat(file_or_path):
        if hasattr(file_or_path, "read"):
            return pickle.load(file_or_path)
        with open(file_or_path, "rb") as f:
            return pickle.load(f)

from inference import (
    PredictionResult,
    load_xgboost_model,
    predict_transaction,
    reconstruct_transaction_input,
)
from analysis_pipeline import render_analysis_pipeline
from evaluation_artifacts import (
    EVALUATION_FIGURES,
    find_evaluation_figures,
    load_model_comparison,
    missing_evaluation_figures,
)
from input_formatting import (
    MIN_STEP, MAX_STEP, step_to_datetime, datetime_to_step,
    format_currency, parse_currency,
)
from history_store import (
    delete_analysis,
    load_analysis_history,
    save_analysis,
)
from sample_import import parse_sample_file


st.set_page_config(
    page_title="Fraud Shield",
    page_icon=":material/shield:",
    layout="wide",
    initial_sidebar_state="auto",
)

st.html(
    """
    <style>
    /* Shared tonal layers: a quiet panel, a raised card, and an input inset.
       Keep the violet identity without giving each section a different hue. */
    html {
        --fraud-panel-background: linear-gradient(145deg, #151a2c, #0f1322);
        --fraud-card-background: linear-gradient(145deg, #1b2133, #141927);
        --fraud-card-accent: #7486c7;
        --fraud-surface-border: rgba(119, 134, 178, 0.32);
        --fraud-surface-edge: rgba(191, 208, 255, 0.08);
        --fraud-panel-shadow: 0 16px 40px rgba(3, 2, 13, 0.28);
        --fraud-card-shadow: 0 8px 24px rgba(3, 2, 13, 0.20);
        --fraud-table-header: #20283a;
    }
    html[data-fraud-shield-theme="light"] {
        --fraud-panel-background: linear-gradient(145deg, #ffffff, #fcfbff);
        --fraud-card-background: linear-gradient(145deg, #ffffff, #f3f3fb);
        --fraud-surface-border: #d5d8e9;
        --fraud-surface-edge: rgba(255, 255, 255, 0.85);
        --fraud-panel-shadow: 0 12px 32px rgba(43, 38, 98, 0.06);
        --fraud-card-shadow: 0 6px 20px rgba(43, 38, 98, 0.05);
        --fraud-table-header: #eeeff8;
    }

    [data-testid="stMainMenuButton"],
    [data-testid="stMainMenuPopover"] {
        visibility: hidden !important;
        pointer-events: none !important;
    }

    /* Preserve a balanced reading width on 34-inch ultrawide displays while
       remaining fully fluid on laptops and smaller screens. */
    [data-testid="stMainBlockContainer"] {
        width: min(100%, 1760px);
        max-width: 1760px;
        margin-inline: auto;
        padding-inline: clamp(1rem, 2vw, 2.25rem);
        container-type: inline-size;
        container-name: fraud-main;
    }

    /* Native metrics remain accessible; the grid prevents content length
       and optional descriptions from changing sibling card dimensions. */
    .st-key-overview_metrics,
    .st-key-history_metrics,
    .st-key-model_status_metrics {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        grid-auto-rows: 1fr;
        align-items: stretch;
        gap: 1rem;
    }
    .st-key-model_status_metrics {
        grid-template-columns: repeat(3, minmax(0, 1fr));
    }
    :is(.st-key-overview_metrics, .st-key-history_metrics, .st-key-model_status_metrics)
        > [data-testid="stElementContainer"] {
        width: 100%;
        min-width: 0;
    }
    :is(.st-key-overview_metrics, .st-key-history_metrics, .st-key-model_status_metrics)
        [data-testid="stMetric"] {
        height: 100%;
        min-height: 9.6rem;
        padding: 1.1rem 1.15rem;
    }
    :is(.st-key-overview_metrics, .st-key-history_metrics, .st-key-model_status_metrics)
        [data-testid="stMetricLabel"] p {
        font-size: 0.95rem;
        font-weight: 600;
        white-space: normal;
    }
    :is(.st-key-overview_metrics, .st-key-history_metrics, .st-key-model_status_metrics)
        [data-testid="stMetricDelta"] {
        max-width: 100%;
        white-space: normal;
    }
    @container fraud-main (max-width: 1000px) {
        .st-key-overview_metrics, .st-key-history_metrics {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }
    @container fraud-main (max-width: 640px) {
        .st-key-model_status_metrics {
            grid-template-columns: minmax(0, 1fr);
        }
    }
    @container fraud-main (max-width: 520px) {
        .st-key-overview_metrics, .st-key-history_metrics {
            grid-template-columns: minmax(0, 1fr);
        }
    }

    .st-key-analyze_transaction {
        width: min(100%, 680px);
        margin-inline: auto;
    }

    .st-key-transaction_form [data-testid="stDateInput"] [data-baseweb="input"],
    .st-key-transaction_form [data-testid="stTextInputRootElement"],
    .st-key-transaction_form [data-testid="stNumberInputContainer"],
    .st-key-transaction_form [data-baseweb="select"] > div {
        min-height: 2.85rem;
    }

    .st-key-transaction_form [data-testid="stButtonGroup"] button[role="radio"],
    .st-key-analyze_transaction button {
        min-height: 2.85rem;
    }

    .st-key-result_panel {
        min-height: 220px;
        padding: 1.25rem !important;
    }

    .st-key-theme_mode_menu {
        position: fixed;
        left: 1.1rem;
        bottom: 1rem;
        z-index: 999;
        width: min(17.7rem, calc(100vw - 2.2rem));
    }

    .st-key-theme_mode_menu button {
        width: 100%;
        justify-content: flex-start;
        background: var(--fraud-card-background) !important;
        border: 1px solid var(--fraud-surface-border) !important;
        color: var(--st-text-color) !important;
    }

    .st-key-theme_bootstrap {
        position: absolute;
        width: 1px;
        height: 1px;
        overflow: hidden;
        visibility: hidden;
        pointer-events: none;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid color-mix(in srgb, var(--st-primary-color) 14%, var(--st-border-color));
        background:
            radial-gradient(circle at 18% 4%, color-mix(in srgb, var(--st-primary-color) 13%, transparent), transparent 25%),
            var(--st-secondary-background-color);
    }

    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        padding-bottom: 5.5rem;
    }

    .st-key-sidebar_brand {
        margin: 0.1rem 0 1.35rem;
        padding: 0.75rem;
        border: 1px solid color-mix(in srgb, var(--st-primary-color) 20%, var(--st-border-color));
        border-radius: 1.15rem;
        background: linear-gradient(135deg, color-mix(in srgb, var(--st-primary-color) 10%, var(--st-background-color)), var(--st-background-color));
        box-shadow: 0 12px 32px color-mix(in srgb, var(--st-primary-color) 8%, transparent);
    }

    .st-key-sidebar_brand [data-testid="stImage"] img {
        border-radius: 0.85rem;
        box-shadow: 0 8px 20px color-mix(in srgb, var(--st-primary-color) 22%, transparent);
    }

    .st-key-sidebar_brand p {
        margin: 0;
        line-height: 1.25;
    }

    [data-testid="stSidebar"] .stButton > button {
        justify-content: flex-start;
        min-height: 3.15rem;
        padding-inline: 1rem;
        border-radius: 0.9rem;
        font-size: 0.96rem;
        font-weight: 650;
        transition: transform 160ms ease, border-color 160ms ease, background 160ms ease, box-shadow 160ms ease;
    }

    [data-testid="stSidebar"] .stButton > button[kind="secondary"] {
        border-color: transparent;
        background: transparent;
        color: var(--st-text-color);
    }

    [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
        transform: translateX(3px);
        border-color: color-mix(in srgb, var(--st-primary-color) 22%, var(--st-border-color));
        background: color-mix(in srgb, var(--st-primary-color) 7%, var(--st-background-color));
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        position: relative;
        border-color: color-mix(in srgb, var(--st-primary-color) 70%, white);
        background: linear-gradient(112deg, #6d28d9, #4f46e5);
        box-shadow: 0 10px 24px color-mix(in srgb, var(--st-primary-color) 25%, transparent);
    }

    .st-key-sidebar_presets {
        margin-top: 1.15rem;
        padding-top: 1rem;
        border-top: 1px solid color-mix(in srgb, var(--st-primary-color) 15%, var(--st-border-color));
    }

    .risk-meter-card {
        --score-color: #22c55e;
        margin-bottom: 0.8rem;
        padding: 1rem;
        border: 1px solid color-mix(in srgb, var(--score-color) 36%, var(--st-border-color));
        border-radius: var(--st-base-radius);
        background: linear-gradient(135deg, color-mix(in srgb, var(--score-color) 7%, var(--st-secondary-background-color)), var(--st-background-color));
    }

    .risk-meter-card.risk-low { --score-color: #22c55e; }
    .risk-meter-card.risk-medium { --score-color: #f97316; }
    .risk-meter-card.risk-high { --score-color: #f43f5e; }

    .risk-meter-card .fraud-score-label,
    .risk-meter-card .fraud-score-title {
        color: var(--score-color) !important;
        -webkit-text-fill-color: var(--score-color) !important;
        opacity: 1 !important;
    }

    .risk-meter-head {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.9rem;
    }

    .fraud-score-label {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.46rem 0.76rem;
        border: 1px solid color-mix(in srgb, var(--score-color) 68%, #ffffff);
        border-radius: 999px;
        color: var(--score-color);
        background: linear-gradient(
            135deg,
            color-mix(in srgb, var(--score-color) 26%, #0b1220),
            color-mix(in srgb, var(--score-color) 42%, #111827)
        );
        font-size: 1.1rem;
        font-weight: 900;
        line-height: 1;
        letter-spacing: 0.075em;
        text-shadow:
            0 1px 2px rgba(0, 0, 0, 0.34),
            0 0 12px color-mix(in srgb, var(--score-color) 44%, transparent);
        box-shadow:
            0 0 0 1px color-mix(in srgb, var(--score-color) 22%, transparent),
            0 8px 24px color-mix(in srgb, var(--score-color) 32%, transparent),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }

    .fraud-score-label::before {
        content: "";
        width: 0.52rem;
        height: 0.52rem;
        flex: 0 0 0.52rem;
        border-radius: 50%;
        background: var(--score-color);
        box-shadow:
            0 0 0 4px color-mix(in srgb, var(--score-color) 18%, transparent),
            0 0 12px color-mix(in srgb, var(--score-color) 58%, transparent);
    }

    .fraud-score-title {
        margin: 0.58rem 0 0;
        color: var(--score-color);
        font: 800 1.55rem/1.2 var(--st-heading-font);
        letter-spacing: -0.025em;
        text-shadow: 0 0 18px color-mix(in srgb, var(--score-color) 24%, transparent);
    }

    .risk-meter-track {
        position: relative;
        height: 12px;
        margin: 2.25rem 0 1.65rem;
        border-radius: 999px;
        background: linear-gradient(90deg, #22c55e 0 35%, #f59e0b 62%, #e11d48 100%);
        box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--st-border-color) 64%, transparent);
    }

    .risk-meter-score-tag {
        position: absolute;
        z-index: 2;
        padding: 0.22rem 0.45rem;
        border-radius: 0.45rem;
        font-size: 0.75rem;
        font-weight: 800;
        line-height: 1;
        white-space: nowrap;
        transform: translateX(-50%);
    }

    .risk-meter-score-tag {
        left: clamp(2.1rem, calc(var(--score) * 1%), calc(100% - 2.1rem));
        bottom: calc(100% + 0.58rem);
        color: white;
        background: var(--score-color);
        box-shadow: 0 5px 14px color-mix(in srgb, var(--score-color) 30%, transparent);
    }

    .risk-meter-score-tag::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        border: 4px solid transparent;
        border-top-color: var(--score-color);
        transform: translateX(-50%);
    }

    .risk-meter-marker {
        position: absolute;
        top: 50%;
        left: clamp(1%, calc(var(--score) * 1%), 99%);
        width: 3px;
        height: 19px;
        border-radius: 999px;
        background: var(--st-text-color);
        box-shadow: 0 0 0 3px var(--st-background-color), 0 0 0 4px var(--score-color);
        transform: translate(-50%, -50%);
    }

    .risk-meter-threshold {
        position: absolute;
        top: -3px;
        bottom: -3px;
        left: clamp(1%, calc(var(--threshold) * 1%), 99%);
        width: 1px;
        border-left: 1px dashed color-mix(in srgb, var(--st-text-color) 48%, transparent);
    }

    .risk-meter-tick {
        position: absolute;
        top: 100%;
        left: calc(var(--tick) * 1%);
        width: 1px;
        height: 5px;
        background: color-mix(in srgb, var(--st-text-color) 36%, transparent);
        transform: translateX(-50%);
    }

    .risk-meter-axis {
        position: absolute;
        top: calc(100% + 0.48rem);
        left: 0;
        right: 0;
        display: flex;
        justify-content: space-between;
        color: var(--st-gray-text-color);
        font-size: 0.72rem;
        font-variant-numeric: tabular-nums;
    }

    .risk-meter-scale {
        display: flex;
        justify-content: space-between;
        color: var(--st-gray-text-color);
        font-size: 0.76rem;
        font-weight: 600;
    }

    @media (min-width: 1800px) {
        html {
            font-size: 16px;
        }

        [data-testid="stMainBlockContainer"] {
            width: min(100%, 1900px);
            max-width: 1900px;
            padding-inline: clamp(1.5rem, 2.2vw, 2.75rem);
        }

        .st-key-analyze_transaction {
            width: min(100%, 720px);
        }

        .st-key-result_panel {
            min-height: 232px;
        }
    }

    @media (max-width: 768px) {
        html {
            font-size: 14px;
        }

        [data-testid="stMainBlockContainer"] {
            width: 100%;
            padding-inline: 0.85rem;
        }

        [data-testid="stMainBlockContainer"] h1 {
            font-size: 2.25rem;
        }

        .st-key-result_panel {
            min-height: 190px;
            padding: 1rem !important;
        }

        .st-key-theme_mode_menu {
            left: 0.85rem;
            bottom: 0.75rem;
        }

        .risk-meter-head { align-items: flex-end; }
        .fraud-score-label {
            padding: 0.42rem 0.66rem;
            font-size: 0.96rem;
        }
        .fraud-score-title { font-size: 1.3rem; }
    }

    </style>
    """
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
_CODE_DIR = PROJECT_ROOT / "code"
PROCESSED_DATA_DIR = (
    (PROJECT_ROOT / "data" / "processed")
    if (PROJECT_ROOT / "data" / "processed").exists()
    else (_CODE_DIR / "data" / "processed")
)
_MODELS_DIR = (
    (PROJECT_ROOT / "models")
    if (PROJECT_ROOT / "models").exists()
    else (DEMO_DIR / "models")
)
SCALER_PATH = _MODELS_DIR / "scaler.pkl"
XGB_MODEL_PATH = _MODELS_DIR / "xgb_smote.json"
LOGO_PATH = DEMO_DIR / "assets" / "fraud-shield-logo.png"
_REPORTS_DIR = (
    (PROJECT_ROOT / "reports")
    if (PROJECT_ROOT / "reports").exists()
    else (_CODE_DIR / "reports")
)
COMPARISON_PATH = _REPORTS_DIR / "model_comparison.csv"
FIGURES_DIR = _REPORTS_DIR / "figures"
XGB_PREDICTIONS_PATH = _REPORTS_DIR / "xgb_predictions.pkl"
TRAINING_SUMMARIES = {
    "Random Forest": _REPORTS_DIR / "rf_smote_summary.txt",
    "XGBoost": _REPORTS_DIR / "xgb_smote_summary.txt",
    "Autoencoder": _REPORTS_DIR / "autoencoder_summary.txt",
}

THEME_SWITCHER = st.components.v2.component(
    "fraud_shield_theme_switcher",
    html="""
<div class="theme-picker" role="radiogroup" aria-label="Chọn chế độ giao diện">
  <button class="theme-option" data-theme="System" type="button" role="radio"
    aria-label="Dùng giao diện theo hệ thống">
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <rect x="3" y="4" width="18" height="13" rx="2"></rect>
      <path d="M8 21h8M12 17v4"></path>
    </svg>
    <span>System</span>
    <span class="theme-check" aria-hidden="true">✓</span>
  </button>
  <button class="theme-option" data-theme="Light" type="button" role="radio"
    aria-label="Dùng giao diện sáng">
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <circle cx="12" cy="12" r="4"></circle>
      <path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.65 17.65l1.42 1.42M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.65 6.35l1.42-1.42"></path>
    </svg>
    <span>Sáng</span>
    <span class="theme-check" aria-hidden="true">✓</span>
  </button>
  <button class="theme-option" data-theme="Dark" type="button" role="radio"
    aria-label="Dùng giao diện tối">
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M20.2 15.2A8.5 8.5 0 0 1 8.8 3.8 8.5 8.5 0 1 0 20.2 15.2Z"></path>
    </svg>
    <span>Tối</span>
    <span class="theme-check" aria-hidden="true">✓</span>
  </button>
</div>
<p id="theme-switcher-status" role="status" aria-live="polite"></p>
""",
    css="""
:host {
  display: block;
  min-width: 16rem;
}

.theme-picker {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.4rem;
  padding: 0.4rem;
  border: 1px solid var(--st-border-color);
  border-radius: var(--st-button-radius);
  background: var(--st-secondary-background-color);
}

.theme-option {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  min-height: 4.25rem;
  padding: 0.65rem 0.35rem;
  border: 1px solid transparent;
  border-radius: var(--st-button-radius);
  background: transparent;
  color: var(--st-text-color);
  font: 600 0.78rem/1 var(--st-font);
  cursor: pointer;
  transition: transform 120ms ease, background-color 120ms ease,
    box-shadow 120ms ease;
}

.theme-option:hover {
  transform: translateY(-1px);
  border-color: var(--st-primary-color);
}

.theme-option:focus-visible {
  outline: 3px solid var(--st-primary-color);
  outline-offset: 2px;
}

.theme-option.is-active {
  border-color: var(--st-primary-color);
  background: var(--st-primary-color);
  color: #ffffff;
  box-shadow: 0 0.35rem 1rem color-mix(in srgb, var(--st-primary-color) 32%, transparent);
}

.theme-option svg {
  width: 1.3rem;
  height: 1.3rem;
  fill: none;
  stroke: currentColor;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.theme-check {
  position: absolute;
  top: 0.28rem;
  right: 0.38rem;
  font-size: 0.65rem;
  opacity: 0;
  transform: scale(0.75);
  transition: opacity 120ms ease, transform 120ms ease;
}

.theme-option.is-active .theme-check {
  opacity: 1;
  transform: scale(1);
}

#theme-switcher-status {
  display: none;
  margin: 0.35rem 0 0;
  color: var(--st-orange-text-color);
  font: 500 0.74rem/1.35 var(--st-font);
}

#theme-switcher-status.is-visible {
  display: block;
}

@media (prefers-reduced-motion: reduce) {
  .theme-option,
  .theme-check {
    transition: none;
  }
}
""",
    js="""
export default function (component) {
  const { data, parentElement } = component
  const buttons = Array.from(parentElement.querySelectorAll("[data-theme]"))
  const status = parentElement.querySelector("#theme-switcher-status")
  if (buttons.length !== 3 || !status) return

  const modes = ["System", "Light", "Dark"]
  const storageKey = `fraudShieldTheme-${window.location.pathname}-v2`
  const appDocument = parentElement.ownerDocument
  const root = appDocument.documentElement
  const systemPreference = window.matchMedia("(prefers-color-scheme: dark)")
  const palettes = {
    Light: {
      primary: "#6D28D9",
      background: "#F4F6FB",
      secondary: "#FFFFFF",
      text: "#17213A",
      border: "#CBD5E1",
      gray: "#526078",
      blue: "#2563EB",
      green: "#16A34A",
      orange: "#EA580C",
      red: "#E11D48",
      violet: "#7C3AED",
      sidebar: "#140A2E",
      sidebarSecondary: "#24124A",
      sidebarText: "#F8FAFC",
      sidebarBorder: "#4C2A7A",
      inputBackground: "#F8FAFC",
      inputBorder: "rgba(99, 102, 241, 0.28)",
      inputHover: "#818CF8",
      inputFocus: "#6366F1",
      inputGlow: "rgba(99, 102, 241, 0.16)",
    },
    Dark: {
      primary: "#7C3AED",
      background: "#080B16",
      secondary: "#11162A",
      text: "#F8FAFC",
      border: "#2D3858",
      gray: "#94A3B8",
      blue: "#38BDF8",
      green: "#34D399",
      orange: "#FB923C",
      red: "#FB7185",
      violet: "#C084FC",
      sidebar: "#070914",
      sidebarSecondary: "#141127",
      sidebarText: "#F1F5F9",
      sidebarBorder: "#292F4B",
      inputBackground: "#121827",
      inputBorder: "rgba(129, 140, 248, 0.32)",
      inputHover: "#818CF8",
      inputFocus: "#8B5CF6",
      inputGlow: "rgba(139, 92, 246, 0.18)",
    },
  }
  const tokenNames = {
    primary: "--st-primary-color",
    background: "--st-background-color",
    secondary: "--st-secondary-background-color",
    text: "--st-text-color",
    border: "--st-border-color",
    gray: "--st-gray-text-color",
    blue: "--st-blue-color",
    green: "--st-green-color",
    orange: "--st-orange-color",
    red: "--st-red-color",
    violet: "--st-violet-color",
  }

  const styleId = "fraud-shield-live-theme"
  let liveStyle = appDocument.getElementById(styleId)
  if (!liveStyle) {
    liveStyle = appDocument.createElement("style")
    liveStyle.id = styleId
    liveStyle.textContent = `
      html[data-fraud-shield-theme] body,
      html[data-fraud-shield-theme] .stApp,
      html[data-fraud-shield-theme] [data-testid="stAppViewContainer"],
      html[data-fraud-shield-theme] [data-testid="stHeader"] {
        background-color: var(--st-background-color) !important;
        color: var(--st-text-color) !important;
        transition: background-color 160ms ease, color 160ms ease;
      }
      html[data-fraud-shield-theme] [data-testid="stSidebar"] {
        background-color: var(--fraud-sidebar-background) !important;
        color: var(--fraud-sidebar-text) !important;
        border-color: var(--fraud-sidebar-border) !important;
        transition: background-color 160ms ease, color 160ms ease;
      }
      html[data-fraud-shield-theme] [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
      html[data-fraud-shield-theme] [data-testid="stSidebar"] p,
      html[data-fraud-shield-theme] [data-testid="stSidebar"] span {
        color: inherit;
      }
      html[data-fraud-shield-theme] [data-testid="stExpandSidebarButton"] span {
        color: var(--st-text-color) !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stWidgetLabel"],
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stMetricLabel"],
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stMetricValue"] {
        color: var(--st-text-color) !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stMetricDelta"] {
        color: var(--st-gray-text-color) !important;
        background: color-mix(in srgb, var(--st-gray-text-color) 10%, transparent) !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stMetricDelta"] svg {
        fill: currentColor !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [class*="st-key-overview_metric_"] {
        --overview-metric-accent: var(--st-blue-color);
        height: 100%;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] .st-key-overview_metric_scope {
        --overview-metric-accent: var(--st-orange-color);
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] .st-key-overview_metric_features {
        --overview-metric-accent: var(--st-violet-color);
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] .st-key-overview_metric_model_ready {
        --overview-metric-accent: var(--st-green-color);
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] .st-key-overview_metric_model_unavailable {
        --overview-metric-accent: var(--st-orange-color);
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [class*="st-key-overview_metric_"] [data-testid="stMetricDelta"] {
        color: var(--overview-metric-accent) !important;
        background: color-mix(in srgb, var(--overview-metric-accent) 13%, transparent) !important;
        box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--overview-metric-accent) 20%, transparent);
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [class*="st-key-model_metric_"] {
        --model-metric-accent: var(--st-gray-text-color);
        height: 100%;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [class*="st-key-model_metric_rf_"] {
        --model-metric-accent: var(--st-blue-color);
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [class*="st-key-model_metric_xgb_"] {
        --model-metric-accent: var(--st-green-color);
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [class*="st-key-model_metric_autoencoder_"] {
        --model-metric-accent: var(--st-orange-color);
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [class*="st-key-model_metric_unavailable_"] {
        --model-metric-accent: var(--st-gray-text-color);
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [class*="st-key-model_metric_"] [data-testid="stMetricDelta"] {
        color: var(--model-metric-accent) !important;
        background: color-mix(in srgb, var(--model-metric-accent) 13%, transparent) !important;
        box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--model-metric-accent) 20%, transparent);
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] .st-key-dataset_fraud_metrics [data-testid="stMetricDelta"] {
        color: var(--st-green-color) !important;
        background: color-mix(in srgb, var(--st-green-color) 13%, transparent) !important;
        box-shadow: inset 0 0 0 1px color-mix(in srgb, var(--st-green-color) 20%, transparent);
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stNumberInputContainer"],
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stNumberInputStepDown"],
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stNumberInputStepUp"] {
        color: var(--st-text-color) !important;
        background: var(--st-secondary-background-color) !important;
        border-color: var(--st-border-color) !important;
      }
      html[data-fraud-shield-theme] .st-key-transaction_form [data-testid="stTextInputRootElement"],
      html[data-fraud-shield-theme] .st-key-transaction_form [data-baseweb="input"],
      html[data-fraud-shield-theme] .st-key-transaction_form [data-baseweb="base-input"],
      html[data-fraud-shield-theme] .st-key-transaction_form [data-baseweb="select"] > div {
        color: var(--st-text-color) !important;
        background: var(--fraud-input-background) !important;
        border-color: var(--fraud-input-border) !important;
        transition: border-color 140ms ease, box-shadow 140ms ease, background 140ms ease;
      }
      html[data-fraud-shield-theme] .st-key-transaction_form input,
      html[data-fraud-shield-theme] .st-key-transaction_form [data-testid="stTextInputIcon"],
      html[data-fraud-shield-theme] .st-key-transaction_form [data-baseweb="select"] [data-baseweb="value-container"],
      html[data-fraud-shield-theme] .st-key-transaction_form svg {
        color: var(--st-text-color) !important;
        -webkit-text-fill-color: var(--st-text-color) !important;
      }
      html[data-fraud-shield-theme] .st-key-transaction_form input {
        background: transparent !important;
        font-variant-numeric: tabular-nums;
      }
      html[data-fraud-shield-theme] .st-key-transaction_form input:disabled {
        opacity: 0.55;
      }
      html[data-fraud-shield-theme] .st-key-transaction_form [data-testid="stTextInputRootElement"]:focus-within {
        border-color: var(--fraud-input-focus) !important;
        box-shadow: 0 0 0 3px var(--fraud-input-glow) !important;
      }
      html[data-fraud-shield-theme] .st-key-transaction_form [data-testid="stTextInputRootElement"]:hover,
      html[data-fraud-shield-theme] .st-key-transaction_form [data-baseweb="input"]:hover,
      html[data-fraud-shield-theme] .st-key-transaction_form [data-baseweb="select"] > div:hover {
        border-color: var(--fraud-input-hover) !important;
      }
      html[data-fraud-shield-theme] .st-key-transaction_form [data-baseweb="input"]:focus-within,
      html[data-fraud-shield-theme] .st-key-transaction_form [data-baseweb="select"] > div:focus-within {
        border-color: var(--fraud-input-focus) !important;
        box-shadow: 0 0 0 3px var(--fraud-input-glow) !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stNumberInputField"] {
        color: var(--st-text-color) !important;
        background: transparent !important;
        -webkit-text-fill-color: var(--st-text-color) !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stButtonGroup"] button[role="radio"] {
        color: var(--st-text-color) !important;
        background: var(--st-background-color) !important;
        border-color: var(--st-border-color) !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stButtonGroup"] button[role="radio"][aria-checked="true"] {
        color: var(--st-violet-color) !important;
        background: color-mix(in srgb, var(--st-violet-color) 14%, var(--st-background-color)) !important;
        border-color: var(--st-primary-color) !important;
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] .stMarkdownBadge {
        color: #111827 !important;
        font-weight: 750 !important;
        letter-spacing: -0.01em;
        text-shadow: none !important;
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] .stMarkdownBadge[style*="124, 58, 237"] {
        background-color: #ede9fe !important;
        box-shadow: inset 0 0 0 1px #7c3aed, 0 5px 14px rgba(109, 40, 217, 0.15);
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] .stMarkdownBadge[style*="22, 163, 74"] {
        background-color: #d1fae5 !important;
        box-shadow: inset 0 0 0 1px #047857, 0 5px 14px rgba(4, 120, 87, 0.14);
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] .stMarkdownBadge[style*="37, 99, 235"] {
        background-color: #dbeafe !important;
        box-shadow: inset 0 0 0 1px #2563eb, 0 5px 14px rgba(37, 99, 235, 0.14);
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] .stMarkdownBadge[style*="100, 116, 139"] {
        background-color: #e2e8f0 !important;
        box-shadow: inset 0 0 0 1px #64748b, 0 5px 14px rgba(71, 85, 105, 0.13);
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] .stMarkdownBadge[style*="234, 88, 12"] {
        background-color: #ffedd5 !important;
        box-shadow: inset 0 0 0 1px #c2410c, 0 5px 14px rgba(194, 65, 12, 0.14);
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] .stMarkdownBadge[style*="225, 29, 72"] {
        background-color: #ffe4e6 !important;
        box-shadow: inset 0 0 0 1px #e11d48, 0 5px 14px rgba(225, 29, 72, 0.14);
      }
      html[data-fraud-shield-theme="light"] [data-testid="stAppViewContainer"] {
        background:
          radial-gradient(circle at 78% -8%, rgba(109, 40, 217, 0.12), transparent 30rem),
          linear-gradient(180deg, #f8faff 0%, #f2f5fb 100%) !important;
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] .st-key-hero_panel {
        background: linear-gradient(135deg, #ffffff 0%, #faf7ff 62%, #eef6ff 100%) !important;
        border-color: var(--fraud-surface-border) !important;
        box-shadow: 0 20px 48px rgba(43, 38, 98, 0.11) !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] :is(
        .st-key-result_panel, .st-key-transaction_form, .st-key-analysis_pipeline_panel,
        .st-key-evaluation_data_panel, [class*="st-key-evaluation_figure_"],
        .st-key-feature_importance_panel, .st-key-confusion_components_panel,
        .st-key-comparison_panel, .st-key-evaluation_pending_panel,
        .st-key-history_empty_panel, .st-key-history_chart_panel, .st-key-history_signal_panel
      ) {
        background: var(--fraud-panel-background) !important;
        border-color: var(--fraud-surface-border) !important;
        box-shadow: var(--fraud-panel-shadow), inset 0 1px 0 var(--fraud-surface-edge) !important;
      }
      html[data-fraud-shield-theme] [data-testid="stDialog"]:has(.st-key-sample_dialog) {
        align-items: center;
        justify-content: center;
        padding: 1rem;
        overflow: hidden;
        background: rgba(2, 6, 23, 0.72);
        backdrop-filter: blur(7px) saturate(0.86);
      }
      html[data-fraud-shield-theme] [role="dialog"]:has(.st-key-sample_dialog) {
        color: var(--st-text-color) !important;
        background: var(--fraud-panel-background) !important;
        border: 1px solid var(--fraud-surface-border) !important;
        max-height: min(820px, calc(100dvh - 2rem));
        overflow-y: auto;
        box-shadow: 0 24px 72px rgba(2, 6, 23, 0.48), inset 0 1px 0 var(--fraud-surface-edge) !important;
      }
      html[data-fraud-shield-theme] [role="dialog"]:has(.st-key-sample_dialog) [data-baseweb="select"] > div {
        color: var(--st-text-color) !important;
        background: var(--fraud-input-background) !important;
        border-color: var(--fraud-input-border) !important;
      }
      html[data-fraud-shield-theme] [role="dialog"]:has(.st-key-sample_dialog) .st-key-choose_sample button:not(:disabled) {
        color: #ffffff !important;
        background: linear-gradient(110deg, #1d4ed8, #2563eb) !important;
        border-color: #60a5fa !important;
        box-shadow: 0 7px 18px rgba(37, 99, 235, 0.24) !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stMetric"] {
        background: var(--fraud-card-background) !important;
        border: 1px solid var(--fraud-surface-border) !important;
        box-shadow: var(--fraud-card-shadow), inset 0 1px 0 var(--fraud-surface-edge) !important;
        font-variant-numeric: tabular-nums;
      }
      html[data-fraud-shield-theme] :is(
        [data-testid="stMainBlockContainer"], [role="dialog"]:has(.st-key-pipeline_dialog_1)
      ) [data-testid="stMetric"] {
        border-top: 2px solid var(--fraud-card-accent) !important;
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] [data-testid="stButtonGroup"] button[role="radio"] {
        color: #334155 !important;
        background: #ffffff !important;
        border-color: #cbd5e1 !important;
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] [data-testid="stButtonGroup"] button[role="radio"][aria-checked="true"] {
        color: #ffffff !important;
        background: #6d28d9 !important;
        border-color: #5b21b6 !important;
        box-shadow: 0 6px 16px rgba(109, 40, 217, 0.22) !important;
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] [data-testid="stNumberInputContainer"] {
        color: #17213a !important;
        background: #f8fafc !important;
        border-color: #b9c4d4 !important;
        box-shadow: inset 0 1px 2px rgba(15, 23, 42, 0.04), 0 2px 8px rgba(30, 41, 59, 0.05) !important;
        transition: border-color 140ms ease, box-shadow 140ms ease;
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] [data-testid="stNumberInputContainer"]:hover {
        border-color: #8b5cf6 !important;
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] [data-testid="stNumberInputContainer"]:focus-within {
        border-color: #6d28d9 !important;
        box-shadow: 0 0 0 3px rgba(109, 40, 217, 0.16), 0 5px 14px rgba(91, 33, 182, 0.12) !important;
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] [data-testid="stNumberInputField"] {
        color: #17213a !important;
        background: #f8fafc !important;
        -webkit-text-fill-color: #17213a !important;
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] [data-testid="stNumberInputStepDown"],
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] [data-testid="stNumberInputStepUp"] {
        color: #5b21b6 !important;
        background: #eef2ff !important;
      }
      html[data-fraud-shield-theme="dark"] [data-testid="stMainBlockContainer"] .stMarkdownBadge[style*="124, 58, 237"] {
        color: #c4b5fd !important;
        background-color: rgba(124, 58, 237, 0.22) !important;
      }
      html[data-fraud-shield-theme="dark"] [data-testid="stMainBlockContainer"] .stMarkdownBadge[style*="22, 163, 74"] {
        color: #6ee7b7 !important;
        background-color: rgba(16, 185, 129, 0.18) !important;
      }
      html[data-fraud-shield-theme="dark"] [data-testid="stMainBlockContainer"] .stMarkdownBadge[style*="37, 99, 235"] {
        color: #93c5fd !important;
        background-color: rgba(59, 130, 246, 0.19) !important;
      }
      html[data-fraud-shield-theme="dark"] [data-testid="stMainBlockContainer"] .stMarkdownBadge[style*="100, 116, 139"] {
        color: #cbd5e1 !important;
        background-color: rgba(148, 163, 184, 0.15) !important;
      }
      html[data-fraud-shield-theme="dark"] [data-testid="stMainBlockContainer"] .stMarkdownBadge[style*="234, 88, 12"] {
        color: #fdba74 !important;
        background-color: rgba(249, 115, 22, 0.2) !important;
        box-shadow: inset 0 0 0 1px rgba(251, 146, 60, 0.28);
      }
      html[data-fraud-shield-theme="dark"] [data-testid="stMainBlockContainer"] .stMarkdownBadge[style*="225, 29, 72"] {
        color: #fda4af !important;
        background-color: rgba(244, 63, 94, 0.2) !important;
        box-shadow: inset 0 0 0 1px rgba(251, 113, 133, 0.28);
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] :is(.st-key-workflow_steps, .st-key-pipeline_stats) {
        margin: 0.15rem 0 0.8rem;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] :is(.st-key-workflow_steps, .st-key-pipeline_stats) .stMarkdownBadge {
        min-height: 2rem;
        padding: 0.48rem 0.72rem;
        border-radius: 0.72rem;
        font-size: 0.9rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.012em;
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] :is(.st-key-workflow_steps, .st-key-pipeline_stats) .stMarkdownBadge {
        color: #111827 !important;
        transform: translateY(-1px);
        text-shadow: none !important;
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] :is(.st-key-workflow_steps, .st-key-pipeline_stats) .stMarkdownBadge[style*="124, 58, 237"] {
        background-color: #ede9fe !important;
        box-shadow: inset 0 0 0 2px #7c3aed, 0 7px 16px rgba(109, 40, 217, 0.16) !important;
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] :is(.st-key-workflow_steps, .st-key-pipeline_stats) .stMarkdownBadge[style*="37, 99, 235"] {
        background-color: #dbeafe !important;
        box-shadow: inset 0 0 0 2px #2563eb, 0 7px 16px rgba(37, 99, 235, 0.15) !important;
      }
      html[data-fraud-shield-theme="light"] [data-testid="stMainBlockContainer"] :is(.st-key-workflow_steps, .st-key-pipeline_stats) .stMarkdownBadge[style*="22, 163, 74"] {
        background-color: #d1fae5 !important;
        box-shadow: inset 0 0 0 2px #047857, 0 7px 16px rgba(4, 120, 87, 0.15) !important;
      }
      html[data-fraud-shield-theme="dark"] [data-testid="stAppViewContainer"] {
        background:
          radial-gradient(circle at 82% -8%, rgba(124, 58, 237, 0.16), transparent 31rem),
          radial-gradient(circle at 28% 58%, rgba(14, 165, 233, 0.055), transparent 28rem),
          #080b16 !important;
      }
      html[data-fraud-shield-theme="dark"] [data-testid="stMainBlockContainer"] .st-key-hero_panel {
        background: linear-gradient(135deg, rgba(20, 27, 46, 0.98), rgba(10, 15, 28, 0.99)) !important;
        border-color: rgba(119, 134, 178, 0.38) !important;
        box-shadow: 0 22px 54px rgba(2, 6, 18, 0.46), inset 0 1px 0 rgba(191, 208, 255, 0.08) !important;
      }
      html[data-fraud-shield-theme="dark"] [data-testid="stMainBlockContainer"] [data-testid="stWidgetLabel"] p {
        font-size: 0.94rem;
        font-weight: 650;
        letter-spacing: -0.008em;
      }
      html[data-fraud-shield-theme="dark"] [data-testid="stMainBlockContainer"] :is(h2, h3) {
        letter-spacing: -0.025em;
      }
      html[data-fraud-shield-theme="dark"] [data-testid="stMainBlockContainer"] [data-testid="stButtonGroup"] button[role="radio"][aria-checked="true"] {
        color: #ffffff !important;
        background: linear-gradient(110deg, #6d28d9, #7c3aed) !important;
        border-color: #a78bfa !important;
        box-shadow: 0 7px 18px rgba(124, 58, 237, 0.3) !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] .st-key-dataset_scope button[role="radio"][aria-checked="true"] {
        color: var(--st-text-color) !important;
        background: color-mix(in srgb, var(--st-blue-color) 16%, var(--fraud-input-background)) !important;
        border-color: var(--st-blue-color) !important;
        box-shadow: none !important;
      }
      html[data-fraud-shield-theme] .st-key-dataset_scope [role="radio"][aria-checked="true"] p {
        color: var(--st-text-color) !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stCaptionContainer"] {
        opacity: 1;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stCaptionContainer"] p {
        color: var(--st-gray-text-color);
        font-size: 0.9rem;
        line-height: 1.5;
      }
      html[data-fraud-shield-theme] .st-key-comparison_snapshot table {
        width: 100%;
        min-width: 680px;
        color: var(--st-text-color);
      }
      html[data-fraud-shield-theme] .st-key-comparison_snapshot :is(th, td) {
        background: var(--fraud-input-background);
        border-color: var(--fraud-surface-border);
        padding: 0.7rem 0.8rem;
        font-variant-numeric: tabular-nums;
      }
      html[data-fraud-shield-theme] .st-key-comparison_snapshot th {
        background: var(--fraud-table-header);
      }
      html[data-fraud-shield-theme] .st-key-comparison_snapshot :is(th, td) p {
        color: var(--st-text-color) !important;
      }
      html[data-fraud-shield-theme] .st-key-comparison_snapshot tbody tr:first-child td {
        background: color-mix(in srgb, var(--st-green-color) 7%, var(--fraud-input-background));
        font-weight: 650;
      }
      html[data-fraud-shield-theme] .st-key-comparison_panel :is([data-testid="stTable"] > div, details) {
        border-color: color-mix(in srgb, var(--st-gray-text-color) 35%, transparent);
      }
      html[data-fraud-shield-theme] .st-key-transaction_type_input [role="radiogroup"] > button:nth-of-type(1)[aria-checked="true"] {
        color: #ffffff !important;
        background: linear-gradient(110deg, #1d4ed8, #2563eb) !important;
        border-color: #60a5fa !important;
        box-shadow: 0 7px 18px rgba(37, 99, 235, 0.28) !important;
      }
      html[data-fraud-shield-theme] .st-key-transaction_type_input [role="radiogroup"] > button:nth-of-type(2)[aria-checked="true"] {
        color: #ffffff !important;
        background: linear-gradient(110deg, #b45309, #d97706) !important;
        border-color: #f59e0b !important;
        box-shadow: 0 6px 16px rgba(217, 119, 6, 0.2) !important;
      }
      html[data-fraud-shield-theme] .st-key-transaction_type_input [role="radiogroup"] > button[aria-checked="true"] * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
      }
      html[data-fraud-shield-theme] .st-key-confusion_sampling_method [role="radiogroup"] > button:first-of-type[aria-checked="true"] {
        color: #ffffff !important;
        background: linear-gradient(110deg, #1d4ed8, #2563eb) !important;
        border-color: #60a5fa !important;
        box-shadow: 0 7px 18px rgba(37, 99, 235, 0.24) !important;
      }
      html[data-fraud-shield-theme] .st-key-confusion_sampling_method [role="radiogroup"] > button:nth-of-type(2)[aria-checked="true"] {
        color: #ffffff !important;
        background: linear-gradient(110deg, #b45309, #d97706) !important;
        border-color: #f59e0b !important;
        box-shadow: 0 7px 18px rgba(217, 119, 6, 0.22) !important;
      }
      html[data-fraud-shield-theme] .st-key-confusion_sampling_method [role="radiogroup"] > button[aria-checked="true"] * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
      }
      html[data-fraud-shield-theme="dark"] [data-testid="stMainBlockContainer"] [data-testid="stNumberInputContainer"] {
        border-color: #493073 !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.035) !important;
        transition: border-color 140ms ease, box-shadow 140ms ease;
      }
      html[data-fraud-shield-theme="dark"] [data-testid="stMainBlockContainer"] [data-testid="stNumberInputContainer"]:hover {
        border-color: #7c3aed !important;
      }
      html[data-fraud-shield-theme="dark"] [data-testid="stMainBlockContainer"] [data-testid="stNumberInputContainer"]:focus-within {
        border-color: #a78bfa !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.18), 0 7px 18px rgba(3, 2, 13, 0.28) !important;
      }
      html[data-fraud-shield-theme] .st-key-transaction_form [data-testid="stNumberInputContainer"] {
        color: var(--st-text-color) !important;
        background: var(--fraud-input-background) !important;
        border-color: var(--fraud-input-border) !important;
        box-shadow: none !important;
      }
      html[data-fraud-shield-theme] .st-key-transaction_form [data-testid="stNumberInputField"] {
        color: var(--st-text-color) !important;
        background: transparent !important;
        -webkit-text-fill-color: var(--st-text-color) !important;
      }
      html[data-fraud-shield-theme] .st-key-transaction_form [data-testid="stNumberInputStepDown"],
      html[data-fraud-shield-theme] .st-key-transaction_form [data-testid="stNumberInputStepUp"] {
        color: var(--st-text-color) !important;
        background: transparent !important;
      }
      html[data-fraud-shield-theme] .st-key-transaction_form [data-testid="stNumberInputContainer"]:hover {
        border-color: var(--fraud-input-hover) !important;
      }
      html[data-fraud-shield-theme] .st-key-transaction_form [data-testid="stNumberInputContainer"]:focus-within {
        border-color: var(--fraud-input-focus) !important;
        box-shadow: 0 0 0 3px var(--fraud-input-glow) !important;
      }
      html[data-fraud-shield-theme] .st-key-analyze_transaction button:not(:disabled) {
        color: #ffffff !important;
        background: #047857 !important;
        border-color: #059669 !important;
        box-shadow: 0 4px 14px rgba(4, 120, 87, 0.18) !important;
      }
      html[data-fraud-shield-theme] .st-key-analyze_transaction button:not(:disabled):hover {
        background: #065f46 !important;
        border-color: #34d399 !important;
      }
      html[data-fraud-shield-theme] .st-key-analyze_transaction button:focus-visible {
        outline: 2px solid #34d399 !important;
        outline-offset: 3px;
      }
      @property --fraud-threshold-fill {
        syntax: "<percentage>";
        inherits: true;
        initial-value: 50%;
      }
      html[data-fraud-shield-theme="light"] .st-key-decision_threshold_percent[data-threshold-mode="detection"] {
        --fraud-threshold-color: #2563eb;
      }
      html[data-fraud-shield-theme="light"] .st-key-decision_threshold_percent[data-threshold-mode="balanced"] {
        --fraud-threshold-color: #16a34a;
      }
      html[data-fraud-shield-theme="light"] .st-key-decision_threshold_percent[data-threshold-mode="precision"] {
        --fraud-threshold-color: #d97706;
      }
      html[data-fraud-shield-theme="dark"] .st-key-decision_threshold_percent[data-threshold-mode="detection"] {
        --fraud-threshold-color: #38bdf8;
      }
      html[data-fraud-shield-theme="dark"] .st-key-decision_threshold_percent[data-threshold-mode="balanced"] {
        --fraud-threshold-color: #34d399;
      }
      html[data-fraud-shield-theme="dark"] .st-key-decision_threshold_percent[data-threshold-mode="precision"] {
        --fraud-threshold-color: #fb923c;
      }
      .st-key-decision_threshold_percent {
        transition: --fraud-threshold-fill 45ms linear;
      }
      .st-key-decision_threshold_percent [data-testid="stSlider"] [role="group"] > div > div:first-child {
        background: linear-gradient(
          to right,
          var(--fraud-threshold-color) 0%,
          var(--fraud-threshold-color) var(--fraud-threshold-fill),
          color-mix(in srgb, var(--fraud-threshold-color) 22%, var(--st-border-color)) var(--fraud-threshold-fill),
          color-mix(in srgb, var(--fraud-threshold-color) 22%, var(--st-border-color)) 100%
        ) !important;
      }
      .st-key-decision_threshold_percent [data-testid="stSlider"] [role="group"] > div > div:nth-child(2) {
        background: var(--fraud-threshold-color) !important;
        box-shadow: 0 0 0 4px color-mix(in srgb, var(--fraud-threshold-color) 18%, transparent) !important;
      }
      .st-key-decision_threshold_percent [data-testid="stSliderThumbValue"] p {
        color: var(--fraud-threshold-color) !important;
        font-weight: 800;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stVegaLiteChart"] svg.marks {
        background-color: transparent !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stVegaLiteChart"] svg text {
        fill: var(--st-text-color) !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stVegaLiteChart"] svg .role-axis-grid line {
        stroke: var(--st-border-color) !important;
        stroke-opacity: 0.55 !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stAlert"] {
        color: var(--st-text-color) !important;
        border-color: var(--st-border-color) !important;
      }
      html[data-fraud-shield-theme] [data-testid="stMainBlockContainer"] [data-testid="stAlert"] * {
        color: inherit !important;
      }
    `
    appDocument.head.appendChild(liveStyle)
  }

  const readStoredTheme = () => {
    try {
      const storedTheme = window.localStorage.getItem(storageKey)
      return modes.includes(storedTheme) ? storedTheme : null
    } catch {
      return null
    }
  }

  let activeTheme = readStoredTheme() ?? "Dark"

  const setActiveTheme = (theme) => {
    activeTheme = theme
    buttons.forEach((button) => {
      const isActive = button.dataset.theme === theme
      button.classList.toggle("is-active", isActive)
      button.setAttribute("aria-checked", String(isActive))
    })
  }

  const applyTheme = (theme) => {
    const resolvedMode = theme === "System"
      ? (systemPreference.matches ? "Dark" : "Light")
      : theme
    const palette = palettes[resolvedMode]

    Object.entries(tokenNames).forEach(([name, token]) => {
      root.style.setProperty(token, palette[name])
    })
    root.style.setProperty("--fraud-sidebar-background", palette.sidebar)
    root.style.setProperty("--fraud-sidebar-secondary", palette.sidebarSecondary)
    root.style.setProperty("--fraud-sidebar-text", palette.sidebarText)
    root.style.setProperty("--fraud-sidebar-border", palette.sidebarBorder)
    root.style.setProperty("--fraud-input-background", palette.inputBackground)
    root.style.setProperty("--fraud-input-border", palette.inputBorder)
    root.style.setProperty("--fraud-input-hover", palette.inputHover)
    root.style.setProperty("--fraud-input-focus", palette.inputFocus)
    root.style.setProperty("--fraud-input-glow", palette.inputGlow)
    root.dataset.fraudShieldTheme = resolvedMode.toLowerCase()
    root.style.colorScheme = resolvedMode.toLowerCase()

    const sidebar = appDocument.querySelector('[data-testid="stSidebar"]')
    if (sidebar) {
      sidebar.style.setProperty("--st-background-color", palette.sidebar)
      sidebar.style.setProperty("--st-secondary-background-color", palette.sidebarSecondary)
      sidebar.style.setProperty("--st-text-color", palette.sidebarText)
      sidebar.style.setProperty("--st-border-color", palette.sidebarBorder)
    }
  }

  const showFallback = () => {
    status.textContent = "Trình duyệt đang chặn lưu lựa chọn giao diện."
    status.classList.add("is-visible")
  }

  const selectTheme = (theme) => {
    status.classList.remove("is-visible")
    if (!modes.includes(theme) || theme === activeTheme) return

    try {
      window.localStorage.setItem(storageKey, theme)
      setActiveTheme(theme)
      applyTheme(theme)
    } catch {
      showFallback()
    }
  }

  setActiveTheme(activeTheme)
  applyTheme(activeTheme)
  buttons.forEach((button) => {
    button.onclick = () => selectTheme(button.dataset.theme)
  })

  const syncSystemTheme = () => {
    if (activeTheme === "System") applyTheme("System")
  }
  systemPreference.addEventListener("change", syncSystemTheme)

  return () => {
    systemPreference.removeEventListener("change", syncSystemTheme)
    buttons.forEach((button) => {
      button.onclick = null
    })
  }
}
""",
)

THRESHOLD_SLIDER_ENHANCER = st.components.v2.component(
    "fraud_shield_threshold_slider_enhancer",
    html="""
<span class="threshold-slider-enhancer" aria-hidden="true"></span>
""",
    css="""
:host,
.threshold-slider-enhancer {
  display: block;
  width: 0;
  height: 0;
  overflow: hidden;
}
""",
    js="""
export default function (component) {
  const { data, parentElement } = component
  const appDocument = parentElement.ownerDocument
  let wrapper = null
  let slider = null
  let sliderObserver = null

  const syncVisualState = () => {
    if (!wrapper || !slider) return
    const rawValue = slider.value || data?.value
    const value = Number(rawValue)
    if (!Number.isFinite(value)) return

    const fill = Math.min(100, Math.max(0, ((value - 10) / 80) * 100))
    wrapper.style.setProperty("--fraud-threshold-fill", `${fill}%`)
    wrapper.dataset.thresholdMode = value < 40
      ? "detection"
      : value <= 60 ? "balanced" : "precision"
  }

  const detachSlider = () => {
    sliderObserver?.disconnect()
    sliderObserver = null
    slider?.removeEventListener("input", syncVisualState)
    slider?.removeEventListener("change", syncVisualState)
  }

  const connectSlider = () => {
    const nextWrapper = appDocument.querySelector(
      ".st-key-decision_threshold_percent"
    )
    const nextSlider = nextWrapper?.querySelector('input[type="range"]')
    if (!nextWrapper || !nextSlider) return
    if (slider === nextSlider) {
      syncVisualState()
      return
    }

    detachSlider()
    wrapper = nextWrapper
    slider = nextSlider
    slider.addEventListener("input", syncVisualState, { passive: true })
    slider.addEventListener("change", syncVisualState, { passive: true })
    sliderObserver = new MutationObserver(syncVisualState)
    sliderObserver.observe(slider, {
      attributes: true,
      attributeFilter: ["value"],
    })
    syncVisualState()
  }

  const documentObserver = new MutationObserver(connectSlider)
  documentObserver.observe(appDocument.body, {
    childList: true,
    subtree: true,
  })
  connectSlider()

  return () => {
    documentObserver.disconnect()
    detachSlider()
  }
}
""",
)

HISTORY_TABLE = st.components.v2.component(
    "fraud_shield_history_table",
    html="""
<div class="history-table-shell">
  <div class="history-table" role="table" aria-label="Chi tiết lịch sử giao dịch">
    <div class="history-grid history-header" role="row">
      <div role="columnheader">Lần</div>
      <div role="columnheader">Loại giao dịch</div>
      <div role="columnheader">Ngày giờ minh họa</div>
      <div role="columnheader">Số tiền</div>
      <div role="columnheader">Xác suất</div>
      <div role="columnheader">Ngưỡng</div>
      <div role="columnheader">Kết quả</div>
      <div role="columnheader">Lưu ý dữ liệu</div>
      <div role="columnheader">Xóa</div>
    </div>
    <div class="history-body"></div>
  </div>
</div>
""",
    css="""
:host {
  display: block;
  width: 100%;
  color: var(--st-text-color);
  font-family: var(--st-font);
}
.history-table-shell {
  --history-text: #17213a;
  --history-surface: var(--fraud-panel-background);
  --history-border: var(--fraud-surface-border);
  --history-divider: color-mix(in srgb, var(--fraud-surface-border) 65%, transparent);
  --history-row: var(--fraud-input-background);
  --history-hover: color-mix(in srgb, var(--history-text) 5%, var(--history-row));
  --history-track: #e2e8f0;
  --history-shadow: rgba(30, 41, 59, .09);
  width: 100%;
  overflow-x: auto;
  color: var(--history-text);
  border: 1px solid var(--history-border);
  border-radius: 1.15rem;
  background: var(--history-surface);
  box-shadow: 0 10px 28px var(--history-shadow);
}
.history-table-shell[data-theme="dark"] {
  --history-text: #f8fafc;
  --history-track: #35344d;
  --history-shadow: rgba(3, 2, 13, .42);
}
.history-table {
  min-width: 900px;
  width: 100%;
}
.history-grid {
  display: grid;
  grid-template-columns: .55fr 1.05fr 1.3fr .85fr 1.35fr .75fr .8fr 1fr 64px;
  align-items: center;
}
.history-header {
  min-height: 40px;
  color: var(--history-text);
  background: var(--fraud-table-header);
  border-bottom: 1px solid var(--history-border);
  font-size: .9rem;
  font-weight: 650;
}
.history-header > div,
.history-row > div {
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 0;
  height: 100%;
  padding: .55rem .45rem;
  text-align: center;
  border-right: 1px solid var(--history-divider);
}
.history-header > div:last-child,
.history-row > div:last-child {
  border-right: 0;
}
.history-row {
  min-height: 46px;
  font-size: .92rem;
  background: var(--history-row);
  border-bottom: 1px solid var(--history-divider);
  transition: background 140ms ease;
}
.history-row:last-child { border-bottom: 0; }
.history-row:hover {
  background: var(--history-hover);
}
.probability-cell { gap: .5rem; }
.probability-track {
  flex: 1;
  min-width: 44px;
  height: 6px;
  overflow: hidden;
  border-radius: 999px;
  background: var(--history-track);
}
.probability-fill {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: linear-gradient(90deg, #2563eb, #38bdf8);
}
.delete-button {
  display: grid;
  place-items: center;
  width: 30px;
  height: 30px;
  padding: 0;
  color: color-mix(in srgb, var(--history-text) 76%, #ef4444);
  border: 0;
  border-radius: .55rem;
  background: transparent;
  cursor: pointer;
  transition: color 140ms ease, background 140ms ease, transform 140ms ease;
}
.delete-button:hover {
  color: #ef4444;
  background: color-mix(in srgb, #ef4444 12%, transparent);
  transform: translateY(-1px);
}
.delete-button:focus-visible {
  outline: 2px solid #38bdf8;
  outline-offset: 2px;
}
.delete-button svg { width: 17px; height: 17px; }
@media (max-width: 760px) {
  .history-table { min-width: 820px; }
  .history-header, .history-row { font-size: .86rem; }
}
""",
    js="""
export default function (component) {
  const { data, parentElement, setTriggerValue } = component
  const body = parentElement.querySelector(".history-body")
  const shell = parentElement.querySelector(".history-table-shell")
  if (!body || !shell) return
  const appRoot = parentElement.ownerDocument.documentElement
  const syncTheme = () => {
    shell.dataset.theme = appRoot.dataset.fraudShieldTheme === "dark"
      ? "dark"
      : "light"
  }
  const themeObserver = new MutationObserver(syncTheme)
  themeObserver.observe(appRoot, {
    attributes: true,
    attributeFilter: ["data-fraud-shield-theme"],
  })
  syncTheme()
  body.replaceChildren()

  const textCell = (value, className = "") => {
    const cell = document.createElement("div")
    cell.className = className
    cell.textContent = String(value ?? "")
    return cell
  }

  for (const item of data?.rows ?? []) {
    const row = document.createElement("div")
    row.className = "history-grid history-row"
    row.setAttribute("role", "row")
    row.append(textCell(item.sequence))
    row.append(textCell(item.transaction_type))
    row.append(textCell(item.simulated_datetime))
    row.append(textCell(item.amount))

    const probability = document.createElement("div")
    probability.className = "probability-cell"
    const track = document.createElement("span")
    track.className = "probability-track"
    const fill = document.createElement("span")
    fill.className = "probability-fill"
    fill.style.width = `${Math.min(100, Math.max(0, Number(item.probability_value) * 100))}%`
    track.append(fill)
    probability.append(track, document.createTextNode(item.probability))
    row.append(probability)

    row.append(textCell(item.threshold))
    row.append(textCell(item.result))
    row.append(textCell(item.quality_warnings))

    const action = document.createElement("div")
    const button = document.createElement("button")
    button.type = "button"
    button.className = "delete-button"
    button.title = `Xóa giao dịch #${item.sequence}`
    button.setAttribute("aria-label", button.title)
    button.innerHTML = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12Zm3.46-7.12 1.41-1.41L12 11.59l1.12-1.12 1.41 1.41L13.41 13l1.12 1.12-1.41 1.41L12 14.41l-1.12 1.12-1.41-1.41L10.59 13l-1.13-1.12ZM15.5 4l-1-1h-5l-1 1H5v2h14V4z"/></svg>'
    button.onclick = () => setTriggerValue("deleted", Number(item.sequence))
    action.append(button)
    row.append(action)
    body.append(row)
  }

  return () => {
    themeObserver.disconnect()
    body.querySelectorAll("button").forEach((button) => { button.onclick = null })
  }
}
""",
)

TRANSACTION_TYPES = ("TRANSFER", "CASH_OUT")
TRANSACTION_LABELS = {
    "TRANSFER": "Chuyển khoản",
    "CASH_OUT": "Rút tiền",
}


@dataclass(frozen=True)
class TransactionInput:
    """Raw values entered by a user before preprocessing."""

    transaction_type: str
    step: int
    amount: float
    old_balance_origin: float
    new_balance_origin: float
    old_balance_destination: float
    new_balance_destination: float

    @property
    def origin_difference(self) -> float:
        """Return the engineered source-account balance difference."""

        return self.old_balance_origin - self.amount - self.new_balance_origin

    @property
    def destination_difference(self) -> float:
        """Return the engineered destination-account balance difference."""

        return (
            self.old_balance_destination
            + self.amount
            - self.new_balance_destination
        )


TRANSACTION_PRESETS = {
    "safe": {
        "title": "Hợp lệ — dòng tiền cân đối",
        "eyebrow": "Mẫu mô phỏng · Model phân loại hợp lệ",
        "description": (
            "Giao dịch chuyển khoản 250.000 đơn vị có số dư hai phía cân đối "
            "và xác suất rủi ro rất thấp."
        ),
        "icon": ":material/verified_user:",
        "color": "green",
        "transaction": TransactionInput(
            transaction_type="TRANSFER",
            step=120,
            amount=250_000.0,
            old_balance_origin=1_000_000.0,
            new_balance_origin=750_000.0,
            old_balance_destination=500_000.0,
            new_balance_destination=750_000.0,
        ),
    },
    "watchlist": {
        "title": "Cần lưu ý — chưa vượt ngưỡng",
        "eyebrow": "Mẫu mô phỏng · Model phân loại hợp lệ",
        "description": (
            "Giao dịch chuyển khoản 2.500.000 đơn vị có dòng tiền cân đối, "
            "dùng để minh họa vùng cần lưu ý; đây không phải mẫu có nhãn thật "
            "và model vẫn phân loại hợp lệ ở ngưỡng 50%."
        ),
        "icon": ":material/visibility:",
        "color": "orange",
        "transaction": TransactionInput(
            transaction_type="TRANSFER",
            step=720,
            amount=2_500_000.0,
            old_balance_origin=3_000_000.0,
            new_balance_origin=500_000.0,
            old_balance_destination=500_000.0,
            new_balance_destination=3_000_000.0,
        ),
    },
    "high_risk": {
        "title": "Nghi vấn gian lận — vượt ngưỡng",
        "eyebrow": "Mẫu mô phỏng · Model gắn cờ rà soát",
        "description": (
            "Giao dịch lớn rút 2.000.000 đơn vị khi số dư nguồn chỉ có "
            "1.600.000, tạo sai lệch rõ ràng và được model gắn cờ ở ngưỡng 50%."
        ),
        "icon": ":material/gpp_maybe:",
        "color": "red",
        "transaction": TransactionInput(
            transaction_type="CASH_OUT",
            step=70,
            amount=2_000_000.0,
            old_balance_origin=1_600_000.0,
            new_balance_origin=0.0,
            old_balance_destination=2_000_000.0,
            new_balance_destination=4_000_000.0,
        ),
    },
}

DEMO_SAMPLE_ORDER = (
    ("preset", "safe"),
    ("preset", "watchlist"),
    ("preset", "high_risk"),
)


@dataclass(frozen=True)
class DatasetSummary:
    """Verified class counts loaded from the committed processed labels."""

    train_total: int
    train_fraud: int
    test_total: int
    test_fraud: int

    @property
    def total(self) -> int:
        return self.train_total + self.test_total

    @property
    def fraud(self) -> int:
        return self.train_fraud + self.test_fraud

    @property
    def normal(self) -> int:
        return self.total - self.fraud

    @property
    def fraud_ratio(self) -> float:
        return self.fraud / self.total if self.total else 0.0


@dataclass(frozen=True)
class LabeledTestCase:
    """One real held-out transaction reconstructed for an explainable demo."""

    title: str
    description: str
    transaction: TransactionInput
    true_label: int
    reference_probability: float
    test_position: int


@st.cache_resource(show_spinner=False)
def load_scaler(path: Path):
    """Load the Phase 01 scaler and report a library-version mismatch."""

    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always")
        with path.open("rb") as scaler_file:
            scaler = load_pickle_compat(scaler_file)

    has_version_mismatch = any(
        item.category.__name__ == "InconsistentVersionWarning"
        for item in caught_warnings
    )
    return scaler, has_version_mismatch


@st.cache_resource(show_spinner=False)
def load_prediction_model(path: Path):
    """Load one deployable model once per Streamlit process."""

    return load_xgboost_model(path)


def run_transaction_inference(
    transaction: TransactionInput,
    threshold: float,
) -> tuple[PredictionResult | None, str | None]:
    """Run inference fail-closed and return a user-facing error when unavailable."""

    try:
        scaler, _ = load_scaler(SCALER_PATH)
        model = load_prediction_model(XGB_MODEL_PATH)
        result = predict_transaction(
            asdict(transaction),
            scaler,
            model,
            threshold=threshold,
        )
    except (FileNotFoundError, ImportError, OSError, TypeError, ValueError) as error:
        return None, str(error)
    return result, None


@st.cache_data(show_spinner=False)
def load_dataset_summary(data_dir: Path) -> DatasetSummary:
    """Load only label artifacts and derive display statistics from real data."""

    y_train = pd.read_pickle(data_dir / "y_train.pkl")
    y_test = pd.read_pickle(data_dir / "y_test.pkl")

    return DatasetSummary(
        train_total=len(y_train),
        train_fraud=int(y_train.sum()),
        test_total=len(y_test),
        test_fraud=int(y_test.sum()),
    )


@st.cache_resource(show_spinner=False)
def load_labeled_test_cases(
    data_dir: Path,
    predictions_path: Path,
    scaler_path: Path,
) -> dict[str, LabeledTestCase]:
    """Load four deterministic XGBoost outcomes from the held-out test set."""

    X_test = pd.read_pickle(data_dir / "X_test.pkl").reset_index(drop=True)
    y_test = pd.Series(pd.read_pickle(data_dir / "y_test.pkl")).reset_index(drop=True)
    with predictions_path.open("rb") as predictions_file:
        prediction_artifact = load_pickle_compat(predictions_file)["xgb_smote"]
    y_pred = pd.Series(prediction_artifact["y_pred"])
    y_prob = pd.Series(prediction_artifact["y_prob"])

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        with scaler_path.open("rb") as scaler_file:
            scaler = load_pickle_compat(scaler_file)

    # Prefer an actual held-out normal transaction whose money flow is easy to
    # verify during a demo. PaySim contains legitimate rows with incomplete
    # source balances, so the lowest-risk row alone is not always intuitive.
    scaler_features = tuple(scaler.feature_names_in_)
    reconstructed_numeric = pd.DataFrame(
        scaler.inverse_transform(X_test.loc[:, scaler_features]),
        columns=scaler_features,
    )
    origin_balance_error = (
        reconstructed_numeric["oldbalanceOrg"]
        - reconstructed_numeric["amount"]
        - reconstructed_numeric["newbalanceOrig"]
    ).abs()
    destination_balance_error = (
        reconstructed_numeric["oldbalanceDest"]
        + reconstructed_numeric["amount"]
        - reconstructed_numeric["newbalanceDest"]
    ).abs()
    display_balances = reconstructed_numeric[
        [
            "oldbalanceOrg",
            "newbalanceOrig",
            "oldbalanceDest",
            "newbalanceDest",
        ]
    ]
    explainable_normal_mask = (
        (y_test == 0)
        & (y_pred == 0)
        & (origin_balance_error <= 0.05)
        & (destination_balance_error <= 0.05)
        & (
            reconstructed_numeric["oldbalanceOrg"]
            >= reconstructed_numeric["amount"]
        )
        & reconstructed_numeric["amount"].between(25_000, 250_000)
        & (display_balances.max(axis=1) <= 1_000_000)
    )
    explainable_fraud_mask = (
        (y_test == 1)
        & (y_pred == 1)
        & y_prob.between(0.95, 0.99995)
        & (reconstructed_numeric["amount"].between(50_000, 500_000))
        & (reconstructed_numeric["oldbalanceOrg"] > 0)
        & (reconstructed_numeric["newbalanceOrig"].abs() <= 0.05)
        & (reconstructed_numeric["oldbalanceDest"] > 0)
        & (reconstructed_numeric["newbalanceDest"] > 0)
        & (origin_balance_error <= 0.05)
        & (destination_balance_error <= 0.05)
    )

    definitions = (
        (
            "true_negative",
            "Hợp lệ — dòng tiền cân đối",
            "Số dư nguồn giảm và số dư đích tăng đúng bằng số tiền giao dịch; nhãn thật và dự đoán đều hợp lệ.",
            explainable_normal_mask,
            "min",
        ),
        (
            "true_positive",
            "Phát hiện gian lận",
            "Nhãn thật 1; giao dịch rút cạn tài khoản có dòng tiền cân đối và được mô hình phát hiện ở ngưỡng 50%.",
            explainable_fraud_mask,
            "min",
        ),
        (
            "false_positive",
            "Cảnh báo nhầm — đối chứng",
            "Nhãn thật 0 nhưng mô hình gắn cờ ở ngưỡng 50%.",
            (y_test == 0) & (y_pred == 1),
            "max",
        ),
        (
            "false_negative",
            "Bỏ sót gian lận",
            "Nhãn thật 1 nhưng mô hình chưa phát hiện ở ngưỡng 50%.",
            (y_test == 1) & (y_pred == 0),
            "min",
        ),
    )

    cases: dict[str, LabeledTestCase] = {}
    for key, title, description, mask, probability_order in definitions:
        candidates = y_prob[mask]
        if candidates.empty:
            continue
        position = int(
            candidates.idxmin() if probability_order == "min" else candidates.idxmax()
        )
        raw_values = reconstruct_transaction_input(X_test.iloc[position], scaler)
        cases[key] = LabeledTestCase(
            title=title,
            description=description,
            transaction=TransactionInput(**raw_values),
            true_label=int(y_test.iloc[position]),
            reference_probability=float(y_prob.iloc[position]),
            test_position=position,
        )
    return cases


@st.cache_data(show_spinner=False)
def load_training_metrics(path: Path) -> dict[str, float]:
    """Read existing Phase 03/04 metrics without inventing evaluation data."""

    content = path.read_text(encoding="utf-8")
    metrics: dict[str, float] = {}
    for key, label in (("f1", "F1-Score"), ("auc", "ROC-AUC")):
        match = re.search(rf"{label}:\s+([0-9.]+)", content)
        if match is None:
            raise ValueError(f"Thiếu {label} trong {path.name}")
        metrics[key] = float(match.group(1))
    return metrics


@st.cache_data(show_spinner=False)
def load_comparison_for_display(path: Path, modified_ns: int) -> pd.DataFrame:
    """Load a validated comparison table and refresh when its file changes."""

    del modified_ns
    return load_model_comparison(path)


def format_money(
    value: float,
    *,
    signed: bool = False,
    include_unit: bool = True,
) -> str:
    """Format a PaySim amount consistently for the Vietnamese UI."""

    prefix = "+" if signed and value > 0 else ""
    unit = " đơn vị" if include_unit else ""
    return f"{prefix}{format_currency(value)}{unit}"


def format_integer(value: int) -> str:
    """Format an integer with Vietnamese thousands separators."""

    return f"{value:,}".replace(",", ".")


def format_percentage(value: float) -> str:
    """Format a percentage using the Vietnamese decimal separator."""

    return f"{value:.2%}".replace(".", ",")


def build_class_distribution_chart(
    summary: DatasetSummary,
    scope: str,
) -> alt.LayerChart:
    """Build an interactive donut from verified train/test labels."""

    if scope == "Train":
        total = summary.train_total
        fraud = summary.train_fraud
    elif scope == "Test":
        total = summary.test_total
        fraud = summary.test_fraud
    else:
        total = summary.total
        fraud = summary.fraud

    normal = total - fraud
    distribution = pd.DataFrame(
        {
            "Nhãn": ["Hợp lệ", "Gian lận"],
            "Số giao dịch": [normal, fraud],
            "Tỷ lệ": [normal / total, fraud / total],
        }
    )
    text_color = "#F8FAFC" if st.context.theme.type == "dark" else "#251A4A"

    arcs = (
        alt.Chart(distribution)
        .mark_arc(innerRadius=62, outerRadius=98, cornerRadius=5, padAngle=0.02)
        .encode(
            theta=alt.Theta("Số giao dịch:Q", stack=True),
            color=alt.Color(
                "Nhãn:N",
                scale=alt.Scale(
                    domain=["Hợp lệ", "Gian lận"],
                    range=["#3B82F6", "#EC4899"],
                ),
                legend=alt.Legend(title=None, orient="bottom"),
            ),
            tooltip=[
                alt.Tooltip("Nhãn:N"),
                alt.Tooltip("Số giao dịch:Q", format=","),
                alt.Tooltip("Tỷ lệ:Q", format=".2%"),
            ],
        )
    )

    center_data = pd.DataFrame(
        {
            "Tỷ lệ gian lận": [format_percentage(fraud / total)],
            "Mô tả": [f"{format_integer(total)} giao dịch"],
        }
    )
    ratio_text = (
        alt.Chart(center_data)
        .mark_text(dy=-7, fontSize=24, fontWeight=700, color=text_color)
        .encode(text="Tỷ lệ gian lận:N")
    )
    total_text = (
        alt.Chart(center_data)
        .mark_text(dy=17, fontSize=12, color=text_color)
        .encode(text="Mô tả:N")
    )

    return (arcs + ratio_text + total_text).properties(height=270)


def build_split_distribution_chart(summary: DatasetSummary) -> alt.Chart:
    """Build normalized train/test bars from verified class counts."""

    rows: list[dict[str, object]] = []
    for split, total, fraud in (
        ("Train", summary.train_total, summary.train_fraud),
        ("Test", summary.test_total, summary.test_fraud),
    ):
        normal = total - fraud
        rows.extend(
            [
                {
                    "Tập dữ liệu": split,
                    "Nhãn": "Hợp lệ",
                    "Số giao dịch": normal,
                    "Tỷ lệ": normal / total,
                    "Thứ tự": 1,
                },
                {
                    "Tập dữ liệu": split,
                    "Nhãn": "Gian lận",
                    "Số giao dịch": fraud,
                    "Tỷ lệ": fraud / total,
                    "Thứ tự": 2,
                },
            ]
        )

    return (
        alt.Chart(pd.DataFrame(rows))
        .mark_bar(cornerRadiusEnd=5, height=24)
        .encode(
            x=alt.X(
                "Số giao dịch:Q",
                stack="normalize",
                axis=alt.Axis(format="%", title="Tỷ trọng nhãn"),
            ),
            y=alt.Y(
                "Tập dữ liệu:N",
                sort=["Train", "Test"],
                title=None,
            ),
            color=alt.Color(
                "Nhãn:N",
                scale=alt.Scale(
                    domain=["Hợp lệ", "Gian lận"],
                    range=["#3B82F6", "#EC4899"],
                ),
                legend=None,
            ),
            order=alt.Order("Thứ tự:Q"),
            tooltip=[
                alt.Tooltip("Tập dữ liệu:N"),
                alt.Tooltip("Nhãn:N"),
                alt.Tooltip("Số giao dịch:Q", format=","),
                alt.Tooltip("Tỷ lệ:Q", format=".2%"),
            ],
        )
        .properties(height=145)
    )


def build_balance_flow_chart(transaction: TransactionInput) -> alt.Chart:
    """Visualize the entered source/destination balances before and after."""

    balances = pd.DataFrame(
        {
            "Tài khoản": ["Nguồn", "Nguồn", "Đích", "Đích"],
            "Trạng thái": ["Trước", "Sau", "Trước", "Sau"],
            "Số dư": [
                transaction.old_balance_origin,
                transaction.new_balance_origin,
                transaction.old_balance_destination,
                transaction.new_balance_destination,
            ],
        }
    )
    balance_ceiling = max(float(balances["Số dư"].max()), 1.0) * 1.14

    return (
        alt.Chart(balances)
        .mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5)
        .encode(
            x=alt.X("Tài khoản:N", title=None),
            xOffset="Trạng thái:N",
            y=alt.Y(
                "Số dư:Q",
                title="Số dư",
                scale=alt.Scale(domain=[0, balance_ceiling], nice=False),
                axis=alt.Axis(format="~s", gridOpacity=0.12),
            ),
            color=alt.Color(
                "Trạng thái:N",
                scale=alt.Scale(
                    domain=["Trước", "Sau"],
                    range=["#22D3EE", "#A855F7"],
                ),
                legend=alt.Legend(title=None, orient="bottom"),
            ),
            tooltip=[
                alt.Tooltip("Tài khoản:N"),
                alt.Tooltip("Trạng thái:N"),
                alt.Tooltip("Số dư:Q", format=",.0f"),
            ],
        )
        .properties(
            height=250,
            padding={"top": 20, "right": 12, "bottom": 10, "left": 10},
        )
    )


def build_balance_error_chart(transaction: TransactionInput) -> alt.LayerChart:
    """Show engineered balance errors around an explicit zero baseline."""

    tolerance = max(1.0, transaction.amount * 0.01)
    errors = [
        transaction.origin_difference,
        transaction.destination_difference,
    ]
    error_frame = pd.DataFrame(
        {
            "Tài khoản": ["Nguồn", "Đích"],
            "Sai lệch": errors,
            "Trạng thái": [
                (
                    "Cân đối"
                    if abs(value) <= tolerance
                    else "Dương"
                    if value > 0
                    else "Âm"
                )
                for value in errors
            ],
        }
    )
    chart_bound = max(
        max(abs(value) for value in errors),
        tolerance * 4,
        1.0,
    ) * 1.15
    tolerance_band = pd.DataFrame(
        {"Bắt đầu": [-tolerance], "Kết thúc": [tolerance]}
    )
    shared_y = alt.Y(
        "Tài khoản:N",
        title=None,
        sort=["Nguồn", "Đích"],
        scale=alt.Scale(paddingInner=0.48, paddingOuter=0.4),
        axis=alt.Axis(labelFontWeight=600),
    )

    shared_x = alt.X(
        "Sai lệch:Q",
        title="Sai lệch số dư (đơn vị)",
        scale=alt.Scale(domain=[-chart_bound, chart_bound]),
        axis=alt.Axis(format="~s", gridOpacity=0.12),
    )
    zone = (
        alt.Chart(tolerance_band)
        .mark_rect(color="#22C55E", opacity=0.1)
        .encode(
            x=alt.X(
                "Bắt đầu:Q",
                scale=alt.Scale(domain=[-chart_bound, chart_bound]),
            ),
            x2="Kết thúc:Q",
        )
    )
    zero_line = (
        alt.Chart(pd.DataFrame({"Mốc": [0]}))
        .mark_rule(color="#94A3B8", strokeWidth=2, strokeDash=[5, 4])
        .encode(x="Mốc:Q")
    )
    bars = (
        alt.Chart(error_frame)
        .mark_bar(cornerRadius=7, size=30)
        .encode(
            x=shared_x,
            y=shared_y,
            color=alt.Color(
                "Trạng thái:N",
                scale=alt.Scale(
                    domain=["Cân đối", "Dương", "Âm"],
                    range=["#22C55E", "#22D3EE", "#F43F5E"],
                ),
                legend=alt.Legend(title=None, orient="bottom"),
            ),
            tooltip=[
                alt.Tooltip("Tài khoản:N"),
                alt.Tooltip("Sai lệch:Q", format="+,.0f"),
                alt.Tooltip("Trạng thái:N"),
            ],
        )
    )
    points = (
        alt.Chart(error_frame)
        .mark_point(filled=True, size=95, stroke="white", strokeWidth=1.5)
        .encode(
            x=shared_x,
            y=shared_y,
            color=alt.Color(
                "Trạng thái:N",
                scale=alt.Scale(
                    domain=["Cân đối", "Dương", "Âm"],
                    range=["#22C55E", "#22D3EE", "#F43F5E"],
                ),
                legend=None,
            ),
            tooltip=[
                alt.Tooltip("Tài khoản:N"),
                alt.Tooltip("Sai lệch:Q", format="+,.0f"),
                alt.Tooltip("Trạng thái:N"),
            ],
        )
    )

    return (zone + zero_line + bars + points).properties(
        height=235,
        padding={"top": 20, "right": 12, "bottom": 10, "left": 12},
    )


def build_transaction_signal_map_chart(
    transaction: TransactionInput,
) -> alt.LayerChart:
    """Build a descriptive transaction signal map without risk inference."""

    amount_reference = max(transaction.amount, 1.0)
    source_reference = max(transaction.old_balance_origin, 1.0)
    destination_change = max(
        transaction.new_balance_destination
        - transaction.old_balance_destination,
        0.0,
    )
    signal_names = [
        "Tỷ trọng giao dịch",
        "Số dư nguồn còn lại",
        "Mức tăng số dư đích",
        "Độ khớp nguồn",
        "Độ khớp đích",
        "Vị trí thời gian",
    ]
    signal_values = [
        min(transaction.amount / source_reference, 1.0),
        min(transaction.new_balance_origin / source_reference, 1.0),
        min(destination_change / amount_reference, 1.0),
        max(
            0.0,
            1.0
            - min(
                abs(transaction.origin_difference) / amount_reference,
                1.0,
            ),
        ),
        max(
            0.0,
            1.0
            - min(
                abs(transaction.destination_difference) / amount_reference,
                1.0,
            ),
        ),
        min(transaction.step / 744, 1.0),
    ]
    signal_map = pd.DataFrame(
        {
            "Tín hiệu": signal_names,
            "Mức tương đối": signal_values,
            "Tỷ lệ hiển thị": [
                format_percentage(value) for value in signal_values
            ],
            "Trọng số": [1] * len(signal_names),
            "Thứ tự": range(len(signal_names)),
        }
    )

    theta_encoding = alt.Theta("Trọng số:Q", stack=True)
    order_encoding = alt.Order("Thứ tự:O")
    backdrop = (
        alt.Chart(signal_map)
        .mark_arc(
            innerRadius=36,
            outerRadius=100,
            cornerRadius=6,
            padAngle=0.045,
            color="#94A3B8",
            opacity=0.12,
        )
        .encode(theta=theta_encoding, order=order_encoding)
    )
    petals = (
        alt.Chart(signal_map)
        .mark_arc(innerRadius=36, cornerRadius=6, padAngle=0.045)
        .encode(
            theta=theta_encoding,
            radius=alt.Radius(
                "Mức tương đối:Q",
                scale=alt.Scale(domain=[0, 1], range=[40, 100]),
            ),
            color=alt.Color(
                "Tín hiệu:N",
                sort=signal_names,
                scale=alt.Scale(
                    domain=signal_names,
                    range=[
                        "#22D3EE",
                        "#3B82F6",
                        "#8B5CF6",
                        "#D946EF",
                        "#EC4899",
                        "#FB7185",
                    ],
                ),
                legend=alt.Legend(
                    title=None,
                    orient="bottom",
                    columns=2,
                ),
            ),
            order=order_encoding,
            tooltip=[
                alt.Tooltip("Tín hiệu:N"),
                alt.Tooltip("Tỷ lệ hiển thị:N", title="Mức tương đối"),
            ],
        )
    )

    return (backdrop + petals).properties(
        height=305,
        padding={"top": 22, "right": 10, "bottom": 10, "left": 10},
    )


def validate_transaction(transaction: TransactionInput) -> list[str]:
    """Return data-quality notes without attempting fraud classification."""

    notes: list[str] = []
    tolerance = max(1.0, transaction.amount * 0.01)

    if transaction.amount <= 0:
        notes.append("Số tiền giao dịch phải lớn hơn 0.")

    if transaction.new_balance_origin > transaction.old_balance_origin:
        notes.append("Số dư nguồn sau giao dịch đang cao hơn số dư ban đầu.")

    if abs(transaction.origin_difference) > tolerance:
        notes.append("Số dư tài khoản nguồn chưa khớp với số tiền giao dịch.")

    if abs(transaction.destination_difference) > tolerance:
        notes.append("Số dư tài khoản đích chưa khớp với số tiền giao dịch.")

    return notes


def initialize_state() -> None:
    """Initialize per-session values in one predictable place."""

    pending_threshold = st.session_state.pop(
        "pending_decision_threshold_percent",
        None,
    )
    if pending_threshold is not None:
        st.session_state["decision_threshold_percent"] = pending_threshold

    st.session_state.setdefault("last_transaction", None)
    st.session_state.setdefault("validation_notes", [])
    st.session_state.setdefault("active_preset", None)
    st.session_state.setdefault("active_test_case", None)
    st.session_state.setdefault("submitted_test_case", None)
    st.session_state.setdefault("imported_samples", {})
    st.session_state.setdefault("show_sample_import", False)
    st.session_state.setdefault("processed_sample_upload", None)
    st.session_state.setdefault(
        "decision_threshold_percent",
        DEFAULT_DECISION_THRESHOLD_PERCENT,
    )
    st.session_state.setdefault("pipeline_detail_step", 1)
    st.session_state.setdefault("active_view", "prediction")
    refresh_analysis_history()


def refresh_analysis_history() -> None:
    """Reload persistent history so restarts and other tabs stay in sync."""

    try:
        history = load_analysis_history(HISTORY_DATABASE_PATH)
    except (OSError, sqlite3.Error, ValueError) as error:
        st.session_state.setdefault("analysis_history", [])
        st.session_state["history_storage_error"] = str(error)
        return

    st.session_state["analysis_history"] = history
    st.session_state["history_storage_error"] = None


def record_analysis(
    transaction: TransactionInput,
    prediction: PredictionResult,
    validation_notes: list[str],
) -> bool:
    """Persist one successful model run and refresh the current view."""

    entry = {
        "created_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "transaction_type": transaction.transaction_type,
        "step": transaction.step,
        "amount": transaction.amount,
        "fraud_probability": prediction.fraud_probability,
        "threshold": prediction.threshold,
        "label": prediction.label,
        "quality_warnings": len(validation_notes),
    }
    try:
        save_analysis(HISTORY_DATABASE_PATH, entry)
    except (OSError, sqlite3.Error, KeyError, TypeError, ValueError) as error:
        st.session_state["history_storage_error"] = str(error)
        return False

    refresh_analysis_history()
    return True


def delete_history_row() -> None:
    """Delete only the history row whose inline icon was clicked."""

    component_state = st.session_state.get("history_table")
    if not component_state:
        return
    analysis_id = component_state.get("deleted")
    if analysis_id is None:
        return
    try:
        delete_analysis(HISTORY_DATABASE_PATH, int(analysis_id))
    except (OSError, sqlite3.Error, TypeError, ValueError) as error:
        st.session_state["history_storage_error"] = str(error)
        return
    refresh_analysis_history()


def sync_time_from_step() -> None:
    value = st.session_state.get("transaction_step_input")
    if value is not None:
        converted = step_to_datetime(value)
        st.session_state["transaction_date_input"] = converted.date()
        st.session_state["transaction_time_input"] = converted.time()


def sync_step_from_time() -> None:
    day = st.session_state.get("transaction_date_input")
    hour = st.session_state.get("transaction_time_input")
    if day is not None and hour is not None:
        try:
            st.session_state["transaction_step_input"] = datetime_to_step(
                datetime.combine(day, hour)
            )
        except ValueError:
            pass  # The input area displays the error and disables analysis.


MONEY_DEFAULTS = {
    "transaction_amount_input": 250_000.0,
    "old_balance_origin": 1_000_000.0,
    "new_balance_origin": 750_000.0,
    "old_balance_destination": 500_000.0,
    "new_balance_destination": 750_000.0,
}


def sync_money_text(key: str) -> None:
    text_key = f"{key}_text"
    try:
        raw = st.session_state[text_key]
        current = st.session_state[key]
        # Merely displaying a reconstructed X_test value must not round it.
        value = current if raw == format_currency(current) else parse_currency(raw)
        st.session_state[key] = value
        st.session_state[text_key] = format_currency(value)
    except ValueError:
        pass  # Keep invalid input visible for correction.


def money_input(label: str, key: str, icon: str | None = None) -> float | None:
    st.session_state.setdefault(key, MONEY_DEFAULTS[key])
    text_key = f"{key}_text"
    st.session_state.setdefault(text_key, format_currency(st.session_state[key]))
    raw = st.text_input(
        label, key=text_key, icon=icon,
        help="Dấu chấm phân tách hàng nghìn, dấu phẩy cho phần lẻ. Ví dụ: 1.143.937,73. Đơn vị tiền mô phỏng PaySim.",
        on_change=sync_money_text, args=(key,),
        persist_state="session",
    )
    try:
        parsed = parse_currency(raw)
        current = st.session_state[key]
        return current if raw == format_currency(current) else parsed
    except ValueError as error:
        st.error(str(error))
        return None


def sync_form_display() -> None:
    sync_time_from_step()
    for key in MONEY_DEFAULTS:
        st.session_state[f"{key}_text"] = format_currency(st.session_state[key])


def apply_transaction_preset(preset_key: str) -> None:
    """Populate the form with a descriptive sample scenario."""

    preset = TRANSACTION_PRESETS[preset_key]
    transaction = preset["transaction"]
    st.session_state.update(
        {
            "transaction_type_input": transaction.transaction_type,
            "transaction_step_input": transaction.step,
            "transaction_amount_input": transaction.amount,
            "old_balance_origin": transaction.old_balance_origin,
            "new_balance_origin": transaction.new_balance_origin,
            "old_balance_destination": transaction.old_balance_destination,
            "new_balance_destination": transaction.new_balance_destination,
            "last_transaction": None,
            "pipeline_submitted_payload": None,
            "validation_notes": [],
            "submitted_test_case": None,
            "active_preset": preset_key,
            "active_test_case": None,
        }
    )


    sync_form_display()


def apply_labeled_test_case(test_case_key: str) -> None:
    """Populate the form with one held-out PaySim transaction."""

    cases = load_labeled_test_cases(
        PROCESSED_DATA_DIR,
        XGB_PREDICTIONS_PATH,
        SCALER_PATH,
    )
    test_case = cases[test_case_key]
    transaction = test_case.transaction
    st.session_state.update(
        {
            "transaction_type_input": transaction.transaction_type,
            "transaction_step_input": transaction.step,
            "transaction_amount_input": transaction.amount,
            "old_balance_origin": transaction.old_balance_origin,
            "new_balance_origin": transaction.new_balance_origin,
            "old_balance_destination": transaction.old_balance_destination,
            "new_balance_destination": transaction.new_balance_destination,
            "last_transaction": None,
            "pipeline_submitted_payload": None,
            "validation_notes": [],
            "submitted_test_case": None,
            "active_preset": None,
            "active_test_case": test_case_key,
        }
    )


    sync_form_display()


def set_active_view(view_key: str) -> None:
    """Switch the workspace without rendering inactive pages."""

    st.session_state["active_view"] = view_key


def render_sidebar_navigation() -> str:
    """Render a focused, collapsible sidebar for primary navigation."""

    navigation_items = (
        (
            "prediction",
            "Phân tích giao dịch",
            ":material/shield:",
        ),
        (
            "results",
            "Hiệu năng mô hình",
            ":material/monitoring:",
        ),
        (
            "history",
            "Lịch sử phân tích",
            ":material/history:",
        ),
    )

    with st.sidebar:
        with st.container(
            key="sidebar_brand",
            horizontal=True,
            vertical_alignment="center",
            gap="small",
        ):
            if LOGO_PATH.exists():
                st.image(LOGO_PATH, width=48)
            st.markdown("**Fraud Shield**  \n:gray[AI fraud intelligence]")

        st.caption("KHÔNG GIAN LÀM VIỆC")

        active_view = st.session_state["active_view"]
        for view_key, label, icon in navigation_items:
            st.button(
                label,
                icon=icon,
                key=f"nav_{view_key}",
                type="primary" if active_view == view_key else "secondary",
                width="stretch",
                on_click=set_active_view,
                args=(view_key,),
            )

        if st.button(
            "Dữ liệu mẫu",
            icon=":material/dataset:",
            key="open_sample_picker",
            type="secondary",
            width="stretch",
            on_click=reset_sample_threshold,
        ):
            show_sample_picker()

        with st.container(key="theme_bootstrap"):
            THEME_SWITCHER(
                key="fraud-shield-theme-bootstrap",
                data={"current_theme": st.context.theme.type or "light"},
                width="stretch",
                height=0,
            )

        with st.popover(
            "Giao diện",
            icon=":material/contrast:",
            type="secondary",
            width="stretch",
            key="theme_mode_menu",
        ):
            st.caption("CHẾ ĐỘ HIỂN THỊ")
            THEME_SWITCHER(
                key="fraud-shield-theme-switcher",
                data={"current_theme": st.context.theme.type or "light"},
                width="stretch",
                height="content",
            )

    return st.session_state["active_view"]


def render_threshold_control() -> None:
    """Render a useful decision-threshold control in place of decoration."""

    st.caption("ĐIỀU KHIỂN PHÂN LOẠI")
    with st.container(
        horizontal=True,
        horizontal_alignment="distribute",
        vertical_alignment="center",
    ):
        st.markdown("#### Ngưỡng cảnh báo")
        threshold = st.session_state["decision_threshold_percent"]
        if threshold < 40:
            st.badge("Ưu tiên phát hiện", icon=":material/radar:", color="blue")
        elif threshold <= 60:
            st.badge("Cân bằng", icon=":material/balance:", color="green")
        else:
            st.badge(
                "Giảm cảnh báo nhầm",
                icon=":material/filter_alt:",
                color="orange",
            )

    st.slider(
        "Ngưỡng xác suất",
        min_value=10,
        max_value=90,
        step=1,
        format="%d%%",
        key="decision_threshold_percent",
        help="Giao dịch có xác suất bằng hoặc cao hơn ngưỡng sẽ được gắn cờ.",
    )
    THRESHOLD_SLIDER_ENHANCER(
        key="fraud-shield-threshold-slider-enhancer",
        data={"value": threshold},
        width="content",
        height=0,
    )
    st.caption(
        "Hạ ngưỡng để tăng độ nhạy; nâng ngưỡng để giảm số cảnh báo nhầm."
    )


def reset_sample_threshold() -> None:
    """Start every sample-selection flow at the standard 50% threshold."""

    st.session_state["decision_threshold_percent"] = (
        DEFAULT_DECISION_THRESHOLD_PERCENT
    )


def apply_selected_sample(selected_sample: str | None = None) -> None:
    """Fill the form from one sample and restore the standard 50% threshold."""

    selected_sample = selected_sample or st.session_state.get("sample_selector")
    if not selected_sample or ":" not in selected_sample:
        return
    source, key = selected_sample.split(":", 1)
    if source == "preset" and key in TRANSACTION_PRESETS:
        apply_transaction_preset(key)
    elif source == "test":
        apply_labeled_test_case(key)
    elif source == "imported" and key in st.session_state["imported_samples"]:
        sample = st.session_state["imported_samples"][key]
        transaction = TransactionInput(**sample["transaction"])
        st.session_state.update(
            {
                "transaction_type_input": transaction.transaction_type,
                "transaction_step_input": transaction.step,
                "transaction_amount_input": transaction.amount,
                "old_balance_origin": transaction.old_balance_origin,
                "new_balance_origin": transaction.new_balance_origin,
                "old_balance_destination": transaction.old_balance_destination,
                "new_balance_destination": transaction.new_balance_destination,
                "last_transaction": None,
                "pipeline_submitted_payload": None,
                "validation_notes": [],
                "submitted_test_case": None,
                "active_preset": None,
                "active_test_case": None,
            }
        )
        sync_form_display()
    else:
        return

    # Every demo/test sample starts from the same documented decision rule.
    # Users can still adjust the slider after choosing a sample for comparison.
    st.session_state["pending_decision_threshold_percent"] = (
        DEFAULT_DECISION_THRESHOLD_PERCENT
    )


@st.dialog(
    "Dữ liệu mẫu",
    width="medium",
    icon=":material/dataset:",
    on_dismiss="rerun",
)
def show_sample_picker() -> None:
    """Choose one sample in a centered dialog, then fill the input form."""

    try:
        labeled_cases = load_labeled_test_cases(
            PROCESSED_DATA_DIR,
            XGB_PREDICTIONS_PATH,
            SCALER_PATH,
        )
    except (FileNotFoundError, KeyError, OSError, ValueError):
        labeled_cases = {}

    sample_options = tuple(
        [
            f"{source}:{key}"
            for source, key in DEMO_SAMPLE_ORDER
            if (source == "preset" and key in TRANSACTION_PRESETS)
            or (source == "test" and key in labeled_cases)
        ]
        + [f"imported:{key}" for key in st.session_state["imported_samples"]]
    )

    def format_sample_option(option: str) -> str:
        source, key = option.split(":", 1)
        if source == "preset":
            preset = TRANSACTION_PRESETS[key]
            return f"{preset['icon']} Mô phỏng · {preset['title']}"
        if source == "test":
            return f"Có nhãn · {labeled_cases[key].title}"
        return f"Đã import · {st.session_state['imported_samples'][key]['title']}"

    with st.container(key="sample_dialog", gap="medium"):
        st.caption(
            "Chọn dữ liệu để điền vào biểu mẫu. Hệ thống chỉ dự đoán sau khi "
            "bạn bấm Phân tích giao dịch."
        )
        selected_sample = st.selectbox(
            "Chọn mẫu giao dịch",
            options=sample_options,
            index=None,
            placeholder="Chọn một dữ liệu mẫu",
            format_func=format_sample_option,
            key="sample_selector",
            width="stretch",
        )

        choose_column, import_column = st.columns(2, gap="small")
        with choose_column:
            choose_sample = st.button(
                "Chọn mẫu",
                icon=":material/check_circle:",
                key="choose_sample",
                type="primary",
                width="stretch",
            )
        with import_column:
            show_import = st.button(
                "Import mẫu",
                icon=":material/upload_file:",
                key="show_sample_import_button",
                type="secondary",
                width="stretch",
            )

        if choose_sample:
            if not selected_sample:
                st.warning("Hãy chọn một dữ liệu mẫu trước.")
            else:
                apply_selected_sample(selected_sample)
                st.session_state["active_view"] = "prediction"
                st.rerun()

        if show_import:
            st.session_state["show_sample_import"] = True

        if st.session_state["show_sample_import"]:
            uploaded_file = st.file_uploader(
                "Import mẫu kiểm thử từ CSV hoặc JSON",
                type=("csv", "json"),
                key="sample_file_upload",
                help=(
                    "Cần các trường type, step, amount, oldbalanceOrg, "
                    "newbalanceOrig, oldbalanceDest và newbalanceDest."
                ),
            )
            st.caption("Tối đa 1 MB và 50 mẫu mỗi lần import.")
            if uploaded_file is not None:
                content = uploaded_file.getvalue()
                signature = (uploaded_file.name, len(content), hash(content))
                if signature != st.session_state["processed_sample_upload"]:
                    if len(content) > 1_000_000:
                        st.error("File vượt quá giới hạn 1 MB.")
                    else:
                        try:
                            imported = parse_sample_file(uploaded_file.name, content)
                        except ValueError as error:
                            st.error(str(error))
                        else:
                            library = dict(st.session_state["imported_samples"])
                            for sample in imported:
                                sample_key = f"sample_{len(library) + 1}"
                                library[sample_key] = sample
                            st.session_state["imported_samples"] = library
                            st.session_state["processed_sample_upload"] = signature
                            st.toast(
                                f"Đã import {len(imported)} mẫu vào thư viện.",
                                icon=":material/check_circle:",
                            )
                            st.rerun(scope="fragment")

        st.caption("Chọn mẫu chỉ điền biểu mẫu · Chưa chạy dự đoán")


def render_risk_meter(prediction: PredictionResult) -> None:
    """Render a compact linear risk meter as the primary result."""

    probability = prediction.fraud_probability * 100
    if prediction.label == 1:
        risk_class = "risk-high"
        risk_label = "RỦI RO CAO"
        decision_title = "Nghi vấn gian lận"
    elif probability >= 20:
        risk_class = "risk-medium"
        risk_label = "CẦN LƯU Ý — CHƯA VƯỢT NGƯỠNG"
        decision_title = "Model vẫn phân loại hợp lệ"
    else:
        risk_class = "risk-low"
        risk_label = "RỦI RO THẤP"
        decision_title = "Không phát hiện gian lận"

    st.html(
        f"""
        <div class="risk-meter-card {risk_class}" role="img"
             aria-label="Xác suất gian lận {probability:.2f} phần trăm">
          <div class="risk-meter-head">
            <div>
              <div class="fraud-score-label">{risk_label}</div>
              <div class="fraud-score-title">{decision_title}</div>
            </div>
          </div>
          <div class="risk-meter-track" style="--score: {probability:.4f}; --threshold: {prediction.threshold * 100:.2f}">
            <span class="risk-meter-score-tag">{probability:.2f}%</span>
            <span class="risk-meter-threshold" aria-hidden="true"></span>
            <span class="risk-meter-marker"></span>
            <span class="risk-meter-tick" style="--tick: 0"></span>
            <span class="risk-meter-tick" style="--tick: 25"></span>
            <span class="risk-meter-tick" style="--tick: 50"></span>
            <span class="risk-meter-tick" style="--tick: 75"></span>
            <span class="risk-meter-tick" style="--tick: 100"></span>
            <div class="risk-meter-axis" aria-hidden="true">
              <span>0%</span><span>25%</span><span>50%</span><span>75%</span><span>100%</span>
            </div>
          </div>
          <div class="risk-meter-scale">
            <span>Thấp</span><span>Cần lưu ý</span><span>Cao</span>
          </div>
        </div>
        """
    )


def render_labeled_test_verdict(prediction: PredictionResult) -> None:
    """Compare the current prediction with the selected held-out label."""

    test_case_key = st.session_state.get("submitted_test_case")
    if not test_case_key:
        return

    try:
        test_case = load_labeled_test_cases(
            PROCESSED_DATA_DIR,
            XGB_PREDICTIONS_PATH,
            SCALER_PATH,
        )[test_case_key]
    except (FileNotFoundError, KeyError, OSError, ValueError):
        st.warning("Không đọc được nhãn thật của mẫu kiểm thử.")
        return

    true_text = "Bất thường" if test_case.true_label == 1 else "Hợp lệ"
    predicted_text = "Bất thường" if prediction.label == 1 else "Hợp lệ"
    is_correct = prediction.label == test_case.true_label

    st.markdown("**Đối chiếu với nhãn thật**")
    with st.container(horizontal=True):
        st.metric("Nhãn thực tế", true_text, border=True)
        st.metric("XGBoost dự đoán", predicted_text, border=True)
    st.badge(
        "Dự đoán đúng" if is_correct else "Dự đoán sai",
        icon=":material/check_circle:" if is_correct else ":material/error:",
        color="green" if is_correct else "red",
    )
    st.caption(
        f"Mã mẫu kiểm thử #{test_case.test_position + 1:,} • "
        f"Nhãn thật {test_case.true_label} • Ngưỡng hiện tại {prediction.threshold:.0%}"
    )


def render_header(summary: DatasetSummary | None) -> None:
    """Render the main page identity and high-level project facts."""

    with st.container(key="hero_panel", border=True):
        hero_copy, signal_visual = st.columns(
            [1.6, 1],
            gap="large",
            vertical_alignment="center",
        )

        with hero_copy:
            st.caption("FRAUD SHIELD • LIVE TRANSACTION SIGNALS")
            st.title("Bản đồ tín hiệu giao dịch")
            st.markdown(
                "Biến số tiền, thời điểm và biến động số dư thành một góc nhìn "
                "**trực quan, dễ đọc**, kèm dự đoán từ mô hình đã huấn luyện."
            )

            with st.container(key="dataset_fraud_metrics", horizontal=True):
                st.badge(
                    "XGBoost sẵn sàng",
                    icon=":material/model_training:",
                    color="green",
                )
                st.badge(
                    "Dữ liệu thật",
                    icon=":material/verified:",
                    color="blue",
                )

        with signal_visual:
            render_threshold_control()

    total_label = format_integer(summary.total) if summary else "200.000"
    split_label = (
        f"{summary.train_total // 1000}k huấn luyện • "
        f"{summary.test_total // 1000}k kiểm thử"
        if summary
        else "160k huấn luyện • 40k kiểm thử"
    )
    fraud_ratio_label = (
        format_percentage(summary.fraud_ratio) if summary else "4,11%"
    )
    model_ready = XGB_MODEL_PATH.is_file() and SCALER_PATH.is_file()

    metric_specs = (
        ("overview_metric_data", "Dữ liệu đã xử lý", total_label, split_label),
        ("overview_metric_scope", "Tỷ lệ gian lận", fraud_ratio_label, "Trên toàn bộ dữ liệu"),
        ("overview_metric_features", "Không gian đặc trưng", "14", "10 số • 4 nhị phân"),
        (
            "overview_metric_model_ready" if model_ready else "overview_metric_model_unavailable",
            "Mô hình phân tích",
            "Sẵn sàng" if model_ready else "Chưa sẵn sàng",
            "XGBoost đang hoạt động" if model_ready else "Kiểm tra dữ liệu mô hình",
        ),
    )
    with st.container(key="overview_metrics", horizontal=True, gap="small"):
        for metric_key, label, value, delta in metric_specs:
            with st.container(key=metric_key, height="stretch", gap=None):
                st.metric(
                    label,
                    value,
                    delta,
                    delta_color="off",
                    delta_arrow="off",
                    border=True,
                    height="stretch",
                )


def render_transaction_form() -> None:
    """Render transaction inputs, signal visuals and real model inference."""

    form_column, preview_column = st.columns([1.48, 1.07], gap="large")

    with form_column:
        st.subheader("Nhập thông tin giao dịch")
        with st.container(key="workflow_steps", horizontal=True):
            st.badge(
                "01 • Nhập",
                icon=":material/edit_note:",
                color="violet",
            )
            st.badge(
                "02 • Soi tín hiệu",
                icon=":material/query_stats:",
                color="blue",
            )
            st.badge(
                "03 • Dự đoán thật",
                icon=":material/model_training:",
                color="green",
            )
        active_preset = st.session_state["active_preset"]
        if active_preset is not None:
            preset = TRANSACTION_PRESETS[active_preset]
            with st.container(horizontal=True, vertical_alignment="center"):
                st.badge(
                    f"Đang dùng kịch bản: {preset['title']}",
                    icon=":material/auto_awesome:",
                    color=preset["color"],
                )
                st.badge(
                    preset["eyebrow"],
                    icon=":material/info:",
                    color="gray",
                )
        active_test_case = st.session_state["active_test_case"]
        if active_test_case is not None:
            try:
                test_case = load_labeled_test_cases(
                    PROCESSED_DATA_DIR,
                    XGB_PREDICTIONS_PATH,
                    SCALER_PATH,
                )[active_test_case]
                st.badge(
                    f"Mẫu kiểm thử: {test_case.title}",
                    icon=":material/fact_check:",
                    color="blue",
                )
            except (FileNotFoundError, KeyError, OSError, ValueError):
                st.badge("Mẫu kiểm thử chưa sẵn sàng", color="red")

        with st.container(key="transaction_form", border=True, gap="medium"):
            st.badge(
                "01 • Giao dịch",
                icon=":material/receipt_long:",
                color="blue",
            )
            transaction_type = st.segmented_control(
                "Loại giao dịch",
                TRANSACTION_TYPES,
                default=(
                    None
                    if "transaction_type_input" in st.session_state
                    else "TRANSFER"
                ),
                required=True,
                format_func=lambda value: TRANSACTION_LABELS[value],
                help="PaySim ghi nhận fraud trong hai loại TRANSFER và CASH_OUT.",
                width="stretch",
                key="transaction_type_input",
            )

            st.session_state.setdefault("transaction_step_input", 120)
            if "transaction_date_input" not in st.session_state:
                sync_time_from_step()
            st.markdown("**Thời điểm giao dịch**")
            date_column, hour_column, step_column = st.columns(3, gap="medium")
            with date_column:
                selected_date = st.date_input(
                    "Ngày", value=None, format="DD/MM/YYYY",
                    min_value=step_to_datetime(MIN_STEP).date(),
                    max_value=step_to_datetime(MAX_STEP).date(),
                    key="transaction_date_input",
                    on_change=sync_step_from_time,
                    persist_state="session",
                )
            with hour_column:
                selected_time = st.time_input(
                    "Giờ", value=None, step=3600,
                    key="transaction_time_input",
                    on_change=sync_step_from_time,
                    persist_state="session",
                )
            with step_column:
                selected_step = st.number_input(
                    "Step",
                    min_value=MIN_STEP,
                    max_value=MAX_STEP,
                    step=1,
                    key="transaction_step_input",
                    on_change=sync_time_from_step,
                    help=(
                        "Mỗi step tương ứng 1 giờ trong mô phỏng PaySim. "
                        "Thay đổi Step sẽ tự cập nhật Ngày và Giờ."
                    ),
                    persist_state="session",
                )
            time_error = None
            try:
                if selected_date is None or selected_time is None:
                    raise ValueError("Chọn đủ ngày và giờ giao dịch.")
                step = datetime_to_step(datetime.combine(selected_date, selected_time))
                if step != int(selected_step):
                    raise ValueError("Step và Ngày/Giờ chưa đồng bộ.")
            except ValueError as error:
                time_error = str(error)
                st.error(time_error)
            amount = money_input(
                "Số tiền giao dịch", "transaction_amount_input", ":material/payments:"
            )

            st.badge(
                "02 • Tài khoản nguồn",
                icon=":material/account_balance_wallet:", color="gray",
            )
            source_before, source_after = st.columns(2, gap="medium")
            with source_before:
                old_balance_origin = money_input("Số dư trước giao dịch", "old_balance_origin")
            with source_after:
                new_balance_origin = money_input("Số dư sau giao dịch", "new_balance_origin")

            st.badge(
                "03 • Tài khoản đích",
                icon=":material/account_balance:", color="gray",
            )
            destination_before, destination_after = st.columns(2, gap="medium")
            with destination_before:
                old_balance_destination = money_input("Số dư trước khi nhận", "old_balance_destination")
            with destination_after:
                new_balance_destination = money_input("Số dư sau khi nhận", "new_balance_destination")

            submitted = st.button(
                "Phân tích giao dịch", key="analyze_transaction",
                type="primary", icon=":material/shield:", width="stretch",
                disabled=time_error is not None or any(value is None for value in (
                    amount, old_balance_origin, new_balance_origin,
                    old_balance_destination, new_balance_destination,
                )),
            )
        if submitted:
            transaction = TransactionInput(
                transaction_type=transaction_type or "TRANSFER",
                step=int(step),
                amount=float(amount),
                old_balance_origin=float(old_balance_origin),
                new_balance_origin=float(new_balance_origin),
                old_balance_destination=float(old_balance_destination),
                new_balance_destination=float(new_balance_destination),
            )
            submitted_test_case = None
            active_test_case = st.session_state.get("active_test_case")
            if active_test_case:
                try:
                    selected_case = load_labeled_test_cases(
                        PROCESSED_DATA_DIR,
                        XGB_PREDICTIONS_PATH,
                        SCALER_PATH,
                    )[active_test_case]
                    if asdict(selected_case.transaction) == asdict(transaction):
                        submitted_test_case = active_test_case
                except (FileNotFoundError, KeyError, OSError, ValueError):
                    submitted_test_case = None
            st.session_state["last_transaction"] = asdict(transaction)
            st.session_state["pipeline_submitted_payload"] = asdict(transaction)
            st.session_state["validation_notes"] = validate_transaction(transaction)
            st.session_state["submitted_test_case"] = submitted_test_case
            st.session_state["active_preset"] = None
            st.session_state["active_test_case"] = None
            submitted_prediction, submitted_error = run_transaction_inference(
                transaction,
                st.session_state["decision_threshold_percent"] / 100,
            )
            if submitted_prediction is not None:
                history_saved = record_analysis(
                    transaction,
                    submitted_prediction,
                    st.session_state["validation_notes"],
                )
                if not history_saved:
                    st.toast(
                        "Đã phân tích nhưng chưa lưu được lịch sử.",
                        icon=":material/error:",
                    )
            else:
                st.toast(
                    f"Không thể lưu kết quả: {submitted_error}",
                    icon=":material/error:",
                )

    prediction = None
    with preview_column:
        st.subheader("Kết quả phân tích")

        with st.container(key="result_panel", border=True, gap="medium"):
            raw_transaction = st.session_state["last_transaction"]
            if raw_transaction is None:
                st.badge(
                    "Sẵn sàng nhận giao dịch",
                    icon=":material/edit_note:",
                    color="blue",
                )
                st.markdown("#### Chưa có bản xem trước")
                st.write(
                    "Hoàn tất biểu mẫu bên trái và chọn "
                    "**Phân tích giao dịch**."
                )
                st.caption("Kết quả chỉ xuất hiện sau khi mô hình phân tích thành công.")
            else:
                transaction = TransactionInput(**raw_transaction)
                prediction, _prediction_error = run_transaction_inference(
                    transaction,
                    st.session_state["decision_threshold_percent"] / 100,
                )
                if prediction is None:
                    st.badge(
                        "Inference tạm khóa",
                        icon=":material/error:",
                        color="red",
                    )
                    st.warning(
                        "Không thể phân tích giao dịch. Vui lòng kiểm tra "
                        "dữ liệu mô hình và thử lại.",
                        icon=":material/lock:",
                    )
                else:
                    render_risk_meter(prediction)
                    render_labeled_test_verdict(prediction)
                    if prediction.label == 1:
                        st.error(
                            "Hệ thống phát hiện tín hiệu rủi ro cao. Giao dịch cần "
                            "được kiểm tra trước khi xử lý tiếp.",
                            icon=":material/gpp_maybe:",
                        )
                    else:
                        st.success(
                            "Model chưa phát hiện dấu hiệu gian lận ở giao dịch này.",
                            icon=":material/shield:",
                        )
                    st.caption(
                        "Đây là hỗ trợ phân loại từ mô hình học máy, không thay "
                        "thế bước rà soát nghiệp vụ."
                    )
                st.markdown(
                    f"#### {TRANSACTION_LABELS[transaction.transaction_type]}"
                )
                st.caption(
                    f"{step_to_datetime(transaction.step):%d/%m/%Y %H:%M} "
                    "· thời gian mô phỏng"
                )

                source_change = (
                    transaction.new_balance_origin
                    - transaction.old_balance_origin
                )
                with st.container(horizontal=True):
                    st.metric(
                        "Số tiền • đơn vị",
                        format_money(transaction.amount, include_unit=False),
                        border=True,
                    )
                    st.metric(
                        "Biến động nguồn • đơn vị",
                        format_money(
                            source_change,
                            signed=True,
                            include_unit=False,
                        ),
                        border=True,
                    )

                visual_mode = st.segmented_control(
                    "Góc nhìn trực quan",
                    ["Tín hiệu", "Dòng tiền", "Số dư"],
                    default="Tín hiệu",
                    key="transaction_visual_mode",
                    width="stretch",
                )
                if visual_mode == "Dòng tiền":
                    st.altair_chart(
                        build_balance_flow_chart(transaction),
                        width="stretch",
                        height=250,
                    )
                    st.caption(
                        "So sánh số dư trước và sau tại tài khoản nguồn, đích."
                    )
                elif visual_mode == "Số dư":
                    st.altair_chart(
                        build_balance_error_chart(transaction),
                        width="stretch",
                        height=235,
                    )
                    st.caption(
                        "Đường 0 là trạng thái cân đối; vùng xanh là khoảng "
                        "sai số ±1% (tối thiểu 1 đơn vị) dùng để kiểm tra "
                        "chất lượng đầu vào."
                    )
                else:
                    st.altair_chart(
                        build_transaction_signal_map_chart(transaction),
                        width="stretch",
                        height=305,
                    )
                    st.caption(
                        "Mỗi cánh mô tả một tín hiệu đã chuẩn hóa từ giao dịch; "
                        "đây không phải fraud score hay xác suất dự đoán."
                    )

                st.markdown("**Kiểm tra chất lượng dữ liệu**")
                notes = st.session_state["validation_notes"]
                quality_score = max(0, 100 - len(notes) * 25)
                st.progress(
                    quality_score,
                    text=f"Độ nhất quán đầu vào: {quality_score}%",
                )
                if notes:
                    for note in notes:
                        st.warning(note, icon=":material/warning:")
                else:
                    st.success(
                        "Các số dư khớp với giá trị giao dịch.",
                        icon=":material/check_circle:",
                    )

                with st.expander(
                    "Hai đặc trưng số dư được tính tự động",
                    icon=":material/function:",
                ):
                    st.metric(
                        "errorBalanceOrig",
                        format_money(transaction.origin_difference, signed=True),
                    )
                    st.metric(
                        "errorBalanceDest",
                        format_money(
                            transaction.destination_difference,
                            signed=True,
                        ),
                    )

                with st.expander(
                    "Payload sẽ chuyển sang preprocessing",
                    icon=":material/data_object:",
                ):
                    st.dataframe(
                        [
                            {"Trường": "type", "Giá trị": transaction.transaction_type},
                            {"Trường": "amount", "Giá trị": str(transaction.amount)},
                            {
                                "Trường": "oldbalanceOrg",
                                "Giá trị": str(transaction.old_balance_origin),
                            },
                            {
                                "Trường": "newbalanceOrig",
                                "Giá trị": str(transaction.new_balance_origin),
                            },
                            {
                                "Trường": "oldbalanceDest",
                                "Giá trị": str(transaction.old_balance_destination),
                            },
                            {
                                "Trường": "newbalanceDest",
                                "Giá trị": str(transaction.new_balance_destination),
                            },
                        ],
                        hide_index=True,
                        width="stretch",
                        column_config={
                            "Trường": st.column_config.TextColumn(
                                "Trường PaySim",
                                width="medium",
                            ),
                            "Giá trị": st.column_config.TextColumn(
                                "Giá trị thô",
                                width="large",
                            ),
                        },
                    )
    # Reuse the preview's real result without running inference again. A changed
    # or invalid form must not show completed steps for the previous payload.
    current_payload = {
        "transaction_type": transaction_type or "TRANSFER",
        "step": selected_step,
        "amount": amount,
        "old_balance_origin": old_balance_origin,
        "new_balance_origin": new_balance_origin,
        "old_balance_destination": old_balance_destination,
        "new_balance_destination": new_balance_destination,
    }
    submitted_payload = st.session_state.get("pipeline_submitted_payload")
    if submitted_payload is None:
        pipeline_state = "idle"
        pipeline_payload = current_payload
    elif time_error is not None or any(value is None for value in current_payload.values()):
        pipeline_state = "invalid"
        pipeline_payload = submitted_payload
    elif current_payload != raw_transaction or current_payload != submitted_payload:
        pipeline_state = "edited"
        pipeline_payload = submitted_payload
    elif prediction is None:
        pipeline_state = "unavailable"
        pipeline_payload = submitted_payload
    else:
        pipeline_state = "complete"
        pipeline_payload = submitted_payload

    with form_column:
        render_analysis_pipeline(
            state=pipeline_state,
            prediction=prediction,
            transaction=pipeline_payload,
            threshold=st.session_state["decision_threshold_percent"] / 100,
            validation_notes=st.session_state["validation_notes"],
            animate=submitted,
        )


def render_dataset_snapshot(summary: DatasetSummary | None) -> None:
    """Render a lively, evidence-based snapshot before models are available."""

    with st.container(key="evaluation_data_panel", border=True):
        with st.container(
            horizontal=True,
            horizontal_alignment="distribute",
            vertical_alignment="center",
        ):
            st.markdown("#### Nền dữ liệu đánh giá")
            st.badge(
                "Dữ liệu đã xác thực",
                icon=":material/verified:",
                color="green",
            )

        st.caption(
            "Phân bố lớp được tính từ tập dữ liệu đánh giá đã xử lý."
        )

        if summary is None:
            st.warning(
                "Dữ liệu đánh giá chưa sẵn sàng.",
                icon=":material/database_off:",
            )
            return

        scope = st.segmented_control(
            "Phạm vi dữ liệu",
            ["Toàn bộ", "Train", "Test"],
            default="Toàn bộ",
            format_func=lambda value: {
                "Toàn bộ": "Toàn bộ",
                "Train": "Huấn luyện",
                "Test": "Kiểm thử",
            }[value],
            key="dataset_scope",
            width="stretch",
        )

        donut_column, distribution_column = st.columns([0.9, 1.35], gap="large")
        with donut_column:
            st.altair_chart(
                build_class_distribution_chart(summary, scope or "Toàn bộ"),
                width="stretch",
                height=270,
            )

        with distribution_column:
            st.markdown("**Tách dữ liệu phân tầng giữ tỷ lệ ổn định**")
            st.altair_chart(
                build_split_distribution_chart(summary),
                width="stretch",
                height=145,
            )
            with st.container(
                key="dataset_fraud_metrics",
                horizontal=True,
                gap="small",
            ):
                st.metric(
                    "Gian lận — huấn luyện",
                    format_integer(summary.train_fraud),
                    format_percentage(summary.train_fraud / summary.train_total),
                    delta_color="off",
                    border=True,
                )
                st.metric(
                    "Gian lận — kiểm thử",
                    format_integer(summary.test_fraud),
                    format_percentage(summary.test_fraud / summary.test_total),
                    delta_color="off",
                    border=True,
                )


def render_model_comparison() -> bool:
    """Render the validated Phase 05 comparison table when available."""

    with st.container(key="comparison_panel", border=True):
        st.markdown("#### So sánh hiệu năng mô hình")
        if not COMPARISON_PATH.is_file():
            st.badge(
                "Dữ liệu so sánh chưa sẵn sàng",
                icon=":material/table_chart:",
                color="orange",
            )
            st.caption(
                "Hệ thống không hiển thị số liệu thay thế khi kết quả đánh giá bị thiếu."
            )
            return False

        try:
            comparison = load_comparison_for_display(
                COMPARISON_PATH,
                COMPARISON_PATH.stat().st_mtime_ns,
            )
        except (OSError, ValueError):
            st.badge(
                "Dữ liệu đánh giá không hợp lệ",
                icon=":material/error:",
                color="red",
            )
            st.error(
                "Không thể đọc kết quả so sánh mô hình.",
                icon=":material/data_alert:",
            )
            return False

        best_model = comparison.iloc[0]
        st.badge(
            "Dữ liệu đánh giá đã sẵn sàng",
            icon=":material/check_circle:",
            color="green",
        )
        st.success(
            f"F1 cao nhất: **{best_model['model']}** "
            f"({best_model['f1_score']:.2%}).",
            icon=":material/trophy:",
        )
        comparison_columns = {
            "model": "Mô hình", "precision": "Precision", "recall": "Recall",
            "f1_score": "F1-score", "roc_auc": "ROC-AUC", "pr_auc": "PR-AUC",
        }
        # This small overview follows instant client-side theme changes. Keep
        # the original interactive grid below for sorting and CSV export.
        with st.container(key="comparison_snapshot"):
            st.table(
                comparison[list(comparison_columns)].rename(columns=comparison_columns).style.format({
                    "Precision": "{:.2%}", "Recall": "{:.2%}", "F1-score": "{:.2%}",
                    "ROC-AUC": "{:.4f}", "PR-AUC": "{:.4f}",
                }),
                hide_index=True,
            )
        with st.expander("Sắp xếp và tải bảng dữ liệu", icon=":material/table_chart:"):
            st.dataframe(
                comparison,
                hide_index=True,
                column_order=tuple(comparison_columns),
                column_config={
                    "model": st.column_config.TextColumn("Mô hình", pinned=True),
                    "precision": st.column_config.NumberColumn("Precision", format="percent"),
                    "recall": st.column_config.NumberColumn("Recall", format="percent"),
                    "f1_score": st.column_config.NumberColumn("F1-score", format="percent"),
                    "roc_auc": st.column_config.NumberColumn("ROC-AUC", format="%.4f"),
                    "pr_auc": st.column_config.NumberColumn("PR-AUC", format="%.4f"),
                },
                width="stretch",
            )
        st.caption(
            "So sánh tập trung vào Precision, Recall, F1-score, ROC-AUC và PR-AUC; "
            "Accuracy không được dùng làm chỉ số chính."
        )
        return True


def render_evaluation_figures() -> bool:
    """Render every official Phase 05 figure currently available."""

    figure_paths = find_evaluation_figures(FIGURES_DIR)
    missing_filenames = missing_evaluation_figures(FIGURES_DIR)

    st.subheader("Biểu đồ đánh giá")
    if not figure_paths:
        with st.container(key="evaluation_pending_panel", border=True):
            st.badge(
                "Biểu đồ đánh giá chưa sẵn sàng",
                icon=":material/monitoring:",
                color="orange",
            )
            st.write(
                "ROC, Precision–Recall và ma trận nhầm lẫn sẽ hiển thị "
                "khi dữ liệu đánh giá đầy đủ."
            )
            st.caption("Không dùng biểu đồ minh họa thay cho kết quả thực nghiệm.")
        return False

    curve_specs = [
        figure
        for figure in EVALUATION_FIGURES
        if figure.category == "curves" and figure.key in figure_paths
    ]
    if curve_specs:
        curve_columns = st.columns(len(curve_specs), gap="large")
        for column, figure in zip(curve_columns, curve_specs):
            with column:
                with st.container(key=f"evaluation_figure_{figure.key}", border=True, height="stretch"):
                    st.markdown(f"#### {figure.title}")
                    st.image(
                        figure_paths[figure.key],
                        caption=figure.caption,
                        width="stretch",
                    )

    importance_specs = [
        figure
        for figure in EVALUATION_FIGURES
        if figure.category == "importance" and figure.key in figure_paths
    ]
    for figure in importance_specs:
        st.markdown("#### Đặc trưng quyết định mô hình")
        with st.container(key="feature_importance_panel", border=True):
            st.badge(
                "GIẢI THÍCH MÔ HÌNH",
                icon=":material/psychology:",
                color="blue",
            )
            st.image(
                figure_paths[figure.key],
                caption=figure.caption,
                width="stretch",
            )

    confusion_available = any(
        figure.category == "confusion" and figure.key in figure_paths
        for figure in EVALUATION_FIGURES
    )
    if confusion_available:
        st.markdown("#### Ma trận nhầm lẫn")
        st.caption(
            "Chuyển phương pháp cân bằng để đối chiếu Random Forest "
            "và XGBoost; Autoencoder không dùng tái lấy mẫu."
        )
        sampling_method = st.segmented_control(
            "Phương pháp cân bằng dữ liệu",
            options=("SMOTENC", "ADASYN"),
            default="SMOTENC",
            required=True,
            format_func=lambda value: (
                "SMOTENC • Chính thức"
                if value == "SMOTENC"
                else "ADASYN • Đối chứng"
            ),
            key="confusion_sampling_method",
            width="stretch",
            persist_state="session",
        )
        selected_keys = {
            "SMOTENC": ("confusion_rf_smotenc", "confusion_xgb_smotenc"),
            "ADASYN": ("confusion_rf_adasyn", "confusion_xgb_adasyn"),
        }[sampling_method or "SMOTENC"]
        visible_keys = (*selected_keys, "confusion_autoencoder")
        confusion_specs = [
            figure
            for figure in EVALUATION_FIGURES
            if figure.key in visible_keys and figure.key in figure_paths
        ]
        confusion_columns = st.columns(3, gap="medium")
        for column, figure in zip(confusion_columns, confusion_specs):
            with column:
                with st.container(key=f"evaluation_figure_{figure.key}", border=True, height="stretch"):
                    st.markdown(f"**{figure.title}**")
                    st.image(
                        figure_paths[figure.key],
                        caption=figure.caption,
                        width="stretch",
                    )

    component_specs = [
        figure
        for figure in EVALUATION_FIGURES
        if figure.category == "components" and figure.key in figure_paths
    ]
    for figure in component_specs:
        with st.container(key="confusion_components_panel", border=True):
            st.markdown(f"**{figure.title}**")
            st.image(
                figure_paths[figure.key],
                caption=figure.caption,
                width="stretch",
            )

    if missing_filenames:
        st.warning(
            f"Còn {len(missing_filenames)} biểu đồ chưa sẵn sàng.",
            icon=":material/pending_actions:",
        )
        return False

    return True


def render_model_performance(summary: DatasetSummary | None) -> None:
    """Render training evidence and official Phase 05 outputs fail-closed."""

    st.caption("PHÂN TÍCH HIỆU NĂNG")
    st.subheader("Hiệu năng và mức sẵn sàng")
    st.caption(
        "Theo dõi chỉ số huấn luyện, so sánh mô hình và các biểu đồ đánh giá."
    )

    render_dataset_snapshot(summary)

    st.subheader("Trạng thái mô hình")

    with st.container(key="model_status_metrics", horizontal=True, gap="small"):
        for index, (model_name, summary_path) in enumerate(TRAINING_SUMMARIES.items(), 1):
            try:
                metrics = load_training_metrics(summary_path)
                tone = {
                    "Random Forest": "rf",
                    "XGBoost": "xgb",
                    "Autoencoder": "autoencoder",
                }.get(model_name, "unavailable")
                with st.container(
                    key=f"model_metric_{tone}_{index}",
                    height="stretch",
                    gap=None,
                ):
                    st.metric(
                        model_name,
                        f"F1 {metrics['f1']:.4f}",
                        f"ROC-AUC {metrics['auc']:.4f}",
                        delta_color="off",
                        delta_arrow="off",
                        border=True,
                        height="stretch",
                    )
            except (FileNotFoundError, OSError, ValueError):
                with st.container(
                    key=f"model_metric_unavailable_{index}",
                    height="stretch",
                    gap=None,
                ):
                    st.metric(
                        model_name,
                        "Chưa có",
                        "Dữ liệu chưa sẵn sàng",
                        delta_color="off",
                        delta_arrow="off",
                        border=True,
                        height="stretch",
                    )

    render_model_comparison()
    render_evaluation_figures()


def render_analysis_history() -> None:
    """Render the persistent review workspace for successful predictions."""

    st.caption("THEO DÕI GIAO DỊCH")
    st.subheader("Lịch sử phân tích")
    st.caption(
        "Theo dõi tối đa 250 giao dịch đã được phân tích. Lịch sử được lưu trên "
        "thiết bị và vẫn còn sau khi khởi động lại ứng dụng."
    )

    storage_error = st.session_state.get("history_storage_error")
    if storage_error:
        st.error(
            "Không thể truy cập nơi lưu lịch sử trên thiết bị. Vui lòng thử lại.",
            icon=":material/database_off:",
        )

    history = st.session_state["analysis_history"]
    if not history:
        with st.container(
            key="history_empty_panel",
            border=True,
            horizontal_alignment="center",
        ):
            st.markdown("### :material/history: Chưa có giao dịch nào")
            st.caption(
                "Chạy một mẫu hoặc nhập giao dịch mới để bắt đầu tạo lịch sử."
            )
            st.button(
                "Phân tích giao dịch đầu tiên",
                icon=":material/arrow_forward:",
                type="primary",
                on_click=set_active_view,
                args=("prediction",),
            )
        return

    history_frame = pd.DataFrame(history)
    history_frame["analysis_label"] = history_frame["sequence"].map(
        lambda sequence: f"#{sequence}"
    )
    fraud_count = int(history_frame["label"].sum())
    average_probability = float(history_frame["fraud_probability"].mean())
    latest_probability = float(history_frame.iloc[-1]["fraud_probability"])

    with st.container(key="history_metrics", horizontal=True, gap="small"):
        st.metric(
            "Đã phân tích",
            len(history_frame),
            "Giao dịch trong lịch sử",
            delta_color="off",
            delta_arrow="off",
            border=True,
            height="stretch",
        )
        st.metric(
            "Cảnh báo rủi ro",
            fraud_count,
            f"{fraud_count / len(history_frame):.0%} lịch sử",
            delta_color="off",
            delta_arrow="off",
            border=True,
            height="stretch",
        )
        st.metric(
            "Xác suất trung bình",
            f"{average_probability:.2%}",
            "Trên toàn bộ lịch sử",
            delta_color="off",
            delta_arrow="off",
            border=True,
            height="stretch",
        )
        st.metric(
            "Lần gần nhất",
            f"{latest_probability:.2%}",
            "Xác suất giao dịch mới nhất",
            delta_color="off",
            delta_arrow="off",
            border=True,
            height="stretch",
        )

    filter_mode = st.segmented_control(
        "Lọc lịch sử",
        ["Tất cả", "Cảnh báo", "Hợp lệ"],
        default="Tất cả",
        key="history_filter",
        width="content",
    )
    if filter_mode == "Cảnh báo":
        filtered_frame = history_frame[history_frame["label"] == 1]
    elif filter_mode == "Hợp lệ":
        filtered_frame = history_frame[history_frame["label"] == 0]
    else:
        filtered_frame = history_frame

    chart_column, summary_column = st.columns([1.55, 1], gap="large")
    with chart_column:
        with st.container(key="history_chart_panel", border=True):
            st.markdown("**Diễn biến xác suất gian lận**")
            probability_chart = (
                alt.Chart(history_frame)
                .mark_area(
                    line={"color": "#8B5CF6", "strokeWidth": 3},
                    point={"filled": True, "size": 85},
                    color=alt.Gradient(
                        gradient="linear",
                        stops=[
                            alt.GradientStop(color="#8B5CF6", offset=0),
                            alt.GradientStop(color="#8B5CF600", offset=1),
                        ],
                        x1=1,
                        x2=1,
                        y1=0,
                        y2=1,
                    ),
                )
                .encode(
                    x=alt.X(
                        "analysis_label:N",
                        title="Lần phân tích",
                        sort=alt.SortField("sequence", order="ascending"),
                    ),
                    y=alt.Y(
                        "fraud_probability:Q",
                        title="Xác suất",
                        scale=alt.Scale(domain=[0, 1]),
                        axis=alt.Axis(format="%"),
                    ),
                    tooltip=[
                        alt.Tooltip("sequence:O", title="Lần"),
                        alt.Tooltip("fraud_probability:Q", title="Xác suất", format=".2%"),
                        alt.Tooltip("threshold:Q", title="Ngưỡng", format=".0%"),
                        alt.Tooltip("amount:Q", title="Số tiền", format=",.0f"),
                    ],
                )
            )
            threshold_chart = (
                alt.Chart(history_frame)
                .mark_line(color="#F59E0B", strokeDash=[6, 5], strokeWidth=2)
                .encode(
                    x=alt.X(
                        "analysis_label:N",
                        sort=alt.SortField("sequence", order="ascending"),
                    ),
                    y=alt.Y("threshold:Q"),
                )
            )
            st.altair_chart(
                (probability_chart + threshold_chart).properties(height=285),
                width="stretch",
            )
            st.caption("Đường nét đứt thể hiện ngưỡng cảnh báo của từng lần chạy.")

    with summary_column:
        with st.container(
            key="history_signal_panel",
            border=True,
            height="stretch",
        ):
            st.markdown("**Tín hiệu phiên hiện tại**")
            high_amount_count = int((history_frame["amount"] > 200_000).sum())
            warning_count = int((history_frame["quality_warnings"] > 0).sum())
            st.metric("Giao dịch lớn", high_amount_count, border=True)
            st.metric("Đầu vào cần lưu ý", warning_count, border=True)
            if fraud_count:
                st.error(
                    f"Có {fraud_count} giao dịch vượt ngưỡng và cần rà soát.",
                    icon=":material/gpp_maybe:",
                )
            else:
                st.success(
                    "Chưa có giao dịch nào vượt ngưỡng cảnh báo.",
                    icon=":material/verified_user:",
                )

    st.markdown("#### Chi tiết giao dịch")
    if filtered_frame.empty:
        st.info("Không có giao dịch phù hợp với bộ lọc này.", icon=":material/filter_alt:")
        return

    display_frame = filtered_frame.iloc[::-1].copy()
    display_frame["Ngày giờ minh họa"] = display_frame["step"].map(
        lambda value: step_to_datetime(int(value)).strftime("%d/%m/%Y %H:%M")
    )
    display_frame["Loại giao dịch"] = display_frame["transaction_type"].map(
        TRANSACTION_LABELS
    )
    display_frame["Kết quả"] = display_frame["label"].map(
        {0: "Hợp lệ", 1: "Cần rà soát"}
    )
    display_frame = display_frame.rename(
        columns={
            "sequence": "Lần",
            "amount": "Số tiền",
            "fraud_probability": "Xác suất",
            "threshold": "Ngưỡng",
            "quality_warnings": "Lưu ý dữ liệu",
        }
    )[
        [
            "Lần",
            "Loại giao dịch",
            "Ngày giờ minh họa",
            "Số tiền",
            "Xác suất",
            "Ngưỡng",
            "Kết quả",
            "Lưu ý dữ liệu",
        ]
    ]
    display_frame["Số tiền"] = display_frame["Số tiền"].map(format_currency)
    component_rows = [
        {
            "sequence": int(row["Lần"]),
            "transaction_type": row["Loại giao dịch"],
            "simulated_datetime": row["Ngày giờ minh họa"],
            "amount": row["Số tiền"],
            "probability": f"{float(row['Xác suất']):.0%}",
            "probability_value": float(row["Xác suất"]),
            "threshold": f"{float(row['Ngưỡng']):.0%}",
            "result": row["Kết quả"],
            "quality_warnings": int(row["Lưu ý dữ liệu"]),
        }
        for _, row in display_frame.iterrows()
    ]
    HISTORY_TABLE(
        data={"rows": component_rows},
        key="history_table",
        width="stretch",
        on_deleted_change=delete_history_row,
    )
    st.download_button(
        "Tải lịch sử CSV",
        data=display_frame.to_csv(index=False).encode("utf-8-sig"),
        file_name="fraud-analysis-history.csv",
        mime="text/csv",
        icon=":material/download:",
    )


try:
    dataset_summary = load_dataset_summary(PROCESSED_DATA_DIR)
except (FileNotFoundError, OSError, ValueError, pickle.UnpicklingError):
    dataset_summary = None

initialize_state()
active_view = render_sidebar_navigation()

if active_view == "prediction":
    render_header(dataset_summary)
    render_transaction_form()
elif active_view == "results":
    render_model_performance(dataset_summary)
else:
    render_analysis_history()
