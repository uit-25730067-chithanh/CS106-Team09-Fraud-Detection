#!/usr/bin/env python3
"""
CS106 Final Project Submission Packager — Nhóm 9 (Financial Fraud Detection)
Prepares and verifies the canonical, clean submission directory:
`submit/CS106_F31_CN2 - Nhom 9/` according to UIT university course requirements.

Cấu trúc thư mục chuẩn nộp bài (Chuẩn tối giản UIT, 0 file rác):
CS106_F31_CN2 - Nhom 9/
├── Danh_sach_nhom.xlsx                     ← [1] Danh sách nhóm Excel (7 thành viên, MSSV, Lớp)
├── Bao_cao/                                ← [2] Báo cáo học thuật & Slide thuyết trình
│   ├── [Nhom9]_Report_FraudDetection.pdf   ← Báo cáo học thuật chính thức (Chương 1–7, 31 trang)
│   └── [Nhom9]_Slide_FraudDetection.pdf    ← Slide thuyết trình dạng PDF (21 trang)
└── Chuong_trinh/                           ← [3] Chương trình & Thực nghiệm
    ├── Huong_dan_su_dung.pdf               ← Hướng dẫn sử dụng (bản PDF in chuẩn UIT theo phong cách học thuật)
    ├── requirements.txt                    ← Danh sách thư viện Python phụ thuộc
    ├── demo/                               ← Ứng dụng Demo Streamlit Fraud Shield
    │   ├── Link_video_demo.txt             ← Liên kết video clip demo chính thức (1 phút 37 giây)
    │   ├── app.py                          ← Giao diện Streamlit chính
    │   ├── ...                             ← 7 modules logic phụ trợ demo & assets/
    │   ├── models/                         ← Trọng số model chạy inference (xgb_smote.json, scaler.pkl)
    │   └── screenshots/                    ← 6 ảnh chụp màn hình UI thực tế qua Playwright
    └── code/                               ← Toàn bộ mã nguồn giải thuật & thực nghiệm
        ├── src/                            ← 4 modules Python: preprocessing, models, evaluation, utils
        ├── notebooks/                      ← 6/6 Jupyter Notebooks thực nghiệm chạy sạch 100%
        ├── data/processed/                 ← 8 tệp .pkl tiền xử lý (chạy ngay không cần 500MB raw)
        └── reports/                        ← Đối sánh mô hình, biểu đồ và 3 predictions .pkl

Usage:
    python scripts/package_submission.py            # Chuẩn bị và kiểm định thư mục nộp bài
    python scripts/package_submission.py --zip      # Chỉ nén ZIP khi người dùng yêu cầu
"""

from __future__ import annotations

import os
import sys
import shutil
import zipfile
import hashlib
import argparse
from pathlib import Path
from datetime import datetime

EXCLUDE_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache",
    "node_modules", ".idea", ".vscode", "tmp", ".data",
    ".ipynb_checkpoints", ".mypy_cache", ".ruff_cache",
}

EXCLUDE_FILES = {
    ".DS_Store", ".gitkeep"
}

EXCLUDE_EXTS = {
    ".pyc", ".pyo", ".tmp", ".log"
}

SUBMISSION_NAME = "CS106_F31_CN2 - Nhom 9"


def calculate_sha256(file_path: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()


def copy_file_safe(src: Path, dst: Path):
    """Copy file ensuring parent directory exists."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def copy_clean_tree(src: Path, dst: Path, skip_names: set[str] = None):
    """Recursively copy directory tree filtering out caches and junk files."""
    if not src.exists():
        return
    dst.mkdir(parents=True, exist_ok=True)
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        rel_root = Path(root).relative_to(src)
        target_root = dst / rel_root
        target_root.mkdir(parents=True, exist_ok=True)
        for f in files:
            if f in EXCLUDE_FILES or f.startswith("._") or f.startswith("~$") or f.startswith(".env") or f.endswith(tuple(EXCLUDE_EXTS)):
                continue
            if skip_names and f in skip_names:
                continue
            if f in {"paysim.csv", "creditcard.csv"}:
                continue
            if f.endswith(".mp4") and "clip" in Path(root).parts:
                continue
            copy_file_safe(Path(root) / f, target_root / f)


def assemble_submission(final_dir: Path, bundle_dir: Path):
    """Assemble project deliverables into canonical UIT submission tree."""
    draft_dir = final_dir / "draft" / "fraud-detection"

    # Preserve canonical submission-only documents if already present in bundle_dir
    preserved: dict[Path, bytes] = {}
    for rel_path in [
        Path("Danh_sach_nhom.xlsx"),
        Path("Chuong_trinh/Huong_dan_su_dung.pdf"),
        Path("Chuong_trinh/demo/Link_video_demo.txt"),
        Path("Chuong_trinh/demo/LINK_VIDEO_DEMO.txt"),
    ]:
        p = bundle_dir / rel_path
        if not p.exists():
            p = final_dir / "submit" / SUBMISSION_NAME / rel_path
        if p.exists():
            preserved[rel_path] = p.read_bytes()

    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)
    bundle_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Assembling deliverables into: {bundle_dir}")

    # 1. Danh sách nhóm (Excel)
    team_excel = bundle_dir / "Danh_sach_nhom.xlsx"
    if Path("Danh_sach_nhom.xlsx") in preserved:
        team_excel.write_bytes(preserved[Path("Danh_sach_nhom.xlsx")])

    # 2. Bao_cao (Official PDF report & PDF slide)
    bao_cao = bundle_dir / "Bao_cao"
    bao_cao.mkdir(parents=True, exist_ok=True)
    report_pdf = draft_dir / "reports" / "[Nhom9]_Report_FraudDetection.pdf"
    if not report_pdf.exists():
        report_pdf = draft_dir / "reports" / "[Nhom9]_BaoCao_FraudDetection.pdf"
    if report_pdf.exists():
        shutil.copy2(report_pdf, bao_cao / "[Nhom9]_Report_FraudDetection.pdf")

    pdf_slide = draft_dir / "slide" / "[Nhom9]_Slide_FraudDetection.pdf"
    if not pdf_slide.exists():
        pdf_slide = draft_dir / "slide" / "[Nhom9]_Slide_FraudDetection_Academic_VN.pdf"
    if pdf_slide.exists():
        shutil.copy2(pdf_slide, bao_cao / "[Nhom9]_Slide_FraudDetection.pdf")

    # 3. Chuong_trinh
    prog = bundle_dir / "Chuong_trinh"
    prog.mkdir(parents=True, exist_ok=True)

    # 3.1 Single unified guide (PDF) & requirements
    guide_pdf = prog / "Huong_dan_su_dung.pdf"
    if (draft_dir / "docs" / "Huong_dan_su_dung.pdf").exists():
        shutil.copy2(draft_dir / "docs" / "Huong_dan_su_dung.pdf", guide_pdf)
    elif Path("Chuong_trinh/Huong_dan_su_dung.pdf") in preserved:
        guide_pdf.write_bytes(preserved[Path("Chuong_trinh/Huong_dan_su_dung.pdf")])

    req_candidates = [
        draft_dir / "requirements.txt",
    ]
    for r in req_candidates:
        if r.exists():
            shutil.copy2(r, prog / "requirements.txt")
            break

    # 3.2 Demo (Streamlit app, 7 supporting modules, assets, models, screenshots, and Link_video_demo.txt)
    demo_dst = prog / "demo"
    demo_dst.mkdir(parents=True, exist_ok=True)
    copy_clean_tree(draft_dir / "demo" / "screenshots", demo_dst / "screenshots")

    # Demo app scripts & assets
    for demo_file in [
        "app.py",
        "analysis_pipeline.py",
        "evaluation_artifacts.py",
        "history_store.py",
        "inference.py",
        "input_formatting.py",
        "pipeline_details.py",
        "sample_import.py",
        "requirements-demo.txt",
    ]:
        src_demo_file = draft_dir / "demo" / demo_file
        if src_demo_file.exists():
            shutil.copy2(src_demo_file, demo_dst / demo_file)

    if (draft_dir / "demo" / "assets").exists():
        copy_clean_tree(draft_dir / "demo" / "assets", demo_dst / "assets")

    # Demo model weights for direct inference
    models_dst = demo_dst / "models"
    models_dst.mkdir(parents=True, exist_ok=True)
    for m in ["xgb_smote.json", "scaler.pkl"]:
        src_m = draft_dir / "models" / m
        if src_m.exists():
            shutil.copy2(src_m, models_dst / m)

    link_file = demo_dst / "Link_video_demo.txt"
    if Path("Chuong_trinh/demo/Link_video_demo.txt") in preserved:
        link_file.write_bytes(preserved[Path("Chuong_trinh/demo/Link_video_demo.txt")])
    elif Path("Chuong_trinh/demo/LINK_VIDEO_DEMO.txt") in preserved:
        link_file.write_bytes(preserved[Path("Chuong_trinh/demo/LINK_VIDEO_DEMO.txt")])
    else:
        link_content = (
            "LIÊN KẾT VIDEO CLIP DEMO HỆ THỐNG PHÁT HIỆN GIAO DỊCH GIAN LẬN (FRAUD SHIELD)\n"
            "NHÓM 9 — MÔN TRÍ TUỆ NHÂN TẠO (CS106) — UIT\n\n"
            "- Video Clip: Demo ứng dụng Streamlit Fraud Shield (Phạm Thành Trung trình bày)\n"
            "- Thời lượng: 1 phút 37 giây\n"
            "- Độ phân giải: 1920x1080 (Full HD / 30fps)\n"
            "- Định dạng: MP4 (H.264 / AAC Stereo)\n\n"
            "ĐƯỜNG DẪN VIDEO DEMO CHÍNH THỨC (TRUY CẬP TRỰC TIẾP):\n"
            "https://aceteam-uit.vercel.app/l/70vGyu\n\n"
            "LƯU Ý:\n"
            "Ảnh minh họa và liên kết trực tiếp tới video này cũng đã được tích hợp trên slide trình chiếu:\n"
            "`Bao_cao/[Nhom9]_Slide_FraudDetection.pdf` (Trang 20 - Demo trực tiếp).\n"
            "Quý Thầy/Cô có thể truy cập xem video qua liên kết trực tiếp ở trên.\n"
        )
        link_file.write_text(link_content, encoding="utf-8")

    # 3.3 Code (src, notebooks, data/processed, reports)
    code_dst = prog / "code"
    code_dst.mkdir(parents=True, exist_ok=True)

    # Core modular packages only (omit dead redundant files)
    src_dst = code_dst / "src"
    src_dst.mkdir(parents=True, exist_ok=True)
    if (draft_dir / "src" / "__init__.py").exists():
        shutil.copy2(draft_dir / "src" / "__init__.py", src_dst / "__init__.py")
    for mod in ["preprocessing", "models", "evaluation", "utils"]:
        src_mod = draft_dir / "src" / mod
        if src_mod.exists():
            copy_clean_tree(src_mod, src_dst / mod, skip_names={"plot_feature_importance.py"})

    # Update src/evaluation/__init__.py to not expose deleted plot_feature_importance
    eval_init = src_dst / "evaluation" / "__init__.py"
    if eval_init.exists():
        lines = eval_init.read_text(encoding="utf-8").splitlines()
        filtered = [
            line for line in lines
            if "plot_feature_importance" not in line
        ]
        eval_init.write_text("\n".join(filtered) + "\n", encoding="utf-8")

    copy_clean_tree(draft_dir / "notebooks", code_dst / "notebooks")
    copy_clean_tree(draft_dir / "data" / "processed", code_dst / "data" / "processed", skip_names={"README.md"})

    # Reports inside code (predictions .pkl, model comparison, summary txt, figures)
    reports_dst = code_dst / "reports"
    reports_dst.mkdir(parents=True, exist_ok=True)
    for f in [
        "rf_predictions.pkl",
        "xgb_predictions.pkl",
        "autoencoder_predictions.pkl",
        "model_comparison.csv",
        "autoencoder_summary.txt",
        "rf_smote_summary.txt",
        "xgb_smote_summary.txt",
    ]:
        src_f = draft_dir / "reports" / f
        if src_f.exists():
            shutil.copy2(src_f, reports_dst / f)

    if (draft_dir / "reports" / "figures").exists():
        copy_clean_tree(draft_dir / "reports" / "figures", reports_dst / "figures")

    # Clean any accidental caches or unwanted files
    for root, dirs, files in os.walk(bundle_dir, topdown=True):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            if f in EXCLUDE_FILES or f.startswith("._") or f.startswith("~$") or f.endswith(tuple(EXCLUDE_EXTS)):
                (Path(root) / f).unlink(missing_ok=True)


def list_bundle_files(bundle_dir: Path) -> list[Path]:
    """Get all clean files inside bundle."""
    files = []
    for root, _, fnames in os.walk(bundle_dir):
        for f in fnames:
            if not f.startswith("~$") and f not in EXCLUDE_FILES and not f.endswith(tuple(EXCLUDE_EXTS)):
                files.append(Path(root) / f)
    return sorted(files)


def main():
    parser = argparse.ArgumentParser(description="UIT CS106 Final Submission Packager — Nhom 9")
    base_default = Path(__file__).resolve().parent.parent.parent.parent
    parser.add_argument("--project", "-p", default=str(base_default), help="Project directory")
    parser.add_argument("--output", "-o", default=str(base_default / "submit"), help="Output directory")
    parser.add_argument("--zip", action="store_true", help="Also generate .zip archive (default: False)")
    parser.add_argument("--dry-run", action="store_true", help="Preview files only without changing submit/")
    args = parser.parse_args()

    final_dir = Path(args.project).resolve()
    submit_dir = Path(args.output).resolve()
    folder_name = "CS106_F31_CN2 - Nhom 9"
    bundle_dir = submit_dir / folder_name

    print("\n=======================================================")
    print("[*] UIT CS106 Final Submission Packager — Nhom 9")
    print(f"[*] Target Directory: {bundle_dir}")
    print("=======================================================\n")

    if args.dry_run:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_bundle = Path(tmp_dir) / folder_name
            assemble_submission(final_dir, tmp_bundle)
            files = list_bundle_files(tmp_bundle)
            total_mb = round(sum(f.stat().st_size for f in files) / (1024 * 1024), 2)
            print(f"[!] DRY RUN MODE — Successfully simulated {len(files)} deliverables ({total_mb} MB):\n")
            for f in files:
                print(f"  - {f.relative_to(tmp_bundle)} ({round(f.stat().st_size / 1024, 1)} KB)")
        return

    assemble_submission(final_dir, bundle_dir)
    files = list_bundle_files(bundle_dir)
    total_mb = round(sum(f.stat().st_size for f in files) / (1024 * 1024), 2)

    print(f"[✓] Successfully assembled {len(files)} clean deliverables ({total_mb} MB total uncompressed)\n")



    if args.zip:
        zip_path = submit_dir / f"{folder_name}.zip"
        print(f"[*] Creating ZIP: {zip_path.name}...")
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                zf.write(f, Path(folder_name) / f.relative_to(bundle_dir))
        sha = calculate_sha256(zip_path)
        print(f"[✓] ZIP created: {zip_path} ({round(zip_path.stat().st_size / (1024*1024), 2)} MB, SHA256: {sha})")
    else:
        print("[i] Skipping ZIP creation as requested. You can compress the directory manually.")


if __name__ == "__main__":
    main()
