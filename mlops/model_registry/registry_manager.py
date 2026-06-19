import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class RegistryManager:
    """
    Manages the promotion of models between environments (Staging -> Production).
    """

    def __init__(
        self, registry_file: str = "backend/app/ai/artifacts/model_registry.json"
    ):
        self.registry_file = Path(registry_file)

    def promote_model(self, version: str, stage: str, features: list, metrics: dict):
        """
        Registers a model version and its metrics to a stage.
        """
        logger.info(f"Promoting model version {version} to {stage}")

        # Load existing
        if self.registry_file.exists():
            with open(self.registry_file) as f:
                registry = json.load(f)
        else:
            registry = {}

        registry["version"] = version
        registry["stage"] = stage
        registry["features"] = features
        registry["metrics"] = metrics

        self.registry_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_file, "w") as f:
            json.dump(registry, f, indent=4)

        logger.info(f"Registry updated at {self.registry_file}")

    def get_production_model(self) -> str:
        """
        Returns the path to the current active production model.
        """
        return "backend/app/ai/artifacts/congestion_model.pkl"
