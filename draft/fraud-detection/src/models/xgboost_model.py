"""XGBoost model for fraud detection.

Huấn luyện, tinh chỉnh siêu tham số và đánh giá XGBoost Classifier trên
tập dữ liệu đã được cân bằng (SMOTE/ADASYN). API được giữ đồng nhất với
``random_forest_model`` để Phase 05 (Evaluation) tái sử dụng chung.

Author: Mỷ Cẩm — Phase 04
"""
import os
import pickle
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import RandomizedSearchCV
from xgboost import XGBClassifier

from src.utils import RANDOM_STATE, get_project_root

# Tái sử dụng các hàm đánh giá / lưu artifact dùng chung (không phụ thuộc mô hình).
from src.models.random_forest_model import (
    evaluate_model,
    get_feature_importance,
    save_predictions,
    save_feature_importance,
)

import builtins as _bi


def _log(*args, **kwargs):
    """print() an toàn cả khi console không phải UTF-8 (Windows cp1252) và
    caller chưa gọi sys.stdout.reconfigure — tránh UnicodeEncodeError vì emoji."""
    try:
        _bi.print(*args, **kwargs)
    except UnicodeEncodeError:
        text = " ".join(str(a) for a in args).encode("ascii", "replace").decode()
        _bi.print(text, **kwargs)

# ─── Default hyperparameter search space ─────────────────────────────────────
# Lưới nhẹ, phù hợp chạy trên CPU với ~230k dòng SMOTE.
PARAM_DIST = {
    "n_estimators": [100, 200, 300, 400],
    "max_depth": [4, 6, 8, 10],
    "learning_rate": [0.03, 0.05, 0.1, 0.2],
    "subsample": [0.7, 0.85, 1.0],
    "colsample_bytree": [0.7, 0.85, 1.0],
    "min_child_weight": [1, 3, 5],
    "gamma": [0, 0.1, 0.3],
}

# ─── Paths ────────────────────────────────────────────────────────────────────
MODELS_DIR = "models"
REPORTS_DIR = "reports"


def train_xgboost(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    tune: bool = True,
    random_state: int = RANDOM_STATE,
    n_iter: int = 20,
    cv: int = 3,
    scoring: str = "f1",
    verbose: int = 1,
    use_scale_pos_weight: bool = False,
) -> tuple[XGBClassifier, dict]:
    """Huấn luyện XGBoost với tùy chọn tinh chỉnh siêu tham số.

    Parameters
    ----------
    X_train, y_train
        Tập huấn luyện đã oversample (SMOTE/ADASYN).
    tune : bool
        True → RandomizedSearchCV; False → baseline config.
    n_iter, cv, scoring
        Cấu hình RandomizedSearchCV.
    use_scale_pos_weight : bool
        Mặc định ``False`` vì dữ liệu đã được cân bằng bằng SMOTE/ADASYN —
        bật thêm ``scale_pos_weight`` sẽ nhân đôi trọng số lớp thiểu số.
        Đặt ``True`` khi train trên dữ liệu gốc chưa cân bằng.

    Returns
    -------
    (model, info) : tuple
        model : XGBClassifier đã fit.
        info  : dict gồm best_params, best_cv_score, training_time_seconds, ...
    """
    start_time = time.time()

    if use_scale_pos_weight:
        n_neg = int((y_train == 0).sum())
        n_pos = int((y_train == 1).sum())
        scale_pos_weight = n_neg / max(n_pos, 1)
    else:
        scale_pos_weight = 1.0

    base_xgb = XGBClassifier(
        objective="binary:logistic",
        eval_metric="aucpr",          # aucpr ổn định hơn auc cho dữ liệu lệch lớp
        tree_method="hist",
        scale_pos_weight=scale_pos_weight,
        random_state=random_state,
        n_jobs=-1,
        verbosity=0,
    )

    if tune:
        _log(f"🔍 RandomizedSearchCV: n_iter={n_iter}, cv={cv}, scoring={scoring}")
        search = RandomizedSearchCV(
            estimator=base_xgb,
            param_distributions=PARAM_DIST,
            n_iter=n_iter,
            cv=cv,
            scoring=scoring,
            random_state=random_state,
            n_jobs=-1,
            verbose=verbose,
            return_train_score=True,
        )
        search.fit(X_train, y_train)

        model = search.best_estimator_
        elapsed = time.time() - start_time
        info = {
            "best_params": search.best_params_,
            "best_cv_score": round(float(search.best_score_), 4),
            "training_time_seconds": round(elapsed, 2),
            "n_iter": n_iter,
            "cv": cv,
            "scoring": scoring,
            "scale_pos_weight": round(scale_pos_weight, 4),
            "tuned": True,
        }
        _log(f"✅ Best CV {scoring}: {info['best_cv_score']}")
        _log(f"⏱️ Training time: {elapsed:.1f}s")
        _log(f"📋 Best params: {info['best_params']}")
    else:
        _log("⚡ Training baseline XGBoost (no tuning)...")
        model = XGBClassifier(
            n_estimators=300,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.85,
            colsample_bytree=0.85,
            objective="binary:logistic",
            eval_metric="aucpr",
            tree_method="hist",
            scale_pos_weight=scale_pos_weight,
            random_state=random_state,
            n_jobs=-1,
            verbosity=0,
        )
        model.fit(X_train, y_train)
        elapsed = time.time() - start_time
        info = {
            "best_params": model.get_params(),
            "training_time_seconds": round(elapsed, 2),
            "scale_pos_weight": round(scale_pos_weight, 4),
            "tuned": False,
        }
        _log(f"✅ Baseline trained in {elapsed:.1f}s")

    return model, info


def predict(
    model: XGBClassifier,
    X_test: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray]:
    """Dự đoán nhãn (0/1) và xác suất lớp fraud."""
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    return np.asarray(y_pred), np.asarray(y_prob)


def save_model(
    model: XGBClassifier,
    name: str,
    models_dir: str | None = None,
) -> str:
    """Lưu model đã train thành file ``.pkl`` (và ``.json`` chuẩn XGBoost)."""
    if models_dir is None:
        models_dir = os.path.join(get_project_root(), MODELS_DIR)

    Path(models_dir).mkdir(parents=True, exist_ok=True)
    path = os.path.join(models_dir, f"{name}.pkl")
    with open(path, "wb") as f:
        pickle.dump(model, f)

    # Bản .json native — portable giữa các phiên bản xgboost, tiện cho demo.
    try:
        model.save_model(os.path.join(models_dir, f"{name}.json"))
    except Exception as exc:  # pragma: no cover - chỉ log, không chặn
        _log(f"⚠️  Không lưu được bản .json: {exc}")

    size_mb = os.path.getsize(path) / (1024 * 1024)
    _log(f"💾 Model saved: {path} ({size_mb:.2f} MB)")
    if size_mb > 50:
        _log("⚠️  File > 50MB — nhớ giữ trong .gitignore")
    return path


def load_model(name: str, models_dir: str | None = None) -> XGBClassifier:
    """Load model từ file ``.pkl``."""
    if models_dir is None:
        models_dir = os.path.join(get_project_root(), MODELS_DIR)
    path = os.path.join(models_dir, f"{name}.pkl")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found: {path}")
    with open(path, "rb") as f:
        model = pickle.load(f)
    _log(f"📂 Loaded model: {path}")
    return model


def save_model_summary(
    metrics: dict,
    train_info: dict,
    name: str = "xgb_model_summary",
    reports_dir: str | None = None,
) -> str:
    """Lưu tóm tắt model (metrics + hyperparams) thành file text."""
    if reports_dir is None:
        reports_dir = os.path.join(get_project_root(), REPORTS_DIR)

    Path(reports_dir).mkdir(parents=True, exist_ok=True)
    path = os.path.join(reports_dir, f"{name}.txt")

    lines = [
        "=" * 60,
        "  XGBoost Model Summary",
        f"  Model: {metrics.get('model_name', 'N/A')}",
        "=" * 60,
        "",
        "--- Evaluation Metrics (Test Set) ---",
        f"  F1-Score:   {metrics['f1_score']}",
        f"  Precision:  {metrics['precision']}",
        f"  Recall:     {metrics['recall']}",
        f"  ROC-AUC:    {metrics['roc_auc']}",
        "",
        "--- Training Info ---",
        f"  Tuned:              {train_info.get('tuned', 'N/A')}",
        f"  Training Time:      {train_info.get('training_time_seconds', 'N/A')}s",
        f"  Best CV Score:      {train_info.get('best_cv_score', 'N/A')}",
        f"  scale_pos_weight:   {train_info.get('scale_pos_weight', 'N/A')}",
        "",
        "--- Best Hyperparameters ---",
    ]
    for k, v in train_info.get("best_params", {}).items():
        lines.append(f"  {k}: {v}")

    lines.extend([
        "",
        "--- Confusion Matrix ---",
        f"  {metrics.get('confusion_matrix', 'N/A')}",
        "",
        "--- Classification Report ---",
        metrics.get("classification_report", "N/A"),
    ])

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    _log(f"📄 Summary saved: {path}")
    return path


__all__ = [
    "train_xgboost",
    "predict",
    "evaluate_model",
    "get_feature_importance",
    "save_model",
    "load_model",
    "save_predictions",
    "save_feature_importance",
    "save_model_summary",
    "PARAM_DIST",
]
