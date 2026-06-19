from backend.app.simulation.simulation_models import (
    SimulationImprovements,
    SimulationState,
)


class ImpactEstimator:
    """Calculates the business value and impact improvements between baseline and optimized states."""

    def estimate_impact(
        self, baseline: SimulationState, optimized: SimulationState
    ) -> SimulationImprovements:
        # Time reduction
        resp_reduction = max(
            0.0, baseline.estimated_clearance_mins - optimized.estimated_clearance_mins
        )

        # Congestion reduction pct
        base_radius = baseline.total_congestion_radius
        opt_radius = optimized.total_congestion_radius
        cong_reduction = (
            ((base_radius - opt_radius) / base_radius * 100.0)
            if base_radius > 0
            else 0.0
        )

        # GORI reduction
        gori_red = max(0.0, baseline.final_gori - optimized.final_gori)

        # Spread reduction radius
        spread_red = max(0.0, base_radius - opt_radius)

        # Derived efficiency and impact
        officer_eff = min(100.0, gori_red * 1.5)
        diversion_eff = min(100.0, cong_reduction * 1.2)
        citizens_impacted = int((spread_red * 10) + (resp_reduction * 50))

        return SimulationImprovements(
            response_time_reduction_mins=round(resp_reduction, 1),
            congestion_reduction_pct=round(cong_reduction, 1),
            gori_reduction=round(gori_red, 1),
            spread_reduction_radius=round(spread_red, 1),
            officer_efficiency_gain_pct=round(officer_eff, 1),
            diversion_effectiveness_score=round(diversion_eff, 1),
            estimated_citizens_impacted=citizens_impacted,
        )
