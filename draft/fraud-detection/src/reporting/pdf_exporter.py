"""
High-Fidelity PDF Exporter for UIT Academic Documents.
Primary method: macOS AppleScript controlling Microsoft Word (100% fidelity, preserves links).
Fallback method: Headless LibreOffice (`soffice --headless --convert-to pdf`).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys


def export_docx_to_pdf(docx_path: str, pdf_path: str) -> bool:
    """
    Export DOCX to PDF with maximum fidelity.
    First tries macOS Microsoft Word via AppleScript, falls back to LibreOffice.
    """
    abs_docx = os.path.abspath(docx_path)
    abs_pdf = os.path.abspath(pdf_path)
    os.makedirs(os.path.dirname(abs_pdf), exist_ok=True)

    if not os.path.exists(abs_docx):
        print(f"[!] Error: Source DOCX file not found: {abs_docx}")
        return False

    # 1. Try macOS Microsoft Word via AppleScript
    if sys.platform == "darwin":
        tmp_in = "/tmp/uit_report_in.docx"
        tmp_out = "/tmp/uit_report_out.pdf"
        try:
            shutil.copyfile(abs_docx, tmp_in)
            if os.path.exists(tmp_out):
                os.remove(tmp_out)

            script = f'''
            set inPath to (POSIX file "{tmp_in}") as text
            set outPath to (POSIX file "{tmp_out}") as text
            tell application "Microsoft Word"
                open file inPath
                set docRef to active document
                save as docRef file name outPath file format format PDF
                close docRef saving no
            end tell
            '''
            res = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, timeout=60)
            if res.returncode == 0 and os.path.exists(tmp_out):
                shutil.move(tmp_out, abs_pdf)
                print(f"[✓] Successfully exported official PDF via Microsoft Word: {abs_pdf}")
                return True
            else:
                print(f"[!] AppleScript Word export failed ({res.stderr.strip()}), trying fallback...")
        except Exception as e:
            print(f"[!] AppleScript execution error: {e}, trying fallback...")

    # 2. Fallback to LibreOffice
    soffice_bin = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice_bin and sys.platform == "darwin":
        mac_soffice = "/Applications/LibreOffice.app/Contents/MacOS/soffice"
        if os.path.exists(mac_soffice):
            soffice_bin = mac_soffice

    if soffice_bin:
        try:
            out_dir = os.path.dirname(abs_pdf)
            cmd = [soffice_bin, "--headless", "--convert-to", "pdf", abs_docx, "--outdir", out_dir]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            expected_pdf = os.path.splitext(abs_docx)[0] + ".pdf"
            if os.path.exists(expected_pdf):
                if expected_pdf != abs_pdf:
                    shutil.move(expected_pdf, abs_pdf)
                print(f"[✓] Successfully exported PDF via LibreOffice: {abs_pdf}")
                return True
            else:
                print(f"[!] LibreOffice failed to generate PDF: {res.stderr.strip()}")
        except Exception as e:
            print(f"[!] LibreOffice execution error: {e}")

    # 3. Fallback to Apple Pages — có sẵn trên macOS khi máy không cài Word
    #    hay LibreOffice. Pages phải đang chạy thì AppleScript mới gọi được,
    #    nếu không osascript trả lỗi -600 "Application isn't running".
    if sys.platform == "darwin" and _pages_bundle_installed():
        try:
            subprocess.run(["open", "-ga", "-b", "com.apple.Pages"], timeout=30)
            script = f'''
            tell application id "com.apple.Pages"
                launch
                delay 2
                set theDoc to open (POSIX file "{abs_docx}" as alias)
                delay 2
                export theDoc to (POSIX file "{abs_pdf}") as PDF
                delay 1
                close theDoc saving no
            end tell
            '''
            res = subprocess.run(
                ["osascript", "-e", script], capture_output=True, text=True, timeout=180
            )
            if res.returncode == 0 and os.path.exists(abs_pdf):
                print(f"[✓] Successfully exported PDF via Apple Pages: {abs_pdf}")
                return True
            print(f"[!] Apple Pages export failed: {res.stderr.strip()}")
        except Exception as e:
            print(f"[!] Apple Pages execution error: {e}")

    print("[!] Warning: Could not export PDF. Please install Microsoft Word, LibreOffice or Pages.")
    return False


def _pages_bundle_installed() -> bool:
    """Pages có thể được cài dưới tên bundle khác, ví dụ Pages Creator Studio."""

    res = subprocess.run(
        ["osascript", "-e", 'POSIX path of (path to application id "com.apple.Pages")'],
        capture_output=True,
        text=True,
    )
    return res.returncode == 0 and bool(res.stdout.strip())


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        success = export_docx_to_pdf(sys.argv[1], sys.argv[2])
        sys.exit(0 if success else 1)
    else:
        print("Usage: python pdf_exporter.py <input.docx> <output.pdf>")
