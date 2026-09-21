"""Clickable overview of the most recently submitted transaction analysis."""

from typing import Literal, Mapping

import streamlit as st

from inference import PredictionResult
from pipeline_details import STEP_TITLES, show_pipeline_details


PipelineState = Literal["idle", "complete", "edited", "invalid", "unavailable"]

PIPELINE_STYLES = """
<style>
.st-key-analysis_pipeline_heading {
    margin-top: 1rem;
}
.st-key-analysis_pipeline_panel {
    padding: clamp(1rem, 1.2vw, 1.35rem) !important;
}
.st-key-analysis_pipeline_panel > [data-testid="stElementContainer"]:has(#analysis-pipeline-overview) {
    display: none;
}
.analysis-pipeline { color: var(--st-text-color); }
.st-key-flow_card_1 { --flow-accent: var(--st-blue-color); }
.st-key-flow_card_2 { --flow-accent: var(--st-violet-color); }
.st-key-flow_card_3 { --flow-accent: var(--st-orange-color); }
.st-key-flow_card_4 { --flow-accent: var(--st-green-color); }
.st-key-analysis_pipeline_panel [class*="st-key-flow_card_"] {
    gap: 0.1rem;
    padding: 0.45rem 0.65rem 0.65rem;
    border: 1px solid var(--fraud-surface-border);
    border-left: 3px solid var(--flow-accent);
    border-radius: 0.75rem;
    background: var(--fraud-card-background);
    transition: border-color 140ms ease, background 140ms ease;
}
.st-key-analysis_pipeline_panel [class*="st-key-flow_card_"]:has(button:not(:disabled):hover) {
    border-color: var(--flow-accent);
    background: color-mix(in srgb, var(--flow-accent) 8%, transparent);
}
.st-key-analysis_pipeline_panel [class*="st-key-flow_card_"] button:focus-visible {
    outline: 2px solid var(--flow-accent);
    outline-offset: 2px;
}
.st-key-analysis_pipeline_panel [class*="st-key-flow_card_"] button {
    justify-content: space-between;
    text-align: left;
    width: 100%;
    padding: 0.2rem 0;
    min-height: 2.15rem;
    border: 0;
    box-shadow: none;
    background: transparent;
}
.st-key-analysis_pipeline_panel [class*="st-key-flow_card_"] button p {
    font-size: 0.95rem;
    text-align: left;
}
.st-key-analysis_pipeline_panel [class*="st-key-flow_card_"] button > div,
.st-key-analysis_pipeline_panel [class*="st-key-flow_card_"] button [data-has-shortcut] {
    width: 100%;
    justify-content: space-between;
}
.st-key-analysis_pipeline_panel [class*="st-key-flow_card_"] button p strong {
    color: var(--flow-accent) !important;
}
.st-key-analysis_pipeline_panel [class*="st-key-flow_card_"] button [data-testid="stIconMaterial"] {
    color: var(--st-green-color) !important;
    -webkit-text-fill-color: var(--st-green-color) !important;
}
.st-key-analysis_pipeline_panel [class*="st-key-flow_card_"] button:disabled [data-testid="stIconMaterial"] {
    color: var(--st-gray-text-color) !important;
    -webkit-text-fill-color: var(--st-gray-text-color) !important;
}
.st-key-analysis_pipeline_panel [class*="st-key-flow_card_"] [data-testid="stCaptionContainer"] p {
    font-size: 0.9rem;
    line-height: 1.5;
    color: var(--st-gray-text-color);
}
.st-key-analysis_pipeline_panel [data-testid="stCaptionContainer"],
[role="dialog"]:has(.st-key-pipeline_dialog_1) [data-testid="stCaptionContainer"] {
    opacity: 1;
}
html[data-fraud-shield-theme] [role="dialog"]:has(.st-key-pipeline_dialog_1) [data-testid="stCaptionContainer"] p {
    color: var(--st-gray-text-color);
}
.st-key-analysis_pipeline_panel:has(.flow-just-completed) .st-key-flow_card_4 {
    animation: flow-complete-glow 800ms ease-out 1;
}
@keyframes flow-complete-glow {
    0% { box-shadow: 0 0 0 0 color-mix(in srgb, var(--st-green-color) 28%, transparent); }
    100% { box-shadow: 0 0 0 0.5rem transparent; }
}
@media (prefers-reduced-motion: reduce) {
    .st-key-analysis_pipeline_panel:has(.flow-just-completed) .st-key-flow_card_4 {
        animation: none;
    }
}
/* Keep the native dialog/focus handling, but center only this detail window. */
[data-testid="stDialog"]:has(.st-key-pipeline_detail_nav) {
    --flow-dialog-surface: var(--fraud-panel-background);
    --flow-dialog-inset: var(--fraud-input-background);
    --flow-dialog-border: var(--fraud-surface-border);
    align-items: center;
    justify-content: center;
    padding: 1rem;
    overflow: hidden;
    background: rgba(2, 6, 23, 0.72);
    -webkit-backdrop-filter: blur(7px) saturate(0.86);
    backdrop-filter: blur(7px) saturate(0.86);
}
[data-testid="stDialog"]:has(.st-key-pipeline_detail_nav) > div {
    margin: 0;
    max-width: calc(100vw - 2rem);
    border-radius: 1.25rem;
}
html[data-fraud-shield-theme] [role="dialog"]:has(.st-key-pipeline_dialog_1) {
    background: var(--flow-dialog-surface) !important;
    color: var(--st-text-color) !important;
    border: 1px solid var(--flow-dialog-border);
    border-radius: 1.25rem;
    max-height: min(900px, calc(100dvh - 2rem));
    overflow: hidden;
}
[role="dialog"]:has(.st-key-pipeline_detail_nav) > div:last-child {
    min-height: 0;
    overflow-y: auto;
    overscroll-behavior: contain;
    scrollbar-width: thin;
    scrollbar-color: var(--flow-dialog-border) transparent;
}
html[data-fraud-shield-theme] [role="dialog"]:has(.st-key-pipeline_dialog_1) :is(h2, h3, h4, p, th, td) {
    color: var(--st-text-color);
}
html[data-fraud-shield-theme] [role="dialog"]:has(.st-key-pipeline_dialog_1) h3 {
    font-size: 1.15rem;
}
html[data-fraud-shield-theme] [role="dialog"]:has(.st-key-pipeline_dialog_1) h4 {
    font-size: 1rem;
}
html[data-fraud-shield-theme] [role="dialog"]:has(.st-key-pipeline_dialog_1) :is(th, td) {
    background: var(--flow-dialog-inset);
    border-color: var(--flow-dialog-border);
    font-variant-numeric: tabular-nums;
}
html[data-fraud-shield-theme] [role="dialog"]:has(.st-key-pipeline_dialog_1) th {
    background: var(--fraud-table-header);
}
html[data-fraud-shield-theme] [role="dialog"]:has(.st-key-pipeline_dialog_1) [data-testid="stMetric"] {
    background: var(--fraud-card-background);
    border-color: var(--flow-dialog-border);
}
[role="dialog"]:has(.st-key-pipeline_detail_nav) [data-testid="stTable"] > div,
[role="dialog"]:has(.st-key-pipeline_detail_nav) [data-testid="stExpander"] details {
    border-color: var(--flow-dialog-border);
}
html[data-fraud-shield-theme] [role="dialog"]:has(.st-key-pipeline_dialog_1) :is([data-testid="stMetricValue"], [data-testid="stMetricLabel"]) {
    color: var(--st-text-color);
}
html[data-fraud-shield-theme] [role="dialog"]:has(.st-key-pipeline_dialog_1) [data-testid="stVegaLiteChart"] svg text {
    fill: var(--st-text-color) !important;
}
html[data-fraud-shield-theme] [role="dialog"]:has(.st-key-pipeline_dialog_1) button[aria-label="Close"] {
    color: var(--st-gray-text-color);
}
html[data-fraud-shield-theme] [role="dialog"] [class*="st-key-pipeline_dialog_"] button {
    color: var(--st-text-color);
    background: var(--flow-dialog-inset);
    border: 1px solid var(--flow-dialog-border);
    border-radius: 0.65rem;
    padding: 0.4rem 0.85rem;
    min-height: 2.5rem;
}
html[data-fraud-shield-theme] [role="dialog"] [class*="st-key-pipeline_dialog_"] button:hover {
    border-color: var(--st-blue-color);
}
html[data-fraud-shield-theme] [role="dialog"] [class*="st-key-pipeline_dialog_"] button[kind="primary"] {
    color: var(--st-text-color);
    background: color-mix(in srgb, var(--st-blue-color) 16%, var(--flow-dialog-inset));
    border-color: var(--st-blue-color);
}
html[data-fraud-shield-theme] [role="dialog"] [class*="st-key-pipeline_dialog_"] button p {
    color: inherit;
}
.st-key-pipeline_feature_table { overflow-x: auto; }
.st-key-pipeline_feature_table table { min-width: 760px; width: 100%; }
.st-key-pipeline_feature_table :is(th, td) { padding: 0.4rem 0.5rem; }
.st-key-pipeline_feature_table :is(th, td):nth-child(3),
.st-key-pipeline_feature_table :is(th, td):nth-child(4) { text-align: right; }
[class*="st-key-pipeline_metrics_"] {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    align-items: stretch;
}
.st-key-pipeline_metrics_prediction {
    grid-template-columns: repeat(2, minmax(0, 1fr));
}
[class*="st-key-pipeline_metrics_"] > [data-testid="stElementContainer"] {
    min-width: 0;
    width: 100%;
}
[class*="st-key-pipeline_metrics_"] [data-testid="stMetric"] {
    height: 100%;
}
@media (max-width: 640px) {
    [class*="st-key-pipeline_metrics_"] {
        grid-template-columns: minmax(0, 1fr);
    }
    .st-key-pipeline_detail_nav {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.4rem;
    }
    .st-key-pipeline_detail_nav [data-testid="stElementContainer"] { width: 100%; }
    html[data-fraud-shield-theme] [role="dialog"] .st-key-pipeline_detail_nav button {
        width: 100%;
        padding-inline: 0.25rem;
    }
}
</style>
"""


def render_analysis_pipeline(
    *,
    state: PipelineState,
    prediction: PredictionResult | None,
    transaction: Mapping[str, object],
    threshold: float,
    validation_notes: list[str],
    animate: bool = False,
) -> None:
    """Open step details only for the actual submitted, unchanged transaction."""

    complete = state == "complete" and prediction is not None
    descriptions = [
        "Đối chiếu 7 trường dữ liệu và tính nhất quán của các số dư.",
        "14 đặc trưng · 10 trường số chuẩn hóa · 4 cờ nhị phân.",
        "Tính xác suất gian lận bằng mô hình đã huấn luyện.",
        f"So sánh xác suất với ngưỡng {threshold:.0%}.",
    ]
    if complete:
        descriptions[0] = (
            f"7 trường đầu vào · {len(validation_notes)} lưu ý về dữ liệu."
            if validation_notes else "7 trường đầu vào · Các số dư nhất quán."
        )
        descriptions[2] = f"Xác suất gian lận: {prediction.fraud_probability:.2%} · 1 giao dịch."
        decision = "Nghi vấn gian lận" if prediction.label else "Hợp lệ"
        descriptions[3] = f"Ngưỡng {prediction.threshold:.0%} · {decision}."

    animation_class = " flow-just-completed" if complete and animate else ""
    with st.container(key="analysis_pipeline_heading", gap=None):
        st.subheader("Quy trình phân tích", anchor="analysis-pipeline-title")
    with st.container(key="pipeline_stats", horizontal=True, gap="small"):
        st.badge("7 trường đầu vào", icon=":material/edit_note:", color="violet")
        st.badge("14 đặc trưng", icon=":material/query_stats:", color="blue")
        st.badge(
            "1 dự đoán" if complete else "Chờ dự đoán",
            icon=":material/model_training:" if complete else ":material/schedule:",
            color="green" if complete else "gray",
        )
    with st.container(key="analysis_pipeline_panel", border=True, gap="small"):
        st.html(
            PIPELINE_STYLES
            + f'<section id="analysis-pipeline-overview" class="analysis-pipeline{animation_class}" data-state="{state}"'
            ' aria-labelledby="analysis-pipeline-title"></section>'
        )
        for index, (title, description) in enumerate(zip(STEP_TITLES, descriptions), 1):
            with st.container(key=f"flow_card_{index}", gap=None):
                clicked = st.button(
                    f"**{index:02}** · {title}",
                    icon=":material/check_circle:" if complete else ":material/schedule:",
                    icon_position="right",
                    key=f"pipeline_open_{index}",
                    width="stretch",
                    type="tertiary",
                    disabled=not complete,
                )
                st.caption(description)
                if clicked:
                    st.session_state["pipeline_detail_step"] = index
                    show_pipeline_details(transaction, prediction, validation_notes)
        if not complete:
            st.caption(
                "Phân tích lại giao dịch để cập nhật và mở chi tiết từng bước."
                if state in {"edited", "invalid"} else
                "Nhập thông tin và chọn Phân tích giao dịch để bắt đầu."
                if state == "idle" else
                "Chưa có kết quả mô hình; các bước chưa được xác nhận hoàn tất."
            )
