import pptx
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_pptx = os.path.join(BASE_DIR, '[Nhom9]_Slide_FraudDetection_Academic.pptx')
output_pptx = os.path.join(BASE_DIR, '[Nhom9]_Slide_FraudDetection_Academic_VN.pptx')

prs = pptx.Presentation(input_pptx)

# Standard Academic Hybrid Mapping:
# - Professional Vietnamese natural explanations
# - Retain standard international AI/ML terminology: Pipeline, Feature Engineering, SMOTE, ADASYN, Random Forest, XGBoost, Autoencoder, Precision, Recall, F1-Score, ROC-AUC, PR-AUC, Decision Boundary, Zero-Day, Joblib, Streamlit, Latency, Data Leakage, True Fraud, False Positive, False Negative.
MAPPING = {
    # Headers & Navigation Pills & Footers
    "UIT • VNU-HCM | CS106: ARTIFICIAL INTELLIGENCE": "UIT • ĐHQG-HCM | CS106: TRÍ TUỆ NHÂN TẠO",
    "UIT • VNU-HCM | CS106 (AI)": "UIT • ĐHQG-HCM | CS106 (AI)",
    "1. Introduction": "1. Giới thiệu",
    "2. EDA & Features": "2. EDA & Features",
    "3. Methodology": "3. Phương pháp",
    "4. Evaluation": "4. Thực nghiệm",
    "5. Demo & Future": "5. Demo & Tương lai",
    "CS106: Artificial Intelligence — Team 09 — Final Project: Financial Fraud Detection": "CS106: Trí tuệ Nhân tạo — Nhóm 09 — Báo cáo Đồ án: Phát hiện Gian lận Tài chính",
    "CS106: Artificial Intelligence — Team 09 — Final Project Defense": "CS106: Trí tuệ Nhân tạo — Nhóm 09 — Báo cáo Bảo vệ Đồ án",
    "UNIVERSITY OF INFORMATION TECHNOLOGY, VNU-HCM  •  CS106 FINAL DEFENSE": "TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN, ĐHQG-HCM  •  BÁO CÁO ĐỒ ÁN CS106",

    # Slide 1: Cover
    "VIETNAM NATIONAL UNIVERSITY HO CHI MINH CITY\nUNIVERSITY OF INFORMATION TECHNOLOGY  •  FACULTY OF COMPUTER SCIENCE": "ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH\nTRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN  •  KHOA KHOA HỌC MÁY TÍNH",
    "FINANCIAL FRAUD DETECTION": "PHÁT HIỆN GIAN LẬN TÀI CHÍNH",
    "Applied Machine Learning & Deep Learning on PaySim Synthetic Dataset": "Ứng dụng Machine Learning & Deep Learning trên Tập dữ liệu PaySim",
    "Course: CS106 — Artificial Intelligence  |  Advisor: Assoc. Prof. Nguyen Dinh Hien": "Môn học: CS106 — Trí tuệ Nhân tạo  |  GVHD: PGS.TS. Nguyễn Đình Hiển",
    "TEAM 09": "NHÓM 09",
    "Tran Hoang Hon (26410046)  •  Dang Chi Thanh (25730067)  •  Nguyen Duy Khang (26410055)\nHoang Cao Son (25730061)  •  Vu Van Duy (26410031)  •  Bui Thi My Cam (25730013)  •  Pham Thanh Trung (26410141)": "Trần Hoàng Hôn (26410046)  •  Đặng Chí Thanh (25730067)  •  Nguyễn Duy Khang (26410055)\nHoàng Cao Sơn (25730061)  •  Vũ Văn Duy (26410031)  •  Bùi Thị Mỷ Cẩm (25730013)  •  Phạm Thanh Trung (26410141)",
    "Ho Chi Minh City, September 2026": "TP. Hồ Chí Minh, Tháng 09/2026",

    # Slide 2: Agenda
    "AGENDA & ROADMAP": "NỘI DUNG BÁO CÁO & LỘ TRÌNH",
    "Introduction & Problem Formulation": "Giới thiệu & Phát biểu Bài toán",
    "Financial context, extreme class imbalance, and formal task formulation.": "Bối cảnh tài chính, bài toán Extreme Class Imbalance và phát biểu bài toán.",
    "Exploratory Data Analysis & Feature Engineering": "Phân tích Khám phá Dữ liệu & Kỹ thuật Đặc trưng",
    "Category confinement, balance drain signatures, and 14 synthesized features.": "Khu biệt loại giao dịch, dấu vết rút cạn số dư và 14 engineered features.",
    "Proposed Methodologies & Machine Learning Pipeline": "Phương pháp Đề xuất & Kiến trúc Pipeline",
    "Resampling (SMOTE/ADASYN), Random Forest, XGBoost, and Deep Autoencoder.": "Kỹ thuật Resampling (SMOTE/ADASYN), Random Forest, XGBoost và Deep Autoencoder.",
    "Experiments, Results & Comparative Evaluation": "Kết quả Thực nghiệm & Đánh giá So sánh",
    "Benchmark metrics, confusion matrices, feature gains, and error trade-offs.": "Benchmark hiệu năng, Confusion Matrix, Feature Gain và phân tích sai số.",
    "Interactive System & Future Research Trajectories": "Hệ thống Demo & Định hướng Tương lai",
    "Streamlit real-time dashboard, business viability, limitations, and GNN roadmap.": "Dashboard Streamlit real-time, đóng góp cốt lõi, hạn chế và lộ trình GNN.",

    # Slide 3: Divider 1
    "PART 01": "PHẦN 01",
    "INTRODUCTION & PROBLEM FORMULATION": "GIỚI THIỆU & PHÁT BIỂU BÀI TOÁN",
    "Industrial Background & Mobile Money Expansion": "Bối cảnh Công nghiệp & Sự bùng nổ Mobile Money",
    "The Asymmetric Cost & Extreme Imbalance Paradox": "Thách thức Extreme Class Imbalance (~0.13%) & Asymmetric Cost",
    "Formal AI Problem Statement & Research Objectives": "Phát biểu Bài toán Hình thức & Mục tiêu Nghiên cứu",

    # Slide 4: Problem Motivation
    "Problem Motivation & Technical Challenges": "Động lực Nghiên cứu & Thách thức Kỹ thuật",
    "1. Industrial Context & Scale": "1. Bối cảnh Thực tiễn & Quy mô",
    "• Mobile money transactions have surged globally, introducing complex synthetic fraud vectors.": "• Giao dịch Mobile Money tăng trưởng bùng nổ, kéo theo các thủ đoạn gian lận tinh vi.",
    "• Real-time defense mechanisms require sub-100ms inference latency before funds leave the system.": "• Hệ thống phòng thủ đòi hỏi độ trễ suy luận real-time (< 100ms) trước khi dòng tiền bị rút khỏi hệ thống.",
    "2. Extreme Class Imbalance (~0.13%)": "2. Thách thức Extreme Class Imbalance (~0.13%)",
    "• Fraud accounts for only ~1 out of every 800 transactions in the PaySim universe.": "• Giao dịch gian lận chỉ chiếm ~1 trên 800 giao dịch trong tập dữ liệu PaySim.",
    "• Cost Asymmetry: False Negatives (missed fraud) lead to direct capital loss, while False Positives cause customer friction.": "• Cost Asymmetry: Bỏ sót gian lận (False Negative) gây tổn thất tài chính trực tiếp, trong khi Báo động nhầm (False Positive) gây gián đoạn trải nghiệm người dùng.",
    "3. Non-Stationary Fraud Patterns": "3. Hành vi Gian lận Phi tĩnh (Non-Stationary)",
    "• Adversaries constantly morph account routing tactics to evade static rule-based threshold filters.": "• Kẻ gian liên tục biến đổi phương thức luân chuyển tiền để lẩn tránh các bộ lọc luật tĩnh (rule-based filters).",
    "Class Target": "Class Target",
    "1 = Fraudulent, 0 = Legitimate": "1 = Fraudulent (Gian lận), 0 = Legitimate (Hợp lệ)",
    "Imbalance": "Imbalance Ratio",
    "8,213 frauds per 6.36M events": "8,213 ca gian lận trên 6.36M giao dịch",
    "1,643 frauds per 1.3M events": "8,213 ca gian lận trên 6.36M giao dịch",
    "Primary Goal": "Primary Metric",
    "Maximize rare fraud recall": "Tối đa hóa Recall trên lớp gian lận hiếm",
    "Loss Asymmetry": "Cost Asymmetry",
    "Cost penalty ratio is critical": "Trọng số phạt tổn thất bất đối xứng (C_FN >> C_FP)",
    "Research Objectives": "Mục tiêu Nghiên cứu",
    "Construct an end-to-end, leak-free ML pipeline.": "Xây dựng end-to-end ML pipeline chuẩn, đảm bảo Leak-Free tuyệt đối.",
    "Formulate domain feature equations capturing ledger state discrepancies.": "Thiết kế các phương trình domain feature bắt trọn sai lệch sổ cái tài khoản.",
    "Benchmark Ensemble Trees against Deep Unsupervised Anomaly Detection.": "Benchmark mô hình Ensemble Trees với Deep Unsupervised Autoencoder.",
    "Deploy interactive real-time decision dashboard.": "Triển khai interactive dashboard phục vụ ra quyết định thời gian thực.",

    # Slide 5: Dataset Characteristics
    "PaySim Dataset: Statistical Characteristics": "Tập Dữ liệu PaySim: Thuộc tính Thống kê",
    "Dataset Scaling": "Quy mô Mẫu sau Downsample",
    "Stratified downsampling preserving 100% fraud": "Stratified downsampling bảo toàn 100% ca gian lận",
    "Positive Instances (isFraud = 1)": "Số ca Gian lận (isFraud = 1)",
    "Ground-truth fraud transactions": "Giao dịch gian lận nhãn ground-truth",
    "11 -> 14 Features": "Không gian 14 Đặc trưng",
    "Synthesized Feature Space": "Feature Space Mở rộng",
    "Expanded with balance delta equations": "Bổ sung các phương trình sai lệch số dư",
    "Feature Name": "Tên Đặc trưng",
    "Data Type": "Kiểu Dữ liệu",
    "Domain Description & Operational Role": "Ý nghĩa Miền & Nghiệp vụ Giao dịch",
    "Integer": "Số nguyên (Integer)",
    "Time step unit in hours (1..744, representing 30 simulation days)": "Bước thời gian theo giờ (1..744, tương ứng 30 ngày mô phỏng)",
    "Categorical": "Phân loại (Categorical)",
    "Transaction category: CASH_OUT, TRANSFER, PAYMENT, CASH_IN, DEBIT": "Loại giao dịch: CASH_OUT, TRANSFER, PAYMENT, CASH_IN, DEBIT",
    "Continuous": "Liên tục (Continuous)",
    "Transaction amount in local currency units": "Số tiền thực hiện giao dịch (đơn vị tiền tệ cục bộ)",
    "Initial balance and post-transaction balance of the sender account": "Số dư trước và ngay sau giao dịch của tài khoản nguồn (sender)",
    "Initial balance and post-transaction balance of the recipient account": "Số dư trước và ngay sau giao dịch của tài khoản đích (recipient)",

    # Slide 6: Divider 2
    "PART 02": "PHẦN 02",
    "EXPLORATORY DATA ANALYSIS & FEATURE ENGINEERING": "KHÁM PHÁ DỮ LIỆU & KỸ THUẬT ĐẶC TRƯNG",
    "Empirical Behavioral Signatures in Financial Fraud": "Dấu vết Hành vi Thực nghiệm trong Gian lận Tài chính",
    "Mathematical Formulation of 14 Engineered Features": "Công thức Toán học của 14 Engineered Domain Features",
    "Handling Class Imbalance: SMOTE vs. ADASYN Formulation": "Kỹ thuật Xử lý Mất cân bằng: SMOTE vs. ADASYN Formulation",

    # Slide 7: EDA Signatures (Academic & Professional terms)
    "Exploratory Data Analysis: Key Behavioral Signatures": "Phân tích Dữ liệu Khám phá: Dấu vết Hành vi Cốt lõi",
    "Finding 1: Category Confinement": "Phát hiện 1: Khu biệt Loại Giao dịch",
    "100% FRAUD CONCENTRATION": "100% GIAN LẬN KHU BIỆT",
    "• 100% of all fraudulent instances occur strictly in TRANSFER and CASH_OUT.": "• 100% giao dịch gian lận chỉ xuất hiện ở TRANSFER và CASH_OUT.",
    "• All PAYMENT, CASH_IN, and DEBIT instances have 0% fraud.": "• Các loại PAYMENT, CASH_IN và DEBIT hoàn toàn không có gian lận (0%).",
    "• Pipeline Action: Filter dataset to only TRANSFER & CASH_OUT to eliminate 70% irrelevant noise.": "• Hành động Pipeline: Lọc dữ liệu chỉ giữ lại TRANSFER & CASH_OUT để triệt tiêu 70% nhiễu.",
    "Finding 2: Total Account Drain": "Phát hiện 2: Vét Sạch Số Dư Tài Khoản",
    "97.56% OF FRAUD CASES": "97.56% TỔNG SỐ CA GIAN LẬN",
    "• In 97.56% of fraudulent transfers, the victim account is completely drained (newbalanceOrig == 0).": "• Ở 97.56% giao dịch gian lận, tài khoản nạn nhân bị rút cạn sạch (newbalanceOrig == 0).",
    "• Perpetrators maximize cash-out efficiency before identity flags trigger.": "• Kẻ gian tối đa hóa hiệu suất rút tiền trước khi bị hệ thống phát hiện định danh.",
    "• Key Signal: Account drain ratio serves as primary discriminator.": "• Tín hiệu cốt lõi: Tỷ lệ rút cạn tài khoản đóng vai trò phân loại chính.",
    "Finding 3: Destination Ledger Mismatch": "Phát hiện 3: Sai Lệch Sổ Cái Tài Khoản Đích",
    "ZERO DELTA ANOMALY": "BẤT THƯỜNG BIẾN ĐỘNG SỐ DƯ",
    "• A massive proportion of fraudulent transactions show no increase in destination account balances.": "• Tỷ lệ lớn giao dịch gian lận không làm tăng số dư tài khoản đích.",
    "• Suggests mule accounts or instant multi-hop laundering routing.": "• Phản ánh tài khoản rác (mule account) hoặc luân chuyển rửa tiền đa tầng tức thì.",
    "• Key Signal: Destination discrepancy error highlights illegal extraction.": "• Tín hiệu cốt lõi: Sai lệch số dư đích vạch trần hành vi rút tiền bất hợp pháp.",

    # Slide 8: Feature Engineering
    "Feature Engineering: 14 Synthesized Domain Predictors": "Feature Engineering: 14 Đặc trưng Miền Bổ sung",
    "1. Origin Balance Error (Delta Orig)": "1. Sai lệch Số dư Nguồn (Delta Orig)",
    "Measures discrepancy between expected and reported sender balance post-transaction.": "Đo lường sai lệch giữa số dư kỳ vọng và số dư thực tế của tài khoản nguồn sau giao dịch.",
    "2. Destination Balance Error (Delta Dest)": "2. Sai lệch Số dư Đích (Delta Dest)",
    "Tracks uncredited or routing discrepancies at receiving destination accounts.": "Theo dõi các sai lệch luân chuyển tiền hoặc không ghi có tại tài khoản đích.",
    "3. Full Account Drain Indicator": "3. Cờ Vét sạch Tài khoản (Drain Flag)",
    "Binary indicator capturing single-step complete account exhaustion.": "Biến nhị phân bắt trọn hành vi vét sạch toàn bộ tài khoản trong 1 bước duy nhất.",
    "Feature Space": "Feature Space",
    "Expanded numeric domain representation": "Không gian 14 đặc trưng số học sau Feature Engineering",
    "Origin Error": "Origin Error",
    "Captures ledger imbalance (49.9% gain)": "Bắt trọn sai lệch sổ cái nguồn (49.9% gain)",
    "Dest Error": "Dest Error",
    "Tracks routing discrepancies": "Ghi nhận bất thường số dư tài khoản đích",
    "Amount Ratio": "Amount Ratio",
    "Hour of Day": "Hour of Day",
    "step % 24 (diurnal temporal cycle)": "step % 24 (chu kỳ thời gian trong ngày)",
    "Overnight Flag": "Overnight Flag",
    "1 if hour in [0..5] (overnight attacks)": "1 nếu hour in [0..5] (khung giờ đêm)",
    "Feature Importance Deductions": "Đúc kết Feature Importance",
    "Engineered ledger errors contribute over 97% of tree split gains.": "Các biến ledger error đóng góp hơn 97% feature split gains của cây quyết định.",
    "Temporal cyclicity (hour) isolates automated scripted nighttime attacks.": "Chu kỳ thời gian (hour) cô lập các cuộc tấn công theo kịch bản tự động vào ban đêm.",
    "All features are scaled strictly on training split to prevent leakage.": "Toàn bộ features được scale nghiêm ngặt CHỈ trên tập Train để chống Data Leakage.",

    # Slide 9: SMOTE vs ADASYN
    "Class Imbalance Mitigation: SMOTE vs. ADASYN": "Xử lý Mất cân bằng Lớp: SMOTE vs. ADASYN",
    "The Accuracy Paradox in Imbalanced AI": "Accuracy Paradox trong Phân lớp Mất cân bằng",
    "• A naive \"All Normal\" classifier achieves 99.87% Accuracy yet misses 100% of fraud attacks.": "• Một baseline ngây thơ dự đoán 100% \"Hợp lệ\" đạt Accuracy 99.87% nhưng bỏ sót 100% gian lận.",
    "• Evaluation Mandate: Model selection must be strictly governed by Precision, Recall, F1-Score, and PR-AUC.": "• Nguyên tắc Đánh giá: Đánh giá mô hình phải dẫn dắt bởi Precision, Recall, F1-Score và PR-AUC.",
    "SMOTE Interpolation Formulation": "Công thức Nội suy Mẫu SMOTE",
    "Synthesizes artificial minority instances along vector line segments connecting k-nearest minority neighbors in latent space.": "Nội suy mẫu nhân tạo thiểu số dọc theo đoạn thẳng nối các láng giềng k-NN trong latent feature space.",
    "ADASYN Density-Weighted Resampling": "Tái lấy mẫu Phân phối Trọng số ADASYN",
    "Generates synthetic minority instances proportionally to Gamma_i near difficult decision boundaries.": "Sinh mẫu nhân tạo thiểu số theo phân phối trọng số mật độ (Gamma_i) ở vùng decision boundary.",
    "Empirical Takeaway for Fraud Detection": "Đúc kết Thực nghiệm",
    "SMOTE produces cleaner synthetic boundaries with lower False Positives.": "SMOTE tạo decision boundary rõ nét hơn với tỷ lệ False Positive thấp hơn.",
    "ADASYN over-synthesizes in high-noise boundary overlap regions, slightly degrading Precision.": "ADASYN over-synthesize ở vùng chồng lấn nhiễu, làm giảm nhẹ chỉ số Precision.",

    # Slide 10: Divider 3
    "PART 03": "PHẦN 03",
    "PROPOSED METHODOLOGIES & PIPELINE": "PHƯƠNG PHÁP ĐỀ XUẤT & KIẾN TRÚC PIPELINE",
    "Leak-Free End-to-End System Pipeline Architecture": "Kiến trúc Pipeline Toàn diện Chuẩn Leak-Free",
    "Supervised Learning: Random Forest (Bagging & MDI Importance)": "Supervised Learning: Random Forest (Bagging & MDI Importance)",
    "Gradient Boosting: XGBoost (Regularized GBDT & Taylor Expansion)": "Gradient Boosting: XGBoost (Regularized GBDT & Taylor Expansion)",
    "Unsupervised Learning: Deep Autoencoder (Manifold Reconstruction)": "Unsupervised Learning: Deep Autoencoder (Manifold Reconstruction)",

    # Slide 11: End-to-End Pipeline (Standard AI Engineering Terminology)
    "End-to-End Leak-Free Machine Learning Pipeline": "Kiến trúc Pipeline Machine Learning Chuẩn Leak-Free",
    "Filtering": "Filtering",
    "Retain TRANSFER & CASH_OUT": "Lọc TRANSFER & CASH_OUT",
    "Feature Eng.": "Feature Eng.",
    "Compute 14 mathematical features": "Tính 14 engineered features",
    "Stratified Split": "Stratified Split",
    "80/20 Train/Test separation": "Chia 80/20 Train/Test phân tầng",
    "Resampling": "Resampling",
    "SMOTE / ADASYN on Train only": "SMOTE / ADASYN trên tập Train",
    "Training": "Model Training",
    "Fit RF, XGBoost & Autoencoder": "Huấn luyện RF, XGBoost & Autoencoder",
    "Evaluation": "Evaluation",
    "Test set inference (N=40,000)": "Đánh giá trên Test set (N=40,000)",
    "Strict Protocol Against Data Leakage": "Quy chuẩn Khắt khe Chống Data Leakage",
    "Oversampling (SMOTE/ADASYN) is strictly executed AFTER data partitioning on training fold only.": "Resampling (SMOTE/ADASYN) tuyệt đối CHỈ thực hiện SAU KHI phân chia Train/Test trên tập Train.",
    "StandardScaler normalization is fitted on the training split only and applied blindly to the test set.": "StandardScaler normalization chỉ fit trên tập Train và transform mù trên tập Test.",
    "Zero test target information is leaked into model feature representations or hyperparameter selection.": "Tuyệt đối không để rò rỉ thông tin tập Test vào feature representation hay hyperparameter tuning.",

    # Slide 12: Random Forest
    "Supervised Architecture 1: Random Forest Ensemble": "Mô hình Giám sát 1: Random Forest Ensemble",
    "Gini Impurity & MDI Split Criterion": "Tiêu chuẩn Phân nhánh Gini Impurity & MDI",
    "Each split optimizes the reduction in Gini impurity across randomly selected feature subspaces.": "Mỗi phân nhánh tối ưu hóa mức giảm Gini Impurity trên các feature subspace được chọn ngẫu nhiên.",
    "Ensemble Size": "Ensemble Size",
    "Number of bagged trees": "Tổng số cây bagged trong rừng (n_estimators)",
    "Depth Limit": "Depth Limit",
    "Prevents tree overfitting": "Giới hạn độ sâu (chống Overfitting)",
    "Split Metric": "Split Metric",
    "Gini Impurity": "Gini Impurity",
    "Information impurity criterion": "Tiêu chuẩn đo impurity thông tin",
    "Feature Subset": "Feature Subset",
    "Random subspace dimension": "Kích thước feature subspace ngẫu nhiên",
    "Architectural Strengths": "Thế mạnh Kiến trúc",
    "Peak Precision: Generates only 1 False Positive across 38,357 test transactions.": "Peak Precision: Chỉ sinh duy nhất 1 False Positive trên 38,357 test samples.",
    "High Interpretability: Transparent decision paths and feature impurity scoring.": "Tính tường minh: Decision path minh bạch và feature importance rõ ràng.",
    "Limitation: High computational training time (~1187s).": "Hạn chế: Thời gian training tương đối lâu (~1187s).",

    # Slide 13: XGBoost
    "Supervised Architecture 2: XGBoost Classifier": "Mô hình Giám sát 2: XGBoost Classifier",
    "Regularized Objective Function (2nd-Order Taylor)": "Hàm Mục tiêu Regularized (Khai triển Taylor Bậc 2)",
    "where g_i and h_i are 1st and 2nd order gradients of the loss function with respect to previous predictions.": "trong đó g_i và h_i là gradients bậc 1 và bậc 2 của loss function theo dự đoán trước.",
    "Objective": "Objective",
    "Regularized loss formulation": "Hàm mục tiêu có regularization",
    "Shrinkage": "Learning Rate",
    "Step size scaling factor": "Hệ số co ngót bước học (eta = 0.2)",
    "Max Depth": "Max Depth",
    "Max tree depth per boosting round": "Độ sâu cây tối đa mỗi boosting round",
    "Subsample": "Subsample",
    "Stochastic row sampling fraction": "Tỷ lệ lấy mẫu hàng ngẫu nhiên (rho = 0.85)",
    "Production Advantages": "Ưu thế trong Môi trường Production",
    "Near-identical F1-score (99.63%) compared to Random Forest (99.73%).": "F1-score đạt 99.63%, gần như tương đương tuyệt đối với Random Forest (99.73%).",
    "Extremely low latency: < 0.5ms single-sample inference time.": "Inference latency đơn mẫu cực thấp: < 0.5ms.",
    "Ideal for live financial transaction gateway screening.": "Lý tưởng để triển khai kiểm duyệt giao dịch real-time tại cổng thanh toán.",

    # Slide 14: Deep Autoencoder
    "Unsupervised Architecture 3: Deep Autoencoder": "Mô hình Không giám sát 3: Deep Autoencoder",
    "Reconstruction Loss & Decision Cutoff": "Hàm Mất mát Tái tạo & Ngưỡng Quyết định",
    "Samples with MSE exceeding the validation 95th percentile threshold tau are classified as anomalous.": "Các mẫu có MSE vượt quá ngưỡng validation 95th percentile (tau) được phân loại là Gian lận (Anomalous).",
    "Bottleneck": "Bottleneck",
    "Latent embedding representation": "Không gian biểu diễn ẩn nén (z in R^4)",
    "Loss Function": "Loss Function",
    "Mean squared reconstruction error": "Mean Squared Reconstruction Error (MSE)",
    "Activation": "Activation",
    "Non-linear hidden layer mappings": "Hàm kích hoạt phi tuyến tính (ReLU)",
    "Threshold": "Decision Threshold",
    "95th percentile validation cutoff": "Ngưỡng quyết định 95th percentile (tau = 0.0455)",
    "Zero-Day Detection Role": "Vai trò Phát hiện Tấn công Zero-Day",
    "Achieves 75.23% Recall without observing any fraud labels during training.": "Đạt 75.23% Recall dù hoàn toàn không quan sát fraud labels khi training.",
    "Acts as a complementary defense layer for novel, unseen attack signatures.": "Đóng vai trò lớp phòng thủ bổ trợ đắc lực cho các attack signatures mới chưa từng xuất hiện.",

    # Slide 15: Divider 4
    "PART 04": "PHẦN 04",
    "EXPERIMENTS, RESULTS & COMPARATIVE EVALUATION": "KẾT QUẢ THỰC NGHIỆM & ĐÁNH GIÁ SO SÁNH",
    "Comprehensive Performance Benchmark (Precision, Recall, F1, AUC)": "Benchmark Hiệu năng Toàn diện (Precision, Recall, F1, ROC-AUC)",
    "Confusion Matrix & False Alarm vs. Missed Fraud Trade-offs": "Confusion Matrix & Đánh đổi False Alarm vs. Missed Fraud",
    "Feature Importance Attribution & Gain Contributions": "Feature Importance Attribution & Split Gain Contributions",
    "Autoencoder Anomaly Thresholding & Reconstruction Dynamics": "Autoencoder Anomaly Thresholding & Reconstruction Dynamics",

    # Slide 16: Benchmark Results
    "Experimental Results: Benchmark Comparison (N = 40,000)": "Kết quả Thực nghiệm: Đánh giá Benchmark (N = 40,000)",
    "Model Architecture": "Kiến trúc Mô hình",
    "Resampling": "Kỹ thuật Resampling",
    "Train Time": "Thời gian Train",
    "Key Empirical Deductions": "Đúc kết Thực nghiệm Cốt lõi",
    "RF + SMOTE achieves peak F1-Score (99.73%) with only 1 False Positive across 38,357 legitimate test samples.": "RF + SMOTE đạt đỉnh F1-Score (99.73%) chỉ với duy nhất 1 False Positive trên 38,357 legitimate test samples.",
    "XGBoost achieves near-identical classification performance (F1 99.63%) with 28.5x computational speedup.": "XGBoost đạt classification performance gần như tương đương (F1 99.63%) nhưng training time nhanh hơn 28.5 lần.",
    "Autoencoder detects 75.23% of fraud cases in an entirely unsupervised setting without seeing fraud labels.": "Autoencoder phát hiện được 75.23% ca gian lận trong bối cảnh hoàn toàn unsupervised, không cần fraud labels.",

    # Slide 17: Confusion Matrix
    "Confusion Matrix & Error Distribution Analysis": "Confusion Matrix & Phân tích Phân phối Sai số",
    "False Negative & False Positive Trade-off Analysis": "Phân tích Đánh đổi giữa False Negative và False Positive",
    "Both Random Forest and XGBoost miss only 8 fraud instances out of 1,643 true fraud cases (Recall = 99.51%).": "Cả Random Forest và XGBoost chỉ bỏ sót 8 ca gian lận trên tổng số 1,643 true fraud cases (Recall = 99.51%).",
    "RF-SMOTE generates only 1 False Alarm (FP=1), whereas Autoencoder generates 1,998 FP due to unsupervised 95% cutoff.": "RF-SMOTE chỉ sinh đúng 1 False Alarm (FP=1), trong khi Autoencoder sinh 1,998 FP do đặc thù cắt ngưỡng 95% cutoff.",

    # Slide 18: Feature Importance
    "Feature Importance: XGBoost Decision Split Gains": "Feature Importance: Đóng góp Phân nhánh của XGBoost",
    "Key Feature Insights": "Đúc kết Đặc trưng Quan trọng",
    "Top 2 features contribute > 97% of total tree split decisions.": "Top 2 features đóng góp > 97% vào tổng quyết định phân nhánh cây.",
    "Raw balance amounts without discrepancy deltas have low predictive power.": "Raw transaction amounts nếu không có sai số delta mang lại rất ít predictive power.",

    # Slide 19: Comparative Evaluation
    "Comparative Evaluation: Precision, Recall & F1-Score": "Đánh giá So sánh: Precision, Recall & F1-Score",
    "Benchmarking Synthesis": "Tổng hợp Đối chuẩn",
    "SMOTE achieves superior boundary separation over ADASYN.": "SMOTE tạo decision boundary phân tách vượt trội hơn ADASYN.",
    "Supervised methods strongly dominate unsupervised reconstruction in known fraud types.": "Supervised learning áp đảo hoàn toàn unsupervised reconstruction trên các dạng gian lận đã biết.",

    # Slide 20: Autoencoder Thresholding
    "Autoencoder Anomaly Thresholding & Decision Boundary": "Autoencoder: Ngưỡng Bất thường & Decision Boundary",
    "Threshold Calibration": "Threshold Calibration",
    "Tau = 0.0455 (95th percentile) optimizes the F1-Score trade-off curve.": "tau = 0.0455 (95th percentile) tối ưu hóa trade-off curve của F1-Score.",
    "Unsupervised model successfully flags 1,236 true fraud events.": "Unsupervised model gắn cờ thành công 1,236 sự kiện gian lận thực tế.",

    # Slide 21: Divider 5
    "PART 05": "PHẦN 05",
    "INTERACTIVE SYSTEM & FUTURE ROADMAP": "HỆ THỐNG DEMO & ĐỊNH HƯỚNG TƯƠNG LAI",
    "Streamlit Real-Time Inference Dashboard Architecture": "Kiến trúc Dashboard Streamlit Real-Time Inference",
    "Summary of Key Academic & Engineering Contributions": "Tổng kết Đóng góp Học thuật & Kỹ thuật Cốt lõi",
    "Research Limitations & Graph Neural Network (GNN) Roadmap": "Hạn chế Nghiên cứu & Graph Neural Network (GNN) Roadmap",

    # Slide 22: Demo Dashboard
    "Interactive Demonstration: Streamlit Real-Time Dashboard": "Demo Trực quan: Dashboard Thời gian Thực trên Streamlit",
    "Real-Time Inference Architecture": "Kiến trúc Real-Time Inference",
    "Lightweight Streamlit UI with dynamic risk probability gauges and visual status cards.": "Giao diện Streamlit tinh gọn với dynamic risk probability gauges và visual status cards.",
    "Instant feature extraction engine transforming raw user inputs into the 14-dimension engineered vector.": "Feature extraction engine tức thì chuyển đổi user input thành 14-dimension engineered vector.",
    "Pre-loaded serialized XGBoost and Random Forest pipelines via Joblib.": "Pre-loaded serialized XGBoost và Random Forest pipelines qua Joblib.",
    "Sub-millisecond single-transaction inference latency (< 1ms).": "Single-transaction inference latency đạt mức sub-millisecond (< 1ms).",
    "Demonstrated Simulation Scenarios": "Các Kịch bản Mô phỏng Thực nghiệm",
    "Scenario 1 (Normal Transfer): Standard transaction with valid balances -> Model Output: SAFE (Risk Probability < 0.1%).": "Scenario 1 (Normal Transfer): Giao dịch tiêu chuẩn với biến động số dư hợp lệ -> Model Output: SAFE (Risk Probability < 0.1%).",
    "Scenario 2 (Account Drain): High-amount transfer leaving zero origin balance -> Model Output: HIGH RISK FRAUD (Risk Probability > 99.8%).": "Scenario 2 (Account Drain): Chuyển tiền lớn khiến số dư nguồn về 0 -> Model Output: HIGH RISK FRAUD (Risk Probability > 99.8%).",
    "Batch CSV Scoring: Allows bulk processing and compliance report exports.": "Batch CSV Scoring: Cho phép chấm điểm hàng loạt và xuất compliance audit report.",

    # Slide 23: Contributions & Roadmap
    "Summary of Contributions & Future Research": "Tổng kết Đóng góp & Định hướng Nghiên cứu",
    "Key Project Contributions": "Đóng góp Cốt lõi của Dự án",
    "Leak-Free Protocol: 80/20 stratified partition preventing synthetic data contamination.": "Leak-Free Protocol: Stratified 80/20 split ngăn chặn hoàn toàn data contamination.",
    "Domain Engineering: 14 synthesized features capturing > 97% of tree split gains.": "Domain Feature Engineering: 14 synthesized features chiếm > 97% tree split gains.",
    "Superior Benchmark: F1-Score = 99.73% and Recall = 99.51% (missing only 8 out of 1,643 frauds).": "Superior Benchmark: F1-Score = 99.73% và Recall = 99.51% (chỉ bỏ sót 8 trên 1,643 frauds).",
    "Operational Deployment: Ready-to-use Streamlit dashboard for real-time risk screening.": "Production Deployment: Dashboard Streamlit hoàn chỉnh phục vụ real-time risk screening.",
    "Future Research Roadmap": "Lộ trình Nghiên cứu Tương lai",
    "Graph Neural Networks (GNN): Deploy GCN / GraphSAGE to uncover structured money-laundering subgraphs.": "Graph Neural Networks (GNN): Ứng dụng GCN / GraphSAGE phát hiện structured money-laundering subgraphs.",
    "Streaming Ingestion: Integrate Apache Kafka / Flink for distributed sub-second streaming transactions.": "Streaming Ingestion: Tích hợp Apache Kafka / Flink phục vụ distributed sub-second streaming transactions.",
    "Explainable AI (XAI): Integrate SHAP / TreeExplainer for regulatory compliant transaction audit logs.": "Explainable AI (XAI): Tích hợp SHAP / TreeExplainer phục vụ regulatory compliant transaction audit logs.",

    # Slide 24: Conclusion & References
    "THANK YOU FOR YOUR ATTENTION!": "CHÂN THÀNH CẢM ƠN THẦY VÀ CÁC BẠN ĐÃ LẮNG NGHE!",
    "CS106: ARTIFICIAL INTELLIGENCE  •  FINAL PROJECT DEFENSE  •  TEAM 09": "CS106: TRÍ TUỆ NHÂN TẠO  •  BÁO CÁO BẢO VỆ ĐỒ ÁN  •  NHÓM 09",
    "KEY ACADEMIC REFERENCES & PROJECT REPOSITORY": "TÀI LIỆU THAM KHẢO HỌC THUẬT & REPOSITORY DỰ ÁN",
    "We cordially welcome all questions, feedback, and discussions from the Committee.": "Nhóm 09 rất mong nhận được những câu hỏi và góp ý quý báu từ Hội đồng!"
}

COMPLEX_REPLACEMENTS = {
    """Insights from XGBoost Feature Gain:

• errorBalanceOrig accounts for ~49.9% of model decision splits.

• newbalanceOrig provides ~47.2% additional predictive power.

• Combined Impact: Engineered ledger discrepancies capture over 97% of overall fraud dynamics, proving the critical efficacy of domain feature engineering.""":
    """Insights từ XGBoost Feature Gain:

• errorBalanceOrig chiếm ~49.9% tổng trọng số phân nhánh của model.

• newbalanceOrig bổ sung thêm ~47.2% predictive power cho cây quyết định.

• Tác động kết hợp: Các engineered ledger discrepancies nắm giữ hơn 97% động lực phân loại gian lận, chứng minh tính hiệu quả vượt bậc của domain feature engineering.""",

    """Resampling Performance Analysis:

• SMOTE consistently outperforms ADASYN across all decision tree architectures.

• ADASYN synthesizes excess noise instances in boundary overlap zones, slightly degrading Precision.

• Recommendation: Deploy XGBoost + SMOTE for optimal inference throughput and fraud detection precision in live production environments.""":
    """Phân tích Hiệu năng Resampling:

• SMOTE vượt trội hơn ADASYN một cách nhất quán trên mọi tree architectures.

• ADASYN sinh nhiều synthetic noise ở vùng boundary overlap, làm tăng nhẹ False Positives.

• Khuyến nghị: Triển khai XGBoost + SMOTE để tối ưu hóa inference throughput và fraud detection precision trong môi trường production.""",

    """Threshold Sweep Dynamics:

• 95th Percentile (tau = 0.0455):
Balances Recall (75.2%) with Precision (38.2%).

• 99.9th Percentile (tau = 0.7460):
Precision jumps to 91.5% but Recall drops to 25.4%.

• Operational Role: Excellent as a secondary zero-day defense layer for unlabelled novel fraud patterns.""":
    """Động lực Quét Ngưỡng (Threshold Sweep):

• 95th Percentile (tau = 0.0455):
Cân bằng giữa Recall (75.2%) và Precision (38.2%).

• 99.9th Percentile (tau = 0.7460):
Precision tăng vọt lên 91.5% nhưng Recall giảm xuống 25.4%.

• Vai trò Vận hành: Đóng vai trò secondary zero-day defense layer đắc lực trước các hình thức gian lận mới chưa có label."""
}

def translate_text(text):
    text_clean = text.strip()
    if not text_clean:
        return text
    
    if text_clean in COMPLEX_REPLACEMENTS:
        return COMPLEX_REPLACEMENTS[text_clean]
    
    if text_clean in MAPPING:
        return MAPPING[text_clean]
    
    # Try line by line
    lines = text.split('\n')
    translated_lines = []
    has_match = False
    for line in lines:
        line_s = line.strip()
        if line_s in MAPPING:
            translated_lines.append(MAPPING[line_s])
            has_match = True
        else:
            translated_lines.append(line)
    
    if has_match:
        return '\n'.join(translated_lines)
    
    return text

def safe_replace_tf(tf):
    full_text = '\n'.join([p.text for p in tf.paragraphs])
    if full_text.strip() in COMPLEX_REPLACEMENTS:
        new_full = COMPLEX_REPLACEMENTS[full_text.strip()]
        new_lines = new_full.split('\n')
        if len(new_lines) == len(tf.paragraphs):
            for p, nl in zip(tf.paragraphs, new_lines):
                if p.runs:
                    p.runs[0].text = nl
                    for r in p.runs[1:]:
                        r.text = ''
                else:
                    p.text = nl
                p.font.name = 'Segoe UI'
            return
        else:
            if tf.paragraphs:
                p0 = tf.paragraphs[0]
                if p0.runs:
                    p0.runs[0].text = new_full
                    for r in p0.runs[1:]:
                        r.text = ''
                else:
                    p0.text = new_full
                p0.font.name = 'Segoe UI'
                for p in tf.paragraphs[1:]:
                    if p.runs:
                        for r in p.runs:
                            r.text = ''
                    else:
                        p.text = ''
            return

    for p in tf.paragraphs:
        p_text = p.text.strip()
        if not p_text:
            continue
        new_text = translate_text(p_text)
        if new_text != p_text:
            if p.runs:
                p.runs[0].text = new_text
                for r in p.runs[1:]:
                    r.text = ''
            else:
                p.text = new_text
        p.font.name = 'Segoe UI'

for s_idx, slide in enumerate(prs.slides):
    for shape in slide.shapes:
        if shape.has_text_frame:
            safe_replace_tf(shape.text_frame)
        elif shape.has_table:
            for row in shape.table.rows:
                for cell in row.cells:
                    safe_replace_tf(cell.text_frame)

prs.save(output_pptx)
print(f'Successfully updated standard Vietnamese PPTX with hybrid academic terminology: {output_pptx}')
