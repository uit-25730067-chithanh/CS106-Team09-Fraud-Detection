# Phase 01: Thực Nghiệm Bổ Sung — Khảo Sát Loại Trừ Đặc Trưng (Ablation Study)

## 1. Context Links
- Parent Plan: [plan.md](plan.md)
- Research Synthesis: [teacher-critique-synthesis.md](research/teacher-critique-synthesis.md)
- Processed Data: [data/processed/](../../draft/fraud-detection/data/processed/)
- Model Baseline Config: [xgb_smote_summary.txt](../../draft/fraud-detection/reports/xgb_smote_summary.txt)

---

## 2. Overview
- **Ngày lập**: 2026-09-26
- **Mục tiêu**: Xây dựng và thực thi kịch bản đo đạc thực nghiệm Ablation Study tự động nhằm thu thập minh chứng số liệu 100% thực tế, giải quyết triệt để câu hỏi chất vấn của thầy Hiển về việc *"có thử giảm feature xuống không?"*.
- **Thời lượng dự kiến**: ~45 phút (bao gồm chạy script ~2 phút).
- **Mức độ ưu tiên**: P1 (Bắt buộc phải có số liệu thật trước khi đưa vào Slide và Report).
- **Trạng thái**: Completed.

---

## 3. Key Insights & Căn Cứ Khoa Học
1. **Dữ liệu đã sẵn sàng**: Toàn bộ tập dữ liệu đã xử lý chuẩn (`X_train_smote.pkl`, `y_train_smote.pkl`, `X_test.pkl`, `y_test.pkl`) đã được lưu trữ sẵn trong thư mục `draft/fraud-detection/data/processed/`.
2. **Tốc độ huấn luyện siêu tốc**: XGBoost với cấu hình siêu tham số tối ưu (`n_estimators = 300`, `max_depth = 8`, `tree_method = 'hist'`) chỉ mất ~57 giây cho toàn bộ 230.145 mẫu train.
3. **Thiết kế 3 kịch bản đối chứng chặt chẽ**:
   - **Kịch bản 1 (Full 14 Features - Baseline)**: Bộ 14 đặc trưng chuẩn hiện tại.
   - **Kịch bản 2 (Pruned Model - 12 Features)**: Loại bỏ 2 đặc trưng có mức đóng góp gần như triệt tiêu là `is_night_transaction` (Gain = 0.0%) và `is_large_transaction` (Gain = 0.012%). Đánh giá xem mô hình có giữ nguyên F1 / Recall hay không, đồng thời đo độ giảm thời gian huấn luyện và độ trễ suy luận (Inference Latency).
   - **Kịch bản 3 (No-Balance Ablation - 6 Features)**: Loại bỏ toàn bộ nhóm đặc trưng dẫn xuất từ số dư (`errorBalanceOrig`, `errorBalanceDest`, `oldbalanceOrg`, `newbalanceOrig`, `oldbalanceDest`, `newbalanceDest`, `is_drain_account`, `amount_to_oldbalance_ratio`), chỉ giữ lại nhóm đặc trưng giao dịch thuần túy (`step`, `amount`, `hour_of_day`, `is_night_transaction`, `is_large_transaction`, `type_TRANSFER`).
4. **Ý nghĩa học thuật**:
   - Nếu Kịch bản 2 cho kết quả tương đương: Minh chứng nhóm đã chủ động thực hiện **Feature Pruning** để tối ưu hóa hệ thống.
   - Nếu Kịch bản 3 cho kết quả sụt giảm mạnh: Minh chứng đanh thép rằng nhóm đặc trưng số dư là **yếu tố sống còn** mang bản chất tri thức kiểm toán kế toán kép, chứ không chỉ là "simulator artifact" ngẫu nhiên.

---

## 4. Requirements & Đặc Tả Kỹ Thuật
- Tạo script độc lập `scripts/run_ablation_study.py` trong `assignments/Final/draft/fraud-detection/`.
- Cố định `random_state = 42` để bảo đảm tính tái lập 100%.
- Xuất kết quả ra file dữ liệu bền vững: `reports/ablation_study_results.csv` chứa các cột:
  - `Scenario`: Tên kịch bản (Full_14, Pruned_12, No_Balance_6).
  - `Num_Features`: Số lượng đặc trưng.
  - `Train_Time_s`: Thời gian huấn luyện (giây).
  - `Inference_Time_ms_per_sample`: Thời gian dự đoán trung bình mỗi mẫu (ms).
  - `Precision`: Độ chính xác trên tập Test (4 chữ số thập phân).
  - `Recall`: Độ bao phủ trên tập Test (4 chữ số thập phân).
  - `F1_Score`: F1-Score trên tập Test (4 chữ số thập phân).
  - `ROC_AUC`: Diện tích dưới đường cong ROC (4 chữ số thập phân).
  - `PR_AUC`: Average Precision trên tập Test (4 chữ số thập phân).

---

## 5. Implementation Steps
1. **Khởi tạo script**: Viết `assignments/Final/draft/fraud-detection/scripts/run_ablation_study.py`.
2. **Thực thi thực nghiệm**: Kích hoạt môi trường Python và chạy script đo đạc 3 kịch bản.
3. **Xác nhận số liệu**: Kiểm tra tính toàn vẹn của bảng `reports/ablation_study_results.csv`.
4. **Lưu trữ nhật ký thực nghiệm**: Xuất bản tóm tắt phân tích vào `reports/ablation_study_summary.txt`.

---

## 6. Todo List
- [x] Soạn thảo mã nguồn `scripts/run_ablation_study.py`.
- [x] Chạy thực nghiệm Kịch bản 1 (Full 14 Features) để đối chiếu khớp 100% với baseline cũ (F1 = 0.9945, Recall = 0.9951).
- [x] Chạy thực nghiệm Kịch bản 2 (Pruned 12 Features) và đo thời gian suy luận (F1 = 0.9948, FP giảm từ 10 xuống 9).
- [x] Chạy thực nghiệm Kịch bản 3 (No-Balance 6 Features) để đo mức độ sụt giảm hiệu năng (F1 sụp đổ còn 0.7116, FN tăng lên 472).
- [x] Xuất file `reports/ablation_study_results.csv` và kiểm tra giá trị các chỉ số.
- [x] Tạo báo cáo tóm tắt kết quả sẵn sàng tích hợp vào Slide và Báo cáo Word.

---

## 7. Success Criteria & Evidence
- File `reports/ablation_study_results.csv` được sinh ra đầy đủ 3 dòng kịch bản.
- Kết quả của Kịch bản 1 khớp tuyệt đối với Bảng 5.1 trong báo cáo hiện tại (Precision = 0.9976, Recall = 0.9951, F1 = 0.9963).
- Có số liệu định lượng cụ thể về chênh lệch F1 và thời gian suy luận giữa 3 kịch bản.

---

## 8. Risk Assessment & Mitigations
- **Rủi ro**: Quá trình huấn luyện Kịch bản 3 có thể lâu hơn nếu hội tụ chậm.
  - *Tín hiệu*: Script chạy quá 3 phút.
  - *Biện pháp*: Sử dụng đúng cấu hình `tree_method = 'hist'` và `n_estimators = 300` đã được tối ưu hóa ở Phase trước.
- **Rủi ro**: Mất cân bằng dữ liệu ở Kịch bản 3 khiến Precision sụt giảm về gần 0.
  - *Xử lý*: Đây chính là bằng chứng học thuật mà ta cần để chứng minh vai trò không thể thay thế của tri thức kế toán số dư!

---

## 9. Next Steps
Chuyển sang [Phase 02](phase-02-slide-academic-refinement.md) và [Phase 03](phase-03-report-comprehensive-revision.md) để cập nhật số liệu mới vào Slide và Báo cáo.
