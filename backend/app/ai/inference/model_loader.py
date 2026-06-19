import warnings
from pathlib import Path
from typing import Any

import joblib

# Suppress version inconsistency warnings from scikit-learn/xgboost for a cleaner demo log
warnings.filterwarnings("ignore", category=UserWarning)

from backend.app.ai.registry.model_registry import ModelRegistry


class ModelLoader:
    """
    Singleton caching loader for production inference models.
    Lazy loads models into memory on first request.
    """

    _instance = None
    _models: dict[str, Any] = {}

    def __new__(cls, artifacts_dir: Path):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.registry = ModelRegistry(artifacts_dir)
            cls._instance.artifacts_dir = artifacts_dir
        return cls._instance

    def get_model(self, model_name: str) -> Any:
        """
        Retrieves a loaded model from the cache or loads it from disk.
        """
        if model_name in self._models:
            return self._models[model_name]

        model_path = self.registry.get_model_path(model_name)
        if not model_path.exists():
            raise FileNotFoundError(f"Missing required model artifact: {model_name}")

        try:
            model = joblib.load(model_path)
            self._models[model_name] = model
            return model
        except Exception as e:
            raise RuntimeError(
                f"Failed to load model {model_name} from {model_path}: {e}"
            )

    def get_feature_contract(self) -> list[str]:
        """Exposes the required feature order from the registry."""
        return self.registry.get_feature_schema()
