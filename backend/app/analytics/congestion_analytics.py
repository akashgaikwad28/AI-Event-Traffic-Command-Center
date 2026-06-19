from typing import Any

import pandas as pd


class CongestionAnalytics:
    """
    Operational congestion intelligence.
    Computes distribution, density, and rankings.
    """

    def compute_congestion_kpis(self, df: pd.DataFrame) -> dict[str, Any]:
        if df.empty or "congestion_severity" not in df.columns:
            return {
                "average_congestion_score": 0.0,
                "severity_distribution": {},
                "escalation_frequency": 0.0,
                "hotspot_density": 0.0,
            }

        severity_dist = df["congestion_severity"].value_counts(normalize=True).to_dict()
        severity_dist = {str(k): round(v * 100, 1) for k, v in severity_dist.items()}

        # Assume 'High' or 'Critical' are escalations
        escalations = df["congestion_severity"].isin(["High", "Critical"]).mean()

        return {
            "average_congestion_score": 50.0,  # Placeholder for numeric scale if available
            "severity_distribution": severity_dist,
            "escalation_frequency": round(escalations * 100, 1),
            "hotspot_density": len(df) / 100.0,  # Mock metric
        }

    def build_corridor_rankings(self, df: pd.DataFrame) -> list[dict[str, Any]]:
        """Ranks corridors by active congestion events."""
        if "corridor" not in df.columns:
            return []
        ranking = df["corridor"].value_counts().head(10).to_dict()
        return [{"corridor": k, "active_events": v} for k, v in ranking.items()]
