from pydantic import Field

from backend.app.api.v1.schemas.base import BaseSchema
from backend.app.core.constants import EventSeverity


class AnalyticsSummaryResponse(BaseSchema):
    total_events: int = Field(
        0, description="Total number of events in the given period"
    )
    active_events: int = Field(0, description="Number of currently active events")
    critical_events: int = Field(0, description="Number of critical events")
    average_resolution_time_minutes: float = Field(
        0.0, description="Average time to resolve events"
    )
    top_congested_zones: list[str] = Field(
        default_factory=list, description="Zones with highest congestion"
    )


class EventDistributionResponse(BaseSchema):
    by_severity: dict[EventSeverity, int] = Field(default_factory=dict)
    by_status: dict[str, int] = Field(default_factory=dict)
    by_type: dict[str, int] = Field(default_factory=dict)
