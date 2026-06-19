from typing import Any

import pandas as pd


class IncidentPatternAnalytics:
    """
    Operational Pattern Detection (Hackathon Differentiator).
    Detects cascading risk, geo recurrence, and temporal windows.
    """

    def detect_recurring_events(self, df: pd.DataFrame) -> dict[str, Any]:
        """Detects high-frequency recurrence in DBSCAN clusters."""
        if "geo_cluster_id" not in df.columns:
            return {"recurring_clusters": []}

        cluster_counts = df["geo_cluster_id"].value_counts()
        recurring = cluster_counts[
            cluster_counts > 3
        ]  # More than 3 incidents in window

        return {
            "recurring_clusters": recurring.to_dict(),
            "hotspot_volatility": (
                round(cluster_counts.std(), 2) if not cluster_counts.empty else 0.0
            ),
        }

    def compute_cascading_probability(self, df: pd.DataFrame) -> float:
        """
        Estimates the probability of a secondary incident (cascading risk).
        In a real scenario, this involves analyzing timestamp proximity within clusters.
        """
        if df.empty or "geo_cluster_id" not in df.columns:
            return 0.0

        # Simplified operational logic: High density in short time = cascade risk
        cluster_density = df.groupby("geo_cluster_id").size().mean()
        base_probability = min(0.95, cluster_density * 0.05)
        return round(base_probability * 100, 1)

    def identify_dangerous_corridors(self, df: pd.DataFrame) -> list[dict[str, Any]]:
        """Identifies corridors with repeated closures."""
        if "corridor" not in df.columns or "requires_road_closure" not in df.columns:
            return []

        closures = df[df["requires_road_closure"] == True]
        corridor_closures = closures["corridor"].value_counts().head(5)

        return [
            {"corridor": k, "closure_count": v} for k, v in corridor_closures.items()
        ]
