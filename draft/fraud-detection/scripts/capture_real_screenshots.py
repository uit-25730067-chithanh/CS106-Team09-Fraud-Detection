#!/usr/bin/env python3
"""Capture 6 authentic, crisp screenshots from the Streamlit demo application."""

from pathlib import Path
import time
from playwright.sync_api import sync_playwright

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
APP_URL = "http://localhost:8501"

BASE_DIR = Path(__file__).resolve().parents[2]
TARGET_DIRS = [
    BASE_DIR / "draft/fraud-detection/demo/screenshots",
    BASE_DIR / "submit/CS106_F31_CN2 - Nhom 9/Chuong_trinh/demo/screenshots",
]

for d in TARGET_DIRS:
    d.mkdir(parents=True, exist_ok=True)


def save_screenshot(page, filename: str):
    """Save screenshot to both target directories."""
    for d in TARGET_DIRS:
        target_path = d / filename
        page.screenshot(path=str(target_path))
        print(f"[✓] Saved {filename} -> {target_path} ({target_path.stat().st_size / 1024:.1f} KB)")


def apply_sample_preset(page, option_text: str):
    """Open sample picker dialog, select preset, and click Choose Sample."""
    page.locator('button:has-text("Dữ liệu mẫu")').click()
    page.wait_for_timeout(1000)

    dialog = page.locator('[role="dialog"]')
    dialog.locator('[data-testid="stSelectbox"]').click()
    page.wait_for_timeout(800)

    page.locator(f'[role="option"]:has-text("{option_text}")').click()
    page.wait_for_timeout(800)

    dialog.locator('button:has-text("Chọn mẫu")').click()
    page.wait_for_timeout(1500)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True,
        )
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1.25,
        )
        page = context.new_page()

        print("[*] Navigating to Streamlit app...")
        page.goto(APP_URL)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(3000)

        # Set harmonious zoom
        page.evaluate("document.body.style.zoom = '0.96'")
        page.wait_for_timeout(1000)

        # 1. Dark Dashboard Overview
        print("[*] Capturing 1/6: dashboard-dark.png...")
        save_screenshot(page, "dashboard-dark.png")

        # 2. Light Dashboard Overview
        print("[*] Capturing 2/6: dashboard-light.png...")
        page.locator('button:has-text("Giao diện")').click()
        page.wait_for_timeout(800)
        page.locator('button.theme-option[data-theme="Light"]').last.click()
        page.wait_for_timeout(1500)
        page.keyboard.press("Escape")
        page.wait_for_timeout(1000)
        save_screenshot(page, "dashboard-light.png")

        # Switch back to Dark theme
        page.locator('button:has-text("Giao diện")').click()
        page.wait_for_timeout(800)
        page.locator('button.theme-option[data-theme="Dark"]').last.click()
        page.wait_for_timeout(1500)
        page.keyboard.press("Escape")
        page.wait_for_timeout(1000)

        # 3. Model Performance View
        print("[*] Capturing 3/6: model-performance.png...")
        page.locator('button:has-text("Hiệu năng mô hình")').click()
        page.wait_for_timeout(3000)
        page.wait_for_load_state("networkidle")
        save_screenshot(page, "model-performance.png")

        # Return to prediction view
        page.locator('button:has-text("Phân tích giao dịch")').first.click()
        page.wait_for_timeout(2000)

        # 4. Case 1: Hợp lệ — dòng tiền cân đối (Legitimate)
        print("[*] Capturing 4/6: prediction-legitimate.png (Case 1: Safe)...")
        apply_sample_preset(page, "Hợp lệ — dòng tiền cân đối")
        page.locator('button:has-text("Phân tích giao dịch")').last.click()
        page.wait_for_timeout(3000)
        page.wait_for_load_state("networkidle")
        page.evaluate("""() => {
            const resultPanel = document.querySelector('.st-key-result_panel');
            if (resultPanel) {
                resultPanel.scrollIntoView({ block: 'start', behavior: 'instant' });
                const main = document.querySelector('section.stMain');
                if (main) main.scrollTop -= 24;
            }
        }""")
        page.wait_for_timeout(1000)
        save_screenshot(page, "prediction-legitimate.png")

        # 5. Case 2: Cần lưu ý — chưa vượt ngưỡng (Watchlist / Warning)
        print("[*] Capturing 5/6: prediction-warning.png (Case 2: Watchlist)...")
        apply_sample_preset(page, "Cần lưu ý — chưa vượt ngưỡng")
        page.locator('button:has-text("Phân tích giao dịch")').last.click()
        page.wait_for_timeout(3000)
        page.wait_for_load_state("networkidle")
        page.evaluate("""() => {
            const resultPanel = document.querySelector('.st-key-result_panel');
            if (resultPanel) {
                resultPanel.scrollIntoView({ block: 'start', behavior: 'instant' });
                const main = document.querySelector('section.stMain');
                if (main) main.scrollTop -= 24;
            }
        }""")
        page.wait_for_timeout(1000)
        save_screenshot(page, "prediction-warning.png")

        # 6. Case 3: Nghi vấn gian lận — vượt ngưỡng (Fraud)
        print("[*] Capturing 6/6: prediction-fraud.png (Case 3: Fraud)...")
        apply_sample_preset(page, "Nghi vấn gian lận — vượt ngưỡng")
        page.locator('button:has-text("Phân tích giao dịch")').last.click()
        page.wait_for_timeout(3000)
        page.wait_for_load_state("networkidle")
        page.evaluate("""() => {
            const resultPanel = document.querySelector('.st-key-result_panel');
            if (resultPanel) {
                resultPanel.scrollIntoView({ block: 'start', behavior: 'instant' });
                const main = document.querySelector('section.stMain');
                if (main) main.scrollTop -= 24;
            }
        }""")
        page.wait_for_timeout(1000)
        save_screenshot(page, "prediction-fraud.png")

        browser.close()
        print("\n[✓] All 6 authentic screenshots captured successfully!")


if __name__ == "__main__":
    main()
