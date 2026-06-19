from typing import Any

from pydantic import BaseModel, ConfigDict


class MapEntity(BaseModel):
    model_config = ConfigDict(frozen=True)
    id: str
    type: str  # "incident", "hotspot", "unit", "barricade", "diversion"
    lat: float
    lng: float
    radius: float | None = None
    metadata: dict[str, Any] = {}


class TimelineFrame(BaseModel):
    model_config = ConfigDict(frozen=True)
    time_offset_mins: int
    gori_score: float
    active_incidents: int
    congestion_radius: float
    map_entities: list[MapEntity]
    cascading_risk: str  # LOW, MEDIUM, HIGH, CRITICAL


class SimulationState(BaseModel):
    model_config = ConfigDict(frozen=True)
    timeline_frames: list[TimelineFrame]
    final_gori: float
    estimated_clearance_mins: float
    total_congestion_radius: float
    cascading_risk_level: str


class SimulationImprovements(BaseModel):
    model_config = ConfigDict(frozen=True)
    response_time_reduction_mins: float
    congestion_reduction_pct: float
    gori_reduction: float
    spread_reduction_radius: float
    officer_efficiency_gain_pct: float
    diversion_effectiveness_score: float
    estimated_citizens_impacted: int


class SimulationResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    scenario_id: str
    scenario_type: str
    baseline_state: SimulationState
    optimized_state: SimulationState
    improvements: SimulationImprovements
    confidence: float
    recommendations: list[dict[str, Any]]
