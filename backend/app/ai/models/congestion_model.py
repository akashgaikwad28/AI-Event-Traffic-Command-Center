import time
from typing import Any

import numpy as np
import pandas as pd

from backend.app.core.logger import get_logger
from backend.app.exceptions.api_exceptions import InferenceFailed

logger = get_logger("ai.models.congestion")


class CongestionModel:
    """
    Production wrapper around the trained congestion prediction model.
    Inference-only — no training logic.
    """

    def __init__(self, model: Any, feature_columns: list[str]):
        self.model = model
        self.feature_columns = feature_columns

    def predict(self, features: pd.DataFrame) -> np.ndarray:
        """Return congestion proxy scores."""
        try:
            start = time.perf_counter()
            X = features[self.feature_columns]
            preds = self.model.predict(X)
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.info("Congestion inference", count=len(X), ms=round(elapsed_ms, 2))
            return np.clip(preds, 0, None)
        except Exception as e:
            raise InferenceFailed(f"Congestion prediction failed: {e}")

    def predict_single(self, features: dict) -> float:
        """Predict for a single event."""
        df = pd.DataFrame([features])
        return float(self.predict(df)[0])

    def metadata(self) -> dict:
        return {
            "model_type": type(self.model).__name__,
            "feature_count": len(self.feature_columns),
            "features": self.feature_columns,
        }
