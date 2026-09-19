# KỊCH BẢN THUYẾT TRÌNH BÁO CÁO ĐỒ ÁN CS106 (VĂN NÓI CHUẨN PHÂN CÔNG FINAL)

## Đề tài: Hệ Thống Phát Hiện Gian Lận Tài Chính Trên Dữ Liệu PaySim Bằng Machine Learning & Deep Learning

**Môn học:** CS106 - Trí tuệ Nhân tạo | **GVHD:** PGS.TS. Nguyễn Đình Hiển  
**Nhóm thực hiện:** Nhóm 09 (7 thành viên)

---

## 👥 BẢNG PHÂN CÔNG THUYẾT TRÌNH CHUẨN THEO TASKS ĐỒ ÁN FINAL

_(Căn cứ theo phân công chính thức trong `plans/fraud-detection-full-submit/plan.md` & `AGENTS.md`)_

| STT | Thành viên                        | Task chính trong Đồ án Final                                   | Slide phụ trách                   | Nội dung thuyết trình phụ trách                                                                                                                     |
| :-- | :-------------------------------- | :------------------------------------------------------------- | :-------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Trần Hoàng Hôn** _(26410046)_   | **PM + PPT + Submit Package** _(Phase 07 & 08)_                | **Slide 1, 2, 21**                | Mở đầu, Giới thiệu thành viên, Lộ trình báo cáo & Tổng kết, Cảm ơn, Điều phối Q&A                                                                   |
| 2   | **Đặng Chí Thanh** _(25730067)_   | **EDA + Preprocessing + 14 Features** _(Phase 00 & 01)_        | **Slide 3, 4, 5, 6, 7, 8**        | Phần 1: Bối cảnh, Thách thức Imbalance & Dữ liệu PaySim.<br>Phần 2: Khám phá EDA, 3 Dấu vết hành vi & Kỹ thuật 14 đặc trưng miền                    |
| 3   | **Hoàng Cao Sơn** _(25730061)_    | **Imbalance (SMOTE/ADASYN) + Random Forest** _(Phase 02 & 03)_ | **Slide 9, 10, 11, 12 (phần RF)** | Phần 2: Xử lý mất cân bằng SMOTE vs. ADASYN.<br>Phần 3: Kiến trúc Pipeline chuẩn Leak-Free & Mô hình Random Forest                                  |
| 4   | **Bùi Thị Mỷ Cẩm** _(25730013)_   | **XGBoost + Deep Autoencoder** _(Phase 04)_                    | **Slide 12 (phần XGB), 13, 18**   | Phần 3: Mô hình XGBoost siêu tốc (41.7s) & Mô hình không giám sát Deep Autoencoder bắt Zero-Day.<br>Phần 4: Phân bố sai số tái tạo & Ngưỡng Anomaly |
| 5   | **Nguyễn Duy Khang** _(26410055)_ | **Evaluation & Cross-Model Comparison** _(Phase 05)_           | **Slide 14, 15, 16, 17**          | Phần 4: Nghiệm thu thực nghiệm, Đối chuẩn đa chỉ số Benchmark, Phân tích Ma trận nhầm lẫn & Feature Importance (97.1%)                              |
| 6   | **Phạm Thành Trung** _(26410141)_ | **Demo UI Streamlit** _(Phase 06)_                             | **Slide 19, 20 (phần Dashboard)** | Phần 5: Trình diễn Giao diện GUI Dashboard Streamlit (Chấm điểm tức thì & Batch CSV)                                                                |
| 7   | **Vũ Văn Duy** _(26410031)_       | **Báo cáo Word + Test Cases & Demo Video** _(Phase 07)_        | **Slide 20 (phần Test & Video)**  | Phần 5: Trình bày 3 Kịch bản Test Case (An toàn, Rút cạn, Zero-Day), Video Demo hoạt động & Tổng kết đóng góp                                       |

---

# LỜI THOẠI VĂN NÓI CHI TIẾT THEO TỪNG SLIDE

---

### SLIDE 1 – TRANG TIÊU ĐỀ & GIỚI THIỆU THÀNH VIÊN

_(Thời lượng: ~60s | Người nói: **Trần Hoàng Hôn** - PM / Trưởng nhóm)_

Em chào thầy và các bạn,

Em là **Trần Hoàng Hôn**, trưởng nhóm của **Nhóm 9**. Hôm nay, nhóm chúng em xin được phép trình bày báo cáo đồ án cuối kỳ môn Trí tuệ Nhân tạo với đề tài: **"Hệ thống phát hiện gian lận tài chính trên dữ liệu giao dịch PaySim bằng Machine Learning và Deep Learning"**.

Trước khi đi vào nội dung chi tiết, em xin phép giới thiệu nhanh 7 thành viên của Nhóm và phần việc mà từng bạn trực tiếp đảm nhận trong đồ án:

- Bạn **Đặng Chí Thanh** — phụ trách phần **EDA, Tiền xử lý dữ liệu và Kỹ thuật trích xuất 14 đặc trưng**.
- Bạn **Hoàng Cao Sơn** — phụ trách phần **Xử lý mất cân bằng dữ liệu SMOTE(X-mốt)/ADASYN(A-đa-sin) và huấn luyện mô hình Random Forest**.
- Bạn **Bùi Thị Mỷ Cẩm** — phụ trách huấn luyện mô hình **XGBoost, mạng Deep Autoencoder không giám sát** và xuất các file model.
- Bạn **Nguyễn Duy Khang** — phụ trách xây dựng module **Đánh giá kiểm thử, vẽ đồ thị ROC-AUC(Rốc - Ây-Du-Xi) và lập bảng đối chuẩn so sánh giữa các mô hình**.
- Bạn **Phạm Thành Trung** — phụ trách lập trình **Giao diện Dashboard Streamlit thời gian thực** để tích hợp mô hình.
- Bạn **Vũ Văn Duy** — phụ trách soạn thảo **Báo cáo kỹ thuật, thiết kế kịch bản test case và quay video demo**.
- Và cuối cùng là em — **Trần Hoàng Hôn**, phụ trách quản lý tiến độ, thiết kế slide thuyết trình và đóng gói sản phẩm.

Sau đây, em xin phép bắt đầu buổi báo cáo ạ.

---

### SLIDE 2 – NỘI DUNG BÁO CÁO & LỘ TRÌNH (AGENDA)

_(Thời lượng: ~40s | Người nói: **Trần Hoàng Hôn**)_

Để thầy và các bạn tiện theo dõi, bài thuyết trình của nhóm em sẽ đi qua **5 phần chính**:

- **Phần 1**: Bạn Thanh sẽ giới thiệu bối cảnh bài toán gian lận tài chính và tập dữ liệu PaySim.
- **Phần 2**: Bạn Thanh và bạn Sơn sẽ phân tích các dấu vết hành vi của kẻ gian, 14 đặc trưng miền kế toán và cách xử lý mất cân bằng dữ liệu.
- **Phần 3**: Bạn Sơn và bạn Cẩm sẽ trình bày kiến trúc Pipeline chuẩn chống rò rỉ dữ liệu cùng 3 mô hình học máy: Random Forest, XGBoost và Deep Autoencoder.
- **Phần 4**: Bạn Khang và bạn Cẩm sẽ trình bày bảng so sánh kết quả thực nghiệm, phân tích ma trận nhầm lẫn và độ quan trọng của đặc trưng.
- **Phần 5**: Bạn Trung và anh Duy sẽ thực hiện Demo Streamlit cùng video kịch bản kiểm thử thực tế.

Bây giờ, em xin nhường lời lại cho bạn **Thanh** bắt đầu với Phần 1 và Phần 2 ạ.

---

### SLIDE 3 – PHẦN 1: TỔNG QUAN ĐỀ TÀI & DỮ LIỆU

_(Thời lượng: ~25s | Người nói: **Đặng Chí Thanh** - EDA & Preprocessing Lead)_

Dạ em cảm ơn anh Hôn cho phần mở đầu vừa rồi. Em chào thầy và các bạn!

Để tiếp nối lộ trình báo cáo của nhóm, em xin phép đi thẳng vào **Phần 01: Giới thiệu và phát biểu bài toán**.

Ở Phần 1 này, nhóm sẽ đi qua 3 nội dung chính như trên slide, gồm: bối cảnh công nghiệp của Mobile Money (thanh toán di động), các thách thức kỹ thuật cốt lõi, và mục tiêu nghiên cứu của nhóm.

---

### SLIDE 4 – ĐỘNG LỰC NGHIÊN CỨU & THÁCH THỨC KỸ THUẬT

_(Thời lượng: ~60s | Người nói: **Đặng Chí Thanh**)_

Về mặt thực tế, hiện nay các giao dịch ví điện tử Mobile Money diễn ra hàng triệu lượt mỗi ngày. Kẻ gian tẩu tán tiền chỉ trong vài giây, nên hệ thống phòng thủ bắt buộc phải đưa ra quyết định real-time với độ trễ dưới 100 mili-giây trước khi tiền bị rút mất.

Thầy và các bạn có thể quan sát ở các khung bên phải màn hình là bảng ký hiệu toán học và các mục tiêu cụ thể mà nhóm hướng tới.

Còn trọng tâm khi tiếp cận bài toán, ở cột bên trái, em đối mặt với **3 thách thức kỹ thuật lớn nhất**:

- **Thứ nhất là Extreme Class Imbalance (Mất cân bằng cực đoan)**: Gian lận chỉ chiếm khoảng `0.13%` — tức là cứ 800 giao dịch bình thường mới có đúng 1 ca gian lận. Với tỷ lệ lệch này, thước đo Accuracy bị vô hiệu hóa hoàn toàn, vì nếu một mô hình ngây thơ lúc nào cũng đoán "Hợp lệ" thì Accuracy đã đạt `99.87%` nhưng thực tế không bắt được tên trộm nào. Do đó, nhóm bắt buộc phải tối ưu **Recall và PR-AUC**.
- **Thứ hai là Cost Asymmetry (Tổn thất bất đối xứng)**: Bỏ sót 1 ca gian lận thì khách hàng mất tiền thật và ngân hàng mất uy tín. Trong khi cảnh báo nhầm thì mình chỉ cần gửi OTP yêu cầu người dùng xác thực lại. Vì vậy, chi phí phạt cho việc bỏ sót phải lớn hơn rất nhiều so với báo nhầm.
- **Thứ ba là tính phi tĩnh**: Kẻ gian liên tục biến đổi thủ đoạn luân chuyển tiền để lách qua các bộ lọc luật tĩnh.

---

### SLIDE 5 – TẬP DỮ LIỆU PAYSIM: THUỘC TÍNH THỐNG KÊ

_(Thời lượng: ~50s | Người nói: **Đặng Chí Thanh**)_

Để thực nghiệm, nhóm em dùng bộ dữ liệu mô phỏng chuẩn học thuật là **PaySim**.

Tập gốc khi em download trên Kaggle về ghi nhận hơn **6.36 triệu giao dịch** trong 30 ngày. Để tối ưu tài nguyên tính toán mà không làm lệch ranh giới bài toán, em thực hiện lấy mẫu phân tầng **200,000 sự kiện**, nhưng **bảo toàn nguyên vẹn 100% toàn bộ 8,213 ca gian lận gốc**. 

Thầy và các bạn có thể nhìn vào bảng ở giữa màn hình: dữ liệu ghi nhận bước thời gian theo giờ, loại giao dịch, số tiền, cùng số dư trước và sau của cả tài khoản chuyển lẫn tài khoản nhận.

Đặc biệt, qua phân tích phân bố ban đầu, em phát hiện ra một quy luật rất đắt giá ở khung màu xanh bên dưới:
**100% tất cả các ca gian lận CHỈ xảy ra ở đúng 2 loại giao dịch: TRANSFER (chuyển khoản) và CASH_OUT (rút tiền mặt)**. Các loại khác an toàn tuyệt đối. Nhờ phát hiện này, bước tiền xử lý lọc chỉ giữ lại 2 loại trên đã giúp nhóm triệt tiêu ngay được `70%` dữ liệu nhiễu vô ích cho toàn bộ pipeline phía sau.

> **Đúc kết Phần 01:**  
> Tóm lại, Phần 1 đã làm rõ bản chất mất cân bằng cực đoan 0.13% và insight khoanh vùng 2 loại giao dịch giúp loại bỏ 70% dữ liệu nhiễu, tạo tiền đề dữ liệu sạch cho Phần 2.

---

### SLIDE 6 – PHẦN 2: TIỀN XỬ LÝ & KỸ THUẬT ĐẶC TRƯNG

_(Thời lượng: ~10s | Người nói: **Đặng Chí Thanh**)_

Sau khi đã khoanh vùng được tập dữ liệu sạch, chúng ta đến với **Phần 02: Phân tích khám phá dữ liệu và kỹ thuật đặc trưng**.

---

### SLIDE 7 – PHÂN TÍCH KHÁM PHÁ DỮ LIỆU: DẤU VẾT HÀNH VI CỐT LÕI

_(Thời lượng: ~55s | Người nói: **Đặng Chí Thanh**)_

Khi thực hiện EDA trên notebook `01_eda.ipynb`, em đúc kết được **3 dấu vết hành vi mang tính bản chất của tội phạm tài chính**, tương ứng với 3 cột trên màn hình:

- **Cột đầu tiên — Khoanh vùng loại giao dịch**: Kẻ gian chiếm được tài khoản sẽ dùng lệnh `TRANSFER` chuyển tiền sang tài khoản trung gian, rồi lập tức rút tiền mặt `CASH_OUT` ngay để cắt đứt dấu vết dòng tiền.
- **Cột thứ hai — Hành vi vét sạch tài khoản**: Trong **97.56%** số vụ gian lận, số dư của nạn nhân sau giao dịch bị rút cạn sạch về đúng bằng 0 (`newbalanceOrig == 0`) trong 1 lần duy nhất trước khi nạn nhân kịp phát hiện và khóa thẻ.
- **Cột thứ ba — Sai lệch sổ cái đích**: Tiền chuyển đi nhưng số dư tài khoản nhận thực tế không tăng tương ứng (`newbalanceDest ≈ 0`), vạch trần việc dùng các tài khoản rác (mule account) để tẩu tán tiền.

Nếu chỉ đưa số tiền hay số dư thô vào mô hình thì rất lãng phí. Vì vậy, em đã tiến hành chuyển đổi các quy luật này thành các đặc trưng kế toán.

---

### SLIDE 8 – KỸ THUẬT ĐẶC TRƯNG: 14 THUỘC TÍNH CỐT LÕI

_(Thời lượng: ~50s | Người nói: **Đặng Chí Thanh**)_

Từ 3 dấu vết trên, em hiện thực trong code tổng cộng **14 đặc trưng miền chuyên sâu** ở 3 khung công thức bên trái: gồm sai lệch số dư nguồn (`errorBalanceOrig`), sai lệch số dư đích (`errorBalanceDest`), cùng cờ rút cạn (`drain_flag`) kết hợp giờ đêm (`is_overnight`).

Điều chứng minh rõ nhất hiệu quả của việc thiết kế đặc trưng nằm ở **khung Feature Importance góc dưới bên phải**:
Khi đánh giá mô hình, **chỉ riêng 2 biến `errorBalanceOrig` (49.9%) và `newbalanceOrig` (47.2%) đã chiếm tới hơn `97.1%` tổng sức mạnh phân loại!**

Điều này chứng minh kỹ thuật đặc trưng miền đã giải quyết bài toán tận gốc, biến ranh giới phân lớp phức tạp thành tuyến tính rõ rệt. Và một nguyên tắc em luôn tuân thủ nghiêm ngặt là chống rò rỉ dữ liệu: toàn bộ các bước scale chuẩn hóa chỉ được fit trên tập Train.

> **Đúc kết Phần 02 (Nhánh EDA & Features):**  
> Tóm lại, nhóm đã chuyển hóa thành công 3 dấu vết hành vi thành các đặc trưng kế toán quyết định 97.1% sức mạnh phân loại và đảm bảo tuyệt đối nguyên tắc Leak-Free.

Khi đã có không gian đặc trưng chất lượng cao, bài toán tiếp theo là xử lý mất cân bằng 0.13% bằng kỹ thuật sinh mẫu thích ứng. 

Sau đây, em xin chuyển lại phần trình bày cho bạn **Hoàng Cao Sơn** tiếp tục với nội dung SMOTE và ADASYN ở Slide 9 ạ.

---

### SLIDE 9 – XỬ LÝ MẤT CÂN BẰNG LỚP: SMOTE và ADASYN

_(Thời lượng: ~50s | Người nói: **Hoàng Cao Sơn** - Imbalance & Random Forest Lead)_

Em chào thầy và các bạn, em là **Hoàng Cao Sơn**.

Em đảm nhận việc xử lý bài toán mất cân bằng dữ liệu 0.13%. Em đã thử nghiệm và so sánh 2 kỹ thuật sinh mẫu nhân tạo là **SMOTE** và **ADASYN**:

- Với **SMOTE**: Thuật toán lấy mẫu gian lận $x_i$ và nội suy tuyến tính với láng giềng gần nhất $k$-NN trong không gian ẩn. Cơ chế này tạo ra ranh giới quyết định rất phẳng và phân tách rõ giữa 2 lớp.
- Với **ADASYN**: Thuật toán cố gắng sinh nhiều mẫu hơn ở các vùng biên khó. Tuy nhiên, trong bài toán PaySim, ADASYN bị hiện tượng sinh mẫu quá đà ở vùng chồng lấn nhiễu, làm tăng tỷ lệ báo động giả (False Alarm).

**Kết luận thực nghiệm**: Em quyết định chọn **SMOTE** làm phương pháp xử lý mất cân bằng chính thức, tạo ra tập dữ liệu huấn luyện cân bằng (230,145 dòng) giúp mô hình đạt F1-Score cao nhất và gần như triệt tiêu hoàn toàn báo động giả.

---

### SLIDE 10 – PHẦN 3: PHƯƠNG PHÁP & MÔ HÌNH HỌC MÁY

_(Thời lượng: ~10s | Người nói: **Hoàng Cao Sơn**)_

Tiếp theo, em xin đi vào Phần 3: Kiến trúc Pipeline chuẩn Leak-Free và Mô hình Random Forest mà em đã huấn luyện.

---

### SLIDE 11 – KIẾN TRÚC PIPELINE CHUẨN LEAK-FREE

_(Thời lượng: ~60s | Người nói: **Hoàng Cao Sơn**)_

Thưa thầy, trong các hệ thống AI tài chính, rủi ro lớn nhất là **Rò rỉ dữ liệu (Data Leakage)** — làm cho mô hình có điểm số cao ảo khi huấn luyện nhưng khi chạy thật thì hoàn toàn thất bại.

Để giải quyết, nhóm em xây dựng một **Pipeline gồm 6 bước** với **4 nguyên tắc bảo vệ**:

1. **Phân chia Stratified Split (80/20) TRƯỚC TIÊN**: Tách riêng tập Train và Test trước khi thực hiện bất kỳ phép biến đổi nào.
2. **Resampling cách ly tuyệt đối**: SMOTE **chỉ được chạy trên 80% tập Train**. Tập Test ($N = 40,000$ mẫu) được giữ nguyên vẹn 100% tỷ lệ mất cân bằng tự nhiên 0.13%, tuyệt đối không có mẫu nhân tạo nào lọt vào tập Test.
3. **Chuẩn hóa Scaler độc lập**: Bộ `StandardScaler` chỉ được `fit` trên tập Train, rồi dùng nguyên tham số đó `transform` trên tập Test.
4. **Không tối ưu tham số trên tập Test**: Toàn bộ quá trình chọn ngưỡng và tune model đều dùng K-Fold Cross Validation nội bộ trên tập Train.

Nhờ 4 nguyên tắc này, toàn bộ kết quả thực nghiệm của nhóm đều đảm bảo tính khách quan và trung thực tuyệt đối.

---

### SLIDE 12 – MÔ HÌNH GIÁM SÁT: RANDOM FOREST và XGBOOST

_(Thời lượng: ~60s | Người nói: **Hoàng Cao Sơn** [phần RF] & **Bùi Thị Mỷ Cẩm** [phần XGB])_

_(Phần 1 - Random Forest: **Hoàng Cao Sơn** trình bày)_

Về mô hình Random Forest ở bên trái: Em sử dụng kỹ thuật Bagging với 100 cây quyết định độc lập, kết hợp tinh chỉnh siêu tham số `RandomizedSearchCV` với 50 vòng lặp trên 5-Fold CV.

Mô hình này cho độ chính xác cực kỳ cao, Precision đạt **99.94%**, trên 38,357 giao dịch bình thường nó chỉ đoán nhầm đúng 1 ca. Tuy nhiên, nhược điểm là thời gian huấn luyện khá lâu, mất gần 20 phút.

_(Phần 2 - XGBoost: **Bùi Thị Mỷ Cẩm** tiếp lời)_

Dạ em chào thầy và các bạn, em là **Bùi Thị Mỷ Cẩm**. Em đảm nhận việc huấn luyện mô hình **XGBoost** ở bên phải:

XGBoost tối ưu hàm mục tiêu bậc hai dựa trên cả gradient bậc 1 ($g_i$) và Hessian bậc 2 ($h_i$), có bổ sung điều chuẩn L2 ($\Omega(f_t)$) để chống Overfitting.

Điểm vượt trội của XGBoost là: F1-Score đạt **99.63%** (tương đương Random Forest), nhưng thời gian huấn luyện chỉ mất **41.7 giây — nhanh gấp 28.5 lần!** Độ trễ suy luận cho 1 giao dịch chỉ dưới **0.5 mili-giây**, cực kỳ thích hợp để triển khai vào thực tế.

---

### SLIDE 13 – MÔ HÌNH KHÔNG GIÁM SÁT: DEEP AUTOENCODER

_(Thời lượng: ~60s | Người nói: **Bùi Thị Mỷ Cẩm** - Modeling XGB & Autoencoder Lead)_

Em đặt ra một bài toán khó hơn: _"Nếu kẻ gian thực hiện một hình thức lừa đảo mới lạ chưa từng có nhãn trong quá khứ thì sao?"_

Để phòng trường hợp này, em xây dựng thêm một mạng **Deep Autoencoder** học không giám sát:

Kiến trúc mạng nén đối xứng từ 14 chiều đầu vào qua nút cổ chai 4 chiều, rồi giải mã ngược ra 14 chiều:

- **Lúc học**: Mạng **chỉ được huấn luyện trên các giao dịch HỢP LỆ**, học cách nén và tái tạo cấu trúc dòng tiền bình thường.
- **Lúc phát hiện**: Khi gặp giao dịch bình thường, mạng tái tạo rất chuẩn. Nhưng khi gặp giao dịch gian lận hoặc biến thể Zero-Day dị biệt, mạng không thể tái tạo chính xác, dẫn đến **Sai số tái tạo MSE ($L_{\text{rec}}$) tăng vọt lên**:
  $$L_{\text{rec}}(x, x_{\text{recon}}) = \frac{1}{d} \sum_{j=1}^d (x_j - x_{\text{recon}, j})^2$$
- **Ra quyết định**: Cứ giao dịch nào có sai số vượt ngưỡng $\tau = 0.0455$, hệ thống sẽ gán cờ cảnh báo.

Mặc dù hoàn toàn không dùng nhãn khi train, Autoencoder vẫn bắt được **75.23% số vụ gian lận**, đóng vai trò như lớp phòng thủ an toàn thứ 2 (Defense-in-Depth).

Tiếp theo, em xin mời bạn **Nguyễn Duy Khang** trình bày phần Đánh giá kiểm thử và Bảng so sánh kết quả giữa các mô hình.

---

### SLIDE 14 – PHẦN 4: KẾT QUẢ THỰC NGHIỆM & PHÂN TÍCH

_(Thời lượng: ~10s | Người nói: **Nguyễn Duy Khang** - Evaluation & Metrics Lead)_

Dạ em cảm ơn chị Cẩm. Em là **Nguyễn Duy Khang**. Em đảm nhận việc viết các script kiểm thử độc lập trong `src/evaluation/`, tính toán các chỉ số và xuất bảng so sánh chéo giữa các mô hình. Sau đây em xin trình bày kết quả.

---

### SLIDE 15 – KẾT QUẢ THỰC NGHIỆM: BẢNG SO SÁNH ĐA CHỈ SỐ

_(Thời lượng: ~60s | Người nói: **Nguyễn Duy Khang**)_

Mọi người nhìn vào bảng so sánh ở bên trái và biểu đồ so sánh ở bên phải do em tổng hợp:

- **Random Forest + SMOTE** đạt hiệu năng phân lớp cao nhất toàn diện: **Precision = 99.94%**, **Recall = 99.51%**, và **F1-Score = 99.73%**.
- **XGBoost + SMOTE** bám sát nút với **Precision = 99.76%**, **Recall = 99.51%**, **F1-Score = 99.63%**, nhưng thời gian chạy thì nhanh vượt trội, chỉ 41.7 giây.
- **Deep Autoencoder** đạt **Recall 75.23%** ở chế độ hoàn toàn không giám sát.

Nhìn vào biểu đồ cột bên phải, thầy và các bạn có thể thấy 2 mô hình cây (cột xanh) đạt độ cân bằng lý tưởng giữa Precision và Recall. Còn Autoencoder (cột đỏ) chấp nhận Precision ở mức 38.2% để giữ Recall cao ở mức 75.2%, đúng với triết lý an toàn: _'Thà cảnh báo nhầm để kiểm tra lại, còn hơn bỏ lọt tội phạm tài chính'_.

---

### SLIDE 16 – PHÂN TÍCH MA TRẬN NHẦM LẪN & ĐÁNH ĐỔI SAI SỐ

_(Thời lượng: ~60s | Người nói: **Nguyễn Duy Khang**)_

Slide này thể hiện chi tiết **Ma trận nhầm lẫn (Confusion Matrix)** trên 40,000 mẫu kiểm thử độc lập mà em đã trích xuất:

- Ở ô đầu tiên — **Random Forest**: Trong 1,643 vụ gian lận thật, mô hình bắt trúng **1,635 vụ (TP)**, chỉ để lọt duy nhất **8 vụ (FN)**. Và trên 38,357 giao dịch bình thường, mô hình chỉ cảnh báo nhầm đúng **1 ca duy nhất (FP)**.
- Ở ô thứ hai — **XGBoost**: Bắt trúng **1,635 vụ gian lận**, bỏ lọt 8 vụ, và chỉ đoán nhầm **4 vụ**. Đây là sự đánh đổi hoàn toàn tối ưu để lấy tốc độ nhanh gấp 28.5 lần.
- Ở ô thứ ba — **Deep Autoencoder**: Bắt trúng **1,236 vụ gian lận** mà không cần biết trước nhãn. Dù có 1,998 ca đoán nhầm, nhưng với quy mô ngân hàng, việc chuyển 5% giao dịch đáng ngờ sang bước xác thực OTP là hoàn toàn chấp nhận được.

---

### SLIDE 17 – PHÂN TÍCH ĐÓNG GÓP ĐẶC TRƯNG (FEATURE IMPORTANCE)

_(Thời lượng: ~50s | Người nói: **Nguyễn Duy Khang**)_

Cũng trong module đánh giá, em tiến hành phân tích **Độ quan trọng của đặc trưng (Feature Importance)**:

Nhìn vào biểu đồ thanh ngang và bảng xếp hạng ở đây, mọi người sẽ thấy một kết quả định lượng rất rõ ràng:

Hai đặc trưng do bạn Thanh thiết kế đứng đầu bảng:

- **`errorBalanceOrig`** (Sai lệch số dư nguồn) chiếm **49.9%** đóng góp (Split Gains).
- **`newbalanceOrig`** (Rút cạn số dư về 0) chiếm **47.2%** đóng góp.

Chỉ riêng 2 đặc trưng này gộp lại đã chiếm tới **97.1% toàn bộ sức mạnh phân loại** của mô hình! Các thuộc tính truyền thống như số tiền giao dịch (`amount`) chỉ chiếm 1.4%, hay khung giờ đêm chỉ chiếm 0.9%.

Điều này chứng minh rằng: Kẻ gian có thể chia nhỏ số tiền để ngụy trang, nhưng không thể xóa được dấu vết sai lệch trên số dư tài khoản.

Tiếp theo, em mời chị **Mỷ Cẩm** sẽ giải thích nốt về cách chọn ngưỡng của mô hình Autoencoder.

---

### SLIDE 18 – PHÂN BỐ SAI SỐ TÁI TẠO & NGƯỠNG ANOMALY

_(Thời lượng: ~50s | Người nói: **Bùi Thị Mỷ Cẩm**)_

Dạ em cảm ơn bạn Khang.

Với mô hình Deep Autoencoder, quyết định then chốt của em khi huấn luyện nằm ở việc **chọn ngưỡng cắt sai số $\tau$**.

Mọi người nhìn vào biểu đồ phân bố bên trái:

- Đường màu xanh (giao dịch bình thường) tập trung ở vùng sai số rất nhỏ, dưới 0.02.
- Đường màu đỏ (giao dịch gian lận) có sai số trải dài sang tận bên phải.

Sau khi quét qua các phân vị từ 90th đến 99.9th, em quyết định chọn **Ngưỡng phân vị 95th ($\tau = 0.0455$)**. Ngưỡng này giúp Autoencoder đạt điểm cân bằng tối ưu: giữ được **Recall 75.23%** cho lớp phòng thủ Zero-Day mà vẫn kiểm soát được tỷ lệ cảnh báo nhầm.

Tiếp theo, em xin mời bạn **Phạm Thành Trung** và anh **Vũ Văn Duy** trình diễn phần Demo giao diện Streamlit và Video kịch bản kiểm thử.

---

### SLIDE 19 – PHẦN 5: DEMO HỆ THỐNG & KẾT LUẬN

_(Thời lượng: ~10s | Người nói: **Phạm Thành Trung** - Demo UI Lead)_

Dạ em cảm ơn bạn Cẩm. Em chào thầy và các bạn, em là **Phạm Thành Trung**. Sau đây em và anh **Vũ Văn Duy** xin đại diện nhóm trình diễn hệ thống Demo Streamlit thực tế và các kịch bản kiểm thử.

---

### SLIDE 20 – HỆ THỐNG DEMO STREAMLIT & KỊCH BẢN KIỂM THỬ

_(Thời lượng: ~75s | Người nói: **Phạm Thành Trung** & **Vũ Văn Duy**)_

_(Phần 1 - Giao diện Dashboard: **Phạm Thành Trung** trình bày)_

Để mô hình không chỉ dừng lại ở các dòng code trong notebook, Em đã phát triển một giao diện **Dashboard giám sát gian lận thời gian thực trên nền tảng Streamlit** như khung hình bên trái.
Giao diện cho phép người vận hành chọn mô hình suy luận (XGBoost, Random Forest hoặc Autoencoder), nhập thông số giao dịch và nhận kết quả cảnh báo rủi ro tức thì trong chưa đầy 0.5 mili-giây. Ngoài ra, hệ thống còn hỗ trợ tính năng **Audit Batch CSV**, cho phép tải lên danh sách hàng nghìn giao dịch để tự động trích xuất các ca có nguy cơ cao.

_(Phần 2 - Kịch bản Test Case & Video Demo: **Vũ Văn Duy** tiếp lời)_

Em chào thầy và các bạn, em là **Vũ Văn Duy**. Em đã hoàn thiện báo cáo Word và thiết kế **3 kịch bản kiểm thử (Test Scenarios)**:

1. _Kịch bản 1 (Giao dịch an toàn):_ Chuyển tiền thông thường, số dư biến động khớp chuẩn ➔ Hệ thống báo Xanh an toàn (Xác suất rủi ro $< 0.1\%$).
2. _Kịch bản 2 (Gian lận rút cạn tài khoản):_ Lệnh chuyển tiền vét sạch số dư về 0 ➔ Hệ thống lập tức báo Đỏ (Xác suất $> 99.8\%$) và khóa giao dịch.
3. _Kịch bản 3 (Bất thường Zero-Day):_ Đưa giao dịch lạ qua Autoencoder để kích hoạt cờ kiểm duyệt thứ cấp.
   Video demo chi tiết hoạt động của 3 kịch bản này đã được em ghi lại và lưu trong thư mục `demo/` của đồ án.

_(Phạm Thành Trung tổng kết 4 đóng góp & Lộ trình)_

Tóm lại, đồ án của nhóm đạt được **4 kết quả cốt lõi**: Pipeline chuẩn Leak-Free; 14 đặc trưng chiếm >97% đóng góp; F1-Score đạt 99.73%; và kiến trúc phòng thủ đa tầng.

Trong tương lai, nhóm sẽ mở rộng sang **Graph Neural Networks (GNN)** như GraphSAGE để phát hiện đường dây rửa tiền, và tích hợp Apache Kafka để xử lý luồng dữ liệu lớn.

---

### SLIDE 21 – TỔNG KẾT, TÀI LIỆU THAM KHẢO & PHIÊN HỎI ĐÁP (Q&A)

_(Thời lượng: ~45s | Người nói: **Trần Hoàng Hôn** - Trưởng nhóm)_

Dạ thưa Thầy và các bạn, toàn bộ mã nguồn chương trình, tài liệu kỹ thuật và mô hình đã được nhóm công khai trên GitHub tại địa chỉ như trên slide.

Thay mặt Nhóm 9, chúng em xin gửi lời cảm ơn chân thành nhất đến **Thầy** đã tận tình hướng dẫn trong suốt học kỳ vừa qua.

Sau đây, nhóm chúng em xin lắng nghe các câu hỏi và góp ý từ Thầy và các bạn để hoàn thiện đồ án hơn nữa ạ. Em xin chân thành cảm ơn!

---

# 🛡️ BỘ CÂU HỎI PHẢN BIỆN DỰ BỊ DÀNH CHO NHÓM (Q&A DEFENSE)

### ❓ Câu 1: "Điểm F1 > 99.6% cao bất thường như vậy có chắc chắn là không bị rò rỉ dữ liệu (Data Leakage) không?"

> **Người trả lời chính:** **Đặng Chí Thanh** _(EDA & Preprocessing)_  
> **Hướng trả lời:**  
> "Dạ thưa thầy, nhóm em đã kiểm soát rất chặt nguy cơ rò rỉ dữ liệu qua 3 chốt chặn:
>
> 1. Tập Test độc lập (20%) được tách ra đầu tiên trước mọi bước xử lý.
> 2. SMOTE chỉ chạy trên 80% tập Train. Tập Test hoàn toàn giữ nguyên phân bố tự nhiên 0.13% và không có mẫu nhân tạo nào.
> 3. Scaler chỉ `fit` trên Train và `transform` mù trên Test.
>    Điểm số cao thực chất là nhờ 2 đặc trưng miền `errorBalanceOrig` và `newbalanceOrig` do em thiết kế đã giải thích đúng bản chất kế toán của hành vi gian lận (chiếm >97% split gains), giúp phân tách dữ liệu gần như tuyến tính thay vì do mô hình học vẹt ạ."

---

### ❓ Câu 2: "Tại sao nhóm lại ưu tiên dùng XGBoost cho thực tế thay vì Random Forest?"

> **Người trả lời chính:** **Bùi Thị Mỷ Cẩm / Hoàng Cao Sơn**  
> **Hướng trả lời:**  
> "Dạ thưa thầy, về chất lượng phân loại thì 2 mô hình tương đương nhau (chỉ chênh nhau 3 ca đoán nhầm trên 40,000 mẫu). Nhưng Random Forest mất gần 20 phút để train và file model rất nặng. Còn XGBoost chỉ mất 41 giây để train, độ trễ suy luận dưới 0.5ms và tốn rất ít RAM. Với hệ thống cổng thanh toán cần xử lý hàng nghìn giao dịch mỗi giây thì XGBoost là lựa chọn tối ưu hơn hẳn ạ."

---

### ❓ Câu 3: "Autoencoder có Precision thấp (38.2%) thì có giá trị gì trong thực tế?"

> **Người trả lời chính:** **Bùi Thị Mỷ Cẩm / Nguyễn Duy Khang**  
> **Hướng trả lời:**  
> "Dạ thưa thầy, Autoencoder đóng vai trò là màng bọc an toàn thứ 2 chứ không thay thế XGBoost. Mô hình có giám sát chỉ bắt được các chiêu trò cũ đã có nhãn. Còn Autoencoder học 'thế nào là bình thường', nên bất kỳ chiêu trò mới nào làm dòng tiền bất thường đều bị nó phát hiện. Tỷ lệ Precision 38.2% là do em chủ động hạ ngưỡng để bắt được 75.2% gian lận. 5% giao dịch bị nghi ngờ này ngân hàng chỉ cần bắt gửi mã OTP hoặc chuyên viên rà soát là xử lý được ạ."

---

### ❓ Câu 4: "Giao diện Streamlit xử lý dữ liệu lớn như thế nào nếu có file CSV hàng trăm ngàn dòng?"

> **Người trả lời chính:** **Phạm Thành Trung / Vũ Văn Duy**  
> **Hướng trả lời:**  
> "Dạ thưa thầy, trong giao diện Streamlit, em đã cấu hình tính năng `st.cache_resource` để tải trước trọng số mô hình XGBoost vào bộ nhớ đệm, và sử dụng thư viện Pandas để vector hóa việc tính 14 đặc trưng miền theo lô (batch processing). Do đó, khi tải file CSV lên, hệ thống chấm điểm song song hàng chục ngàn dòng chỉ trong vài giây mà không bị nghẽn giao diện ạ."
