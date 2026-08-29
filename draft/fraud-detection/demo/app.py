"""Streamlit UI shell for the CS106 fraud-detection project.

Run from ``draft/fraud-detection`` with::

    streamlit run demo/app.py

The current Sprint 2 version intentionally stops before model inference. It
captures and validates a transaction preview while making the missing-model
state explicit. Real prediction is connected in Sprint 4 after Phases 04–05.
"""

from __future__ import annotations

import pickle
import warnings
from dataclasses import asdict, dataclass
from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Fraud Shield | Nhóm 9",
    page_icon=":material/shield:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.html(
    """
    <style>
    [data-testid="stMainMenuButton"],
    [data-testid="stMainMenuPopover"] {
        visibility: hidden !important;
        pointer-events: none !important;
    }

    .st-key-theme_mode_menu {
        position: fixed;
        left: 1.15rem;
        bottom: 1rem;
        z-index: 999;
    }

    @media (max-width: 768px) {
        .st-key-theme_mode_menu {
            left: 0.85rem;
            bottom: 0.75rem;
        }
    }
    </style>
    """
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"
SCALER_PATH = PROJECT_ROOT / "models" / "scaler.pkl"
LOGO_PATH = PROJECT_ROOT / "demo" / "assets" / "fraud-shield-logo.png"
MODEL_CANDIDATES = (
    PROJECT_ROOT / "models" / "xgb_smote.pkl",
    PROJECT_ROOT / "models" / "rf_smote.pkl",
    PROJECT_ROOT / "models" / "random_forest_smote.pkl",
)
COMPARISON_PATH = PROJECT_ROOT / "reports" / "model_comparison.csv"

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
  // Streamlit 1.59 persists the active mode per URL path with schema v2.
  // Using the same key keeps this compact control independent of the native menu.
  const storageKey = `stActiveTheme-${window.location.pathname}-v2`
  const resolvedTheme = data?.current_theme === "dark" ? "Dark" : "Light"
  let reloadTimer = null

  const readStoredTheme = () => {
    try {
      const storedTheme = JSON.parse(window.localStorage.getItem(storageKey) ?? "null")
      return modes.includes(storedTheme) ? storedTheme : null
    } catch {
      return null
    }
  }

  let activeTheme = readStoredTheme() ?? resolvedTheme

  const setActiveTheme = (theme) => {
    activeTheme = theme
    buttons.forEach((button) => {
      const isActive = button.dataset.theme === theme
      button.classList.toggle("is-active", isActive)
      button.setAttribute("aria-checked", String(isActive))
    })
  }

  const showFallback = () => {
    status.textContent = "Không đổi được giao diện. Hãy tải lại trang rồi thử lại."
    status.classList.add("is-visible")
  }

  const selectTheme = (theme) => {
    status.classList.remove("is-visible")
    if (!modes.includes(theme) || theme === activeTheme) return

    try {
      window.localStorage.setItem(storageKey, JSON.stringify(theme))
      setActiveTheme(theme)
      status.textContent = "Đang chuyển giao diện…"
      status.classList.add("is-visible")
      reloadTimer = window.setTimeout(() => window.location.reload(), 80)
    } catch {
      showFallback()
    }
  }

  setActiveTheme(activeTheme)
  buttons.forEach((button) => {
    button.onclick = () => selectTheme(button.dataset.theme)
  })

  return () => {
    window.clearTimeout(reloadTimer)
    buttons.forEach((button) => {
      button.onclick = null
    })
  }
}
""",
)

if LOGO_PATH.exists():
    st.logo(LOGO_PATH, size="large", icon_image=LOGO_PATH)

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
    "balanced": {
        "title": "Cân đối",
        "eyebrow": "DÒNG TIỀN KHỚP",
        "description": "Nguồn giảm và đích tăng đúng 250.000 đơn vị.",
        "icon": ":material/balance:",
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
    "mismatch": {
        "title": "Lệch số dư",
        "eyebrow": "SOI SAI LỆCH",
        "description": "Hai đầu số dư không khớp để khám phá cảnh báo.",
        "icon": ":material/difference:",
        "color": "orange",
        "transaction": TransactionInput(
            transaction_type="TRANSFER",
            step=410,
            amount=300_000.0,
            old_balance_origin=800_000.0,
            new_balance_origin=620_000.0,
            old_balance_destination=200_000.0,
            new_balance_destination=430_000.0,
        ),
    },
    "large": {
        "title": "Giao dịch lớn",
        "eyebrow": "QUY MÔ CAO",
        "description": "2.500.000 đơn vị với dòng tiền vẫn cân đối.",
        "icon": ":material/payments:",
        "color": "violet",
        "transaction": TransactionInput(
            transaction_type="CASH_OUT",
            step=720,
            amount=2_500_000.0,
            old_balance_origin=3_000_000.0,
            new_balance_origin=500_000.0,
            old_balance_destination=10_000_000.0,
            new_balance_destination=12_500_000.0,
        ),
    },
}


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


@st.cache_resource(show_spinner=False)
def load_scaler(path: Path):
    """Load the Phase 01 scaler and report a library-version mismatch."""

    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter("always")
        with path.open("rb") as scaler_file:
            scaler = pickle.load(scaler_file)

    has_version_mismatch = any(
        item.category.__name__ == "InconsistentVersionWarning"
        for item in caught_warnings
    )
    return scaler, has_version_mismatch


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


def format_money(
    value: float,
    *,
    signed: bool = False,
    include_unit: bool = True,
) -> str:
    """Format a PaySim amount consistently for the Vietnamese UI."""

    prefix = "+" if signed and value > 0 else ""
    unit = " đơn vị" if include_unit else ""
    return f"{prefix}{value:,.0f}{unit}".replace(",", ".")


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
                    range=["#7C3AED", "#EC4899"],
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
        .mark_text(dy=17, fontSize=11, color=text_color)
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
                    range=["#7C3AED", "#EC4899"],
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

    st.session_state.setdefault("last_transaction", None)
    st.session_state.setdefault("validation_notes", [])
    st.session_state.setdefault("signal_motion_enabled", True)
    st.session_state.setdefault("active_preset", None)


def apply_transaction_preset(preset_key: str) -> None:
    """Populate the form and preview with a descriptive sample scenario."""

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
            "last_transaction": asdict(transaction),
            "validation_notes": validate_transaction(transaction),
            "active_preset": preset_key,
        }
    )


def render_sidebar(summary: DatasetSummary | None) -> None:
    """Render project-level status and resource readiness."""

    with st.sidebar:
        theme_type = st.context.theme.type

        st.title("Fraud Shield")
        st.caption("SIGNAL UNIVERSE • NHÓM 9")
        st.badge(
            "Vibrant UI • Sprint 2",
            icon=":material/auto_awesome:",
            color="violet",
        )
        st.space("small")
        with st.container(border=True):
            st.markdown("**Trạng thái tài nguyên**")
            if summary is not None:
                st.badge(
                    f"Processed data • {format_integer(summary.total)} dòng",
                    icon=":material/database:",
                    color="green",
                )
            else:
                st.badge(
                    "Chưa đọc được processed data",
                    icon=":material/error:",
                    color="red",
                )

            try:
                scaler, has_version_mismatch = load_scaler(SCALER_PATH)
                feature_count = getattr(scaler, "n_features_in_", 8)
                if has_version_mismatch:
                    st.badge(
                        "Scaler cần scikit-learn 1.9",
                        icon=":material/warning:",
                        color="orange",
                    )
                else:
                    st.badge(
                        f"Scaler sẵn sàng • {feature_count} biến",
                        icon=":material/check_circle:",
                        color="green",
                    )
            except (FileNotFoundError, OSError, pickle.UnpicklingError):
                st.badge(
                    "Chưa đọc được scaler",
                    icon=":material/error:",
                    color="red",
                )

            available_models = sum(path.exists() for path in MODEL_CANDIDATES)
            if available_models:
                st.badge(
                    f"{available_models} model đã sẵn sàng",
                    icon=":material/model_training:",
                    color="green",
                )
            else:
                st.badge(
                    "Model đang chờ huấn luyện",
                    icon=":material/schedule:",
                    color="orange",
                )

            comparison_color = "green" if COMPARISON_PATH.exists() else "orange"
            comparison_icon = (
                ":material/check_circle:"
                if COMPARISON_PATH.exists()
                else ":material/schedule:"
            )
            comparison_label = (
                "Bảng so sánh sẵn sàng"
                if COMPARISON_PATH.exists()
                else "Kết quả đang chờ Phase 05"
            )
            st.badge(
                comparison_label,
                icon=comparison_icon,
                color=comparison_color,
            )

        st.markdown("**Tiến độ pipeline**")
        st.progress(2 / 9, text="2/9 phase đã hoàn thành")
        st.caption("Phase 00–01 đã passed. UI chưa chạy suy luận khi model chưa được bàn giao.")

        with st.expander("Chuyển động giao diện", icon=":material/animation:"):
            st.toggle(
                "Nhịp tín hiệu sống",
                key="signal_motion_enabled",
                help="Tắt nếu bạn muốn giao diện đứng yên.",
            )

        st.space("small")
        st.caption("UIT • CS106.F31.CN2.TTNT • 2026")
        st.space(64)

        with st.popover(
            "Giao diện",
            icon=":material/contrast:",
            help="Chọn System, Sáng hoặc Tối.",
            type="secondary",
            width="content",
            key="theme_mode_menu",
        ):
            st.caption("SYSTEM • LIGHT • DARK")
            THEME_SWITCHER(
                key="fraud-shield-theme-switcher",
                data={"current_theme": theme_type or "light"},
                width="stretch",
                height="content",
            )


def render_signal_pulse(animated: bool) -> None:
    """Render a subtle native motion cue without implying model inference."""

    status_label = (
        "Nhịp giao diện đang hoạt động"
        if animated
        else "Nhịp giao diện đã tạm dừng"
    )
    status_state = "running" if animated else "complete"

    with st.status(status_label, state=status_state, expanded=True):
        st.caption("LIVE SIGNAL • VISUAL FLOW")
        st.markdown(
            ":blue-badge[01 • Nhận] :violet-badge[02 • Đối chiếu] "
            ":green-badge[03 • Hiển thị]"
        )
        st.progress(1.0, text="INPUT → VALIDATE → VISUALIZE")
        st.caption(
            "Biểu tượng chuyển động chỉ tạo điểm nhấn; không phải kết quả model."
        )


def render_header(summary: DatasetSummary | None) -> None:
    """Render the main page identity and high-level project facts."""

    with st.container(border=True):
        hero_copy, signal_visual = st.columns(
            [1.55, 0.85],
            gap="large",
            vertical_alignment="center",
        )

        with hero_copy:
            st.caption("FRAUD SHIELD • LIVE TRANSACTION SIGNALS")
            st.title("Bản đồ tín hiệu giao dịch")
            st.markdown(
                "Biến số tiền, thời điểm và biến động số dư thành một góc nhìn "
                "**trực quan, dễ đọc**, sẵn sàng kết nối model thật của Nhóm 9."
            )

            with st.container(horizontal=True):
                st.badge(
                    "Phase 06 • Đang phát triển",
                    icon=":material/rocket_launch:",
                    color="violet",
                )
                st.badge(
                    "Dữ liệu thật • Không kết quả giả",
                    icon=":material/verified:",
                    color="green",
                )

            with st.container(horizontal=True):
                st.badge(
                    "Model đang chờ bàn giao",
                    icon=":material/model_training:",
                    color="orange",
                )
                st.badge(
                    "Inference đang khóa an toàn",
                    icon=":material/lock:",
                    color="gray",
                )

        with signal_visual:
            render_signal_pulse(st.session_state["signal_motion_enabled"])

    total_label = format_integer(summary.total) if summary else "200.000"
    split_label = (
        f"{summary.train_total // 1000}k train • {summary.test_total // 1000}k test"
        if summary
        else "160k train • 40k test"
    )
    fraud_ratio_label = (
        format_percentage(summary.fraud_ratio) if summary else "4,11%"
    )
    available_models = sum(path.exists() for path in MODEL_CANDIDATES)

    with st.container(horizontal=True):
        st.metric(
            "Dữ liệu đã xử lý",
            f"{total_label} giao dịch",
            split_label,
            delta_color="off",
            border=True,
        )
        st.metric(
            "Tỷ lệ gian lận",
            fraud_ratio_label,
            "Tính từ y_train + y_test",
            delta_color="off",
            border=True,
        )
        st.metric(
            "Không gian đặc trưng",
            "9 biến",
            "Đã scale & encode",
            delta_color="off",
            border=True,
        )
        st.metric(
            "Model dự đoán",
            f"{available_models}/3 sẵn sàng",
            "Tích hợp sau Phase 05",
            delta_color="off",
            border=True,
        )


def render_transaction_form() -> None:
    """Render the Sprint 2 input form and non-predictive preview."""

    st.subheader("Kịch bản khám phá nhanh")
    st.caption(
        "Chạm một kịch bản để nạp dữ liệu mẫu và xem ba góc nhìn ngay lập tức. "
        "Các kịch bản chỉ mô tả cấu trúc giao dịch, không gắn nhãn gian lận."
    )
    with st.container(horizontal=True):
        for preset_key, preset in TRANSACTION_PRESETS.items():
            is_active = st.session_state["active_preset"] == preset_key
            with st.container(border=True):
                st.badge(
                    preset["eyebrow"],
                    icon=preset["icon"],
                    color=preset["color"],
                )
                st.markdown(f"#### {preset['title']}")
                st.caption(preset["description"])
                st.button(
                    "Đang khám phá" if is_active else f"Mở {preset['title'].lower()}",
                    key=f"preset_{preset_key}",
                    type="primary" if is_active else "secondary",
                    icon=":material/check:" if is_active else ":material/arrow_forward:",
                    width="stretch",
                    on_click=apply_transaction_preset,
                    args=(preset_key,),
                )

    st.space("small")

    form_column, preview_column = st.columns([1.55, 1], gap="large")

    with form_column:
        st.subheader("Nhập thông tin giao dịch")
        st.caption("Các trường bám đúng schema PaySim đã dùng trong Phase 01.")
        st.markdown(
            ":violet-badge[01 • Nhập] :blue-badge[02 • Soi tín hiệu] "
            ":gray-badge[03 • Chờ model thật]"
        )
        active_preset = st.session_state["active_preset"]
        if active_preset is not None:
            st.badge(
                f"Đang dùng kịch bản: {TRANSACTION_PRESETS[active_preset]['title']}",
                icon=":material/auto_awesome:",
                color=TRANSACTION_PRESETS[active_preset]["color"],
            )

        with st.form("transaction_form", border=True):
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

            timing_column, amount_column = st.columns([1, 1.4])
            with timing_column:
                step = st.number_input(
                    "Thời điểm (step)",
                    min_value=1,
                    max_value=744,
                    value=(
                        None
                        if "transaction_step_input" in st.session_state
                        else 120
                    ),
                    step=1,
                    help="Số giờ tính từ đầu mô phỏng PaySim.",
                    icon=":material/schedule:",
                    key="transaction_step_input",
                )
            with amount_column:
                amount = st.number_input(
                    "Số tiền giao dịch",
                    min_value=0.0,
                    value=(
                        None
                        if "transaction_amount_input" in st.session_state
                        else 250_000.0
                    ),
                    step=10_000.0,
                    format="%.0f",
                    icon=":material/payments:",
                    key="transaction_amount_input",
                )

            st.badge(
                "02 • Tài khoản nguồn",
                icon=":material/account_balance_wallet:",
                color="gray",
            )
            source_before, source_after = st.columns(2)
            with source_before:
                old_balance_origin = st.number_input(
                    "Số dư trước giao dịch",
                    min_value=0.0,
                    value=(
                        None
                        if "old_balance_origin" in st.session_state
                        else 1_000_000.0
                    ),
                    step=10_000.0,
                    format="%.0f",
                    key="old_balance_origin",
                )
            with source_after:
                new_balance_origin = st.number_input(
                    "Số dư sau giao dịch",
                    min_value=0.0,
                    value=(
                        None
                        if "new_balance_origin" in st.session_state
                        else 750_000.0
                    ),
                    step=10_000.0,
                    format="%.0f",
                    key="new_balance_origin",
                )

            st.badge(
                "03 • Tài khoản đích",
                icon=":material/account_balance:",
                color="gray",
            )
            destination_before, destination_after = st.columns(2)
            with destination_before:
                old_balance_destination = st.number_input(
                    "Số dư trước khi nhận",
                    min_value=0.0,
                    value=(
                        None
                        if "old_balance_destination" in st.session_state
                        else 500_000.0
                    ),
                    step=10_000.0,
                    format="%.0f",
                    key="old_balance_destination",
                )
            with destination_after:
                new_balance_destination = st.number_input(
                    "Số dư sau khi nhận",
                    min_value=0.0,
                    value=(
                        None
                        if "new_balance_destination" in st.session_state
                        else 750_000.0
                    ),
                    step=10_000.0,
                    format="%.0f",
                    key="new_balance_destination",
                )

            submitted = st.form_submit_button(
                "Dựng bản đồ tín hiệu",
                type="primary",
                icon=":material/radar:",
                width="stretch",
                help="Kiểm tra dữ liệu nhập; chưa chạy mô hình trong Sprint 2.",
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
            st.session_state["last_transaction"] = asdict(transaction)
            st.session_state["validation_notes"] = validate_transaction(transaction)
            st.session_state["active_preset"] = None
            st.toast(
                "Đã dựng bản đồ tín hiệu giao dịch.",
                icon=":material/query_stats:",
            )

    with preview_column:
        st.subheader("Bản xem trước")
        st.caption("Kết quả tại đây chỉ phản ánh dữ liệu đã nhập.")

        with st.container(border=True):
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
                    "**Dựng bản đồ tín hiệu**."
                )
                st.caption(
                    "Model chưa được huấn luyện nên hệ thống không hiển thị "
                    "xác suất gian lận giả."
                )
            else:
                transaction = TransactionInput(**raw_transaction)
                st.badge(
                    "Chưa chạy mô hình",
                    icon=":material/hourglass_top:",
                    color="orange",
                )
                st.markdown(
                    f"#### {TRANSACTION_LABELS[transaction.transaction_type]}"
                )
                st.caption(f"Thời điểm mô phỏng: step {transaction.step}")

                source_change = (
                    transaction.new_balance_origin
                    - transaction.old_balance_origin
                )
                st.metric(
                    "Số tiền giao dịch • đơn vị",
                    format_money(transaction.amount, include_unit=False),
                    border=True,
                )
                st.metric(
                    "Biến động tài khoản nguồn • đơn vị",
                    format_money(
                        source_change,
                        signed=True,
                        include_unit=False,
                    ),
                    border=True,
                )

                visual_mode = st.segmented_control(
                    "Góc nhìn trực quan",
                    ["Bản đồ tín hiệu", "Dòng tiền", "Sai lệch số dư"],
                    default="Bản đồ tín hiệu",
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
                elif visual_mode == "Sai lệch số dư":
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
                            {"Trường": "step", "Giá trị": str(transaction.step)},
                            {"Trường": "amount", "Giá trị": f"{transaction.amount:.0f}"},
                            {
                                "Trường": "oldbalanceOrg",
                                "Giá trị": f"{transaction.old_balance_origin:.0f}",
                            },
                            {
                                "Trường": "newbalanceOrig",
                                "Giá trị": f"{transaction.new_balance_origin:.0f}",
                            },
                            {
                                "Trường": "oldbalanceDest",
                                "Giá trị": f"{transaction.old_balance_destination:.0f}",
                            },
                            {
                                "Trường": "newbalanceDest",
                                "Giá trị": f"{transaction.new_balance_destination:.0f}",
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

        st.info(
            "Xác suất và nhãn **Hợp lệ / Nghi vấn gian lận** sẽ được "
            "mở khi model tốt nhất được bàn giao.",
            icon=":material/lock:",
        )


def render_dataset_snapshot(summary: DatasetSummary | None) -> None:
    """Render a lively, evidence-based snapshot before models are available."""

    with st.container(border=True):
        with st.container(
            horizontal=True,
            horizontal_alignment="distribute",
            vertical_alignment="center",
        ):
            st.markdown("#### Nền dữ liệu đánh giá")
            st.badge(
                "Số liệu thật • Phase 01",
                icon=":material/verified:",
                color="green",
            )

        st.caption(
            "Phân bố dưới đây được đọc trực tiếp từ y_train.pkl và y_test.pkl; "
            "không phải dữ liệu minh họa."
        )

        if summary is None:
            st.warning(
                "Chưa đọc được processed labels để tạo trực quan hóa.",
                icon=":material/database_off:",
            )
            return

        scope = st.segmented_control(
            "Phạm vi dữ liệu",
            ["Toàn bộ", "Train", "Test"],
            default="Toàn bộ",
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
            st.markdown("**Stratified split giữ tỷ lệ ổn định**")
            st.altair_chart(
                build_split_distribution_chart(summary),
                width="stretch",
                height=145,
            )
            with st.container(horizontal=True):
                st.metric(
                    "Fraud train",
                    format_integer(summary.train_fraud),
                    format_percentage(summary.train_fraud / summary.train_total),
                    delta_color="off",
                    border=True,
                )
                st.metric(
                    "Fraud test",
                    format_integer(summary.test_fraud),
                    format_percentage(summary.test_fraud / summary.test_total),
                    delta_color="off",
                    border=True,
                )


def render_results_placeholder(summary: DatasetSummary | None) -> None:
    """Render honest placeholders for Phase 05 outputs."""

    st.caption("MODEL PERFORMANCE WORKSPACE")
    st.subheader("Hiệu năng và mức sẵn sàng")
    st.caption(
        "Dữ liệu đánh giá đã sẵn sàng; metric mô hình sẽ tự động đọc artifact "
        "do Khang bàn giao trong Phase 05."
    )

    render_dataset_snapshot(summary)

    st.subheader("Trạng thái mô hình")

    with st.container(horizontal=True):
        st.metric("Random Forest", "Chưa có", "Phase 03", delta_color="off", border=True)
        st.metric("XGBoost", "Chưa có", "Phase 04", delta_color="off", border=True)
        st.metric("Autoencoder", "Chưa có", "Phase 04", delta_color="off", border=True)

    comparison_column, chart_column = st.columns(2, gap="large")
    with comparison_column:
        with st.container(border=True, height="stretch"):
            st.badge(
                "Đang chờ model_comparison.csv",
                icon=":material/table_chart:",
                color="orange",
            )
            st.markdown("#### Bảng so sánh")
            st.write("Khu vực này sẽ hiển thị Precision, Recall, F1-score và ROC-AUC.")
            st.caption("Không dùng Accuracy làm metric chính do dữ liệu mất cân bằng.")

    with chart_column:
        with st.container(border=True, height="stretch"):
            st.badge(
                "Đang chờ figures",
                icon=":material/monitoring:",
                color="orange",
            )
            st.markdown("#### Biểu đồ đánh giá")
            st.write("ROC, Precision–Recall và confusion matrix sẽ xuất hiện tại đây.")
            st.caption("UI không tự tạo số liệu mô phỏng để thay cho kết quả thực nghiệm.")


def render_project_info(summary: DatasetSummary | None) -> None:
    """Render concise project and pipeline information."""

    overview_column, pipeline_column = st.columns([1, 1.35], gap="large")

    with overview_column:
        with st.container(border=True):
            st.subheader("Về dự án")
            processed_total = format_integer(summary.total) if summary else "200.000"
            st.markdown(
                f"""
                **Bài toán:** Phân loại nhị phân giao dịch tài chính  
                **Dữ liệu:** PaySim Mobile Money  
                **Quy mô gốc:** 6.362.620 giao dịch  
                **Sau preprocessing:** {processed_total} giao dịch  
                **Mô hình:** Random Forest, XGBoost, Autoencoder  
                **Metric chính:** F1-score, ROC-AUC, Precision, Recall
                """
            )

        with st.container(border=True):
            st.subheader("Phụ trách demo")
            st.markdown("**Phạm Thành Trung • MSSV 26410141**")
            st.caption("Wireframe → UI shell → Kết nối model → Demo clip")

    with pipeline_column:
        with st.container(border=True):
            st.subheader("Pipeline thực hiện")
            st.markdown(
                """
                1. :green-badge[Đã xong] EDA và preprocessing
                2. :orange-badge[Đang chờ] SMOTE / ADASYN trên train set
                3. :orange-badge[Đang chờ] Huấn luyện ba mô hình
                4. :orange-badge[Đang chờ] Đánh giá và chọn mô hình tốt nhất
                5. :blue-badge[Đang làm] Tích hợp Streamlit UI
                6. :gray-badge[Cuối kỳ] Quay clip và đóng gói bản nộp
                """
            )

            st.info(
                "SMOTE/ADASYN chỉ áp dụng trên tập train; test set được giữ nguyên "
                "để tránh rò rỉ dữ liệu.",
                icon=":material/security:",
            )


try:
    dataset_summary = load_dataset_summary(PROCESSED_DATA_DIR)
except (FileNotFoundError, OSError, ValueError, pickle.UnpicklingError):
    dataset_summary = None

initialize_state()
render_sidebar(dataset_summary)
render_header(dataset_summary)

prediction_tab, results_tab, info_tab = st.tabs(
    [
        ":material/shield: Phân tích giao dịch",
        ":material/analytics: Hiệu năng mô hình",
        ":material/info: Hồ sơ dự án",
    ]
)

with prediction_tab:
    render_transaction_form()

with results_tab:
    render_results_placeholder(dataset_summary)

with info_tab:
    render_project_info(dataset_summary)
