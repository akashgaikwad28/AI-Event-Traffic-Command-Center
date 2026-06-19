import json
from pathlib import Path
from typing import Any

import joblib

from backend.app.core.config import get_settings
from backend.app.core.logger import get_logger
from backend.app.exceptions.api_exceptions import ArtifactNotFound

logger = get_logger("ai.artifact_manager")
settings = get_settings()


class ArtifactManager:
    """Config-driven artifact path resolution and persistence utilities."""

    def __init__(self, base_dir: str | None = None):
        self.base_dir = Path(base_dir or settings.ai_artifacts_dir)

    def _resolve(self, *parts: str) -> Path:
        return self.base_dir.joinpath(*parts)

    def load_model(self, filename: str) -> Any:
        path = self._resolve(filename)
        if not path.exists():
            raise ArtifactNotFound(f"Model artifact not found: {path}")
        logger.info("Loading model artifact", path=str(path))
        return joblib.load(path)

    def load_json(self, *parts: str) -> dict:
        path = self._resolve(*parts)
        if not path.exists():
            raise ArtifactNotFound(f"JSON artifact not found: {path}")
        with open(path) as f:
            return json.load(f)

    def load_encoder(self, filename: str) -> Any:
        return self.load_model(f"encoders/{filename}")

    def model_exists(self, filename: str) -> bool:
        return self._resolve(filename).exists()

    def get_metadata(self) -> dict:
        return self.load_json("model_registry.json")
