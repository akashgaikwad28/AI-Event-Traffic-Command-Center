import pandas as pd


def generate_traffic_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate traffic, congestion, and severity related features.
    Includes temporally-safe rolling features to prevent data leakage.
    """
    if df.empty:
        return df

    # Normalize severity: Assuming low=1, medium=2, high=3, critical=4
    severity_map = {"low": 1.0, "medium": 2.0, "high": 3.0, "critical": 4.0}
    if "severity" in df.columns:
        df["severity_encoded"] = (
            df["severity"].str.lower().map(severity_map).fillna(1.0)
        )
        # Scale to 0-1
        df["severity_scaled"] = (df["severity_encoded"] - 1.0) / 3.0

    if "road_closure" in df.columns:
        df["road_closure_binary"] = df["road_closure"].astype(int)
        df["closure_severity"] = df["severity_scaled"] * (df["road_closure_binary"] + 1)

    if "congestion_score" in df.columns:
        # Impute missing congestion with 0.5 (moderate)
        df["congestion_score"] = df["congestion_score"].fillna(0.5)
        df["blockage_level"] = df["severity_scaled"] * df["congestion_score"]

    # Temporal safe rolling features (Requires start_time)
    if "start_time" in df.columns:
        # Sort chronologically to prevent future data leakage
        df = df.sort_values("start_time").copy()

        # We need a datetime index for rolling window
        df_temp = df.set_index(pd.to_datetime(df["start_time"]))

        # Count incidents in the last 1 hour and 24 hours BEFORE the current row
        # closed='left' ensures the current event is NOT included in the count (leakage prevention)

        # 1-hour rolling count
        df["incidents_last_hour"] = (
            df_temp["id"].rolling("1h", closed="left").count().fillna(0).values
        )

        # 24-hour rolling count
        df["incidents_last_24h"] = (
            df_temp["id"].rolling("24h", closed="left").count().fillna(0).values
        )

        # Recurring zone frequency in last 24h
        if "zone_name" in df.columns:
            # We can group by zone and do a rolling count
            df["zone_incidents_24h"] = (
                df_temp.groupby("zone_name")["id"]
                .rolling("24h", closed="left")
                .count()
                .reset_index(level=0, drop=True)
                .reindex(df_temp.index)
                .fillna(0)
                .values
            )

    return df
