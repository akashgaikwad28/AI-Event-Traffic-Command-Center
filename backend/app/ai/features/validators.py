import numpy as np
import pandas as pd


def validate_features(
    df: pd.DataFrame, columns_to_check: list[str] = None
) -> pd.DataFrame:
    """
    Validate features for NaNs, infinite values, and duplicates.
    Provides safe fallback or raises errors if dataset is too corrupt.
    """
    if df.empty:
        return df

    cols = columns_to_check if columns_to_check else df.columns

    # 1. Check for duplicate columns
    if df.columns.duplicated().any():
        dupes = df.columns[df.columns.duplicated()].tolist()
        raise ValueError(f"Duplicate columns found in features: {dupes}")

    # 2. Handle Inf/NaN values in numeric columns safely
    numeric_cols = df[cols].select_dtypes(include=[np.number]).columns

    # Replace inf with NaN first
    df[numeric_cols] = df[numeric_cols].replace([np.inf, -np.inf], np.nan)

    # Fill remaining NaNs with 0 (safe default for frequencies/counts)
    # For more complex pipelines, we'd use a fitted imputer
    df[numeric_cols] = df[numeric_cols].fillna(0.0)

    # 3. Impossible values validation (e.g. negative duration)
    if "event_duration_minutes" in df.columns:
        # Cap impossible negative durations to 0
        df.loc[df["event_duration_minutes"] < 0, "event_duration_minutes"] = 0.0

    return df
