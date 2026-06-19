import logging
import os

import dagshub

import mlflow

logger = logging.getLogger(__name__)


class MLFlowTracker:
    """
    MLFlow Tracking for experiment parameters, metrics, and models.
    """

    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        self.active_run = None

        os.environ["DAGSHUB_USER_TOKEN"] = "64439ce9f57e346ec0a6f8e6879e2e5bfa181fea"
        dagshub.auth.add_app_token("64439ce9f57e346ec0a6f8e6879e2e5bfa181fea")
        dagshub.init(
            repo_owner="akash.gaikwad9945",
            repo_name="AI-Event-Traffic-Command-Center",
            mlflow=True,
        )

        mlflow.set_tracking_uri(
            "https://dagshub.com/akash.gaikwad9945/AI-Event-Traffic-Command-Center.mlflow"
        )
        mlflow.set_experiment(experiment_name)

    def start_run(self, run_name: str):
        self.active_run = mlflow.start_run(run_name=run_name)
        logger.info(
            f"[MLFlow] Started run: {run_name} under experiment {self.experiment_name}"
        )

    def end_run(self):
        mlflow.end_run()
        self.active_run = None
        logger.info("[MLFlow] Ended run")

    def log_param(self, key: str, value: any):
        mlflow.log_param(key, value)
        logger.info(f"[MLFlow] Logged Param - {key}: {value}")

    def log_metric(self, key: str, value: float):
        mlflow.log_metric(key, value)
        logger.info(f"[MLFlow] Logged Metric - {key}: {value}")

    def log_artifact(self, artifact_path: str):
        mlflow.log_artifact(artifact_path)
        logger.info(f"[MLFlow] Logged Artifact - Path: {artifact_path}")

    def log_xgboost_model(self, model, artifact_path: str, registered_model_name: str):
        mlflow.xgboost.log_model(
            model,
            artifact_path=artifact_path,
            registered_model_name=registered_model_name,
        )
        logger.info(
            f"[MLFlow] Registered XGBoost Model - Name: {registered_model_name}"
        )

    def log_sklearn_model(self, model, artifact_path: str, registered_model_name: str):
        mlflow.sklearn.log_model(
            model,
            artifact_path=artifact_path,
            registered_model_name=registered_model_name,
        )
        logger.info(
            f"[MLFlow] Registered Sklearn Model - Name: {registered_model_name}"
        )
