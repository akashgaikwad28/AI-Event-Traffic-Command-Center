from typing import Any

import pandas as pd

from backend.app.analytics.scoring.city_health_score import (
    compute_city_health,
    compute_operational_pressure,
)


class OperationalKPIEngine:
    """
    Executive-level KPIs for Command Center Dashboards.
    """

    def generate_executive_kpis(
        self, df: pd.DataFrame, avg_gori: float = 0.0, sla_breach: float = 0.0
    ) -> dict[str, Any]:
        """Generates the high-level operational snapshot."""
        if df.empty:
            return self._empty_kpis()

        total_incidents = len(df)
        high_priority = (
            len(df[df["priority"] == "High"]) if "priority" in df.columns else 0
        )

        health_score = compute_city_health(total_incidents, avg_gori, sla_breach)
        pressure_score = compute_operational_pressure(total_incidents, high_priority)

        return {
            "city_health_score": health_score,
            "operational_pressure": pressure_score,
            "active_incidents": total_incidents,
            "high_priority_incidents": high_priority,
            "avg_gori_score": round(avg_gori, 1),
            "dispatch_pressure": (
                "CRITICAL"
                if pressure_score > 80
                else ("HIGH" if pressure_score > 60 else "NORMAL")
            ),
        }

    def _empty_kpis(self) -> dict[str, Any]:
        return {
            "city_health_score": 100.0,
            "operational_pressure": 0.0,
            "active_incidents": 0,
            "high_priority_incidents": 0,
            "avg_gori_score": 0.0,
            "dispatch_pressure": "NORMAL",
        }
