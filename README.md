# Hệ Thống Phát Hiện Giao Dịch Tài Chính Bất Thường (Fraud Shield)

<p align="center">
  <img src="docs/cover.png" alt="Financial Fraud Detection Project Cover" width="100%" style="border-radius: 8px;" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat-square&logo=python" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/scikit--learn-1.3%2B-orange.svg?style=flat-square&logo=scikit-learn" alt="Scikit-Learn" />
  <img src="https://img.shields.io/badge/XGBoost-2.0%2B-red.svg?style=flat-square" alt="XGBoost" />
  <img src="https://img.shields.io/badge/Streamlit-1.36%2B-FF4B4B.svg?style=flat-square&logo=streamlit" alt="Streamlit" />
  <img src="https://img.shields.io/badge/Tests-110%20passed-brightgreen.svg?style=flat-square" alt="Tests" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License MIT" />
</p>

> **Đồ án cuối kỳ môn Trí tuệ Nhân tạo (CS106)**  
> **Trường Đại học Công nghệ Thông tin — ĐHQG-HCM (UIT)**  
> **Đề tài số 7:** Hệ thống phát hiện giao dịch tài chính bất thường  
> **Nhóm thực hiện:** Nhóm 09 (7 thành viên)

---

## 📌 Giới thiệu đề tài

Trong kỷ nguyên thanh toán kỹ thuật số, gian lận tài chính (Financial Fraud) gây thất thoát hàng tỷ USD mỗi năm và đe dọa sự ổn định của hệ thống ngân hàng. Bài toán đặt ra thách thức lớn về **mất cân bằng dữ liệu cực đoan** (tỷ lệ giao dịch gian lận trong thực tế chỉ chiếm ~0.13%) và yêu cầu phát hiện theo thời gian thực với độ chính xác cao nhằm hạn chế tối đa báo động giả (False Positives).

Dự án **Fraud Shield** xây dựng một pipeline phân tích và phát hiện giao dịch gian lận toàn diện từ dữ liệu mô phỏng [PaySim Mobile Money (Kaggle)](https://www.kaggle.com/datasets/ealaxi/paysim1), kết hợp giữa:
1. **Tiền xử lý & Kỹ nghệ đặc trưng:** Lọc miền nghiệp vụ (`TRANSFER`, `CASH_OUT`), xây dựng 7 đặc trưng tài chính mới (chênh lệch số dư trước/sau, tỷ lệ giao dịch).
2. **Cân bằng dữ liệu nâng cao:** Ứng dụng các thuật toán oversampling SMOTE-NC và ADASYN trên tập huấn luyện.
3. **Mô hình học máy đa phương pháp:** Đối sánh giữa học có giám sát (Random Forest, XGBoost) và học không giám sát (Deep Autoencoder Anomaly Detection).
4. **Ứng dụng thực tế (Streamlit Web Dashboard):** Giao diện tương tác trực quan cho phép thẩm định rủi ro giao dịch, đối sánh hiệu năng mô hình và giải thích quyết định dự đoán theo thời gian thực.

---

## 📊 Kết quả thực nghiệm chính

Đánh giá trên tập kiểm tra độc lập (40,000 giao dịch, giữ nguyên phân phối thực tế):

| Mô hình | Phương pháp cân bằng | Precision | Recall | F1-Score | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|
| **Random Forest** | **SMOTE-NC** | **0.9994** | **0.9951** | **0.9973** | **0.9994** | **0.9983** |
| Random Forest | ADASYN | 0.9982 | 0.9951 | 0.9966 | 0.9992 | 0.9978 |
| **XGBoost** | **SMOTE-NC** | 0.9976 | 0.9951 | 0.9963 | 0.9993 | 0.9969 |
| XGBoost | ADASYN | 0.9957 | 0.9951 | 0.9954 | 0.9994 | 0.9976 |
| **Autoencoder** | Unsupervised Reconstruction | 0.3822 | 0.7523 | 0.5069 | 0.9318 | 0.5973 |

> **Nhận xét chuyên sâu:**
> - **Random Forest kết hợp SMOTE-NC** đạt hiệu năng tổng thể vượt trội nhất (`F1 = 0.9973`, `Precision = 0.9994`), chỉ ghi nhận 1 trường hợp dương tính giả (False Positive) trên toàn bộ 40,000 giao dịch thử nghiệm.
> - Các đặc trưng tài chính tạo mới như `errorBalanceOrig` (sai lệch số dư tài khoản chuyển) và `errorBalanceDest` (sai lệch số dư tài khoản nhận) đóng góp hơn 65% độ quan trọng trong cây quyết định.
> - **Autoencoder** thể hiện ưu thế phát hiện bất thường mà không cần gán nhãn (`ROC-AUC = 0.9318`), phù hợp đóng vai trò bộ lọc tầng 1 (First-tier filter) trong kiến trúc giám sát đa tầng.

### 🔬 Thực nghiệm đối chứng (Ablation Study & Feature Pruning)

Nhằm tiếp thu phản biện học thuật từ hội đồng và khảo sát sự phụ thuộc vào các biến số dư của bộ dữ liệu PaySim, nhóm thiết kế 3 kịch bản thực nghiệm đối chứng trên mô hình XGBoost (SMOTE-NC, tập kiểm tra 40,000 mẫu):

| Kịch bản thực nghiệm | Số lượng đặc trưng | Recall | F1-Score | FP / 1 triệu GD | Đánh giá & Tác động thực tế |
|---|---|---|---|---|---|
| **Full_14 (Baseline)** | 14 đặc trưng | **0.9951** | **0.9945** | 261 | Mô hình nền tảng khai thác triệt để 8 đặc trưng số dư và 6 biến giao dịch |
| **Pruned_12 (Tối ưu hóa)** | 12 đặc trưng *(cắt bỏ `is_night`, `is_large`)* | **0.9951** | **0.9948** | **235** | Tinh gọn 14.3% số biến, giữ nguyên Recall, F1 tăng nhẹ, FP giảm còn 235 |
| **No_Balance_6 (Loại số dư)** | 6 đặc trưng thuần giao dịch | 0.7127 | 0.7116 | 12,436 | **F1 sụt giảm 28.3%**, số ca bỏ sót tăng từ 8 lên 472 ca (gấp 59 lần), FP tăng vọt 47 lần |

<p align="center">
  <img src="reports/figures/ablation_study_comparison.png" alt="Ablation Study Comparison" width="85%" style="border-radius: 6px;" />
</p>

> **Kết luận thực nghiệm:**
> 1. Đặc trưng số dư (`errorBalanceOrig`, `errorBalanceDest`) mang tính sống còn đối với bài toán nhận diện gian lận trên dữ liệu PaySim do cơ chế gian lận rửa tiền luôn tìm cách rút cạn tài khoản (`oldbalanceOrg == amount`).
> 2. Kịch bản **Pruned_12** chứng minh việc loại bỏ 2 đặc trưng nhiễu/ít phân hóa giúp mô hình tối ưu hơn về chi phí tính toán khi triển khai thực tế mà không làm suy giảm hiệu năng nhận diện.

---

## 🏗️ Kiến trúc hệ thống

Quy trình xử lý dữ liệu và suy luận của hệ thống:

```
[Dữ liệu gốc PaySim] (6.36M mẫu)
         │
         ▼
[1. Preprocessing & Filtering]
  ├── Lọc giao dịch nguy cơ cao: TRANSFER & CASH_OUT
  ├── Phân tầng Stratified Downsampling (~200,000 mẫu)
  └── Trích xuất 7 đặc trưng tài chính (errorBalance, ratios)
         │
         ▼
[2. Imbalance Handling & Scaling]
  ├── Chuẩn hóa StandardScaler
  └── Xử lý mất cân bằng: SMOTE-NC / ADASYN (chỉ áp dụng trên Train)
         │
         ├───► [Supervised] Random Forest & XGBoost ──► [Inference Engine]
         │                                                      │
         └───► [Unsupervised] Deep Autoencoder (Recon Error) ───┤
                                                                ▼
                                                   [Streamlit Web Dashboard]
                                                     - Thẩm định đơn lẻ
                                                     - Batch CSV / JSON
                                                     - Đối sánh & Giải thích
```

Chi tiết kiến trúc và chuẩn thiết kế: xem tại [docs/system-architecture.md](docs/system-architecture.md) và [docs/code-standards.md](docs/code-standards.md).

---

## 📁 Cấu trúc thư mục

```text
CS106-Team09-Fraud-Detection/
├── docs/                                           ← Tài liệu đề bài, kiến trúc & lộ trình
│   ├── cover.png                                   ← Banner đồ án
│   ├── 2026, De tai mon TTNT 2 - He tu xa.pdf      ← Đề bài chính thức từ GV
│   ├── system-architecture.md                      ← Thiết kế kiến trúc hệ thống
│   ├── code-standards.md                           ← Quy chuẩn code & tái hiện
│   ├── project-roadmap.md                          ← Phân công & lộ trình nhóm
│   └── project-overview-pdr.md                     ← Tổng quan dự án & nghiên cứu
├── src/                                            ← Mã nguồn Python modular hóa
│   ├── preprocessing/                              ← Đọc, lọc, chia tập, chuẩn hóa & oversampling
│   │   ├── data_loader.py
│   │   ├── data_splitter.py
│   │   ├── feature_scaler.py
│   │   └── imbalance_handler.py
│   ├── models/                                     ← Định nghĩa & huấn luyện mô hình
│   │   ├── random_forest_model.py
│   │   ├── xgboost_model.py
│   │   └── autoencoder_model.py
│   ├── evaluation/                                 ← Đánh giá chỉ số, ROC/PR curves, ma trận nhầm lẫn
│   │   ├── metrics_calculator.py
│   │   ├── model_comparator.py
│   │   ├── confusion_matrix_plot.py
│   │   ├── plot_roc_curve.py
│   │   ├── plot_feature_importance.py
│   │   └── prevalence_projection.py
│   └── utils/                                      ← Cấu hình đường dẫn & hàm bổ trợ
│       └── helpers.py
├── notebooks/                                      ← 6 Jupyter Notebooks thực nghiệm sạch 100%
│   ├── 01_eda.ipynb                                ← Khám phá & phân tích dữ liệu PaySim
│   ├── 02_imbalance_handling.ipynb                 ← Thực nghiệm SMOTE-NC & ADASYN
│   ├── 03_model_random_forest.ipynb                ← Huấn luyện & tối ưu Random Forest
│   ├── 04_model_xgboost.ipynb                      ← Huấn luyện & tối ưu XGBoost
│   ├── 05_model_autoencoder.ipynb                  ← Xây dựng mạng Deep Autoencoder
│   └── 06_evaluation_comparison.ipynb              ← Đánh giá đối sánh toàn diện các mô hình
├── data/
│   ├── raw/                                        ← Thư mục chứa dữ liệu thô (paysim.csv)
│   └── processed/                                  ← Dữ liệu đã tiền xử lý (.pkl)
│       └── README.md                               ← Hướng dẫn sử dụng tập dữ liệu processed
├── models/                                         ← Model checkpoints & scaler đã huấn luyện
│   ├── scaler.pkl                                  ← Scaler chuẩn hóa đã fit
│   ├── xgb_smote.json                              ← Model XGBoost (SMOTE-NC)
│   ├── xgb_adasyn.json                             ← Model XGBoost (ADASYN)
│   └── autoencoder_meta.json                       ← Trọng số & ngưỡng Autoencoder
├── reports/                                        ← Minh chứng thực nghiệm & đối sánh mô hình
│   ├── figures/                                    ← Biểu đồ ROC, PR, ma trận nhầm lẫn, Ablation Study
│   ├── model_comparison.csv                        ← Bảng số liệu tổng hợp đối sánh
│   ├── ablation_study_results.csv                  ← Bảng dữ liệu thực nghiệm Ablation Study
│   └── *.pkl, *.csv, *.txt                         ← Tập predictions & báo cáo chi tiết
├── demo/                                           ← Ứng dụng Web Streamlit Fraud Shield
│   ├── app.py                                      ← Điểm khởi chạy giao diện
│   ├── inference.py                                ← Module kết nối suy luận thời gian thực
│   ├── analysis_pipeline.py                        ← Quy trình phân tích giao dịch 4 bước
│   ├── history_store.py                            ← Quản lý lịch sử kiểm tra
│   ├── screenshots/                                ← Bộ 6 ảnh chụp giao diện (Fraud, Legitimate, Warning)
│   └── requirements-demo.txt                       ← Thư viện tối giản cho Demo
├── slide/                                          ← Slide thuyết trình học thuật
│   ├── [Nhom9]_Slide_FraudDetection.pdf            ← Slide PDF chính thức (21 trang)
│   └── slide_assets/                               ← Đồ họa & hình ảnh phục vụ slide
├── scripts/                                        ← Scripts chạy thực nghiệm độc lập
│   ├── run_ablation_study.py                       ← Khảo sát 3 kịch bản thực nghiệm đối chứng
│   └── plot_ablation_study.py                      ← Xuất biểu đồ phân tích Ablation Study
├── tests/                                          ← Bộ kiểm thử tự động (110 unit & integration tests)
│   ├── demo/                                       ← Kiểm thử giao diện & suy luận Streamlit
│   └── evaluation/                                 ← Kiểm thử bộ tính toán chỉ số & biểu đồ
├── requirements.txt                                ← Danh sách thư viện phụ thuộc toàn dự án
├── pytest.ini                                      ← Cấu hình Pytest
├── run_preprocessing.py                            ← Script tái lập toàn bộ dữ liệu processed
└── LICENSE                                         ← Giấy phép mã nguồn mở MIT
```

---

## 🚀 Hướng dẫn cài đặt & Thực thi

### 1. Khởi tạo môi trường

Yêu cầu: Python phiên bản 3.10 đến 3.12 (khuyến nghị Python 3.11 hoặc 3.12).

```bash
# Clone repository
git clone https://github.com/uit-25730067-chithanh/CS106-Team09-Fraud-Detection.git
cd CS106-Team09-Fraud-Detection

# Tạo và kích hoạt môi trường ảo
python3 -m venv .venv
source .venv/bin/activate        # Trên Linux/macOS
# .venv\Scripts\activate         # Trên Windows

# Cài đặt các thư viện cần thiết
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Chạy ứng dụng Demo (Streamlit)

Ứng dụng Web đã tích hợp sẵn scaler và mô hình nhẹ trong `models/`, có thể khởi chạy ngay lập tức:

```bash
streamlit run demo/app.py
```

Truy cập trình duyệt tại địa chỉ mặc định: `http://localhost:8501`.

Các tính năng nổi bật của ứng dụng:
- **Kiểm tra giao dịch đơn lẻ:** Nhập thông số số dư, số tiền, loại giao dịch để nhận diện gian lận tức thì kèm giải thích chỉ số rủi ro.
- **Tải lên hàng loạt (Batch):** Hỗ trợ nạp file CSV hoặc JSON mẫu để phân tích danh sách giao dịch.
- **Trung tâm đối sánh mô hình:** Xem trực quan ma trận nhầm lẫn, đường cong ROC và mức độ quan trọng của đặc trưng.

### 3. Thực thi chuỗi Jupyter Notebooks

Các notebook được đánh số theo thứ tự luồng xử lý và có thể chạy độc lập nhờ dữ liệu đã tiền xử lý sẵn trong `data/processed/`:

1. `notebooks/01_eda.ipynb`: Phân tích thống kê mô tả, phân phối lệch và tương quan thuộc tính.
2. `notebooks/02_imbalance_handling.ipynb`: Thử nghiệm cân bằng dữ liệu bằng SMOTE-NC và ADASYN.
3. `notebooks/03_model_random_forest.ipynb`: Huấn luyện bộ phân loại Random Forest.
4. `notebooks/04_model_xgboost.ipynb`: Tinh chỉnh siêu tham số và huấn luyện XGBoost.
5. `notebooks/05_model_autoencoder.ipynb`: Xây dựng mô hình dò bất thường bằng Autoencoder.
6. `notebooks/06_evaluation_comparison.ipynb`: Đối chiếu ma trận nhầm lẫn, ROC-AUC, PR-AUC giữa các giải thuật.

### 4. Chạy bộ kiểm thử tự động (Unit Tests)

Dự án duy trì 110 automated tests bao phủ từ module tiền xử lý, tính toán chỉ số đến luồng suy luận của demo:

```bash
pytest
```

Kết quả mong đợi: `110 passed`.

---

## 📄 Ấn phẩm học thuật

- **Báo cáo toàn văn (PDF 31 trang):** Đã nộp chính thức trên hệ thống UIT Moodle LMS theo quy chế môn học (Nhóm bảo lưu quyền tác giả và phòng chống sao chép học thuật; vui lòng liên hệ nhóm nếu cần tham khảo nghiên cứu).
- **Slide thuyết trình (PDF 21 trang):** [slide/[Nhom9]_Slide_FraudDetection.pdf](slide/[Nhom9]_Slide_FraudDetection.pdf)
- **Video Clip Demo (Full HD):** Đã tích hợp tại Slide 15 và truy cập trực tiếp tại [Video Demo Fraud Shield](https://aceteam-uit.vercel.app/l/70vGyu).

---

## 👥 Thành viên nhóm 09

| Họ và tên | MSSV | Lớp | Trách nhiệm chính trong đồ án |
|---|---|---|---|
| **Trần Hoàng Hôn** *(Trưởng nhóm)* | 22520468 | KTPM2022 | Quản lý tiến độ (PM), biên soạn Slide thuyết trình, điều phối diễn tập & nộp bài |
| **Đặng Chí Thanh** | 25730067 | HTTT2025.2 | Phân tích khám phá (EDA), xây dựng pipeline tiền xử lý dữ liệu & kỹ nghệ đặc trưng |
| **Hoàng Cao Sơn** | 22521252 | KHCL2022.1 | Phân tích mất cân bằng dữ liệu, thực nghiệm SMOTE-NC / ADASYN, mô hình Random Forest |
| **Bùi Thị Mỷ Cẩm** | 22520145 | KTPM2022 | Xây dựng và huấn luyện mô hình XGBoost, mô hình Deep Autoencoder |
| **Nguyễn Duy Khang** | 22520630 | HTTT2022 | Viết module đánh giá, đo lường chỉ số (F1, ROC-AUC, PR-AUC) & tổng hợp đối sánh |
| **Vũ Văn Duy** | 22520330 | KTPM2022 | Soạn thảo và chuẩn hóa báo cáo học thuật toàn văn (Chương 1 đến 7) |
| **Phạm Thành Trung** | 22521558 | KTPM2022 | Thiết kế & lập trình Web App Streamlit, tích hợp mô hình suy luận & quay video demo |

---

## 📜 Giấy phép (License)

Dự án được phân phối dưới giấy phép nguồn mở **MIT License**. Xem chi tiết tại [LICENSE](LICENSE).
Nghiên cứu được thực hiện vì mục đích học thuật tại Trường Đại học Công nghệ Thông tin — ĐHQG-HCM.
