import pptx
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
input_pptx = os.path.join(BASE_DIR, '[Nhom9]_Slide_FraudDetection_Academic.pptx')
output_pptx = os.path.join(BASE_DIR, '[Nhom9]_Slide_FraudDetection_Academic_VN.pptx')

prs = pptx.Presentation(input_pptx)

# Standard Academic Hybrid Mapping: Professional Vietnamese explanations + Standard English AI/ML terms
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
    "VIETNAM NATIONAL UNIVERSITY HO CHI MINH CITY": "ĐẠI HỌC QUỐC GIA THÀNH PHỐ HỒ CHÍ MINH",
    "UNIVERSITY OF INFORMATION TECHNOLOGY  •  FACULTY OF COMPUTER SCIENCE": "TRƯỜNG ĐẠI HỌC CÔNG NGHỆ THÔNG TIN  •  KHOA KHOA HỌC MÁY TÍNH",
    "FINANCIAL FRAUD DETECTION": "PHÁT HIỆN GIAN LẬN TÀI CHÍNH",
    "Applied Machine Learning & Deep Learning on PaySim Synthetic Dataset": "Ứng dụng Machine Learning & Deep Learning trên Tập dữ liệu PaySim",
    "Course: CS106 — Artificial Intelligence  |  Advisor: Assoc. Prof. Nguyen Dinh Hien": "Môn học: CS106 — Trí tuệ Nhân tạo  |  GVHD: PGS.TS. Nguyễn Đình Hiển",
    "TEAM 09": "NHÓM 09",
    "Tran Hoang Hon (26410046)  •  Dang Chi Thanh (25730067)  •  Nguyen Duy Khang (26410055)": "Trần Hoàng Hôn (26410046)  •  Đặng Chí Thanh (25730067)  •  Nguyễn Duy Khang (26410055)",
    "Hoang Cao Son (25730061)  •  Vu Van Duy (26410031)  •  Bui Thi My Cam (25730013)  •  Pham Thanh Trung (26410141)": "Hoàng Cao Sơn (25730061)  •  Vũ Văn Duy (26410031)  •  Bùi Thị Mỹ Cẩm (25730013)  •  Phạm Thanh Trung (26410141)",
    "Ho Chi Minh City, September 2026": "TP. Hồ Chí Minh, Tháng 09/2026",

    # Slide 2: Agenda
    "AGENDA & ROADMAP": "NỘI DUNG BÁO CÁO & LỘ TRÌNH",
    "Introduction & Problem Formulation": "Giới thiệu & Problem Formulation",
    "Financial context, extreme class imbalance, and formal task formulation.": "Bối cảnh tài chính, bài toán Extreme Class Imbalance và phát biểu bài toán.",
    "Exploratory Data Analysis & Feature Engineering": "Exploratory Data Analysis & Feature Engineering",
    "Category confinement, balance drain signatures, and 14 synthesized features.": "Khu biệt loại giao dịch, dấu vết rút cạn số dư và 14 engineered features.",
    "Proposed Methodologies & Machine Learning Pipeline": "Phương pháp Đề xuất & ML Pipeline",
    "Resampling (SMOTE/ADASYN), Random Forest, XGBoost, and Deep Autoencoder.": "Resampling (SMOTE/ADASYN), Random Forest, XGBoost và Deep Autoencoder.",
    "Experiments, Results & Comparative Evaluation": "Kết quả Thực nghiệm & Đánh giá So sánh",
    "Benchmark metrics, confusion matrices, feature gains, and error trade-offs.": "Benchmark hiệu năng, Confusion Matrix, Feature Gain và phân tích sai số.",
    "Interactive System & Future Research Trajectories": "Hệ thống Thực thi & Hướng Phát triển",
    "Streamlit real-time dashboard, business viability, limitations, and GNN roadmap.": "Dashboard Streamlit real-time, đóng góp cốt lõi, hạn chế và lộ trình GNN.",

    # Slide 3: Divider 1
    "PART 01": "PHẦN 01",
    "INTRODUCTION & PROBLEM FORMULATION": "GIỚI THIỆU & PROBLEM FORMULATION",
    "Industrial Background & Mobile Money Expansion": "Bối cảnh Công nghiệp & Sự bùng nổ Mobile Money",
    "The Asymmetric Cost & Extreme Imbalance Paradox": "Thách thức Extreme Class Imbalance (~0.13%) & Asymmetric Cost",
    "Formal AI Problem Statement & Research Objectives": "Phát biểu Bài toán Hình thức & Mục tiêu Nghiên cứu",

    # Slide 4: Problem Motivation
    "Problem Motivation & Technical Challenges": "Động lực Nghiên cứu & Thách thức Kỹ thuật",
    "1. Industrial Context & Scale": "1. Bối cảnh Thực tiễn & Quy mô",
    "• Mobile money transactions have surged globally, introducing complex synthetic fraud vectors.": "• Giao dịch tiền di động (Mobile Money) tăng trưởng bùng nổ, kéo theo các thủ đoạn gian lận tinh vi.",
    "• Real-time defense mechanisms require sub-100ms inference latency before funds leave the system.": "• Hệ thống phòng thủ đòi hỏi độ trễ suy luận thời gian thực (Inference Latency < 100ms) trước khi dòng tiền bị rút khỏi hệ thống.",
    "2. Extreme Class Imbalance (~0.13%)": "2. Extreme Class Imbalance (~0.13%)",
    "• Fraud accounts for only ~1 out of every 800 transactions in the PaySim universe.": "• Giao dịch gian lận chỉ chiếm ~1 trên 800 giao dịch trong tập dữ liệu PaySim.",
    "• Cost Asymmetry: False Negatives (missed fraud) lead to direct capital loss, while False Positives cause customer friction.": "• Cost Asymmetry: Bỏ sót gian lận (False Negative) gây tổn thất vốn trực tiếp, trong khi Báo động nhầm (False Positive) gây phiền hà khách hàng.",
    "3. Non-Stationary Fraud Patterns": "3. Non-Stationary Fraud Patterns",
    "• Adversaries constantly morph account routing tactics to evade static rule-based threshold filters.": "• Kẻ gian liên tục biến đổi phương thức luân chuyển tiền để lẩn tránh các bộ lọc luật tĩnh (rule-based).",
    "Class Target": "Class Target",
    "1 = Fraudulent, 0 = Legitimate": "1 = Fraudulent (Gian lận), 0 = Legitimate",
    "Imbalance": "Imbalance Ratio",
    "1,643 frauds per 1.3M events": "1,643 ca gian lận trên 1.3M giao dịch",
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
    "Dataset Scaling": "Dataset Scaling",
    "Stratified downsampling preserving 100% fraud": "Stratified downsampling bảo toàn 100% gian lận",
    "Positive Instances (isFraud = 1)": "Positive Instances (isFraud = 1)",
    "Ground-truth fraud transactions": "Giao dịch gian lận nhãn ground-truth",
    "11 -> 14 Features": "11 -> 14 Features",
    "Synthesized Feature Space": "Feature Space Mở rộng",
    "Expanded with balance delta equations": "Bổ sung các phương trình sai lệch số dư",
    "Feature Name": "Feature Name",
    "Data Type": "Data Type",
    "Domain Description & Operational Role": "Domain Description & Ý nghĩa Nghiệp vụ",
    "Integer": "Integer",
    "Time step unit in hours (1..744, representing 30 simulation days)": "Time step theo giờ (1..744, tương ứng 30 ngày mô phỏng)",
    "Categorical": "Categorical",
    "Transaction category: CASH_OUT, TRANSFER, PAYMENT, CASH_IN, DEBIT": "Loại giao dịch: CASH_OUT, TRANSFER, PAYMENT, CASH_IN, DEBIT",
    "Continuous": "Continuous",
    "Transaction amount in local currency units": "Số tiền thực hiện giao dịch (đơn vị tiền tệ cục bộ)",
    "Initial balance and post-transaction balance of the sender account": "Số dư trước và ngay sau giao dịch của tài khoản nguồn (sender)",
    "Initial balance and post-transaction balance of the recipient account": "Số dư trước và ngay sau giao dịch của tài khoản đích (recipient)",

    # Slide 6: Divider 2
    "PART 02": "PHẦN 02",
    "EXPLORATORY DATA ANALYSIS & FEATURE ENGINEERING": "EXPLORATORY DATA ANALYSIS & FEATURE ENGINEERING",
    "Empirical Behavioral Signatures in Financial Fraud": "Phân tích Dấu vết Hành vi Thực nghiệm (Behavioral Signatures)",
    "Mathematical Formulation of 14 Engineered Features": "Công thức Toán học của 14 Engineered Domain Features",
    "Handling Class Imbalance: SMOTE vs. ADASYN Formulation": "Xử lý Mất cân bằng Lớp: SMOTE vs. ADASYN Formulation",

    # Slide 7: EDA Signatures
    "Exploratory Data Analysis: Key Behavioral Signatures": "Exploratory Data Analysis: Dấu vết Hành vi Cốt lõi",
    "Finding 1: Category Confinement": "Finding 1: Category Confinement",
    "100% FRAUD CONCENTRATION": "100% FRAUD CONCENTRATION",
    "• 100% of all fraudulent instances occur strictly in TRANSFER and CASH_OUT.": "• 100% giao dịch gian lận chỉ xuất hiện ở TRANSFER và CASH_OUT.",
    "• All PAYMENT, CASH_IN, and DEBIT instances have 0% fraud.": "• Các loại PAYMENT, CASH_IN và DEBIT hoàn toàn không có gian lận (0%).",
    "• Pipeline Action: Filter dataset to only TRANSFER & CASH_OUT to eliminate 70% irrelevant noise.": "• Pipeline Action: Lọc dữ liệu chỉ giữ lại TRANSFER & CASH_OUT để triệt tiêu 70% nhiễu.",
    "Finding 2: Total Account Drain": "Finding 2: Total Account Drain",
    "97.56% OF FRAUD CASES": "97.56% OF FRAUD CASES",
    "• In 97.56% of fraudulent transfers, the victim account is completely drained (newbalanceOrig == 0).": "• Ở 97.56% giao dịch gian lận, tài khoản nạn nhân bị rút cạn sạch (newbalanceOrig == 0).",
    "• Perpetrators maximize cash-out efficiency before identity flags trigger.": "• Kẻ gian tối đa hóa hiệu suất rút tiền trước khi bị hệ thống phát hiện định danh.",
    "• Key Signal: Account drain ratio serves as primary discriminator.": "• Key Signal: Tỷ lệ rút cạn tài khoản đóng vai trò phân loại chính.",
    "Finding 3: Destination Ledger Mismatch": "Finding 3: Destination Ledger Mismatch",
    "ZERO DELTA ANOMALY": "ZERO DELTA ANOMALY",
    "• A massive proportion of fraudulent transactions show no increase in destination account balances.": "• Tỷ lệ lớn giao dịch gian lận không làm tăng số dư tài khoản đích.",
    "• Suggests mule accounts or instant multi-hop laundering routing.": "• Phản ánh tài khoản rác (mule account) hoặc luân chuyển rửa tiền đa tầng tức thì.",
    "• Key Signal: Destination discrepancy error highlights illegal extraction.": "• Key Signal: Destination discrepancy error vạch trần hành vi rút tiền bất hợp pháp.",

    # Slide 8: Feature Engineering
    "Feature Engineering: 14 Synthesized Domain Predictors": "Feature Engineering: 14 Synthesized Domain Predictors",
    "1. Origin Balance Error (Delta Orig)": "1. Origin Balance Error (Delta Orig)",
    "Measures discrepancy between expected and reported sender balance post-transaction.": "Đo lường sai lệch giữa số dư kỳ vọng và số dư thực tế của tài khoản nguồn sau giao dịch.",
    "2. Destination Balance Error (Delta Dest)": "2. Destination Balance Error (Delta Dest)",
    "Tracks uncredited or routing discrepancies at receiving destination accounts.": "Theo dõi các sai lệch luân chuyển tiền hoặc không ghi có tại tài khoản đích.",
    "3. Full Account Drain Indicator": "3. Full Account Drain Indicator Flag",
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
    "Feature Importance Deductions": "Feature Importance Insights",
    "Engineered ledger errors contribute over 97% of tree split gains.": "Các biến ledger error đóng góp hơn 97% feature split gains của cây quyết định.",
    "Temporal cyclicity (hour) isolates automated scripted nighttime attacks.": "Chu kỳ thời gian (hour) cô lập các cuộc tấn công theo kịch bản tự động vào ban đêm.",
    "All features are scaled strictly on training split to prevent leakage.": "Toàn bộ features được scale nghiêm ngặt CHỈ trên tập Train để chống Data Leakage.",

    # Slide 9: SMOTE vs ADASYN
    "Class Imbalance Mitigation: SMOTE vs. ADASYN": "Xử lý Mất cân bằng Lớp: SMOTE vs. ADASYN",
    "The Accuracy Paradox in Imbalanced AI": "Accuracy Paradox in Imbalanced Classification",
    "• A naive \"All Normal\" classifier achieves 99.87% Accuracy yet misses 100% of fraud attacks.": "• Một baseline ngây thơ dự đoán 100% \"Hợp lệ\" đạt Accuracy 99.87% nhưng bỏ sót 100% gian lận.",
    "• Evaluation Mandate: Model selection must be strictly governed by Precision, Recall, F1-Score, and PR-AUC.": "• Evaluation Mandate: Lựa chọn model phải được dẫn dắt tuyệt đối bởi Precision, Recall, F1-Score và PR-AUC.",
    "SMOTE Interpolation Formulation": "SMOTE Interpolation Formulation",
    "Synthesizes artificial minority instances along vector line segments connecting k-nearest minority neighbors in latent space.": "Nội suy mẫu nhân tạo thiểu số dọc theo đoạn thẳng nối các láng giềng k-NN trong latent feature space.",
    "ADASYN Density-Weighted Resampling": "ADASYN Density-Weighted Resampling",
    "Generates synthetic minority instances proportionally to Gamma_i near difficult decision boundaries.": "Sinh mẫu nhân tạo thiểu số theo phân phối trọng số mật độ (Gamma_i) ở vùng decision boundary.",
    "Empirical Takeaway for Fraud Detection": "Đúc kết Thực nghiệm (Empirical Insights)",
    "SMOTE produces cleaner synthetic boundaries with lower False Positives.": "SMOTE tạo decision boundary rõ nét hơn với tỷ lệ False Positive thấp hơn.",
    "ADASYN over-synthesizes in high-noise boundary overlap regions, slightly degrading Precision.": "ADASYN over-synthesize ở vùng chồng lấn nhiễu, làm giảm nhẹ chỉ số Precision.",

    # Slide 10: Divider 3
    "PART 03": "PHẦN 03",
    "PROPOSED METHODOLOGIES & PIPELINE": "PHƯƠNG PHÁP ĐỀ XUẤT & PIPELINE",
    "Leak-Free End-to-End System Pipeline Architecture": "Kiến trúc Pipeline Toàn diện Chuẩn Leak-Free",
    "Supervised Learning: Random Forest (Bagging & MDI Importance)": "Supervised Learning: Random Forest (Bagging & MDI Importance)",
    "Gradient Boosting: XGBoost (Regularized GBDT & Taylor Expansion)": "Gradient Boosting: XGBoost (Regularized GBDT & Taylor Expansion)",
    "Unsupervised Learning: Deep Autoencoder (Manifold Reconstruction)": "Unsupervised Learning: Deep Autoencoder (Manifold Reconstruction)",

    # Slide 11: End-to-End Pipeline
    "End-to-End Leak-Free Machine Learning Pipeline": "End-to-End Leak-Free Machine Learning Pipeline",
    "Filtering": "Filtering",
    "Retain TRANSFER & CASH_OUT": "Giữ lại TRANSFER & CASH_OUT",
    "Feature Eng.": "Feature Eng.",
    "Compute 14 mathematical features": "Tính toán 14 mathematical features",
    "Stratified Split": "Stratified Split",
    "80/20 Train/Test separation": "Tách 80/20 Train/Test phân tầng",
    "Resampling": "Resampling",
    "SMOTE / ADASYN on Train only": "SMOTE / ADASYN CHỈ trên Train fold",
    "Training": "Training",
    "Fit RF, XGBoost & Autoencoder": "Fit RF, XGBoost & Autoencoder",
    "Evaluation": "Evaluation",
    "Test set inference (N=40,000)": "Inference trên tập Test độc lập (N=40,000)",
    "Strict Protocol Against Data Leakage": "Quy chuẩn Khắt khe Chống Data Leakage",
    "Oversampling (SMOTE/ADASYN) is strictly executed AFTER data partitioning on training fold only.": "Resampling (SMOTE/ADASYN) tuyệt đối CHỈ thực hiện SAU KHI phân chia Train/Test trên tập Train.",
    "StandardScaler normalization is fitted on the training split only and applied blindly to the test set.": "StandardScaler normalization chỉ fit trên tập Train và transform mù trên tập Test.",
    "Zero test target information is leaked into model feature representations or hyperparameter selection.": "Tuyệt đối không để rò rỉ thông tin tập Test vào feature representation hay hyperparameter tuning.",

    # Slide 12: Random Forest
    "Supervised Architecture 1: Random Forest Ensemble": "Supervised Architecture 1: Random Forest Ensemble",
    "Gini Impurity & MDI Split Criterion": "Gini Impurity & MDI Split Criterion",
    "Each split optimizes the reduction in Gini impurity across randomly selected feature subspaces.": "Mỗi phân nhánh tối ưu hóa mức giảm Gini Impurity trên các feature subspace được chọn ngẫu nhiên.",
    "Ensemble Size": "Ensemble Size",
    "Number of bagged trees": "Tổng số cây bagged trong rừng",
    "Depth Limit": "Depth Limit",
    "Prevents tree overfitting": "Giới hạn độ sâu (chống Overfitting)",
    "Split Metric": "Split Metric",
    "Gini Impurity": "Gini Impurity",
    "Information impurity criterion": "Tiêu chuẩn đo impurity thông tin",
    "Feature Subset": "Feature Subset",
    "Random subspace dimension": "Kích thước feature subspace ngẫu nhiên",
    "Architectural Strengths": "Thế mạnh Kiến trúc",
    "Peak Precision: Generates only 1 False Positive across 38,357 test transactions.": "Peak Precision: Chỉ sinh duy nhất 1 False Positive trên 38,357 test samples.",
    "High Interpretability: Transparent decision paths and feature impurity scoring.": "High Interpretability: Decision path minh bạch và feature importance rõ ràng.",
    "Limitation: High computational training time (~1187s).": "Hạn chế: Thời gian training tương đối lâu (~1187s).",

    # Slide 13: XGBoost
    "Supervised Architecture 2: XGBoost Classifier": "Supervised Architecture 2: XGBoost Classifier",
    "Regularized Objective Function (2nd-Order Taylor)": "Regularized Objective Function (Taylor Bậc 2)",
    "where g_i and h_i are 1st and 2nd order gradients of the loss function with respect to previous predictions.": "trong đó g_i và h_i là 1st và 2nd order gradients của loss function theo dự đoán trước.",
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
    "Extremely low latency: < 0.5ms single-sample inference time.": "Single-sample inference latency cực thấp: < 0.5ms.",
    "Ideal for live financial transaction gateway screening.": "Lý tưởng để triển khai kiểm duyệt giao dịch real-time tại payment gateway.",

    # Slide 14: Deep Autoencoder
    "Unsupervised Architecture 3: Deep Autoencoder": "Unsupervised Architecture 3: Deep Autoencoder",
    "Reconstruction Loss & Decision Cutoff": "Reconstruction Loss & Decision Cutoff",
    "Samples with MSE exceeding the validation 95th percentile threshold tau are classified as anomalous.": "Các mẫu có MSE vượt quá ngưỡng validation 95th percentile (tau) được phân loại là Anomalous (Gian lận).",
    "Bottleneck": "Bottleneck",
    "Latent embedding representation": "Không gian biểu diễn ẩn nén (z in R^4)",
    "Loss Function": "Loss Function",
    "Mean squared reconstruction error": "Mean Squared Reconstruction Error (MSE)",
    "Activation": "Activation",
    "Non-linear hidden layer mappings": "Non-linear hidden layer mappings (ReLU)",
    "Threshold": "Decision Threshold",
    "95th percentile validation cutoff": "Ngưỡng quyết định 95th percentile (tau = 0.0455)",
    "Zero-Day Detection Role": "Vai trò Phát hiện Tấn công Zero-Day",
    "Achieves 75.23% Recall without observing any fraud labels during training.": "Đạt 75.23% Recall dù hoàn toàn không quan sát fraud labels khi training.",
    "Acts as a complementary defense layer for novel, unseen attack signatures.": "Đóng vai trò lớp phòng thủ bổ trợ đắc lực cho các attack signatures mới chưa từng xuất hiện.",

    # Slide 15: Divider 4
    "PART 04": "PHẦN 04",
    "EXPERIMENTS, RESULTS & COMPARATIVE EVALUATION": "KẾT QUẢ THỰC NGHIỆM & ĐÁNH GIÁ SO SÁNH",
    "Comprehensive Performance Benchmark (Precision, Recall, F1, AUC)": "Comprehensive Performance Benchmark (Precision, Recall, F1, ROC-AUC)",
    "Confusion Matrix & False Alarm vs. Missed Fraud Trade-offs": "Confusion Matrix & Đánh đổi False Alarm vs. Missed Fraud",
    "Feature Importance Attribution & Gain Contributions": "Feature Importance Attribution & Split Gain Contributions",
    "Autoencoder Anomaly Thresholding & Reconstruction Dynamics": "Autoencoder Anomaly Thresholding & Reconstruction Dynamics",

    # Slide 16: Benchmark Results
    "Experimental Results: Benchmark Comparison (N = 40,000)": "Kết quả Thực nghiệm: So sánh Đối chuẩn (N = 40,000)",
    "Model Architecture": "Model Architecture",
    "Resampling": "Resampling",
    "Train Time": "Train Time",
    "0.9973 (Best)": "0.9973 (Best)",
    "None (One-Class)": "None (One-Class)",
    "Key Empirical Deductions": "Đúc kết Thực nghiệm Cốt lõi",

    # Slide 17: Confusion Matrix
    "Confusion Matrix & Error Distribution Analysis": "Confusion Matrix & Phân tích Phân phối Sai số",
    "False Negative & False Positive Trade-off Analysis": "Phân tích Đánh đổi giữa False Negative và False Positive",
    "Both Random Forest and XGBoost miss only 8 fraud instances out of 1,643 true fraud cases (Recall = 99.51%).": "Cả Random Forest và XGBoost chỉ bỏ sót 8 ca gian lận trên tổng số 1,643 true fraud cases (Recall = 99.51%).",
    "RF-SMOTE generates only 1 False Alarm (FP=1), whereas Autoencoder generates 1,998 FP due to unsupervised 95% cutoff.": "RF-SMOTE chỉ sinh đúng 1 False Alarm (FP=1), trong khi Autoencoder sinh 1,998 FP do đặc thù cắt ngưỡng 95% cutoff.",

    # Slide 18: Feature Importance
    "Feature Importance: XGBoost Decision Split Gains": "Feature Importance: XGBoost Decision Split Gains",
    "Key Feature Insights": "Đúc kết Đặc trưng Quan trọng",
    "Top 2 features contribute > 97% of total tree split decisions.": "Top 2 features đóng góp > 97% vào tổng quyết định phân nhánh cây.",
    "Raw balance amounts without discrepancy deltas have low predictive power.": "Raw transaction amounts nếu không có sai số delta mang lại rất ít predictive power.",

    # Slide 19: Precision, Recall & F1
    "Comparative Evaluation: Precision, Recall & F1-Score": "Đánh giá So sánh: Precision, Recall & F1-Score",
    "Benchmarking Synthesis": "Tổng hợp Đối chuẩn",
    "SMOTE achieves superior boundary separation over ADASYN.": "SMOTE tạo decision boundary phân tách vượt trội hơn ADASYN.",
    "Supervised methods strongly dominate unsupervised reconstruction in known fraud types.": "Supervised learning áp đảo hoàn toàn unsupervised reconstruction trên các dạng gian lận đã biết.",

    # Slide 20: Autoencoder Thresholding
    "Autoencoder Anomaly Thresholding & Decision Boundary": "Autoencoder Anomaly Thresholding & Decision Boundary",
    "Threshold Calibration": "Threshold Calibration",
    "Tau = 0.0455 (95th percentile) optimizes the F1-Score trade-off curve.": "tau = 0.0455 (95th percentile) tối ưu hóa trade-off curve của F1-Score.",
    "Unsupervised model successfully flags 1,236 true fraud events.": "Unsupervised model gắn cờ thành công 1,236 sự kiện gian lận thực tế.",

    # Slide 21: Divider 5
    "PART 05": "PHẦN 05",
    "INTERACTIVE SYSTEM & FUTURE ROADMAP": "HỆ THỐNG THỰC THI & ĐỊNH HƯỚNG TƯƠNG LAI",
    "Streamlit Real-Time Inference Dashboard Architecture": "Streamlit Real-Time Inference Dashboard Architecture",
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

    # Slide 24: Q&A / References
    "THANK YOU FOR YOUR ATTENTION!": "CHÂN THÀNH CẢM ƠN THẦY VÀ CÁC BẠN ĐÃ LẮNG NGHE!",
    "CS106: ARTIFICIAL INTELLIGENCE  •  FINAL PROJECT DEFENSE  •  TEAM 09": "CS106: TRÍ TUỆ NHÂN TẠO  •  BÁO CÁO BẢO VỆ ĐỒ ÁN  •  NHÓM 09",
    "KEY ACADEMIC REFERENCES & PROJECT REPOSITORY": "TÀI LIỆU THAM KHẢO HỌC THUẬT & REPOSITORY DỰ ÁN",
    "We cordially welcome all questions, feedback, and discussions from the Committee.": "Nhóm 09 rất mong nhận được những câu hỏi và góp ý quý báu từ Hội đồng!"
}

# Multi-line & complex paragraph text replacements
COMPLEX_REPLACEMENTS = {
    # Slide 4
    "1. Industrial Context & Scale\n• Mobile money transactions have surged globally, introducing complex synthetic fraud vectors.\n• Real-time defense mechanisms require sub-100ms inference latency before funds leave the system.\n\n2. Extreme Class Imbalance (~0.13%)\n• Fraud accounts for only ~1 out of every 800 transactions in the PaySim universe.\n• Cost Asymmetry: False Negatives (missed fraud) lead to direct capital loss, while False Positives cause customer friction.\n\n3. Non-Stationary Fraud Patterns\n• Adversaries constantly morph account routing tactics to evade static rule-based threshold filters.":
    "1. Bối cảnh Thực tiễn & Quy mô\n• Giao dịch tiền di động (Mobile Money) tăng trưởng bùng nổ, kéo theo các thủ đoạn gian lận tinh vi.\n• Hệ thống phòng thủ đòi hỏi độ trễ suy luận thời gian thực (Inference Latency < 100ms) trước khi dòng tiền bị rút khỏi hệ thống.\n\n2. Extreme Class Imbalance (~0.13%)\n• Giao dịch gian lận chỉ chiếm ~1 trên 800 giao dịch trong tập dữ liệu PaySim.\n• Cost Asymmetry: Bỏ sót gian lận (False Negative) gây tổn thất vốn trực tiếp, trong khi Báo động nhầm (False Positive) gây phiền hà khách hàng.\n\n3. Non-Stationary Fraud Patterns\n• Kẻ gian liên tục biến đổi phương thức luân chuyển tiền để lẩn tránh các bộ lọc luật tĩnh (rule-based).",

    # Slide 8
    "• 100% of all fraud instances occur exclusively in TRANSFER and CASH_OUT transactions.\n• PAYMENT, CASH_IN, and DEBIT categories exhibit exactly 0.0% fraud.\n• Pipeline Action: Filter non-vulnerable categories to eliminate 68% of ambient noise.":
    "• 100% giao dịch gian lận chỉ xuất hiện ở TRANSFER và CASH_OUT.\n• Các loại PAYMENT, CASH_IN và DEBIT hoàn toàn không có gian lận (0%).\n• Pipeline Action: Lọc dữ liệu chỉ giữ lại TRANSFER & CASH_OUT để triệt tiêu 70% nhiễu.",

    "• 97.56% of fraudulent transfers result in newbalanceOrig == 0.\n• Perpetrators systematically drain the victim's entire balance in a single execution step.\n• High-confidence heuristic: Full-balance transfer implies severe compromise.":
    "• 97.56% giao dịch gian lận làm số dư nguồn về đúng bằng 0 (newbalanceOrig == 0).\n• Kẻ gian tìm cách vét sạch toàn bộ số dư của nạn nhân trong 1 lần chuyển duy nhất.\n• Key Signal: Tỷ lệ rút cạn tài khoản đóng vai trò phân loại chính.",

    "• A massive proportion of fraud transactions show zero balance delta at the destination.\n• Large funds are transferred out of the origin without appearing in recipient ledgers.":
    "• Tỷ lệ lớn giao dịch gian lận có độ lệch biến động số dư tại đích bằng 0.\n• Dòng tiền lớn chuyển ra khỏi nguồn nhưng không được ghi tăng tương ứng ở sổ cái đích.",

    # Slide 11
    "• A trivial baseline predicting 100% \"Legitimate\" achieves 99.87% Accuracy yet misses all fraud.\n\n• Evaluation Mandate: Model selection must be strictly governed by Precision, Recall, F1-Score, and PR-AUC.":
    "• Một baseline ngây thơ dự đoán 100% \"Hợp lệ\" đạt Accuracy 99.87% nhưng bỏ sót 100% gian lận.\n\n• Evaluation Mandate: Lựa chọn model phải được dẫn dắt tuyệt đối bởi Precision, Recall, F1-Score và PR-AUC.",

    # Slide 12
    "Ensemble Bagging Architecture:\n• Constructs an ensemble of B decorrelated Decision Trees trained on bootstrap sub-samples.\n• Reduces variance without inflating bias, demonstrating high resilience against feature co-linearity.\n• Provides Gini Impurity-based Mean Decrease in Impurity (MDI) feature ranking.\n\nOptimal Hyperparameter Configuration:\n• n_estimators: 200 (SMOTE) / 500 (ADASYN)\n• max_depth: 20 | min_samples_split: 2 | max_features: \"sqrt\" | class_weight: \"balanced\"":
    "Ensemble Bagging Architecture:\n• Xây dựng tập hợp B Decision Trees độc lập huấn luyện trên các bootstrap sub-samples.\n• Lấy trung bình dự đoán giúp giảm mạnh variance mà không làm tăng bias, chống feature multicollinearity cực tốt.\n• Cung cấp xếp hạng tầm quan trọng đặc trưng theo Mean Decrease in Impurity (Gini MDI).\n\nCấu hình Hyperparameter Tối ưu:\n• n_estimators: 200 (SMOTE) / 500 (ADASYN)\n• max_depth: 20 | min_samples_split: 2 | max_features: \"sqrt\" | class_weight: \"balanced\"",

    "Exceptional resistance to feature multicollinearity and outliers.\nConsistently stable generalization performance on unseen test distributions.":
    "Khả năng chống chịu cực tốt trước hiện tượng feature multicollinearity và nhiễu ngoại lai.\nKhả năng tổng quát hóa ổn định vượt trội trên unseen test distributions.",

    # Slide 13
    "Gradient Boosted Decision Trees (GBDT):\n• Minimizes a regularized objective function using second-order Taylor expansion.\n• Incorporates explicit L1/L2 leaf regularization to prevent over-complex structures.\n• High Throughput: Trains in ~41.6s (28.5x faster than Random Forest ~1187s).\n\nTuned Hyperparameter Setup:\n• learning_rate (eta): 0.2 | n_estimators: 300 | max_depth: 8\n• subsample: 0.85 | colsample_bytree: 1.0 | eval_metric: \"logloss\"":
    "Gradient Boosted Decision Trees (GBDT):\n• Tối thiểu hóa hàm mục tiêu có regularization bằng khai triển Taylor bậc 2.\n• Tích hợp explicit L1/L2 regularization trên lá để kiểm soát độ phức tạp của cây.\n• High Throughput: Training chỉ mất ~41.6s (nhanh hơn 28.5 lần so với Random Forest ~1187s).\n\nTuned Hyperparameter Setup:\n• learning_rate (eta): 0.2 | n_estimators: 300 | max_depth: 8\n• subsample: 0.85 | colsample_bytree: 1.0 | eval_metric: \"logloss\"",

    "Near-identical F1-score (99.63%) compared to Random Forest (99.73%).\nExtremely low latency: < 0.5ms single-sample inference time.\nIdeal for live financial transaction gateway screening.":
    "F1-score đạt 99.63%, gần như tương đương tuyệt đối với Random Forest (99.73%).\nSingle-sample inference latency cực thấp: < 0.5ms.\nLý tưởng để triển khai kiểm duyệt giao dịch real-time tại payment gateway.",

    # Slide 14
    "One-Class Semi-Supervised Anomaly Detection:\n• Network is trained EXCLUSIVELY on legitimate transactions (N = 122,744 normal samples).\n• Learns a low-dimensional manifold encoding normal transaction behavior.\n• Anomaly Scoring: Fraudulent instances fail reconstruction -> Yield high Reconstruction Error.\n\nArchitectural Specifications:\n• Symmetric Topology: 16 -> 8 -> 4 (Bottleneck) -> 8 -> 16\n• Optimizer: Adam (lr=1e-3) | Loss: MSE | Threshold: tau = 0.045456 (95th percentile)":
    "One-Class Semi-Supervised Anomaly Detection:\n• Mạng được huấn luyện HOÀN TOÀN trên legitimate transactions (N = 122,744 normal samples).\n• Học low-dimensional manifold biểu diễn hành vi giao dịch bình thường.\n• Anomaly Scoring: Giao dịch gian lận không thể tái tạo chuẩn -> Reconstruction Error (MSE) tăng vọt.\n\nCấu hình Kiến trúc Mạng:\n• Symmetric Topology: 16 -> 8 -> 4 (Bottleneck) -> 8 -> 16\n• Optimizer: Adam (lr=1e-3) | Loss: MSE | Threshold: tau = 0.045456 (95th percentile)",

    # Slide 16
    "RF + SMOTE achieves peak F1-Score (99.73%) with only 1 False Positive across 38,357 legitimate test samples.\nXGBoost achieves near-identical classification performance (F1 99.63%) with 28.5x computational speedup.\nAutoencoder detects 75.23% of fraud cases in an entirely unsupervised setting without seeing fraud labels.":
    "RF + SMOTE đạt đỉnh F1-Score (99.73%) với chỉ duy nhất 1 False Positive trên 38,357 legitimate test samples.\nXGBoost đạt classification performance gần như tương đương (F1 99.63%) nhưng training time nhanh hơn 28.5 lần.\nAutoencoder phát hiện được 75.23% ca gian lận trong bối cảnh hoàn toàn unsupervised, không cần fraud labels.",

    # Slide 18
    "Top 2 features contribute > 97% of total tree split decisions.\nRaw balance amounts without discrepancy deltas have low predictive power.":
    "Top 2 features đóng góp > 97% vào tổng quyết định phân nhánh cây.\nRaw transaction amounts nếu không có sai số delta mang lại rất ít predictive power.",

    "Insights from XGBoost Feature Gain:\n\n• errorBalanceOrig accounts for ~49.9% of model decision splits.\n\n• newbalanceOrig provides ~47.2% additional predictive power.\n\n• Combined Impact: Engineered ledger discrepancies capture over 97% of overall fraud dynamics, proving the critical efficacy of domain feature engineering.":
    "Insights từ XGBoost Feature Gain:\n\n• errorBalanceOrig chiếm ~49.9% tổng trọng số phân nhánh của model.\n\n• newbalanceOrig bổ sung thêm ~47.2% predictive power cho cây quyết định.\n\n• Tác động kết hợp: Các engineered ledger discrepancies nắm giữ hơn 97% động lực phân loại gian lận, chứng minh tính hiệu quả vượt bậc của domain feature engineering.",

    # Slide 19
    "Resampling Performance Analysis:\n\n• SMOTE consistently outperforms ADASYN across all decision tree architectures.\n\n• ADASYN synthesizes excess noise instances in boundary overlap zones, slightly increasing False Positives.\n\n• Recommendation: Deploy XGBoost + SMOTE for optimal inference throughput and fraud detection precision in live production environments.":
    "Phân tích Hiệu năng Resampling:\n\n• SMOTE vượt trội hơn ADASYN một cách nhất quán trên mọi tree architectures.\n\n• ADASYN sinh nhiều synthetic noise ở vùng boundary overlap, làm tăng nhẹ False Positives.\n\n• Khuyến nghị: Triển khai XGBoost + SMOTE để tối ưu hóa inference throughput và fraud detection precision trong môi trường production.",

    # Slide 20
    "Threshold Sweep Dynamics:\n\n• 95th Percentile (tau = 0.0455):\nBalances Recall (75.2%) with Precision (38.2%).\n\n• 99.9th Percentile (tau = 0.7460):\nPrecision jumps to 91.5% but Recall drops to 25.4%.\n\n• Operational Role: Excellent as a secondary zero-day defense layer for unlabelled novel fraud patterns.":
    "Động lực Quét Ngưỡng (Threshold Sweep):\n\n• 95th Percentile (tau = 0.0455):\nCân bằng giữa Recall (75.2%) và Precision (38.2%).\n\n• 99.9th Percentile (tau = 0.7460):\nPrecision tăng vọt lên 91.5% nhưng Recall giảm xuống 25.4%.\n\n• Vai trò Vận hành: Đóng vai trò secondary zero-day defense layer đắc lực trước các hình thức gian lận mới chưa có label.",

    # Slide 24
    "[1] E. A. Lopez-Rojas, A. Elmir, S. Axelsson. \"PaySim: A Financial Mobile Money Simulator for Fraud Detection\", 28th EMSS, 2016.\n[2] T. Chen, C. Guestrin. \"XGBoost: A Scalable Tree Boosting System\", Proc. 22nd ACM SIGKDD, 2016.\n[3] N. V. Chawla, K. W. Bowyer, L. O. Hall, W. P. Kegelmeyer. \"SMOTE: Synthetic Minority Over-sampling Technique\", JAIR, 2002.\n[4] L. Breiman. \"Random Forests\", Machine Learning, 45(1), pp. 5-32, 2001.\n[5] Project Submodule: https://github.com/uit-25730067-chithanh/CS106-Team09-Fraud-Detection":
    "[1] E. A. Lopez-Rojas, A. Elmir, S. Axelsson. \"PaySim: A Financial Mobile Money Simulator for Fraud Detection\", 28th EMSS, 2016.\n[2] T. Chen, C. Guestrin. \"XGBoost: A Scalable Tree Boosting System\", Proc. 22nd ACM SIGKDD, 2016.\n[3] N. V. Chawla, K. W. Bowyer, L. O. Hall, W. P. Kegelmeyer. \"SMOTE: Synthetic Minority Over-sampling Technique\", JAIR, 2002.\n[4] L. Breiman. \"Random Forests\", Machine Learning, 45(1), pp. 5-32, 2001.\n[5] Mã nguồn Dự án: https://github.com/uit-25730067-chithanh/CS106-Team09-Fraud-Detection"
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

for s_idx, slide in enumerate(prs.slides):
    for shape in slide.shapes:
        if shape.has_text_frame:
            safe_replace_tf(shape.text_frame)
        elif shape.has_table:
            for row in shape.table.rows:
                for cell in row.cells:
                    safe_replace_tf(cell.text_frame)

prs.save(output_pptx)
print(f'Successfully updated standard terminology PPTX: {output_pptx}')
