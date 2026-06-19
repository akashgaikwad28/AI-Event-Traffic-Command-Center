from typing import Any

from pydantic import BaseModel, ConfigDict


class CongestionAnalyticsDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    zone_id: str
    congestion_score: float
    severity: str
    active_incidents: int


class ResponseMetricsDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    corridor_id: str
    avg_clearance_mins: float
    p90_clearance_mins: float
    sla_breaches: int


class GeoRiskDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    latitude: float
    longitude: float
    risk_score: float
    cluster_id: str
    cascading_probability: float


class IncidentPatternDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    pattern_type: str
    frequency: int
    temporal_window: str
    recurrence_score: float


class OperationalSnapshotDTO(BaseModel):
    model_config = ConfigDict(frozen=True)
    snapshot_id: str
    generated_at: str
    city_health_score: float
    metrics: dict[str, Any]
