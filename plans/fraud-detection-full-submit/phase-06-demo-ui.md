# Phase 06 — Demo UI (Streamlit)

**Parent plan:** [plan.md](./plan.md)  
**Depends on:** [Phase 05](./phase-05-evaluation-comparison.md) — PASSED *(kết nối model thật — Sprint 4)*  
**Early Start:** Wireframe + UI shell + placeholder predict từ **Sprint 2** — không cần model  
**Parallel with:** [Phase 07](./phase-07-report-ppt.md)  
**Next phase:** [Phase 08 — Submit Package](./phase-08-submit-package.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Trung** |
| Priority | P1 — Cần thiết nhưng không block báo cáo |
| Status | `pending` |
| Review | ⬜ Not reviewed |
| Estimated effort | 2–3 giờ |
| Sprint | Sprint 2–3 (UI shell), Sprint 4 (kết nối model + demo clip) |

## ⚡ Early Start Tasks — Trung bắt đầu từ Sprint 2 (không cần đợi model)

> Xây UI shell trong Sprint 2–3. Khi Cẩm lưu `.pkl` (Sprint 4), chỉ cần **swap placeholder → model thật**.

| Task | Sprint | Ghi chú |
|------|--------|----------|
| Thiết kế wireframe UI (layout, input fields, output area) | Sprint 2 | Figma / vẽ tay / mô tả |
| Implement Streamlit form nhập thông tin giao dịch | Sprint 2 | Chưa cần model |
| Viết placeholder `predict()` function (mock output) | Sprint 3 | Return random prob để test UI |
| Kết nối model `.pkl` thật + hiển thị kết quả & probability | Sprint 4 | Cần `.pkl` từ Cẩm |
| Quay clip demo + viết user guide ngắn | Sprint 4 | |

## Context

Trung build Demo UI để visualize kết quả và cho phép nhập giao dịch thử dự đoán. Sử dụng Streamlit (đơn giản, phù hợp academic demo).

## Requirements

- Load best model (từ Phase 05 kết luận)
- UI cho phép nhập giá trị 1 giao dịch và predict
- Hiển thị metrics tổng quan (bảng so sánh từ `reports/model_comparison.csv`)
- Hiển thị các figures đã tạo (ROC, confusion matrix)
- Chạy được bằng `streamlit run demo/app.py`

## Key Insights

- Streamlit: `pip install streamlit` — không cần thêm vào requirements chính nếu chỉ demo
- Load model một lần với `@st.cache_resource`
- Demo UI không cần chạy trên production — chỉ cần screenshot/clip

## Related Files

```
draft/fraud-detection/
├── demo/
│   ├── app.py                    ← [TẠO MỚI] Main Streamlit app
│   └── requirements-demo.txt    ← [TẠO MỚI] streamlit + deps
└── reports/
    ├── figures/                  ← Dùng figures từ Phase 05
    └── model_comparison.csv     ← Load cho bảng tổng hợp
```

## Implementation Steps

### Step 1 — `demo/requirements-demo.txt`

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
xgboost>=2.0.0
matplotlib>=3.7.0
plotly>=5.15.0
```

### Step 2 — `demo/app.py`

```python
"""
Fraud Detection Demo — Streamlit App
Run: streamlit run demo/app.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pickle
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Fraud Detection — Nhóm 9",
    page_icon="🔍",
    layout="wide",
)

# ─── Load Resources ───────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_resource
def load_best_model():
    """Load the best performing model (XGBoost or RF)."""
    model_path = os.path.join(PROJECT_ROOT, "models", "xgb_smote.pkl")  # update to best model
    with open(model_path, "rb") as f:
        return pickle.load(f)

@st.cache_resource
def load_scaler():
    """Load the fitted StandardScaler."""
    scaler_path = os.path.join(PROJECT_ROOT, "models", "scaler.pkl")
    with open(scaler_path, "rb") as f:
        return pickle.load(f)

@st.cache_data
def load_comparison():
    path = os.path.join(PROJECT_ROOT, "reports", "model_comparison.csv")
    return pd.read_csv(path)

@st.cache_data
def load_sample_data():
    """Load a few sample transactions for demo."""
    X_path = os.path.join(PROJECT_ROOT, "data", "processed", "X_test.pkl")
    y_path = os.path.join(PROJECT_ROOT, "data", "processed", "y_test.pkl")
    with open(X_path, "rb") as f:
        X_test = pickle.load(f)
    with open(y_path, "rb") as f:
        y_test = pickle.load(f)
    return X_test, y_test

# ─── Header ───────────────────────────────────────────────────────────────────
st.title("🔍 Hệ thống Phát hiện Giao dịch Gian lận")
st.markdown("""
**Môn học:** CS106 — Trí tuệ Nhân tạo | **Nhóm:** 9 | **Đề tài:** #7
""")

st.divider()

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🎯 Dự đoán", "📊 Kết quả Models", "ℹ️ Thông tin"])

# ─── Tab 1: Prediction ────────────────────────────────────────────────────────
with tab1:
    st.header("Nhập thông tin giao dịch")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tx_type = st.selectbox("Loại giao dịch (Type)", ["TRANSFER", "CASH_OUT"])
        amount = st.number_input("Số tiền giao dịch (Amount)", min_value=0.0, value=1000.0)
        step = st.number_input("Thời gian (Step - giờ trong tháng)", min_value=1, max_value=744, value=1)
    
    with col2:
        oldbalanceOrg = st.number_input("Số dư gửi ban đầu (oldbalanceOrg)", min_value=0.0, value=5000.0)
        newbalanceOrig = st.number_input("Số dư gửi lúc sau (newbalanceOrig)", min_value=0.0, value=4000.0)
        oldbalanceDest = st.number_input("Số dư nhận ban đầu (oldbalanceDest)", min_value=0.0, value=0.0)
        newbalanceDest = st.number_input("Số dư nhận lúc sau (newbalanceDest)", min_value=0.0, value=1000.0)
    
    if st.button("🔮 Dự đoán", type="primary"):
        model = load_best_model()
        scaler = load_scaler()
        
        # 1. Tạo input DataFrame
        input_data = {
            "step": [step],
            "type": [tx_type],
            "amount": [amount],
            "oldbalanceOrg": [oldbalanceOrg],
            "newbalanceOrig": [newbalanceOrig],
            "oldbalanceDest": [oldbalanceDest],
            "newbalanceDest": [newbalanceDest],
            "nameOrig": ["C_DEMO"], # Placeholder
            "nameDest": ["M_DEMO" if tx_type == "PAYMENT" else "C_DEMO"] # Placeholder
        }
        X_input = pd.DataFrame(input_data)
        
        # 2. Feature Engineering
        X_input["errorBalanceOrig"] = X_input["oldbalanceOrg"] - X_input["amount"] - X_input["newbalanceOrig"]
        X_input["errorBalanceDest"] = X_input["oldbalanceDest"] + X_input["amount"] - X_input["newbalanceDest"]
        
        # 3. One-Hot Encoding type (đảm bảo khớp với tập train: type_TRANSFER)
        # Giả sử trong tập train chỉ có type_TRANSFER (type_CASH_OUT bị loại bỏ khi drop_first=True)
        # Hoặc viết logic OHE khớp chính xác với scaler/model:
        X_input["type_TRANSFER"] = 1 if tx_type == "TRANSFER" else 0
        
        # 4. Scale các cột số
        cols_to_scale = ["amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest", "step", "errorBalanceOrig", "errorBalanceDest"]
        X_input[cols_to_scale] = scaler.transform(X_input[cols_to_scale])
        
        # 5. Drop các cột ID không dùng
        X_input_processed = X_input[["step", "amount", "oldbalanceOrg", "newbalanceOrig", "oldbalanceDest", "newbalanceDest", "errorBalanceOrig", "errorBalanceDest", "type_TRANSFER"]]
        
        prob = model.predict_proba(X_input_processed)[0][1]
        pred = model.predict(X_input_processed)[0]
        
        if pred == 1:
            st.error(f"⚠️ **GIAO DỊCH NGHI VẤN GIAN LẬN** (Xác suất: {prob:.1%})")
        else:
            st.success(f"✅ **GIAO DỊCH HỢP LỆ** (Xác suất gian lận: {prob:.1%})")
        
        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prob * 100,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": "Fraud Probability (%)"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "red" if prob > 0.5 else "green"},
                "steps": [
                    {"range": [0, 30], "color": "lightgreen"},
                    {"range": [30, 70], "color": "yellow"},
                    {"range": [70, 100], "color": "lightsalmon"},
                ],
                "threshold": {"line": {"color": "red", "width": 4}, "value": 50},
            },
        ))
        st.plotly_chart(fig, use_container_width=True)

# ─── Tab 2: Results ───────────────────────────────────────────────────────────
with tab2:
    st.header("📊 So sánh hiệu năng các Models")
    
    try:
        df_compare = load_comparison()
        st.dataframe(df_compare, use_container_width=True)
    except FileNotFoundError:
        st.warning("Chưa có kết quả comparison. Cần chạy Phase 05 trước.")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("ROC Curves")
        try:
            st.image("reports/figures/roc_curves_all.png")
        except:
            st.info("ROC curve figure chưa có")
    
    with col2:
        st.subheader("Precision-Recall Curves")
        try:
            st.image("reports/figures/pr_curves_all.png")
        except:
            st.info("PR curve figure chưa có")
    
    st.subheader("Confusion Matrices")
    cols = st.columns(3)
    for i, (name, fig_name) in enumerate([
        ("Random Forest", "confusion_matrix_random_forest.png"),
        ("XGBoost", "confusion_matrix_xgboost.png"),
        ("Autoencoder", "confusion_matrix_autoencoder.png"),
    ]):
        with cols[i]:
            st.caption(name)
            try:
                st.image(f"reports/figures/{fig_name}")
            except:
                st.info(f"{name} figure chưa có")

# ─── Tab 3: Info ──────────────────────────────────────────────────────────────
with tab3:
    st.header("ℹ️ Thông tin dự án")
    st.markdown("""
    **Dataset:** PaySim Mobile Money Fraud Detection (Kaggle)
    - 6.36 triệu giao dịch (lọc & downsample còn ~200k) | 11 features | Fraud ratio: ~0.13%
    
    **Pipeline:**
    1. EDA & Preprocessing & Downsampling (Thanh)
    2. Feature Engineering (errorBalance) & Encoding (Thanh)
    3. Imbalance Handling: SMOTE + ADASYN (Sơn)
    4. Random Forest (Sơn)
    5. XGBoost + Autoencoder (Cẩm)
    6. Evaluation (Khang)
    
    **Metrics chính:** F1-Score, ROC-AUC (không dùng Accuracy do imbalanced data)
    """)
```

### Step 3 — Test Run

```bash
cd draft/fraud-detection
source .venv/bin/activate
pip install streamlit plotly
streamlit run demo/app.py
```

### Step 4 — Record Demo

Sau khi app chạy OK:
1. Chụp screenshot các tab
2. Optional: quay screen clip 1–2 phút
3. Lưu vào `demo/screenshots/` hoặc `demo/demo_clip.mp4`

## Checklist

- [ ] `demo/app.py` tạo xong
- [ ] `demo/requirements-demo.txt` tạo xong
- [ ] `streamlit run demo/app.py` chạy không error
- [ ] Tab "Dự đoán" hoạt động — nhập giá trị → predict → hiển thị kết quả
- [ ] Tab "Kết quả Models" hiển thị được comparison table
- [ ] Tab "Kết quả Models" hiển thị được ít nhất 1 figure
- [ ] Screenshot app lưu vào `demo/screenshots/`
- [ ] App chạy với `data/processed/*.pkl` và `models/*.pkl` từ các phases trước

## Success Criteria

| Criterion | Expected | Evidence |
|-----------|---------|---------|
| App starts | `streamlit run` OK | ___________ |
| Prediction works | No error on predict | ___________ |
| Figures displayed | ≥ 2 figures visible | ___________ |
| Screenshot captured | ≥ 1 screenshot | ___________ |

## Evidence Section *(điền sau khi làm)*

```
App URL: http://localhost:____
Tabs working: Dự đoán ✅/❌  Kết quả ✅/❌  Info ✅/❌
Screenshot count: ____
Demo clip: ✅/❌
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Model file path wrong | Medium | Medium | Use absolute paths or `os.path.join` from project root |
| Streamlit version conflict | Low | Low | Pin to 1.28+ in requirements-demo.txt |
| figures not found | Low | Low | Add try/except + fallback message (already in code) |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa hoàn thành

```
Hoàn thành: __/__/2026
Người thực hiện: Trung
App URL tested: http://localhost:____
Features working: ...
Screenshots location: demo/screenshots/
```

## Commit

```bash
git add demo/ 
git commit -m "feat(phase06): Streamlit demo UI with prediction + visualization tabs"
```
