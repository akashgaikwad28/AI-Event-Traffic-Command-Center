from datetime import datetime
from typing import Any

from pydantic import Field

from backend.app.api.v1.schemas.base import BaseSchema, IDModelMixin, TimestampMixin
from backend.app.core.constants import EventSeverity, EventStatus


class EventBase(BaseSchema):
    event_type: str = Field(..., min_length=1)
    event_category: str = Field(..., min_length=1)
    description: str | None = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    junction_name: str | None = None
    zone_name: str | None = None
    severity: EventSeverity
    status: EventStatus
    road_closure: bool = False
    start_time: datetime
    end_time: datetime | None = None
    resolved_at: datetime | None = None
    police_station: str | None = None
    assigned_officer_count: int = Field(default=0, ge=0)
    metadata_info: dict[str, Any] | None = None


class EventCreate(EventBase):
    pass


class EventUpdate(BaseSchema):
    event_type: str | None = None
    event_category: str | None = None
    description: str | None = None
    severity: EventSeverity | None = None
    status: EventStatus | None = None
    road_closure: bool | None = None
    end_time: datetime | None = None
    resolved_at: datetime | None = None
    assigned_officer_count: int | None = None
    metadata_info: dict[str, Any] | None = None


class EventResponse(EventBase, IDModelMixin, TimestampMixin):
    pass
