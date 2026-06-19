from typing import Any

from pydantic import BaseModel, ConfigDict


class CongestionSummaryContract(BaseModel):
    model_config = ConfigDict(frozen=True)
    severity_distribution: dict[str, float]
    hotspot_density: float
    average_congestion_score: float
    corridor_rankings: list[dict[str, Any]]
    escalation_frequency: float


class ResponseMetricsContract(BaseModel):
    model_config = ConfigDict(frozen=True)
    p50_clearance_mins: float
    p90_clearance_mins: float
    p95_clearance_mins: float
    tail_latency_mins: float
    sla_breach_rate: float
    zone_efficiency: dict[str, float]


class TrendSummaryContract(BaseModel):
    model_config = ConfigDict(frozen=True)
    rolling_anomaly_detected: bool
    surge_detected: bool
    degradation_trend_score: float
    hourly_trends: list[dict[str, Any]]


class CityHealthMetricsContract(BaseModel):
    model_config = ConfigDict(frozen=True)
    health_score: float
    operational_pressure: float
    active_incidents: int
    avg_gori_score: float
    dispatch_pressure: str


class OperationalSnapshotContract(BaseModel):
    model_config = ConfigDict(frozen=True)
    timestamp: str
    city_health: CityHealthMetricsContract
    congestion: CongestionSummaryContract
    response_efficiency: ResponseMetricsContract
    trends: TrendSummaryContract
