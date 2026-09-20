# HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG CHƯƠNG TRÌNH
## ĐỒ ÁN MÔN HỌC: TRÍ TUỆ NHÂN TẠO (CS106) — UIT ĐHQG-HCM

> **Đề tài #7:** Hệ thống phát hiện giao dịch tài chính bất thường và nghi vấn gian lận (Financial Fraud Detection)  
> **Nhóm thực hiện:** Nhóm 09 (7 thành viên)  
> **GitHub Repository:** [https://github.com/uit-25730067-chithanh/CS106-Team09-Fraud-Detection](https://github.com/uit-25730067-chithanh/CS106-Team09-Fraud-Detection)

---

## 1. Yêu cầu Môi trường & Cài đặt

Chương trình được phát triển và kiểm thử ổn định trên hệ điều hành Windows / Linux / macOS với **Python 3.10 trở lên** (khuyến nghị Python 3.10 – 3.11).

### Bước 1: Tạo và kích hoạt môi trường ảo (Khuyến nghị)
```bash
# Tạo virtual environment
python -m venv .venv

# Kích hoạt trên Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Hoặc kích hoạt trên Linux / macOS
source .venv/bin/activate
```

### Bước 2: Cài đặt các thư viện phụ thuộc
Từ thư mục mã nguồn chứa file `requirements.txt`:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

*(Lưu ý: Nếu máy tính đã có sẵn các thư viện khoa học dữ liệu như `pandas`, `scikit-learn`, `xgboost`, `streamlit`, `openpyxl`, `matplotlib`, `seaborn` thì có thể chạy trực tiếp mà không cần cài đặt lại).*

---

## 2. Cấu trúc Mã nguồn & Hoạt động các Module

Toàn bộ mã nguồn được thiết kế theo kiến trúc module hóa hướng đối tượng (OOP & Functional Pipeline), tuân thủ nguyên tắc **chống rò rỉ dữ liệu (Anti-leakage)**:

```
Code/
├── src/
│   ├── preprocessing/     # Tiền xử lý & Trích xuất đặc trưng
│   │   ├── data_loader.py         # Lọc tập TRANSFER/CASH_OUT, lấy mẫu phân tầng 200k
│   │   ├── data_splitter.py       # Chia tập Train/Test (80/20) Stratified
│   │   ├── feature_scaler.py      # Tạo 14 đặc trưng (5 derived features) + StandardScaler
│   │   └── imbalance_handler.py   # Xử lý mất cân bằng: SMOTENC & ADASYN (chỉ trên Train)
│   ├── models/            # 3 họ mô hình phân loại & phát hiện bất thường
│   │   ├── random_forest_model.py # Random Forest + RandomizedSearchCV
│   │   ├── xgboost_model.py       # Gradient Boosting (XGBoost) siêu tốc + native JSON
│   │   └── autoencoder_model.py   # Deep Learning Autoencoder (Anomaly Detection không giám sát)
│   ├── evaluation/        # Đánh giá & So sánh chéo
│   │   ├── metrics_calculator.py  # Tính F1, ROC-AUC, PR-AUC, Precision, Recall
│   │   ├── plot_roc_curve.py      # Trực quan hóa ROC Curves & PR Curves
│   │   ├── confusion_matrix_plot.py# Vẽ ma trận nhầm lẫn chuẩn hóa
│   │   └── model_comparator.py    # Bảng tổng hợp so sánh chéo 5 biến thể mô hình
│   └── utils/             # Hằng số, helper functions, cố định Random Seed (42)
├── notebooks/             # 6 Notebooks thực nghiệm trực quan (từ EDA đến So sánh)
├── demo/                  # Giao diện tương tác Streamlit Web UI (app.py)
├── models/                # Artifacts mô hình (scaler.pkl, xgb_smote.json, autoencoder_meta.json)
└── data/
    └── processed/         # Dữ liệu đã chia tập (X_train, X_test, y_train, y_test)
```

---

## 3. Hướng dẫn Chạy Thử nghiệm

### Cách 1: Khởi chạy Giao diện Trực quan Streamlit Web UI (Khuyến nghị)
Nhóm đã phát triển giao diện Web hoàn chỉnh cho phép nhập thông tin giao dịch, kiểm tra rủi ro gian lận thời gian thực với mô hình XGBoost-SMOTE:

```bash
# Chạy ứng dụng Demo
streamlit run demo/app.py
```
* Trình duyệt sẽ tự động mở tại địa chỉ: `http://localhost:8501`.
* **Tính năng trên giao diện:**
  1. **Phân tích giao dịch:** Hỗ trợ nhập số tiền (tự động phân cách hàng nghìn VNĐ), số dư gốc/đích, loại giao dịch; cung cấp các nút chọn sẵn mẫu giao dịch thực tế.
  2. **Risk Meter & Cảnh báo:** Đo lường mức độ rủi ro gian lận trực quan (Thấp / Trung bình / Cao / Nghi vấn gian lận).
  3. **Hiệu năng mô hình:** Xem bảng số liệu so sánh chéo 5 mô hình, đường cong ROC/PR Curves và ma trận nhầm lẫn.
  4. **Chuyển đổi Giao diện:** Hỗ trợ Theme Tối (Dark mode), Theme Sáng (Light mode) và Tự động theo hệ thống.

---

### Cách 2: Chạy các Notebooks Thực nghiệm Jupyter
Thầy/cô và các bạn có thể mở và chạy lại 6 Notebooks trong thư mục `notebooks/` theo thứ tự:
1. `01_eda.ipynb`: Thăm dò phân phối dữ liệu, hành vi gian lận và tương quan đặc trưng.
2. `02_imbalance_handling.ipynb`: Thử nghiệm kỹ thuật SMOTENC và ADASYN trên tập huấn luyện.
3. `03_model_random_forest.ipynb`: Huấn luyện, dò siêu tham số và phân tích Feature Importance của Random Forest.
4. `04_model_xgboost.ipynb`: Huấn luyện mô hình XGBoost trên SMOTE và ADASYN (đạt F1 = 0.9963).
5. `05_model_autoencoder.ipynb`: Huấn luyện mô hình Autoencoder phát hiện bất thường không cần nhãn.
6. `06_evaluation_comparison.ipynb`: Tổng hợp, đánh giá chéo toàn diện và xuất các biểu đồ so sánh.

*(Tất cả 6 notebooks đều đã được chạy sạch (Clean Run), lưu sẵn toàn bộ biểu đồ và kết quả đầu ra).*

---

### Cách 3: Chạy Kiểm thử Tự động (Unit Tests)
Dự án được bảo vệ bằng hệ thống 116 bài test tự động (đạt tỷ lệ vượt qua 100%):
```bash
pytest tests/
```

---

## 4. Tóm tắt Kết quả Thực nghiệm Chính

| Thứ hạng | Mô hình thực nghiệm | Kỹ thuật cân bằng | F1-Score | ROC-AUC | PR-AUC | Thời gian train |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 🥇 1 | **Random Forest** | SMOTENC | **0.9973** | **0.9994** | **0.9981** | ~180s |
| 🥈 2 | **Random Forest** | ADASYN | 0.9966 | 0.9992 | 0.9974 | ~195s |
| 🥉 3 | **XGBoost (Được chọn triển khai UI)** | SMOTENC | **0.9963** | **0.9993** | **0.9978** | **41.6s** |
| 4 | **XGBoost** | ADASYN | 0.9954 | 0.9994 | 0.9975 | 45.2s |
| 5 | **Autoencoder (Anomaly Detection)**| Normal Only | 0.5074 | 0.9318 | 0.4421 | ~90s |

> **Lý do chọn XGBoost-SMOTE cho Demo UI:** Hiệu năng xấp xỉ Random Forest (F1 đạt 0.9963 so với 0.9973) nhưng thời gian huấn luyện nhanh hơn gấp 4.3 lần và kích thước file mô hình cực nhẹ (chỉ 410 KB dạng JSON Native so với 50MB+ của Random Forest).
