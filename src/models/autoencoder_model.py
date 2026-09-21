"""Autoencoder cho phát hiện gian lận theo hướng anomaly detection.

Ý tưởng: huấn luyện autoencoder CHỈ trên giao dịch bình thường (isFraud=0).
Khi gặp giao dịch gian lận, mạng tái tạo kém → reconstruction error (MSE) tăng
vọt → phân loại là fraud nếu error > ngưỡng.

⚠️  Lưu ý triển khai
--------------------
Phase-04 doc mô tả autoencoder bằng Keras/TensorFlow. Máy phát triển hiện tại
chạy **Python 3.14**, chưa có bản TensorFlow nào hỗ trợ (pip báo "No matching
distribution"). Vì vậy autoencoder ở đây được cài bằng
``sklearn.neural_network.MLPRegressor`` với cùng kiến trúc đối xứng
16 → 8 → 4 → 8 → 16 (bottleneck 4), tối ưu Adam + early stopping.
Model được lưu ``.pkl`` thay cho ``.h5``. API (build / train / reconstruction
error / threshold / predict / save) giữ nguyên như doc để phần sau không đổi.

Author: Mỷ Cẩm — Phase 04
"""
import os
import json
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor

from src.utils import RANDOM_STATE, get_project_root

import builtins as _bi


def _log(*args, **kwargs):
    """print() an toàn cả khi console không phải UTF-8 (Windows cp1252) và
    caller chưa gọi sys.stdout.reconfigure — tránh UnicodeEncodeError vì emoji."""
    try:
        _bi.print(*args, **kwargs)
    except UnicodeEncodeError:
        text = " ".join(str(a) for a in args).encode("ascii", "replace").decode()
        _bi.print(text, **kwargs)


MODELS_DIR = "models"
REPORTS_DIR = "reports"

# Kiến trúc encoder→decoder đối xứng (bottleneck = 4).
HIDDEN_LAYER_SIZES = (16, 8, 4, 8, 16)


def build_autoencoder(
    input_dim: int,
    epochs: int = 200,
    batch_size: int = 256,
    learning_rate: float = 1e-3,
    random_state: int = RANDOM_STATE,
) -> MLPRegressor:
    """Khởi tạo autoencoder (MLPRegressor) chưa huấn luyện.

    ``input_dim`` được giữ trong chữ ký cho khớp doc; MLPRegressor tự suy ra
    số chiều đầu vào/đầu ra khi ``fit``.
    """
    return MLPRegressor(
        hidden_layer_sizes=HIDDEN_LAYER_SIZES,
        activation="relu",
        solver="adam",
        alpha=1e-5,
        batch_size=batch_size,
        learning_rate_init=learning_rate,
        max_iter=epochs,
        shuffle=True,
        random_state=random_state,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=8,
        tol=1e-5,
        verbose=False,
    )


def train_autoencoder(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    epochs: int = 200,
    batch_size: int = 256,
    learning_rate: float = 1e-3,
    random_state: int = RANDOM_STATE,
    verbose: bool = True,
) -> tuple[MLPRegressor, dict]:
    """Huấn luyện autoencoder CHỈ trên giao dịch bình thường (isFraud=0).

    Returns
    -------
    (model, history) : tuple
        model   : MLPRegressor đã fit.
        history : dict gồm loss_curve, best_validation_score, n_iter, n_normal.
    """
    y_arr = np.asarray(y_train)
    X_df = X_train if isinstance(X_train, pd.DataFrame) else pd.DataFrame(X_train)
    X_normal = X_df[y_arr == 0].to_numpy(dtype=np.float32)

    if verbose:
        _log(f"🧠 Autoencoder train trên {len(X_normal):,} giao dịch bình thường "
              f"({X_normal.shape[1]} features)")

    model = build_autoencoder(
        input_dim=X_normal.shape[1],
        epochs=epochs,
        batch_size=batch_size,
        learning_rate=learning_rate,
        random_state=random_state,
    )
    model.fit(X_normal, X_normal)  # bài toán tái tạo: input = target

    history = {
        "loss_curve": [float(v) for v in getattr(model, "loss_curve_", [])],
        "validation_scores": [float(v) for v in getattr(model, "validation_scores_", [])],
        "best_validation_score": float(getattr(model, "best_validation_score_", np.nan)),
        "n_iter": int(getattr(model, "n_iter_", 0)),
        "n_normal_train": int(len(X_normal)),
    }
    if verbose:
        _log(f"✅ Dừng sau {history['n_iter']} epoch — "
              f"final train loss={history['loss_curve'][-1]:.6f}"
              if history["loss_curve"] else "✅ Huấn luyện xong")
    return model, history


def compute_reconstruction_error(
    model: MLPRegressor,
    X: np.ndarray | pd.DataFrame,
) -> np.ndarray:
    """MSE tái tạo trên từng dòng."""
    X_arr = X.to_numpy(dtype=np.float32) if isinstance(X, pd.DataFrame) else np.asarray(X, dtype=np.float32)
    reconstructed = model.predict(X_arr)
    return np.mean(np.square(X_arr - reconstructed), axis=1)


def find_threshold(
    recon_errors_normal: np.ndarray,
    percentile: float = 99.0,
) -> float:
    """Ngưỡng = percentile của reconstruction error trên tập bình thường.

    Dòng có error > ngưỡng được coi là fraud.
    """
    threshold = float(np.percentile(recon_errors_normal, percentile))
    _log(f"Threshold (p{percentile:.2f}): {threshold:.6f}")
    return threshold


def select_threshold_by_f1(
    model: MLPRegressor,
    X_val: pd.DataFrame,
    y_val: pd.Series,
    percentiles: tuple[float, ...] = (80.0, 85.0, 90.0, 95.0, 99.0, 99.5, 99.9),
    min_recall: float | None = None,
) -> tuple[float, pd.DataFrame]:
    """Quét nhiều percentile, chọn ngưỡng trên tập validation.

    Ngưỡng tại mỗi percentile được tính từ error của các mẫu BÌNH THƯỜNG trong
    ``X_val``; F1/precision/recall được đo trên toàn bộ ``X_val`` (normal + fraud).

    - Mặc định: chọn ngưỡng cho **F1 cao nhất**.
    - Nếu truyền ``min_recall``: trong các ngưỡng đạt recall ≥ ``min_recall``,
      chọn ngưỡng có F1 cao nhất (fallback về F1 tốt nhất nếu không ngưỡng nào đạt).

    Returns
    -------
    (best_threshold, table) : tuple
        table : DataFrame gồm percentile, threshold, precision, recall, f1.
    """
    from sklearn.metrics import f1_score, precision_score, recall_score

    y_arr = np.asarray(y_val).astype(int)
    errors = compute_reconstruction_error(model, X_val)
    errors_normal = errors[y_arr == 0]

    rows = []
    for p in percentiles:
        thr = float(np.percentile(errors_normal, p))
        y_pred = (errors > thr).astype(int)
        rows.append({
            "percentile": p,
            "threshold": thr,
            "precision": round(float(precision_score(y_arr, y_pred, zero_division=0)), 4),
            "recall": round(float(recall_score(y_arr, y_pred, zero_division=0)), 4),
            "f1": round(float(f1_score(y_arr, y_pred, zero_division=0)), 4),
        })

    table = pd.DataFrame(rows)

    pool = table
    if min_recall is not None:
        eligible = table[table["recall"] >= min_recall]
        if not eligible.empty:
            pool = eligible
        else:
            _log(f"⚠️  Không percentile nào đạt recall ≥ {min_recall} — fallback theo F1.")

    best_row = pool.loc[pool["f1"].idxmax()]
    best_threshold = float(best_row["threshold"])
    _log("\n📊 Quét ngưỡng (validation):")
    _log(table.to_string(index=False))
    _log(f"👉 Chọn p{best_row['percentile']:.1f} → threshold={best_threshold:.6f} "
          f"(F1={best_row['f1']}, recall={best_row['recall']})")
    return best_threshold, table


def predict_autoencoder(
    model: MLPRegressor,
    X_test: pd.DataFrame,
    threshold: float,
) -> dict:
    """Phân loại fraud (1) nếu reconstruction error > threshold."""
    errors = compute_reconstruction_error(model, X_test)
    y_pred = (errors > threshold).astype(int)
    return {
        "y_pred": y_pred,
        "y_prob": errors,               # dùng error như "điểm bất thường"
        "reconstruction_errors": errors,
    }


def save_autoencoder(
    model: MLPRegressor,
    threshold: float,
    name: str = "autoencoder",
    history: dict | None = None,
    models_dir: str | None = None,
) -> str:
    """Lưu model (``.pkl``) + threshold (``.txt``) + metadata (``.json``)."""
    if models_dir is None:
        models_dir = os.path.join(get_project_root(), MODELS_DIR)
    Path(models_dir).mkdir(parents=True, exist_ok=True)

    model_path = os.path.join(models_dir, f"{name}.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    with open(os.path.join(models_dir, f"{name}_threshold.txt"), "w", encoding="utf-8") as f:
        f.write(str(threshold))

    meta = {
        "implementation": "sklearn.neural_network.MLPRegressor",
        "reason": "TensorFlow/Keras không có bản cho Python 3.14 trên máy phát triển",
        "hidden_layer_sizes": list(HIDDEN_LAYER_SIZES),
        "threshold": threshold,
        "history": history or {},
    }
    with open(os.path.join(models_dir, f"{name}_meta.json"), "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    size_mb = os.path.getsize(model_path) / (1024 * 1024)
    _log(f"💾 Autoencoder saved: {model_path} ({size_mb:.3f} MB)")
    _log(f"   threshold → {models_dir}/{name}_threshold.txt = {threshold:.6f}")
    return model_path


def load_autoencoder(
    name: str = "autoencoder",
    models_dir: str | None = None,
) -> tuple[MLPRegressor, float]:
    """Load autoencoder + threshold."""
    if models_dir is None:
        models_dir = os.path.join(get_project_root(), MODELS_DIR)
    model_path = os.path.join(models_dir, f"{name}.pkl")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(models_dir, f"{name}_threshold.txt"), encoding="utf-8") as f:
        threshold = float(f.read().strip())
    _log(f"📂 Loaded autoencoder: {model_path} (threshold={threshold:.6f})")
    return model, threshold


def save_autoencoder_summary(
    metrics: dict,
    history: dict,
    threshold: float,
    threshold_table: pd.DataFrame | None = None,
    name: str = "autoencoder_summary",
    reports_dir: str | None = None,
) -> str:
    """Lưu tóm tắt autoencoder thành file text."""
    if reports_dir is None:
        reports_dir = os.path.join(get_project_root(), REPORTS_DIR)
    Path(reports_dir).mkdir(parents=True, exist_ok=True)
    path = os.path.join(reports_dir, f"{name}.txt")

    n_normal = history.get("n_normal_train")
    n_normal_str = f"{n_normal:,}" if isinstance(n_normal, int) else "N/A"

    lines = [
        "=" * 60,
        "  Autoencoder (Anomaly Detection) — Model Summary",
        f"  Model: {metrics.get('model_name', 'N/A')}",
        "=" * 60,
        "",
        "  Implementation: sklearn MLPRegressor (thay Keras — Python 3.14)",
        f"  Kiến trúc: {' → '.join(map(str, HIDDEN_LAYER_SIZES))} (bottleneck 4)",
        f"  Train chỉ trên normal: {n_normal_str} dòng",
        f"  Epoch đã chạy: {history.get('n_iter', 'N/A')}",
        f"  Threshold (reconstruction error): {threshold:.6f}",
        "",
        "--- Evaluation Metrics (Test Set) ---",
        f"  F1-Score:   {metrics['f1_score']}",
        f"  Precision:  {metrics['precision']}",
        f"  Recall:     {metrics['recall']}",
        f"  ROC-AUC:    {metrics['roc_auc']}",
        "",
        "--- Confusion Matrix ---",
        f"  {metrics.get('confusion_matrix', 'N/A')}",
        "",
        "--- Classification Report ---",
        metrics.get("classification_report", "N/A"),
    ]
    if threshold_table is not None:
        lines += ["", "--- Threshold sweep (validation) ---", threshold_table.to_string(index=False)]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    _log(f"📄 Summary saved: {path}")
    return path


__all__ = [
    "build_autoencoder",
    "train_autoencoder",
    "compute_reconstruction_error",
    "find_threshold",
    "select_threshold_by_f1",
    "predict_autoencoder",
    "save_autoencoder",
    "load_autoencoder",
    "save_autoencoder_summary",
    "HIDDEN_LAYER_SIZES",
]
