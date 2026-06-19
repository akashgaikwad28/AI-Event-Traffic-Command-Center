import json
from pathlib import Path
from typing import Any


class ModelRegistry:
    """
    Centralized artifact and version control for the Operational Intelligence Engine.
    """

    def __init__(self, artifacts_dir: Path):
        self.artifacts_dir = artifacts_dir
        self.registry_path = artifacts_dir / "model_registry.json"
        self._registry_cache: dict[str, Any] | None = None

    def load_registry(self) -> dict[str, Any]:
        """Loads the registry metadata from the artifacts directory."""
        if self._registry_cache is not None:
            return self._registry_cache

        if not self.registry_path.exists():
            raise FileNotFoundError(
                f"Model registry not found at {self.registry_path}. Ensure models are exported."
            )

        with open(self.registry_path) as f:
            self._registry_cache = json.load(f)

        return self._registry_cache

    def get_model_path(self, model_name: str) -> Path:
        """Resolves the physical path to a trained model artifact."""
        return self.artifacts_dir / f"{model_name}.pkl"

    def get_feature_schema(self) -> list[str]:
        """Returns the strictly ordered list of features required for inference."""
        registry = self.load_registry()
        if "features" not in registry:
            raise KeyError("Feature schema not found in model registry.")
        return registry["features"]

    def get_version(self) -> str:
        """Returns the active version of the deployed model ensemble."""
        registry = self.load_registry()
        return registry.get("version", "unknown")


# Singleton instance will be initialized in the model loader
