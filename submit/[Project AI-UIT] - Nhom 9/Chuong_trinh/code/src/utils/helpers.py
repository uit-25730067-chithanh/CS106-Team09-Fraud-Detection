"""Shared constants and utility helpers for the fraud detection project."""
import numpy as np
import random

# ─── Constants ────────────────────────────────────────────────────────────────
RANDOM_STATE = 42
TEST_SIZE = 0.2
DATA_RAW_PATH = "data/raw/paysim.csv"
DATA_PROCESSED_DIR = "data/processed"

# ─── Reproducibility ──────────────────────────────────────────────────────────

def set_seeds(seed: int = RANDOM_STATE) -> None:
    """Set all random seeds for reproducibility."""
    np.random.seed(seed)
    random.seed(seed)

# ─── Path helpers ─────────────────────────────────────────────────────────────

def get_project_root() -> str:
    """Return the project root directory (fraud-detection/)."""
    import os
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ─── Pickle Compatibility ────────────────────────────────────────────────────

import pickle
from typing import Any, BinaryIO


class CompatUnpickler(pickle.Unpickler):
    """Cầu nối unpickle tương thích giữa NumPy 2.x (nguồn lưu) và NumPy 1.x (môi trường đọc)."""

    def find_class(self, module: str, name: str):
        if module.startswith("numpy._core"):
            module = module.replace("numpy._core", "numpy.core")
        return super().find_class(module, name)


def load_pickle_compat(file_or_path: str | BinaryIO) -> Any:
    """Nạp tệp pickle an toàn, tự động tương thích ngược giữa các phiên bản NumPy."""
    if hasattr(file_or_path, "read"):
        return CompatUnpickler(file_or_path).load()
    with open(file_or_path, "rb") as f:
        return CompatUnpickler(f).load()
