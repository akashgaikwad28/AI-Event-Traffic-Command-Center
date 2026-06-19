import logging

import pandas as pd

logger = logging.getLogger(__name__)


class DataCleaner:
    """
    Implements the cleaning operations from 02_data_cleaning.ipynb.
    Parses dates, handles missing values, and drops fundamental corruption.
    """

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        initial_len = len(df)

        # 1. Parse Dates
        date_cols = [
            "start_datetime",
            "resolved_datetime",
            "closed_datetime",
            "modified_datetime",
        ]
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)

        # 2. Check and Drop Timestamp Inconsistencies
        invalid_times = df[df["resolved_datetime"] < df["start_datetime"]]

        # 3. Drop missing start times (cannot do operational analysis without it)
        df = df.dropna(subset=["start_datetime"])

        # 4. Handle invalid coordinates
        invalid_coords = df[
            (df["latitude"] < -90)
            | (df["latitude"] > 90)
            | (df["longitude"] < -180)
            | (df["longitude"] > 180)
        ]

        if len(invalid_coords) > 0:
            df = df.drop(invalid_coords.index)

        if len(invalid_times) > 0:
            df = df.drop(invalid_times.index)

        # 5. Fill essential missing values with 'unknown'
        fill_cols = ["event_cause", "veh_type", "priority"]
        for col in fill_cols:
            if col in df.columns:
                df[col] = df[col].fillna("unknown")

        logger.info(
            f"Dropped {initial_len - len(df)} rows due to corruption/invalid data."
        )
        return df
