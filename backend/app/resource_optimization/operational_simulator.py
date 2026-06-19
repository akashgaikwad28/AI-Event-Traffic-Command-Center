from backend.app.resource_optimization.contracts.optimization_contracts import (
    SimulationResultDTO,
)


class OperationalSimulator:
    """
    What-if analysis engine.
    Evaluates deployment plans across Best, Expected, and Worst case scenarios.
    """

    def simulate_plan(
        self,
        plan_name: str,
        baseline_clearance: int,
        allocated_officers: int,
        diverted: bool,
    ) -> dict[str, SimulationResultDTO]:

        # Heuristics for expected impact
        officer_impact = allocated_officers * 3  # 3 mins saved per officer
        diversion_impact = 15 if diverted else 0

        expected_clearance = max(
            15, baseline_clearance - officer_impact - diversion_impact
        )

        # Best Case Scenario (Perfect Execution)
        best_clearance = max(10, int(expected_clearance * 0.8))
        best = SimulationResultDTO(
            scenario="BEST_CASE",
            estimated_clearance_minutes=best_clearance,
            congestion_reduction=min(
                100, (allocated_officers * 5) + (20 if diverted else 0) + 15
            ),
            spread_risk="NEGLIGIBLE",
            confidence=0.4,  # Less likely to be perfect
        )

        # Expected Case Scenario
        expected = SimulationResultDTO(
            scenario="EXPECTED_CASE",
            estimated_clearance_minutes=expected_clearance,
            congestion_reduction=min(
                100, (allocated_officers * 5) + (20 if diverted else 0)
            ),
            spread_risk="LOW" if allocated_officers > 3 else "MODERATE",
            confidence=0.85,
        )

        # Worst Case Scenario (Complications)
        worst_clearance = int(baseline_clearance * 1.2)  # Escalation
        worst = SimulationResultDTO(
            scenario="WORST_CASE",
            estimated_clearance_minutes=worst_clearance,
            congestion_reduction=10,  # Minimal gain
            spread_risk="HIGH",
            confidence=0.3,
        )

        return {"best_case": best, "expected_case": expected, "worst_case": worst}
