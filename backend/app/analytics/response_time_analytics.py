from typing import Any

import pandas as pd


class ResponseTimeAnalytics:
    """
    Operational efficiency analytics engine.
    Computes p50, p90, p95, tail latency, and SLA breaches.
    """

    def __init__(self, sla_threshold_mins: float = 60.0):
        self.sla_threshold = sla_threshold_mins

    def compute_response_metrics(self, df: pd.DataFrame) -> dict[str, Any]:
        """
        Computes enterprise tail-latency metrics for clearance times.
        Expects a DataFrame with 'closed_datetime' and 'start_datetime'.
        """
        if df.empty:
            return self._empty_metrics()

        # Ensure duration is calculated
        if "duration_mins" not in df.columns:
            df["duration_mins"] = (
                pd.to_datetime(df["closed_datetime"])
                - pd.to_datetime(df["start_datetime"])
            ).dt.total_seconds() / 60.0
            df = df.dropna(subset=["duration_mins"])

        if df.empty:
            return self._empty_metrics()

        durations = df["duration_mins"]

        return {
            "avg_clearance_duration": round(durations.mean(), 1),
            "median_resolution_time": round(durations.median(), 1),
            "p50": round(durations.quantile(0.50), 1),
            "p90": round(durations.quantile(0.90), 1),
            "p95": round(durations.quantile(0.95), 1),
            "tail_latency_mins": round(durations.quantile(0.99), 1),
            "sla_breach_rate": round((durations > self.sla_threshold).mean() * 100, 1),
            "total_breaches": int((durations > self.sla_threshold).sum()),
        }

    def _empty_metrics(self) -> dict[str, Any]:
        return {
            "avg_clearance_duration": 0.0,
            "median_resolution_time": 0.0,
            "p50": 0.0,
            "p90": 0.0,
            "p95": 0.0,
            "tail_latency_mins": 0.0,
            "sla_breach_rate": 0.0,
            "total_breaches": 0,
        }
