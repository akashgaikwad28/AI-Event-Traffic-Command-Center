from typing import Any

import pandas as pd


class FeatureValidationException(Exception):
    """Raised when the inference payload violates the feature contract."""

    pass


class FeatureContract:
    """
    Enforces strict schema validation between the notebook training environment
    and the production inference engine.
    """

    def __init__(self, required_features: list[str]):
        """
        Initializes the contract with the locked feature order from the model registry.
        """
        self.required_features = required_features

        # Expected datatypes derived from training
        self.expected_dtypes = {
            "latitude": float,
            "longitude": float,
            "hour_of_day": int,
            "day_of_week": int,
            "is_weekend": bool,
            "is_peak_hour": bool,
            "priority_encoded": int,
            "is_closed": bool,
        }

    def validate_and_format(self, raw_features: dict[str, Any]) -> pd.DataFrame:
        """
        Validates the raw dictionary against the contract and returns a strictly
        ordered DataFrame ready for inference.
        """
        # 1. Missing Feature Check
        missing = [f for f in self.required_features if f not in raw_features]
        if missing:
            raise FeatureValidationException(f"Missing required features: {missing}")

        # 2. Unexpected Feature Check (Warning or Drop)
        # We drop them rather than failing, to support API evolution.
        clean_features = {
            k: v for k, v in raw_features.items() if k in self.required_features
        }

        # 3. Datatype and Value Validation
        for feature, value in clean_features.items():
            expected_type = self.expected_dtypes.get(feature)
            if expected_type and value is not None:
                try:
                    clean_features[feature] = expected_type(value)
                except (ValueError, TypeError):
                    raise FeatureValidationException(
                        f"Type mismatch for {feature}: expected {expected_type.__name__}"
                    )

        # 4. Coordinate Validity Check
        lat, lon = clean_features.get("latitude"), clean_features.get("longitude")
        if lat is not None and (lat < -90 or lat > 90):
            raise FeatureValidationException(f"Invalid latitude: {lat}")
        if lon is not None and (lon < -180 or lon > 180):
            raise FeatureValidationException(f"Invalid longitude: {lon}")

        # 5. Order Locking (Crucial for XGBoost/LightGBM)
        df = pd.DataFrame([clean_features])
        df = df[self.required_features]  # Reorder to perfectly match training

        return df
