# Phase 07 — Báo cáo Word + PPT

**Parent plan:** [plan.md](./plan.md)  
**Depends on:** [Phase 05](./phase-05-evaluation-comparison.md) — `pending` *(chỉ phần Results & Discussion + điền số cuối vào PPT — Sprint 4)*
**Early Start:** ~70% Word + PPT skeleton có thể viết từ **Sprint 2** — không cần kết quả  
**Parallel with:** [Phase 06](./phase-06-demo-ui.md)  
**Next phase:** [Phase 08 — Submit Package](./phase-08-submit-package.md)

---

## Overview

| Field | Value |
|-------|-------|
| Owner | **Duy** (Word) + **Hôn** (PPT) |
| Priority | P0 — Required for submission |
| Status | `pending` |
| Review | ⬜ Not reviewed |
| Estimated effort | 4–6 giờ tổng (2 người) |
| Sprint | Sprint 2–3 (phần không cần kết quả), Sprint 4 (Results & Hoàn thiện) |

## ⚡ Early Start Tasks — Duy + Hôn bắt đầu từ Sprint 2

> **Duy:** ~70% báo cáo không cần số kết quả. Viết ngay từ Sprint 2, điền Results sau Sprint 4.
> **Hôn:** Template + slides non-technical bắt đầu ngay từ Sprint 2. Điền số sau Sprint 4.

### Duy — Báo cáo Word
| Task | Sprint | Ghi chú | Trạng thái |
|------|--------|---------|------------|
| Viết Introduction + Problem Statement | Sprint 2 | Không cần code | ✅ Hoàn thành |
| Viết Dataset Description (Kaggle stats) | Sprint 2 | Dùng đề bài, Kaggle, PaySim paper và evidence Phase 01 | ✅ Hoàn thành |
| Viết Methodology (thuật toán + preprocessing + imbalance) | Sprint 3 | Dựa trên evidence Phase 01–04 | ✅ Hoàn thành |
| Viết Results & Discussion (điền số từ Khang) | Sprint 3–4 | Chương 5 (5.1–5.6) và Chương 6 (6.1–6.7) đã viết xong và tái lập được qua `run_report_metrics.py`; còn đối chiếu với ROC/PR figures của Phase 05 và ablation đặc trưng số dư | ✅ Hoàn thành bản nháp |
| Viết Conclusion + References | Sprint 4 | Draft trước, hoàn thiện sau | 🔲 Chưa bắt đầu |
| Format Word + Abstract + kiểm tra citation | Sprint 4 | | 🔲 Chưa bắt đầu |

#### Evidence Early Start — Duy, Sprint 2 (29/08/2026)

- Branch riêng: `docs/vu-van-duy-sprint2-report`.
- Source có thể review bằng Git: `draft/fraud-detection/reports/report-source.md`.
- Word draft: `draft/fraud-detection/reports/[Nhom9]_BaoCao_FraudDetection_Sprint2_Duy.docx`.
- Phạm vi đã viết: Chương 1 — Giới thiệu; Chương 2 — Phát biểu bài toán; Chương 3 — Mô tả dữ liệu.
- Evidence sử dụng: đề bài CS106, notebook EDA, Phase 01, PaySim paper và Kaggle data card.
- Kiểm tra lại artifact hiện tại: DOCX package validation PASS; 132 paragraphs, 6 tables; PDF Sprint 2 tồn tại với 13 trang.
- Quy trình dựng bản nộp đã được tự động hoá, không phải chỉnh tay trong trình soạn thảo.
- Phase 07 tổng thể vẫn `pending`; Methodology, Results, Discussion, Conclusion và Abstract chờ Sprint 3–4.

#### Quy trình dựng bản Word/PDF (Duy)

Bản DOCX được sinh hoàn toàn từ `reports/report-source.md`, không chỉnh tay:

```bash
cd draft/fraud-detection
python build_report.py        # dựng DOCX theo khuôn reports/_report_template.docx
# xuất PDF từ DOCX
python sync_toc_pages.py      # đọc số trang thật từ PDF
python build_report.py        # dựng lại, mục lục đã có số trang đúng
# xuất PDF lần cuối
```

`_report_template.docx` là bản Sprint 2 đã bị xoá sạch phần thân, chỉ giữ styles,
header, footer, khổ A4 và lề. Nhờ vậy định dạng không đổi qua các sprint, còn nội
dung luôn khớp source. Vòng lặp hai lần là để số trang trong mục lục hội tụ — đã
xác nhận ổn định ngay từ vòng thứ nhất.

#### Evidence — Chương 6 Thảo luận, Duy (04/09/2026)

- Đã viết Chương 6 gồm 7 mục: trả lời ba câu hỏi nghiên cứu của Mục 2.5, giải thích vì sao các chỉ số cao bất thường, quy chiếu hiệu năng về tỷ lệ gian lận gốc, kiểm tra độ tin cậy của thứ hạng, đánh giá vai trò mô hình phát hiện bất thường, tổng hợp hạn chế và kết luận chương.
- **Bảng 6.1** quy chiếu Precision về tỷ lệ gian lận gốc 0,129082% của PaySim. Phép quy chiếu hợp lệ vì downsampling chỉ lấy mẫu ngẫu nhiên lớp bình thường nên không đổi phân bố có điều kiện, do đó TPR và FPR đo trên test vẫn dùng được. Kết quả: RF-SMOTENC 0,9994 → 0,9801, RF-ADASYN → 0,9427, XGB-SMOTENC → 0,9250, XGB-ADASYN → 0,8757, Autoencoder 0,3822 → 0,0183 (khoảng 52.000 cảnh báo nhầm mỗi triệu giao dịch).
- **Phát hiện đáng chú ý:** khoảng tin cậy Clopper–Pearson 95% của bốn biến thể học có giám sát chồng lấn nhau (RF-SMOTENC 0,8985–0,9995 so với XGB-ADASYN 0,7738–0,9460), nên thứ tự 1/3/4/7 FP **chưa đủ tin cậy thống kê để xếp hạng**. Mục 6.4 phát biểu lại kết luận Chương 5 cho chính xác. Muốn xếp hạng có căn cứ cần lặp nhiều seed hoặc tập kiểm tra lớn hơn.
- Đã mở rộng `run_report_metrics.py` sinh thêm `reports/ch6_prevalence_projection.csv`, nên toàn bộ số liệu Chương 6 cũng tái lập được bằng một lệnh.
- Đã chuyển mục tài liệu tham khảo sang căn trái để hết hiện tượng giãn ký tự ở dòng chứa DOI dài.

#### Evidence Early Start — Duy, Sprint 3 (04/09/2026)

- Branch riêng: `docs/vu-van-duy-sprint3-methodology` từ `origin/main` tại `646ca1d`.
- Source đã đồng bộ: `draft/fraud-detection/reports/report-source.md`.
- Word/PDF draft mới, giữ format của bản Sprint 2:
  - `draft/fraud-detection/reports/[Nhom9]_BaoCao_FraudDetection_Sprint3_Duy.docx`.
  - `draft/fraud-detection/reports/[Nhom9]_BaoCao_FraudDetection_Sprint3_Duy.pdf`.
- Đã sửa mô tả pipeline từ 9 lên 14 đặc trưng và bổ sung đầy đủ 7 đặc trưng dẫn xuất. Nội dung báo cáo không còn trộn tên Phase, file plan hoặc tiến độ nội bộ vào phần trình bày khoa học.
- Đã mô tả đúng thứ tự chống rò rỉ dữ liệu: chia train/test trước khi khớp `StandardScaler`, chỉ khớp scaler trên train rồi transform test, chỉ áp dụng SMOTENC/ADASYN trên train và giữ nguyên test để đánh giá.
- Đã thêm Chương 4 gồm quy trình thực nghiệm, preprocessing, SMOTENC/ADASYN, Random Forest, XGBoost, Autoencoder, giao thức đánh giá, khả năng tái lập và giới hạn phương pháp.
- Đã thêm bản nháp Chương 5 (5.1–5.6) từ `rf_predictions.pkl`, `xgb_predictions.pkl`, `autoencoder_predictions.pkl` và `y_test.pkl`: bảng 5 biến thể, biểu đồ bốn thành phần TN/FP/FN/TP, mức đóng góp đặc trưng và phân tích SMOTENC/ADASYN. Random Forest + SMOTENC tạm dẫn đầu với F1=0.9973.
- Đã thêm `src/evaluation/plot_confusion_components.py` và `reports/figures/confusion_matrix_components.png`. Hình 5.1 dùng bốn đồ thị riêng, cùng trục hoành mô hình và trục tung số giao dịch để tránh TN/TP che khuất FP/FN. Hai panel FP và FN chuyển sang trục tung thang logarit vì giá trị chênh nhau tới ba bậc độ lớn (FP: 1 so với 1.998) — ở thang tuyến tính, các cột 1/3/4/7 bị dí sát trục và không so sánh được với nhau.
- Đã rà soát lại thuật ngữ Chương 4 và 5, bỏ lối dịch sát nghĩa và thống nhất cách gọi trong toàn báo cáo: `random_state = 42` thay cho "hạt giống 42", `k_neighbors = 5` thay cho "năm láng giềng", `batch_size` / `learning_rate_init` / `max_iter` / epoch / early stopping thay cho "kích thước lô" / "tốc độ học" / "chu kỳ huấn luyện" / "điều kiện dừng sớm", cross-validation k-fold thay cho "kiểm định chéo k phần", oversampling và downsampling thay cho "sinh mẫu" và "giảm mẫu", tập validation thay cho "tập xác thực", "độ bất thuần Gini" thay cho "tạp chất", "xác suất đã hiệu chuẩn" thay cho "hiệu chỉnh", bottleneck và anomaly score giữ nguyên thuật ngữ gốc. Mục 4.7 đổi tiêu đề từ "Giao thức đánh giá" thành "Quy trình đánh giá".
- Đã viết lại phần mô tả thuật toán cho đúng bản chất thay vì dịch máy móc tiêu đề bài báo: Random Forest nêu rõ bootstrap, tập con đặc trưng và cơ chế giảm phương sai; XGBoost nêu gradient boosting trên cây cùng ba cải tiến của bài báo gốc; Autoencoder giải thích vì sao bottleneck buộc mạng học biểu diễn nén. Mục 4.8 tách năm giới hạn thành danh sách có đánh thứ tự và trỏ sang bằng chứng ở Mục 5.5. Chương 5 bổ sung câu nối giải thích vì sao 8 giao dịch bỏ sót cần đặc trưng mới chứ không phải đổi thuật toán.
- Đã thêm `src/evaluation/plot_feature_importance.py` và `reports/figures/feature_importance_comparison.png` (Hình 5.2). Hình vẽ đủ 14 đặc trưng của cả hai mô hình trên hai panel riêng vì Gini và gain là hai thang đo khác nhau, tô màu tách nhóm đặc trưng số dư và ghi thẳng tỷ lệ 90,50% / 99,30% lên panel. Kèm 8 test trong `tests/evaluation/test_plot_feature_importance.py`.
- Đã mở rộng `run_report_metrics.py` để sinh lại **cả hai hình** của Chương 5 cùng lúc với bảng chỉ số, nên toàn bộ số và hình trong chương đều tái lập được bằng một lệnh.
- ⚠️ Ghi chú cho Thanh/Hôn: `slide/slide_assets/academic_feature_importance.png` ghi nhãn trục là "Relative Importance (F-Score)", nhưng giá trị 0.499 / 0.472 chính là `feature_importances_` mặc định của XGBoost, tức **gain** chứ không phải F-Score (weight). Số liệu khớp với Bảng 5.2, chỉ sai nhãn.
- Đã thêm `tests/evaluation/test_plot_confusion_components.py` (7 test: số bar khớp confusion matrix, quy tắc chuyển thang log, bỏ qua ghi file, hai nhánh lỗi đầu vào). Chạy `pytest tests/evaluation/` — 15 test pass, không có test nào của Khang bị ảnh hưởng.
- Đã thêm `run_report_metrics.py` (gọi `compute_metrics` của Khang) và `reports/ch5_metrics_recomputed.csv`. Toàn bộ số liệu Chương 5 nay truy được về một nguồn duy nhất và chạy lại được. Bảng 5.1 bổ sung cột Average Precision cho cả 5 biến thể: RF-SMOTENC 0.9983, RF-ADASYN 0.9978, XGB-SMOTENC 0.9969, XGB-ADASYN 0.9976, Autoencoder 0.5973. Khoảng cách ROC-AUC 0.9318 so với AP 0.5973 của Autoencoder được phân tích tại Mục 5.2. Bảng này là bằng chứng nháp và sẽ được thay bằng `model_comparison.csv` của Phase 05.
- Đã xác minh 8 giao dịch bị bỏ sót là **cùng một tập hợp** ở cả bốn mô hình học có giám sát (giao = hợp = 8), và Autoencoder bỏ sót 7/8 giao dịch đó. Kết luận này được viết vào Mục 5.3: phần gian lận chưa phát hiện là giới hạn của biểu diễn đặc trưng, không phải sai số ngẫu nhiên của từng mô hình.
- Đã thêm Mục 5.5 trả lời câu hỏi nghiên cứu thứ ba tại Mục 2.5, gồm Bảng 5.2 và Hình 5.2, dùng `rf_smote_feature_importance.csv` và `xgb_smote_feature_importance.csv`. `errorBalanceOrig` đứng đầu ở cả hai mô hình. Nhóm đặc trưng số dư chiếm 74,41% (RF) và 98,54% (XGB) mức đóng góp, lên 90,50% và 99,30% nếu tính thêm `is_drain_account` và `amount_to_oldbalance_ratio`. Đây là bằng chứng định lượng cho cảnh báo tại Mục 3.6.2.
- Đã sửa sơ đồ Pipeline Overview trong `AGENTS.md`: sơ đồ cũ ghi `feature_scaler.py` trước `data_splitter.py`, trái với `run_preprocessing.py` (split ở dòng 29, scale ở dòng 33) và trái với khẳng định chống rò rỉ dữ liệu tại Mục 2.3.3 và 4.1 của báo cáo.
- Đã công khai giới hạn PaySim không có vị trí để tính khoảng cách địa lý; không tự sinh dữ liệu vị trí không có nguồn gốc.
- Đã bổ sung nguồn gốc SMOTE, ADASYN, Random Forest, XGBoost và Autoencoder. Trích dẫn [1]–[8] được chuẩn hóa theo kiểu IEEE, đặt ngay sau tác giả, bộ dữ liệu, phương pháp hoặc mô hình được dẫn thay vì treo ở cuối đoạn. Danh mục tài liệu bên ngoài có đủ tác giả, tên công trình, nơi công bố, năm, trang và DOI/URL, đồng thời dùng thụt treo để dễ tra cứu.
- Kiểm tra cấu trúc: DOCX đọc lại bằng python-docx PASS; 216 paragraphs, 9 tables, 1 hình; mục lục đủ 38 dòng, gồm toàn bộ mục 4.1–4.9 và 5.1–5.6, kế thừa đúng style Sprint 2; bảng feature 14 dòng dữ liệu; không còn placeholder hoặc stale text của Sprint 2 trong bản Sprint 3.
- ✅ **DOCX/PDF đã dựng lại** từ source mới bằng `build_report.py`: Bảng 5.1 có cột Average Precision, có Mục 5.5 và Bảng 5.2, Mục 5.6 đánh số lại, Hình 5.1 dùng bản vẽ log-scale, danh mục tham khảo bỏ dấu ngoặc nhọn quanh URL và dùng thụt treo.
- Định dạng nội dung Chương 1–5 đã thống nhất theo hệ không thụt đầu dòng, căn đều hai lề, line spacing 1,3 và cách đoạn 4 pt. Mục 4.1 trình bày 6 bước bằng bullet. Bảng đặc trưng dùng cột `#` hẹp, cột nội dung căn trái và hàng 9–10 không còn bị giãn ký tự.
- Kiểm tra dấu câu: `report-source.md`, DOCX và PDF đều có 0 dấu chấm phẩy.
- Kiểm tra render: PDF A4 gồm 28 trang, có text layer trên cả 28 trang, không trang nào trống, 2 hình được nhúng đúng vị trí, mục lục 46 mục trải đúng 2 trang.
- Visual QA toàn bộ 23 trang: không có trang trắng, clipping, chồng chữ hoặc bảng vỡ; mục lục trang 2–3 có đủ 38 mục của Chương 1–5 và Tài liệu tham khảo; Chương 1 bắt đầu sạch ở trang 4; Hình 5.1 ở trang 19; footer chạy đúng `Page 1 of 23` đến `Page 23 of 23`; bản DOCX có 216 paragraph, 9 bảng, 1 hình.
- Danh sách và mục tài liệu tham khảo đã căn trái và dùng thụt treo, không còn hiện tượng giãn ký tự ở các dòng chứa tên tệp dài.
- ⚠️ Khác biệt duy nhất so với bản dựng tay trước đó: bảng 14 đặc trưng ở Mục 3.5 tách sang trang 12 mà không lặp lại hàng tiêu đề. XML đã đặt `tblHeader` đúng chuẩn nhưng Pages không áp dụng khi nhập từ DOCX. Có thể bật lại thủ công trong Pages (Table → Header rows) nếu cần.
- Phase 07 tổng thể vẫn `pending`; Chương 5 cần đối chiếu `model_comparison.csv` và figures chính thức từ Phase 05 trước khi viết Discussion, Conclusion, Abstract và bản Word cuối.

### Hôn — PPT
| Task | Sprint | Ghi chú | Trạng thái |
|------|--------|----------|------------|
| Thiết kế template PPT (theme, layout, màu, font) | Sprint 2 | Chuẩn phong cách UIT & Financial AI | ✅ Hoàn thành |
| Điền slides: Title, Team, Giới thiệu bài toán, Dataset, EDA (Slides 1–5) | Sprint 2 | Khớp dữ liệu PaySim và EDA | ✅ Hoàn thành |
| Điền slides: Pipeline, Preprocessing 14 features, Imbalance & Models (Slides 6–9) | Sprint 2–3 | Sơ đồ data flow chống leakage, 14 features, RF/XGB/AE | ✅ Hoàn thành |
| Điền slides: Kết quả, ROC, Confusion Matrix (Slides 10–12) | Sprint 3 | Số liệu thực nghiệm RF, XGBoost, Autoencoder | ✅ Hoàn thành |
| Điền slide Demo & Tổng kết (Slides 13–15) | Sprint 3 | Demo Streamlit, Hướng phát triển, Q&A | ✅ Hoàn thành |
| Hoàn thiện PPT + kiểm tra timing (15 slides) | Sprint 3 | Khớp 100% metrics thực tế | ✅ Hoàn thành |

#### Evidence Hoàn thiện Slides — Hôn (01/09/2026)

- Google Slides thiết kế gốc: [Google Slides Link](https://docs.google.com/presentation/d/1GEibG9p26vu57G15NdChx8SQrG0zTD50LZBwpIXPU58/edit?usp=sharing).
- File artifacts lưu trữ tại repo:
  - `draft/fraud-detection/reports/[Nhom9]_Slide_FraudDetection_Hon.pptx` (1.41 MB)
  - `draft/fraud-detection/reports/[Nhom9]_Slide_FraudDetection_Hon.pdf` (4.91 MB)
- Số lượng slide: **15 slides** hoàn chỉnh (Bìa, Mục lục, Đặt vấn đề & Thách thức, Dữ liệu PaySim, EDA Discoveries, Kiến trúc Pipeline, Tiền xử lý 14 features, Xử lý mất cân bằng, 3 Mô hình RF/XGB/AE, Tiêu chí đánh giá, Bảng so sánh đa tiêu chí, Ma trận nhầm lẫn & Feature Importance, Live Demo Streamlit, Tổng kết & Hướng phát triển, Q&A & Cảm ơn).
- Nội dung xác minh: Đầy đủ 15 slides, tích hợp 100% metrics thực tế từ Phase 03–04, hình ảnh trực quan và phân tích nghiệp vụ sâu sắc.
- Tài liệu bổ trợ (PR #13): Đã tích hợp bộ slide học thuật 24 trang song ngữ EN-VN (`draft/fraud-detection/slide/`) kèm bộ biểu đồ 300 DPI phục vụ làm tài liệu tham khảo và backup Q&A.

## Context

Duy viết báo cáo Word theo chuẩn Scientific Report. Hôn làm PPT cho buổi báo cáo. Cả 2 dùng kết quả từ Phase 05 (metrics, figures, comparison table).

## Requirements

**Word (Duy):**
- Scientific Report format (theo yêu cầu đề)
- Minimum sections: Abstract, Introduction, Dataset, Method, Results, Conclusion, References
- Chèn figures từ `reports/figures/`
- Chèn bảng so sánh từ `reports/model_comparison.csv`

**PPT (Hôn):**
- ~10–15 slides
- Slide kết quả phải có bảng so sánh và ít nhất 1 chart
- Thời lượng trình bày ước tính 10–15 phút

## Key Insights

- Hình ảnh: mọi hình trong báo cáo lấy từ `reports/figures/*.png`. Hiện có `confusion_matrix_components.png` (Hình 5.1, do Duy sinh bằng `src/evaluation/plot_confusion_components.py`). Các hình ROC và Precision–Recall tổng hợp sẽ được Phase 05 bổ sung vào cùng thư mục.
- Abstract: viết sau cùng khi có kết quả đầy đủ

## 💡 Ý tưởng Đề xuất & Cải tiến Nâng cao (từ MY_IDEAS)

1. **Điểm nhấn mở đầu: Sự thất bại của Rule cổ điển (`isFlaggedFraud`):**
   * Đưa số liệu thực chứng lên Slide 2 và Chương 1: Cờ cố định của ngân hàng cũ (chỉ flag khi `TRANSFER > 200,000`) chỉ bắt được **16 / 8,213 vụ** ($\approx \mathbf{0.19\%}$).
   * *Mục tiêu:* Tạo lập luận đanh thép và thuyết phục về lý do ngân hàng bắt buộc phải chuyển dịch sang AI/Machine Learning.
2. **Phản biện học thuật sâu sắc (Threats to Validity — Đã có trong Chương 3.6):**
   * **Prevalence Shift:** Tỷ lệ gian lận trong tập test sau downsample là $4.1\%$ (so với $0.13\%$ thực tế), do đó Precision đo được sẽ cao hơn môi trường thực $\rightarrow$ giải thích cách hiệu chỉnh ngưỡng xác suất khi triển khai thực tế.
   * **Simulator Artifacts:** Dữ liệu PaySim là dữ liệu mô phỏng, cần thảo luận việc các biến `errorBalance` có thể phản ánh cơ chế cập nhật của phần mềm giả lập bên cạnh hành vi con người.
   * **Temporal Leakage vs Random Split:** Thảo luận về sự khác biệt giữa Stratified Random Split và Time-based Split theo chuỗi thời gian `step`.
3. **Cấu trúc Slide thuyết trình 12 trang đạt chuẩn Rubric tối đa:**
   * Phân bổ thời lượng 10–15 phút chuẩn chỉ: 4 Slide đầu đặt vấn đề & Data $\rightarrow$ 3 Slide Pipeline & Modeling $\rightarrow$ 3 Slide Kết quả & Demo $\rightarrow$ 2 Slide Phản biện học thuật & Q&A.

## Related Files

```
draft/fraud-detection/
└── reports/
    ├── [Nhom9]_BaoCao_FraudDetection.docx    ← OUTPUT (Duy)
    ├── [Nhom9]_PPT_FraudDetection.pptx        ← OUTPUT (Hôn)
    ├── model_comparison.csv                   ← Input từ Phase 05
    └── figures/                               ← Input từ Phase 05
        ├── roc_curves_all.png
        ├── pr_curves_all.png
        ├── confusion_matrix_*.png
        └── ...
```

## Implementation Steps

### Báo cáo Word (Duy)

**Outline chuẩn Scientific Report:**

```
Title: Hệ thống Phát hiện Giao dịch Tài chính Bất thường
       và Nghi vấn Gian lận (Đề tài 7)
       
Group: Nhóm 9 — CS106, UIT

─────────────────────────────────────
1. TÓM TẮT (Abstract)                     [~150 words, viết sau cùng]
─────────────────────────────────────
2. GIỚI THIỆU (Introduction)
   2.1. Bối cảnh và tầm quan trọng
   2.2. Vấn đề nghiên cứu
   2.3. Mục tiêu đề tài
   2.4. Phạm vi nghiên cứu

3. DỮ LIỆU (Dataset)
   3.1. Mô tả dataset (Kaggle PaySim Mobile Money)
   3.2. Thống kê mô tả (shape, features, missing values, downsampling)
   3.3. Phân tích mất cân bằng (chart từ EDA)
   
4. PHƯƠNG PHÁP (Methodology)
   4.1. Tiền xử lý dữ liệu
        - Feature scaling (StandardScaler) & Encoding (One-Hot Encoding)
        - Stratified Downsampling và lọc giao dịch
        - Train/Test split (stratified 80/20)
   4.2. Xử lý mất cân bằng
        - SMOTE
        - ADASYN
        - So sánh trước/sau
   4.3. Mô hình học máy
        4.3.1. Random Forest
        4.3.2. XGBoost
        4.3.3. Autoencoder (Anomaly Detection)
   4.4. Metrics đánh giá
        - Lý do không dùng Accuracy
        - Precision, Recall, F1-Score, ROC-AUC

5. KẾT QUẢ (Results)
   5.1. Bảng so sánh hiệu năng (model_comparison.csv)
   5.2. ROC Curves (roc_curves_all.png)
   5.3. Precision-Recall Curves (pr_curves_all.png)
   5.4. Confusion Matrices
   5.5. Feature Importance (RF và XGBoost)

6. THẢO LUẬN (Discussion)
   6.1. Phân tích kết quả
   6.2. So sánh SMOTE vs ADASYN
   6.3. Hạn chế của nghiên cứu

7. KẾT LUẬN (Conclusion)
   7.1. Kết luận chính
   7.2. Đề xuất hướng phát triển

8. TÀI LIỆU THAM KHẢO (References)
   - Kaggle dataset citation
   - scikit-learn, xgboost, keras papers/docs
   - SMOTE original paper (Chawla et al. 2002)
   - ADASYN paper (He et al. 2008)
```

**Lưu ý format:**
- Font: Times New Roman 12pt (body), 14pt (headings)
- Page margins: 2.5cm all sides
- Line spacing: 1.5
- Figures: caption bên dưới, "Hình X: ..."
- Tables: caption bên trên, "Bảng X: ..."

### PPT Slides (Hôn)

```
Slide 1: Title Slide
  - Tên đề tài, môn học, nhóm, thành viên

Slide 2: Giới thiệu bài toán
  - Fraud detection là gì?
  - Thách thức chính (imbalanced data)

Slide 3: Dataset
  - Stats: ~200,000 transactions (downsampled), ~4.1% fraud
  - Chart: Class distribution (isFraud)

Slide 4: Pipeline Overview
  - Flow chart: Data → Preprocessing → Models → Evaluation

Slide 5: Tiền xử lý & Xử lý imbalance
  - StandardScaler cho balances/amount, OHE type
  - Downsampling & Feature Engineering (errorBalance)
  - SMOTE vs ADASYN: before/after distribution

Slide 6: Mô hình Random Forest
  - Architecture, best params, training time

Slide 7: Mô hình XGBoost
  - Architecture, best params, so sánh nhanh với RF

Slide 8: Mô hình Autoencoder
  - Architecture diagram
  - Reconstruction error approach

Slide 9: Kết quả tổng hợp
  - Bảng so sánh (dạng table đẹp)
  - Highlight best model

Slide 10: ROC Curves & Confusion Matrices
  - roc_curves_all.png
  - Best model confusion matrix

Slide 11: Demo
  - Screenshot từ Streamlit app

Slide 12: Kết luận & Đề xuất
  - Best model recommendation
  - Hạn chế + hướng phát triển

Slide 13: Q&A + Cảm ơn
```

## Checklist

**Word (Duy):**
- [ ] File Word được lưu: `reports/[Nhom9]_BaoCao_FraudDetection.docx`
- [ ] Có đủ 8 sections chính (TT → GTTK → ... → TLTK)
- [ ] Bảng so sánh models được chèn (từ Phase 05)
- [ ] Ít nhất 3 figures được chèn (ROC curves, confusion matrix, ...)
- [ ] Tài liệu tham khảo có ≥ 5 nguồn
- [ ] Abstract viết sau khi có kết quả (không phải plan)
- [ ] Đọc lại pass 1 lần trước khi commit

**PPT (Hôn):**
- [ ] File PPT được lưu: `reports/[Nhom9]_PPT_FraudDetection.pptx`
- [ ] Có đủ 12–15 slides
- [ ] Slide kết quả có bảng so sánh models
- [ ] Slide kết quả có ít nhất 1 chart (ROC hoặc confusion matrix)
- [ ] Slide demo có screenshot từ app
- [ ] Font size body ≥ 18pt (readable từ xa)
- [ ] Consistent design theme (không dùng quá nhiều màu)

## Success Criteria

| Criterion | Expected | Evidence |
|-----------|---------|---------|
| Word file exists | .docx saved | ___________ |
| PPT file exists | .pptx saved | ___________ |
| Word has sections | 8 sections | ___________ |
| PPT slide count | 12–15 slides | ___________ |
| Metrics in Word | correct values from Phase 05 | ___________ |

## Evidence Section *(điền sau khi làm)*

```
Word file: reports/[Nhom9]_BaoCao_FraudDetection.docx
  - Pages: ____
  - Figures inserted: ____ figures
  - Tables: ____ tables
  
PPT file: reports/[Nhom9]_PPT_FraudDetection.pptx
  - Slides: ____
  - Estimated time: ____ phút
```

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Metrics in report ≠ actual results | Medium | High | Copy directly from Phase 05 evidence section |
| Figures not displaying in Word | Low | Low | Insert as PNG, not linked |
| PPT too long/short | Low | Medium | Practice timing — target 10–15 min |

## Phase Summary *(viết sau khi làm — evidence-based)*

> ⬜ Chưa hoàn thành

```
Hoàn thành: __/__/2026
Duy: Word ____pages, ____figures
Hôn: PPT ____slides, ____min estimated
Kết quả best model ghi trong báo cáo: ____________________
```

## Commit

```bash
git add reports/
git commit -m "feat(phase07): scientific report (Word) + presentation slides (PPT)"
```
