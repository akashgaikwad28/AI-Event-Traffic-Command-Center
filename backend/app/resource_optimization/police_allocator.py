from typing import Any

from backend.app.resource_optimization.contracts.optimization_contracts import (
    OptimizationRequestDTO,
)


class PoliceAllocator:
    """
    AI-assisted officer deployment optimization.
    Risk-aware allocation combining GORI, hotspots, and temporal stress.
    """

    def allocate_officers(self, request: OptimizationRequestDTO) -> dict[str, Any]:
        base_officers = 1

        # ML / Severity integration
        if request.gori_score > 80:
            base_officers += 4
        elif request.gori_score > 50:
            base_officers += 2

        # Geo / Temporal Heuristics
        if request.hotspot_recurrence > 0.6:
            base_officers += 1

        if request.heavy_vehicle_involved:
            base_officers += 2

        if request.is_rush_hour:
            base_officers += 1

        priority = (
            "CRITICAL"
            if base_officers >= 5
            else ("ELEVATED" if base_officers >= 3 else "STANDARD")
        )

        return {
            "recommended_officers": min(10, base_officers),  # Hard cap heuristic
            "deployment_priority": priority,
            "mobile_patrol_allocation": (
                2 if request.historical_spread_probability > 0.5 else 0
            ),
        }
