# BÁO CÁO ĐIỀU CHỈNH SLIDE — TOÀN BỘ 21 SLIDE NHÓM 9

**Gửi:** Anh Hôn (PM, phụ trách slide) · **Người kiểm tra:** Bùi Thị Mỷ Cẩm · **Ngày:** 20/09/2026
**Đối tượng:** `[Nhom9]_Slide_FraudDetection_Academic_VN.pptx` / `.pdf` (21 trang; đã kiểm cả text trong PPTX lẫn ảnh render PDF)
**Trạng thái repo lúc kiểm tra:** máy em đã ngang `origin/main` (commit `5cdfca3`, 19/09 23:23, PR #36). Slide chưa được sửa kể từ đó. Có 2 nhánh chưa merge, **chỉ chứa script** (không có slide): `docs/update-thanh-presentation-script` (bản script Thanh rút gọn) và `docs/hoang-son-presentation-script-html` (script HTML của Sơn).

Anh Hôn ơi, em đã đối chiếu **toàn bộ slide** với code, model đã lưu, file kết quả, báo cáo Word và demo. Mọi con số dưới đây đều **được tính lại từ dữ liệu thật** (không chỉ đọc file tóm tắt). Cách kiểm tra lại ở Phụ lục.

---

## 0. TÓM TẮT

**Báo cáo Word khớp với code và dữ liệu. Slide thì không:** có **18 điểm bắt buộc sửa (Nhóm A)** trên 15 slide (4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21). Nếu thầy đối chiếu slide với báo cáo hoặc mở link repo, các điểm này sẽ bị phát hiện ngay.

**3 việc gấp nhất (làm hỏng buổi bảo vệ nếu để nguyên):**
1. **Slide 21: repo đang PRIVATE nhưng slide ghi "Public Repo"** (A1). Thầy bấm link sẽ thấy 404.
2. **Slide 20: demo không có "Batch Audit CSV chấm hàng nghìn giao dịch"** và mẫu "Fraud > 99.8%" thực tế ra **88.36%** (A18). Clip demo nhúng ngay trong file PPTX sẽ **mâu thuẫn với chữ trên slide**.
3. **Các số không có nguồn:** 41.7s, 43.2s, 68.4s, 0.0211, 0.2104, 88.4%, 49.8%, 24.1%, 68.5% **không xuất hiện ở đâu trong repo** ngoài file sinh slide (A7, A8, A13).

### Danh sách Nhóm A theo slide

| # | Slide | Người phụ trách | Vấn đề bắt buộc sửa | Loại |
|---|---|---|---|---|
| A1 | 21 (và script) | Hôn | "Public Repo" nhưng repo là **PRIVATE** | Sai sự thật |
| A2 | 11 (và Q&A câu 1) | Sơn | Tập Test "0.13% fraud"; thực tế **4.11%** | Sai sự thật |
| A3 | 4, 11, 20 | Thanh / Sơn | "Leak-Free **tuyệt đối**" mâu thuẫn với 2 giới hạn chính báo cáo đã nêu | Mâu thuẫn báo cáo |
| A4 | 11, 6, 8, 20 | Sơn / Thanh | Thứ tự pipeline sai so với code; "14 engineered features" (thực tế 7 đặc trưng dẫn xuất) | Sai sự thật |
| A5 | 12 (khung RF) | Sơn | RF "100 cây, max_depth 15"; thực tế **200 cây, max_depth 20** | Sai sự thật |
| A6 | 13 | Cẩm | Kiến trúc Autoencoder `14→8→4→8→14`; thực tế `14→16→8→4→8→16→14` | Sai sự thật |
| A7 | 12, 15 | Cẩm / Khang | Thời gian train XGBoost 41.7s / 43.2s và "nhanh gấp 28.5 lần" không có nguồn | Số không nguồn |
| A8 | 15 | Khang | Thời gian train Autoencoder 68.4s không có nguồn; RF-ADASYN sai (Precision, F1, thời gian); Autoencoder Precision/F1 lệch 0.01–0.02 điểm | Sai / không nguồn |
| A9 | 17 | Khang | Bảng đóng góp: amount, hour, "10 features khác" sai | Sai sự thật |
| A10 | 17 (và 8, 20) | Khang / Thanh | "Top 2 đặc trưng **tự chế**" (`newbalanceOrig` là cột gốc); "số dư **đích**" (đúng: nguồn) | Sai sự thật |
| A11 | 8, 14, 17, 20 | Thanh / Khang | "Biến bài toán thành **tuyến tính**", "Engineering tạo **bước nhảy vọt**" không có thí nghiệm; báo cáo coi đây là **rủi ro tính hợp lệ** | Mâu thuẫn báo cáo |
| A12 | 4, 13, 15, 16, 18 | Cẩm / Khang | "Bắt tấn công **Zero-Day**" trái với kết luận của báo cáo | Mâu thuẫn báo cáo |
| A13 | 18 | Cẩm | Bảng ngưỡng: hàng 90th, 99th không có nguồn; trộn 2 nguồn | Số không nguồn |
| A14 | 18 | Cẩm | Hình phân bố sai số không tái lập được; trục cắt ẩn ~38–40% ca gian lận | Hình sai lệch |
| A15 | 12, 16, 20 | Cẩm / Trung | "Độ trễ suy luận < 0.5ms" không có phép đo | Số không nguồn |
| A16 | 5, 7 | Thanh | Lọc 2 loại giao dịch "triệt tiêu **70%**"; thực tế **56.5%** | Sai sự thật |
| A17 | 7 | Thanh | "Rút cạn số dư ... phân loại chính xác hàng đầu": cờ này cũng bật ở **42.95% giao dịch bình thường** | Hiểu sai dữ liệu |
| A18 | 20 (và script) | Trung / Duy | Demo: chọn RF/Autoencoder để suy luận, Batch CSV hàng nghìn dòng, "Fraud > 99.8%" đều **không đúng** với demo thật | Sai sự thật |

Nhóm B (14 mục) là chỗ nói quá, dễ bị hỏi vặn. Nhóm C là lỗi nhỏ. Mục 5 liệt kê những gì **đã kiểm chứng đúng**. Mục 6 là bảng việc theo từng người.

---

## 1. PHƯƠNG PHÁP VÀ GIỚI HẠN

**Đã làm:**
- Trích text từ PDF và XML trong PPTX (khớp nhau); render ảnh các slide 12, 13, 18; xem trực tiếp 4 ảnh biểu đồ trong `slide/slide_assets/`.
- Tính lại từ dữ liệu thật: confusion matrix 5 mô hình (`reports/*_predictions.pkl`); sai số tái tạo Autoencoder (tính lại từ `models/autoencoder.pkl`, khớp file đã lưu); sweep ngưỡng validation (tách lại đúng như `run_autoencoder.py`); độ quan trọng đặc trưng; tỷ lệ gian lận; cờ rút cạn trên toàn bộ 8,213 ca gian lận (Train + Test).
- Chạy 3 mẫu của demo qua `demo/inference.py` với `models/xgb_smote.json` thật; đo độ trễ (2,000 lần/kiểu).
- Tìm **từng con số nghi ngờ trong toàn repo** (mọi loại file). Kiểm tra trạng thái repo bằng `gh repo view`.
- Đối chiếu thứ tự pipeline với `run_preprocessing.py`, `feature_scaler.py`, báo cáo mục 4.1.

**Không kiểm tra được:**
- File `data/raw/paysim.csv` không có trên máy em. Tỷ lệ lọc loại giao dịch (56.5%) lấy từ **Bảng 3.3 báo cáo Word**, không tự đếm lại.
- Nội dung bên trong clip demo (mp4 76 MB nhúng trong PPTX): em không xem được video, chỉ đối chiếu với `demo/DEMO-SCRIPT.md` và chạy lại model.
- Độ trễ phụ thuộc máy (cấu hình ở Phụ lục).

**Tiêu chí:** **A** = mâu thuẫn trực tiếp với code / kết quả / báo cáo Word, hoặc số không có nguồn ở bất kỳ đâu. **B** = nói quá mức bằng chứng. **C** = lỗi nhỏ.

> ⚠️ Bản `.pptx` đã được chỉnh tay sau khi xuất từ `generate_cs106_style_slides_vn.js` (ví dụ Slide 12 trong PPTX: "khoảng 28 lần (~42s)", trong JS: "28.5 lần (~41.7s)"). Anh **sửa trực tiếp trên PPTX**; số dòng JS chỉ để tra nhanh.

---

## 2. NHÓM A — BẮT BUỘC SỬA

### A1. Slide 21 — Link repo đang PRIVATE (Hôn)
- **Đang ghi:** "Mã nguồn Dự án (Public Repo): https://github.com/uit-25730067-chithanh/CS106-Team09-Fraud-Detection". Script Slide 21: "đã được nhóm công khai trên GitHub".
- **Thực tế:** `gh repo view` trả về `"visibility":"PRIVATE"`. Truy cập không đăng nhập (web và API) đều **HTTP 404**. Thầy và các bạn sẽ không mở được.
- **Cách xử lý (chọn 1):**
  1. **Chuyển repo sang Public** trước buổi báo cáo. Em đã kiểm tra: **không có `.env`/token trong git** (chỉ có `.env.example`, `.env` đã nằm trong `.gitignore`, lịch sử không chứa file `.env`/`kaggle.json`). Lưu ý file PPTX 77.7 MB (kèm video) đang nằm trong repo. Vẫn nên tự rà lại trước khi công khai.
  2. Hoặc đổi chữ thành "Mã nguồn có trong gói nộp bài" và bỏ chữ "Public".
- Nhờ anh xác nhận với Thanh (chủ repo) vì repo thuộc tài khoản `uit-25730067-chithanh`.

### A2. Slide 11 — Tập Test "0.13% fraud" sai (Sơn)
- **Đang ghi:** "Tập Test hoàn toàn giữ nguyên phân bố tự nhiên (0.13% fraud)". Cũng có trong script Slide 11 và Q&A câu 1.
- **Thực tế:** Test có **1,643 / 40,000 = 4.1075%** gian lận, vì lớp bình thường đã downsample xuống 191,787. 0.13% chỉ là tỷ lệ PaySim gốc.
- **Bằng chứng:** `y_test.mean() = 0.041075` (tính lại từ `data/processed/y_test.pkl`); báo cáo mục 3.4 (bảng: Test 4,1075%) và mục 4.8 (giới hạn thứ nhất); AGENTS.md.
- **Sửa thành:** "Tập Test giữ nguyên phân bố sau downsample (4.11% fraud), không chứa mẫu nhân tạo". Nên nói rõ thêm: Precision trên Test không suy rộng được sang tỷ lệ 0.13% gốc (báo cáo Bảng 6.1).

### A3. Slide 4, 11, 20 — "Leak-Free tuyệt đối" mâu thuẫn với giới hạn báo cáo đã nêu (Thanh / Sơn)
- **Đang ghi:** Slide 4: "đảm bảo Leak-Free **tuyệt đối**"; Slide 11 tiêu đề "Chuẩn Leak-Free"; Slide 20: "Quy chuẩn Leak-Free".
- **Thực tế:** không có rò rỉ sang **tập Test** (đúng). Nhưng báo cáo Word tự nêu 2 giới hạn khiến "tuyệt đối" là quá mức:
  - **Mục 4.3 và 4.8 (giới hạn thứ ba):** oversampling chạy **một lần trên toàn bộ Train trước `RandomizedSearchCV`**, không đặt trong `imblearn.Pipeline` theo từng fold, nên điểm cross-validation "có thể lạc quan" do mẫu tổng hợp rò sang fold kiểm định.
  - **Mục 4.8 (giới hạn thứ năm):** tập validation của Autoencoder được tách **sau khi** `StandardScaler` đã khớp trên toàn bộ Train.
- Slide 11 còn ghi "Resampling ... (Train fold)" và "tune tham số đều tuân thủ Cross-Validation nội bộ" mà không nói CV chạy trên dữ liệu đã oversampling.
- **Sửa thành:** "Không rò rỉ sang tập Test: split trước, scaler chỉ fit trên Train, oversampling chỉ trên Train". Thêm 1 dòng: "Giới hạn: oversampling chưa nằm trong từng fold CV nên điểm CV có thể lạc quan (báo cáo mục 4.8)". Bỏ chữ "tuyệt đối".

### A4. Slide 11 (và 4, 6, 8, 20) — Thứ tự pipeline và "14 engineered features" (Sơn / Thanh)
- **Đang ghi:** Slide 11 thứ tự `B.1 Filtering → B.2 Feature Eng → B.3 Stratified Split → B.4 Resampling → ...` với "B.2: Tính toán **14** engineered features". Slide 4: "Thiết kế 14 features"; Slide 6: "Công thức Toán học của **14 Engineered Features**"; Slide 20: "**14 engineered features** chiếm > 97% split gains".
- **Thực tế (thứ tự):** code `run_preprocessing.py` (dòng 24–33): load (lọc + downsample) → **split** → `scale_features` (tạo đặc trưng **bên trong**, sau split). Báo cáo mục 4.1: Bước 3 = Chia dữ liệu, Bước 4 = Xây dựng đặc trưng, Bước 5 = Oversampling. Slide 11 để Feature Eng **trước** Split.
- **Thực tế (số lượng):** tổng **14 đặc trưng** đầu vào mô hình, trong đó **7 là đặc trưng dẫn xuất** (`errorBalanceOrig`, `errorBalanceDest`, `is_drain_account`, `hour_of_day`, `is_night_transaction`, `amount_to_oldbalance_ratio`, `is_large_transaction`); còn lại là 6 cột số gốc + `type_TRANSFER`. Báo cáo mục 3.5: "bảy đặc trưng dẫn xuất".
- **Sửa thành:** Slide 11: `Filtering & Downsample → Stratified Split → Feature Eng + Scaler (fit trên Train) → Resampling (chỉ Train) → Model Training → Evaluation`; "B.2: 7 đặc trưng dẫn xuất → 14 đặc trưng". Slide 4/6/20: "14 đặc trưng (7 dẫn xuất)" thay cho "14 engineered features".
- Lưu ý: vì các đặc trưng dẫn xuất tính theo từng dòng nên kết quả không đổi, nhưng slide viết về nguyên tắc chống rò rỉ mà thứ tự lại khác code thì dễ bị bắt lỗi.

### A5. Slide 12, khung Random Forest — sai tham số (Sơn)
- **Đang ghi:** "Tham số: n_estimators = 100, max_depth = 15", "Tập hợp 100 cây quyết định".
- **Thực tế:** cấu hình tốt nhất **n_estimators = 200, max_depth = 20** (SMOTENC); **500 cây** (ADASYN).
- **Bằng chứng:** `reports/rf_smote_summary.txt` (Best Hyperparameters); báo cáo mục 4.4; AGENTS.md.
- **Sửa thành:** "n_estimators = 200, max_depth = 20 (RandomizedSearchCV, 50 cấu hình, 5-fold)" và "Tập hợp 200 cây".

### A6. Slide 13 — Kiến trúc Autoencoder sai (Cẩm)
- **Đang ghi:** `14 (Input) → 8 (Dense) → 4 (Bottleneck) → 8 (Dense) → 14 (Output)`. Slide 13 không có hình mạng, chỉ có dòng chữ này.
- **Thực tế:** `14 → 16 → 8 → 4 → 8 → 16 → 14` (5 lớp ẩn 16-8-4-8-16).
- **Bằng chứng (4 nguồn khớp nhau):** `src/models/autoencoder_model.py:47` `HIDDEN_LAYER_SIZES = (16, 8, 4, 8, 16)`; `models/autoencoder_meta.json`; nạp `models/autoencoder.pkl` thấy ma trận trọng số `(14,16) (16,8) (8,4) (4,8) (8,16) (16,14)`; báo cáo mục 4.6.
- **Sửa thành:** `14 (Input) → 16 → 8 → 4 (Bottleneck) → 8 → 16 → 14 (Output)`.

### A7. Slide 12 và 15 — Thời gian train XGBoost và "nhanh gấp 28.5 lần" không có nguồn (Cẩm / Khang)
- **Đang ghi:** Slide 12 "nhanh gấp khoảng 28 lần (~42s)"; Slide 15 XGB-SMOTE **41.7s**, XGB-ADASYN **43.2s**, "nhanh gấp 28.5 lần".
- **Thực tế:** repo có **4 con số khác nhau** cho XGB-SMOTE:

| Giá trị | Nguồn |
|---|---|
| **57.94s** | `reports/xgb_smote_summary.txt` (đi kèm model đã lưu, sinh 03/09) |
| 43.7s | Output notebook `04_model_xgboost.ipynb` |
| 41.6s | `AGENTS.md` |
| 41.7s | **Slide (không nguồn nào)** |

  XGB-ADASYN: summary ghi **45.48s**, slide ghi 43.2s (không nguồn). Tỷ lệ cùng đợt chạy: RF-SMOTE 1187.68s / 57.94s = **20.5 lần**; ADASYN 1167.5 / 45.48 = 25.7 lần.
- **Sửa thành:** dùng số truy nguồn được: XGB-SMOTE **57.94s**, XGB-ADASYN **45.48s**, "nhanh hơn ~20 lần". Nếu anh muốn số khác, em **chạy lại `run_xgboost.py`** để có log gốc rồi cập nhật đồng loạt (slide, AGENTS.md). Cần thống nhất **một** con số.

### A8. Slide 15 — Sai số trong bảng chính (Khang; dòng Autoencoder của Cẩm)
| Ô | Đang ghi | Đúng là | Nguồn |
|---|---|---|---|
| RF-ADASYN Precision | 99.88% | **99.82%** | `model_comparison.csv`; tính lại từ pkl (FP = 3) |
| RF-ADASYN F1 | 99.69% | **99.66%** | như trên |
| RF-ADASYN Time | 1215s | **1167.5s** | `rf_adasyn_summary.txt` |
| XGB-SMOTE / XGB-ADASYN Time | 41.7s / 43.2s | **57.94s / 45.48s** | mục A7 |
| Autoencoder Precision | 38.23% | **38.22%** (1236/3234) | `model_comparison.csv` |
| Autoencoder F1 | 50.71% | **50.69%** (2·1236/4877) | như trên |
| Autoencoder Time | 68.4s | **không có số nào trong repo**, đổi thành "—" hoặc em chạy lại | không nguồn |

### A9. Slide 17 — Bảng đóng góp đặc trưng sai 3 dòng (Khang; số từ XGBoost của Cẩm)
| Đặc trưng | Slide | Thực tế (`xgb_smote_feature_importance.csv`) |
|---|---|---|
| amount | 1.4% | **0.49%** |
| hour / overnight | 0.9% | **0.03%** (`hour_of_day` 0.034% + `is_night_transaction` 0.000%) |
| 10 features khác | 0.6% | 9 features còn lại (ngoài top-2, amount, hour_of_day, is_night_transaction) cộng **2.36%** |

Báo cáo Bảng 5.2 ghi `amount` = **0,0049**, nên slide mâu thuẫn trực tiếp. Hai dòng đầu (errorBalanceOrig 49.9%, newbalanceOrig 47.2%; tổng 97.1%) **đúng**. **Sửa thành:** amount 0.5%, hour/overnight 0.03%, "9 features khác" 2.4%.

### A10. Slide 17 (và 8, 20) — "đặc trưng tự chế" và "số dư đích" sai (Khang / Thanh)
- **Đang ghi:** Slide 17 "Top 2 đặc trưng **tự chế** chiếm 97.1%"; Slide 8 "Hai biến errorBalanceOrig và newbalanceOrig ... Engineering"; Slide 17 chú thích "newbalanceOrig = 47.2%: 97.56% ca gian lận để lại **số dư đích** danh bằng 0".
- **Thực tế:** chỉ `errorBalanceOrig` là đặc trưng tự tạo. **`newbalanceOrig` là cột gốc của PaySim** (báo cáo mục 3.5, bảng đặc trưng, dòng 4: "Gốc + StandardScaler"). `newbalanceOrig` là số dư **nguồn**, không phải đích.
- **Về 97.56%:** em kiểm chứng trên toàn bộ 8,213 ca gian lận (Train + Test): cờ `is_drain_account` = **97.55%** (8,012/8,213). Gần đúng, nhưng là của cờ rút cạn, không riêng `newbalanceOrig`.
- **Sửa thành:** "`errorBalanceOrig` (đặc trưng dẫn xuất) và `newbalanceOrig` (cột gốc) chiếm 97.1% tổng Split Gains của XGBoost-SMOTE"; "97.55% ca gian lận rút cạn số dư **nguồn** về 0".

### A11. Slide 8, 14, 17, 20 — Khẳng định về feature engineering không có thí nghiệm, trái báo cáo (Thanh / Khang / Trung)
- **Đang ghi:** Slide 17: "Kỹ thuật đặc trưng biến bài toán phân lớp phi tuyến phức tạp thành ranh giới quyết định **tuyến tính** rõ rệt"; Slide 8: "Engineering tạo **bước nhảy vọt**"; Slide 14: "**Đóng góp Vượt bậc** của Engineering"; Slide 20: "14 engineered features chiếm > 97% split gains".
- **Vấn đề:** (1) không có thí nghiệm nào dùng mô hình tuyến tính hay so sánh có/không feature engineering; (2) báo cáo Word nói điều **ngược lại**:
  - **Mục 3.6.2:** Data card Kaggle **khuyến cáo không dùng** 4 cột số dư để phát hiện gian lận; mô hình "có thể học tín hiệu phát sinh từ cơ chế cập nhật hoặc hủy giao dịch của bộ mô phỏng". "Báo cáo xem đây là một **nguy cơ ảnh hưởng tính hợp lệ**".
  - **Mục 5.5:** nhóm đặc trưng số dư chiếm **98.54%** (XGB) và 74.41% (RF); "hiệu năng rất cao ... có thể phản ánh cơ chế cập nhật số dư của bộ mô phỏng thay vì đặc điểm tổng quát của hành vi gian lận". Chương 7: "Hạn chế lớn nhất là nguy cơ rò rỉ nhãn qua nhóm đặc trưng số dư".
- Slide đang trình bày đúng dữ liệu đó như **thành công**, trong khi báo cáo coi là **rủi ro**.
- **Sửa thành:** bỏ "tuyến tính", "bước nhảy vọt", "Đóng góp Vượt bậc". Thay bằng: "XGBoost dựa gần như hoàn toàn vào nhóm đặc trưng số dư (98.5%); đây cũng là rủi ro về tính hợp lệ (báo cáo mục 3.6.2)". Thêm 1 dòng vào mục "Hướng phát triển/Hạn chế" ở Slide 20.

### A12. Slide 4, 13, 15, 16, 18 — Khẳng định "Zero-Day" trái báo cáo (Cẩm / Khang)
- **Đang ghi:** Slide 4: "Unsupervised Deep Autoencoder **bắt Zero-Day**"; Slide 13: "Vai trò **Độc tôn**: Bắt Tấn công Zero-Day", "**Miễn nhiễm mẫu cũ**: Phát hiện hiệu quả các thủ thuật gian lận mới chưa từng có nhãn"; Slide 15/16: nhãn "(Zero-Day)", "phòng thủ **Zero-Day vững chắc**"; Slide 18: "Autoencoder **sẽ kích hoạt** báo động".
- **Vấn đề:** nhóm **chưa có thí nghiệm Zero-Day**. Em kiểm chứng trên Test: trong 8 ca XGBoost bỏ sót (chỉ số 8, 9040, 10743, 18058, 20647, 27968, 29114, 36335), Autoencoder chỉ bắt thêm **1 ca**, bỏ sót **7/8**. Báo cáo Word ghi: "trên bộ dữ liệu này Autoencoder **không bổ sung được vùng phủ nào** ... việc ghép hai hướng tiếp cận lại **chưa đem lại lợi ích đo được**".
- **Sửa thành:** "Bắt Tấn công Zero-Day" → "Lớp phòng thủ thứ cấp không cần nhãn"; "(Zero-Day)" → "(Unsupervised)"; "Miễn nhiễm ..." → "Không bị giới hạn bởi kiểu gian lận đã có nhãn (về nguyên lý; nhóm chưa kiểm thử riêng trên biến thể mới)"; "sẽ kích hoạt" → "có thể kích hoạt"; Slide 4 → "phát hiện bất thường (anomaly detection)".

### A13. Slide 18 — Bảng ngưỡng có 2 hàng không có nguồn, 4 hàng trộn 2 nguồn (Cẩm)
- **Đang ghi:** 90th (τ 0.0211, R 88.4%, P 24.1%); 95th (0.0455, 75.2%, 38.2%); 99th (0.2104, 49.8%, 68.5%); 99.9th (0.7460, 25.4%, 91.5%).
- **Vấn đề 1:** sáu giá trị `0.0211, 0.2104, 88.4%, 49.8%, 24.1%, 68.5%` **không có trong bất kỳ file nào của repo** (đã tìm mọi loại file), chỉ có trong `generate_cs106_style_slides_vn.js` (dòng 1044–1046).
- **Vấn đề 2:** hàng 95th là số **Test**, hàng 99.9th là số **validation** (trên Test là τ 0.8134, R 22.7%, P 90.5%).
- **Số đúng** (tính lại trên validation, khớp 100% `reports/autoencoder_summary.txt`):

| Phân vị | τ | Recall | Precision | F1 |
|---|---|---|---|---|
| 90th | 0.0134 | 84.78% | 26.63% | 0.4053 |
| 95th (chọn) | 0.0455 | 73.52% | 38.62% | 0.5064 |
| 99th | 0.1240 | 47.03% | 66.81% | 0.5520 |
| 99.9th | 0.7460 | 25.42% | 91.51% | 0.3979 |

- **Sửa thành:** thay 4 hàng bằng bảng trên (làm tròn 1 chữ số), tiêu đề "Quét ngưỡng trên tập validation". Bullet ghi rõ "Trên tập **Test**: Recall 75.2%, Precision 38.2%" (1,236/1,643 và 1,236/3,234).

### A14. Slide 18 — Hình phân bố sai số không tái lập được và gây hiểu sai (Cẩm)
- **Đang có:** `slide_assets/academic_autoencoder_dist.png` (thêm vào ở PR #13, **không có script nào trong repo tạo ra**).
- **Không tái lập được:** trục y: đỉnh Normal ~**128**, đỉnh Fraud ~**16**. Em vẽ lại cùng khoảng 0–0.18, `density=True`: Test (100 bins) đỉnh Normal **324**, Fraud **51**; validation (50 và 100 bins) Normal **213–322**, Fraud **52–56**. Không cấu hình nào ra 128/16.
- **Trục x cắt ở 0.18 ẩn phần lớn đuôi:** Test có **37.6%** (617/1,643) ca gian lận sai số > 0.18 (validation 39.8%); max ~1,389.
- **Hình cho thấy hai lớp tách gần hoàn toàn**, nhưng thực tế **24.8% ca gian lận (407 ca) nằm dưới ngưỡng** (chính là FN ở Slide 16) và **17.2% có sai số < 0.02**, cùng vùng với đa số giao dịch hợp lệ.
- **Phần đúng:** "giao dịch hợp lệ tập trung < 0.02" đúng (92.1% Test, 92.3% validation); sai số trung vị của gian lận lớn gấp **58 lần** của hợp lệ.
- **Sửa thành:** vẽ lại từ `reports/autoencoder_recon_errors.pkl` (đã có sẵn), **trục x thang log**; hoặc giữ trục tuyến tính và ghi chú "trục cắt ở 0.18; 37.6% ca gian lận nằm ngoài". Em có thể vẽ và gửi ảnh.

### A15. Slide 12, 16, 20 — "Độ trễ suy luận < 0.5 ms" không có phép đo (Cẩm / Trung)
- **Đang ghi:** Slide 12 và 16 "Độ trễ suy luận < 0.5ms"; Slide 20 banner "Latency < 0.5ms" và "XGBoost (< 0.5ms)".
- **Vấn đề:** không notebook, file kết quả, code demo hay báo cáo nào có phép đo (đã tìm `latency`, `perf_counter`, `time.time` trong `demo/` và notebook 04). Số được lặp 4 lần, không nguồn.
- **Em đo lại** (`xgb_smote.json`, xgboost 3.4.1, 2,000 lần):

| Cách gọi | Trung vị | p95 | p99 |
|---|---|---|---|
| numpy 1 dòng | **0.36 ms** | 0.53 ms | 0.65 ms |
| numpy 1 dòng, `n_jobs=1` | 0.19 ms | 0.41 ms | 0.55 ms |
| DataFrame 1 dòng (đường đi của `demo/inference.py`) | **1.86 ms** | 2.18 ms | 2.45 ms |

  Nghĩa là "< 0.5 ms" đúng ở trung vị mô hình thuần, **vượt ở p95/p99, và sai ~4 lần nếu tính cả đường đi của demo** (chưa kể scaler).
- **Sửa thành (chọn 1):** đổi thành "**cỡ nửa mili-giây** (mô hình thuần, 1 giao dịch, CPU)" và bỏ "Latency < 0.5ms" ở banner Slide 20; hoặc em thêm phép đo có log vào notebook 04 để có nguồn.

### A16. Slide 5, 7 — "triệt tiêu 70% dữ liệu" (Thanh)
- **Đang ghi:** lọc chỉ giữ TRANSFER & CASH_OUT "triệt tiêu **70%** dữ liệu nhiễu".
- **Thực tế:** giữ 2,770,409 / 6,362,620 = 43.5% → loại **56.5%** (báo cáo Bảng 3.3: CASH_OUT 2,237,500 + TRANSFER 532,909). *(Em không có CSV gốc, lấy từ báo cáo.)*
- **Sửa thành:** "loại ~56% giao dịch không có gian lận". Sửa cả script Slide 5 và Q&A.

### A17. Slide 7 — "Rút cạn số dư phân loại chính xác hàng đầu" (Thanh)
- **Đang ghi:** "Tín hiệu Cốt lõi: Tỷ lệ rút cạn tài khoản đóng vai trò phân loại chính xác hàng đầu".
- **Thực tế:** cờ `is_drain_account` = 1 ở **97.55%** ca gian lận nhưng **cũng bằng 1 ở 42.95% giao dịch bình thường** (tập Test, `X_test.pkl`), nên riêng nó không phân loại tốt. Trong XGBoost nó chỉ xếp **hạng 4 (0.59%)**; tín hiệu chính là `errorBalanceOrig` (sai lệch sổ cái).
- **Sửa thành:** "Gần như mọi ca gian lận (97.55%) rút cạn số dư nguồn; kết hợp với sai lệch sổ cái `errorBalanceOrig` mới tạo tín hiệu phân loại mạnh".

### A18. Slide 20 (và script Trung, Duy, Q&A câu 4) — Mô tả demo không đúng với demo thật (Trung / Duy)
Em đọc `demo/inference.py`, `demo/sample_import.py`, `demo/DEMO-SCRIPT.md` và **chạy 3 mẫu có sẵn của demo qua model thật**:

| # | Slide/Script ghi | Demo thật |
|---|---|---|
| a | Script Trung: "chọn mô hình suy luận (XGBoost, Random Forest hoặc Autoencoder)". Slide: "Phòng thủ Đa tầng: XGBoost + Autoencoder" | `demo/inference.py` **chỉ nạp XGBoost** (`load_xgboost_model`). RF và Autoencoder chỉ hiển thị chỉ số/biểu đồ so sánh |
| b | Slide: "**3. Batch Audit CSV**". Script Trung: "tải lên danh sách **hàng nghìn** giao dịch để tự động trích xuất các ca có nguy cơ cao". Q&A câu 4: "chấm điểm song song hàng chục ngàn dòng chỉ trong vài giây", "vector hóa" | Chức năng nhập file là **"Dữ liệu mẫu" CSV/JSON, tối đa 50 mẫu** (`sample_import.py:24 MAX_IMPORTED_SAMPLES = 50`, dòng 119–120), mỗi mẫu chấm từng giao dịch một. **Không có** chấm điểm hàng loạt hàng nghìn dòng. Lịch sử SQLite có xuất CSV, khác với "Batch Audit" |
| c | Slide banner: "**Rút cạn số dư (Fraud > 99.8%)**" | Mẫu "Nghi vấn gian lận" của demo: **88.36%** (`DEMO-SCRIPT.md` cũng ghi "khoảng 88%"). Mẫu "Cần lưu ý": 31.95%. Chỉ mẫu hợp lệ khớp: **0.004%** (< 0.1% ✓). Một giao dịch rút cạn khác em tự dựng cho 100.000%, nên "> 99.8%" chỉ đúng với input đặc biệt, không phải mẫu trong demo/clip |
| d | Script Duy: Kịch bản 3 = "**Zero-Day qua Autoencoder**". Slide: Kịch bản 3 = "Batch Audit CSV" | Hai nơi **mâu thuẫn nhau**; và cả hai đều không có trong demo |

- Điều đáng lo nhất: **clip demo (mp4 76 MB) nhúng ngay trong PPTX**, sẽ chiếu 88%, còn banner slide ghi > 99.8%.
- **Sửa thành:** banner Slide 20 → "3 tình huống mô phỏng: Hợp lệ (< 0.1%) · Cần lưu ý (~32%) · Nghi vấn gian lận (~88%)"; thay "Batch Audit CSV" bằng "Nhập dữ liệu mẫu CSV/JSON (tối đa 50 mẫu) & lịch sử phân tích SQLite"; bỏ nội dung "chọn RF/Autoencoder để suy luận" và "hàng nghìn giao dịch"; sửa Q&A câu 4 (`st.cache_resource` là đúng, còn "chấm hàng chục ngàn dòng" thì bỏ).

---

## 3. NHÓM B — NÊN SỬA (nói quá, dễ bị hỏi vặn)

| # | Slide | Đang ghi | Vấn đề | Đề nghị |
|---|---|---|---|---|
| B1 | 18 | "Điểm cắt Ngưỡng **Tối ưu**"; "cân bằng **tối ưu**" | F1 cao nhất trên validation là **99th (0.552)** > 95th (0.506). 95th được chọn vì ràng buộc `min_recall=0.60` (`run_autoencoder.py:75`); 99th chỉ đạt Recall 47% nên bị loại | "F1 cao nhất trong các ngưỡng có Recall ≥ 60%" |
| B2 | 18 | "Không phụ thuộc nhãn ... **tự thích ứng bền bỉ**" | Mô hình đã train xong, ngưỡng cố định, không tự thích ứng | "Không cần nhãn gian lận để huấn luyện mạng" |
| B3 | 13, 18 | "hoàn toàn KHÔNG sử dụng nhãn" | Đúng khi huấn luyện mạng; **chọn ngưỡng dùng nhãn fraud** của validation (`select_threshold_by_f1`) | Thêm "(nhãn chỉ dùng để chọn ngưỡng)" |
| B4 | 8, 17 | "Hai biến chiếm 97.1%" như chung mọi mô hình | Chỉ đúng với **XGBoost-SMOTE**. RF-SMOTE: errorBalanceOrig 41.1%, newbalanceOrig 4.9%, oldbalanceOrg 16.1% | Ghi "(XGBoost + SMOTE)" |
| B5 | 17 | Nhãn trục: "Relative Importance (**F-Score**)" | Giá trị là **gain** (tổng = 1; báo cáo cũng ghi gain). Đã có ghi chú ở `plans/.../phase-07-report-ppt.md` dòng 90 nhưng chưa sửa | "Relative Importance (Gain)" |
| B6 | 6, 9, 11, 15 | "SMOTE" | Code (`imbalance_handler.py`, dùng `SMOTENC`) và báo cáo đều là **SMOTENC** | Đổi thành "SMOTENC" hoặc chú thích |
| B7 | 9 | SMOTE nội suy "trong **Latent Space**" | SMOTE nội suy trong **không gian đặc trưng**, không phải latent space | "trong không gian đặc trưng" |
| B8 | 9 | "SMOTE **vượt trội** hơn ADASYN trên cả RF và XGBoost" | Chênh F1 chỉ 0.0007–0.0009 (RF: FP 1 vs 3; XGB: FP 4 vs 7), một lần chia dữ liệu; XGB-ADASYN còn có ROC-AUC cao hơn (0.9994 vs 0.9993) | "nhỉnh hơn nhẹ (ít cảnh báo nhầm hơn)" |
| B9 | 9 | "Accuracy Paradox: dự đoán toàn 'Hợp lệ' vẫn đạt Accuracy 99.87%" | Đúng với PaySim gốc; trên **tập Test của nhóm** (4.11% fraud) mốc đó là **95.89%** (38,357/40,000) | Ghi rõ "trên PaySim gốc" |
| B10 | 7 | "tài khoản rác (mule account) hoặc luân chuyển rửa tiền đa tầng" | Diễn giải không kiểm chứng trên dữ liệu **mô phỏng**; báo cáo cảnh báo tín hiệu số dư có thể do cơ chế mô phỏng | Thêm "(diễn giải, dữ liệu mô phỏng)" |
| B11 | 20 | "**Superior** Benchmark: F1 = 99.73%" | RF vs XGB chỉ khác nhau 3 mẫu FP trên 40,000; báo cáo (mục 4.8) nêu chỉ có 1 lần chia dữ liệu, không có ước lượng phương sai | "Benchmark: F1 = 99.73% (RF-SMOTENC)" |
| B12 | 15 | Autoencoder "hy sinh Precision ... **phòng ngừa triệt để** tổn thất" | Vẫn bỏ sót 407/1,643 ca (24.8%) | "nhằm giảm bỏ sót" |
| B13 | 14, 4 | Nêu chỉ số "PR-AUC" làm chỉ số chính | Bảng Slide 15 không có cột PR-AUC (`model_comparison.csv` có: RF 0.9983, XGB 0.9969, AE 0.5973) | Thêm cột PR-AUC vào bảng Slide 15 |
| B14 | 12, 13 | Khung XGBoost không nêu tham số; Autoencoder không nói cách cài | XGB: n_estimators 300, max_depth 8, learning_rate 0.2. Autoencoder cài bằng `sklearn MLPRegressor` (ReLU, Adam, 200 epoch, train trên 122,744 giao dịch hợp lệ) vì TensorFlow không có bản cho Python 3.14. Báo cáo có nêu; nếu thầy hỏi "Deep" sẽ bị bất ngờ | Thêm 1 dòng chú thích mỗi khung |

---

## 4. NHÓM C — LỖI NHỎ

- **Slide 4:** "~1 trên 800 giao dịch"; chính xác 6,362,620 / 8,213 = **1 trên 775**.
- **Slide 5:** "step 1..744"; dữ liệu là **1..743** (kiểm trên dữ liệu đã xử lý: min 1, max 743).
- **Slide 1:** "Phạm **Thanh** Trung"; toàn repo (báo cáo, AGENTS.md, script) ghi "Phạm **Thành** Trung". Cần xác nhận tên chuẩn.
- **Tên đặc trưng** (Slide 8, 17, script): `drain_flag`, `is_overnight`, `hour` khác code/báo cáo: `is_drain_account`, `is_night_transaction`, `hour_of_day`.
- **Slide 16:** hình ma trận và số **đúng**; chỉ sửa chữ ở A12, A15.
- **AGENTS.md** (dòng 57, 250): "XGBoost train 41.6s" mâu thuẫn `xgb_smote_summary.txt` (57.94s). Cập nhật cùng A7.
- **Script toàn team** (`SCRIPT_THUYET_TRINH_TOAN_TEAM_CS106.md` trên main) còn các lỗi tương ứng: "100 cây" (A5), "0.13%" (A2), "70%" (A16), "28.5 lần" (A7), Q&A 4 (A18), "công khai trên GitHub" (A1), "Precision 99.88%..."; cần cập nhật sau khi sửa slide. Ngoài ra bản script rút gọn của Thanh (`docs/update-thanh-presentation-script`) và script HTML của Sơn (`docs/hoang-son-presentation-script-html`) **chưa được merge vào main**.
- **Gói nộp bài:** file PPTX hiện 77.7 MB (kèm clip demo); cần tính vào dung lượng gói ZIP.

---

## 5. ĐÃ KIỂM CHỨNG ĐÚNG — KHÔNG CẦN SỬA

| Slide | Nội dung | Kết quả |
|---|---|---|
| 1, 2 | Tên, MSSV, GVHD, mục lục 5 phần | Khớp AGENTS.md (trừ chính tả "Thanh/Thành") |
| 4, 5 | 8,213 ca gian lận trên 6.36M; IR ≈ 0.13% (0.1291%); mẫu 200,000, bảo toàn 100% fraud | Đúng (báo cáo Bảng 3.4) |
| 5, 7 | 100% gian lận ở TRANSFER (4,097) và CASH_OUT (4,116); PAYMENT/CASH_IN/DEBIT = 0 | Đúng (báo cáo Bảng 3.3) |
| 5 | "11 → 14 đặc trưng" | Đúng |
| 7 | Cờ rút cạn 97.56% | Gần đúng: **97.55%** (8,012/8,213) |
| 8 | Công thức `errorBalanceOrig`, `errorBalanceDest`, `drain_flag`, `hour = step % 24`, đêm = 0–5h | Khớp code `feature_scaler.py` |
| 9 | Công thức SMOTE `x_new = x_i + λ(x_zi − x_i)`, trọng số ADASYN `Γ_i = r_i/Σr_i`; SMOTE đạt F1 99.73% với 1 FP | Đúng |
| 11 | Split 80/20 stratified trước resampling; scaler chỉ fit trên Train; Test N = 40,000 | Đúng |
| 12 | Công thức Gini, `Obj^(t)`, `Ω = γT + ½λΣw²`; RF Precision 99.94%, 1 FP/38,357; XGB F1 99.63% | Đúng |
| 13 | `L_rec = (1/d)Σ(x_j − x_recon,j)²`, d = 14; τ = 0.0455 là phân vị 95 sai số giao dịch hợp lệ (validation); Recall 75.23%; chỉ train trên giao dịch hợp lệ | Đúng; khớp code `np.mean(np.square(...), axis=1)` |
| 15 | Hàng RF-SMOTE, XGB-SMOTE, XGB-ADASYN (P/R/F1); Recall Autoencoder; thời gian RF-SMOTE 1187s; biểu đồ cột | Khớp `model_comparison.csv` |
| 16 | TP/FP/FN/TN của RF-SMOTE (1635/1/8/38356), XGB-SMOTE (1635/4/8/38353), Autoencoder (1236/1998/407/36359) và hình 3 ma trận | Khớp tính lại từ pkl |
| 17 | errorBalanceOrig 49.9%, newbalanceOrig 47.2%; hình bar chart Top 8 | Khớp csv |
| 18 | Hàng 95th (số Test); "hợp lệ tập trung < 0.02" | Đúng |
| 20 | Mẫu hợp lệ "Safe < 0.1%" | Đúng: **0.004%** |
| 20 | F1 99.73%, Recall 99.51%, "bỏ sót 8 ca"; hướng phát triển GNN/Kafka/XAI | Đúng / hợp lý |
| 21 | Trích dẫn PaySim (EMSS 2016, tr. 249–255), XGBoost (KDD 2016, tr. 785–794), SMOTE (JAIR 16, tr. 321–357, 2002) | Đúng thông tin thư mục |

---

## 6. VIỆC THEO TỪNG NGƯỜI

| Người | Slide | Việc cần làm |
|---|---|---|
| **Hôn** | 1, 2, 21 | **A1 (chuyển repo Public hoặc đổi chữ)**; tên "Thành/Thanh"; tổng hợp sửa PPTX; đồng bộ script toàn team; merge 2 nhánh script |
| **Thanh** | 3–8 | A3 (Slide 4), A4 (Slide 6, 8), A11 (Slide 8), A16, A17, B4, B9, B10; C: 1/775, step 1..743 |
| **Sơn** | 9–12 (RF) | **A2, A3, A4 (Slide 11)**, **A5**, B6, B7, B8 |
| **Cẩm** | 12 (XGB), 13, 18 | A6, A7, A12, A13, A14, A15, B1–B3, B14 (em sẽ cung cấp: số đúng, hình vẽ lại, phép đo) |
| **Khang** | 14–17 | **A8, A9, A10, A11**, A12 (Slide 15), B4, B5, B12, B13 |
| **Trung / Duy** | 19, 20 | **A18**, A15 (banner), A11 (Slide 20), B11; sửa Q&A câu 4 và mô tả kịch bản |

**Quyết định cần thống nhất:**
1. Thời gian train XGBoost: dùng 57.94s / 45.48s hay chạy lại để lấy số mới (em làm được).
2. Latency: dùng "cỡ nửa mili-giây" hay em thêm phép đo có log.
3. Repo: chuyển Public hay đổi chữ trên Slide 21.
4. Cách trình bày rủi ro "đặc trưng số dư" (A11) trong Slide 20.

Em sẵn sàng: chạy lại XGBoost/Autoencoder lấy thời gian có log, đo latency có log, vẽ lại hình Slide 18, cập nhật `AGENTS.md`, và sau khi anh sửa slide sẽ chạy lại toàn bộ phép kiểm ở Phụ lục để xác nhận từng mục.

---

## PHỤ LỤC. Cách kiểm tra lại (chạy trong `draft/fraud-detection/`)

```python
import joblib, numpy as np, pandas as pd
from sklearn.model_selection import train_test_split

# A2: tỷ lệ gian lận Test
y = np.asarray(joblib.load('data/processed/y_test.pkl')).ravel(); print(y.mean(), y.sum(), len(y))   # 0.041075 1643 40000

# A6: kiến trúc Autoencoder
m = joblib.load('models/autoencoder.pkl'); print(m.hidden_layer_sizes, [c.shape for c in m.coefs_])

# A13: sweep ngưỡng trên validation (tách đúng như run_autoencoder.py)
Xtr = joblib.load('data/processed/X_train.pkl'); ytr = joblib.load('data/processed/y_train.pkl')
_, Xv, _, yv = train_test_split(Xtr, ytr, test_size=0.2, random_state=42, stratify=ytr)
a = Xv.to_numpy(dtype=np.float32); ev = np.mean((a - m.predict(a))**2, axis=1); yv = np.asarray(yv).ravel()
print(np.percentile(ev[yv == 0], [90, 95, 99, 99.9]))     # 0.0134 0.0455 0.1240 0.7460

# A8: chỉ số Autoencoder Test
tp, fp, fn = 1236, 1998, 407; print(tp/(tp+fp), tp/(tp+fn), 2*tp/(2*tp+fp+fn))   # 0.38219 0.75228 0.50687

# A9: độ quan trọng XGBoost-SMOTE
print(pd.read_csv('reports/xgb_smote_feature_importance.csv'))

# A12: Autoencoder bắt được bao nhiêu ca XGBoost bỏ sót
xs = np.asarray(joblib.load('reports/xgb_predictions.pkl')['xgb_smote']['y_pred'])
ae = np.asarray(joblib.load('reports/autoencoder_predictions.pkl')['y_pred'])
miss = np.where((y == 1) & (xs == 0))[0]; print(miss, ae[miss])                  # 8 ca; AE bắt 1

# A17 và A10: cờ rút cạn
X = pd.concat([Xtr, joblib.load('data/processed/X_test.pkl')]); yy = np.concatenate([np.asarray(ytr).ravel(), y])
print(X.is_drain_account[yy == 1].mean())                                        # 0.9755
print(joblib.load('data/processed/X_test.pkl').is_drain_account[y == 0].mean())  # 0.4295

# A18: 3 mẫu demo qua model thật
import sys; sys.path.insert(0, 'demo'); import inference as inf; from pathlib import Path
sc = joblib.load('models/scaler.pkl'); mdl = inf.load_xgboost_model(Path('models/xgb_smote.json'))
safe = dict(transaction_type='TRANSFER', step=120, amount=250000., old_balance_origin=1e6, new_balance_origin=750000., old_balance_destination=5e5, new_balance_destination=750000.)
print(inf.predict_transaction(safe, sc, mdl).fraud_probability)                  # ~0.00004
```

```bash
# Số "không nguồn" (A7, A8, A13): chỉ trả về file sinh slide và các file báo cáo này
grep -rIl -E "41\.7|43\.2|68\.4|0\.0211|0\.2104" . --exclude-dir=.git
# A1: trạng thái repo
gh repo view uit-25730067-chithanh/CS106-Team09-Fraud-Detection --json visibility     # PRIVATE
```

**Cấu hình đo độ trễ (A15):** xgboost 3.4.1, Windows 11, CPU Intel64 Family 6 Model 151 (12 luồng), Python 3.12; 2,000 lần gọi sau 50 lần khởi động. Kết quả phụ thuộc máy.
