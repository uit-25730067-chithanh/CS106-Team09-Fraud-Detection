# System Architecture — Financial Fraud Detection

## Tổng quan kiến trúc

```
┌─────────────────────────────────────────────────────────┐
│                      DATA LAYER                          │
│  paysim.csv → data/raw/ → data/processed/               │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                  PREPROCESSING PIPELINE                  │
│  1. Load data & filter (TRANSFER, CASH_OUT)              │
│  2. Stratified Downsampling to ~200,000 transactions    │
│  3. Feature scaling (StandardScaler: balances, amount)   │
│  4. One-Hot Encoding on Type column                      │
│  5. Train/Test split (stratified, 80/20)                │
│  6. Imbalance handling (SMOTE / ADASYN on train only)   │
└─────────────────────┬───────────────────────────────────┘
                      │
         ┌────────────┼────────────┐
         ▼            ▼            ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│ Random Forest│ │ XGBoost  │ │  Autoencoder │
│  (sklearn)   │ │(xgboost) │ │  (Keras)     │
└──────┬───────┘ └────┬─────┘ └──────┬───────┘
       │              │              │
       └──────────────▼──────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                  EVALUATION MODULE                       │
│  - Confusion Matrix                                      │
│  - Precision, Recall, F1-Score (per class)              │
│  - ROC-AUC Curve                                        │
│  - Cross-model comparison table                         │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                   DEMO LAYER                             │
│  Streamlit / Gradio UI — nhập giao dịch → dự đoán      │
└─────────────────────────────────────────────────────────┘
```

---

## Chi tiết các thành phần

### 1. Data Layer

| File | Mô tả |
|------|-------|
| `data/raw/paysim.csv` | File gốc từ Kaggle (không commit git) |
| `data/processed/X_train.pkl` | Features training sau scaling, encoding, downsampling |
| `data/processed/X_test.pkl` | Features test sau scaling, encoding, downsampling |
| `data/processed/y_train.pkl` | Labels training (oversampled) |
| `data/processed/y_test.pkl` | Labels test (giữ nguyên tỷ lệ downsampled) |

### 2. Preprocessing Pipeline (`src/preprocessing/`)

| Module | Chức năng |
|--------|-----------|
| `data_loader.py` | Load CSV, lọc loại giao dịch & downsampling |
| `feature_scaler.py` | StandardScaler cho balances/amount & One-Hot Encoding |
| `data_splitter.py` | Stratified train/test split |
| `imbalance_handler.py` | SMOTE và ADASYN implementation |

### 3. Models (`src/models/`)

| Module | Thuật toán | Framework |
|--------|-----------|-----------|
| `random_forest_model.py` | Random Forest Classifier | scikit-learn |
| `xgboost_model.py` | XGBoost Classifier | xgboost |
| `autoencoder_model.py` | Autoencoder (anomaly) | Keras/TF |

### 4. Evaluation (`src/evaluation/`)

| Module | Chức năng |
|--------|-----------|
| `metrics_calculator.py` | Precision, Recall, F1, AUC |
| `plot_roc_curve.py` | ROC curve visualization |
| `confusion_matrix_plot.py` | Confusion matrix heatmap |
| `model_comparator.py` | Bảng so sánh tổng hợp |

---

## Data Flow

```
paysim.csv
    ↓ [data-loader & downsampler]
Filtered & Downsampled DataFrame (~200,000 × 11)
    ↓ [feature-scaler & encoder]
Scaled & Encoded DataFrame
    ↓ [data-splitter] → 80% train | 20% test
    ↓ [imbalance-handler] → SMOTE/ADASYN trên train only
    ↓ [models] → Random Forest / XGBoost / Autoencoder
    ↓ [evaluation] → Metrics trên test set
    ↓ [reports] → Bảng so sánh, biểu đồ, kết luận
```

---

## Quyết định thiết kế quan trọng

1. **Chỉ apply SMOTE/ADASYN trên train set** — tránh data leakage, test set giữ nguyên tỷ lệ thực tế
2. **Stratified split** — đảm bảo tỷ lệ fraud được giữ trong cả train và test
3. **Không dùng Accuracy** — do imbalance quá nghiêm trọng; dùng F1-Score và ROC-AUC
4. **Mỗi model 1 notebook riêng** — tránh conflict giữa thành viên
5. **Lưu processed data vào `.pkl`** — chạy lại nhanh, không cần reprocess
