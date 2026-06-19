from typing import Any

from backend.app.resource_optimization.contracts.optimization_contracts import (
    OptimizationRequestDTO,
)


class BarricadeOptimizer:
    """
    Road closure and perimeter control intelligence.
    Supports operational strategies.
    """

    def __init__(self, strategy_mode: str = "BALANCED_RESPONSE"):
        # Modes: MINIMAL_DISRUPTION, AGGRESSIVE_CONTAINMENT, BALANCED_RESPONSE
        self.strategy_mode = strategy_mode

    def optimize_placement(self, request: OptimizationRequestDTO) -> dict[str, Any]:
        """Recommends barricade configurations based on GORI and strategy."""

        if not request.requires_closure:
            return {
                "barricades_required": 0,
                "strategy": "No closure required",
                "closure_type": "NONE",
            }

        base_barricades = 5
        closure_type = "PARTIAL"

        if request.gori_score > 75 or self.strategy_mode == "AGGRESSIVE_CONTAINMENT":
            base_barricades += 15
            closure_type = "FULL_PERIMETER"
        elif self.strategy_mode == "MINIMAL_DISRUPTION":
            base_barricades -= 2
            closure_type = "LANE_RESTRICTION"
        else:  # BALANCED
            base_barricades += 5

        if request.historical_spread_probability > 0.6:
            base_barricades += 10  # Expand perimeter

        return {
            "barricades_required": max(0, base_barricades),
            "closure_type": closure_type,
            "strategy_applied": self.strategy_mode,
        }
