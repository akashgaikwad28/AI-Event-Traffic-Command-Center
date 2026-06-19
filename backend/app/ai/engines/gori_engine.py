from typing import Any


class GoriEngine:
    """
    GridWise Operational Risk Index (GORI) Engine.
    The unified severity intelligence layer synthesizing ML predictions and operational rules.
    """

    def calculate_gori(
        self,
        congestion_score: float,
        clearance_mins: float,
        deployment_class: str,
        is_rush_hour: bool,
        is_closed: bool,
    ) -> dict[str, Any]:
        """
        Calculates the GORI score (0-100) and provides a contribution breakdown.
        """
        # Base Component Calculations
        c_risk = min(30, int((congestion_score / 100) * 30))
        c_duration = min(25, int((clearance_mins / 120) * 25))

        c_rush = 15 if is_rush_hour else 0
        c_deploy = (
            15
            if "Heavy" in deployment_class or "Traffic Control" in deployment_class
            else 5
        )
        c_closure = 15 if is_closed else 0

        # Calculate Total Score
        gori_score = min(100, c_risk + c_duration + c_rush + c_deploy + c_closure)

        # Severity Tiers
        if gori_score <= 20:
            severity = "LOW"
            color = "GREEN"
        elif gori_score <= 40:
            severity = "MODERATE"
            color = "YELLOW"
        elif gori_score <= 60:
            severity = "ELEVATED"
            color = "ORANGE"
        elif gori_score <= 80:
            severity = "HIGH"
            color = "RED"
        else:
            severity = "CRITICAL"
            color = "DARK RED"

        return {
            "gori_score": gori_score,
            "severity_tier": severity,
            "alert_color": color,
            "breakdown": {
                "congestion_risk": c_risk,
                "clearance_duration": c_duration,
                "rush_hour_stress": c_rush,
                "deployment_pressure": c_deploy,
                "cascading_spread_risk": c_closure,
            },
        }
