from pydantic import Field

from backend.app.api.v1.schemas.base import BaseSchema
from backend.app.core.constants import CongestionLevel


class CongestionPredictionRequest(BaseSchema):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_km: float = Field(5.0, gt=0, le=50.0)
    future_minutes: int = Field(60, gt=0, le=1440)


class CongestionPredictionResponse(BaseSchema):
    predicted_level: CongestionLevel
    probability: float = Field(..., ge=0.0, le=1.0)
    expected_delay_minutes: int = Field(0, ge=0)
    affected_routes: list[str] = Field(default_factory=list)
