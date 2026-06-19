import logging
from datetime import datetime
from pathlib import Path

import joblib
import pandas as pd
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier

from ml_pipeline.evaluation.model_evaluator import ModelEvaluator
from mlops.mlflow.tracker import MLFlowTracker
from mlops.model_registry.registry_manager import RegistryManager

logger = logging.getLogger(__name__)


class ModelTrainer:
    """
    Trains final models on all data, evaluates them, logs metrics via MLFlow,
    and exports inference artifacts to the registry.
    """

    def __init__(self, cleaned_data_path: str, artifacts_dir: str):
        self.data_path = Path(cleaned_data_path)
        self.artifacts_dir = Path(artifacts_dir)
        self.features = [
            "latitude",
            "longitude",
            "hour_of_day",
            "day_of_week",
            "is_weekend",
            "is_peak_hour",
            "priority_encoded",
            "is_closed",
        ]

        # Initialize MLOps Components
        self.tracker = MLFlowTracker(experiment_name="Gridwise_AI_Traffic_Models")
        self.registry = RegistryManager(
            registry_file=str(self.artifacts_dir / "model_registry.json")
        )
        self.evaluator = ModelEvaluator()
        from ml_pipeline.evaluation.visualize_metrics import ModelVisualizer

        self.visualizer = ModelVisualizer(output_dir="reports/figures")

    def train_and_export(self):
        logger.info(f"Loading data from {self.data_path}")
        if not self.data_path.exists():
            logger.error("Cleaned dataset not found. Run dataset_builder first.")
            return

        df = pd.read_parquet(self.data_path)
        X = df[self.features]

        self.tracker.start_run(
            run_name=f"Training_Run_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        )
        self.tracker.log_param("features", self.features)

        # Log Data Versions
        logger.info("Logging DVC data versions to MLflow...")
        if Path("data/raw.dvc").exists():
            self.tracker.log_artifact("data/raw.dvc")
        if Path("data/processed.dvc").exists():
            self.tracker.log_artifact("data/processed.dvc")

        # 1. Congestion Model (Regression)
        logger.info("Training Congestion Proxy Model (XGBoost)...")
        y_congestion = df.get("congestion_proxy_score", 0)
        congestion_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
        congestion_model.fit(X, y_congestion)

        y_pred_cong = congestion_model.predict(X)
        cong_metrics = self.evaluator.evaluate_regression(y_congestion, y_pred_cong)
        self.tracker.log_metric("congestion_rmse", cong_metrics["rmse"])
        self.tracker.log_metric("congestion_mae", cong_metrics["mae"])
        self.tracker.log_metric("congestion_r2", cong_metrics["r2"])

        self.visualizer.plot_feature_importance(
            model=congestion_model,
            feature_names=self.features,
            title="Congestion Model Feature Importance",
            filename="congestion_feature_importance.png",
        )

        # 2. Deployment Load Model (Classification)
        logger.info("Training Deployment Load Classification Model (RandomForest)...")
        y_deployment = df.get("deployment_load_class", "LOW")
        deployment_model = RandomForestClassifier(n_estimators=100, random_state=42)
        deployment_model.fit(X, y_deployment)

        y_pred_dep = deployment_model.predict(X)
        dep_metrics = self.evaluator.evaluate_classification(y_deployment, y_pred_dep)
        self.tracker.log_metric("deployment_accuracy", dep_metrics["accuracy"])
        self.tracker.log_metric("deployment_precision", dep_metrics["precision"])
        self.tracker.log_metric("deployment_recall", dep_metrics["recall"])
        self.tracker.log_metric("deployment_f1", dep_metrics["f1"])

        self.visualizer.plot_confusion_matrix(
            cm=dep_metrics["confusion_matrix"],
            class_names=list(deployment_model.classes_),
            filename="deployment_confusion_matrix.png",
        )
        self.visualizer.plot_feature_importance(
            model=deployment_model,
            feature_names=self.features,
            title="Deployment Load Feature Importance",
            filename="deployment_feature_importance.png",
        )

        # 3. Response Time Model (Regression)
        logger.info("Training Response Time Model (XGBoost)...")
        response_mask = df["resolution_time_minutes"].notna()
        X_resp = X[response_mask]
        y_resp = df.loc[response_mask, "resolution_time_minutes"]

        response_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
        response_model.fit(X_resp, y_resp)

        y_pred_resp = response_model.predict(X_resp)
        resp_metrics = self.evaluator.evaluate_regression(y_resp, y_pred_resp)
        self.tracker.log_metric("response_rmse", resp_metrics["rmse"])
        self.tracker.log_metric("response_mae", resp_metrics["mae"])
        self.tracker.log_metric("response_r2", resp_metrics["r2"])

        # Export Artifacts
        self.artifacts_dir.mkdir(parents=True, exist_ok=True)
        cong_path = self.artifacts_dir / "congestion_model.pkl"
        dep_path = self.artifacts_dir / "deployment_model.pkl"
        resp_path = self.artifacts_dir / "response_time_model.pkl"

        joblib.dump(congestion_model, cong_path)
        joblib.dump(deployment_model, dep_path)
        joblib.dump(response_model, resp_path)

        self.tracker.log_xgboost_model(
            congestion_model, "congestion_model", "Gridwise_Congestion_Proxy"
        )
        self.tracker.log_sklearn_model(
            deployment_model, "deployment_model", "Gridwise_Deployment_Load"
        )
        self.tracker.log_xgboost_model(
            response_model, "response_time_model", "Gridwise_Response_Time"
        )

        # Update Registry via MLOps RegistryManager
        final_metrics = {
            "congestion_rmse": cong_metrics["rmse"],
            "congestion_mae": cong_metrics["mae"],
            "congestion_r2": cong_metrics["r2"],
            "deployment_accuracy": dep_metrics["accuracy"],
            "deployment_precision": dep_metrics["precision"],
            "deployment_recall": dep_metrics["recall"],
            "deployment_f1": dep_metrics["f1"],
            "deployment_cm": dep_metrics["confusion_matrix"],
            "response_rmse": resp_metrics["rmse"],
            "response_mae": resp_metrics["mae"],
            "response_r2": resp_metrics["r2"],
        }
        self.registry.promote_model(
            version="1.0",
            stage="Production",
            features=self.features,
            metrics=final_metrics,
        )

        self.tracker.end_run()
        logger.info("Training Pipeline Completed Successfully.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    trainer = ModelTrainer(
        cleaned_data_path="data/processed/cleaned_dataset.parquet",
        artifacts_dir="backend/app/ai/artifacts",
    )
    trainer.train_and_export()
