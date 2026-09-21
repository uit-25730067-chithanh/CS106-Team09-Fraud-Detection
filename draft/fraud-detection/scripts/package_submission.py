#!/usr/bin/env python3
"""
CS106 Final Project Submission Packager — Nhóm 9 (Financial Fraud Detection)
Prepares and verifies the canonical, clean submission directory:
`submit/[Project AI-UIT] - Nhom 9/` according to UIT university course requirements.

Cấu trúc thư mục chuẩn nộp bài (Chuẩn tối giản UIT, 0 file rác):
[Project AI-UIT] - Nhom 9/
├── Danh_sach_nhom.xlsx                     ← [1] Danh sách nhóm Excel (7 thành viên, MSSV, Lớp)
├── Bao_cao/                                ← [2] Báo cáo học thuật & Slide thuyết trình
│   ├── [Nhom9]_BaoCao_FraudDetection.pdf   ← Báo cáo học thuật chính thức (Chương 1–7, 31 trang)
│   ├── [Nhom9]_BaoCao_FraudDetection.docx  ← Báo cáo học thuật định dạng Word
│   ├── [Nhom9]_Slide_FraudDetection_Academic_VN.pdf  ← Slide thuyết trình dạng PDF
│   └── [Nhom9]_Slide_FraudDetection_Academic_VN.pptx ← Slide PowerPoint (ảnh minh họa & link Google Drive)
└── Chuong_trinh/                           ← [3] Chương trình & Thực nghiệm
    ├── HUONG_DAN_SU_DUNG.docx              ← Hướng dẫn sử dụng (bản Word chính thức)
    ├── requirements.txt                    ← Danh sách thư viện Python phụ thuộc
    ├── demo/                               ← Minh chứng sản phẩm Demo
    │   ├── LINK_VIDEO_DEMO.txt             ← Liên kết video clip demo Google Drive (quyền xem công khai)
    │   └── screenshots/                    ← 5 ảnh chụp màn hình UI sắc nét
    └── code/                               ← Toàn bộ mã nguồn giải thuật & thực nghiệm
        ├── src/                            ← 4 modules Python: preprocessing, models, evaluation, utils
        ├── notebooks/                      ← 6/6 Jupyter Notebooks thực nghiệm chạy sạch 100%
        ├── data/processed/                 ← 8 tệp .pkl tiền xử lý (chạy ngay không cần 500MB raw)
        └── reports/                        ← 3 tệp predictions .pkl (đầu vào cho Notebook 06 đối sánh)

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

    if bundle_dir.exists():
        shutil.rmtree(bundle_dir)
    bundle_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Assembling deliverables into: {bundle_dir}")

    # 1. Danh sách nhóm (Excel)
    candidates_excel = [
        draft_dir / "docs" / "Danh_sach_nhom.xlsx",
        draft_dir / "reports" / "Danh sách nhóm.xlsx",
        final_dir / "Danh_sach_nhom.xlsx",
    ]
    for c in candidates_excel:
        if c.exists():
            shutil.copy2(c, bundle_dir / "Danh_sach_nhom.xlsx")
            break

    # 2. Bao_cao (Official Word & PDF report, and official PPTX & PDF slide)
    bao_cao = bundle_dir / "Bao_cao"
    bao_cao.mkdir(parents=True, exist_ok=True)
    report_docx = draft_dir / "reports" / "[Nhom9]_BaoCao_FraudDetection.docx"
    report_pdf = draft_dir / "reports" / "[Nhom9]_BaoCao_FraudDetection.pdf"
    if report_docx.exists():
        shutil.copy2(report_docx, bao_cao / "[Nhom9]_BaoCao_FraudDetection.docx")
    if report_pdf.exists():
        shutil.copy2(report_pdf, bao_cao / "[Nhom9]_BaoCao_FraudDetection.pdf")

    pptx_slide = draft_dir / "slide" / "[Nhom9]_Slide_FraudDetection_Academic_VN.pptx"
    pdf_slide = draft_dir / "slide" / "[Nhom9]_Slide_FraudDetection_Academic_VN.pdf"
    if pptx_slide.exists():
        shutil.copy2(pptx_slide, bao_cao / "[Nhom9]_Slide_FraudDetection_Academic_VN.pptx")
    if pdf_slide.exists():
        shutil.copy2(pdf_slide, bao_cao / "[Nhom9]_Slide_FraudDetection_Academic_VN.pdf")

    # 3. Chuong_trinh
    prog = bundle_dir / "Chuong_trinh"
    prog.mkdir(parents=True, exist_ok=True)

    # 3.1 Single unified guide (DOCX) & requirements
    guide_candidates = [
        draft_dir / "docs" / "HUONG_DAN_SU_DUNG.docx",
        draft_dir / "docs" / "Huong_dan_su_dung.docx",
        final_dir / "HUONG_DAN_SU_DUNG.docx",
    ]
    for c in guide_candidates:
        if c and c.exists():
            shutil.copy2(c, prog / "HUONG_DAN_SU_DUNG.docx")
            break

    req_candidates = [
        draft_dir / "requirements.txt",
    ]
    for r in req_candidates:
        if r.exists():
            shutil.copy2(r, prog / "requirements.txt")
            break

    # 3.2 Demo (Strictly screenshots and video link)
    demo_dst = prog / "demo"
    demo_dst.mkdir(parents=True, exist_ok=True)
    copy_clean_tree(draft_dir / "demo" / "screenshots", demo_dst / "screenshots")

    # Prefer PDF link if available, fallback to TXT
    link_candidates = [
        draft_dir / "demo" / "clip" / "LINK_VIDEO_DEMO.pdf",
        draft_dir / "demo" / "clip" / "LINK_VIDEO_DEMO.txt",
    ]
    for lc in link_candidates:
        if lc.exists():
            shutil.copy2(lc, demo_dst / lc.name)
            break

    # 3.3 Code (src, notebooks, data/processed, reports)
    code_dst = prog / "code"
    code_dst.mkdir(parents=True, exist_ok=True)

    # Core modular packages only (omit internal reporting builders and scripts)
    src_dst = code_dst / "src"
    src_dst.mkdir(parents=True, exist_ok=True)
    if (draft_dir / "src" / "__init__.py").exists():
        shutil.copy2(draft_dir / "src" / "__init__.py", src_dst / "__init__.py")
    for mod in ["preprocessing", "models", "evaluation", "utils"]:
        src_mod = draft_dir / "src" / mod
        if src_mod.exists():
            copy_clean_tree(src_mod, src_dst / mod)

    copy_clean_tree(draft_dir / "notebooks", code_dst / "notebooks")
    copy_clean_tree(draft_dir / "data" / "processed", code_dst / "data" / "processed", skip_names={"README.md"})

    # Reports inside code (strictly prediction pickles needed as input for Notebook 06)
    reports_dst = code_dst / "reports"
    reports_dst.mkdir(parents=True, exist_ok=True)
    for f in ["rf_predictions.pkl", "xgb_predictions.pkl", "autoencoder_predictions.pkl"]:
        src_f = draft_dir / "reports" / f
        if src_f.exists():
            shutil.copy2(src_f, reports_dst / f)

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
    folder_name = "[Project AI-UIT] - Nhom 9"
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
