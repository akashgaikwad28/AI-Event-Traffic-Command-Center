import json

import pandas as pd

from backend.app.ai.features.constants import (
    DEFAULT_FEATURE_CONFIG,
    ENCODERS_DIR,
    METADATA_DIR,
)
from backend.app.ai.features.encoders import CategoricalEncoder
from backend.app.ai.features.geo_features import generate_geo_features
from backend.app.ai.features.time_features import generate_time_features
from backend.app.ai.features.traffic_features import generate_traffic_features
from backend.app.ai.features.validators import validate_features
from backend.app.geo.spatial_engine import SpatialEngine


class FeaturePipeline:
    """
    Central orchestration for ML feature generation.
    Ensures training and inference consistency.
    """

    def __init__(self, config: dict = DEFAULT_FEATURE_CONFIG):
        self.config = config
        self.spatial_engine = SpatialEngine()

        # Encoders
        self.zone_encoder = CategoricalEncoder(unknown_value=-1)
        self.type_encoder = CategoricalEncoder(unknown_value=-1)
        self.category_encoder = CategoricalEncoder(unknown_value=-1)

        self.feature_columns = []

    def _ensure_dirs(self):
        ENCODERS_DIR.mkdir(parents=True, exist_ok=True)
        METADATA_DIR.mkdir(parents=True, exist_ok=True)

    def _generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Internal method to generate all raw features."""
        df = df.copy()

        df = generate_time_features(df, self.config)
        df = generate_traffic_features(df)
        df = generate_geo_features(df, self.spatial_engine)

        return df

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Run on training data to generate features and FIT stateful encoders.
        Persists the final feature schema.
        """
        df = self._generate_features(df)

        # Fit & Transform encoders
        if "zone_name" in df.columns:
            df["zone_encoded"] = self.zone_encoder.fit_transform(df["zone_name"])
        if "event_type" in df.columns:
            df["type_encoded"] = self.type_encoder.fit_transform(df["event_type"])
        if "event_category" in df.columns:
            df["category_encoded"] = self.category_encoder.fit_transform(
                df["event_category"]
            )

        # Validate
        df = validate_features(df)

        # Select numeric ML-ready columns
        self.feature_columns = df.select_dtypes(include=["number"]).columns.tolist()
        # Drop IDs or raw labels if they accidentally leaked in numeric form
        if "id" in self.feature_columns:
            self.feature_columns.remove("id")

        df = df[self.feature_columns]

        # Save artifacts
        self._save_artifacts()

        return df

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Run on inference data using LOADED stateful encoders.
        Ensures strict schema ordering.
        """
        self._load_artifacts()

        df = self._generate_features(df)

        if "zone_name" in df.columns:
            df["zone_encoded"] = self.zone_encoder.transform(df["zone_name"])
        if "event_type" in df.columns:
            df["type_encoded"] = self.type_encoder.transform(df["event_type"])
        if "event_category" in df.columns:
            df["category_encoded"] = self.category_encoder.transform(
                df["event_category"]
            )

        df = validate_features(df)

        # Ensure exact column match (fill missing with 0.0)
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0.0

        return df[self.feature_columns]

    def _save_artifacts(self):
        self._ensure_dirs()
        self.zone_encoder.save(ENCODERS_DIR / "zone_encoder.joblib")
        self.type_encoder.save(ENCODERS_DIR / "type_encoder.joblib")
        self.category_encoder.save(ENCODERS_DIR / "category_encoder.joblib")

        with open(METADATA_DIR / "feature_metadata.json", "w") as f:
            json.dump({"feature_columns": self.feature_columns}, f, indent=2)

    def _load_artifacts(self):
        self.zone_encoder.load(ENCODERS_DIR / "zone_encoder.joblib")
        self.type_encoder.load(ENCODERS_DIR / "type_encoder.joblib")
        self.category_encoder.load(ENCODERS_DIR / "category_encoder.joblib")

        with open(METADATA_DIR / "feature_metadata.json") as f:
            metadata = json.load(f)
            self.feature_columns = metadata["feature_columns"]
