from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.v1.schemas.query import (
    EventFilterQuery,
    PaginationQuery,
    TimeRangeQuery,
)
from backend.app.core.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


async def get_db_session() -> AsyncSession:
    # A wrapper around get_db to be used directly in API routes
    # This keeps naming explicit and standard.
    # Yielding is handled by the get_db dependency.
    raise NotImplementedError("Use get_db directly")


def get_pagination_query(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(
        DEFAULT_PAGE_SIZE,
        ge=1,
        le=MAX_PAGE_SIZE,
        description="Number of items per page",
    ),
) -> PaginationQuery:
    return PaginationQuery(page=page, page_size=page_size)


def get_time_range_query(
    start_time: str | None = Query(None, description="Start time (ISO)"),
    end_time: str | None = Query(None, description="End time (ISO)"),
) -> TimeRangeQuery:
    # Optional parsing could be added here, but Pydantic handles ISO format
    # conversion if using datetime in query.
    # Using Pydantic class to parse directly is better, but this wrapper
    # can be used as Depends().
    return TimeRangeQuery(start_time=start_time, end_time=end_time)  # type: ignore


def get_event_filter_query(
    event_type: str | None = Query(None, description="Event type"),
    severity: str | None = Query(None, description="Severity"),
    status: str | None = Query(None, description="Status"),
    zone_name: str | None = Query(None, description="Zone name"),
) -> EventFilterQuery:
    return EventFilterQuery(
        event_type=event_type, severity=severity, status=status, zone_name=zone_name
    )
