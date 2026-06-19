from typing import Any

from pydantic import BaseModel, Field, ConfigDict


class PredictionRequest(BaseModel):
    """External API Schema for Inference Requests."""

    model_config = ConfigDict(frozen=True)
    latitude: float = Field(..., description="Incident coordinate latitude")
    longitude: float = Field(..., description="Incident coordinate longitude")
    priority: str = Field("Medium", description="Incident operational priority")
    requires_road_closure: bool = Field(
        False, description="Does the incident close the road?"
    )
    timestamp: str | None = Field(None, description="ISO8601 timestamp")


class GoriBreakdown(BaseModel):
    model_config = ConfigDict(frozen=True)
    congestion_risk: int
    clearance_duration: int
    rush_hour_stress: int
    deployment_pressure: int
    cascading_spread_risk: int


class GoriResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    gori_score: int
    severity_tier: str
    alert_color: str
    breakdown: GoriBreakdown


class OperationalPredictions(BaseModel):
    model_config = ConfigDict(frozen=True)
    clearance_minutes: float
    congestion_proxy_score: float
    deployment_load: str


class TrustScore(BaseModel):
    model_config = ConfigDict(frozen=True)
    reliability_score: int
    tier: str


class PredictionResponse(BaseModel):
    """External API Schema for Inference Responses."""

    model_config = ConfigDict(frozen=True)
    success: bool = True
    gori: GoriResponse
    predictions: OperationalPredictions
    trust: TrustScore
    recommendations: list[str]
    explainability: dict[str, Any]
