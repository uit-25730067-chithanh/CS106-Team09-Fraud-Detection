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
│   ├── 02_imbalance_handling.ipynb ✔ Hoàn thành (SMOTENC & ADASYN)
│   ├── 03_model_random_forest.ipynb ✔ Hoàn thành (Random Forest & Tuning)
│   ├── 04_model_xgboost.ipynb ✔ Hoàn thành (XGBoost SMOTE/ADASYN)
│   ├── 05_model_autoencoder.ipynb ✔ Hoàn thành (Autoencoder Anomaly Detection)
│   └── 06_evaluation_comparison.ipynb ✔ Hoàn thành (Model Comparison & Evaluation)
├── src/
│   ├── preprocessing/     ✔ data_loader, feature_scaler, data_splitter, imbalance_handler
│   ├── models/            ✔ random_forest_model.py, xgboost_model.py, autoencoder_model.py
│   ├── evaluation/        ✔ metrics_calculator, plot_roc_curve, confusion_matrix_plot, model_comparator (4/4 scripts)
│   └── utils/             ✔ helpers.py, constants, set_seeds()
├── reports/               # ✅ Báo cáo Chương 1–7 DOCX/PDF + Predictions (RF, XGB, Autoencoder)
│   ├── model_comparison.csv        # Bảng so sánh 5 biến thể chính thức (Phase 05 output)
│   ├── ch5_metrics_recomputed.csv  # Chỉ số Chương 5 tái lập (khớp 100% model_comparison.csv)
│   ├── ch6_prevalence_projection.csv # Precision quy chiếu về tỷ lệ gian lận gốc (Bảng 6.1)
│   ├── _report_template.docx       # Khuôn định dạng (styles, header, footer, A4) cho build_report.py
│   ├── _toc_pages.json             # Số trang mục lục do sync_toc_pages.py sinh ra
│   └── figures/           # Hình dùng trong báo cáo (Hình 5.1 confusion_matrix_components.png, Hình 5.2 feature_importance_comparison.png, 7 ROC/PR/Confusion plots)
├── slide/                 # ✅ Bộ Slide học thuật 21 trang & Kịch bản bảo vệ toàn team (PM chính thức phê duyệt)
├── demo/                  # 🟡 Streamlit UI + XGBoost inference + mapping datetime/VNĐ (chờ screenshots & video clip)
│   ├── inference.py      # 14-feature contract + XGBoost probability
│   ├── app.py            # Quick presets + signal/flow/error views + native motion
│   ├── assets/           # Logo và tài nguyên hình ảnh của demo
│   ├── screenshots/      # Ảnh kiểm thử giao diện
│   ├── WIREFRAME.md      # Bố cục và nguyên tắc giao diện
│   └── requirements-demo.txt
├── docs/                  # Tài liệu dự án
├── run_preprocessing.py   # Script chạy lại pipeline tiền xử lý (Phase 01)
├── run_imbalance_handling.py # Script chạy SMOTENC & ADASYN (Phase 02)
├── run_random_forest.py   # Script train & evaluate Random Forest (Phase 03)
├── run_xgboost.py         # Script train & evaluate XGBoost (Phase 04)
├── run_autoencoder.py     # Script train & evaluate Autoencoder (Phase 04)
├── run_report_metrics.py  # Script tính lại chỉ số + sinh lại 2 hình của Chương 5 (Phase 07)
├── build_report.py        # Script dựng bản Word của báo cáo từ report-source.md (Phase 07)
├── sync_toc_pages.py      # Script đọc số trang thật từ PDF để điền vào mục lục (Phase 07)
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

Demo đã tích hợp XGBoost-SMOTE và scaler thật, tái tạo đúng contract 14 đặc trưng, trả xác suất/nhãn theo ngưỡng và khóa an toàn nếu model, scaler hoặc schema lỗi.

**Trạng thái:** Model integration, comparison CSV và 9 figures đã tích hợp; có chuyển SMOTENC/ADASYN, Feature Importance, so sánh TP/FP/FN và lịch sử SQLite. Browser QA bố cục mới đạt; `45` demo tests và `87` tests toàn project pass. Phase 06 vẫn `pending`; còn screenshots và demo clip. Xem evidence tại [phase-06-demo-ui.md](../../plans/fraud-detection-full-submit/phase-06-demo-ui.md).

---

## 📊 Workflow

```
1. EDA            ✔ Phân tích phân phối, correlation, visualize imbalance (Thanh)
2. Preprocessing  ✔ Feature Engineering (14 features), chuẩn hóa, train/test split (Thanh)
3. Imbalance      ✔ SMOTENC & ADASYN trên tập train (Phase 02 — Sơn)
4. Modeling       ✔ Random Forest (Sơn) | XGBoost & Autoencoder (Cẩm) — ALL 3 MODELS DONE
5. Evaluation     ✔ 4/4 scripts done (PR #7, #26, #28); 74 tests pass (Khang)
6. Comparison     ✔ Bảng reports/model_comparison.csv + 7 figures ROC/PR/Confusion Matrix (Khang)
7. Demo UI        ✔ UI + inference + mapping datetime/VNĐ + comparison/9 figures + SQLite + Browser QA; → Chờ screenshots/clip (Trung)
8. Report         ✔ Báo cáo Word/PDF Tóm tắt + Chương 1–7 đầy đủ, 32 trang (Duy) + Bộ Slide 21 trang đã duyệt chính thức (Hôn)
```

> ⚠️ **PM Audit (09/09):** Đầy đủ 6/6 notebooks hoàn thành và chạy sạch (01–06); Phase 00–05 đạt 66.7%. Đang hoàn thiện evidence Demo UI và chuẩn bị đóng gói nộp bài cho Sprint 4.

> 📄 Dữ liệu đầu ra từ bước 2 đã được commit trong git. Xem chi tiết: [data/processed/README.md](./data/processed/README.md)

---

## 📝 Báo cáo & Nộp bài

- **Word**: Scientific Report + Technical Report
- **PPT**: Trình bày kết quả tại buổi báo cáo
- **Code**: Toàn bộ notebook + src scripts
- **Demo**: Clip hoặc hình ảnh demo
- **Nộp theo tên**: `[Project AI-UIT] - Nhóm 9`
