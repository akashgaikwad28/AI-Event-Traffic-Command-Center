from backend.app.resource_optimization.contracts.optimization_contracts import (
    OptimizationRequestDTO,
)


class RecommendationExplainer:
    """
    Generates human-readable operational reasoning for command center dashboards.
    """

    def generate_explanation(
        self,
        request: OptimizationRequestDTO,
        allocated_officers: int,
        is_diverted: bool,
    ) -> list[str]:
        explanations = []

        if request.gori_score > 80:
            explanations.append(
                f"GORI score is Critical ({request.gori_score}), triggering maximum operational escalation."
            )

        if request.hotspot_recurrence > 0.7:
            explanations.append(
                "Incident occurred in a highly recurrent hotspot; deploying preemptive perimeter control."
            )

        if request.is_rush_hour:
            explanations.append(
                "Rush hour timing detected; cascading congestion probability heavily weighted."
            )

        if request.heavy_vehicle_involved:
            explanations.append(
                "Heavy vehicle involvement increases expected clearance duration, requiring specialized tow dispatch."
            )

        if is_diverted and request.requires_closure:
            explanations.append(
                "Road closure mandated dynamic graph rerouting to adjacent operational corridors."
            )

        if allocated_officers > 4:
            explanations.append(
                f"High risk profile mandated escalation to {allocated_officers} officers to contain spatial spread."
            )

        return explanations
