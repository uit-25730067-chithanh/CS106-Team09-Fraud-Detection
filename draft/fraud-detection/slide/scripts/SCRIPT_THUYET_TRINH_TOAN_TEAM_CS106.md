# KỊCH BẢN THUYẾT TRÌNH BÁO CÁO ĐỒ ÁN CS106 (VĂN NÓI CHUẨN PHÂN CÔNG FINAL)

## Đề tài: Hệ Thống Phát Hiện Gian Lận Tài Chính Trên Dữ Liệu PaySim Bằng Machine Learning & Deep Learning

**Môn học:** CS106 - Trí tuệ Nhân tạo | **GVHD:** PGS.TS. Nguyễn Đình Hiển
**Nhóm thực hiện:** Nhóm 09 (7 thành viên)
**Phiên bản:** Hiệu chỉnh theo dữ liệu thực nghiệm chạy thử (Meeting Dry-Run 18/09/2026)

---

> ⏱️ **KẾT QUẢ ĐO ĐẠC & HIỆU CHỈNH THỜI LƯỢNG THỰC TẾ (TỪ CUỘC HỌP DRY-RUN 18/09/2026):**
>
> - **Căn cứ thực nghiệm:** Dữ liệu bóc tách từ file ghi âm cuộc họp diễn tập toàn team Meeting in [Nhóm 14-15] _ Trí tuệ nhân tạo - CS106.F31.CN2.TTNT.docx (tổng thời lượng 49 phút 48 giây).
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
| **2** | **Đặng Chí Thanh**   |  **Slide 3, 4, 5, 6, 7, 8**  |   🟢**Đã cập nhật** *(Rút gọn Slide 3–8 PR #37 & #38)*   | Bối cảnh, PaySim 200k, 100% gian lận ở 2 loại, 14 đặc trưng miền.                                       |     **4 phút 00s** *(240s)*     |        **4 phút 48s** *(288s)*        |      *7 phút 54s* *(474s)*      |    🟡**Vượt +48s** *(+20%)*    | ✅**Hợp lý 6 slides kỹ thuật dày (PR #38):** Nội dung kỹ thuật cốt lõi đã cô đọng tối đa, không cắt thêm để giữ 97.1% & 3 thách thức.             |
| **3** | **Hoàng Cao Sơn**     | **Slide 9, 10, 11, 12 (RF)** |     🟢**Đã cập nhật** *(Rút gọn Slide 9–12 PR #42)*     | SMOTENC giữ nguyên cờ 0/1, 4 chốt chặn Leak-Free và Random Forest.                                         |     **2 phút 00s** *(120s)*     |        **2 phút 30s** *(150s)*        |      *7 phút 17s* *(437s)*      |    🟢**Vượt +30s** *(+25%)*    | ✅**Đã rút gọn (PR #42):** Bám sát slide, 4 nguyên tắc Leak-Free & kết quả RF F1=0.9973.           |
| **4** | **Bùi Thị Mỷ Cẩm**  |  **Slide 12 (XGB), 13, 18**  |     🟢**Đã cập nhật** *(Chuẩn hóa tối ưu 15p)*     | XGBoost (57.94s, nhanh hơn RF ~20 lần) và Deep Autoencoder (14-16-8-4-8-16-14, phân vị 95th, Recall 75.2%).                                         |     **2 phút 30s** *(150s)*     |        **2 phút 40s** *(160s)* *(Slide 12 XGB: 50s, Slide 13: 55s, Slide 18: 55s)*        |      *4 phút 15s* *(255s)*      |    🟢**Vượt +10s** *(+7%)*    | ✅**TỐI ƯU HOÀN HẢO:** Giữ nguyên 100% chiều sâu kỹ thuật, văn nói cô đọng giúp Cẩm nói tự tin, trôi chảy, đúng chuẩn 15p toàn team. |
| **5** | **Nguyễn Duy Khang**   |   **Slide 14, 15, 16, 17**   |     🟢**Đã cập nhật** *(Rút gọn Slide 15–17 PR #50)*     | Đối chuẩn 5 mô hình, Ma trận nhầm lẫn (sót 8 ca) và Feature Importance.                                |     **2 phút 15s** *(135s)*     |        **2 phút 30s** *(150s)*        |      *4 phút 27s* *(267s)*      |    🟢**Vượt +15s** *(+11%)*    | ✅**Đã rút gọn (PR #50):** Lời thoại ngắn gọn (~40–45s/slide), bỏ đọc số liệu chi tiết; nêu bật RF/XGBoost và 2 đặc trưng chính 97%. |
| **6** | **Vũ Văn Duy**        |       *Không nói Slide*       |     🟢**Đã cập nhật** *(0s — Chuyển sang Q&A)*     | **Chuyên trách phản biện:** Trụ cột trả lời Q&A về Báo cáo Word 31 trang & phương pháp luận học thuật. |      **0 phút 00s** *(0s)*      |         **0 phút 00s** *(0s)*         |      *2 phút 29s* *(149s)*      |   🟢**0s (Khớp tuyệt đối)**   | 🎯**HOÀN THÀNH MỤC TIÊU:** Duy không nói slide, tránh độ trễ chuyển đổi micro.                      |
| **7** | **Phạm Thành Trung**  | **Slide 20 + Cảm ơn** | 🟢**Đã cập nhật** *(Gộp hoàn chỉnh Slide 20)* | Dẫn nhập (~10s), Trình diễn Demo 2m17s (3 kịch bản), 4 đóng góp cốt lõi & Cảm ơn Q&A (~35s).          |     **2 phút 40s** *(160s)*     |        **3 phút 00s** *(180s)* *(Demo 2m17s + nói 43s)* |      *5 phút 04s* *(304s)*      |    🟢**Vượt +20s** *(+12%)*    | ✅**ĐÃ TỐI ƯU DEMO:** Demo tinh gọn 2m17s chạy trực tiếp trên Slide 20, Trung dẫn nhập 10s và chốt kết bài 33s. |
|     ⏩     | **Slide 21**            |            *Bỏ qua*            |       🟢**Đã cập nhật** *(Slide dự bị)*       | Trung nói cảm ơn trực tiếp tại cuối Slide 20, chuyển sang Slide 21 làm phông nền cho phiên Q&A.                                  |      **0 phút 00s** *(0s)*      |         **0 phút 00s** *(0s)*         |               *45s*               |   🟢**0s (Khớp tuyệt đối)**   | 🎯**HOÀN THÀNH MỤC TIÊU:** Cắt bỏ hoàn toàn độ trễ switch slide.                    |
|    ⏱️    | **Dự phòng (Buffer)** |                 —                 |                                —                                | Độ trễ chuyển slide giữa các thành viên và kết nối micro.                                             |      **30s** *(30s)*      |                       —                       |                  —                  |                     —                     | Dành cho việc chuyển slide và kết nối âm thanh giữa các phần.                                               |
|     🏁     | **TỔNG TOÀN BÀI**    |        **20 Slides**        |                 **7/7 bạn đã cập nhật & tối ưu hoàn tất**                 | **6 thành viên nói Slide + Trình diễn Demo (Duy phụ trách chính Q&A)**                             |     **15 phút 00s** *(900s)*     |      **14 phút 20s** *(860s)* *(chưa buffer)*      |      *~35m02s (Thuần nói)*      |      🟢**KHỚP CHUẨN MỤC TIÊU 15P**      | 🎯**TOÀN BỘ KỊCH BẢN ĐẠT ĐỘ DÀI LÝ TƯỞNG (~14M20S THUẦN NÓI + 30S BUFFER = 14M50S < 15 PHÚT).** |

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

Bây giờ, em xin nhường lời lại cho bạn **Thanh** bắt đầu với 2 phần đầu tiên ạ. Mời Thanh!

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

- **Thứ nhất là Extreme Class Imbalance (Mất cân bằng cực đoan)**: Gian lận chỉ chiếm khoảng 0.13% — tức là cứ khoảng 775 đến 800 giao dịch bình thường mới có đúng 1 ca gian lận (chính xác 1 trên 775 ca theo tỷ lệ 8,213 ca trên 6.36 triệu sự kiện PaySim gốc). Với tỷ lệ lệch này, thước đo Accuracy bị vô hiệu hóa hoàn toàn, vì nếu một mô hình ngây thơ lúc nào cũng đoán "Hợp lệ" thì Accuracy đã đạt 99.87% nhưng thực tế không bắt được tên trộm nào. Do đó, nhóm bắt buộc phải tối ưu **Recall và PR-AUC**.
- **Thứ hai là Cost Asymmetry (Tổn thất bất đối xứng)**: Bỏ sót 1 ca gian lận thì khách hàng mất tiền thật và ngân hàng mất uy tín. Trong khi cảnh báo nhầm thì mình chỉ cần gửi OTP yêu cầu người dùng xác thực lại. Vì vậy, chi phí phạt cho việc bỏ sót phải lớn hơn rất nhiều so với báo nhầm.
- **Thứ ba là tính phi tĩnh**: Kẻ gian liên tục biến đổi thủ đoạn luân chuyển tiền để lách qua các bộ lọc luật tĩnh.

---

### SLIDE 5 – TẬP DỮ LIỆU PAYSIM: THUỘC TÍNH THỐNG KÊ

_(Thời lượng chuẩn hóa: **~60s – 65s** [Meeting thực tế: ~94s] | Người nói: **Đặng Chí Thanh**)_

Để thực nghiệm, nhóm sử dụng bộ dữ liệu mô phỏng chuẩn học thuật là **PaySim**.

Tập gốc khi em download trên Kaggle về ghi nhận hơn **6.36 triệu giao dịch** trong 30 ngày. Để tối ưu tài nguyên tính toán mà không làm lệch ranh giới bài toán, em thực hiện lấy mẫu phân tầng **200,000 sự kiện**, nhưng **bảo toàn nguyên vẹn 100% toàn bộ 8,213 ca gian lận gốc**, đồng thời mở rộng không gian từ 11 lên 14 đặc trưng.

Thầy và các bạn có thể nhìn vào bảng ở giữa màn hình: dữ liệu ghi nhận bước thời gian theo giờ, loại giao dịch, số tiền, cùng số dư trước và sau của cả tài khoản chuyển lẫn tài khoản nhận.

Đặc biệt, qua phân tích phân bố ban đầu, em phát hiện ra một quy luật rất đắt giá ở khung màu xanh bên dưới: **100% tất cả các ca gian lận CHỈ xảy ra ở đúng 2 loại giao dịch: TRANSFER (chuyển khoản) và CASH_OUT (rút tiền mặt)**. Các loại khác an toàn tuyệt đối. Nhờ phát hiện này, bước tiền xử lý lọc chỉ giữ lại 2 loại trên đã giúp nhóm loại bỏ ngay được ~56.5% giao dịch hoàn toàn không có gian lận, tối ưu tài nguyên tính toán cho toàn bộ pipeline phía sau.

> **Đúc kết Phần 01:**
> Tóm lại, Phần 1 đã làm rõ bản chất mất cân bằng cực đoan 0.13% và insight khoanh vùng 2 loại giao dịch giúp loại bỏ ~56.5% giao dịch không có rủi ro gian lận, tạo tiền đề dữ liệu sạch cho Phần 2.

---

### SLIDE 6 – PHẦN 2: TIỀN XỬ LÝ & KỸ THUẬT ĐẶC TRƯNG

_(Thời lượng chuẩn hóa: **~10s** [Meeting thực tế: ~10s] | Người nói: **Đặng Chí Thanh**)_

Sau khi đã khoanh vùng được tập dữ liệu sạch, chúng ta đến với **Phần 02** — gồm 3 nội dung: phân tích dấu vết hành vi thực nghiệm, công thức toán học của 14 đặc trưng, và xử lý mất cân bằng lớp.

---

### SLIDE 7 – PHÂN TÍCH KHÁM PHÁ DỮ LIỆU: DẤU VẾT HÀNH VI CỐT LÕI

_(Thời lượng chuẩn hóa: **~45s – 50s** [Meeting thực tế: ~110s] | Người nói: **Đặng Chí Thanh**)_

Khi thực hiện EDA trên notebook 01_eda.ipynb, em đúc kết được **3 dấu vết hành vi mang tính bản chất của tội phạm tài chính**, tương ứng với 3 cột trên màn hình:

- **Phát hiện 1 — Khoanh vùng loại giao dịch**: Kẻ gian chiếm được tài khoản sẽ dùng lệnh TRANSFER chuyển tiền sang tài khoản trung gian, rồi lập tức rút tiền mặt CASH_OUT ngay để cắt đứt dấu vết dòng tiền.
- **Phát hiện 2 — Vét sạch số dư nguồn**: Trong **97.55%** số vụ gian lận, số dư của nạn nhân sau giao dịch bị rút cạn sạch về đúng bằng 0 (newbalanceOrig == 0) trong 1 lần duy nhất trước khi nạn nhân kịp phát hiện và khóa thẻ.
- **Phát hiện 3 — Sai lệch số dư đích**: Tiền chuyển đi nhưng số dư tài khoản nhận thực tế không tăng tương ứng (newbalanceDest ≈ 0), vạch trần việc dùng các tài khoản rác (mule account) để tẩu tán tiền.

---

### SLIDE 8 – KỸ THUẬT ĐẶC TRƯNG: 14 THUỘC TÍNH CỐT LÕI

_(Thời lượng chuẩn hóa: **~50s – 55s** [Meeting thực tế: ~127s] | Người nói: **Đặng Chí Thanh**)_

Từ 3 dấu vết trên, em hiện thực trong code tổng cộng **14 đặc trưng miền chuyên sâu** ở 3 khung công thức bên trái: gồm sai lệch số dư nguồn (errorBalanceOrig), sai lệch số dư đích (errorBalanceDest), cùng cờ rút cạn (drain_flag) kết hợp giờ đêm (is_overnight).

Ở khung Feature Importance bên phải, khi đánh giá mô hình XGBoost, **chỉ riêng 2 biến errorBalanceOrig (49.9%) và newbalanceOrig (47.2%) đã chiếm tới 97.1% tổng Feature Split Gains!** Nhóm cũng thẳng thắn ghi nhận việc mô hình dựa 98.5% vào số dư là rủi ro simulator artifact theo Mục 3.6.2. Toàn bộ các bước chuẩn hóa chỉ fit trên tập Train để đảm bảo nguyên tắc Leak-Free.

Sau đây, em xin chuyển lại phần trình bày cho bạn **Hoàng Cao Sơn** tiếp tục với nội dung SMOTE và ADASYN ở slide tiếp theo ạ.

---

### SLIDE 9 – XỬ LÝ MẤT CÂN BẰNG LỚP: SMOTE và ADASYN

_(Thời lượng chuẩn hóa: **~75s – 80s** [Meeting thực tế: ~153s] | Người nói: **Hoàng Cao Sơn** - Imbalance & Random Forest Lead)_

Cảm ơn Thanh. Chào Thầy và các bạn, sau khi bạn Thanh đã trích xuất 14 đặc trưng, mình tiếp nhận bài toán và xử lý thách thức cốt lõi đầu tiên: **Dữ liệu bị mất cân bằng (Imbalanced Data) cực đoan ~0.13%**.

Nhìn vào khung cảnh báo màu đỏ ở trên cùng: Đây là **Accuracy Paradox (nghịch lý độ chính xác)**. Nếu mô hình ngây thơ đoán 100% giao dịch là bình thường thì **Accuracy (độ chính xác tổng thể)** vẫn đạt 99.87% nhưng bỏ sót toàn bộ gian lận. Do đó, việc đánh giá bắt buộc phải dẫn dắt bởi **Precision (độ chuẩn xác)**, **Recall (độ phủ)**, **F1-Score** và **PR-AUC**.

Để cân bằng dữ liệu, mình đưa 2 kỹ thuật sinh mẫu vào đối chuẩn:
- Ở khung màu xanh bên trái: Như công thức hiển thị, bản chất của **SMOTE (Kỹ thuật nội suy mẫu tổng hợp)** là nội suy mẫu nhân tạo dọc theo đoạn thẳng nối các láng giềng **k-NN (k láng giềng gần nhất)**, tạo ra đường biên phân tách phẳng và rõ nét. Điểm mấu chốt là mình dùng biến thể **SMOTENC (Nominal & Continuous - biến định danh và liên tục)** để bảo toàn nguyên vẹn giá trị 0-1 của các cờ nhị phân.
- Ngược lại, ở khung màu xám bên phải là **ADASYN (Lấy mẫu thích ứng theo mật độ)**: Do cố sinh mẫu theo mật độ vùng biên khó, mà kẻ gian lại ngụy trang tinh vi, ADASYN đã đẻ mẫu quá đà ở vùng chồng lấn nhiễu, làm tăng **False Positives (báo động giả)**.

👉 **Chốt lại:** Mình chọn **SMOTENC**, tạo ra tập train cân bằng **230.145 dòng** (theo tỷ lệ 1:2 tối ưu), triệt tiêu tối đa báo động giả.

---

### SLIDE 10 – PHẦN 3: PHƯƠNG PHÁP & MÔ HÌNH HỌC MÁY

_(Thời lượng chuẩn hóa: **~10s** [Meeting thực tế: ~10s] | Người nói: **Hoàng Cao Sơn**)_

Tiếp theo, mình xin đi vào Phần 3: Kiến trúc Pipeline chuẩn Leak-Free và Mô hình Random Forest do mình huấn luyện.

---

### SLIDE 11 – KIẾN TRÚC PIPELINE CHUẨN LEAK-FREE

_(Thời lượng chuẩn hóa: **~85s – 90s** [Meeting thực tế: ~140s] | Người nói: **Hoàng Cao Sơn**)_

Bước sang slide tiếp theo là kiến trúc **Pipeline (chuỗi quy trình xử lý)** gồm 6 bước của nhóm (từ Lọc dữ liệu, Trích xuất đặc trưng, Chia tập, Tái lấy mẫu, Huấn luyện đến Đánh giá), được thiết kế để triệt tiêu hoàn toàn nguy cơ **Data Leakage (rò rỉ dữ liệu)**.

Mọi người có thể thấy **4 quy chuẩn bảo vệ nghiêm ngặt** ở khung bên dưới:
1. **Stratified Split (chia phân tầng) 80/20** được chốt chặn trước bất kỳ bước tái lấy mẫu hay chuẩn hóa nào.
2. **Resampling (tái lấy mẫu)** ở Bước 4 **tuyệt đối chỉ chạy trên tập Train (huấn luyện)**; tập **Test (kiểm thử)** 40.000 mẫu được giữ nguyên vẹn 100% tỷ lệ thực tế ngoài đời, không một mẫu nhân tạo nào được lọt vào.
3. **StandardScaler (chuẩn hóa độ lệch chuẩn)** chỉ fit (học tham số) trên Train rồi mới transform (áp dụng chuyển đổi) mù sang Test.
4. Toàn bộ khâu chọn ngưỡng và dò **Hyperparameters (siêu tham số)** đều dùng **Cross-Validation (kiểm định chéo)** nội bộ trên Train, không chạm vào Test.

Nhờ 4 nguyên tắc này, toàn bộ kết quả thực nghiệm của nhóm đều đảm bảo tính khách quan và trung thực tuyệt đối.

---

### SLIDE 12 – MÔ HÌNH GIÁM SÁT: RANDOM FOREST và XGBOOST

_(Thời lượng chuẩn hóa: **~154s** [Sơn ~40s, Cẩm ~114s / 258 từ] [Meeting thực tế: ~200s] | Người nói: **Hoàng Cao Sơn** [phần RF] & **Bùi Thị Mỷ Cẩm** [phần XGB])_

_(Phần 1 - Random Forest: **Hoàng Cao Sơn** trình bày - ~40s)_

Ở nửa bên trái là mô hình **Random Forest (Rừng ngẫu nhiên)** do mình huấn luyện.

Về kiến trúc, mô hình tập hợp **200 Decision Trees (cây quyết định độc lập)** theo cơ chế **Ensemble Bagging (học kết hợp đóng bao)**, phân nhánh tối ưu theo độ tinh khiết **Gini** như công thức trên slide. Để chống **Overfitting (học vẹt)**, mình khống chế độ sâu tối đa max_depth = 20.

🎯 **Kết quả thực nghiệm nổi bật:**
- **Peak Precision (độ chuẩn xác đỉnh cao) đạt 99.94%:** Trong 38.357 giao dịch hợp lệ, mô hình chỉ báo nhầm duy nhất **đúng 1 ca**!
- **F1-Score đạt 0.9973:** Đưa Random Forest trở thành mô hình có độ chính xác cao nhất toàn đồ án.
- **Hạn chế:** Thời gian huấn luyện khá lâu, mất gần 20 phút (~1187 giây).

Để giải quyết bài toán tốc độ, phần tiếp theo sẽ do bạn **Bùi Thị Mỷ Cẩm** trình bày về mô hình XGBoost.

_(Phần 2 - XGBoost: **Bùi Thị Mỷ Cẩm** tiếp lời — ~50s [~110 từ])_

Dạ em cảm ơn anh Sơn. Em chào Thầy và các bạn!

Ở khung bên phải, mô hình **XGBoost** là lời giải tối ưu về tốc độ triển khai thực tế so với 20 phút của Random Forest:

- **Về cơ chế:** XGBoost xây dựng chuỗi cây nối tiếp sửa lỗi theo Gradient bậc 1 và Hessian bậc 2, kết hợp hàm phạt L2 để triệt tiêu Overfitting.
- **Về hiệu năng:** Mô hình đạt **F1-Score 99.63%** — tương đương Random Forest — nhưng thời gian huấn luyện chỉ **57.94 giây**, tức là **nhanh hơn 20 lần**!
- **Độ trễ suy luận:** Chỉ **nửa mili-giây** cho mỗi giao dịch trên CPU, đáp ứng chuẩn xử lý thời gian thực. Vì vậy, nhóm chọn XGBoost làm động cơ suy luận chính cho hệ thống demo.

---

### SLIDE 13 – MÔ HÌNH KHÔNG GIÁM SÁT: DEEP AUTOENCODER

_(Thời lượng chuẩn hóa: **~55s** [~130 từ] | Người nói: **Bùi Thị Mỷ Cẩm** - Modeling XGB & Autoencoder Lead)_

Tuy nhiên, cả Random Forest và XGBoost đều là học có giám sát, phụ thuộc hoàn toàn vào nhãn cũ. Để chủ động phát hiện hành vi gian lận mới chưa từng có nhãn, em phát triển mạng **Deep Autoencoder** theo hướng **học không giám sát (Unsupervised)**:

- **Cấu trúc mạng:** Gồm 5 lớp ẩn đối xứng 14 → 16 → 8 → 4 → 8 → 16 → 14. Nút cổ chai 4 chiều hẹp buộc mạng phải cô đọng bản chất dòng tiền an toàn.
- **Cơ chế phát hiện:** Mạng chỉ train trên giao dịch hợp lệ. Khi gặp giao dịch gian lận dị biệt, mạng không thể tái tạo khiến sai số MSE tăng vọt. Hệ thống sẽ gắn cờ khi sai số vượt ngưỡng τ = 0.0455.
- **Hiệu năng:** Dù không dùng nhãn khi train, Autoencoder vẫn đạt **Recall 75.23%** (bắt trúng 1,236 ca gian lận). Nhóm định vị đây là lớp phòng thủ thứ hai (**Defense-in-Depth**) để kích hoạt xác thực OTP hoặc chuyển chuyên viên rà soát.

Sau đây, em xin mời bạn **Khang** trình bày bảng so sánh đối chuẩn giữa các mô hình ở Slide tiếp theo ạ.

---

### SLIDE 14 – PHẦN 4: KẾT QUẢ THỰC NGHIỆM & PHÂN TÍCH

_(Thời lượng chuẩn hóa: **~25s** [Meeting thực tế: ~25s] | Người nói: **Nguyễn Duy Khang** - Evaluation & Metrics Lead)_

Dạ em cảm ơn chị Cẩm. Em chào Thầy và các bạn, sau đây em xin trình bày kết quả kiểm thử độc lập và đối chuẩn so sánh chéo giữa các mô hình ở các slide tiếp theo ạ.

---

### SLIDE 15 – KẾT QUẢ THỰC NGHIỆM: BẢNG SO SÁNH ĐA CHỈ SỐ

_(Thời lượng chuẩn hóa: **~45s – 50s** | Người nói: **Nguyễn Duy Khang**)_

Nhìn vào bảng so sánh bên trái, thầy và các bạn có thể thấy hai mô hình cây là **Random Forest** và **XGBoost** đều đạt F1-Score trên **99.5%**, tức là bắt gần như trọn gian lận mà rất ít báo động nhầm. Random Forest nhỉnh hơn một chút, với F1 là **99.73%**.

Điểm khác biệt nằm ở thời gian huấn luyện: XGBoost chỉ mất **chưa tới một phút**, còn Random Forest mất gần 20 phút, tức là nhanh hơn khoảng **20 lần**.

Riêng **Autoencoder** học hoàn toàn không cần nhãn nhưng vẫn bắt được khoảng **75%** số vụ gian lận, nên đóng vai trò lớp phòng thủ dự phòng.

Ở biểu đồ bên phải, hai mô hình cây gần như đạt tối đa cả ba chỉ số, còn Autoencoder chủ động chấp nhận Precision thấp, khoảng 38%, để giữ Recall cao. Đây là đánh đổi có chủ đích: *"Thà cảnh báo nhầm để xác thực thêm một bước OTP, còn hơn bỏ lọt tội phạm tài chính"*.

---

### SLIDE 16 – PHÂN TÍCH MA TRẬN NHẦM LẪN & ĐÁNH ĐỔI SAI SỐ

_(Thời lượng chuẩn hóa: **~45s – 50s** | Người nói: **Nguyễn Duy Khang**)_

Đây là **Ma trận nhầm lẫn** của các mô hình trên 40,000 mẫu kiểm thử độc lập.

Với **Random Forest**, trong 1,643 vụ gian lận thật, mô hình bắt trúng 1,635 vụ, chỉ để lọt **8 vụ**, và trên hơn 38 nghìn giao dịch bình thường chỉ cảnh báo nhầm **đúng 1 ca**. **XGBoost**, mô hình nhóm chọn đưa vào sản xuất, cũng bắt trúng 1,635 vụ và bỏ lọt 8 vụ, chỉ cảnh báo nhầm **4 ca**, nhưng huấn luyện nhanh hơn nhiều và độ trễ chỉ cỡ nửa mili-giây.

Còn **Autoencoder** bắt được **1,236 vụ** mà không cần nhãn, đóng vai trò màng lọc thứ cấp cho các kiểu tấn công lạ. Đổi lại, mô hình vẫn bỏ lọt 407 vụ và cảnh báo nhầm cỡ **5%** giao dịch. Với ngân hàng thì con số này vẫn chấp nhận được, vì chỉ cần chuyển các giao dịch đó sang bước xác thực OTP.

---

### SLIDE 17 – PHÂN TÍCH ĐÓNG GÓP ĐẶC TRƯNG (FEATURE IMPORTANCE)

_(Thời lượng chuẩn hóa: **~45s – 50s** | Người nói: **Nguyễn Duy Khang**)_

Tiếp theo là **Độ quan trọng của đặc trưng**, tức là mô hình XGBoost dựa vào thông tin nào nhiều nhất để ra quyết định.

Nhìn vào biểu đồ, hai đặc trưng đứng đầu là **errorBalanceOrig**, tức sai lệch số dư nguồn, chiếm khoảng **50%**, và **newbalanceOrig**, tức số dư về 0 sau khi rút cạn, chiếm khoảng **47%**. Gộp lại, riêng hai đặc trưng này đã chiếm tới **97%** sức mạnh phân loại. Số tiền giao dịch hay khung giờ đêm gần như không đóng góp đáng kể.

Điều này cho thấy mô hình bám rất chặt vào dấu vết sai lệch số dư. Tuy nhiên, nhóm cũng lưu ý đây là đặc thù của dữ liệu mô phỏng PaySim, nên chưa thể khẳng định kết quả này giữ nguyên ngoài thực tế.

Tiếp theo, em xin mời chị **Mỷ Cẩm** giải thích phần chọn ngưỡng của mô hình Autoencoder ở slide tiếp theo ạ.

---

### SLIDE 18 – PHÂN BỐ SAI SỐ TÁI TẠO & NGƯỠNG ANOMALY

_(Thời lượng chuẩn hóa: **~55s** [~130 từ] | Người nói: **Bùi Thị Mỷ Cẩm**)_

Dạ em cảm ơn bạn Khang. Đây là quyết định kỹ thuật then chốt của mô hình Autoencoder: **Xác định ngưỡng cảnh báo τ (Anomaly Cutoff)**:

- **Phân bố sai số:** Biểu đồ bên trái cho thấy hơn 92% giao dịch hợp lệ tập trung ở sai số rất thấp dưới 0.02. Vùng chồng lấn giữa hai phân bố khiến mô hình để lọt 407 ca, buộc nhóm phải cân đối giữa báo động giả và bỏ sót gian lận.
- **Chiến lược chọn ngưỡng:** Nhóm quét ngưỡng trên tập Validation tách từ Train để đảm bảo Leak-Free, đặt ràng buộc tiên quyết **Recall tối thiểu ≥ 60%** vì bỏ lọt gian lận nguy hiểm hơn nhiều so với báo nhầm.
- **Điểm cắt tối ưu:** Trong các ngưỡng thỏa mãn, **phân vị 95th (τ = 0.0455)** đạt F1 cao nhất. Khi kiểm định mù trên tập Test độc lập, ngưỡng này mang lại **Recall 75.23%** và **Precision 38.22%**.

Tóm lại, Autoencoder và XGBoost bổ trợ chặt chẽ trong kiến trúc phòng thủ đa tầng. Tiếp theo, em xin mời bạn **Trung** trình diễn hệ thống Demo ở slide tiếp theo ạ. Mời anh Trung!

---

### SLIDE 19 – PHẦN 5: DEMO HỆ THỐNG & KẾT LUẬN

_(Trạng thái: **SLIDE BÌA CHUYỂN MỤC** — Người chuyển slide lướt qua Slide 19 trong 1–2 giây để vào thẳng Slide 20, không dừng lại nói thoại để tiết kiệm thời lượng)_

---

### SLIDE 20 – HỆ THỐNG DEMO STREAMLIT & ĐÓNG GÓP CỐT LÕI

_(Thời lượng chuẩn hóa: **~3 phút 00s** [Trung dẫn nhập ~10s, Trình diễn Demo 2m17s, Tổng kết 4 đóng góp & Cảm ơn ~33s] | Người nói: **Phạm Thành Trung** [Phụ trách toàn bộ Slide 20 & Kết bài])_

Dạ em cảm ơn bạn Cẩm. Em chào Thầy và các bạn!

Ở phần cuối này, em xin đại diện nhóm trình diễn hệ thống **Dashboard giám sát gian lận thời gian thực xây dựng trên nền tảng Streamlit**, kết nối trực tiếp mô hình XGBoost-SMOTE và bộ chuẩn hóa StandardScaler đã huấn luyện. 

Sau đây, em xin mời Thầy và các bạn cùng theo dõi ạ.

---

#### 🔹 PHẦN 1: TRÌNH DIỄN DEMO TRÊN SLIDE 20 (~2 phút 17 giây)

*(Phạm Thành Trung kích hoạt phần trình diễn demo trực tiếp trên Slide 20 của PowerPoint. Bản demo mô phỏng 3 kịch bản kiểm thử thực tế và dừng lại ở kết quả cảnh báo gian lận).*

---

#### 🔹 PHẦN 2: TIẾP NỐI SAU DEMO – TỔNG KẾT ĐÓNG GÓP, HƯỚNG PHÁT TRIỂN & KẾT BÀI (~35s)

*(Ngay khi phần demo kết thúc tại câu "...để ưu tiên đưa vào quá trình rà soát" với cờ đỏ 88.36%, Phạm Thành Trung cầm micro tiếp lời liền mạch)*

Dạ như Thầy và các bạn vừa theo dõi qua demo thực tế, mô hình XGBoost đã bắt trọn dấu hiệu sai lệch số dư và rút cạn ví ở kịch bản rủi ro cao với xác suất 88.36%, đồng thời phản hồi siêu tốc dưới 0.5 mili-giây cho cả 3 cấp độ.

Để khép lại bài báo cáo hôm nay, em xin tổng kết **4 đóng góp kỹ thuật cốt lõi** của đồ án:

1. **Pipeline chuẩn mực Leak-Free 100%**, phân lập triệt để dữ liệu kiểm thử độc lập.
2. **Kỹ thuật 14 đặc trưng miền kế toán**, trong đó Top 2 đặc trưng số dư giải thích tới **97.1%** sức mạnh phân loại.
3. **Hiệu năng thực nghiệm vượt trội:** **F1-Score 99.73%** (Random Forest) và mô hình triển khai **XGBoost 57.94s siêu tốc (nhanh hơn ~20 lần so với Random Forest)**, độ trễ suy luận cỡ nửa mili-giây.
4. **Kiến trúc phòng thủ đa tầng**, kết hợp Deep Autoencoder phát hiện bất thường luồng tiền không cần nhãn (Defense-in-Depth).

Về hướng phát triển dài hạn, nhóm định hướng mở rộng sang **Graph Neural Networks (GraphSAGE)** để bóc tách mạng lưới rửa tiền đa tài khoản, và tích hợp Apache Kafka để xử lý luồng dữ liệu lớn hàng trăm ngàn giao dịch/giây.

---

### SLIDE 21 – TỔNG KẾT, TÀI LIỆU THAM KHẢO & PHIÊN HỎI ĐÁP (Q&A)

_(Trạng thái: **SLIDE DỰ BỊ / PHÔNG NỀN Q&A** | Người nói: **Phạm Thành Trung**)_

Dạ, toàn bộ mã nguồn chương trình, bộ dữ liệu thực nghiệm đã xử lý, tài liệu kỹ thuật, báo cáo Word và slide thuyết trình đã được nhóm chúng em đóng gói và phát hành đầy đủ trên repository của đồ án.

Thay mặt toàn thể 7 thành viên Nhóm 09, em xin chân thành cảm ơn Thầy và các bạn đã chú ý theo dõi phần trình bày của nhóm. Sau đây, nhóm chúng em xin trân trọng kính mời Thầy và hội đồng bắt đầu phiên hỏi đáp phản biện Q&A ạ!

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
