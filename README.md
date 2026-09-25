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
| **Nộp bài** | Tên: `CS106_F31_CN2 - Nhom 9` |

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
| **Sprint 4 (11/9 – 18/9)** | Hoàn thiện Demo UI tương tác, quy trình phân tích 4 bước, import CSV/JSON, video demo Google Drive (Trung ✅); xuất bản báo cáo DOCX/PDF chuẩn UIT (Duy ✅); hiệu chỉnh kịch bản thuyết trình toàn team theo diễn tập meeting (Hôn ✅). | ✅ Hoàn tất Sprint 4 (9/9 phases passed — 100%) | Cả nhóm |
| **Nộp bài (20/9)** | Đóng gói cấu trúc nộp bài `CS106_F31_CN2 - Nhom 9` (50 deliverables sạch, an toàn Git, 102 tests pass) & Sẵn sàng nộp chính thức trước deadline 28/09 (Phase 08) | ✅ Hoàn thành đóng gói | Hôn |


---

## 🔗 Links nhanh

- [Đề bài (PDF)](./docs/2026,%20De%20tai%20mon%20TTNT%202%20-%20He%20tu%20xa.pdf)
- [Project README](./draft/fraud-detection/README.md)
- [Lộ trình & Phân công](./draft/fraud-detection/docs/project-roadmap.md)
- [Kiến trúc hệ thống](./draft/fraud-detection/docs/system-architecture.md)
- [Code Standards](./draft/fraud-detection/docs/code-standards.md)
- [Dữ liệu đã xử lý (data/processed)](./draft/fraud-detection/data/processed/README.md) ← **đọc trước khi dùng `.pkl`**

---

## 📦 Hướng dẫn đóng gói & nộp bài chuẩn UIT

Gói bài nộp chính thức được tự động chuẩn bị và kiểm định qua script:
`draft/fraud-detection/scripts/package_submission.py`

### 1. Cấu trúc thư mục chuẩn nộp bài (`CS106_F31_CN2 - Nhom 9/`)

```text
CS106_F31_CN2 - Nhom 9/
├── Danh_sach_nhom.xlsx                     ← [1] Danh sách nhóm Excel (7 thành viên, MSSV, Lớp)
├── Bao_cao/                                ← [2] Báo cáo học thuật & Slide thuyết trình
│   ├── [Nhom9]_Report_FraudDetection.pdf   ← Báo cáo học thuật chính thức (Chương 1–7, 31 trang)
│   └── [Nhom9]_Slide_FraudDetection.pdf    ← Slide thuyết trình dạng PDF (21 trang)
└── Chuong_trinh/                           ← [3] Chương trình & Thực nghiệm
    ├── Huong_dan_su_dung.pdf               ← Hướng dẫn sử dụng (bản PDF in học thuật chuẩn UIT)
    ├── requirements.txt                    ← Danh sách thư viện Python phụ thuộc tối giản
    ├── demo/                               ← Minh chứng sản phẩm Demo & Mã nguồn Web UI
    │   ├── Link_video_demo.txt             ← Liên kết video clip demo chính thức (1 phút 37 giây)
    │   ├── screenshots/                    ← Bộ 6 ảnh chụp màn hình UI thực tế qua Playwright
    │   ├── app.py                          ← Ứng dụng Web Demo Streamlit tương tác
    │   ├── models/                         ← Trọng số mô hình phục vụ Demo (XGBoost & Scaler)
    │   └── assets/                         ← Logo nhận diện ứng dụng Fraud Shield
    └── code/                               ← Toàn bộ mã nguồn giải thuật & thực nghiệm
        ├── src/                            ← 4 modules Python modular (preprocessing, models, evaluation, utils)
        ├── notebooks/                      ← 6/6 Jupyter Notebooks thực nghiệm chạy sạch 100%
        ├── data/processed/                 ← 8 tệp .pkl tiền xử lý (chạy ngay không cần 500MB raw)
        └── reports/                        ← 3 tệp predictions .pkl (đầu vào cho Notebook 06 đối sánh)
```

### 2. Trạng thái nghiệm thu & các lưu ý của Nhóm 9:
* **Báo cáo & Slide:** Báo cáo PDF 31 trang (`[Nhom9]_Report_FraudDetection.pdf`) và Slide PDF 21 trang (`[Nhom9]_Slide_FraudDetection.pdf`) đã hoàn tất nghiệm thu và đồng bộ 100% số liệu.
* **Hướng dẫn sử dụng:** File `Huong_dan_su_dung.pdf` trình bày theo chuẩn học thuật (Times New Roman, bảng booktabs, đơn sắc trắng đen tương đồng với báo cáo), hướng dẫn chi tiết chạy 6 Notebooks thực nghiệm và khởi chạy ứng dụng Web UI Streamlit. Bản nháp `.docx` được lưu trữ tại `draft/fraud-detection/docs/` và `tmp/`.
* **Liên kết video demo:** File `Link_video_demo.txt` cung cấp liên kết video clip demo Full HD 1 phút 37 giây tại [https://aceteam-uit.vercel.app/l/70vGyu](https://aceteam-uit.vercel.app/l/70vGyu) và được minh họa tại Trang 15 của Slide PDF.
* **Mã nguồn đầy đủ & Tests:** Toàn bộ ứng dụng Web UI Streamlit, pipeline ML và 116 unit/integration tests được đóng gói và lưu trữ đầy đủ tại GitHub Repository chính thức.

### 3. Lệnh đóng gói và nén file:
```bash
# Kiểm tra thử (không làm thay đổi file):
python draft/fraud-detection/scripts/package_submission.py --dry-run

# Đóng gói vào submit/CS106_F31_CN2 - Nhom 9:
python draft/fraud-detection/scripts/package_submission.py

# Hoặc tự nén ZIP:
cd submit && zip -r "CS106_F31_CN2 - Nhom 9.zip" "CS106_F31_CN2 - Nhom 9"
```
