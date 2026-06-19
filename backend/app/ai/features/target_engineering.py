import numpy as np
import pandas as pd


def generate_response_duration_target(
    df: pd.DataFrame,
    start_col: str = "start_datetime",
    end_col: str = "resolved_datetime",
) -> pd.Series:
    """
    Generate the target for response time in minutes.
    This is the operational proxy for resolution duration.
    """
    start_dt = pd.to_datetime(df[start_col], errors="coerce", utc=True)
    end_dt = pd.to_datetime(df[end_col], errors="coerce", utc=True)

    duration_mins = (end_dt - start_dt).dt.total_seconds() / 60.0
    return duration_mins.clip(lower=0)


def generate_congestion_proxy(df: pd.DataFrame) -> pd.Series:
    """
    Generate an operational proxy for congestion severity.
    Weighted combination of:
    - severity / priority (High/Low)
    - closure status
    - event duration proxy
    """
    # Initialize base score
    score = np.zeros(len(df))

    # 1. Priority weight
    priority = df.get("priority", pd.Series(["Low"] * len(df))).astype(str).str.lower()
    score += np.where(priority == "high", 3.0, 1.0)

    # 2. Road Closure weight
    closure = df.get("requires_road_closure", pd.Series([False] * len(df)))
    # convert to bool just in case
    if closure.dtype == object:
        closure = closure.astype(str).str.lower() == "true"
    score += np.where(closure, 5.0, 0.0)

    # 3. Event Type weight (heuristic)
    event_type = (
        df.get("event_type", pd.Series(["unknown"] * len(df))).astype(str).str.lower()
    )
    score += np.where(event_type.isin(["planned", "accident"]), 2.0, 0.0)

    # 4. Event Cause weight
    cause = (
        df.get("event_cause", pd.Series(["unknown"] * len(df))).astype(str).str.lower()
    )
    score += np.where(cause.isin(["tree_fall", "water_logging", "accident"]), 2.0, 0.0)

    # Optional: If duration is already calculated, we could weight extremely long events higher.
    if "resolution_time_minutes" in df.columns:
        dur = df["resolution_time_minutes"].fillna(0)
        # Cap duration impact at max 5.0 to prevent blowing up the score
        score += np.clip(dur / 60.0, 0, 5.0)

    return pd.Series(score, index=df.index, name="congestion_proxy_score")


def generate_deployment_target(df: pd.DataFrame) -> pd.Series:
    """
    Generate an operational deployment load target.
    This classifies deployment load into 'LOW', 'MEDIUM', 'HIGH'.
    It's built off severity, closure, cause, and vehicle type.
    """
    load = np.zeros(len(df))

    # Add weights
    priority = df.get("priority", pd.Series(["Low"] * len(df))).astype(str).str.lower()
    load += np.where(priority == "high", 2.0, 0.5)

    closure = df.get("requires_road_closure", pd.Series([False] * len(df)))
    if closure.dtype == object:
        closure = closure.astype(str).str.lower() == "true"
    load += np.where(closure, 3.0, 0.0)

    veh_type = (
        df.get("veh_type", pd.Series(["unknown"] * len(df))).astype(str).str.lower()
    )
    load += np.where(veh_type.isin(["heavy_vehicle", "bus", "truck"]), 2.0, 0.0)

    # Discretize into classes
    def _discretize(val):
        if val < 2.5:
            return "LOW"
        elif val < 5.0:
            return "MEDIUM"
        else:
            return "HIGH"

    return pd.Series(
        [_discretize(v) for v in load], index=df.index, name="deployment_load_class"
    )
