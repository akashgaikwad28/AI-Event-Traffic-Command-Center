from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CongestionBase(BaseModel):
    model_config = ConfigDict(frozen=True)
    event_id: UUID
    congestion_score: float = Field(..., ge=0.0, le=1.0)
    predicted_delay_minutes: int = Field(..., ge=0)
    impact_radius_km: float = Field(..., ge=0.0)
    affected_routes: list[str] = Field(default_factory=list)
    congestion_level: str = Field(..., min_length=1)


class CongestionCreate(CongestionBase):
    pass


class CongestionResponse(CongestionBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, frozen=True)
