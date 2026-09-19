"""Read-only, visual explanations of the exact submitted inference result."""

from typing import Mapping

import altair as alt
import pandas as pd
import streamlit as st

from inference import MODEL_FEATURES, SCALED_FEATURES, PredictionResult
from input_formatting import format_currency, step_to_datetime


STEP_TITLES = (
    "Kiểm tra đầu vào",
    "Tạo đặc trưng & chuẩn hóa",
    "Dự đoán bằng XGBoost",
    "Phân loại theo ngưỡng",
)

FEATURE_LABELS = (
    "Bước thời gian",
    "Số tiền giao dịch",
    "Số dư nguồn trước",
    "Số dư nguồn sau",
    "Số dư đích trước",
    "Số dư đích sau",
    "Cạn tài khoản nguồn",
    "Giờ trong ngày",
    "Giao dịch ban đêm",
    "Tỷ lệ tiền / số dư nguồn",
    "Giao dịch lớn",
    "Sai lệch số dư nguồn",
    "Sai lệch số dư đích",
    "Là chuyển khoản",
)


def feature_trace_table(prediction: PredictionResult) -> pd.DataFrame:
    """Build the explanation from captured model inputs, not a second transform."""

    trace = prediction.feature_trace
    if trace is None:
        raise ValueError("Chưa có dữ liệu đặc trưng của lần phân tích này.")
    return pd.DataFrame({
        "Đặc trưng": FEATURE_LABELS,
        "Trường mô hình": MODEL_FEATURES,
        "Trước chuẩn hóa": trace.raw_values,
        "Đưa vào mô hình": trace.model_values,
        "Xử lý": [
            "StandardScaler" if feature in SCALED_FEATURES else "Giữ nguyên 0/1"
            for feature in MODEL_FEATURES
        ],
    })


def _show_input_step(transaction: Mapping[str, object], notes: list[str]) -> None:
    st.write("Dữ liệu của giao dịch vừa phân tích được kiểm tra và đối chiếu trước khi tạo đặc trưng.")
    time_value = step_to_datetime(int(transaction["step"]))
    fields = [
        ("Loại giao dịch", "Chuyển khoản" if transaction["transaction_type"] == "TRANSFER" else "Rút tiền"),
        ("Thời điểm mô phỏng", f"{time_value:%d/%m/%Y %H:%M} · Step {transaction['step']}"),
        ("Số tiền giao dịch", format_currency(transaction["amount"])),
        ("Số dư nguồn trước", format_currency(transaction["old_balance_origin"])),
        ("Số dư nguồn sau", format_currency(transaction["new_balance_origin"])),
        ("Số dư đích trước", format_currency(transaction["old_balance_destination"])),
        ("Số dư đích sau", format_currency(transaction["new_balance_destination"])),
    ]
    data_column, check_column = st.columns([1.25, 1], gap="large")
    with data_column:
        st.markdown("#### 7 trường đầu vào")
        st.table(pd.DataFrame(fields, columns=["Trường dữ liệu", "Giá trị đã phân tích"]), hide_index=True)
        st.caption("Đơn vị tiền mô phỏng PaySim; số tiền hiển thị tối đa 2 chữ số thập phân.")
    with check_column:
        st.markdown("#### Đối chiếu số dư")
        origin_error = (
            transaction["old_balance_origin"] - transaction["amount"]
            - transaction["new_balance_origin"]
        )
        destination_error = (
            transaction["old_balance_destination"] + transaction["amount"]
            - transaction["new_balance_destination"]
        )
        st.metric("Sai lệch nguồn", format_currency(origin_error), border=True)
        st.caption("Số dư trước − số tiền − số dư sau")
        st.metric("Sai lệch đích", format_currency(destination_error), border=True)
        st.caption("Số dư trước + số tiền − số dư sau")
        if notes:
            for note in notes:
                st.warning(note, icon=":material/info:")
        else:
            st.success("Các số dư nhất quán với giao dịch.", icon=":material/check_circle:")
    st.caption("Sai lệch số dư là tín hiệu đầu vào; nhãn phân loại được xác định ở bước 4 từ kết quả mô hình.")


def _show_features_step(prediction: PredictionResult) -> None:
    if prediction.feature_trace is None:
        st.info("Chạy lại Phân tích giao dịch để xem các đặc trưng.")
        return
    with st.container(horizontal=True, key="pipeline_metrics_features"):
        st.metric("Đặc trưng đầu vào", 14, border=True)
        st.metric("Trường số chuẩn hóa", 10, border=True)
        st.metric("Cờ nhị phân giữ nguyên", 4, border=True)
    st.write("Bảng dưới là dữ liệu trước chuẩn hóa và đúng hàng dữ liệu đã đưa vào XGBoost trong lần phân tích này.")
    # A semantic table follows the client-side theme instantly, unlike a canvas
    # grid. Preserve the full captured floats; round only the displayed text.
    def format_number(value: float) -> str:
        if abs(value) < 1e-9:
            value = 0.0
        return f"{value:,.6f}".rstrip("0").rstrip(".").translate(str.maketrans(",.", ".,"))

    with st.container(key="pipeline_feature_table"):
        st.table(
            feature_trace_table(prediction).style.format({
                "Trước chuẩn hóa": format_number,
                "Đưa vào mô hình": format_number,
            }),
            hide_index=True,
        )
    st.caption("Giá trị hiển thị được làm tròn tối đa 6 chữ số thập phân; dữ liệu tính toán giữ nguyên độ chính xác.")
    with st.expander("Các đặc trưng được tính như thế nào?", icon=":material/functions:"):
        st.table(pd.DataFrame([
            ("Giờ trong ngày", "step % 24"),
            ("Ban đêm", "1 nếu giờ < 6; ngược lại 0"),
            ("Cạn tài khoản", "1 nếu số dư nguồn trước > 0 và sau = 0"),
            ("Giao dịch lớn", "1 nếu số tiền > 200.000 đơn vị"),
            ("Tỷ lệ tiền / số dư nguồn", "Số tiền / (số dư nguồn trước + 0,00001)"),
            ("Sai lệch nguồn", "Số dư nguồn trước − số tiền − số dư nguồn sau"),
            ("Sai lệch đích", "Số dư đích trước + số tiền − số dư đích sau"),
            ("Là chuyển khoản", "TRANSFER = 1; CASH_OUT = 0"),
        ], columns=["Đặc trưng", "Cách tính"]), hide_index=True)
    st.caption("StandardScaler dùng trung bình và độ lệch chuẩn đã học trên tập huấn luyện. Các giá trị sau chuẩn hóa không còn mang đơn vị tiền tệ.")


def _probability_chart(prediction: PredictionResult, *, threshold: bool = False):
    data = pd.DataFrame({
        "Kết quả": ["Hợp lệ", "Gian lận"],
        "Xác suất": [1 - prediction.fraud_probability, prediction.fraud_probability],
    })
    bars = alt.Chart(data).mark_bar(cornerRadiusEnd=6, size=30).encode(
        y=alt.Y("Kết quả:N", sort=["Hợp lệ", "Gian lận"], title=None),
        x=alt.X("Xác suất:Q", scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(
            format=".0%", values=[0, 0.25, 0.5, 0.75, 1], title="Xác suất",
        )),
        color=alt.Color("Kết quả:N", scale=alt.Scale(
            domain=["Hợp lệ", "Gian lận"], range=["#16a34a", "#f43f5e"],
        ), legend=None),
        tooltip=["Kết quả:N", alt.Tooltip("Xác suất:Q", format=".2%")],
    )
    if not threshold:
        return bars.properties(height=150, background="transparent").configure_view(stroke=None)
    rule = alt.Chart(pd.DataFrame({"Ngưỡng": [prediction.threshold]})).mark_rule(
        color="#f59e0b", strokeDash=[6, 4], strokeWidth=2,
    ).encode(x=alt.X("Ngưỡng:Q", title="Xác suất"), tooltip=[alt.Tooltip("Ngưỡng:Q", format=".0%")])
    return (bars + rule).properties(height=150, background="transparent").configure_view(stroke=None)


def _show_prediction_step(prediction: PredictionResult) -> None:
    st.write("XGBoost nhận một hàng gồm 14 đặc trưng đã xử lý và trả về xác suất cho hai lớp.")
    with st.container(horizontal=True, key="pipeline_metrics_prediction"):
        st.metric("Xác suất hợp lệ", f"{1 - prediction.fraud_probability:.2%}", border=True)
        st.metric("Xác suất gian lận", f"{prediction.fraud_probability:.2%}", border=True)
    st.altair_chart(_probability_chart(prediction), width="stretch")
    st.caption("Các tỷ lệ là đầu ra của mô hình cho giao dịch này. Nhãn cảnh báo còn phụ thuộc ngưỡng ở bước tiếp theo.")


def _show_decision_step(prediction: PredictionResult) -> None:
    probability, threshold = prediction.fraud_probability, prediction.threshold
    with st.container(horizontal=True, key="pipeline_metrics_decision"):
        st.metric("Xác suất gian lận", f"{probability:.2%}", border=True)
        st.metric("Ngưỡng cảnh báo", f"{threshold:.0%}", border=True)
        st.metric("Chênh lệch với ngưỡng", f"{(probability - threshold) * 100:+.2f} điểm %", border=True)
    st.altair_chart(_probability_chart(prediction, threshold=True), width="stretch")
    st.caption("Vạch vàng là ngưỡng; đối chiếu ngưỡng với thanh xác suất gian lận.")
    operator = "≥" if prediction.label else "<"
    decision = "Nghi vấn gian lận" if prediction.label else "Hợp lệ"
    message = f"{probability:.2%} {operator} {threshold:.0%} → {decision}"
    if prediction.label:
        st.error(message, icon=":material/gpp_maybe:")
    else:
        st.success(message, icon=":material/verified_user:")
    st.table(pd.DataFrame([
        ("Xác suất ≥ ngưỡng", "Gắn cờ nghi vấn gian lận"),
        ("Xác suất < ngưỡng", "Phân loại hợp lệ"),
    ], columns=["Điều kiện", "Quyết định"]), hide_index=True)
    st.caption("Thay đổi ngưỡng có thể đổi nhãn, nhưng không làm thay đổi xác suất do mô hình tính. Phép so sánh dùng giá trị đầy đủ trước khi làm tròn để hiển thị.")


@st.dialog("Khám phá quy trình phân tích", width="large", icon=":material/account_tree:")
def show_pipeline_details(
    transaction: Mapping[str, object], prediction: PredictionResult,
    validation_notes: list[str],
) -> None:
    """Navigate read-only details inside the dialog without recording history."""

    current_step = st.session_state.get("pipeline_detail_step", 1)
    with st.container(horizontal=True, gap="small", key="pipeline_detail_nav"):
        for index in range(1, 5):
            if st.button(
                f"Bước {index:02}", key=f"pipeline_dialog_{index}",
                type="primary" if index == current_step else "secondary",
            ):
                st.session_state["pipeline_detail_step"] = index
                st.rerun(scope="fragment")
    step = st.session_state.get("pipeline_detail_step", 1)
    st.subheader(f"{step:02} · {STEP_TITLES[step - 1]}")
    if step == 1:
        _show_input_step(transaction, validation_notes)
    elif step == 2:
        _show_features_step(prediction)
    elif step == 3:
        _show_prediction_step(prediction)
    else:
        _show_decision_step(prediction)
