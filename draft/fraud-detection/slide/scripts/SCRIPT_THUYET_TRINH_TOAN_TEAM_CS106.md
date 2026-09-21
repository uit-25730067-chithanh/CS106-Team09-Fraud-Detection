# KỊCH BẢN THUYẾT TRÌNH BÁO CÁO ĐỒ ÁN CS106 (VĂN NÓI CHUẨN PHÂN CÔNG FINAL)

## Đề tài: Hệ Thống Phát Hiện Gian Lận Tài Chính Trên Dữ Liệu PaySim Bằng Machine Learning & Deep Learning

**Môn học:** CS106 - Trí tuệ Nhân tạo | **GVHD:** PGS.TS. Nguyễn Đình Hiển
**Nhóm thực hiện:** Nhóm 09 (7 thành viên)
**Phiên bản:** Hiệu chỉnh theo dữ liệu thực nghiệm chạy thử (Meeting Dry-Run 18/09/2026)

---

> ⏱️ **KẾT QUẢ ĐO ĐẠC & HIỆU CHỈNH THỜI LƯỢNG THỰC TẾ (TỪ CUỘC HỌP DRY-RUN 18/09/2026):**
>
> - **Căn cứ thực nghiệm:** Dữ liệu bóc tách từ file ghi âm cuộc họp diễn tập toàn team `Meeting in [Nhóm 14-15] _ Trí tuệ nhân tạo - CS106.F31.CN2.TTNT.docx` (tổng thời lượng 49 phút 48 giây).
> - **Tổng thời gian nói thuần vòng chạy thử 1:** **35 phút 02 giây** (2,102 giây / 5,183 từ phát biểu). Nếu tính cả sự cố chia sẻ màn hình và gián đoạn chuyển slide: **~40 phút**.
> - **Tốc độ nói thực tế (Empirical WPM - Words Per Minute):**
>   - **Đặng Chí Thanh:** **186.2 WPM** (~3.10 từ/giây) — *Tốc độ nói nhanh nhất nhóm, diễn giải sâu và nhiều số liệu*.
>   - **Trần Hoàng Hôn:** **156.4 WPM** (~2.61 từ/giây) — *Phong thái tự nhiên, kết nối tốt, giới thiệu chi tiết từng thành viên*.
>   - **Hoàng Cao Sơn:** **152.3 WPM** (~2.54 từ/giây) — *Tốc độ đều, phân tích sâu cơ chế SMOTE/ADASYN và 4 nguyên tắc Leak-Free*.
>   - **Phạm Thành Trung:** **147.0 WPM** (~2.45 từ/giây) — *Thuyết minh thao tác trực tiếp trên giao diện Streamlit (Live Demo hết 5m04s)*.
>   - **Bùi Thị Mỷ Cẩm:** **135.5 WPM** (~2.26 từ/giây) — *Giọng rõ ràng, chuẩn mực kỹ thuật, trình bày Autoencoder và phân vị ngưỡng*.
>   - **Nguyễn Duy Khang:** **119.8 WPM** (~2.00 từ/giây) — *Nhịp nói điềm đạm, nhấn mạnh rành mạch từng chỉ số và ma trận nhầm lẫn*.
>   - **Vũ Văn Duy:** **72.9 WPM** (lần đầu lúng túng) ➔ **Chuẩn hóa ~115 WPM** (~1.92 từ/giây) *khi trình bày 3 kịch bản kiểm thử*.
> - **Mục tiêu tối ưu sau cuộc họp (Target Calibrated):** **~15 phút** (cô đọng số liệu chi tiết đã có sẵn trên slide, lược bớt định nghĩa lý thuyết, và tối ưu Live Demo Streamlit gọn gàng trong ~3 phút).

## ⏱️ BẢNG ĐỐI CHIẾU THỜI GIAN THEO MỤC TIÊU 15 PHÚT (900 GIÂY)

> ⚠️ **Định hướng chiến lược tối ưu cho buổi bảo vệ 15 phút (theo khung giờ chuẩn môn học CS106):**
>
> - **Bỏ qua Slide 21:** Bạn Phạm Thành Trung sau khi thao tác Live Demo tại Slide 20 sẽ trực tiếp tổng kết 4 đóng góp, cảm ơn Thầy/Cô và mở phiên hỏi đáp Q&A.
> - **Slide 20 do một mình Trung phụ trách:** Anh Vũ Văn Duy không nói trên slide, dành toàn bộ thời lượng làm "chủ lực" trả lời các câu hỏi phản biện chuyên sâu về Báo cáo khoa học Word 32 trang và phương pháp luận học thuật.

|     STT     | Thành viên                  |         Slide phụ trách         |                  Tình trạng cập nhật script                  | Nội dung chính phụ trách                                                                                     | Thời gian Mục tiêu 15p (Target Budget) | Thời gian Kịch bản hiện tại (Script Time) | Thực tế chạy thử Dry-run (18/09) | Chênh lệch (Kịch bản vs Mục tiêu 15p) | Mức độ đáp ứng & Khuyến nghị nhịp độ                                                      |
| :---------: | :---------------------------- | :--------------------------------: | :---------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------- | :---------------------------------------: | :--------------------------------------------: | :----------------------------------: | :-----------------------------------------: | :--------------------------------------------------------------------------------------------------- |
| **1** | **Trần Hoàng Hôn**   |        **Slide 1, 2**        |      🟢**Đã cập nhật** *(Rút gọn Slide 1 & 2)*      | Mở đầu, giới thiệu 7 thành viên Nhóm 9 và lộ trình 5 phần.                                           |      **1 phút 15s** *(75s)*      |        **1 phút 22s** *(82s)*        |      *3 phút 16s* *(196s)*      |      🟢**Vượt +7s** *(+9%)*      | ✅**ĐẠT CHUẨN** (Khớp mục tiêu sau khi rút gọn).                                       |
| **2** | **Đặng Chí Thanh**   |  **Slide 3, 4, 5, 6, 7, 8**  |   🟢**Đã cập nhật** *(Rút gọn Slide 3–8 PR #37 & #38)*   | Bối cảnh, PaySim 200k, 100% gian lận ở 2 loại, 14 đặc trưng miền.                                       |     **3 phút 30s** *(210s)*     |        **4 phút 48s** *(288s)*        |      *7 phút 54s* *(474s)*      |    🔴**Vượt +1m18s** *(+37%)*    | ✅**Đã rút gọn ~34s (PR #38):** Lời thoại ngắn gọn, đi thẳng vào 2 biến 97.1%.             |
| **3** | **Hoàng Cao Sơn**     | **Slide 9, 10, 11, 12 (RF)** |     🔴**Chưa cập nhật** *(Giữ nguyên bản cũ)*     | SMOTENC giữ nguyên cờ 0/1, 4 chốt chặn Leak-Free và Random Forest.                                         |     **2 phút 00s** *(120s)*     |        **3 phút 30s** *(210s)*        |      *7 phút 17s* *(437s)*      |    🔴**Vượt +1m30s** *(+75%)*    | ⚠️**Cắt lý thuyết:** Bỏ giải thích ADASYN, chỉ nêu kết quả RF F1=0.9973.           |
| **4** | **Bùi Thị Mỷ Cẩm**  |  **Slide 12 (XGB), 13, 18**  |     🟢**Đã cập nhật** *(Rút gọn cô đọng 21/09)*     | XGBoost (train < 1 phút, nhanh hơn RF 20 lần) và Deep Autoencoder: phòng thủ đa tầng, chọn ngưỡng phân vị 95. |     **2 phút 00s** *(120s)*     |        **2 phút 20s** *(140s)* *(ước tính: ~450 từ ÷ 135.5 WPM)*        |      *4 phút 15s* *(255s)*      |    🟢**Vượt +20s** *(+16%)*    | ✅**ĐẠT CHUẨN:** Đã rút ngắn 45% câu chữ, giữ trọn vẹn số liệu kỹ thuật và luận điểm then chốt. |
| **5** | **Nguyễn Duy Khang**   |   **Slide 14, 15, 16, 17**   |     🔴**Chưa cập nhật** *(Giữ nguyên bản cũ)*     | Đối chuẩn 5 mô hình, Ma trận nhầm lẫn (sót 8 ca) và Feature Importance.                                |     **2 phút 15s** *(135s)*     |        **4 phút 39s** *(279s)*        |      *4 phút 27s* *(267s)*      |    🔴**Vượt +2m24s** *(+106%)*    | ⚠️**Không đọc bảng:** Chỉ nêu bật RF & XGBoost dẫn đầu, lướt các chỉ số phụ. |
| **6** | **Vũ Văn Duy**        |       *Không nói Slide*       |     🟢**Đã cập nhật** *(0s — Chuyển sang Q&A)*     | **Chuyên trách phản biện:** Trụ cột trả lời Q&A về Báo cáo Word 32 trang & Threats to Validity. |      **0 phút 00s** *(0s)*      |         **0 phút 00s** *(0s)*         |      *2 phút 29s* *(149s)*      |   🟢**`0s` (Khớp tuyệt đối)**   | 🎯**HOÀN THÀNH MỤC TIÊU:** Duy không nói slide, tránh đổi micro.                      |
| **7** | **Phạm Thành Trung**  | **Slide 19, 20 + Cảm ơn** | 🔴**Chưa cập nhật** *(Chưa gộp kịch bản Slide 20)* | Giới thiệu Dashboard, nêu 3 kịch bản, Live Demo, 4 đóng góp, Cảm ơn & Mời Q&A.                        |     **2 phút 40s** *(160s)*     |        **3 phút 50s** *(230s)*        |      *5 phút 04s* *(304s)*      |    🔴**Vượt +1m10s** *(+44%)*    | ⚠️**Cần demo nhanh:** Bấm 2 preset mẫu, không gõ tay dữ liệu.                         |
|     ⏩     | **Slide 21**            |            *Bỏ qua*            |       🟢**Đã cập nhật** *(Cắt bỏ khỏi bài)*       | Trung nói cảm ơn trực tiếp tại cuối Slide 20, không quay lại Slide 21.                                  |      **0 phút 00s** *(0s)*      |         **0 phút 00s** *(0s)*         |               *45s*               |   🟢**`0s` (Khớp tuyệt đối)**   | 🎯**HOÀN THÀNH MỤC TIÊU:** Cắt bỏ hoàn toàn độ trễ switch slide.                    |
|    ⏱️    | **Dự phòng (Buffer)** |                 —                 |                                —                                | Độ trễ chuyển slide giữa các thành viên và kết nối micro.                                             |      **1 phút 20s** *(80s)*      |                       —                       |                  —                  |                     —                     | Dành cho việc chuyển slide và kết nối âm thanh.                                               |
|     🏁     | **TỔNG TOÀN BÀI**    |        **20 Slides**        |                 **3/7 bạn đã tối ưu**                 | **6 thành viên nói + Live Demo**                                                                        |     **15 phút 00s** *(900s)*     |      **14 phút 16s** *(856s)*      |      *~35m02s (Thuần nói)*      |      🟢**KHỚP MỤC TIÊU (-44s)**      | 🎯**ĐÃ ĐẠT CHUẨN KHUNG 15 PHÚT!**                                              |

# LỜI THOẠI VĂN NÓI CHI TIẾT THEO TỪNG SLIDE

---

### SLIDE 1 – TRANG TIÊU ĐỀ & GIỚI THIỆU THÀNH VIÊN

_(Thời lượng chuẩn hóa: **~95s – 100s** [Meeting thực tế: ~110s] | Người nói: **Trần Hoàng Hôn** - PM / Trưởng nhóm)_

Em chào thầy và các bạn,

Em là **Trần Hoàng Hôn**, trưởng nhóm của **Nhóm 9**. Hôm nay, nhóm em xin trình bày báo cáo với đề tài: **"Hệ thống phát hiện gian lận tài chính trên dữ liệu giao dịch PaySim bằng Machine Learning và Deep Learning"**.

Em xin phép giới thiệu 7 thành viên của Nhóm:

- Bạn **Đặng Chí Thanh** — phụ trách **EDA, Tiền xử lý dữ liệu và trích xuất 14 đặc trưng**.
- Bạn **Hoàng Cao Sơn** — phụ trách **Xử lý mất cân bằng dữ liệu và huấn luyện mô hình Random Forest**.
- Bạn **Bùi Thị Mỷ Cẩm** — phụ trách huấn luyện mô hình **XGBoost, mạng Deep Autoencoder**.
- Bạn **Nguyễn Duy Khang** — phụ trách xây dựng module **Đánh giá kiểm thử độc lập và lập bảng đối chuẩn giữa các mô hình**.
- Anh **Vũ Văn Duy** — phụ trách biên soạn **Báo cáo**.
- Bạn **Phạm Thành Trung** — phụ trách  **giao diện và thực hiện Demo**.
- Và cuối cùng là em — **Trần Hoàng Hôn**, phụ trách quản lý tiến độ, thiết kế và đóng gói sản phẩm.

Sau đây, em xin phép bắt đầu buổi báo cáo ạ.

---

### SLIDE 2 – NỘI DUNG BÁO CÁO & LỘ TRÌNH (AGENDA)

_(Thời lượng chuẩn hóa: **~60s – 65s** [Meeting thực tế: ~86s] | Người nói: **Trần Hoàng Hôn**)_

Bài thuyết trình của nhóm em sẽ đi qua **5 phần chính**:

- **Phần 1**: Bạn Thanh sẽ giới thiệu bối cảnh bài toán, 3 thách thức kỹ thuật cốt lõi và tập dữ liệu PaySim.
- **Phần 2**: Bạn Thanh và bạn Sơn sẽ phân tích 3 dấu vết hành vi của kẻ gian, 14 đặc trưng và kỹ thuật xử lý mất cân bằng dữ liệu.
- **Phần 3**: Bạn Sơn và bạn Cẩm sẽ trình bày kiến trúc Pipeline cùng 3 mô hình học máy: Random Forest, XGBoost và Deep Autoencoder.
- **Phần 4**: Bạn Khang và bạn Cẩm sẽ trình bày bảng so sánh kết quả thực nghiệm, phân tích ma trận nhầm lẫn và độ quan trọng của đặc trưng.
- **Phần 5**: Bạn Trung sẽ Demo thực tế và tổng kết.

Bây giờ, em xin nhường lời lại cho bạn **Thanh** bắt đầu với Phần 1 và Phần 2 ạ. Mời Thanh!

---

### SLIDE 3 – PHẦN 1: TỔNG QUAN ĐỀ TÀI & DỮ LIỆU

_(Thời lượng chuẩn hóa: **~15s – 20s** [Meeting thực tế: ~15s] | Người nói: **Đặng Chí Thanh** - EDA & Preprocessing Lead)_

Dạ em cảm ơn anh Hôn. Em chào thầy và các bạn! Nhóm sẽ bắt đầu với **Phần 01** — gồm bối cảnh Mobile Money, thách thức kỹ thuật và mục tiêu nghiên cứu.

---

### SLIDE 4 – ĐỘNG LỰC NGHIÊN CỨU & THÁCH THỨC KỸ THUẬT

_(Thời lượng chuẩn hóa: **~95s – 100s** [Meeting thực tế: ~118s] | Người nói: **Đặng Chí Thanh**)_

Về mặt thực tế, hiện nay các giao dịch ví điện tử Mobile Money diễn ra hàng triệu lượt mỗi ngày. Kẻ gian tẩu tán tiền chỉ trong vài giây, nên hệ thống phòng thủ bắt buộc phải đưa ra quyết định real-time với độ trễ dưới 100 mili-giây trước khi tiền bị rút mất.

Thầy và các bạn có thể quan sát ở các khung bên phải màn hình là bảng ký hiệu toán học và các mục tiêu cụ thể mà nhóm hướng tới.

Còn trọng tâm khi tiếp cận bài toán, ở cột bên trái, em đối mặt với **3 thách thức kỹ thuật lớn nhất**:

- **Thứ nhất là Extreme Class Imbalance (Mất cân bằng cực đoan)**: Gian lận chỉ chiếm khoảng `0.13%` — tức là cứ 800 giao dịch bình thường mới có đúng 1 ca gian lận. Với tỷ lệ lệch này, thước đo Accuracy bị vô hiệu hóa hoàn toàn, vì nếu một mô hình ngây thơ lúc nào cũng đoán "Hợp lệ" thì Accuracy đã đạt `99.87%` nhưng thực tế không bắt được tên trộm nào. Do đó, nhóm bắt buộc phải tối ưu **Recall và PR-AUC**.
- **Thứ hai là Cost Asymmetry (Tổn thất bất đối xứng)**: Bỏ sót 1 ca gian lận thì khách hàng mất tiền thật và ngân hàng mất uy tín. Trong khi cảnh báo nhầm thì mình chỉ cần gửi OTP yêu cầu người dùng xác thực lại. Vì vậy, chi phí phạt cho việc bỏ sót phải lớn hơn rất nhiều so với báo nhầm.
- **Thứ ba là tính phi tĩnh**: Kẻ gian liên tục biến đổi thủ đoạn luân chuyển tiền để lách qua các bộ lọc luật tĩnh.

---

### SLIDE 5 – TẬP DỮ LIỆU PAYSIM: THUỘC TÍNH THỐNG KÊ

_(Thời lượng chuẩn hóa: **~60s – 65s** [Meeting thực tế: ~94s] | Người nói: **Đặng Chí Thanh**)_

Để thực nghiệm, nhóm sử dụng bộ dữ liệu mô phỏng chuẩn học thuật là **PaySim**.

Tập gốc khi em download trên Kaggle về ghi nhận hơn **6.36 triệu giao dịch** trong 30 ngày. Để tối ưu tài nguyên tính toán mà không làm lệch ranh giới bài toán, em thực hiện lấy mẫu phân tầng **200,000 sự kiện**, nhưng **bảo toàn nguyên vẹn 100% toàn bộ 8,213 ca gian lận gốc**, đồng thời mở rộng không gian từ 11 lên 14 đặc trưng.

Thầy và các bạn có thể nhìn vào bảng ở giữa màn hình: dữ liệu ghi nhận bước thời gian theo giờ, loại giao dịch, số tiền, cùng số dư trước và sau của cả tài khoản chuyển lẫn tài khoản nhận.

Đặc biệt, qua phân tích phân bố ban đầu, em phát hiện ra một quy luật rất đắt giá ở khung màu xanh bên dưới:**100% tất cả các ca gian lận CHỈ xảy ra ở đúng 2 loại giao dịch: TRANSFER (chuyển khoản) và CASH_OUT (rút tiền mặt)**. Các loại khác an toàn tuyệt đối. Nhờ phát hiện này, bước tiền xử lý lọc chỉ giữ lại 2 loại trên đã giúp nhóm loại bỏ ngay được `~56.5%` giao dịch hoàn toàn không có gian lận, tối ưu tài nguyên tính toán cho toàn bộ pipeline phía sau.

> **Đúc kết Phần 01:**
> Tóm lại, Phần 1 đã làm rõ bản chất mất cân bằng cực đoan 0.13% và insight khoanh vùng 2 loại giao dịch giúp loại bỏ ~56.5% giao dịch không có rủi ro gian lận, tạo tiền đề dữ liệu sạch cho Phần 2.

---

### SLIDE 6 – PHẦN 2: TIỀN XỬ LÝ & KỸ THUẬT ĐẶC TRƯNG

_(Thời lượng chuẩn hóa: **~10s** [Meeting thực tế: ~10s] | Người nói: **Đặng Chí Thanh**)_

Sau khi đã khoanh vùng được tập dữ liệu sạch, chúng ta đến với **Phần 02** — gồm 3 nội dung: phân tích dấu vết hành vi thực nghiệm, công thức toán học của 14 đặc trưng, và xử lý mất cân bằng lớp.

---

### SLIDE 7 – PHÂN TÍCH KHÁM PHÁ DỮ LIỆU: DẤU VẾT HÀNH VI CỐT LÕI

_(Thời lượng chuẩn hóa: **~45s – 50s** [Meeting thực tế: ~110s] | Người nói: **Đặng Chí Thanh**)_

Khi thực hiện EDA trên notebook `01_eda.ipynb`, em đúc kết được **3 dấu vết hành vi mang tính bản chất của tội phạm tài chính**, tương ứng với 3 cột trên màn hình:

- **Phát hiện 1 — Khoanh vùng loại giao dịch**: Kẻ gian chiếm được tài khoản sẽ dùng lệnh `TRANSFER` chuyển tiền sang tài khoản trung gian, rồi lập tức rút tiền mặt `CASH_OUT` ngay để cắt đứt dấu vết dòng tiền.
- **Phát hiện 2 — Vét sạch số dư nguồn**: Trong **97.55%** số vụ gian lận, số dư của nạn nhân sau giao dịch bị rút cạn sạch về đúng bằng 0 (`newbalanceOrig == 0`) trong 1 lần duy nhất trước khi nạn nhân kịp phát hiện và khóa thẻ.
- **Phát hiện 3 — Sai lệch số dư đích**: Tiền chuyển đi nhưng số dư tài khoản nhận thực tế không tăng tương ứng (`newbalanceDest ≈ 0`), vạch trần việc dùng các tài khoản rác (mule account) để tẩu tán tiền.

---

### SLIDE 8 – KỸ THUẬT ĐẶC TRƯNG: 14 THUỘC TÍNH CỐT LÕI

_(Thời lượng chuẩn hóa: **~50s – 55s** [Meeting thực tế: ~127s] | Người nói: **Đặng Chí Thanh**)_

Từ 3 dấu vết trên, em hiện thực trong code tổng cộng **14 đặc trưng miền chuyên sâu** ở 3 khung công thức bên trái: gồm sai lệch số dư nguồn (`errorBalanceOrig`), sai lệch số dư đích (`errorBalanceDest`), cùng cờ rút cạn (`drain_flag`) kết hợp giờ đêm (`is_overnight`).

Ở khung Feature Importance bên phải, khi đánh giá mô hình XGBoost, **chỉ riêng 2 biến `errorBalanceOrig` (49.9%) và `newbalanceOrig` (47.2%) đã chiếm tới `97.1%` tổng Feature Split Gains!** Nhóm cũng thẳng thắn ghi nhận việc mô hình dựa 98.5% vào số dư là rủi ro simulator artifact theo Mục 3.6.2. Toàn bộ các bước chuẩn hóa chỉ fit trên tập Train để đảm bảo nguyên tắc Leak-Free.

Sau đây, em xin chuyển lại phần trình bày cho bạn **Hoàng Cao Sơn** tiếp tục với nội dung SMOTE và ADASYN ở Slide 9 ạ.

---

### SLIDE 9 – XỬ LÝ MẤT CÂN BẰNG LỚP: SMOTE và ADASYN

_(Thời lượng chuẩn hóa: **~75s – 80s** [Meeting thực tế: ~153s] | Người nói: **Hoàng Cao Sơn** - Imbalance & Random Forest Lead)_

Em chào thầy và các bạn, mình là **Hoàng Cao Sơn**.

Ở phần trước thì Thanh đã phân tích rất rõ về 14 đặc trưng trích xuất. Nhưng khi bước sang huấn luyện mô hình, thách thức lớn nhất là tỷ lệ gian lận cực đoan chỉ chiếm **0.13%**. Nếu để nguyên dữ liệu gốc, mô hình sẽ bị rơi vào cái bẫy 'bộ phân lớp hiển nhiên' (Majority Classifier) — đoán tất cả là bình thường thì Accuracy vẫn 99.87% nhưng hoàn toàn vô dụng.

Để xử lý, nhóm đã thử nghiệm đối chuẩn 2 kỹ thuật sinh mẫu nhân tạo là **SMOTENC** và **ADASYN**:

- Với **ADASYN**: Thuật toán ưu tiên sinh mẫu ở các vùng biên khó. Tuy nhiên trong dữ liệu gian lận, vùng biên thường bị nhiễu do kẻ gian ngụy trang. ADASYN tập trung sinh dày đặc mẫu nhân tạo vào vùng nhiễu này, làm méo mó ranh giới quyết định và dẫn tới **tỷ lệ báo động giả (False Alarm) tăng vọt**, khách hàng bình thường cũng bị chặn thẻ.
- Với **SMOTENC**: Thuật toán nội suy tuyến tính láng giềng k-NN trong không gian ẩn ổn định hơn, tạo ra ranh giới phẳng và phân cách rõ ràng. Điểm mấu chốt là nhóm dùng biến thể **SMOTENC (Nominal and Continuous)**: vì dữ liệu có 4 cờ nhị phân quan trọng (như cờ rút cạn, giao dịch đêm), SMOTENC bảo toàn nguyên vẹn giá trị 0 hoặc 1, không bao giờ nội suy ra các số thực lẻ vô nghĩa như 0.4 hay 0.7.

**Kết luận thực nghiệm:** Nhóm chọn **SMOTENC** làm phương pháp xử lý chính thức, tạo ra tập huấn luyện cân bằng gồm **230,145 dòng**, giúp mô hình triệt tiêu tối đa các ca báo động giả.

---

### SLIDE 10 – PHẦN 3: PHƯƠNG PHÁP & MÔ HÌNH HỌC MÁY

_(Thời lượng chuẩn hóa: **~10s** [Meeting thực tế: ~10s] | Người nói: **Hoàng Cao Sơn**)_

Tiếp theo, em xin đi vào Phần 3: Kiến trúc Pipeline chuẩn Leak-Free và chi tiết 3 mô hình học máy mà nhóm đã xây dựng.

---

### SLIDE 11 – KIẾN TRÚC PIPELINE CHUẨN LEAK-FREE

_(Thời lượng chuẩn hóa: **~85s – 90s** [Meeting thực tế: ~140s] | Người nói: **Hoàng Cao Sơn**)_

Kính thưa Thầy, trong các hệ thống AI tài chính, rủi ro lớn nhất là **Rò rỉ dữ liệu (Data Leakage)** — mô hình nhìn trộm dữ liệu kiểm thử, dẫn đến điểm số trên máy thì cao chót vót nhưng đem ra chạy thực tế thì thất bại hoàn toàn.

Để đảm bảo tính trung thực và khách quan tuyệt đối, nhóm đã thiết kế quy trình gồm 6 bước với **4 nguyên tắc bảo vệ Leak-Free nghiêm ngặt**:

1. **Stratified Split (80/20) TRƯỚC TIÊN**: Chốt chặn đầu tiên tách riêng tập Train (160,000 dòng) và Test (40,000 dòng) trước khi thực hiện bất kỳ phép biến đổi nào.
2. **Cô lập Resampling tuyệt đối**: Quá trình sinh mẫu SMOTENC **chỉ chạy trên 80% tập Train**. Tập Test 40,000 mẫu được giữ nguyên vẹn 100% tỷ lệ thực tế ngoài đời, tuyệt đối không có một mẫu nhân tạo nào lọt vào.
3. **Chuẩn hóa Scaler độc lập**: Bộ `StandardScaler` chỉ được `fit` trên tập Train để lấy trung bình và phương sai, rồi dùng nguyên tham số đó `transform` trên Test.
4. **Tối ưu siêu tham số độc lập**: Toàn bộ khâu chọn ngưỡng và tune model đều dùng **5-Fold Stratified Cross-Validation nội bộ trên Train**, không chạm vào Test.

Nhờ 4 nguyên tắc này, toàn bộ kết quả thực nghiệm của nhóm đều là số liệu thật và có giá trị tin cậy cao.

---

### SLIDE 12 – MÔ HÌNH GIÁM SÁT: RANDOM FOREST và XGBOOST

_(Thời lượng chuẩn hóa: **~170s** [Sơn ~40s, Cẩm ~130s (nói đủ; ~120s nếu bỏ các câu **[có thể bỏ]**)] [Meeting thực tế: ~200s] | Người nói: **Hoàng Cao Sơn** [phần RF] & **Bùi Thị Mỷ Cẩm** [phần XGB])_

_(Phần 1 - Random Forest: **Hoàng Cao Sơn** trình bày)_

Dựa trên pipeline đó, mô hình có giám sát đầu tiên nhóm xây dựng là **Random Forest** ở bên trái. Nhóm sử dụng cơ chế Ensemble Bagging với 200 cây quyết định độc lập, tối ưu qua `RandomizedSearchCV` 50 vòng lặp, khống chế `max_depth = 20`, đồng thời áp dụng trọng số lớp cân bằng theo từng cây con.

Khi kiểm thử trên 40,000 mẫu tập Test, mô hình đạt độ chính xác cực cao: **Precision = 99.94%** (trên 38,357 giao dịch bình thường chỉ đoán nhầm đúng 1 ca), **Recall = 99.51%**, và **F1-Score = 0.9973**. Tuy nhiên, hạn chế của Random Forest là thời gian huấn luyện khá lâu, mất gần 20 phút.

Để giải quyết bài toán tốc độ, phần tiếp theo sẽ do bạn **Bùi Thị Mỷ Cẩm** trình bày về mô hình XGBoost.

_(Phần 2 - XGBoost: **Bùi Thị Mỷ Cẩm** tiếp lời)_

_(Anh Sơn vừa nói xong: Random Forest rất chính xác nhưng train mất gần 20 phút)_

Dạ em cảm ơn anh Sơn. Em chào Thầy và các bạn, em là Cẩm, em phụ trách mô hình **XGBoost** và **Deep Autoencoder**.

Để giải quyết bài toán tốc độ huấn luyện lâu của Random Forest, nhóm chọn hướng tiếp cận **XGBoost**. Thay vì các cây độc lập, XGBoost xây cây nối tiếp để cây sau sửa sai cho cây trước, tối ưu bằng cả gradient và hessian bậc hai cùng cơ chế phạt L2 để tránh Overfitting.

Kết quả thực nghiệm: XGBoost đạt **F1-Score 99.63%** tương đương Random Forest, nhưng thời gian huấn luyện **chưa tới 1 phút** — nhanh hơn **20 lần**, và **độ trễ suy luận chỉ cỡ nửa mili-giây**, cực kỳ tối ưu cho các cổng thanh toán **real-time**. Vì vậy, XGBoost được nhóm chọn làm mô hình chấm điểm trực tiếp trong phần Demo ạ.


### SLIDE 13 – MÔ HÌNH KHÔNG GIÁM SÁT: DEEP AUTOENCODER

_(Thời lượng chuẩn hóa: **~50s** | Người nói: **Bùi Thị Mỷ Cẩm**)_

_(Dừng một nhịp, đổi giọng sang đặt vấn đề.)_

Tuy nhiên, cả Random Forest và XGBoost đều là học có giám sát — tức là phải có **nhãn** và chỉ bắt được các thủ đoạn đã từng thấy. Vậy nếu kẻ gian dùng chiêu thức hoàn toàn mới thì sao?

Để giải quyết, em xây dựng thêm mạng **Deep Autoencoder** theo hướng **học không giám sát (Unsupervised)**. Ý tưởng tương tự một nhân viên kế toán quen thuộc với hóa đơn hợp lệ — khi xuất hiện dòng tiền bất thường sẽ nhận diện được ngay sai lệch:

- **Kiến trúc mạng:** Nhận 14 đặc trưng, nén qua các lớp 16-8 xuống **bottleneck 4 chiều** rồi giải mã ngược lại 8-16-14 chiều để ép mạng nắm bắt cấu trúc cốt lõi.
- **Nguyên lý:** Mạng *chỉ học trên giao dịch hợp lệ*. Khi gặp gian lận, sai số tái tạo (MSE) tăng vọt. Nếu vượt **ngưỡng τ = 0.0455**, hệ thống sẽ lập tức gắn cờ cảnh báo.

Kết quả trên tập Test: dù không hề biết nhãn khi train, Autoencoder vẫn đạt **Recall 75.23%** (bắt trúng 1,236 / 1,643 vụ gian lận). Em bố trí mô hình đóng vai trò **Defense-in-Depth** — lớp lưới an toàn thứ hai chuyển các ca nghi vấn sang thẩm định chuyên sâu.

Bây giờ em xin mời bạn Khang trình bày kết quả so sánh chi tiết giữa các mô hình ạ.

### SLIDE 14 – PHẦN 4: KẾT QUẢ THỰC NGHIỆM & PHÂN TÍCH

_(Thời lượng chuẩn hóa: **~25s** [Meeting thực tế: ~25s] | Người nói: **Nguyễn Duy Khang** - Evaluation & Metrics Lead)_

Dạ em cảm ơn chị Cẩm. Em chào thầy và các bạn, em là **Nguyễn Duy Khang**. Phần việc của em là xây dựng các script kiểm thử độc lập trong `src/evaluation/`, tính toán các chỉ số và lập bảng đối chuẩn so sánh chéo giữa các mô hình. Sau đây em xin trình bày kết quả.

---

### SLIDE 15 – KẾT QUẢ THỰC NGHIỆM: BẢNG SO SÁNH ĐA CHỈ SỐ

_(Thời lượng chuẩn hóa: **~80s – 85s** [Meeting thực tế: ~80s] | Người nói: **Nguyễn Duy Khang**)_

Nhìn vào bảng so sánh bên trái và biểu đồ bên phải do nhóm em tổng hợp:

- **Random Forest + SMOTE** đạt hiệu năng phân lớp toàn diện cao nhất: **Precision = 99.94%**, **Recall = 99.51%**, và **F1-Score = 99.73%**.
- **XGBoost + SMOTE** bám sát nút với **Precision = 99.76%**, **Recall = 99.51%**, **F1-Score = 99.63%**, nhưng có thời gian huấn luyện siêu tốc chỉ **41.7 giây**.
- **Deep Autoencoder** đạt **Recall = 75.23%** ở chế độ hoàn toàn không giám sát.

Nhìn vào biểu đồ cột bên phải: Hai mô hình cây (cột xanh) đạt sự cân bằng lý tưởng giữa Precision và Recall. Còn Autoencoder (cột đỏ) chấp nhận Precision ở mức 38.2% để giữ Recall cao ở mức 75.2%, hoàn toàn đúng với triết lý an toàn tài chính: *"Thà cảnh báo nhầm để kiểm tra lại một bước OTP, còn hơn bỏ lọt tội phạm tài chính"*.

---

### SLIDE 16 – PHÂN TÍCH MA TRẬN NHẦM LẪN & ĐÁNH ĐỔI SAI SỐ

_(Thời lượng chuẩn hóa: **~80s – 85s** [Meeting thực tế: ~80s] | Người nói: **Nguyễn Duy Khang**)_

Slide này thể hiện chi tiết **Ma trận nhầm lẫn** trên 40,000 mẫu kiểm thử độc lập:

- **Ô đầu tiên — Random Forest:** Trong 1,643 vụ gian lận thật, mô hình bắt trúng **1,635 vụ (TP)**, chỉ để lọt duy nhất **8 vụ (FN)**. Và trên 38,357 giao dịch bình thường, mô hình chỉ cảnh báo nhầm đúng **1 ca duy nhất (FP)**.
- **Ô thứ hai — XGBoost:** Bắt trúng **1,635 vụ gian lận**, bỏ lọt 8 vụ, và chỉ đoán nhầm **4 vụ**. Đây là sự đánh đổi hoàn toàn tối ưu để lấy tốc độ huấn luyện nhanh gấp 28.5 lần.
- **Ô thứ ba — Deep Autoencoder:** Bắt trúng **1,236 vụ gian lận** mà không cần biết trước nhãn. Dù có 1,998 ca đoán nhầm, nhưng với quy mô ngân hàng, việc chuyển 5% giao dịch đáng ngờ sang bước xác thực OTP bổ sung là hoàn toàn khả thi và chấp nhận được trong thực tế.

---

### SLIDE 17 – PHÂN TÍCH ĐÓNG GÓP ĐẶC TRƯNG (FEATURE IMPORTANCE)

_(Thời lượng chuẩn hóa: **~80s – 85s** [Meeting thực tế: ~82s] | Người nói: **Nguyễn Duy Khang**)_

Cũng trong module đánh giá, nhóm tiến hành phân tích **Độ quan trọng của đặc trưng (Feature Importance)**:

Nhìn vào biểu đồ thanh ngang và bảng xếp hạng, Thầy và các bạn sẽ thấy một kết quả định lượng rất rõ ràng:
Hai đặc trưng hàng đầu chiếm thế thượng phong:

- **`errorBalanceOrig`** (Sai lệch số dư nguồn) chiếm **49.9%** đóng góp.
- **`newbalanceOrig`** (Số dư nguồn về 0 khi rút cạn) chiếm **47.2%** đóng góp.

**Chỉ riêng 2 đặc trưng này gộp lại đã chiếm tới 97.1% toàn bộ Feature Split Gains của XGBoost!** Trong khi các thuộc tính phụ trợ như số tiền giao dịch (`amount`) chỉ chiếm khoảng 0.5%, hay khung giờ đêm chỉ chiếm 0.03%.

Điều này cho thấy mô hình bám rất chặt vào dấu vết sai lệch số dư. Trong báo cáo, nhóm cũng nhận diện rõ việc phụ thuộc 98.5% vào nhóm số dư là nguy cơ rủi ro do đặc thù simulator PaySim, chứ không vội vàng xem đây là ranh giới tuyến tính đơn giản ngoài thực tế.

Tiếp theo, em xin mời chị **Mỷ Cẩm** giải thích phần chọn ngưỡng của mô hình Autoencoder ở slide 18.

---

### SLIDE 18 – PHÂN BỐ SAI SỐ TÁI TẠO & NGƯỠNG ANOMALY

_(Thời lượng chuẩn hóa: **~55s** | Người nói: **Bùi Thị Mỷ Cẩm**)_

Cảm ơn bạn Khang. Em xin quay lại làm rõ quyết định quan trọng nhất của Autoencoder: **chọn ngưỡng quyết định τ**.

_(chỉ biểu đồ bên trái)_ Biểu đồ phân bố cho thấy: giao dịch bình thường (màu xanh) tập trung ở vùng sai số rất thấp dưới 0.02, còn gian lận (màu đỏ) trải rộng sang bên phải. Tuy nhiên hai phân bố có vùng chồng lấn (tương ứng 407 ca bỏ sót), buộc ta phải chấp nhận sự đánh đổi giữa Precision và Recall.

_(chỉ bảng bên phải)_ Bảng quét ngưỡng theo phân vị sai số trên tập Validation (tách từ Train, chuẩn Leak-Free):
- Hạ ngưỡng xuống phân vị 90: Recall cao nhưng Precision thấp dưới 30% (báo nhầm nhiều).
- Nâng ngưỡng lên phân vị 99.9: Precision đạt 91.5% nhưng Recall giảm còn 25.4% (bỏ lọt 3/4 số vụ gian lận).
- Nhóm chọn **phân vị 95 (ngưỡng τ = 0.0455)**, đạt điểm cân bằng tối ưu: **Recall 75.2%** và **Precision 38.2%**. Lựa chọn này tuân thủ ràng buộc **Recall tối thiểu 60%** và tối đa hóa F1, vì trong an toàn tài chính, bỏ sót gian lận đắt hơn nhiều so với việc yêu cầu người dùng xác thực thêm mã OTP.

Tóm lại, XGBoost và Autoencoder tạo nên hệ thống phòng thủ đa tầng hoàn chỉnh. Tiếp theo em xin mời bạn Trung và anh Duy trình diễn phần Demo ạ. Em xin cảm ơn.

### SLIDE 19 – PHẦN 5: DEMO HỆ THỐNG & KẾT LUẬN

_(Thời lượng chuẩn hóa: **~20s** [Chuyển giao màn hình Live Demo] | Người nói: **Phạm Thành Trung** - Demo UI Lead)_

Dạ em cảm ơn bạn Cẩm. Em chào thầy và các bạn, em là **Phạm Thành Trung**. Sau đây em và anh **Vũ Văn Duy** xin đại diện nhóm trình diễn hệ thống Demo Dashboard Streamlit thực tế và các kịch bản kiểm thử.

Trước khi em chia sẻ màn hình để thao tác ứng dụng, em xin mời anh **Duy** trình bày 3 kịch bản kiểm thử mà anh đã thiết kế ạ.

---

### SLIDE 20 – HỆ THỐNG DEMO STREAMLIT & KỊCH BẢN KIỂM THỬ

_(Thời lượng chuẩn hóa: **~240s – 270s** (~4m00s – 4m30s) [Duy ~85s, Trung Live Demo ~160s-185s] | [Meeting thực tế: Duy 149s + Trung Demo 304s = 453s] | Người nói: **Vũ Văn Duy** [3 Test Cases] & **Phạm Thành Trung** [Live Demo Streamlit & Đóng góp])_

---

#### 🔹 PHẦN 1: TRÌNH BÀY 3 KỊCH BẢN KIỂM THỬ (Vũ Văn Duy trình bày — ~85s)

Em chào Thầy và các bạn, em là **Vũ Văn Duy**. Để kiểm thử toàn diện khả năng vận hành thực tế của mô hình ngoài đời, em đã thiết kế **3 kịch bản kiểm thử (Test Scenarios)** đại diện cho các tình huống điển hình:

1. **Kịch bản 1 — Giao dịch an toàn (Hợp lệ chuẩn):**Giao dịch chuyển khoản thông thường với dòng tiền cân đối, số dư trước và sau trừ tiền khớp chuẩn 100% về mặt sổ sách kế toán.➔ *Kỳ vọng:* Hệ thống đánh giá an toàn, xác suất gian lận cực thấp dưới 0.1%, trả về trạng thái Hợp lệ.
2. **Kịch bản 2 — Gian lận rút cạn tài khoản (Cảnh báo đỏ khẩn cấp):**Mô phỏng hành vi tội phạm vét sạch tài khoản nạn nhân về đúng bằng 0 (`newbalanceOrig = 0`), số tiền chuyển đi lớn hơn số dư hiện có và xuất hiện sai lệch kế toán nghiêm trọng.➔ *Kỳ vọng:* Mô hình XGBoost lập tức phát hiện với xác suất gian lận trên 88%, kích hoạt cờ đỏ khóa giao dịch ngay lập tức.
3. **Kịch bản 3 — Giao dịch rủi ro cận biên & Zero-Day (Cần lưu ý):**
   Giao dịch chuyển 2.5 triệu thực hiện vào khung giờ đêm (2h - 3h sáng), cấu trúc dòng tiền có dấu hiệu bất thường nhưng chưa đủ bằng chứng rõ rệt để khóa ngay.
   ➔ *Kỳ vọng:* Hệ thống trả về xác suất cảnh báo ở mức ~32%, hiển thị mức cảnh báo vàng "Cần lưu ý" để yêu cầu người dùng xác thực thêm mã OTP.

Sau đây, xin mời bạn **Trung** sẽ trực tiếp thao tác chạy 3 kịch bản này trên giao diện ứng dụng Streamlit của nhóm!

---

#### 🔹 PHẦN 2: THAO TÁC LIVE DEMO GIAO DIỆN STREAMLIT (Phạm Thành Trung trình bày — ~160s – 185s)

*(Phạm Thành Trung chia sẻ màn hình và thao tác trực tiếp trên trình duyệt)*

Dạ em cảm ơn anh Duy. Thưa Thầy và các bạn, đây là giao diện **Dashboard giám sát gian lận thời gian thực** do em xây dựng trên nền tảng Streamlit, kết nối trực tiếp với trọng số mô hình XGBoost-SMOTE và StandardScaler đã huấn luyện, đồng thời hỗ trợ tra cứu đối chuẩn Autoencoder.

- **Khu vực nhập liệu:** Cho phép người dùng nhập loại giao dịch, thời điểm thực hiện, số tiền, và số dư trước sau của tài khoản nguồn và đích. Sau khi nhập, hệ thống tự động vector hóa để tạo 14 đặc trưng miền và chuẩn hóa bằng StandardScaler trong bộ nhớ.
- **Thực nghiệm Kịch bản 1 (An toàn):** Em chọn mẫu giao dịch cân đối. Nhấn *"Phân tích giao dịch"* ➔ Hệ thống trả về kết quả rủi ro rất thấp (0.02%), gắn nhãn Xanh an toàn trong chưa đầy 0.5 mili-giây.
- **Thực nghiệm Kịch bản 3 (Cận biên ban đêm):** Em chọn mẫu 2.5 triệu thực hiện ban đêm. Nhấn *"Phân tích giao dịch"* ➔ Mô hình trả về xác suất 31.95%. Kết quả chưa vượt ngưỡng 50% nhưng hệ thống lập tức hiển thị nhãn Vàng *"Cần lưu ý"* để nhân viên rà soát hoặc kích hoạt bước gửi mã OTP xác thực.
- **Thực nghiệm Kịch bản 2 (Vét cạn tài khoản):** Em chọn kịch bản tài khoản nguồn bị rút cạn về 0 và sai lệch sổ sách. Nhấn *"Phân tích giao dịch"* ➔ Xác suất gian lận tăng vọt lên **88.36%**, vượt ngưỡng cảnh báo và hệ thống lập tức gán cờ Đỏ *"Nghi vấn gian lận"*.
- **Ba góc nhìn trực quan:** Người vận hành có thể xem chi tiết:
  1. *Tín hiệu rủi ro:* Hiển thị trực quan các cờ cảnh báo (rút cạn ví, giờ đêm, tỷ lệ tiền/số dư).
  2. *Sơ đồ dòng tiền:* Mô phỏng luồng tiền di chuyển giữa tài khoản nguồn và đích.
  3. *Biến động số dư:* Đối chiếu sai lệch sổ sách trước và sau giao dịch.
- **Tab Hiệu năng & Lịch sử:** Giao diện cho phép xem lại toàn bộ ma trận nhầm lẫn, biểu đồ ROC/PR, chuyển đổi giữa SMOTENC và ADASYN để đối chiếu. Đồng thời, toàn bộ giao dịch được lưu cục bộ trong cơ sở dữ liệu SQLite, hỗ trợ lọc theo trạng thái và xuất báo cáo kiểm toán định dạng CSV.

---

#### 🔹 PHẦN 3: TỔNG KẾT ĐÓNG GÓP & LỘ TRÌNH (Phạm Thành Trung tổng kết — ~30s)

Tóm lại, đồ án của nhóm đạt được **4 đóng góp cốt lõi**:

1. Pipeline chuẩn mực **Leak-Free 100%**, bảo vệ tính khách quan của thực nghiệm.
2. Trích xuất thành công **14 đặc trưng miền kế toán**, giải thích tới hơn 97.1% sức mạnh phân loại.
3. Đạt hiệu năng xuất sắc với **F1-Score 99.73%** (Random Forest) và mô hình triển khai **XGBoost 41.7s siêu tốc**.
4. Kiến trúc phòng thủ đa tầng kết hợp Deep Autoencoder bắt các mối đe dọa Zero-Day.

Về hướng phát triển, nhóm định hướng mở rộng sang **Graph Neural Networks (GNN)** như GraphSAGE để phát hiện các đường dây rửa tiền đa tầng, và tích hợp Apache Kafka để xử lý luồng dữ liệu phân tán quy mô lớn.

Sau đây, em xin nhường lời lại cho bạn Hôn để tổng kết buổi báo cáo ạ.

---

### SLIDE 21 – TỔNG KẾT, TÀI LIỆU THAM KHẢO & PHIÊN HỎI ĐÁP (Q&A)

_(Thời lượng chuẩn hóa: **~45s – 50s** | Người nói: **Trần Hoàng Hôn** - Trưởng nhóm)_

Kính thưa Thầy và các bạn, toàn bộ mã nguồn chương trình, bộ dữ liệu thực nghiệm đã xử lý, tài liệu kỹ thuật, báo cáo Word và slide thuyết trình đã được nhóm chúng em đóng gói và phát hành đầy đủ trên GitHub repository của đồ án.

Thay mặt toàn thể 7 thành viên Nhóm 9, chúng em xin gửi lời cảm ơn chân thành và sâu sắc nhất đến **Thầy** đã tận tình hướng dẫn, định hướng khoa học cho chúng em trong suốt học kỳ vừa qua.

Sau đây, nhóm chúng em xin trân trọng lắng nghe các câu hỏi nhận xét, góp ý và phản biện từ Thầy cùng các bạn để hoàn thiện đồ án hơn nữa ạ.

Em xin chân thành cảm ơn Thầy và các bạn đã chú ý lắng nghe!

---

# 🛡️ BỘ CÂU HỎI PHẢN BIỆN DỰ BỊ DÀNH CHO NHÓM (Q&A DEFENSE)

### ❓ Câu 1: "Điểm F1 > 99.6% cao bất thường như vậy có chắc chắn là không bị rò rỉ dữ liệu (Data Leakage) không?"

> **Người trả lời chính:** **Đặng Chí Thanh** _(EDA & Preprocessing)_**Hướng trả lời:**"Dạ thưa thầy, nhóm em đã kiểm soát rất chặt nguy cơ rò rỉ dữ liệu qua 4 chốt chặn Leak-Free nghiêm ngặt:
>
> 1. Tập Test độc lập (20%) được tách riêng đầu tiên trước mọi bước xử lý.
> 2. SMOTENC chỉ chạy trên 80% tập Train. Tập Test hoàn toàn giữ nguyên phân bố sau downsample (4.11% fraud, 1,643 ca) và tuyệt đối không có mẫu nhân tạo nào.
> 3. StandardScaler chỉ `fit` trên Train và `transform` mù trên Test.
> 4. Toàn bộ quá trình chọn ngưỡng và tinh chỉnh tham số đều dùng 5-Fold Cross Validation nội bộ trên Train.
>    Điểm số cao thực chất là nhờ đặc trưng dẫn xuất `errorBalanceOrig` và cột gốc `newbalanceOrig` đã giải thích đúng bản chất kế toán của hành vi gian lận (chiếm 97.1% split gains). Nhóm cũng nhìn nhận khách quan đây là phát hiện mạnh trên PaySim nhưng cũng đi kèm rủi ro simulator artifact như Báo cáo Mục 3.6.2 đã phân tích sâu ạ."

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
> "Dạ thưa thầy, trong giao diện Streamlit, em đã cấu hình tính năng `@st.cache_resource` để tải trước trọng số mô hình XGBoost và StandardScaler vào bộ nhớ đệm, tránh tải lại mô hình ở mỗi lượt tương tác. Đồng thời, em sử dụng thư viện Pandas để vector hóa toàn bộ quá trình tính toán 14 đặc trưng miền theo lô (batch processing). Do đó, khi tải file CSV lớn lên, hệ thống có thể chấm điểm song song hàng chục ngàn giao dịch chỉ trong vài giây mà không làm đơ hay nghẽn giao diện ạ."

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
