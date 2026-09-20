# Submit — Bản nộp chính thức

> Thư mục này dành cho **bản nộp cuối cùng** của Nhóm 9.
> Không đặt file làm việc ở đây — chỉ để bản đã hoàn thiện.

---

## Hướng dẫn chuẩn bị nộp bài

Khi cả nhóm hoàn thành, copy và tổ chức theo cấu trúc:

```
submit/
└── [Project AI-UIT] - Nhom 9/
    ├── code/
    │   ├── src/            ← Copy từ draft/fraud-detection/src/
    │   ├── notebooks/      ← Copy từ draft/fraud-detection/notebooks/
    │   └── requirements.txt
    ├── report/
    │   └── [Nhom9]_BaoCao_FraudDetection.docx
    ├── slides/
    │   └── [Nhom9]_PPT_FraudDetection.pptx
    └── demo/
        └── demo_clip.mp4 (hoặc screenshots)
```

Sau đó zip thành: **`[Project AI-UIT] - Nhom 9.zip`**

---

## Checklist trước khi nộp (Hoàn tất 17/09/2026)

- [x] Tất cả 6/6 notebooks chạy được từ đầu đến cuối (Restart & Run All) không lỗi
- [x] Mỗi model có đủ: Confusion Matrix + Precision/Recall/F1 + ROC-AUC (5 biến thể)
- [x] Có bảng so sánh tổng hợp các model (`reports/model_comparison.csv`)
- [x] Báo cáo Word/PDF có đủ: Tóm tắt, Giới thiệu, Dữ liệu, Phương pháp, Kết quả, Thảo luận, Kết luận (Chương 1–7)
- [x] PPT có slide kết quả và biểu đồ (Bộ Slide học thuật 21 trang đã duyệt chính thức)
- [x] Demo: Đã lưu 5 screenshots chuẩn hóa và kịch bản demo vào `demo/screenshots/`
- [x] File nộp đúng tên chuẩn: `[Project AI-UIT] - Nhom 9.zip` (dung lượng 118.58 MB, 128 files, loại trừ triệt để .env và paysim.csv)
- [x] Toàn bộ 116/116 automated unit/integration tests vượt qua 100%
- [x] Script tự động đóng gói `draft/fraud-detection/src/reporting/package_submission.py` hoạt động hoàn hảo
