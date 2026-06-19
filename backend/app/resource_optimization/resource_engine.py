import uuid
from typing import Any

from backend.app.resource_optimization.barricade_optimizer import BarricadeOptimizer
from backend.app.resource_optimization.constraints_engine import ConstraintsEngine
from backend.app.resource_optimization.contracts.optimization_contracts import (
    OperationalPlanDTO,
    OptimizationRequestDTO,
)
from backend.app.resource_optimization.diversion_engine import DiversionEngine
from backend.app.resource_optimization.explainability.recommendation_explainer import (
    RecommendationExplainer,
)
from backend.app.resource_optimization.operational_simulator import OperationalSimulator
from backend.app.resource_optimization.playbooks.incident_playbooks import (
    IncidentPlaybookEngine,
)
from backend.app.resource_optimization.police_allocator import PoliceAllocator
from backend.app.resource_optimization.scoring.operational_efficiency_score import (
    compute_efficiency_score,
)
from backend.app.resource_optimization.simulation.cascade_simulator import (
    CascadeSimulator,
)


class ResourceOptimizationEngine:
    """
    The Operational Brain.
    Orchestrates AI predictions, constraints, diversion routing, and scenario simulation.
    """

    def __init__(self):
        self.allocator = PoliceAllocator()
        self.barricades = BarricadeOptimizer(strategy_mode="BALANCED_RESPONSE")
        self.diversion = DiversionEngine()
        self.simulator = OperationalSimulator()
        self.cascade = CascadeSimulator()
        self.playbooks = IncidentPlaybookEngine()
        self.explainer = RecommendationExplainer()
        self.constraints = ConstraintsEngine()

    def generate_operational_plan(self, payload: dict[str, Any]) -> OperationalPlanDTO:
        # 1. Map to strict contract
        request = OptimizationRequestDTO(**payload)

        # 2. Allocate Resources
        officer_plan = self.allocator.allocate_officers(request)
        barricade_plan = self.barricades.optimize_placement(request)

        # 3. Apply Constraints (Enterprise Realism)
        validated_resources = self.constraints.validate_deployment(
            requested_officers=officer_plan["recommended_officers"],
            requested_barricades=barricade_plan["barricades_required"],
        )

        # 4. Graph Rerouting
        diversion_plan = self.diversion.generate_diversion_plan(
            "North_Arterial", request.gori_score
        )  # Mock corridor

        # 5. Playbook Engine
        playbook = self.playbooks.fetch_playbook(request)

        # 6. What-If Simulation
        # Simulate based on validated constraints, not just requested
        simulations = self.simulator.simulate_plan(
            plan_name=playbook["playbook_name"],
            baseline_clearance=90,  # From ML Inference Layer
            allocated_officers=validated_resources["allocated_officers"],
            diverted=diversion_plan["requires_diversion"],
        )

        # 7. Cascading Failure Simulation
        cascade_risk = self.cascade.simulate_failure_cascade(request)

        # 8. Operational Efficiency Score
        efficiency = compute_efficiency_score(
            officers_allocated=validated_resources["allocated_officers"],
            barricades_allocated=validated_resources["allocated_barricades"],
            congestion_reduction_pct=simulations["expected_case"].congestion_reduction,
            base_gori=request.gori_score,
        )

        # 9. Explainability
        explanations = self.explainer.generate_explanation(
            request,
            validated_resources["allocated_officers"],
            diversion_plan["requires_diversion"],
        )

        # 10. Assemble Command Center Plan
        resource_plan_dict = {
            "police_officers": validated_resources["allocated_officers"],
            "barricades": validated_resources["allocated_barricades"],
            "patrol_vehicles": validated_resources["allocated_officers"] // 2,
            "estimated_cost": validated_resources["allocated_officers"] * 150
            + validated_resources["allocated_barricades"] * 50,
            "shortage_warning": validated_resources["shortage_warning"],
            "closure_type": barricade_plan["closure_type"],
            "efficiency_metrics": efficiency,
        }

        return OperationalPlanDTO(
            plan_id=f"PLAN-{str(uuid.uuid4())[:8].upper()}",
            gori_score=request.gori_score,
            operational_risk=officer_plan["deployment_priority"],
            recommended_plan=playbook["playbook_name"],
            resource_plan=resource_plan_dict,
            diversion_plan=diversion_plan,
            predicted_impact=simulations,
            confidence=simulations["expected_case"].confidence,
            recommended_actions=playbook["predefined_actions"],
            explainability=explanations,
        )
