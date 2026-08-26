# CS106 — Final Project Index

<p align="center">
  <img src="./docs/cover.png" alt="Financial Fraud Detection Project Cover" width="100%" style="border-radius: 8px;" />
</p>

> **Môn học:** Trí tuệ Nhân tạo (CS106) — UIT, ĐHQG-HCM  
> **Đề tài:** #7 — Hệ thống Phát hiện Giao dịch Tài chính Bất thường  
> **Nhóm:** 9 | **Thành viên:** 7 người

---

## 📂 Cấu trúc thư mục

```
Final/
├── docs/                          ← Đề bài gốc từ giảng viên (PDF)
│   └── 2026, De tai mon TTNT 2 - He tu xa.pdf
│
├── draft/                         ← Workspace làm việc của nhóm
│   └── fraud-detection/           ← Project chính (đang phát triển)
│       ├── src/                   ← Source code Python
│       ├── notebooks/             ← Jupyter notebooks
│       ├── data/                  ← Dataset (raw + processed)
│       ├── docs/                  ← Tài liệu kỹ thuật
│       ├── reports/               ← Kết quả, biểu đồ
│       ├── demo/                  ← Demo UI
│       └── README.md
│
├── submit/                        ← Bản nộp chính thức (ZIP cuối)
│   └── (trống — điền vào khi nộp bài)
│
└── README.md                      ← File này
```

---

## 🎯 Tổng quan dự án

| Thông tin | Chi tiết |
|-----------|---------|
| **Bài toán** | Binary Classification — Phân loại giao dịch gian lận |
| **Dataset** | [PaySim Mobile Money — Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1) (Downsample còn ~200,000 mẫu) |
| **Models** | Random Forest, XGBoost, Autoencoder |
| **Imbalance** | SMOTE / ADASYN (~0.13% fraud gốc, điều chỉnh khi downsample) |
| **Metrics** | F1-Score, ROC-AUC, Precision, Recall |
| **Nộp bài** | Tên: `[Project AI-UIT] - Nhóm 9` |

---

## 👥 Phân công nhóm

| Người | Lớp | Vai trò chính | Số tasks |
|-------|-----|--------------|----------|
| **Trần Hoàng Hôn** (trưởng) | A | PM + Theo dõi tiến độ + PPT + Nộp bài | 5 |
| **Nguyễn Duy Khang** | A | Viết Evaluation scripts + Chạy metrics + Bảng so sánh | 6 |
| **Vũ Văn Duy** | A | Báo cáo Word: Intro → Methodology → Results → Format | 6 |
| **Phạm Thành Trung** | A | Demo UI: Wireframe → Implement → Kết nối model → Demo clip | 5 |
| **Đặng Chí Thanh** | B | EDA + Preprocessing + Feature Engineering | 5 |
| **Bùi Thị Mỷ Cẩm** | B | XGBoost + Autoencoder + Lưu models | 5 |
| **Hoàng Cao Sơn** | B | Imbalance Analysis + SMOTE/ADASYN + Random Forest | 5 |

---

## 📊 Tiến độ

| Sprint | Nội dung công việc | Trạng thái | Người phụ trách |
|--------|-------------------|-----------|------------------|
| **Sprint 1 (25/8 – 28/8)** | Khởi tạo Repo, phân công & thiết kế khung dự án | ✅ Xong | Thanh + Hôn |
| **Sprint 2 (28/8 – 4/9)** | Phân tích dữ liệu (EDA), viết evaluation scripts & thiết kế UI demo | 🔲 Chưa làm | Cả nhóm (song song) |
| **Sprint 3 (4/9 – 11/9)** | Xử lý mất cân bằng & huấn luyện các mô hình (RF, XGBoost, Autoencoder) | 🔲 Chưa làm | Thanh + Sơn + Cẩm |
| **Sprint 4 (11/9 – 18/9)** | Đánh giá so sánh, tích hợp model vào UI & hoàn thiện báo cáo Word/PPT | 🔲 Chưa làm | Khang + Trung + Duy + Hôn |
| **Nộp bài (18/9)** | Đóng gói zip & Nộp bài chính thức trước deadline | 🔲 Chưa làm | Hôn |

---

## 🔗 Links nhanh

- [Đề bài (PDF)](./docs/2026,%20De%20tai%20mon%20TTNT%202%20-%20He%20tu%20xa.pdf)
- [Project README](./draft/fraud-detection/README.md)
- [Lộ trình & Phân công](./draft/fraud-detection/docs/project-roadmap.md)
- [Kiến trúc hệ thống](./draft/fraud-detection/docs/system-architecture.md)
- [Code Standards](./draft/fraud-detection/docs/code-standards.md)

---

## 📦 Hướng dẫn nộp bài

Khi hoàn thành, tạo thư mục trong `submit/`:

```
submit/
└── [Project AI-UIT] - Nhom 9/
    ├── code/                ← Toàn bộ src/ + notebooks/
    ├── report/              ← File Word báo cáo
    ├── slides/              ← File PPT
    └── demo/                ← Clip hoặc ảnh demo
```

Zip lại: `[Project AI-UIT] - Nhom 9.zip`
