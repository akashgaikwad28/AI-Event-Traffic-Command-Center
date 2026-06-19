from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from backend.app.core.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


class PaginationQuery(BaseModel):
    model_config = ConfigDict(frozen=True)
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(
        DEFAULT_PAGE_SIZE,
        ge=1,
        le=MAX_PAGE_SIZE,
        description="Number of items per page",
    )


class TimeRangeQuery(BaseModel):
    model_config = ConfigDict(frozen=True)
    start_time: datetime | None = Field(None, description="Filter from start time")
    end_time: datetime | None = Field(None, description="Filter to end time")


class EventFilterQuery(BaseModel):
    model_config = ConfigDict(frozen=True)
    event_type: str | None = Field(None, description="Filter by event type")
    severity: str | None = Field(None, description="Filter by severity level")
    status: str | None = Field(None, description="Filter by event status")
    zone_name: str | None = Field(None, description="Filter by zone name")
