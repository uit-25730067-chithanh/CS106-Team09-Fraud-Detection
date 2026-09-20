"""
Copy generated screenshots into demo/screenshots/ directory with standard names.
"""
from pathlib import Path
from PIL import Image

brain_dir = Path(r"C:\Users\ASUS\.gemini\antigravity-ide\brain\0883334d-1c5d-4818-92df-4008641c9314")
dest_dir = Path("draft/fraud-detection/demo/screenshots")
dest_dir.mkdir(parents=True, exist_ok=True)

mapping = [
    ("dashboard_dark_1789646776230.jpg", "dashboard-dark.png"),
    ("prediction_fraud_1789646798535.jpg", "prediction-fraud.png"),
    ("prediction_legit_1789646816293.jpg", "prediction-legitimate.png"),
    ("model_performance_1789646835981.jpg", "model-performance.png"),
]

for src_name, dest_name in mapping:
    src_file = brain_dir / src_name
    if src_file.exists():
        im = Image.open(src_file)
        # save as png
        im.save(dest_dir / dest_name, "PNG")
        print(f"Copied {src_name} -> {dest_name}")
    else:
        print(f"Warning: {src_file} not found")

print("Done copying screenshots.")
