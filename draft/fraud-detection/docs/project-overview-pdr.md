# Project Overview — Financial Fraud Detection (Đề tài 7)

## Tổng quan dự án

**Tên dự án:** Hệ thống Phát hiện Giao dịch Tài chính Bất thường và Nghi vấn Gian lận  
**Môn học:** CS106 — Trí tuệ Nhân tạo  
**Nhóm:** 9 (7 thành viên)  
**Ngày báo cáo:** Buổi 10

---

## Vấn đề cần giải quyết

Gian lận thẻ tín dụng gây thiệt hại hàng tỷ USD mỗi năm trên toàn cầu. Bài toán phát hiện gian lận có hai thách thức chính:

1. **Mất cân bằng dữ liệu cực độ**: Tỷ lệ giao dịch gian lận chỉ ~0.17% → Accuracy truyền thống vô nghĩa
2. **Chi phí lỗi không đối xứng**: False Negative (bỏ sót gian lận) tốn kém hơn nhiều False Positive

## Mục tiêu

- Xây dựng pipeline phát hiện gian lận end-to-end
- Thử nghiệm ≥2 thuật toán (Random Forest, XGBoost, Autoencoder)
- Xử lý mất cân bằng với SMOTE và/hoặc ADASYN
- Đánh giá bằng Precision, Recall, F1-Score, ROC-AUC

## Dataset

| Thuộc tính | Giá trị |
|-----------|---------|
| Nguồn | [Kaggle — PaySim Mobile Money Fraud](https://www.kaggle.com/datasets/ealaxi/paysim1) |
| Số mẫu | 6,362,620 giao dịch (Downsample còn ~200,000) |
| Features | 10 (step, type, amount, oldbalanceOrg, newbalanceOrig, oldbalanceDest, newbalanceDest...) + 1 label (isFraud) |
| Tỷ lệ gian lận | 8,213 / 6,362,620 ≈ 0.13% (Giữ toàn bộ mẫu gian lận khi downsample) |
| Yêu cầu tối thiểu đề | ≥500 mẫu ✅ (8,213 mẫu > 500) |

## Phạm vi đề tài

- ✅ EDA và phân tích phân phối
- ✅ Preprocessing và chuẩn hóa dữ liệu
- ✅ Xử lý imbalanced data (SMOTE/ADASYN)
- ✅ ≥2 models (RF + XGBoost bắt buộc; Autoencoder bonus)
- ✅ Evaluation đúng chuẩn (không dùng Accuracy đơn thuần)
- ✅ Báo cáo Word + PPT + Code + Demo

## Ngoài phạm vi

- ❌ Deploy lên production server
- ❌ Real-time transaction monitoring
- ❌ Integration với banking system thực tế
