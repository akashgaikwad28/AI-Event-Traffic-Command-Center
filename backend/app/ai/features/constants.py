from pathlib import Path

from backend.app.ai.features.types import FeatureConfig

# Directory for storing ML artifacts
ARTIFACTS_DIR = Path("backend/app/ai/artifacts")
ENCODERS_DIR = ARTIFACTS_DIR / "encoders"
SCALERS_DIR = ARTIFACTS_DIR / "scalers"
METADATA_DIR = ARTIFACTS_DIR / "metadata"
DATASETS_DIR = ARTIFACTS_DIR / "datasets"

# Pipeline versions
PIPELINE_VERSION = "1.0.0"

DEFAULT_FEATURE_CONFIG: FeatureConfig = {
    "peak_hours_morning": (7, 10),
    "peak_hours_evening": (16, 19),
    "late_night_hours": (0, 5),
    "max_impact_radius_km": 2.0,
    "rolling_window_hours": 1,
    "rolling_window_days": 1,
}

# Values for handling unseen categorical data
UNKNOWN_CATEGORY = "UNKNOWN"
