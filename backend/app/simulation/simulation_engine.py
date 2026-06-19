from typing import Any

# In a real setup, we would inject these engines.
# We'll use mock responses representing the output of the Optimization Engine.
from backend.app.resource_optimization.resource_engine import ResourceOptimizationEngine
from backend.app.simulation.congestion_spread_simulator import CongestionSpreadSimulator
from backend.app.simulation.impact_estimator import ImpactEstimator
from backend.app.simulation.intervention_simulator import InterventionSimulator
from backend.app.simulation.scenario_builder import ScenarioBuilder
from backend.app.simulation.simulation_constants import (
    ScenarioType,
)
from backend.app.simulation.simulation_models import SimulationResult, SimulationState


class SimulationEngine:
    """Orchestrates the entire simulation process calling other engines."""

    def __init__(self):
        self.builder = ScenarioBuilder()
        self.spread_simulator = CongestionSpreadSimulator()
        self.intervention_simulator = InterventionSimulator()
        self.impact_estimator = ImpactEstimator()
        self.resource_engine = ResourceOptimizationEngine()

    def run_simulation(
        self, scenario_type: ScenarioType, params: dict[str, Any] = None
    ) -> SimulationResult:
        scenario_id = (
            f"sim_{scenario_type.value.lower()}_{len(params) if params else 0}"
        )

        # 1. Build Base Scenario
        base_state = self.builder.build_scenario(scenario_type, params)

        # 2. Simulate Baseline (No interventions)
        baseline_frames = self.spread_simulator.simulate_baseline(base_state)

        baseline_final = baseline_frames[-1]
        baseline_sim_state = SimulationState(
            timeline_frames=baseline_frames,
            final_gori=baseline_final.gori_score,
            estimated_clearance_mins=base_state["base_response_time"],
            total_congestion_radius=baseline_final.congestion_radius,
            cascading_risk_level=baseline_final.cascading_risk,
        )

        # 3. Call Resource Optimization Engine
        # We mock a dataframe and list of incidents/hotspots based on base_state
        # For the hackathon, we assume the resource engine gives us a playbook
        optimization_plan = (
            self.resource_engine.generate_playbook(
                scenario_id=scenario_id,
                gori=base_state["initial_gori"],
                severity="high" if base_state["initial_gori"] > 60 else "medium",
            )
            if hasattr(self.resource_engine, "generate_playbook")
            else {"deployments": [], "diversions": []}
        )

        # Format recommendations from the optimization plan
        recommendations = [
            {
                "type": "unit",
                "location": {"lat": 40.7130, "lng": -74.0050},
                "description": "Deploy rapid response unit",
            },
            {
                "type": "diversion",
                "location": {"lat": 40.7140, "lng": -74.0040},
                "description": "Divert NB traffic",
            },
        ]
        if "deployments" in optimization_plan:
            recommendations = optimization_plan["deployments"] + optimization_plan.get(
                "diversions", []
            )

        # 4. Simulate Interventions
        optimized_frames = self.intervention_simulator.simulate_optimized(
            base_state, recommendations
        )

        optimized_final = optimized_frames[-1]
        opt_clearance = max(
            10.0, base_state["base_response_time"] * 0.5
        )  # cut time by half

        optimized_sim_state = SimulationState(
            timeline_frames=optimized_frames,
            final_gori=optimized_final.gori_score,
            estimated_clearance_mins=opt_clearance,
            total_congestion_radius=optimized_final.congestion_radius,
            cascading_risk_level=optimized_final.cascading_risk,
        )

        # 5. Estimate Impact
        improvements = self.impact_estimator.estimate_impact(
            baseline_sim_state, optimized_sim_state
        )

        return SimulationResult(
            scenario_id=scenario_id,
            scenario_type=scenario_type.value,
            baseline_state=baseline_sim_state,
            optimized_state=optimized_sim_state,
            improvements=improvements,
            confidence=0.88,
            recommendations=recommendations,
        )
