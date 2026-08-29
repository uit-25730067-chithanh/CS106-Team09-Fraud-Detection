# HỆ THỐNG PHÁT HIỆN GIAO DỊCH TÀI CHÍNH BẤT THƯỜNG VÀ NGHI VẤN GIAN LẬN

**Môn học:** CS106 — Trí tuệ Nhân tạo  
**Nhóm:** 9  
**Người soạn bản nháp Sprint 2:** Vũ Văn Duy — MSSV 26410031 — Lớp A  
**Phiên bản:** Bản nháp Sprint 2 — Chương 1, 2 và 3  
**Ngày cập nhật:** 29/08/2026

| STT | Họ và tên | MSSV | Lớp |
|---:|---|---:|:---:|
| 1 | Trần Hoàng Hôn | 26410046 | A |
| 2 | Nguyễn Duy Khang | 26410055 | A |
| 3 | Vũ Văn Duy | 26410031 | A |
| 4 | Phạm Thành Trung | 26410141 | A |
| 5 | Đặng Chí Thanh | 25730067 | B |
| 6 | Bùi Thị Mỷ Cẩm | 25730013 | B |
| 7 | Hoàng Cao Sơn | 25730061 | B |

> Phạm vi bản nháp Sprint 2: Introduction, Problem Statement và Dataset Description. Các phần Methodology, Results, Discussion, Conclusion và Abstract sẽ được hoàn thiện ở Sprint 3–4 sau khi nhận evidence từ các phase modeling và evaluation.

---

# CHƯƠNG 1. GIỚI THIỆU

## 1.1. Bối cảnh

Sự phát triển của các hệ thống thương mại điện tử, thanh toán trực tuyến và dịch vụ tài chính trên thiết bị di động làm cho số lượng giao dịch điện tử tăng nhanh. Song song với sự thuận tiện đó, các tổ chức tài chính phải đối mặt với những hành vi gian lận ngày càng đa dạng. Một hệ thống phát hiện gian lận không chỉ cần nhận biết các giao dịch có dấu hiệu bất thường mà còn phải hạn chế cảnh báo nhầm đối với giao dịch hợp lệ. Các khảo sát trong lĩnh vực cho thấy phát hiện gian lận là một bài toán phức tạp vì dữ liệu thường có quy mô lớn, phân bố lệch, thay đổi theo thời gian và có thể tạo ra nhiều cảnh báo giả.[1]

Trong bài toán phân loại giao dịch, mỗi giao dịch được mô tả bởi một tập đặc trưng như thời điểm, loại giao dịch, số tiền và biến động số dư. Hệ thống học máy nhận các đặc trưng này và dự đoán giao dịch thuộc lớp hợp lệ hay gian lận. Khác với bài toán phân loại cân bằng, số giao dịch gian lận thường rất nhỏ so với số giao dịch bình thường. Nếu chỉ tối ưu Accuracy, một mô hình dự đoán tất cả giao dịch là bình thường vẫn có thể đạt tỷ lệ đúng cao nhưng không đáp ứng mục tiêu phát hiện gian lận.

Một khó khăn khác là dữ liệu giao dịch thực tế có tính nhạy cảm cao và ít khi được công bố. Công trình PaySim được xây dựng nhằm tạo dữ liệu giao dịch mobile money tổng hợp dựa trên đặc tính thống kê của dữ liệu thật, qua đó hỗ trợ nghiên cứu mà không công khai nhật ký giao dịch riêng tư.[2] Bộ dữ liệu PaySim trên Kaggle vì vậy phù hợp với phạm vi học thuật của đề tài, nhưng kết quả thu được cần được diễn giải trong giới hạn của dữ liệu mô phỏng.[3]

## 1.2. Lý do chọn đề tài

Đề tài “Hệ thống phát hiện giao dịch tài chính bất thường và nghi vấn gian lận” kết hợp nhiều nội dung quan trọng của môn Trí tuệ Nhân tạo: biểu diễn dữ liệu, tiền xử lý, học có giám sát, phát hiện bất thường, xử lý dữ liệu mất cân bằng và đánh giá mô hình. Đây cũng là bài toán có ý nghĩa thực tiễn rõ ràng vì quyết định của mô hình liên quan trực tiếp đến hai loại rủi ro:

- **False Negative:** giao dịch gian lận không được phát hiện, có thể gây thiệt hại tài chính.
- **False Positive:** giao dịch hợp lệ bị gắn cờ nhầm, làm gián đoạn trải nghiệm người dùng và tăng chi phí kiểm tra.

Do đó, nhóm không sử dụng Accuracy như tiêu chí duy nhất. Báo cáo tập trung vào Precision, Recall, F1-Score và ROC-AUC theo yêu cầu của đề bài. Các chỉ số này cho phép phân tích rõ hơn khả năng phát hiện lớp gian lận và sự đánh đổi giữa bỏ sót với cảnh báo nhầm.

## 1.3. Mục tiêu đề tài

### 1.3.1. Mục tiêu tổng quát

Xây dựng và đánh giá một quy trình học máy có khả năng phân loại giao dịch tài chính mobile money thành hai nhóm: giao dịch hợp lệ và giao dịch có dấu hiệu gian lận.

### 1.3.2. Mục tiêu cụ thể

1. Khảo sát và mô tả bộ dữ liệu PaySim, bao gồm cấu trúc, phân bố loại giao dịch và tỷ lệ gian lận.
2. Xây dựng quy trình tiền xử lý có thể tái sử dụng: lọc dữ liệu, tạo đặc trưng, mã hóa biến phân loại, chuẩn hóa và chia train/test.
3. Khảo sát các kỹ thuật xử lý mất cân bằng như SMOTE và ADASYN trên tập huấn luyện; không thay đổi tập kiểm tra.
4. Thử nghiệm ít nhất hai thuật toán trong số Random Forest, XGBoost và Autoencoder theo yêu cầu đề bài.
5. Đánh giá mô hình bằng Precision, Recall, F1-Score, ROC-AUC và các biểu đồ phù hợp.
6. So sánh mô hình, phân tích hạn chế và đề xuất hướng phát triển.
7. Chuẩn bị một giao diện minh họa để nhập thông tin giao dịch và hiển thị dự đoán khi mô hình cuối đã sẵn sàng.

> Ở thời điểm Sprint 2, mục tiêu 1 và phần preprocessing của mục tiêu 2 đã có evidence từ Phase 00–01. Các mục tiêu modeling, evaluation và demo vẫn là mục tiêu dự kiến, chưa được trình bày như kết quả hoàn thành.

## 1.4. Đối tượng và phạm vi nghiên cứu

- **Đối tượng nghiên cứu:** giao dịch mobile money trong bộ dữ liệu tổng hợp PaySim.
- **Bài toán:** phân loại nhị phân, với `isFraud = 0` là giao dịch bình thường và `isFraud = 1` là giao dịch gian lận.
- **Phạm vi dữ liệu:** bộ dữ liệu PaySim công khai trên Kaggle; tập làm việc của nhóm được lọc còn hai loại `TRANSFER` và `CASH_OUT`, sau đó downsample còn 200.000 giao dịch.
- **Phạm vi thuật toán:** dự kiến Random Forest, XGBoost và Autoencoder; SMOTE/ADASYN được xem xét để xử lý mất cân bằng trên train set.
- **Phạm vi đánh giá:** đánh giá trên test set được tách từ tập 200.000 giao dịch đã downsample.
- **Ngoài phạm vi:** triển khai production, xử lý giao dịch thời gian thực, kết nối hệ thống ngân hàng thật và khẳng định hiệu quả trên dữ liệu tài chính thực tế.

## 1.5. Cấu trúc báo cáo dự kiến

- Chương 1 giới thiệu bối cảnh, mục tiêu và phạm vi.
- Chương 2 phát biểu bài toán và các yêu cầu kỹ thuật.
- Chương 3 mô tả dữ liệu và kết quả EDA.
- Chương 4 trình bày phương pháp tiền xử lý, xử lý mất cân bằng và các mô hình.
- Chương 5 trình bày kết quả thực nghiệm.
- Chương 6 thảo luận kết quả và hạn chế.
- Chương 7 kết luận và hướng phát triển.
- Phần cuối gồm tài liệu tham khảo và phụ lục mô tả chương trình.

---

# CHƯƠNG 2. PHÁT BIỂU BÀI TOÁN

## 2.1. Mô tả bài toán

Cho tập dữ liệu giao dịch tài chính, mỗi giao dịch được biểu diễn bởi vector đặc trưng $x$. Mục tiêu là xây dựng hàm dự đoán $f(x)$ trả về một trong hai nhãn:

- $f(x) = 0$: giao dịch hợp lệ;
- $f(x) = 1$: giao dịch gian lận.

Trong dữ liệu sau Phase 01, vector đầu vào cuối cùng gồm chín đặc trưng: `step`, `amount`, `oldbalanceOrg`, `newbalanceOrig`, `oldbalanceDest`, `newbalanceDest`, `errorBalanceOrig`, `errorBalanceDest` và `type_TRANSFER`. Nhãn cần dự đoán là `isFraud`.

Vì tỷ lệ gian lận thấp hơn nhiều so với giao dịch bình thường, bài toán không chỉ là tìm một đường phân tách giữa hai lớp. Mô hình còn phải học được tín hiệu của lớp thiểu số trong khi hạn chế cảnh báo nhầm. Việc lựa chọn cách lấy mẫu, thuật toán và ngưỡng dự đoán có thể làm thay đổi cân bằng giữa Precision và Recall.

## 2.2. Đầu vào và đầu ra

### Đầu vào

Một giao dịch sau khi tiền xử lý, gồm:

- thời điểm giao dịch theo đơn vị `step`;
- số tiền giao dịch;
- số dư tài khoản nguồn trước và sau giao dịch;
- số dư tài khoản đích trước và sau giao dịch;
- hai đặc trưng chênh lệch số dư được tạo mới;
- loại giao dịch được mã hóa thành `type_TRANSFER`.

### Đầu ra

- Nhãn dự đoán `0` hoặc `1`.
- Xác suất/điểm bất thường nếu mô hình hỗ trợ.
- Trong demo cuối: thông báo giao dịch bình thường hoặc có nghi vấn gian lận.

## 2.3. Các thách thức chính

### 2.3.1. Mất cân bằng lớp

Dữ liệu PaySim gốc có 8.213 giao dịch gian lận trên tổng số 6.362.620 giao dịch, tương đương khoảng 0,129082%. Tỷ lệ này khiến lớp gian lận dễ bị lấn át khi huấn luyện. Nhóm đã downsample lớp bình thường để tạo tập làm việc có 200.000 dòng và tỷ lệ gian lận khoảng 4,1065%. Thao tác này giúp giảm chi phí tính toán nhưng làm thay đổi phân bố lớp so với dữ liệu gốc, vì vậy kết quả phải được diễn giải thận trọng.

### 2.3.2. Chi phí của hai loại sai số

False Negative và False Positive không có tác động giống nhau. Bỏ sót giao dịch gian lận có thể dẫn đến tổn thất, trong khi cảnh báo nhầm làm tăng chi phí xác minh và ảnh hưởng người dùng. Do đề bài chưa đưa ra ma trận chi phí cụ thể, nhóm sẽ báo cáo nhiều chỉ số thay vì kết luận dựa trên một metric duy nhất.

### 2.3.3. Rò rỉ dữ liệu

Các bước học tham số từ dữ liệu, chẳng hạn StandardScaler hoặc kỹ thuật sinh mẫu, chỉ được fit trên tập train. Tập test phải được giữ độc lập để phản ánh khả năng tổng quát hóa. Phase 01 đã thực hiện split trước khi fit StandardScaler. SMOTE/ADASYN ở các phase sau cũng phải chỉ được áp dụng trên train set.

### 2.3.4. Dữ liệu mô phỏng

PaySim được sinh bằng mô phỏng dựa trên dữ liệu mobile money tổng hợp từ thống kê của nhật ký thật.[2][3] Vì vậy, mô hình có thể học các quy luật đặc trưng của simulator thay vì toàn bộ hành vi phức tạp trong hệ thống tài chính thực. Đây là giới hạn ngoại suy quan trọng của đề tài.

## 2.4. Yêu cầu kỹ thuật

Theo đề bài môn học, hệ thống cần:

1. Sử dụng bộ dữ liệu công khai hoặc synthetic với tối thiểu 500 giao dịch.
2. Tiền xử lý và chuẩn hóa dữ liệu định lượng.
3. Thử nghiệm ít nhất hai thuật toán trong số Random Forest, XGBoost hoặc Autoencoder.
4. Xử lý mất cân bằng bằng SMOTE, ADASYN hoặc class weights.
5. Đánh giá bằng Precision, Recall, F1-Score và ROC-AUC; không dùng Accuracy đơn thuần.
6. Có code, báo cáo khoa học, mô tả chương trình và demo/hình ảnh nếu có.

## 2.5. Câu hỏi nghiên cứu

Báo cáo hướng tới trả lời các câu hỏi sau khi hoàn tất thực nghiệm:

- Kỹ thuật xử lý mất cân bằng nào phù hợp hơn trên tập PaySim đã tiền xử lý?
- Trong các mô hình được thử nghiệm, mô hình nào đạt cân bằng tốt nhất giữa Precision và Recall cho lớp fraud?
- Các đặc trưng nào đóng góp nhiều nhất vào quyết định của mô hình, và các đặc trưng này có nguy cơ phản ánh cơ chế mô phỏng của PaySim hay không?

---

# CHƯƠNG 3. MÔ TẢ DỮ LIỆU

## 3.1. Nguồn dữ liệu

Nhóm sử dụng bộ “Synthetic Financial Datasets for Fraud Detection” do Edgar Lopez-Rojas công bố trên Kaggle.[3] Bộ dữ liệu được sinh từ PaySim, một simulator giao dịch mobile money dựa trên đặc tính của một mẫu nhật ký giao dịch thực. Công trình gốc mô tả PaySim như một cách tạo dữ liệu tổng hợp để hỗ trợ nghiên cứu trong bối cảnh dữ liệu tài chính thật khó tiếp cận vì tính riêng tư.[2]

Theo data card, mỗi `step` tương ứng một giờ và bộ dữ liệu mô phỏng khoảng một tháng hoạt động. Năm loại giao dịch gồm `CASH_IN`, `CASH_OUT`, `DEBIT`, `PAYMENT` và `TRANSFER`.[3]

## 3.2. Cấu trúc dữ liệu gốc

| Thuộc tính | Kiểu/nhóm | Ý nghĩa |
|---|---|---|
| `step` | Thời gian | Một đơn vị tương ứng một giờ mô phỏng |
| `type` | Phân loại | Loại giao dịch |
| `amount` | Định lượng | Số tiền giao dịch |
| `nameOrig` | Định danh | Tài khoản khởi tạo giao dịch |
| `oldbalanceOrg` | Định lượng | Số dư nguồn trước giao dịch |
| `newbalanceOrig` | Định lượng | Số dư nguồn sau giao dịch |
| `nameDest` | Định danh | Tài khoản nhận |
| `oldbalanceDest` | Định lượng | Số dư đích trước giao dịch |
| `newbalanceDest` | Định lượng | Số dư đích sau giao dịch |
| `isFraud` | Nhãn | 1 là fraud, 0 là normal |
| `isFlaggedFraud` | Cờ nghiệp vụ | Cờ giao dịch chuyển khoản lớn theo rule của simulator |

Notebook EDA xác nhận file gốc có **6.362.620 dòng và 11 cột**, không có giá trị thiếu trong 11 cột được kiểm tra. Tập dữ liệu gồm **6.354.407 giao dịch bình thường** và **8.213 giao dịch gian lận**.

## 3.3. Phân bố giao dịch và nhãn

| Loại giao dịch | Normal | Fraud | Tổng |
|---|---:|---:|---:|
| `CASH_IN` | 1.399.284 | 0 | 1.399.284 |
| `CASH_OUT` | 2.233.384 | 4.116 | 2.237.500 |
| `DEBIT` | 41.432 | 0 | 41.432 |
| `PAYMENT` | 2.151.495 | 0 | 2.151.495 |
| `TRANSFER` | 528.812 | 4.097 | 532.909 |
| **Tổng** | **6.354.407** | **8.213** | **6.362.620** |

Trong lần chạy EDA hiện tại, toàn bộ fraud xuất hiện ở `TRANSFER` và `CASH_OUT`. Đây là cơ sở để Phase 01 lọc hai loại giao dịch này trước khi downsample. Nhận định này là đặc điểm quan sát được trong bộ PaySim cụ thể, không nên diễn giải thành quy luật chung cho mọi hệ thống tài chính.

## 3.4. Downsampling và chia tập

Để giảm yêu cầu bộ nhớ và thời gian huấn luyện, pipeline giữ toàn bộ 8.213 giao dịch fraud và lấy mẫu ngẫu nhiên 191.787 giao dịch normal với `random_state = 42`. Tập làm việc sau downsample có đúng 200.000 giao dịch.

| Tập dữ liệu | Normal | Fraud | Tổng | Fraud ratio |
|---|---:|---:|---:|---:|
| Dữ liệu gốc | 6.354.407 | 8.213 | 6.362.620 | 0,129082% |
| Sau downsample | 191.787 | 8.213 | 200.000 | 4,106500% |
| Train | 153.430 | 6.570 | 160.000 | 4,106250% |
| Test | 38.357 | 1.643 | 40.000 | 4,107500% |

Train/test được chia theo tỷ lệ 80/20 bằng stratified split. Chỉ số stratified giúp tỷ lệ fraud của hai tập gần nhau. Tập test chưa được áp dụng SMOTE/ADASYN và phải tiếp tục được giữ nguyên trong các phase sau.

## 3.5. Các đặc trưng sau Phase 01

Phase 01 loại `nameOrig`, `nameDest` và `isFlaggedFraud`; mã hóa `type`; đồng thời tạo hai đặc trưng chênh lệch số dư:

- `errorBalanceOrig = oldbalanceOrg - amount - newbalanceOrig`;
- `errorBalanceDest = oldbalanceDest + amount - newbalanceDest`.

Tám biến định lượng được StandardScaler fit trên train và transform trên test. Biến `type_TRANSFER` được giữ dạng nhị phân.

| # | Feature cuối | Xử lý |
|---:|---|---|
| 1 | `step` | StandardScaler |
| 2 | `amount` | StandardScaler |
| 3 | `oldbalanceOrg` | StandardScaler |
| 4 | `newbalanceOrig` | StandardScaler |
| 5 | `oldbalanceDest` | StandardScaler |
| 6 | `newbalanceDest` | StandardScaler |
| 7 | `errorBalanceOrig` | Tạo mới + StandardScaler |
| 8 | `errorBalanceDest` | Tạo mới + StandardScaler |
| 9 | `type_TRANSFER` | One-hot/dummy binary |

Artifacts đã được bàn giao qua Git gồm `X_train.pkl`, `X_test.pkl`, `y_train.pkl`, `y_test.pkl` và `models/scaler.pkl`.

## 3.6. Hạn chế và nguy cơ ảnh hưởng tính hợp lệ

### 3.6.1. Thay đổi tỷ lệ lớp

Fraud ratio tăng từ 0,129082% lên khoảng 4,1065% sau downsample. Do Precision và đường Precision–Recall phụ thuộc vào prevalence, kết quả trên test downsample không thể được trình bày như hiệu năng trên phân bố PaySim gốc hoặc trên hệ thống thật.

### 3.6.2. Cảnh báo về các cột balance

Data card của Kaggle lưu ý rằng giao dịch bị phát hiện là fraud trong simulator có thể bị hủy và cảnh báo không nên dùng các cột `oldbalanceOrg`, `newbalanceOrig`, `oldbalanceDest`, `newbalanceDest` cho fraud detection.[3] Trong Phase 01 hiện tại, pipeline vẫn sử dụng các cột balance và hai đặc trưng `errorBalance`. Vì vậy, báo cáo xem đây là một **threat to validity**: mô hình có thể học tín hiệu từ cơ chế cập nhật/hủy giao dịch của simulator. Một kiểm tra bổ sung nên so sánh mô hình có và không có nhóm balance features trước khi đưa ra kết luận cuối.

### 3.6.3. Dữ liệu tổng hợp

PaySim hỗ trợ thử nghiệm có thể tái lập nhưng không đại diện hoàn toàn cho hành vi, quy trình nghiệp vụ và chiến thuật gian lận trong môi trường thật. Kết quả của đồ án chỉ nên được xem là kết quả trên bộ dữ liệu mô phỏng.

### 3.6.4. Cách chia dữ liệu

Phase 01 dùng random stratified split thay vì temporal split hoặc group split theo tài khoản. Cách chia này phù hợp với baseline của đồ án nhưng chưa chứng minh khả năng dự báo giao dịch trong khoảng thời gian tương lai hoặc cho tài khoản chưa từng xuất hiện.

## 3.7. Kết luận chương

Bộ dữ liệu PaySim đáp ứng yêu cầu về quy mô và cung cấp nhãn fraud rõ ràng. Phase 01 đã hoàn thành EDA, downsampling, stratified split, feature engineering, encoding và scaling. Tuy nhiên, tỷ lệ lớp đã thay đổi đáng kể và nhóm balance features có nguy cơ phản ánh cơ chế của simulator. Hai vấn đề này cần được theo dõi trong Methodology và Discussion ở các sprint sau.

---

# TÀI LIỆU THAM KHẢO TẠM THỜI

Các nguồn [1]–[3] được sử dụng trực tiếp trong bản nháp Sprint 2. Danh mục sẽ được mở rộng ở Sprint 3–4 với tài liệu SMOTE, ADASYN, Random Forest, XGBoost và Autoencoder.

## Tài liệu nội bộ của dự án

- Trường Đại học Công nghệ Thông tin, “Đề tài môn Trí tuệ Nhân tạo”, mục Đề tài 7, 2026.
- Đặng Chí Thanh, `notebooks/01_eda.ipynb`, output đã thực thi ngày 28/08/2026.
- Nhóm 9, `plans/fraud-detection-full-submit/phase-01-eda-preprocessing.md`, evidence Phase 01.
- Nhóm 9, `draft/fraud-detection/data/processed/README.md`, mô tả processed artifacts.

## Sources

[1] https://doi.org/10.1016/j.jnca.2016.04.007 — Fraud detection system: A survey
[2] https://www.msc-les.org/proceedings/emss/2016/EMSS2016_249.pdf — PaySim: A Financial Mobile Money Simulator for Fraud Detection
[3] https://www.kaggle.com/datasets/ealaxi/paysim1 — Synthetic Financial Datasets for Fraud Detection
