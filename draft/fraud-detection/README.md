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
├── demo/                  # ✅ Streamlit UI + XGBoost inference + Quy trình 4 bước + Import mẫu (74 tests pass, video Google Drive)
│   ├── app.py            # Giao diện chính Fraud Shield (Presets, Form, Kết quả, Pipeline)
│   ├── analysis_pipeline.py # Quy trình tiền xử lý, trích xuất đặc trưng & suy luận 4 bước
│   ├── pipeline_details.py  # Modal chi tiết từng bước trong quy trình phân tích
│   ├── sample_import.py     # Hộp chọn mẫu kiểm thử, parser CSV/JSON an toàn
│   ├── inference.py         # Hợp đồng 14 đặc trưng + XGBoost probability fail-closed
│   ├── evaluation_artifacts.py # Adapter nạp kết quả so sánh mô hình & 9 biểu đồ Phase 05
│   ├── DEMO-SCRIPT.md       # Kịch bản thuyết minh 7 cảnh demo kèm link video ngoại tuyến
│   ├── WIREFRAME.md         # Bố cục và nguyên tắc thiết kế giao diện
│   ├── assets/              # Logo và tài nguyên hình ảnh của demo
│   ├── screenshots/         # Ảnh chụp kiểm thử giao diện
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

**Trạng thái:** ✅ **Hoàn tất (Passed)** — Tích hợp đầy đủ XGBoost model inference, comparison CSV và 9 figures Phase 05; bổ sung quy trình phân tích 4 bước trực quan, hộp chọn/nhập mẫu CSV/JSON; Browser QA đạt chuẩn; `74/74` demo tests và `116/116` tests toàn project passed. Video clip demo lưu trữ ngoại tuyến tại Google Drive (tuân thủ giới hạn Git < 50MB) và kịch bản chi tiết tại `demo/DEMO-SCRIPT.md`. Xem evidence tại [phase-06-demo-ui.md](../../plans/fraud-detection-full-submit/phase-06-demo-ui.md).

---

## 📊 Workflow

```
1. EDA            ✔ Phân tích phân phối, correlation, visualize imbalance (Thanh)
2. Preprocessing  ✔ Feature Engineering (14 features), chuẩn hóa, train/test split (Thanh)
3. Imbalance      ✔ SMOTENC & ADASYN trên tập train (Phase 02 — Sơn)
4. Modeling       ✔ Random Forest (Sơn) | XGBoost & Autoencoder (Cẩm) — ALL 3 MODELS DONE
5. Evaluation     ✔ 4/4 scripts done (PR #7, #26, #28); 42 tests pass (Khang)
6. Comparison     ✔ Bảng reports/model_comparison.csv + 7 figures ROC/PR/Confusion Matrix (Khang)
7. Demo UI        ✔ Streamlit UI + XGBoost inference + Quy trình 4 bước + Import mẫu + 74 tests pass + Clip Google Drive (Trung)
8. Report         ✔ Báo cáo Word/PDF Tóm tắt + Chương 1–7 đầy đủ, 32 trang (Duy) + Bộ Slide 21 trang & Kịch bản đã duyệt chính thức (Hôn)
9. Packaging      ✔ Đóng gói tự động [Project AI-UIT] - Nhom 9.zip (118.58 MB), 116/116 tests pass, bảo mật 100% (Hôn)
```

> 🏆 **PM Audit & Final Verdict (19/09/2026):** Toàn bộ 9/9 phases (100%) đã chính thức **PASSED**. 6/6 notebooks hoàn thành và chạy sạch (01–06), 116/116 tests toàn dự án passed (74 demo tests + 42 evaluation/reporting tests). Gói nộp bài `[Project AI-UIT] - Nhom 9.zip` đã sẵn sàng nộp chính thức.

> 📄 Dữ liệu đầu ra từ bước 2 đã được commit trong git. Xem chi tiết: [data/processed/README.md](./data/processed/README.md)

---

## 📝 Báo cáo & Nộp bài

- **Word**: Scientific Report + Technical Report
- **PPT**: Trình bày kết quả tại buổi báo cáo
- **Code**: Toàn bộ notebook + src scripts
- **Demo**: Clip hoặc hình ảnh demo
- **Nộp theo tên**: `[Project AI-UIT] - Nhóm 9`
