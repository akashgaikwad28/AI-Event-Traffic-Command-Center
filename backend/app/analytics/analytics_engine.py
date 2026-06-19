from datetime import datetime
from typing import Any

import pandas as pd

from backend.app.analytics.congestion_analytics import CongestionAnalytics
from backend.app.analytics.contracts.analytics_contracts import (
    OperationalSnapshotContract,
)
from backend.app.analytics.incident_patterns import IncidentPatternAnalytics
from backend.app.analytics.operational_kpis import OperationalKPIEngine
from backend.app.analytics.response_time_analytics import ResponseTimeAnalytics
from backend.app.analytics.trend_analysis import TrendAnalysisEngine


class AnalyticsEngine:
    """
    Central orchestration layer for the Operational Analytics Engine.
    Coordinates sub-modules without executing complex math directly.
    """

    def __init__(self):
        self.congestion = CongestionAnalytics()
        self.response = ResponseTimeAnalytics()
        self.patterns = IncidentPatternAnalytics()
        self.kpis = OperationalKPIEngine()
        self.trends = TrendAnalysisEngine()

    def generate_command_center_snapshot(
        self, current_df: pd.DataFrame, historical_df: pd.DataFrame
    ) -> dict[str, Any]:
        """
        Orchestrates the massive, multi-module aggregation for the main dashboard.
        """
        # 1. Response Metrics
        resp_metrics = self.response.compute_response_metrics(historical_df)

        # 2. Congestion KPIs
        cong_metrics = self.congestion.compute_congestion_kpis(current_df)

        # 3. Trends & Surges
        trend_metrics = self.trends.detect_operational_anomalies(historical_df)

        # 4. Executive KPIs & City Health
        # We pass the avg congestion/duration up to the KPI engine
        exec_kpis = self.kpis.generate_executive_kpis(
            current_df,
            avg_gori=50.0,  # Placeholder, would be fetched from Inference Engine DB logs
            sla_breach=resp_metrics.get("sla_breach_rate", 0.0),
        )

        # Contract Enforcement
        # We output a dictionary that matches the OperationalSnapshotContract
        snapshot = {
            "timestamp": datetime.utcnow().isoformat(),
            "city_health": {
                "health_score": exec_kpis["city_health_score"],
                "operational_pressure": exec_kpis["operational_pressure"],
                "active_incidents": exec_kpis["active_incidents"],
                "avg_gori_score": exec_kpis["avg_gori_score"],
                "dispatch_pressure": exec_kpis["dispatch_pressure"],
            },
            "congestion": {
                "severity_distribution": cong_metrics["severity_distribution"],
                "hotspot_density": cong_metrics["hotspot_density"],
                "average_congestion_score": cong_metrics["average_congestion_score"],
                "corridor_rankings": self.congestion.build_corridor_rankings(
                    current_df
                ),
                "escalation_frequency": cong_metrics["escalation_frequency"],
            },
            "response_efficiency": {
                "p50_clearance_mins": resp_metrics["p50"],
                "p90_clearance_mins": resp_metrics["p90"],
                "p95_clearance_mins": resp_metrics["p95"],
                "tail_latency_mins": resp_metrics["tail_latency_mins"],
                "sla_breach_rate": resp_metrics["sla_breach_rate"],
                "zone_efficiency": {},  # Placeholder
            },
            "trends": {
                "rolling_anomaly_detected": trend_metrics["surge_detected"],
                "surge_detected": trend_metrics["surge_detected"],
                "degradation_trend_score": trend_metrics.get(
                    "degradation_trend_score", 0.0
                ),
                "hourly_trends": [],  # Placeholder
            },
        }

        # Validate via contract before returning
        validated_snapshot = OperationalSnapshotContract(**snapshot)
        return validated_snapshot.dict()
