# Project Roadmap — Fraud Detection Nhóm 9

## Hành trình dự án

**Bắt đầu:** 25/08/2026 (Thứ 3) &nbsp;|&nbsp; **Báo cáo:** Buổi 10 (~19/09/2026) &nbsp;|&nbsp; **Sprint review:** Mỗi tối Thứ 6 hàng tuần

> Nhóm Preprocessing & Modeling (Thanh, Sơn, Cẩm) tập trung triển khai pipeline dữ liệu và huấn luyện. Nhóm Đánh giá & Báo cáo (Hôn, Khang, Duy, Trung) triển khai song song các phần việc bổ trợ để tối ưu thời gian.

---

## 🗺️ Lộ trình tổng thể (Biểu đồ Gantt)

```mermaid
gantt
    title Hệ thống Phát hiện Giao dịch Bất thường - Tiến độ Nhóm 9
    dateFormat  YYYY-MM-DD
    axisFormat  %d/%m
    tickInterval 1w

    section Sprint 1 (25/8 - 28/8)
    Setup repo & Scaffold (Thanh)        :done, s1_1, 2026-08-25, 2026-08-28
    Lên kế hoạch & Phân công (Hôn)      :done, s1_2, 2026-08-25, 2026-08-28

    section Sprint 2 (28/8 - 4/9)
    Tải dữ liệu & EDA (Thanh)            :done, s2_1, 2026-08-28, 2d
    Preprocessing & Outliers (Thanh)     :done, s2_2, 2026-08-30, 2d
    Imbalance Analysis & SMOTE/ADASYN (Sơn) :done, s2_3, 2026-08-28, 4d
    Huấn luyện Random Forest (Sơn)       :done, s2_4, 2026-08-30, 2d
    Viết Eval scripts template (Khang)   :done, s2_5, 2026-08-28, 7d
    Thiết kế UI & Form shell (Trung)     :done, s2_6, 2026-08-28, 2d
    Viết báo cáo Intro + Dataset (Duy)   :done, s2_7, 2026-08-28, 4d
    PPT Template & 9 slides nháp (Hôn)   :done, s2_8, 2026-08-28, 4d

    section Sprint 3 (4/9 - 11/9)
    XGBoost & Autoencoder (Cẩm)          :done, s3_1, 2026-09-01, 7d
    Evaluation metrics execution (Khang) :done, s3_2, 2026-09-01, 7d
    Tích hợp model thật vào UI (Trung)   :done, s3_3, 2026-09-01, 4d
    Viết Methodology + Results (Duy)      :done, s3_4, 2026-09-01, 4d
    Cập nhật slides kết quả (Hôn)        :done, s3_5, 2026-09-01, 7d

    section Sprint 4 (11/9 - 18/9)
    Chạy evaluation & So sánh (Khang)   :done, s4_1, 2026-09-06, 3d
    Figures & demo evidence (Trung)      :done, s4_2, 2026-09-09, 4d
    Báo cáo Results & Conclusion (Duy)   :done, s4_3, 2026-09-09, 4d
    Hoàn thiện PPT & Review (Hôn)        :done, s4_4, 2026-09-09, 4d
    Đóng gói & Nộp bài (Hôn)             :done, s4_5, 2026-09-17, 1d
```

---

## 🏃 Sprint 1 — 25/8 (Thứ 3) → 28/8 tối (Thứ 6)

> **Mục tiêu Sprint 1:** Khởi động dự án, thiết lập môi trường và cấu trúc thư mục, thống nhất phân công.
> **Sprint Review:** Tối Thứ 6 28/8 — tổng kết setup repo và kick-off Sprint 2.

### Thanh
| Task | Trạng thái |
|------|-----------|
| ✅ Setup repo, tạo cấu trúc thư mục | **Xong** |

### Hôn
| Task | Trạng thái |
|------|-----------|
| ✅ PM: Lên kế hoạch dự án, phân công vai trò & theo dõi tiến độ nhóm hàng tuần | **Xong** |

---

## 🏃 Sprint 2 — 28/8 (Thứ 6) → 4/9 tối (Thứ 6)

> **Mục tiêu Sprint 2:** Hoàn thành EDA, Preprocessing (Thanh) + Imbalance Analysis (Sơn). Lớp A viết xong các template scripts, UI shell và nháp báo cáo.
> **Sprint Review:** Tối Thứ 6 4/9 — báo cáo tiến độ EDA và check-point code/design của lớp A.

### Thanh
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| Setup môi trường (venv) & Tải dataset từ Kaggle <br> *[Đầu vào: Kaggle dataset link \| Đầu ra: `data/raw/paysim.csv`, `.venv`]* | 🔴 Critical | ✅ |
| Notebook EDA & Trực quan hóa (Phân phối Class, Amount, step, type, balances) <br> *[Đầu vào: `data/raw/paysim.csv` \| Đầu ra: `notebooks/01_eda.ipynb` với ít nhất 5 charts]* | 🔴 Critical | ✅ |
| Preprocessing dữ liệu (Chuẩn hóa các cột balances/amount & One-Hot Encoding `type` & Downsampling) <br> *[Đầu vào: `data/raw/paysim.csv` \| Đầu ra: scaled columns, OHE, downsampled splits, fitted `models/scaler.pkl`]* | 🔴 Critical | ✅ |
| Chia tập dữ liệu Train/Test split (Stratified 80/20) <br> *[Đầu vào: scaled data \| Đầu ra: `data/processed/X_train.pkl`, `X_test.pkl`, `y_train.pkl`, `y_test.pkl`]* | 🔴 Critical | ✅ |
### Sơn
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| Phân tích + visualize tỷ lệ mất cân bằng (sau khi Thanh tải xong) <br> *[Đầu vào: `data/raw/paysim.csv` \| Đầu ra: tỷ lệ phân phối Class trên biểu đồ]* | 🟡 High | ✅ |
| Áp dụng SMOTE & ADASYN trên tập train <br> *[Đầu vào: `data/processed/X_train.pkl`, `y_train.pkl` \| Đầu ra: `X_train_smote.pkl`, `X_train_adasyn.pkl`]* | 🔴 Critical | ✅ |
| Huấn luyện mô hình Random Forest & Tuning (RandomizedSearchCV) <br> *[Đầu vào: resampled training data \| Đầu ra: `models/rf_smote.pkl`, `reports/rf_predictions.pkl`]* | 🔴 Critical | ✅ |

### Khang *(bắt đầu ngay, không cần chờ data)*
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| Viết `src/evaluation/metrics_calculator.py` template <br> *[Đầu vào: None \| Đầu ra: script định nghĩa hàm `compute_metrics`]* | 🟡 High | ✅ (PR #7 merged) |
| Viết `src/evaluation/plot_roc_curve.py` template <br> *[Đầu vào: None \| Đầu ra: script định nghĩa hàm `plot_roc_curves` & `plot_pr_curves`]* | 🟡 High | ✅ (PR #7 merged) |

### Trung *(bắt đầu ngay, không cần chờ data)*
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| Thiết kế wireframe UI (layout, input fields, output area) <br> *[Đầu vào: None \| Đầu ra: `demo/WIREFRAME.md`]* | 🟡 High | ✅ |
| Implement Streamlit UI shell <br> *[Đầu vào: processed labels \| Đầu ra: `demo/app.py` với form, 4 presets, theme switcher và 3 góc nhìn giao dịch]* | 🟡 High | ✅ |

### Duy *(bắt đầu ngay, không cần chờ data)*
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| Viết phần Introduction + Problem Statement (Word) <br> *[Đầu vào: Đề bài PDF \| Đầu ra: nháp Chương 1 & 2 của báo cáo]* | 🔴 Critical | ✅ |
| Viết phần Dataset Description (Word) <br> *[Đầu vào: Đề bài PDF + thông tin Kaggle \| Đầu ra: nháp Chương 3 mô tả dữ liệu]* | 🟡 High | ✅ |

### Hôn *(bắt đầu ngay, không cần chờ data)*
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| PPT: Thiết kế slide template (theme, layout, font) và chuẩn bị slide nháp giới thiệu (slide 1-9) <br> *[Đầu vào: Slide guidelines + Đề tài \| Đầu ra: file `.pptx` & `.pdf` slide nháp 9 trang]* | 🟡 High | ✅ |

---

## 🏃 Sprint 3 — 4/9 (Thứ 6) → 11/9 tối (Thứ 6)

> **Mục tiêu Sprint 3:** Hoàn thiện các phần mô hình còn lại, evaluation scripts, Methodology và tích hợp model thật vào UI.
> **Sprint Review:** Tối Thứ 6 11/9 — kiểm tra artifacts mô hình, tiến độ Phase 05, báo cáo và UI Streamlit sử dụng inference thật.

### Sơn
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| Áp dụng SMOTE trên tập train <br> *[Đầu vào: `data/processed/X_train.pkl`, `y_train.pkl` \| Đầu ra: `X_train_smote.pkl`, `y_train_smote.pkl`]* | 🔴 Critical | ✅ |
| Áp dụng ADASYN trên tập train (so sánh với SMOTE) <br> *[Đầu vào: `data/processed/X_train.pkl`, `y_train.pkl` \| Đầu ra: `X_train_adasyn.pkl`, `y_train_adasyn.pkl`]* | 🟡 High | ✅ |
| Huấn luyện mô hình Random Forest <br> *[Đầu vào: resampled training data \| Đầu ra: `src/models/random_forest_model.py`]* | 🔴 Critical | ✅ |
| Tối ưu hyperparameter cho Random Forest (RandomizedSearchCV) <br> *[Đầu vào: resampled training data + RF model \| Đầu ra: optimal RF model, `models/rf_smote.pkl`]* | 🟡 High | ✅ |

### Cẩm *(cần data đã split từ Thanh)*
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| Chuẩn bị dữ liệu: Load dữ liệu train/test đã tiền xử lý <br> *[Đầu vào: `data/processed/` `.pkl` files \| Đầu ra: dữ liệu sẵn sàng trong bộ nhớ để huấn luyện]* | 🟡 High | ✅ |
| Notebook & script huấn luyện mô hình XGBoost <br> *[Đầu ra: `run_xgboost.py`, `src/models/xgboost_model.py`, `notebooks/04_model_xgboost.ipynb`]* | 🔴 Critical | ✅ |
| Tối ưu hyperparameter cho XGBoost (RandomizedSearchCV) <br> *[Đầu ra: `models/xgb_smote.pkl` — F1=0.9963, AUC=0.9993 trên test]* | 🟡 High | ✅ |
| Script huấn luyện Autoencoder <br> *[⚠️ Keras/TF không có bản Python 3.14 → dùng sklearn MLPRegressor, cùng kiến trúc 16-8-4-8-16. Đầu ra: `models/autoencoder.pkl`, `models/autoencoder_threshold.txt` — Recall(fraud)=0.75, AUC=0.93]* | 🟢 Medium | ✅ |
| Lưu tất cả models vào `models/` <br> *[`xgb_smote.pkl`, `xgb_adasyn.pkl`, `autoencoder.pkl` (+ `.json` / threshold / meta)]* | 🔴 Critical | ✅ |

### Khang
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| Viết `src/evaluation/confusion_matrix_plot.py` template <br> *[Đầu vào: None \| Đầu ra: script định nghĩa hàm `plot_confusion_matrix`]* | 🟡 High | ✅ (PR #26 merged) |
| Viết `src/evaluation/model_comparator.py` template <br> *[Đầu vào: None \| Đầu ra: script định nghĩa hàm `compare_models` để tạo bảng so sánh]* | 🟡 High | ✅ (PR #26 merged) |

### Trung
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| Tích hợp XGBoost-SMOTE vào Streamlit và kiểm thử dự đoán <br> *[Đầu vào: `models/scaler.pkl`, `models/xgb_smote.json` \| Đầu ra: probability/nhãn theo contract 14 đặc trưng, 4 presets và mẫu X_test có nhãn]* | 🟡 High | ✅ |

### Duy
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| Viết phần Methodology: Preprocessing, Imbalance, Models (Word) <br> *[Đầu vào: Phase plans 01-04 \| Đầu ra: Chương 4 trong `report-source.md` + bản Word Sprint 3]* | 🔴 Critical | ✅ |
| Viết Results từ prediction artifacts <br> *[Đầu vào: `reports/*_predictions.pkl` + `y_test.pkl` \| Đầu ra: Chương 5 (5.1–5.6), `run_report_metrics.py` → `reports/ch5_metrics_recomputed.csv`, Hình 5.1, Hình 5.2 và hai bảng kết quả trong DOCX/PDF Sprint 3]* | 🔴 Critical | ✅ |

### Hôn
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| Cập nhật các slides non-tech (Dataset, Preprocessing, Models overview) <br> *[Đầu vào: Phase plans 01-04 \| Đầu ra: Slide nháp PPT]* | 🟡 High | ✅ (Bộ slide học thuật 21 trang & Kịch bản toàn team chính thức được PM duyệt; PM Audit Sprint 3 Closing) |

---

## 🏃 Sprint 4 — 11/9 (Thứ 6) → 18/9 (Thứ 6, Nộp bài)

> **Mục tiêu Sprint 4:** Chạy đánh giá và so sánh mô hình, hoàn tất browser QA/demo evidence, hoàn thiện báo cáo Word/PPT và đóng gói nộp bài.
> ⚠️ **Nộp bài:** Đóng gói và upload trước tối Thứ 6 18/9.

### Khang *(cần model output từ Sơn/Cẩm)*
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| Run: Chạy các scripts tính toán metrics và vẽ biểu đồ ROC/PR/Ma trận nhầm lẫn cho cả 3 mô hình <br> *[Đầu vào: trained models in `models/` + test data \| Đầu ra: computed metrics, `reports/roc_curves_all.png`, `pr_curves_all.png`, `confusion_matrix_[model].png`]* | 🔴 Critical | ✅ (Hoàn thành sớm ở Phase 05) |
| So sánh: Tổng hợp kết quả và xuất bảng so sánh hiệu năng các mô hình <br> *[Đầu vào: computed metrics \| Đầu ra: `reports/model_comparison.csv`]* | 🔴 Critical | ✅ (Hoàn thành sớm ở Phase 05) |

### Trung *(cần figures/kết luận từ Phase 05)*
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| Browser QA System/Sáng/Tối <br> *[Đầu vào: app đã tích hợp XGBoost \| Đầu ra: giao diện được kiểm tra trực quan trên ba theme]* | 🟡 High | ✅ |
| Tích hợp figures/kết luận model <br> *[Đầu vào: output Phase 05 \| Đầu ra: UI hiển thị kết quả so sánh chính thức]* | 🟡 High | ✅ (Đã kết nối qua `evaluation_artifacts.py`) |
| Quay clip demo + viết hướng dẫn sử dụng UI ngắn <br> *[Đầu vào: Running Streamlit app \| Đầu ra: `demo/screenshots` hoặc video mp4]* | 🟢 Medium | ✅ Đã hoàn tất: Kịch bản `DEMO-SCRIPT.md`, 74 tests pass, video demo lưu trữ Google Drive |

### Duy *(cần kết quả từ Khang)*
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| Đối chiếu Results draft và viết Discussion (Word) <br> *[Đầu vào: `reports/model_comparison.csv` + plots \| Đầu ra: Chương 5 đã xác nhận + Chương 6 Thảo luận]* | 🔴 Critical | ✅ (Chương 5 & 6 khớp 100% Phase 05) |
| Viết Conclusion + References, tóm tắt Abstract <br> *[Đầu vào: Final outcomes \| Đầu ra: Chương 7, Tóm tắt & tài liệu tham khảo]* | 🟡 High | ✅ (Chương 7, Bảng 7.1 & [1]–[8] IEEE) |
| Format báo cáo Word & kiểm tra tài liệu tham khảo <br> *[Đầu vào: All text segments \| Đầu ra: `reports/[Nhom9]_BaoCao_FraudDetection.docx` hoàn chỉnh]* | 🟡 High | ✅ Hoàn thành: DOCX/PDF 32 trang chuẩn cấu trúc UIT qua build_report.py |

### Hôn
| Task | Ưu tiên | Trạng thái |
|------|---------|-----------|
| PPT: Cập nhật kết quả thực tế, biểu đồ so sánh và ảnh chụp Streamlit UI vào PPT <br> *[Đầu vào: `reports/model_comparison.csv` + plots + UI screenshots \| Đầu ra: `reports/[Nhom9]_PPT_FraudDetection.pptx` hoàn chỉnh]* | 🔴 Critical | ✅ (Slide 21 trang & kịch bản 7 người đã duyệt) |
| Đóng gói: Kiểm tra chạy notebooks end-to-end không lỗi, nén zip thư mục `submit/` và nộp bài <br> *[Đầu vào: code, report, slides, demo folders \| Đầu ra: `submit/[Project AI-UIT] - Nhom 9.zip` nộp trước deadline]* | 🔴 Critical | ✅ Hoàn thành đóng gói tự động: ZIP 118.58 MB (128 files), 116 tests pass, bảo mật 100% |

---

## 📊 Tổng kết phân công

| Người | Lớp | Số tasks | Sprint bắt đầu | Ghi chú |
|-------|-----|---------|---------------|---------|
| **Đặng Chí Thanh** | B | 5 | Sprint 1 | Setup repo, tải dữ liệu, EDA, Preprocessing, Splitting |
| **Hoàng Cao Sơn** | B | 5 | Sprint 2 | Phân tích imbalance, SMOTE/ADASYN, RF |
| **Bùi Thị Mỷ Cẩm** | B | 5 | Sprint 3 | XGBoost, Autoencoder, Chuẩn bị dữ liệu & Lưu model |
| **Nguyễn Duy Khang** | A | 6 | Sprint 2 (scripts), Sprint 4 (chạy) | Đánh giá, vẽ biểu đồ, so sánh hiệu năng |
| **Phạm Thành Trung** | A | 5 | Sprint 2 (UI), Sprint 4 (kết nối) | Demo UI shell, kết nối model, quay clip |
| **Vũ Văn Duy** | A | 6 | Sprint 2 (70%), Sprint 4 (kết quả) | Soạn thảo báo cáo Word (Scientific) |
| **Trần Hoàng Hôn** | A | 5 | Sprint 1 (PM), Sprint 4 (hoàn thiện) | PM, PPT, Đóng gói & Nộp bài |

> Nhóm Đánh giá & Báo cáo phụ thuộc vào output của các mô hình từ nhóm Preprocessing/Modeling.

---

## Risk Register

| Rủi ro | Khả năng | Tác động | Biện pháp giảm thiểu |
|--------|----------|----------|------------|
| Dataset tải chậm / bị chặn | Thấp | Cao | Dùng Kaggle API hoặc link backup |
| Tiến độ báo cáo bị trễ do chờ kết quả model | Trung bình | Trung bình | Xây dựng trước các template code đánh giá và khung báo cáo trong Sprint 2-3 |
| Autoencoder khó huấn luyện | Trung bình | Thấp | Xem đây là phần tùy chọn (bonus), tập trung RF và XGBoost trước |
| SMOTE làm overfit | Trung bình | Trung bình | Chỉ thực hiện trên tập train, đánh giá chéo (cross-validation) |
| Xung đột code giữa các thành viên | Thấp | Trung bình | Mỗi thành viên thực hiện trên notebook và file script riêng biệt |
