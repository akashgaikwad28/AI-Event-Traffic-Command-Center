import logging

import pandas as pd

logger = logging.getLogger(__name__)


class FeatureGenerator:
    """
    Extracts features from 04_feature_engineering_validation.ipynb.
    Generates temporal features and encoded operational states.
    """

    def generate_features(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Generating operational features...")

        # Time features from start_datetime
        df["start_datetime"] = pd.to_datetime(df["start_datetime"], utc=True)

        df["hour_of_day"] = df["start_datetime"].dt.hour
        df["day_of_week"] = df["start_datetime"].dt.dayofweek
        df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)
        df["is_peak_hour"] = df["hour_of_day"].isin([8, 9, 10, 17, 18, 19]).astype(int)

        # Operational Features
        priority_map = {"unknown": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
        if "priority" in df.columns:
            df["priority_encoded"] = (
                df["priority"].str.lower().map(priority_map).fillna(0)
            )

        # Road Closure
        if "requires_road_closure" in df.columns:
            df["is_closed"] = (
                df["requires_road_closure"].astype(str).str.lower() == "true"
            )
            df["is_closed"] = df["is_closed"].astype(int)

        # Additional features
        df["heavy_vehicle"] = (
            df["veh_type"].str.lower().isin(["truck", "bus", "heavy"]).astype(int)
        )
        from backend.app.ai.features.target_engineering import (
            generate_congestion_proxy,
            generate_deployment_target,
            generate_response_duration_target,
        )

        # Target Generation
        df["resolution_time_minutes"] = generate_response_duration_target(df)
        df["congestion_proxy_score"] = generate_congestion_proxy(df)
        df["deployment_load_class"] = generate_deployment_target(df)

        return df
