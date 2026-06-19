from typing import Any

from backend.app.simulation.simulation_constants import ScenarioType
from backend.app.simulation.simulation_engine import SimulationEngine
from backend.app.simulation.simulation_models import SimulationResult


class SimulationService:
    """Service layer to interact with simulation engine and maintain history."""

    def __init__(self):
        self.engine = SimulationEngine()
        self.history: list[SimulationResult] = []
        self.MAX_HISTORY = 10

    def _add_to_history(self, result: SimulationResult):
        self.history.append(result)
        if len(self.history) > self.MAX_HISTORY:
            self.history.pop(0)

    def run_scenario(
        self, scenario_type: ScenarioType, params: dict[str, Any] = None
    ) -> SimulationResult:
        result = self.engine.run_simulation(scenario_type, params)
        self._add_to_history(result)
        return result

    def get_history(self) -> list[SimulationResult]:
        return list(reversed(self.history))

    def get_scenarios(self) -> list[dict[str, str]]:
        return [
            {"id": ScenarioType.ACCIDENT_CASCADE.value, "name": "Accident Cascade"},
            {
                "id": ScenarioType.STADIUM_EVENT_EGRESS.value,
                "name": "Stadium Event Egress",
            },
            {"id": ScenarioType.CUSTOM_INCIDENT.value, "name": "Custom Incident"},
        ]


# Singleton service
simulation_service = SimulationService()
