from typing import Any

from backend.app.resource_optimization.contracts.optimization_contracts import (
    OptimizationRequestDTO,
)


class CascadeSimulator:
    """
    Simulates catastrophic operational failure paths.
    Predicts which adjacent clusters fail if the incident is unhandled.
    """

    def simulate_failure_cascade(
        self, request: OptimizationRequestDTO
    ) -> dict[str, Any]:
        """
        Calculates impact if incident is not resolved within 60 minutes.
        """
        # Baseline probability based on historical recurrence and GORI
        cascade_probability = min(
            0.99,
            (request.gori_score / 100) * 0.5
            + (request.historical_spread_probability * 0.5),
        )

        at_risk_clusters = []
        if cascade_probability > 0.6:
            at_risk_clusters.append("Upstream Corridor Alpha")
            if request.is_rush_hour:
                at_risk_clusters.append("Adjacent Arterial Node 4")

        return {
            "cascading_failure_probability": round(cascade_probability * 100, 1),
            "critical_time_to_failure_mins": 45 if request.is_rush_hour else 90,
            "at_risk_clusters": at_risk_clusters,
        }
