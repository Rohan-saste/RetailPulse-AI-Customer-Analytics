# ==============================================================
# RetailPulse Server – ML Model Service
# ==============================================================

import os
import sys
import pickle
import numpy as np
import pandas as pd
from typing import Optional, Tuple, Dict
from app.config import settings
from app.utils.logger import logger


def _apply_numpy_compat_patch():
    """Apply numpy._core compatibility patch for models serialized with numpy 2.x."""
    try:
        import numpy._core  # noqa: F401
    except ImportError:
        import numpy.core as _core
        sys.modules["numpy._core"] = _core
        for name in ["multiarray", "numeric", "defchararray", "records", "memmap", "function_base", "fromnumeric"]:
            try:
                __import__("numpy.core." + name)
            except ImportError:
                pass
        for key in list(sys.modules.keys()):
            if key.startswith("numpy.core"):
                alias_key = key.replace("numpy.core", "numpy._core")
                sys.modules[alias_key] = sys.modules[key]
        logger.info("Numpy compatibility patch applied (numpy.core → numpy._core)")


class MLService:
    """Singleton service for loading and running ML model predictions."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.model = None
        self.scaler = None

    def load_models(self):
        """Load the churn prediction model and scaler from pickle files."""
        _apply_numpy_compat_patch()

        models_dir = settings.ML_MODELS_DIR
        model_path = os.path.join(models_dir, "best_churn_model.pkl")
        scaler_path = os.path.join(models_dir, "scaler.pkl")

        if os.path.exists(model_path) and os.path.exists(scaler_path):
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
            with open(scaler_path, "rb") as f:
                self.scaler = pickle.load(f)
            logger.info(f"ML models loaded from {models_dir}")
        else:
            logger.warning(f"ML model files not found in {models_dir}")

    def predict_churn(
        self,
        recency: int,
        frequency: int,
        monetary: float,
        avg_revenue: float,
        total_items: int,
        avg_quantity: float,
    ) -> Optional[Dict]:
        """Run churn prediction and return probability, label, and risk level."""
        if self.model is None or self.scaler is None:
            return None

        features = ["Recency", "Frequency", "Monetary", "AvgRevenue", "TotalItems", "AvgQuantity"]
        input_arr = pd.DataFrame(
            [[recency, frequency, monetary, avg_revenue, total_items, avg_quantity]],
            columns=features,
        )
        scaled_input = self.scaler.transform(input_arr)

        probability = float(self.model.predict_proba(scaled_input)[0][1])
        prediction = int(self.model.predict(scaled_input)[0])

        if probability < 0.4:
            risk_level = "Low"
        elif probability < 0.75:
            risk_level = "Medium"
        else:
            risk_level = "High"

        return {
            "probability": round(probability, 4),
            "prediction": prediction,
            "risk_level": risk_level,
        }


# Singleton instance
ml_service = MLService()
