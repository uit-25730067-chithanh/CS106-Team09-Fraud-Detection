"""Script tiện ích: Đọc lại các tệp dự đoán bằng CompatUnpickler và ghi đè lại

nhằm đảm bảo tương thích 100% với cả NumPy 1.x lẫn NumPy 2.x khi dùng pickle.load chuẩn.
"""

from __future__ import annotations

import os
import pickle
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.utils import load_pickle_compat


def resave_artifact(file_path: str) -> None:
    print(f"Đang xử lý: {file_path}")
    data = load_pickle_compat(file_path)
    with open(file_path, "wb") as f:
        pickle.dump(data, f, protocol=4)
    print(f"  -> Đã lưu lại thành công: {file_path}")


def main() -> None:
    reports_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports"
    )
    targets = [
        os.path.join(reports_dir, "xgb_predictions.pkl"),
        os.path.join(reports_dir, "autoencoder_predictions.pkl"),
    ]

    for target in targets:
        if os.path.exists(target):
            resave_artifact(target)
        else:
            print(f"Bỏ qua (không tồn tại): {target}")


if __name__ == "__main__":
    main()
