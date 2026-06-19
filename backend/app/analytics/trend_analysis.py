from typing import Any

import pandas as pd


class TrendAnalysisEngine:
    """
    Temporal intelligence engine.
    Computes rolling anomalies, surges, and degradation trends.
    """

    def detect_operational_anomalies(
        self, timeseries_df: pd.DataFrame, window: int = 12, threshold_std: float = 2.0
    ) -> dict[str, Any]:
        """
        Detects surges using a rolling z-score methodology.
        """
        if timeseries_df.empty or len(timeseries_df) < window:
            return {"surge_detected": False, "anomalies": []}

        rolling_mean = timeseries_df["incident_count"].rolling(window=window).mean()
        rolling_std = timeseries_df["incident_count"].rolling(window=window).std()

        z_scores = (timeseries_df["incident_count"] - rolling_mean) / (
            rolling_std + 1e-9
        )
        anomalies = timeseries_df[z_scores > threshold_std]

        return {
            "surge_detected": len(anomalies) > 0,
            "anomaly_count": len(anomalies),
            "degradation_trend_score": (
                round(z_scores.iloc[-1], 2) if not z_scores.empty else 0.0
            ),
        }

    def compute_peak_hour_analysis(self, df: pd.DataFrame) -> dict[str, Any]:
        """Analyzes degradation during rush hours."""
        if "hour_of_day" not in df.columns:
            df["hour_of_day"] = pd.to_datetime(df["start_datetime"]).dt.hour

        peak_mask = df["hour_of_day"].isin([7, 8, 9, 16, 17, 18, 19])
        peak_avg = (
            df.loc[peak_mask, "duration_mins"].mean()
            if "duration_mins" in df.columns
            else 0.0
        )
        offpeak_avg = (
            df.loc[~peak_mask, "duration_mins"].mean()
            if "duration_mins" in df.columns
            else 0.0
        )

        return {
            "rush_hour_escalation_ratio": (
                round(peak_avg / offpeak_avg, 2) if offpeak_avg > 0 else 1.0
            ),
            "peak_avg_duration": round(peak_avg, 1),
        }
