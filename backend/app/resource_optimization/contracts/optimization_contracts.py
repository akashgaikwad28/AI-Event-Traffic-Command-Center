from typing import Any

from pydantic import BaseModel, ConfigDict


class OperationalConstraintsContract(BaseModel):
    model_config = ConfigDict(frozen=True)
    max_available_officers: int = 50
    active_deployed_officers: int = 0
    max_barricades: int = 100
    active_barricades: int = 0
    restricted_zones: list[str] = []
    response_capacity_percentage: float = 100.0


class OptimizationRequestDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    incident_id: str
    latitude: float
    longitude: float
    gori_score: float
    congestion_severity: str
    requires_closure: bool
    heavy_vehicle_involved: bool
    is_rush_hour: bool
    hotspot_recurrence: float
    historical_spread_probability: float
    # Optional taxonomy metadata (PLANNED / UNPLANNED + subtype). Passed through
    # by the demo panel so the Post-Event Learning loop can split accuracy.
    scenario_category: str | None = None
    scenario_subtype: str | None = None


class SimulationResultDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    scenario: str
    estimated_clearance_minutes: int
    congestion_reduction: int
    spread_risk: str
    confidence: float


class OperationalPlanDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    plan_id: str
    gori_score: float
    operational_risk: str
    recommended_plan: str
    resource_plan: dict[str, Any]
    diversion_plan: dict[str, Any]
    predicted_impact: dict[str, SimulationResultDTO]
    confidence: float
    recommended_actions: list[str]
    explainability: list[str]
