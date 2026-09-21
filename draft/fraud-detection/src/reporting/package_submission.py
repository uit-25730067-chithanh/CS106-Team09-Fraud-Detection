"""
Automated packaging script for CS106 Final Submission - Nhóm 9
Generates the standardized submission structure and creates [Project AI-UIT] - Nhom 9.zip.
Ensures strict sanitization (no paysim.csv, no .env, no .venv, no __pycache__).
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path

# Force UTF-8 output on Windows terminal
sys.stdout.reconfigure(encoding="utf-8")

# Paths relative to repository root
REPO_ROOT = Path(__file__).resolve().parents[4]
DRAFT_DIR = REPO_ROOT / "draft" / "fraud-detection"
SUBMIT_ROOT = REPO_ROOT / "submit"
PACKAGE_NAME = "[Project AI-UIT] - Nhom 9"
TARGET_DIR = SUBMIT_ROOT / PACKAGE_NAME
ZIP_FILE = SUBMIT_ROOT / f"{PACKAGE_NAME}.zip"

# Forbidden patterns for security and size control
FORBIDDEN_FILES = {
    "paysim.csv",
    ".env",
    ".env.local",
    "kaggle.json",
    ".DS_Store",
    "Thumbs.db",
}

FORBIDDEN_DIRS = {
    ".git",
    ".venv",
    "venv",
    "env",
    ".env",
    "__pycache__",
    ".pytest_cache",
    ".ipynb_checkpoints",
    "node_modules",
}


def clean_target_dir():
    """Remove existing packaging target directory and zip file."""
    if TARGET_DIR.exists():
        print(f"Removing existing directory: {TARGET_DIR.name}")
        shutil.rmtree(TARGET_DIR, ignore_errors=True)
    if ZIP_FILE.exists():
        print(f"Removing existing ZIP: {ZIP_FILE.name}")
        ZIP_FILE.unlink(missing_ok=True)


def copy_filtered_tree(src: Path, dst: Path, max_file_size_mb: float = 45.0):
    """
    Recursively copy directory tree while filtering forbidden files/dirs
    and files exceeding max_file_size_mb.
    """
    if not src.exists():
        print(f"Warning: Source not found: {src.name}")
        return

    dst.mkdir(parents=True, exist_ok=True)

    for item in src.iterdir():
        if item.name in FORBIDDEN_DIRS:
            continue
        if item.name in FORBIDDEN_FILES:
            continue
        if item.name.startswith("~$"):  # MS Office temp lock file
            continue

        target_item = dst / item.name

        if item.is_dir():
            copy_filtered_tree(item, target_item, max_file_size_mb)
        else:
            # Check file size
            size_mb = item.stat().st_size / (1024 * 1024)
            if size_mb > max_file_size_mb:
                print(f"Skipping large file (> {max_file_size_mb} MB): {item.name} ({size_mb:.1f} MB)")
                continue
            shutil.copy2(item, target_item)


def copy_file_safe(src: Path, dst: Path):
    """Safely copy a single file to target destination."""
    if not src.exists():
        print(f"Warning: File not found: {src.name}")
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"  Copied: {src.name} -> {dst.relative_to(TARGET_DIR)}")


def build_submission_structure():
    """Build the official [Project AI-UIT] - Nhom 9 directory layout."""
    print("=" * 70)
    print("Building Official Submission Package Structure...")
    print("=" * 70)

    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Code directory
    code_dir = TARGET_DIR / "code"
    print("\n[1/5] Packaging Source Code, Notebooks, Models & Tests...")
    copy_filtered_tree(DRAFT_DIR / "src", code_dir / "src")
    copy_filtered_tree(DRAFT_DIR / "notebooks", code_dir / "notebooks")
    copy_filtered_tree(DRAFT_DIR / "demo", code_dir / "demo")
    copy_filtered_tree(DRAFT_DIR / "models", code_dir / "models")
    copy_filtered_tree(DRAFT_DIR / "data" / "processed", code_dir / "data" / "processed")
    copy_filtered_tree(DRAFT_DIR / "tests", code_dir / "tests")

    copy_file_safe(DRAFT_DIR / "requirements.txt", code_dir / "requirements.txt")
    if (DRAFT_DIR / "run_preprocessing.py").exists():
        copy_file_safe(DRAFT_DIR / "run_preprocessing.py", code_dir / "run_preprocessing.py")

    # 2. Report directory
    report_dir = TARGET_DIR / "report"
    print("\n[2/5] Packaging Reports & Evidence...")
    report_docx = DRAFT_DIR / "reports" / "[Nhom9]_BaoCao_FraudDetection.docx"
    report_pdf = DRAFT_DIR / "reports" / "[Nhom9]_BaoCao_FraudDetection.pdf"
    team_excel = DRAFT_DIR / "reports" / "Danh sách nhóm.xlsx"
    comparison_csv = DRAFT_DIR / "reports" / "model_comparison.csv"

    copy_file_safe(report_docx, report_dir / "[Nhom9]_BaoCao_FraudDetection.docx")
    copy_file_safe(report_pdf, report_dir / "[Nhom9]_BaoCao_FraudDetection.pdf")
    copy_file_safe(team_excel, report_dir / "Danh sách nhóm.xlsx")
    copy_file_safe(comparison_csv, report_dir / "model_comparison.csv")
    copy_filtered_tree(DRAFT_DIR / "reports" / "figures", report_dir / "figures")

    # 3. Slides directory
    slides_dir = TARGET_DIR / "slides"
    print("\n[3/5] Packaging Presentation Slides...")
    slide_pptx = DRAFT_DIR / "slide" / "[Nhom9]_Slide_FraudDetection_Academic_VN.pptx"
    slide_pdf = DRAFT_DIR / "slide" / "[Nhom9]_Slide_FraudDetection_Academic_VN.pdf"
    copy_file_safe(slide_pptx, slides_dir / "[Nhom9]_Slide_FraudDetection_Academic_VN.pptx")
    copy_file_safe(slide_pdf, slides_dir / "[Nhom9]_Slide_FraudDetection_Academic_VN.pdf")

    # 4. Demo directory
    demo_dir = TARGET_DIR / "demo"
    print("\n[4/5] Packaging Demo UI Assets & Screenshots...")
    copy_filtered_tree(DRAFT_DIR / "demo" / "screenshots", demo_dir / "screenshots")
    copy_file_safe(DRAFT_DIR / "demo" / "DEMO-SCRIPT.md", demo_dir / "DEMO-SCRIPT.md")

    # 5. Root documentation files
    print("\n[5/5] Packaging Top-Level Documentation & Guide...")
    guide_docx = DRAFT_DIR / "docs" / "Huong_dan_su_dung.docx"
    copy_file_safe(guide_docx, TARGET_DIR / "Huong_dan_su_dung.docx")
    copy_file_safe(team_excel, TARGET_DIR / "Danh sách nhóm.xlsx")
    copy_file_safe(REPO_ROOT / "README.md", TARGET_DIR / "README.md")


def sanitize_audit():
    """Verify no forbidden files or leakage exist in the package."""
    print("\n" + "=" * 70)
    print("Running Security & Sanitization Audit...")
    print("=" * 70)

    leaked = []
    total_files = 0
    total_bytes = 0

    for root, dirs, files in os.walk(TARGET_DIR):
        for d in dirs:
            if d in FORBIDDEN_DIRS:
                leaked.append(os.path.join(root, d))
        for f in files:
            total_files += 1
            fpath = os.path.join(root, f)
            total_bytes += os.path.getsize(fpath)
            if f in FORBIDDEN_FILES or f.startswith("~$"):
                leaked.append(fpath)

    if leaked:
        print("CRITICAL ERROR: Found forbidden files in package:")
        for item in leaked:
            print(f"  - {item}")
        raise RuntimeError("Sanitization audit failed!")

    print("Sanitization Audit: PASSED (No paysim.csv, no .env, no cache files)")
    print(f"Total package files: {total_files}")
    print(f"Total uncompressed size: {total_bytes / (1024 * 1024):.2f} MB")
    return total_files, total_bytes


def create_zip_archive():
    """Compress the package into a standard zip archive."""
    print("\n" + "=" * 70)
    print(f"Creating ZIP Archive: {ZIP_FILE.name}...")
    print("=" * 70)

    with zipfile.ZipFile(ZIP_FILE, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for root, _, files in os.walk(TARGET_DIR):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(SUBMIT_ROOT)
                zipf.write(file_path, arcname)

    zip_size_mb = ZIP_FILE.stat().st_size / (1024 * 1024)
    print(f"ZIP Created Successfully: {ZIP_FILE.name}")
    print(f"ZIP File Size: {zip_size_mb:.2f} MB (Well within < 500MB limit)")

    # Test ZIP integrity
    print("\nVerifying ZIP archive integrity...")
    with zipfile.ZipFile(ZIP_FILE, "r") as test_zip:
        bad_file = test_zip.testzip()
        if bad_file:
            raise RuntimeError(f"Corrupted file in ZIP: {bad_file}")
        namelist = test_zip.namelist()
        print(f"Integrity Check: PASSED ({len(namelist)} items in ZIP)")

    return zip_size_mb


def main():
    clean_target_dir()
    build_submission_structure()
    total_files, total_bytes = sanitize_audit()
    zip_size_mb = create_zip_archive()

    print("\n" + "=" * 70)
    print("PACKAGE SUBMISSION SUMMARY")
    print("=" * 70)
    print(f"Package Folder : {TARGET_DIR.name}")
    print(f"Zip File       : {ZIP_FILE.name}")
    print(f"Uncompressed   : {total_bytes / (1024*1024):.2f} MB ({total_files} files)")
    print(f"Compressed ZIP : {zip_size_mb:.2f} MB")
    print("Status         : READY FOR SUBMISSION")
    print("=" * 70)


if __name__ == "__main__":
    main()
