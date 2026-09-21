"""Random Forest model for fraud detection.

Huấn luyện, tinh chỉnh siêu tham số và đánh giá Random Forest Classifier
trên tập dữ liệu đã được cân bằng (SMOTE/ADASYN).

Author: Hoàng Cao Sơn — Phase 03
"""
import numpy as np
import pandas as pd
import pickle
import os
import time
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    roc_auc_score,
    precision_score,
    recall_score,
)

from src.utils import RANDOM_STATE, get_project_root


# ─── Default hyperparameter search space ─────────────────────────────────────
PARAM_DIST = {
    "n_estimators": [100, 200, 300, 500],
    "max_depth": [10, 20, 30, None],
    "min_samples_split": [2, 5, 10],
    "min_samples_leaf": [1, 2, 4],
    "max_features": ["sqrt", "log2"],
    "class_weight": ["balanced", "balanced_subsample", None],
}

# ─── Paths ────────────────────────────────────────────────────────────────────
MODELS_DIR = "models"
REPORTS_DIR = "reports"


def train_random_forest(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    tune: bool = True,
    random_state: int = RANDOM_STATE,
    n_iter: int = 50,
    cv: int = 5,
    scoring: str = "f1",
    verbose: int = 1,
) -> tuple[RandomForestClassifier, dict]:
    """Huấn luyện Random Forest với tùy chọn tinh chỉnh siêu tham số.

    Parameters
    ----------
    X_train : pd.DataFrame
        Features tập huấn luyện (đã oversample).
    y_train : pd.Series
        Nhãn tập huấn luyện.
    tune : bool
        True → dùng RandomizedSearchCV để tìm hyperparameters tốt nhất.
        False → dùng baseline config mặc định.
    random_state : int
        Seed cố định.
    n_iter : int
        Số lần thử trong RandomizedSearchCV.
    cv : int
        Số fold cross-validation.
    scoring : str
        Metric tối ưu hóa. Default: 'f1'.
    verbose : int
        Mức độ log.

    Returns
    -------
    (model, info) : tuple
        model: RandomForestClassifier đã train.
        info: dict chứa best_params, best_score, training_time_seconds.
    """
    start_time = time.time()

    if tune:
        print(f"🔍 RandomizedSearchCV: n_iter={n_iter}, cv={cv}, scoring={scoring}")
        base_rf = RandomForestClassifier(random_state=random_state, n_jobs=-1)

        search = RandomizedSearchCV(
            estimator=base_rf,
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
            "best_cv_score": round(search.best_score_, 4),
            "training_time_seconds": round(elapsed, 2),
            "n_iter": n_iter,
            "cv": cv,
            "scoring": scoring,
            "tuned": True,
        }
        print(f"✅ Best CV {scoring}: {info['best_cv_score']}")
        print(f"⏱️ Training time: {elapsed:.1f}s")
        print(f"📋 Best params: {info['best_params']}")

    else:
        print("🌲 Training baseline Random Forest (no tuning)...")
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features="sqrt",
            class_weight="balanced",
            random_state=random_state,
            n_jobs=-1,
        )
        model.fit(X_train, y_train)
        elapsed = time.time() - start_time

        info = {
            "best_params": model.get_params(),
            "training_time_seconds": round(elapsed, 2),
            "tuned": False,
        }
        print(f"✅ Baseline trained in {elapsed:.1f}s")

    return model, info


def predict(
    model: RandomForestClassifier,
    X_test: pd.DataFrame,
) -> tuple[np.ndarray, np.ndarray]:
    """Dự đoán nhãn và xác suất.

    Returns
    -------
    (y_pred, y_prob) : tuple
        y_pred: Nhãn dự đoán (0/1).
        y_prob: Xác suất thuộc lớp fraud (dùng cho ROC-AUC).
    """
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    return y_pred, y_prob


def evaluate_model(
    y_test: pd.Series,
    y_pred: np.ndarray,
    y_prob: np.ndarray,
    model_name: str = "Random Forest",
) -> dict:
    """Tính và in các metrics đánh giá.

    Returns
    -------
    dict
        Chứa f1, precision, recall, roc_auc, classification_report, confusion_matrix.
    """
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    auc = roc_auc_score(y_test, y_prob)
    cm = confusion_matrix(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=["Normal", "Fraud"], digits=4)

    metrics = {
        "model_name": model_name,
        "f1_score": round(f1, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "roc_auc": round(auc, 4),
        "confusion_matrix": cm,
        "classification_report": report,
    }

    print(f"\n{'='*50}")
    print(f"📊 {model_name} — Evaluation Results")
    print(f"{'='*50}")
    print(f"  F1-Score:   {f1:.4f}")
    print(f"  Precision:  {precision:.4f}")
    print(f"  Recall:     {recall:.4f}")
    print(f"  ROC-AUC:    {auc:.4f}")
    print(f"\nConfusion Matrix:")
    print(f"  TN={cm[0][0]:,}  FP={cm[0][1]:,}")
    print(f"  FN={cm[1][0]:,}  TP={cm[1][1]:,}")
    print(f"\n{report}")

    return metrics


def get_feature_importance(
    model: RandomForestClassifier,
    feature_names: list[str],
    top_n: int = 15,
) -> pd.DataFrame:
    """Trích xuất và sắp xếp độ quan trọng đặc trưng.

    Returns
    -------
    pd.DataFrame
        Bảng Feature/Importance sắp xếp giảm dần, top_n dòng.
    """
    importances = model.feature_importances_
    df = pd.DataFrame({
        "Feature": feature_names,
        "Importance": importances,
    }).sort_values("Importance", ascending=False).reset_index(drop=True)

    return df.head(top_n)


def save_model(
    model: RandomForestClassifier,
    name: str,
    models_dir: str | None = None,
) -> str:
    """Lưu model đã train thành file .pkl.

    Parameters
    ----------
    model : RandomForestClassifier
        Model đã train.
    name : str
        Tên file (không cần extension). VD: "rf_smote".
    models_dir : str, optional
        Thư mục lưu. Default: models/ trong project root.

    Returns
    -------
    str
        Đường dẫn file đã lưu.
    """
    if models_dir is None:
        models_dir = os.path.join(get_project_root(), MODELS_DIR)

    Path(models_dir).mkdir(parents=True, exist_ok=True)
    path = os.path.join(models_dir, f"{name}.pkl")

    with open(path, "wb") as f:
        pickle.dump(model, f)

    size_mb = os.path.getsize(path) / (1024 * 1024)
    print(f"💾 Model saved: {path} ({size_mb:.1f} MB)")

    if size_mb > 50:
        print(f"⚠️  File > 50MB — nên thêm vào .gitignore")

    return path


def load_model(
    name: str,
    models_dir: str | None = None,
) -> RandomForestClassifier:
    """Load model từ file .pkl.

    Parameters
    ----------
    name : str
        Tên file (không cần extension). VD: "rf_smote".
    models_dir : str, optional
        Thư mục chứa model. Default: models/ trong project root.

    Returns
    -------
    RandomForestClassifier
    """
    if models_dir is None:
        models_dir = os.path.join(get_project_root(), MODELS_DIR)

    path = os.path.join(models_dir, f"{name}.pkl")

    if not os.path.exists(path):
        raise FileNotFoundError(f"Model file not found: {path}")

    with open(path, "rb") as f:
        model = pickle.load(f)

    print(f"📂 Loaded model: {path}")
    return model


def save_predictions(
    y_pred: np.ndarray,
    y_prob: np.ndarray,
    name: str = "rf_predictions",
    reports_dir: str | None = None,
) -> str:
    """Lưu predictions (y_pred, y_prob) thành dict trong file .pkl.

    Returns
    -------
    str
        Đường dẫn file đã lưu.
    """
    if reports_dir is None:
        reports_dir = os.path.join(get_project_root(), REPORTS_DIR)

    Path(reports_dir).mkdir(parents=True, exist_ok=True)
    path = os.path.join(reports_dir, f"{name}.pkl")

    data = {"y_pred": y_pred, "y_prob": y_prob}
    with open(path, "wb") as f:
        pickle.dump(data, f)

    print(f"📊 Predictions saved: {path}")
    return path


def save_feature_importance(
    importance_df: pd.DataFrame,
    name: str = "rf_feature_importance",
    reports_dir: str | None = None,
) -> str:
    """Lưu bảng feature importance thành CSV.

    Returns
    -------
    str
        Đường dẫn file đã lưu.
    """
    if reports_dir is None:
        reports_dir = os.path.join(get_project_root(), REPORTS_DIR)

    Path(reports_dir).mkdir(parents=True, exist_ok=True)
    path = os.path.join(reports_dir, f"{name}.csv")

    importance_df.to_csv(path, index=False)
    print(f"📊 Feature importance saved: {path}")
    return path


def save_model_summary(
    metrics: dict,
    train_info: dict,
    name: str = "rf_model_summary",
    reports_dir: str | None = None,
) -> str:
    """Lưu tóm tắt model (metrics + hyperparams) thành file text.

    Returns
    -------
    str
        Đường dẫn file đã lưu.
    """
    if reports_dir is None:
        reports_dir = os.path.join(get_project_root(), REPORTS_DIR)

    Path(reports_dir).mkdir(parents=True, exist_ok=True)
    path = os.path.join(reports_dir, f"{name}.txt")

    lines = [
        f"{'='*60}",
        f"  Random Forest Model Summary",
        f"  Model: {metrics.get('model_name', 'N/A')}",
        f"{'='*60}",
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
        "",
        "--- Best Hyperparameters ---",
    ]

    best_params = train_info.get("best_params", {})
    for k, v in best_params.items():
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

    print(f"📄 Summary saved: {path}")
    return path
