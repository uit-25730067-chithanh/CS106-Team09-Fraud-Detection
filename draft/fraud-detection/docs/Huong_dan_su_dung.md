# HƯỚNG DẪN CÀI ĐẶT VÀ SỬ DỤNG CHƯƠNG TRÌNH
## ĐỒ ÁN MÔN HỌC: TRÍ TUỆ NHÂN TẠO (CS106) — UIT ĐHQG-HCM

> **Đề tài #7:** Hệ thống phát hiện giao dịch tài chính bất thường và nghi vấn gian lận (Financial Fraud Detection)  
> **Nhóm thực hiện:** Nhóm 09 (7 thành viên)  
> **GitHub Repository:** [https://github.com/uit-25730067-chithanh/CS106-Team09-Fraud-Detection](https://github.com/uit-25730067-chithanh/CS106-Team09-Fraud-Detection)

---

## 1. Yêu cầu Môi trường & Cài đặt

Chương trình được phát triển và kiểm thử ổn định trên hệ điều hành Windows / Linux / macOS với **Python 3.10 trở lên** (khuyến nghị Python 3.10 – 3.12).

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

*(Lưu ý: Nếu máy tính đã có sẵn các thư viện khoa học dữ liệu như `pandas`, `scikit-learn`, `xgboost`, `imbalanced-learn`, `openpyxl`, `matplotlib`, `seaborn` thì có thể chạy trực tiếp mà không cần cài đặt lại).*

---

## 2. Cấu trúc Mã nguồn & Hoạt động các Module

Toàn bộ mã nguồn thực nghiệm được thiết kế theo kiến trúc module hóa hướng đối tượng (OOP & Functional Pipeline), tuân thủ nguyên tắc **chống rò rỉ dữ liệu (Anti-leakage)**:

```text
Chuong_trinh/
├── HUONG_DAN_SU_DUNG.docx              # Bản Word hướng dẫn sử dụng chính thức
├── HUONG_DAN_SU_DUNG.md                # Bản Markdown đối soát nhanh
├── requirements.txt                    # Danh sách thư viện Python phụ thuộc
├── demo/                               # Minh chứng sản phẩm Demo
│   ├── LINK_VIDEO_DEMO.txt             # Liên kết video clip demo Google Drive (quyền xem công khai)
│   └── screenshots/                    # 5 ảnh chụp màn hình giao diện UI trực quan
└── code/                               # Toàn bộ mã nguồn giải thuật & thực nghiệm
    ├── src/                            # 4 modules Python modular
    │   ├── preprocessing/              # data_loader, feature_scaler, data_splitter, imbalance_handler
    │   ├── models/                     # random_forest_model, xgboost_model, autoencoder_model
    │   ├── evaluation/                 # metrics_calculator, plot_roc_curve, confusion_matrix_plot, model_comparator...
    │   └── utils/                      # helpers.py, constants, compatibility
    ├── notebooks/                      # 6/6 Jupyter Notebooks thực nghiệm chạy sạch 100%
    ├── data/processed/                 # Dữ liệu tiền xử lý (X_train, X_test, y_train, y_test, SMOTE/ADASYN)
    └── reports/                        # Prediction caches đầu vào đối sánh (rf, xgb, autoencoder)
```

*(Lưu ý: Ứng dụng tương tác Web UI Streamlit và bộ 102 bài kiểm thử tự động được quản lý đầy đủ tại GitHub Repository chính thức của đồ án).*

---

## 3. Hướng dẫn Chạy Thử nghiệm

### 3.1. Chạy các Notebooks Thực nghiệm Jupyter (Phương thức thẩm định chính)
Thầy/cô và các bạn có thể mở và chạy lại 6 Notebooks trong thư mục `code/notebooks/` theo thứ tự:
1. `01_eda.ipynb`: Thăm dò phân phối dữ liệu, hành vi gian lận và tương quan đặc trưng.
2. `02_imbalance_handling.ipynb`: Thử nghiệm kỹ thuật SMOTENC và ADASYN trên tập huấn luyện.
3. `03_model_random_forest.ipynb`: Huấn luyện, dò siêu tham số và phân tích Feature Importance của Random Forest.
4. `04_model_xgboost.ipynb`: Huấn luyện mô hình XGBoost trên SMOTE và ADASYN (đạt F1 = 0.9963).
5. `05_model_autoencoder.ipynb`: Huấn luyện mô hình Autoencoder phát hiện bất thường không cần nhãn.
6. `06_evaluation_comparison.ipynb`: Tổng hợp, đánh giá chéo toàn diện và xuất các biểu đồ so sánh.

*(Tất cả 6 notebooks đều đã được chạy sạch (Clean Run), lưu sẵn toàn bộ biểu đồ và kết quả đầu ra).*

---

### 3.2. Xem Minh chứng Video Clip Thuyết minh Demo Giao diện
Thầy/cô có thể xem video thuyết minh giao diện tương tác (Streamlit Web UI) độ phân giải Full HD 1080p, thời lượng 05 phút 34 giây do sinh viên Phạm Thành Trung trình bày:
- **Xem trực tiếp qua liên kết Google Drive:** Mở tệp `demo/LINK_VIDEO_DEMO.txt` hoặc truy cập trực tiếp:  
  [https://drive.google.com/file/d/1QkrP-Zl4LXTgB13U0lQkLU9hB72qkZGL/view](https://drive.google.com/file/d/1QkrP-Zl4LXTgB13U0lQkLU9hB72qkZGL/view)
- **Xem qua Slide trình chiếu:** Slide 15 trong tệp `Bao_cao/[Nhom9]_Slide_FraudDetection_Academic_VN.pptx`.
- **Xem hình ảnh giao diện:** 5 ảnh chụp màn hình độ phân giải cao tại thư mục `demo/screenshots/`.

---

### 3.3. Trải nghiệm Demo Trực tiếp & Chạy Unit Tests trên GitHub Repository
Để tương tác với giao diện Web thời gian thực hoặc chạy toàn bộ **102 bài test tự động (`pytest`)**, kính mời Quý Thầy/Cô truy cập kho mã nguồn chính thức:
```bash
# Clone repository chính thức
git clone https://github.com/uit-25730067-chithanh/CS106-Team09-Fraud-Detection.git
cd CS106-Team09-Fraud-Detection/draft/fraud-detection

# Cài đặt và khởi chạy Streamlit Web UI
pip install -r requirements.txt
streamlit run demo/app.py

# Chạy kiểm thử tự động toàn diện (102 tests pass sạch)
pytest tests/
```

---

## 4. Tóm tắt Kết quả Thực nghiệm Chính

Bảng số liệu đối sánh thực nghiệm chính thức (trích từ Bảng 5 Báo cáo học thuật và `ch5_metrics_recomputed.csv`):

| Thứ hạng | Mô hình thực nghiệm | Kỹ thuật cân bằng | Precision | Recall | F1-Score | ROC-AUC | PR-AUC | Thời gian train |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| 🥇 1 | **Random Forest** | SMOTENC | **0.9994** | **0.9951** | **0.9973** | **0.9994** | **0.9983** | 1187s (~19.8m) |
| 🥈 2 | **Random Forest** | ADASYN | 0.9982 | 0.9951 | 0.9966 | 0.9992 | 0.9978 | 1168s (~19.5m) |
| 🥉 3 | **XGBoost (Được chọn triển khai UI)** | SMOTENC | **0.9976** | **0.9951** | **0.9963** | **0.9993** | **0.9969** | **57.94s** |
| 4 | **XGBoost** | ADASYN | 0.9957 | 0.9951 | 0.9954 | 0.9994 | 0.9976 | 45.48s |
| 5 | **Autoencoder (Anomaly Detection)**| Normal Only | 0.3822 | 0.7523 | 0.5069 | 0.9318 | 0.5973 | ~90s |

> **Lý do chọn XGBoost-SMOTE cho Demo UI:** Hiệu năng xấp xỉ Random Forest (F1 đạt 0.9963 so với 0.9973) nhưng thời gian huấn luyện nhanh hơn gấp 20.5 lần (57.94s so với 1187s) và kích thước file mô hình cực nhẹ (chỉ 495 KB dạng JSON Native so với 50MB+ của Random Forest).
