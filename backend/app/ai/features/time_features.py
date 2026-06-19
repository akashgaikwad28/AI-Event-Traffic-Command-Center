import pandas as pd

from backend.app.ai.features.constants import DEFAULT_FEATURE_CONFIG


def generate_time_features(
    df: pd.DataFrame, config: dict = DEFAULT_FEATURE_CONFIG
) -> pd.DataFrame:
    """
    Generate temporal features from timestamps.
    Operates vectorially on the DataFrame.
    """
    if df.empty:
        return df

    # We assume 'start_time' exists.
    if "start_time" not in df.columns:
        raise ValueError("Column 'start_time' is required for time features.")

    # Ensure start_time is datetime
    start_times = pd.to_datetime(df["start_time"])

    df["hour_of_day"] = start_times.dt.hour
    df["day_of_week"] = start_times.dt.dayofweek
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    # Operational windows
    m_start, m_end = config["peak_hours_morning"]
    e_start, e_end = config["peak_hours_evening"]
    l_start, l_end = config["late_night_hours"]

    df["is_morning_rush"] = df["hour_of_day"].between(m_start, m_end).astype(int)
    df["is_evening_rush"] = df["hour_of_day"].between(e_start, e_end).astype(int)

    # Late night could cross midnight, but let's assume 0-5
    df["is_late_night"] = df["hour_of_day"].between(l_start, l_end).astype(int)

    # Duration features
    # If resolved_at is not present, we use end_time or default to some duration if active
    if "resolved_at" in df.columns:
        resolved_times = pd.to_datetime(df["resolved_at"])
        # Fill missing resolved_at with end_time if available, else assume current time for active?
        # Actually, if an event is active, resolution_delay might be NaN. We should fill carefully.
        # But for ML, we only use historical closed events for duration training.
        # So we leave as NaN and let validators or traffic_features handle imputation.
        df["event_duration_minutes"] = (
            resolved_times - start_times
        ).dt.total_seconds() / 60.0

        # If end_time is present, we can compute delay past expected end_time
        if "end_time" in df.columns:
            end_times = pd.to_datetime(df["end_time"])
            df["resolution_delay_minutes"] = (
                resolved_times - end_times
            ).dt.total_seconds() / 60.0

    return df
