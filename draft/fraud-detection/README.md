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

Phân loại giao dịch tài chính di động thành **hợp lệ** hoặc **gian lận (bất thường)** dựa trên tập dữ liệu mô phỏng thực tế với đặc điểm mất cân bằng nghiêm trọng (tỷ lệ gian lận ~0.13%).

**Bài toán:** Binary Classification với Imbalanced Data  
**Dataset:** [PaySim Mobile Money Fraud Detection — Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1)  
**Kích thước:** 6,362,620 giao dịch (sẽ được downsample còn ~200,000 giao dịch), 11 features (step, type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest, isFraud, etc.)

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
│   ├── raw/               # paysim.csv (tải từ Kaggle, KHÔNG commit git — ~500MB)
│   └── processed/         # ✅ Dữ liệu đã xử lý — X_train/X_test/y_train/y_test.pkl
│                          #    → Đã có trong git, chỉ cần git pull
│                          #    → Xem: data/processed/README.md
├── models/                # scaler.pkl, xgb_smote.json, autoencoder_threshold.txt
├── notebooks/             # Jupyter notebooks cho EDA và thử nghiệm
│   ├── 01_eda.ipynb       ✔ Hoàn thành (EDA & Feature Distributions)
│   ├── 02_imbalance_handling.ipynb
│   ├── 03_model_random_forest.ipynb
│   ├── 04_model_xgboost.ipynb ✔ Hoàn thành (XGBoost SMOTE/ADASYN)
│   ├── 05_model_autoencoder.ipynb ✔ Hoàn thành (Autoencoder Anomaly Detection)
│   └── 06_evaluation_comparison.ipynb
├── src/
│   ├── preprocessing/     ✔ data_loader, feature_scaler, data_splitter, imbalance_handler
│   ├── models/            ✔ random_forest_model.py, xgboost_model.py, autoencoder_model.py
│   ├── evaluation/        ⏳ Metrics và đánh giá (metrics_calculator, plot_roc_curve)
│   └── utils/             ✔ helpers.py, constants, set_seeds()
├── reports/               # ✅ Báo cáo nháp Docx/PDF + Slide PPT + Predictions (RF, XGB, Autoencoder)
├── demo/                  # ✅ Signal Universe Streamlit UI shell (Phase 06 checkpoint)
│   ├── app.py            # Quick presets + signal/flow/error views + native motion
│   ├── assets/           # Custom crystal logo + hero asset của revision cũ
│   ├── screenshots/      # Revision 5 rendered QA evidence
│   ├── WIREFRAME.md      # Bố cục và nguyên tắc giao diện
│   └── requirements-demo.txt
├── docs/                  # Tài liệu dự án
├── run_preprocessing.py   # Script chạy lại pipeline tiền xử lý (Phase 01)
├── run_imbalance_handling.py # Script chạy SMOTENC & ADASYN (Phase 02)
├── run_random_forest.py   # Script train & evaluate Random Forest (Phase 03)
├── run_xgboost.py         # Script train & evaluate XGBoost (Phase 04)
├── run_autoencoder.py     # Script train & evaluate Autoencoder (Phase 04)
├── requirements.txt
└── README.md
```

---

## 🚀 Hướng dẫn Cài đặt

```bash
# Bước 1. Clone repo (nếu dùng git riêng)
git clone <url-repo>
cd draft/fraud-detection

# Bước 2. Tạo môi trường ảo Python (bắt buộc!)
python -m venv .venv

# Kích hoạt môi trường ảo:
source .venv/bin/activate      # macOS / Linux
# hoặc trên Windows:
# .venv\Scripts\activate        # Windows (Command Prompt)
# .venv\Scripts\Activate.ps1    # Windows (PowerShell)

# Kiểm tra đã kích hoạt chưa: terminal sẽ hiện (.venv) ở đầu dòng

# Bước 3. Cài các thư viện cần thiết
pip install -r requirements.txt

# Bước 4. (Chỉ khi cần tạo lại dữ liệu) Tải dataset
# Truy cập https://www.kaggle.com/datasets/ealaxi/paysim1
# Tải file csv (đổi tên thành paysim.csv), đặt vào: data/raw/paysim.csv

# Bước 5. (Tùy chọn) Chạy lại preprocessing nếu muốn tạo lại .pkl từ đầu
# ✔ Bước này KHÔNG cần thiết nếu đã git pull — file .pkl đã có trong git!
python run_preprocessing.py
```

> ⚠️ **Lưu ý cho người chưa dùng terminal bao giờ:** Chỉ cần `git pull` là có đủ file dữ liệu rồi. Không cần chạy preprocessing. Môi trường ảo chỉ cần khi muốn chạy notebook hoặc script.

### Chạy Demo UI

```bash
pip install -r demo/requirements-demo.txt
streamlit run demo/app.py
```

UI shell Revision 7.7 gồm form PaySim, 3 quick presets, Bản đồ tín hiệu/Dòng tiền/Sai lệch số dư và chế độ System/Sáng/Tối. Các visual hiện chỉ mô tả dữ liệu đầu vào; ứng dụng không hiển thị nhãn hoặc xác suất gian lận cho đến khi model thật từ Phase 04–05 được bàn giao.

**Trạng thái:** UI shell đã được xác minh ở cấp code, AppTest và local runtime. Phase 06 vẫn `pending`; còn browser/pixel QA, tích hợp model/figures thật, screenshot và demo clip. Xem evidence tại [phase-06-demo-ui.md](../../plans/fraud-detection-full-submit/phase-06-demo-ui.md).

---

## 📊 Workflow

```
1. EDA            ✔ Phân tích phân phối, correlation, visualize imbalance (Thanh)
2. Preprocessing  ✔ Feature Engineering (14 features), chuẩn hóa, train/test split (Thanh)
3. Imbalance      ✔ SMOTENC & ADASYN trên tập train (Phase 02 — Sơn)
4. Modeling       ✔ Random Forest (Sơn) | XGBoost & Autoencoder (Cẩm) — ALL 3 MODELS DONE
5. Evaluation     ⏳ 2/4 scripts done (PR #7); còn confusion_matrix_plot + model_comparator (Khang)
6. Comparison     ⏳ Chưa chạy; cần tạo reports/figures/ + model_comparison.csv
7. Demo UI        ✔ UI shell Rev 7.7 + 3 presets + safe-preview; → Chờ nạp model weights (Trung)
8. Report         ✔ Nháp Báo cáo Word Ch.1-3 (Duy) + Slide PPT 15 slides (Hôn) + Slide học thuật 24 trang
```

> ⚠️ **PM Audit (04/09):** Thiếu 3 notebooks: `02_imbalance_handling`, `03_model_random_forest`, `06_evaluation_comparison` — cần cho submit package.

> 📄 Dữ liệu đầu ra từ bước 2 đã được commit trong git. Xem chi tiết: [data/processed/README.md](./data/processed/README.md)

---

## 📝 Báo cáo & Nộp bài

- **Word**: Scientific Report + Technical Report
- **PPT**: Trình bày kết quả tại buổi báo cáo
- **Code**: Toàn bộ notebook + src scripts
- **Demo**: Clip hoặc hình ảnh demo
- **Nộp theo tên**: `[Project AI-UIT] - Nhóm 9`
