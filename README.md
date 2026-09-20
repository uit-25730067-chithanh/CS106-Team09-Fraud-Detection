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
| **Sprint 2 (28/8 – 4/9)** | EDA ✅, Preprocessing ✅, Imbalance (SMOTE/ADASYN) ✅, Random Forest ✅, XGBoost & Autoencoder ✅, Báo cáo Word nháp (Chương 1–3) ✅, Slide PPT 21 slides học thuật & Kịch bản toàn team ✅, Streamlit UI Shell ✅ | ✅ Vượt tiến độ | Cả nhóm (song song) |
| **Sprint 3 (4/9 – 11/9)** | Đầy đủ 6/6 notebooks hoàn thành & chạy sạch; Phase 05 Evaluation hoàn tất (Khang ✅); Báo cáo Tóm tắt + Chương 1–7 (32 trang DOCX/PDF, số liệu khớp 100% Phase 05); Demo UI kết nối model thật + mapping datetime/VNĐ (Trung ✅); Slide 21 trang & Kịch bản 7 người chính thức duyệt (Hôn ✅); PM Audit Sprint 3 Closing (Hôn ✅). | ✅ Hoàn tất Sprint 3 | Cả nhóm |
| **Sprint 4 (11/9 – 18/9)** | Hoàn thiện Demo UI tương tác, quy trình phân tích 4 bước, import CSV/JSON, video demo Google Drive (Trung ✅); xuất bản báo cáo DOCX/PDF chuẩn UIT (Duy ✅); hiệu chỉnh kịch bản thuyết trình ~23–25 phút theo diễn tập meeting (Hôn ✅). | ✅ Hoàn tất Sprint 4 (9/9 phases passed — 100%) | Cả nhóm |
| **Nộp bài (18/9)** | Đóng gói tự động `[Project AI-UIT] - Nhom 9.zip` (118.58 MB, 128 files, 116 tests pass) & Sẵn sàng nộp chính thức trước deadline (Phase 08) | ✅ Hoàn thành đóng gói | Hôn |

---

## 🔗 Links nhanh

- [Đề bài (PDF)](./docs/2026,%20De%20tai%20mon%20TTNT%202%20-%20He%20tu%20xa.pdf)
- [Project README](./draft/fraud-detection/README.md)
- [Lộ trình & Phân công](./draft/fraud-detection/docs/project-roadmap.md)
- [Kiến trúc hệ thống](./draft/fraud-detection/docs/system-architecture.md)
- [Code Standards](./draft/fraud-detection/docs/code-standards.md)
- [Dữ liệu đã xử lý (data/processed)](./draft/fraud-detection/data/processed/README.md) ← **đọc trước khi dùng `.pkl`**

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
