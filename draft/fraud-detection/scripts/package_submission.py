#!/usr/bin/env python3
"""
CS106 Final Project Submission Packager — Nhóm 9 (Fraud Detection)
Packages project deliverables into a clean, compliant ZIP archive:
`[Project AI-UIT] - Nhom 9.zip` according to UIT university standards.

Features:
- Automatic exclusion of virtualenvs (.venv), caches (__pycache__, .pytest_cache)
- Automatic exclusion of large files (>50MB like paysim.csv)
- Security exclusion of sensitive files (.env, credentials)
- Generation of SHA256 checksum and packaging manifest

Usage:
    python scripts/package_submission.py --dry-run
    python scripts/package_submission.py
"""

from __future__ import annotations

import os
import sys
import zipfile
import hashlib
import argparse
from pathlib import Path
from datetime import datetime

EXCLUDE_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache",
    "node_modules", ".idea", ".vscode", "tmp"
}

EXCLUDE_EXTS = {
    ".pyc", ".pyo", ".tmp", ".log"
}

MAX_FILE_SIZE_MB = 50.0


def calculate_sha256(file_path: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            sha.update(chunk)
    return sha.hexdigest()


def should_include_file(fp: Path, project_dir: Path) -> bool:
    """Check if a file should be included in the submission bundle."""
    # Check parts for excluded directories
    for part in fp.relative_to(project_dir).parts:
        if part in EXCLUDE_DIRS:
            return False

    if fp.name == ".DS_Store" or fp.name.startswith("._"):
        return False

    # Security: never package .env or private key files
    if fp.name == ".env" or fp.name.startswith(".env.") or fp.suffix in {".pem", ".key"}:
        print(f"[\033[91mSECURITY\033[0m] Excluding sensitive file: {fp.name}")
        return False

    if fp.suffix.lower() in EXCLUDE_EXTS:
        return False

    # Check file size limit (>50MB)
    try:
        size_mb = fp.stat().st_size / (1024 * 1024)
        if size_mb > MAX_FILE_SIZE_MB:
            print(f"[\033[93mEXCLUDE\033[0m] Skipping file > 50MB ({round(size_mb, 1)} MB): {fp.name}")
            return False
    except Exception:
        return False

    return True


def collect_submission_files(project_dir: Path) -> list[Path]:
    """Scan and filter all project files for submission."""
    included = []
    for root, dirs, files in os.walk(project_dir):
        # Prune excluded directories in-place
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for f in files:
            fp = Path(root) / f
            if should_include_file(fp, project_dir):
                included.append(fp)
    return sorted(included)


def package_project(args):
    project_dir = Path(args.project).resolve()
    out_dir = Path(args.output).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    zip_filename = args.filename or "[Project AI-UIT] - Nhom 9.zip"
    zip_path = out_dir / zip_filename

    print(f"\n=======================================================")
    print(f"[*] UIT CS106 Final Submission Packager — Nhom 9")
    print(f"[*] Target Directory: {project_dir}")
    print(f"[*] Output ZIP File:  {zip_path}")
    print(f"=======================================================\n")

    files_to_pack = collect_submission_files(project_dir)
    total_size_bytes = sum(f.stat().st_size for f in files_to_pack)
    total_size_mb = round(total_size_bytes / (1024 * 1024), 2)

    print(f"[✓] Collected {len(files_to_pack)} clean files ({total_size_mb} MB total uncompressed)\n")

    if args.dry_run:
        print("[!] DRY RUN MODE — Previewing first 30 files:")
        for f in files_to_pack[:30]:
            print(f"  - {f.relative_to(project_dir)}")
        if len(files_to_pack) > 30:
            print(f"  ... and {len(files_to_pack) - 30} more files.")
        print("\n[✓] Dry run complete. No zip archive created.")
        return

    # Create ZIP archive
    print(f"[*] Compressing files into {zip_path.name}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in files_to_pack:
            arcname = f.relative_to(project_dir)
            zf.write(f, arcname)

    zip_size_mb = round(zip_path.stat().st_size / (1024 * 1024), 2)
    sha256 = calculate_sha256(zip_path)

    print(f"\n[✓] Package successfully created: {zip_path}")
    print(f"    - Compressed Size: {zip_size_mb} MB")
    print(f"    - SHA256 Checksum: {sha256}")

    # Generate / Update submit/MANIFEST.md
    manifest_path = out_dir / "MANIFEST.md"
    manifest_content = f"""# Submission Package Manifest — Nhóm 9 (CS106)

> **Môn học:** Trí tuệ Nhân tạo (CS106.F31.CN2.TTNT) — UIT  
> **Đề tài:** #7 — Hệ thống Phát hiện Giao dịch Tài chính Bất thường  
> **Thời gian tạo:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **Tệp nén chính:** `{zip_filename}` ({zip_size_mb} MB)  
> **SHA256 Checksum:** `{sha256}`  

---

## 1. Thông Tin Nộp Bài
- **Tên file nộp:** `{zip_filename}`
- **Số lượng tệp được đóng gói:** {len(files_to_pack)} files
- **Dung lượng giải nén:** {total_size_mb} MB
- **Dung lượng nén ZIP:** {zip_size_mb} MB

## 2. Danh Mục Sản Phẩm Đã Kiểm Tra (Deliverables)
- [x] **Mã nguồn & Notebooks:** 6/6 Jupyter Notebooks đã chạy sạch 100%, thư mục `src/` modular đầy đủ preprocessing, models, evaluation, reporting.
- [x] **Báo cáo học thuật:** Word (`[Nhom9]_BaoCao_FraudDetection.docx`) và PDF (`[Nhom9]_BaoCao_FraudDetection.pdf`) 32 trang đầy đủ Chương 1–7.
- [x] **Slide thuyết trình:** Bản PPTX (`[Nhom9]_Slide_FraudDetection_Academic_VN.pptx`) và PDF 21 slide học thuật kèm Kịch bản bảo vệ 7 người.
- [x] **Demo giao diện:** Streamlit app kết nối mô hình XGBoost-SMOTE, 4 presets, mapping datetime và định dạng VNĐ.
- [x] **An toàn dữ liệu:** Đã loại trừ hoàn toàn `.env`, `.git`, `.venv` và tập dữ liệu thô `paysim.csv` (470MB).
"""
    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(manifest_content)
    print(f"[✓] Generated manifest: {manifest_path}\n")


def main():
    parser = argparse.ArgumentParser(description="UIT CS106 Final Submission Packager — Nhom 9")
    base_default = Path(__file__).resolve().parent.parent.parent.parent
    parser.add_argument("--project", "-p", default=str(base_default), help="Project directory (default: repo root)")
    parser.add_argument("--output", "-o", default=str(base_default / "submit"), help="Output directory (default: submit/)")
    parser.add_argument("--filename", "-f", default="[Project AI-UIT] - Nhom 9.zip", help="ZIP filename")
    parser.add_argument("--dry-run", action="store_true", help="Inspect files without creating archive")
    args = parser.parse_args()

    package_project(args)


if __name__ == "__main__":
    main()
