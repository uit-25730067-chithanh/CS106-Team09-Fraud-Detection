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
│  3. Train/Test split (stratified, 80/20)                │
│  4. Feature Engineering (7 đặc trưng: 2 errorBalances + 5 derived) │
│  5. Feature scaling (StandardScaler: continuous features)│
│     fit trên train set, transform cả train & test        │
│  6. One-Hot Encoding on Type column                      │
│  7. Drop unused columns (nameOrig, nameDest, isFlaggedFraud) │
│  8. Imbalance handling (SMOTE / ADASYN on train only)   │
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
| `data/raw/paysim.csv` | File gốc từ Kaggle (**không commit git** — ~500MB) |
| `data/processed/X_train.pkl` | Features training: 160,000 × 14, đã scale + encode (**đã commit**) |
| `data/processed/X_test.pkl` | Features test: 40,000 × 14 (**đã commit**) |
| `data/processed/y_train.pkl` | Labels training, trước oversample (**đã commit**) |
| `data/processed/y_test.pkl` | Labels test, giữ nguyên tỷ lệ thực tế (**đã commit**) |
| `models/scaler.pkl` | Fitted StandardScaler, dùng khi predict mới (**đã commit**) |

### 2. Preprocessing Pipeline (`src/preprocessing/`)

| Module | Chức năng |
|--------|-----------|
| `data_loader.py` | Load CSV, lọc loại giao dịch & downsampling |
| `feature_scaler.py` | Tạo 7 đặc trưng mới, StandardScaler cho continuous & One-Hot Encoding |
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
    ↓ [data-splitter] → 80% train | 20% test
Train DataFrame (80%)          Test DataFrame (20%)
    ↓ [feature-engineering]       ↓ [feature-engineering]
7 features mới thêm vào cả 2 tập (2 errorBalances + 5 derived)
    ↓ [feature-scaler & encoder]    ↓ [transform only — không fit]
Scaled & Encoded Train Set (14 cols) Scaled & Encoded Test Set (14 cols)
    ↓ ↳ Lưu: X_train.pkl, y_train.pkl   ↳ Lưu: X_test.pkl, y_test.pkl
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
