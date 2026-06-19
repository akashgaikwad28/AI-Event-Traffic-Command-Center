import logging

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    precision_score,
    r2_score,
    recall_score,
)

logger = logging.getLogger(__name__)


class ModelEvaluator:
    """
    Evaluates ML models and calculates comprehensive performance metrics.
    """

    @staticmethod
    def evaluate_regression(y_true, y_pred) -> dict:
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)

        logger.info(
            f"Regression Evaluation - RMSE: {rmse:.4f}, MAE: {mae:.4f}, R2: {r2:.4f}"
        )
        return {"rmse": rmse, "mae": mae, "r2": r2}

    @staticmethod
    def evaluate_classification(y_true, y_pred) -> dict:
        accuracy = accuracy_score(y_true, y_pred)
        # We use macro average for multi-class/imbalanced robust metrics
        precision = precision_score(y_true, y_pred, average="macro", zero_division=0)
        recall = recall_score(y_true, y_pred, average="macro", zero_division=0)
        f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
        cm = confusion_matrix(y_true, y_pred).tolist()

        logger.info(
            f"Classification Evaluation - Accuracy: {accuracy:.4f}, F1: {f1:.4f}"
        )
        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "confusion_matrix": cm,
        }
