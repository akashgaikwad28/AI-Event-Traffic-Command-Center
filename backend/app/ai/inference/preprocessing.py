from typing import Any

import pandas as pd


class PreprocessingEngine:
    """
    Transforms raw API payloads into validated feature vectors.
    Strictly mirrors the notebook training preprocessing logic.
    """

    @staticmethod
    def process_raw_payload(payload: dict[str, Any]) -> dict[str, Any]:
        """
        Converts the API request data into the exact features expected by the models.
        """
        features = {}

        # 1. Geographic Features
        features["latitude"] = payload.get("latitude")
        features["longitude"] = payload.get("longitude")

        # 2. Temporal Features
        dt = payload.get("timestamp")
        if not dt:
            dt = pd.Timestamp.now()  # Fallback to current time
        elif isinstance(dt, str):
            dt = pd.to_datetime(dt)

        features["hour_of_day"] = dt.hour
        features["day_of_week"] = dt.dayofweek
        features["is_weekend"] = dt.dayofweek >= 5
        features["is_peak_hour"] = (7 <= dt.hour <= 9) or (16 <= dt.hour <= 19)

        # 3. Operational Features
        priority_map = {"Low": 0, "Medium": 1, "High": 2}
        priority_raw = payload.get("priority", "Medium")
        features["priority_encoded"] = priority_map.get(priority_raw, 1)

        features["is_closed"] = payload.get("requires_road_closure", False)

        return features
