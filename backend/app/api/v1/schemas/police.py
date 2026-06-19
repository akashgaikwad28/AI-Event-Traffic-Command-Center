from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PoliceDeploymentBase(BaseModel):
    model_config = ConfigDict(frozen=True)
    event_id: UUID
    police_station: str = Field(..., min_length=1)
    officer_count: int = Field(..., gt=0)
    barricade_count: int = Field(default=0, ge=0)
    deployment_status: str = Field(..., min_length=1)
    deployed_at: datetime
    resolved_at: datetime | None = None


class PoliceDeploymentCreate(PoliceDeploymentBase):
    pass


class PoliceDeploymentResponse(PoliceDeploymentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, frozen=True)
