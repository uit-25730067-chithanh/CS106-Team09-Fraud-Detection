# KỊCH BẢN THUYẾT TRÌNH BÁO CÁO ĐỒ ÁN CS106 (VĂN NÓI CHUẨN PHÂN CÔNG FINAL)

## Đề tài: Hệ Thống Phát Hiện Gian Lận Tài Chính Trên Dữ Liệu PaySim Bằng Machine Learning & Deep Learning

**Môn học:** CS106 - Trí tuệ Nhân tạo | **GVHD:** PGS.TS. Nguyễn Đình Hiển
**Phiên bản:** Hiệu chỉnh theo khung thời gian 10 phút (Meeting Dry-Run 18/09/2026)

---

> ⏱️ **KẾT QUẢ ĐO ĐẠC & HIỆU CHỈNH THỜI LƯỢNG THỰC TẾ (MỤC TIÊU 10 PHÚT / 600 GIÂY):**
> - **Thời lượng quy định mới:** Thầy thông báo thời gian báo cáo chính thức được rút gọn còn **10 phút (600 giây)**.
> - **Tốc độ nói thực tế (Empirical WPM - Words Per Minute):**
>   - **Đặng Chí Thanh:** **186.2 WPM** (~3.10 từ/giây) — *Tốc độ nói nhanh nhất nhóm, diễn giải sâu và nhiều số liệu*.
>   - **Trần Hoàng Hôn:** **156.4 WPM** (~2.61 từ/giây) — *Phong thái tự nhiên, mở đầu dứt khoát*.
>   - **Hoàng Cao Sơn:** **152.3 WPM** (~2.54 từ/giây) — *Tốc độ đều, phân tích sâu cơ chế SMOTENC và 4 nguyên tắc Leak-Free*.
>   - **Phạm Thành Trung:** **147.0 WPM** (~2.45 từ/giây) — *Dẫn nhập và chốt kết quả sau phần trình diễn Video Demo*.
>   - **Bùi Thị Mỷ Cẩm:** **135.5 WPM** (~2.26 từ/giây) — *Giọng rõ ràng, chuẩn mực kỹ thuật, trình bày XGBoost, Autoencoder và phân vị ngưỡng*.
>   - **Nguyễn Duy Khang:** **119.8 WPM** (~2.00 từ/giây) — *Nhịp nói điềm đạm, nhấn mạnh rành mạch đối chuẩn mô hình và Feature Importance*.
>   - **Vũ Văn Duy:** *Trụ cột phản biện Q&A chuyên sâu (0s trên slide để tối ưu thời lượng toàn team)*.
> - **Chiến lược tối ưu 10 phút (Hard Mode):**
>   - **Giữ nguyên Video Demo thực nghiệm 2m17s** (137s) trên Slide 20 theo chuẩn yêu cầu đồ án.
>   - **Lướt qua các slide tiêu đề chuyển phần (Slide 3, 6, 10, 14, 19)** trong 1–2 giây (0s thuyết minh).
>   - **Cô đọng tối đa lời thoại của 5 người nói**: Hôn (1m05s), Thanh (2m10s), Sơn (1m20s), Cẩm (1m30s), Khang (1m10s), Demo + Trung kết bài (2m30s), Buffer chuyển slide/micro (15s) = **Đúng 10 phút 00 giây (600s)**.

## ⏱️ BẢNG ĐỐI CHIẾU THỜI GIAN THEO MỤC TIÊU 10 PHÚT (600 GIÂY)

| STT | Thành viên | Slide phụ trách | Tình trạng kịch bản | Nội dung chính phụ trách | Thời gian Mục tiêu 10p (Target Budget) | Thời gian Kịch bản chuẩn hóa (Script Time) | Thực tế chạy thử Dry-run (18/09) | Chênh lệch (Kịch bản vs Mục tiêu 10p) | Mức độ đáp ứng & Khuyến nghị nhịp độ |
| :---: | :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | **Trần Hoàng Hôn** | **Slide 1, 2** | 🟢**Đã tối ưu 10p** | Mở đầu, giới thiệu 7 thành viên kèm nhiệm vụ cốt lõi và 5 phần lộ trình báo cáo. | **1 phút 05s** *(65s)* | **1 phút 05s** *(~170 từ)* | *3 phút 16s* | 🟢**Khớp 100% (0s)** | ✅**BÁM SÁT SLIDE:** Giới thiệu rõ ràng tên và vai trò từng bạn (do slide chỉ hiện tên và MSSV) và 5 phần lộ trình. |
| **2** | **Đặng Chí Thanh** | **Slide 3, 4, 5, 6, 7, 8** | 🟢**Đã tối ưu 10p** | 3 thách thức kỹ thuật, PaySim 200k (100% ở 2 loại), 3 dấu vết hành vi và 14 đặc trưng miền (97.1%). | **2 phút 10s** *(130s)* | **2 phút 10s** *(~340 từ)* | *7 phút 54s* | 🟢**Khớp 100% (0s)** | ✅**ĐẠT CHUẨN 10P:** Lướt 2 slide tiêu đề, cô đọng 4 slide kỹ thuật ~30–35s/slide, bảo toàn 100% số liệu đắt giá. |
| **3** | **Hoàng Cao Sơn** | **Slide 9, 10, 11, 12 (RF)** | 🟢**Đã tối ưu 10p** | Nghịch lý Accuracy, SMOTENC 230k dòng, 4 chốt chặn Leak-Free và Random Forest F1 99.73%. | **1 phút 20s** *(80s)* | **1 phút 20s** *(~200 từ)* | *7 phút 17s* | 🟢**Khớp 100% (0s)** | ✅**ĐẠT CHUẨN 10P:** Lướt slide 10, tập trung SMOTENC giữ cờ 0/1, 4 chốt chặn Leak-Free và đỉnh cao F1 99.73%. |
| **4** | **Bùi Thị Mỷ Cẩm** | **Slide 12 (XGB), 13, 18** | 🟢**Đã tối ưu 10p** | XGBoost 57.94s (nhanh gấp 20 lần), Deep Autoencoder Recall 75.2% và Ngưỡng Anomaly τ=0.0455 (phân vị 95th). | **1 phút 30s** *(90s)* | **1 phút 30s** *(~215 từ)* | *4 phút 15s* | 🟢**Khớp 100% (0s)** | ✅**ĐẠT CHUẨN 10P:** Nêu bật XGBoost siêu tốc cho Demo, cơ chế sai số MSE Autoencoder và điểm cắt ngưỡng tối ưu. |
| **5** | **Nguyễn Duy Khang** | **Slide 14, 15, 16, 17** | 🟢**Đã tối ưu 10p** | Đối chuẩn 5 mô hình (RF/XGB F1>99.6%), Ma trận nhầm lẫn (chỉ sót 8 ca) và Độ quan trọng đặc trưng (Top 2 đạt 97%). | **1 phút 10s** *(70s)* | **1 phút 10s** *(~170 từ)* | *4 phút 27s* | 🟢**Khớp 100% (0s)** | ✅**ĐẠT CHUẨN 10P:** Lướt slide 14, đi thẳng vào bảng so sánh, ma trận nhầm lẫn chỉ sót 8 ca và chốt 97% từ 2 biến số dư. |
| **6** | **Vũ Văn Duy** | *Không nói Slide* | 🟢**Đã cập nhật** *(0s)* | **Chuyên trách phản biện:** Trụ cột trả lời Q&A về Báo cáo Word 31 trang & phương pháp luận học thuật. | **0s** | **0s** | *2 phút 29s* | 🟢**0s (Khớp tuyệt đối)** | 🎯**TẬP TRUNG TRẢ LỜI CÂU HỎI:** Duy không nói slide, triệt tiêu độ trễ chuyển đổi micro. |
| **7** | **Phạm Thành Trung** | **Slide 20 + Cảm ơn** | 🟢**Đã tối ưu 10p** | Dẫn nhập (8s), Trình diễn Demo thực nghiệm (2m17s), 4 đóng góp cốt lõi và Cảm ơn (15s). | **2 phút 30s** *(150s)* | **2 phút 30s** *(Demo 137s + nói 13s)* | *5 phút 04s* | 🟢**Khớp 100% (0s)** | ✅**DEMO THỰC NGHIỆM ĐỈNH CAO:** Giữ trọn 2m17s demo video minh chứng thực nghiệm, dẫn nhập 8s và chốt kết bài 13s. |
| ⏩ | **Slide 21** | *Bỏ qua* | 🟢**Đã cập nhật** | Slide phông nền tĩnh chiếu mã nguồn, tài liệu tham khảo và mở phiên hỏi đáp Q&A. | **0s** | **0s** | *45s* | 🟢**0s (Khớp tuyệt đối)** | 🎯**TIẾT KIỆM THỜI GIAN:** Không thuyết minh, chuyển slide làm phông nền khi bắt đầu Q&A. |
| ⏱️ | **Dự phòng (Buffer)** | — | — | Độ trễ chuyển slide giữa các phần và kết nối micro giữa các thành viên. | **15s** | **15s** | — | 🟢**Khớp (15s)** | Dành cho việc chuyển giao micro và chuyển trang màn hình. |
| 🏁 | **TỔNG TOÀN BÀI** | **21 Slides** | **7/7 thành viên sẵn sàng** | **6 thành viên thuyết trình + Video Demo thực nghiệm (Duy trụ cột phản biện Q&A)** | **10 phút 00s** *(600s)* | **10 phút 00s** *(Thuần nói 448s + Demo 137s + Buffer 15s)* | *~35m02s* | 🟢**KHỚP CHUẨN HOÀN TOÀN 10 PHÚT** | 🎯**KỊCH BẢN TỐI ƯU CỰC HẠN CHO KHUNG THỜI GIAN 10 PHÚT CHÍNH XÁC.** |

# LỜI THOẠI VĂN NÓI CHI TIẾT THEO TỪNG SLIDE

---

### SLIDE 1 – TRANG TIÊU ĐỀ & GIỚI THIỆU THÀNH VIÊN

_(Thời lượng chuẩn hóa: **~45s** [~120 từ] | Người nói: **Trần Hoàng Hôn** - PM / Trưởng nhóm)_

Em chào Thầy và các bạn!

Em là **Trần Hoàng Hôn**, đại diện **Nhóm 09** báo cáo đề tài: **"Hệ thống phát hiện gian lận tài chính trên dữ liệu giao dịch PaySim bằng Machine Learning và Deep Learning"**.

Nhóm em gồm **7 thành viên**:
- Bạn **Đặng Chí Thanh** — phụ trách thu thập dữ liệu, EDA, tiền xử lý và trích xuất 14 đặc trưng miền.
- Bạn **Hoàng Cao Sơn** — phụ trách xử lý mất cân bằng và huấn luyện mô hình Random Forest.
- Bạn **Bùi Thị Mỷ Cẩm** — phụ trách huấn luyện mô hình XGBoost và Deep Autoencoder.
- Bạn **Nguyễn Duy Khang** — phụ trách kiểm thử độc lập và đối chuẩn đa chỉ số.
- Anh **Vũ Văn Duy** — phụ trách biên soạn báo cáo khoa học và phản biện học thuật.
- Bạn **Phạm Thành Trung** — phụ trách thiết kế Dashboard Streamlit và thực hiện Demo.
- Và em — **Trần Hoàng Hôn**, quản lý tiến độ dự án, thiết kế slide và đóng gói sản phẩm.

Sau đây, em xin phép bắt đầu buổi báo cáo ạ.

---

### SLIDE 2 – NỘI DUNG BÁO CÁO & LỘ TRÌNH (AGENDA)

_(Thời lượng chuẩn hóa: **~20s** [~50 từ] | Người nói: **Trần Hoàng Hôn**)_

Bài báo cáo của nhóm sẽ đi qua **5 phần chính**:
- **Phần 1**: Giới thiệu & Phát biểu bài toán, bối cảnh Mobile Money và 3 thách thức kỹ thuật.
- **Phần 2**: Phân tích khám phá dữ liệu & Kỹ thuật 14 đặc trưng miền.
- **Phần 3**: Phương pháp đề xuất & Kiến trúc Pipeline chuẩn Leak-Free.
- **Phần 4**: Kết quả thực nghiệm & Đánh giá so sánh đa chỉ số.
- **Phần 5**: Hệ thống Demo thời gian thực & Định hướng tương lai.

Sau đây, em xin nhường lời cho bạn **Đặng Chí Thanh** bắt đầu với 2 phần đầu tiên ạ. Mời Thanh!

---

### SLIDE 3 – PHẦN 1: TỔNG QUAN ĐỀ TÀI & DỮ LIỆU

_(Trạng thái: **SLIDE TIÊU ĐỀ PHẦN 1** — Lướt qua trong 1–2 giây để vào thẳng Slide 4, không dừng lại nói thoại để tối ưu thời lượng 10 phút | Phụ trách: **Đặng Chí Thanh**)_

---

### SLIDE 4 – ĐỘNG LỰC NGHIÊN CỨU & THÁCH THỨC KỸ THUẬT

_(Thời lượng chuẩn hóa: **~35s** [~110 từ] | Người nói: **Đặng Chí Thanh**)_

Em chào Thầy và các bạn! Trong các giao dịch ví điện tử Mobile Money, kẻ gian có thể tẩu tán tiền chỉ trong vài giây. Do đó, hệ thống phòng thủ bắt buộc phải đưa ra quyết định thời gian thực với độ trễ dưới 100 mili-giây.

Về mặt kỹ thuật, nhóm đối mặt với **3 thách thức lớn nhất**:

- **Thứ nhất — Mất cân bằng cực đoan (0.13%)**: Cứ 775 giao dịch bình thường mới có đúng 1 ca gian lận. Thước đo Accuracy bị vô hiệu hóa hoàn toàn, buộc nhóm phải tối ưu **Recall và PR-AUC**.
- **Thứ hai — Tổn thất bất đối xứng**: Bỏ sót gian lận gây mất tiền thật và uy tín, nên chi phí phạt bỏ sót phải cao hơn nhiều so với báo nhầm.
- **Thứ ba — Tính phi tĩnh**: Thủ đoạn luân chuyển tiền của kẻ gian liên tục biến đổi tinh vi.

---

### SLIDE 5 – TẬP DỮ LIỆU PAYSIM: THUỘC TÍNH THỐNG KÊ

_(Thời lượng chuẩn hóa: **~35s** [~105 từ] | Người nói: **Đặng Chí Thanh**)_

Để thực nghiệm, nhóm sử dụng bộ dữ liệu mô phỏng chuẩn học thuật **PaySim** với hơn 6.36 triệu giao dịch. Nhóm thực hiện lấy mẫu phân tầng **200,000 sự kiện**, nhưng **bảo toàn nguyên vẹn 100% toàn bộ 8,213 ca gian lận gốc**.

Đặc biệt, qua phân tích phân bố, nhóm phát hiện một quy luật đắt giá: **100% tất cả các ca gian lận CHỈ xảy ra ở đúng 2 loại giao dịch: TRANSFER (chuyển khoản) và CASH_OUT (rút tiền mặt)**. 

Nhờ insight này, bước lọc chỉ giữ 2 loại trên đã giúp loại bỏ ngay **~56.5%** giao dịch an toàn không có gian lận, tối ưu vượt bậc tài nguyên tính toán cho toàn bộ pipeline phía sau.

---

### SLIDE 6 – PHẦN 2: TIỀN XỬ LÝ & KỸ THUẬT ĐẶC TRƯNG

_(Trạng thái: **SLIDE TIÊU ĐỀ PHẦN 2** — Lướt qua trong 1–2 giây để vào thẳng Slide 7, không dừng lại nói thoại | Phụ trách: **Đặng Chí Thanh**)_

---

### SLIDE 7 – PHÂN TÍCH KHÁM PHÁ DỮ LIỆU: DẤU VẾT HÀNH VI CỐT LÕI

_(Thời lượng chuẩn hóa: **~30s** [~100 từ] | Người nói: **Đặng Chí Thanh**)_

Khi thực hiện EDA, nhóm đúc kết được **3 dấu vết hành vi cốt lõi của tội phạm**:

- **Thứ nhất — Khoanh vùng dòng tiền**: Kẻ gian dùng lệnh TRANSFER chuyển tiền sang tài khoản trung gian, rồi lập tức CASH_OUT rút tiền mặt ngay để cắt đứt dấu vết.
- **Thứ hai — Vét sạch số dư nguồn**: Trong **97.55%** số vụ gian lận, số dư của nạn nhân bị rút cạn sạch về đúng bằng 0 (`newbalanceOrig == 0`) trong một lần duy nhất.
- **Thứ ba — Sai lệch số dư đích**: Tiền chuyển đi nhưng số dư tài khoản nhận không tăng tương ứng (`newbalanceDest ≈ 0`), vạch trần việc dùng các tài khoản rác (mule accounts).

---

### SLIDE 8 – KỸ THUẬT ĐẶC TRƯNG: 14 THUỘC TÍNH CỐT LÕI

_(Thời lượng chuẩn hóa: **~30s** [~110 từ] | Người nói: **Đặng Chí Thanh**)_

Từ 3 dấu vết trên, nhóm trích xuất **14 đặc trưng miền kế toán chuyên sâu**: gồm sai lệch số dư nguồn (`errorBalanceOrig`), sai lệch số dư đích (`errorBalanceDest`), cờ rút cạn (`drain_flag`) và giao dịch giờ đêm (`is_overnight`).

Đáng chú ý, khi đánh giá mô hình XGBoost, **chỉ riêng 2 biến sai lệch số dư nguồn (49.9%) và số dư sau giao dịch (47.2%) đã giải thích tới 97.1% tổng Feature Split Gains!** Nhóm cũng nhìn nhận khách quan đây là phát hiện mạnh nhưng có rủi ro simulator artifact theo Mục 3.6.2 của báo cáo.

Sau đây, em xin chuyển phần trình bày cho bạn **Hoàng Cao Sơn** với nội dung xử lý mất cân bằng và Random Forest ạ.

---

### SLIDE 9 – XỬ LÝ MẤT CÂN BẰNG LỚP: SMOTE VÀ ADASYN

_(Thời lượng chuẩn hóa: **~30s** [~110 từ] | Người nói: **Hoàng Cao Sơn** - Imbalance & Random Forest Lead)_

Cảm ơn Thanh. Chào Thầy và các bạn, với tỷ lệ gian lận chỉ 0.13%, đây là bài toán mất cân bằng cực đoan. Nếu đoán 100% hợp lệ thì Accuracy vẫn đạt 99.87% nhưng vô giá trị (Accuracy Paradox).

Để cân bằng dữ liệu, nhóm đối chuẩn 2 kỹ thuật:

- **SMOTENC**: Nội suy mẫu nhân tạo dọc theo đoạn nối các láng giềng k-NN, bảo toàn nguyên vẹn giá trị 0-1 của các cờ nhị phân. Nhóm chọn SMOTENC để sinh tập Train cân bằng **230,145 dòng** (tỷ lệ 1:2 tối ưu), triệt tiêu tối đa báo động giả.
- **ADASYN**: Do cố sinh mẫu theo mật độ vùng biên khó, ADASYN sinh mẫu quá đà ở vùng chồng lấn nhiễu, làm tăng nhiều False Positives.

---

### SLIDE 10 – PHẦN 3: PHƯƠNG PHÁP & MÔ HÌNH HỌC MÁY

_(Trạng thái: **SLIDE TIÊU ĐỀ PHẦN 3** — Lướt qua trong 1–2 giây để vào thẳng Slide 11, không dừng lại nói thoại | Phụ trách: **Hoàng Cao Sơn**)_

---

### SLIDE 11 – KIẾN TRÚC PIPELINE CHUẨN LEAK-FREE

_(Thời lượng chuẩn hóa: **~35s** [~95 từ] | Người nói: **Hoàng Cao Sơn**)_

Để đảm bảo tính khách quan tuyệt đối, pipeline 6 bước của nhóm tuân thủ nghiêm ngặt **4 chốt chặn Leak-Free**:

1. **Stratified Split 80/20** chốt chặn đầu tiên trước mọi bước xử lý.
2. **Resampling tuyệt đối chỉ chạy trên tập Train**; tập Test 40,000 mẫu được giữ nguyên 100% tỷ lệ thực tế, không có bất kỳ mẫu nhân tạo nào lọt vào.
3. **StandardScaler chỉ fit trên Train**, sau đó mới transform mù sang Test.
4. **Chọn ngưỡng và dò siêu tham số** hoàn toàn bằng Cross-Validation nội bộ trên Train.

Nhờ 4 nguyên tắc này, kết quả của nhóm hoàn toàn không bị rò rỉ dữ liệu.

---

### SLIDE 12 – MÔ HÌNH GIÁM SÁT: RANDOM FOREST VÀ XGBOOST

_(Thời lượng chuẩn hóa: **~45s** [Sơn ~20s, Cẩm ~25s] | Người nói: **Hoàng Cao Sơn** [RF] & **Bùi Thị Mỷ Cẩm** [XGB])_

_(Phần 1 - Random Forest: **Hoàng Cao Sơn** trình bày - ~20s)_

Ở khung bên trái là mô hình **Random Forest** gồm **200 cây quyết định**, khống chế max_depth = 20 để chống Overfitting. 

Mô hình đạt kết quả ấn tượng: **Precision đạt 99.94%** (trên 38,357 giao dịch hợp lệ chỉ báo nhầm đúng 1 ca!), và **F1-Score đạt 99.73%** — cao nhất toàn đồ án. Tuy nhiên, thời gian huấn luyện mất gần **20 phút** (~1,187 giây). Sau đây, bạn **Bùi Thị Mỷ Cẩm** sẽ trình bày về giải pháp tốc độ với XGBoost ạ.

---

_(Phần 2 - XGBoost: **Bùi Thị Mỷ Cẩm** tiếp lời — ~25s)_

Dạ em cảm ơn anh Sơn! Em chào Thầy và các bạn!

Ở khung bên phải, **XGBoost** giải quyết triệt để bài toán tốc độ triển khai:

- Mô hình đạt **F1-Score 99.63%**, tương đương Random Forest.
- Nhưng thời gian huấn luyện chỉ **57.94 giây**, tức là **nhanh hơn 20 lần**!
- Độ trễ suy luận chỉ **nửa mili-giây** cho mỗi giao dịch trên CPU. Do đó, nhóm chọn XGBoost làm động cơ suy luận chính cho hệ thống demo thực tế.

---

### SLIDE 13 – MÔ HÌNH KHÔNG GIÁM SÁT: DEEP AUTOENCODER

_(Thời lượng chuẩn hóa: **~35s** [~115 từ] | Người nói: **Bùi Thị Mỷ Cẩm** - Modeling XGB & Autoencoder Lead)_

Để phát hiện các thủ đoạn gian lận mới chưa từng có nhãn, em phát triển mạng **Deep Autoencoder** theo hướng **học không giám sát (Unsupervised)**:

- **Cấu trúc mạng:** Gồm 5 lớp ẩn đối xứng 14 → 16 → 8 → 4 → 8 → 16 → 14. Nút cổ chai 4 chiều hẹp buộc mạng phải nén và học bản chất dòng tiền an toàn.
- **Cơ chế:** Mạng chỉ học trên giao dịch hợp lệ. Khi gặp giao dịch gian lận dị biệt, sai số tái tạo MSE sẽ tăng vọt và bị gắn cờ cảnh báo.
- **Hiệu năng:** Dù hoàn toàn không dùng nhãn khi huấn luyện, Autoencoder vẫn đạt **Recall 75.23%** (bắt trúng 1,236 ca gian lận), đóng vai trò lớp phòng thủ thứ hai (**Defense-in-Depth**) để chuyển chuyên viên rà soát.

Sau đây, em xin mời bạn **Khang** trình bày bảng so sánh đối chuẩn giữa các mô hình ạ.

---

### SLIDE 14 – PHẦN 4: KẾT QUẢ THỰC NGHIỆM & PHÂN TÍCH

_(Trạng thái: **SLIDE TIÊU ĐỀ PHẦN 4** — Lướt qua trong 1–2 giây để vào thẳng Slide 15, không dừng lại nói thoại | Phụ trách: **Nguyễn Duy Khang**)_

---

### SLIDE 15 – KẾT QUẢ THỰC NGHIỆM: BẢNG SO SÁNH ĐA CHỈ SỐ

_(Thời lượng chuẩn hóa: **~25s** [~70 từ] | Người nói: **Nguyễn Duy Khang** - Evaluation & Metrics Lead)_

Em chào Thầy và các bạn! Nhìn vào bảng đối chuẩn đa chỉ số, cả hai mô hình cây là **Random Forest** và **XGBoost** đều đạt F1-Score vượt trội trên **99.6%**, bắt trọn gần như toàn bộ gian lận. Điểm khác biệt mấu chốt là XGBoost huấn luyện chưa tới 1 phút, nhanh hơn Random Forest tới 20 lần.

Còn **Autoencoder** học không cần nhãn vẫn đạt Recall **75.23%**. Mô hình chủ động chấp nhận Precision khoảng 38% để đổi lấy độ bao phủ cao: *"Thà cảnh báo nhầm để xác thực thêm OTP, còn hơn bỏ lọt tội phạm tài chính"*.

---

### SLIDE 16 – PHÂN TÍCH MA TRẬN NHẦM LẪN & ĐÁNH ĐỔI SAI SỐ

_(Thời lượng chuẩn hóa: **~25s** [~70 từ] | Người nói: **Nguyễn Duy Khang**)_

Đi sâu vào **Ma trận nhầm lẫn** trên 40,000 mẫu kiểm thử độc lập:

- Cả **Random Forest** và **XGBoost** đều bắt trúng **1,635 trên 1,643 vụ** gian lận thật, chỉ để lọt duy nhất **8 ca**. Trên 38,000 giao dịch bình thường, Random Forest chỉ báo nhầm 1 ca, còn XGBoost chỉ báo nhầm 4 ca.
- **Autoencoder** bắt được **1,236 vụ** mà không cần nhãn, đóng vai trò màng lọc thứ cấp, chấp nhận báo nhầm khoảng 5% giao dịch hợp lệ để chuyển sang bước kiểm tra thứ hai.

---

### SLIDE 17 – PHÂN TÍCH ĐÓNG GÓP ĐẶC TRƯNG (FEATURE IMPORTANCE)

_(Thời lượng chuẩn hóa: **~25s** [~85 từ] | Người nói: **Nguyễn Duy Khang**)_

Về **Độ quan trọng đặc trưng**: Biểu đồ bên phải chỉ ra rằng 2 đặc trưng đứng đầu là sai lệch số dư nguồn (`errorBalanceOrig`, ~50%) và số dư sau giao dịch (`newbalanceOrig`, ~47%). 

Gộp lại, riêng 2 biến này đã chiếm tới **97.1%** tổng Feature Split Gains, chứng minh mô hình bám rất chặt vào dấu vết rút cạn ví. Nhóm cũng ghi nhận đây là rủi ro simulator artifact của tập dữ liệu PaySim.

Tiếp theo, em xin mời chị **Mỷ Cẩm** giải thích phần xác định ngưỡng Anomaly của mô hình Autoencoder ạ.

---

### SLIDE 18 – PHÂN BỐ SAI SỐ TÁI TẠO & NGƯỠNG ANOMALY

_(Thời lượng chuẩn hóa: **~35s** [~110 từ] | Người nói: **Bùi Thị Mỷ Cẩm**)_

Dạ em cảm ơn bạn Khang. Đây là quyết định kỹ thuật then chốt của Autoencoder: **Xác định ngưỡng cắt dị biệt τ (Anomaly Cutoff)**:

- **Phân bố sai số:** Hơn 92% giao dịch hợp lệ có sai số MSE rất thấp dưới 0.02, trong khi gian lận có sai số phân tán cao.
- **Chiến lược chọn ngưỡng:** Để đảm bảo Leak-Free, nhóm quét ngưỡng trên tập Validation với ràng buộc tiên quyết **Recall tối thiểu ≥ 60%** (vì bỏ sót gian lận đắt hơn nhiều so với báo nhầm).
- **Điểm cắt tối ưu:** Trong các ngưỡng thỏa mãn, **phân vị 95th (τ = 0.0455)** cho F1 cao nhất. Khi kiểm định mù trên tập Test độc lập, ngưỡng này mang lại **Recall 75.23%** và **Precision 38.22%**.

Tiếp theo, em xin mời bạn **Trung** trình diễn hệ thống Demo thực tế ạ. Mời anh Trung!

---

### SLIDE 19 – PHẦN 5: DEMO HỆ THỐNG & KẾT LUẬN

_(Trạng thái: **SLIDE BÌA CHUYỂN MỤC** — Người chuyển slide lướt qua Slide 19 trong 1–2 giây để vào thẳng Slide 20, không dừng lại nói thoại để tiết kiệm thời lượng)_

---

### SLIDE 20 – HỆ THỐNG DEMO STREAMLIT & ĐÓNG GÓP CỐT LÕI

_(Thời lượng chuẩn hóa: **~2 phút 35s** [Trung dẫn nhập ~8s, Trình diễn Demo thực nghiệm 2m17s, Tổng kết 4 đóng góp & Cảm ơn ~15s] | Người nói: **Phạm Thành Trung** [Phụ trách toàn bộ Slide 20 & Kết bài])_

Dạ em cảm ơn bạn Cẩm! Em chào Thầy và các bạn!

Sau đây, em xin trình diễn hệ thống **Dashboard giám sát gian lận thời gian thực xây dựng trên nền tảng Streamlit**, tích hợp trực tiếp mô hình XGBoost-SMOTE đã huấn luyện. Xin mời Thầy và các bạn cùng theo dõi!

---

#### 🔹 PHẦN 1: TRÌNH DIỄN DEMO TRÊN SLIDE 20 (~2 phút 17 giây)

*(Phạm Thành Trung kích hoạt phần trình diễn demo trực tiếp trên Slide 20 của PowerPoint. Bản demo mô phỏng 3 kịch bản kiểm thử thực tế và dừng lại ở kết quả cảnh báo gian lận).*

---

#### 🔹 PHẦN 2: TIẾP NỐI SAU DEMO – TỔNG KẾT ĐÓNG GÓP & KẾT BÀI (~15s)

*(Ngay khi phần demo kết thúc... Trung cầm micro tiếp lời)*

Dạ qua demo thực tế, mô hình XGBoost đã bắt trọn dấu hiệu rút cạn ví ở kịch bản rủi ro cao với xác suất 88.36% và độ trễ dưới 0.5 mili-giây.

Đồ án mang lại **4 đóng góp kỹ thuật cốt lõi**:

1. **Pipeline chuẩn Leak-Free 100%**, phân lập triệt để dữ liệu kiểm thử.
2. **Kỹ thuật 14 đặc trưng miền kế toán**, trong đó Top 2 đặc trưng số dư giải thích **97.1%** split gains.
3. **Hiệu năng vượt trội:** **F1-Score 99.73%** (Random Forest) và mô hình triển khai **XGBoost 57.94s** siêu tốc (nhanh hơn ~20 lần).
4. **Phòng thủ đa tầng**, kết hợp Deep Autoencoder phát hiện bất thường không cần nhãn (Recall 75.23%).

---

### SLIDE 21 – TỔNG KẾT, TÀI LIỆU THAM KHẢO & PHIÊN HỎI ĐÁP (Q&A)

_(Trạng thái: **SLIDE DỰ BỊ / PHÔNG NỀN Q&A** | Người nói: **Phạm Thành Trung**)_

Toàn bộ mã nguồn, dữ liệu thực nghiệm, báo cáo Word và slide đã được nhóm đóng gói đầy đủ trên repository của đồ án.

Thay mặt Nhóm 09, em xin chân thành cảm ơn Thầy và các bạn đã chú ý lắng nghe phần trình bày của nhóm ạ!

---

# 🛡️ BỘ CÂU HỎI PHẢN BIỆN DỰ BỊ DÀNH CHO NHÓM (Q&A DEFENSE)

### ❓ Câu 1: "Điểm F1 > 99.6% cao bất thường như vậy có chắc chắn là không bị rò rỉ dữ liệu (Data Leakage) không?"

> **Người trả lời chính:** **Đặng Chí Thanh** _(EDA & Preprocessing)_  
> **Hướng trả lời:**  
> "Dạ thưa thầy, nhóm em đã kiểm soát rất chặt nguy cơ rò rỉ dữ liệu qua 4 chốt chặn Leak-Free nghiêm ngặt:
>
> 1. Tập Test độc lập (20%) được tách riêng đầu tiên trước mọi bước xử lý.
> 2. SMOTENC chỉ chạy trên 80% tập Train. Tập Test hoàn toàn giữ nguyên phân bố sau downsample (4.11% fraud, 1,643 ca) và tuyệt đối không có mẫu nhân tạo nào.
> 3. StandardScaler chỉ fit trên Train và transform mù trên Test.
> 4. Toàn bộ quá trình chọn ngưỡng và tinh chỉnh tham số đều dùng 5-Fold Cross Validation nội bộ trên Train.
>    Điểm số cao thực chất là nhờ đặc trưng dẫn xuất errorBalanceOrig và cột gốc newbalanceOrig đã giải thích đúng bản chất kế toán của hành vi gian lận (chiếm 97.1% split gains). Nhóm cũng nhìn nhận khách quan đây là phát hiện mạnh trên PaySim nhưng cũng đi kèm rủi ro simulator artifact như Báo cáo Mục 3.6.2 đã phân tích sâu ạ."

---

### ❓ Câu 2: "Tại sao nhóm lại ưu tiên dùng XGBoost cho thực tế thay vì Random Forest?"

> **Người trả lời chính:** **Bùi Thị Mỷ Cẩm / Hoàng Cao Sơn**
> **Hướng trả lời:**
> "Dạ thưa thầy, về chất lượng phân loại thì 2 mô hình tương đương nhau (F1 99.73% so với 99.63%, chỉ chênh 3 ca đoán nhầm trên 40,000 mẫu). Nhưng Random Forest mất gần 20 phút để huấn luyện, còn XGBoost chưa tới một phút, nhanh hơn hơn 20 lần, và độ trễ suy luận cỡ nửa mili-giây cho một giao dịch. Với cổng thanh toán cần xử lý thời gian thực thì XGBoost là lựa chọn phù hợp để triển khai, và cũng là mô hình mà phần demo dùng để chấm điểm trực tiếp ạ."

---

### ❓ Câu 3: "Autoencoder có Precision thấp (38.2%) thì có giá trị gì trong thực tế?"

> **Người trả lời chính:** **Bùi Thị Mỷ Cẩm / Nguyễn Duy Khang**
> **Hướng trả lời:**
> "Dạ thưa thầy, Deep Autoencoder đóng vai trò lớp phòng thủ thứ hai (Defense-in-Depth), không thay thế XGBoost. Precision 38.2% là do em chủ động đặt ngưỡng ở phân vị 95 với ràng buộc Recall tối thiểu 60%, để ưu tiên bắt được nhiều vụ gian lận (Recall 75.2%) vì bỏ sót một vụ gian lận đắt hơn nhiều so với báo nhầm.
> Với vai trò lớp thứ hai, giao dịch bị gắn cờ chỉ bị chuyển sang bước xác thực thêm, ví dụ OTP hoặc chuyên viên rà soát; khoảng 5% giao dịch hợp lệ bị báo nhầm nên chấp nhận Precision thấp là hợp lý. Ưu điểm của Autoencoder là không dùng nhãn khi huấn luyện mạng, nên về nguyên lý không bị giới hạn bởi các kiểu gian lận đã có nhãn. Tuy nhiên nhóm chưa kiểm thử riêng trên biến thể gian lận mới, và trong 8 ca XGBoost bỏ sót thì Autoencoder chỉ bắt thêm được 1 ca ạ."

---

### ❓ Câu 4: "Giao diện Streamlit xử lý dữ liệu lớn như thế nào nếu có file CSV hàng trăm ngàn dòng?"

> **Người trả lời chính:** **Phạm Thành Trung / Vũ Văn Duy**
> **Hướng trả lời:**
> "Dạ thưa thầy, trong phạm vi ứng dụng prototype Streamlit, nhóm tối ưu hiệu năng tương tác bằng hai giải pháp kỹ thuật:
> 1. Sử dụng decorator @st.cache_resource để nạp sẵn trọng số mô hình XGBoost và bộ chuẩn hóa StandardScaler vào bộ nhớ RAM một lần duy nhất, tránh độ trễ nạp lại ở mỗi lượt suy luận.
> 2. Tính toán 14 đặc trưng miền hoàn toàn bằng các phép toán vector hóa của Pandas.
> Bản Demo giao diện hiện tại của nhóm hỗ trợ chức năng 'Nhập dữ liệu mẫu' với các tệp CSV/JSON tối đa 50 giao dịch nhằm phục vụ mục đích kiểm thử trực quan và lưu vết kiểm toán vào SQLite. Còn đối với bài toán sản xuất thực tế khi phải xử lý hàng trăm ngàn giao dịch mỗi ngày, nhóm định hướng tách tầng giao diện khỏi tầng tính toán, triển khai mô hình dưới dạng REST/gRPC API độc lập và kết nối với hàng đợi Apache Kafka hoặc Flink để xử lý phân tán theo luồng, thay vì để web server Streamlit gánh trực tiếp tải batch lớn ạ."

---

### ❓ Câu 5: "Autoencoder có bắt được Zero-Day thật không?"

> **Người trả lời chính:** **Bùi Thị Mỷ Cẩm**
> **Hướng trả lời:**
> "Dạ, do không dùng nhãn khi huấn luyện nên về nguyên lý nó không bị giới hạn bởi kiểu gian lận cũ. Còn trên PaySim, nhóm chưa có thí nghiệm riêng cho biến thể mới, và trong 8 ca mà XGBoost bỏ sót thì Autoencoder chỉ bắt thêm được 1 ca. Đó là hướng phát triển của nhóm ạ."

---

### ❓ Câu 6: "Autoencoder hoàn toàn không dùng nhãn à?"

> **Người trả lời chính:** **Bùi Thị Mỷ Cẩm**
> **Hướng trả lời:**
> "Dạ, không dùng nhãn khi huấn luyện mạng. Nhãn chỉ dùng ở bước chọn ngưỡng trên tập validation ạ."

---

### ❓ Câu 7: "Sao không chọn phân vị 99, F1 cao hơn?"

> **Người trả lời chính:** **Bùi Thị Mỷ Cẩm**
> **Hướng trả lời:**
> "Dạ, phân vị 99 cho F1 cao hơn nhưng Recall chỉ 47%, không đạt ràng buộc Recall tối thiểu 60% mà em đặt, vì bỏ sót gian lận đắt hơn báo nhầm ạ."

---

### ❓ Câu 8: "Tại sao gọi là Deep Autoencoder mà dùng scikit-learn?"

> **Người trả lời chính:** **Bùi Thị Mỷ Cẩm**
> **Hướng trả lời:**
> "Dạ, TensorFlow/Keras chưa có bản tương thích với Python 3.14 trên máy phát triển, nên nhóm triển khai cùng nguyên lý bằng MLPRegressor với 5 lớp ẩn 16-8-4-8-16, và đã ghi rõ trong báo cáo ạ."
