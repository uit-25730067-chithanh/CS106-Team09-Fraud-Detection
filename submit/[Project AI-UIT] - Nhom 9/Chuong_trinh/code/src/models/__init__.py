from .random_forest_model import (
    train_random_forest,
    predict,
    evaluate_model,
    get_feature_importance,
    save_model,
    load_model,
    save_predictions,
    save_feature_importance,
    save_model_summary,
)
try:
    from .xgboost_model import (
        train_xgboost,
        save_model as save_xgb_model,
        load_model as load_xgb_model,
        save_model_summary as save_xgb_model_summary,
    )
except ImportError:
    pass

try:
    from .autoencoder_model import (
        build_autoencoder,
        train_autoencoder,
        compute_reconstruction_error,
        find_threshold,
        select_threshold_by_f1,
        predict_autoencoder,
        save_autoencoder,
        load_autoencoder,
        save_autoencoder_summary,
    )
except ImportError:
    pass

__all__ = [
    # Random Forest (Phase 03)
    "train_random_forest",
    "predict",
    "evaluate_model",
    "get_feature_importance",
    "save_model",
    "load_model",
    "save_predictions",
    "save_feature_importance",
    "save_model_summary",
    # XGBoost (Phase 04)
    "train_xgboost",
    "save_xgb_model",
    "load_xgb_model",
    "save_xgb_model_summary",
    # Autoencoder (Phase 04)
    "build_autoencoder",
    "train_autoencoder",
    "compute_reconstruction_error",
    "find_threshold",
    "select_threshold_by_f1",
    "predict_autoencoder",
    "save_autoencoder",
    "load_autoencoder",
    "save_autoencoder_summary",
]
