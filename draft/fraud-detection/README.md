# 🔍 Hệ thống Phát hiện Giao dịch Tài chính Bất thường (Financial Fraud Detection)

> **Môn học:** Trí tuệ Nhân tạo (CS106.F31.CN2.TTNT) — UIT, ĐHQG-HCM  
> **Đề tài số:** 7  
> **Nhóm:** 9

---

## 👥 Thành viên & Phân công

> 📌 Xem chi tiết tasks từng phase tại: [project-roadmap.md](./docs/project-roadmap.md)

| STT | Họ tên | MSSV | Lớp | Vai trò chính | Tasks |
|-----|--------|------|-----|---------------|-------|
| 1 | **Trần Hoàng Hôn** (Nhóm trưởng) | 26410046 | A | PM + Theo dõi tiến độ + PPT + Nộp bài | 5 |
| 2 | **Nguyễn Duy Khang** | 26410055 | A | Viết Evaluation scripts + Chạy metrics + Bảng so sánh | 6 |
| 3 | **Vũ Văn Duy** | 26410031 | A | Báo cáo Word: Intro → Methodology → Results → Format | 6 |
| 4 | **Phạm Thành Trung** | 26410141 | A | Demo UI: Wireframe → Implement → Kết nối model → Demo clip | 5 |
| 5 | **Đặng Chí Thanh** | 25730067 | B | EDA + Preprocessing + Feature Engineering | 5 |
| 6 | **Bùi Thị Mỷ Cẩm** | 25730013 | B | XGBoost + Autoencoder + Lưu models (.pkl/.h5) | 5 |
| 7 | **Hoàng Cao Sơn** | 25730061 | B | Imbalance Analysis + SMOTE/ADASYN + Random Forest | 5 |

---

## 🎯 Mô tả Bài toán

Phân loại giao dịch thẻ tín dụng thành **hợp lệ** hoặc **gian lận (bất thường)** dựa trên tập dữ liệu thực tế với đặc điểm mất cân bằng nghiêm trọng (tỷ lệ gian lận ~0.17%).

**Bài toán:** Binary Classification với Imbalanced Data  
**Dataset:** [Credit Card Fraud Detection — Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)  
**Kích thước:** 284,807 giao dịch, 31 features (V1–V28 PCA-transformed, Time, Amount, Class)

---

## 🛠️ Tech Stack

```
Python 3.10+
├── pandas, numpy          — Xử lý dữ liệu
├── scikit-learn           — Random Forest, preprocessing, metrics
├── xgboost / lightgbm     — Gradient Boosting models
├── imbalanced-learn       — SMOTE, ADASYN
├── tensorflow / keras     — Autoencoder (anomaly detection)
├── matplotlib, seaborn    — Visualization
├── shap                   — Model explainability (optional bonus)
└── jupyter / notebook     — Experiments & EDA
```

---

## 📂 Cấu trúc Dự án

```
fraud-detection/
├── data/
│   ├── raw/               # creditcard.csv (download từ Kaggle, không commit lên git)
│   └── processed/         # Dữ liệu đã qua preprocessing
├── notebooks/             # Jupyter notebooks cho EDA và thử nghiệm
│   ├── 01_eda.ipynb
│   ├── 02_imbalance_handling.ipynb
│   ├── 03_model_random_forest.ipynb
│   ├── 04_model_xgboost.ipynb
│   ├── 05_model_autoencoder.ipynb
│   └── 06_evaluation_comparison.ipynb
├── src/
│   ├── preprocessing/     # Scripts tiền xử lý dữ liệu
│   ├── models/            # Training scripts cho từng model
│   ├── evaluation/        # Metrics và đánh giá
│   └── utils/             # Các hàm tiện ích
├── reports/               # Báo cáo kết quả, biểu đồ
├── demo/                  # Demo UI
├── docs/                  # Tài liệu dự án
├── requirements.txt
└── README.md
```

---

## 🚀 Hướng dẫn Cài đặt

```bash
# 1. Clone repo (nếu dùng git riêng)
# 2. Tạo virtual environment
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate    # Windows

# 3. Cài dependencies
pip install -r requirements.txt

# 4. Tải dataset
# Truy cập https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
# Tải file creditcard.csv vào thư mục data/raw/
```

---

## 📊 Workflow

```
1. EDA → Phân tích phân phối, correlation, visualize imbalance
2. Preprocessing → Chuẩn hóa, train/test split (stratified)
3. Imbalance Handling → SMOTE / ADASYN trên tập train
4. Modeling → RF, XGBoost, Autoencoder
5. Evaluation → Precision, Recall, F1-Score, ROC-AUC
6. Comparison → Bảng so sánh hiệu năng các mô hình
```

---

## 📝 Báo cáo & Nộp bài

- **Word**: Scientific Report + Technical Report
- **PPT**: Trình bày kết quả tại buổi báo cáo
- **Code**: Toàn bộ notebook + src scripts
- **Demo**: Clip hoặc hình ảnh demo
- **Nộp theo tên**: `[Project AI-UIT] - Nhóm 9`
