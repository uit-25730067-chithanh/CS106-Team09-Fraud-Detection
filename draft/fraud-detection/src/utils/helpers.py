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
