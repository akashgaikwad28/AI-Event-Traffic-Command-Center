import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.dependencies import (
    get_event_filter_query,
    get_pagination_query,
    get_time_range_query,
)
from backend.app.api.v1.schemas.event import EventCreate, EventResponse, EventUpdate
from backend.app.api.v1.schemas.query import (
    EventFilterQuery,
    PaginationQuery,
    TimeRangeQuery,
)
from backend.app.db.session import get_db
from backend.app.services.event_service import event_service
from backend.app.utils.pagination import PaginatedResponse, paginate
from backend.app.utils.response import APIResponse, success_response

router = APIRouter()


@router.post("", response_model=APIResponse[EventResponse], status_code=201)
async def create_event(
    event_in: EventCreate, db: AsyncSession = Depends(get_db)
) -> APIResponse[EventResponse]:
    """Create a new event."""
    event = await event_service.create_event(db, event_in)
    return success_response(
        EventResponse.model_validate(event), message="Event created successfully"
    )


@router.get("", response_model=APIResponse[PaginatedResponse[EventResponse]])
async def list_events(
    pagination: PaginationQuery = Depends(get_pagination_query),
    filters: EventFilterQuery = Depends(get_event_filter_query),
    time_range: TimeRangeQuery = Depends(get_time_range_query),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[PaginatedResponse[EventResponse]]:
    """List events with pagination and filters."""
    # Here we would normally pass filters to the service.
    # For now, we pass page and page_size.
    items, total = await event_service.list_events(
        db, pagination.page, pagination.page_size
    )
    paginated = paginate(
        [EventResponse.model_validate(i) for i in items],
        total,
        pagination.page,
        pagination.page_size,
    )
    return success_response(paginated)


@router.get("/{event_id}", response_model=APIResponse[EventResponse])
async def get_event(
    event_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> APIResponse[EventResponse]:
    """Get a single event by ID."""
    event = await event_service.get_event(db, event_id)
    return success_response(EventResponse.model_validate(event))


@router.patch("/{event_id}", response_model=APIResponse[EventResponse])
async def update_event(
    event_id: uuid.UUID, event_in: EventUpdate, db: AsyncSession = Depends(get_db)
) -> APIResponse[EventResponse]:
    """Update an existing event."""
    # This requires event_service.update_event which we will ensure exists
    # later or assume exists.
    # event = await event_service.update_event(db, event_id, event_in)
    # return success_response(
    #     EventResponse.model_validate(event),
    #     message="Event updated successfully"
    # )
    raise NotImplementedError("Update not fully implemented in service yet")


@router.delete("/{event_id}", response_model=APIResponse[dict[str, str]])
async def delete_event(
    event_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> APIResponse[dict[str, str]]:
    """Delete an event."""
    # await event_service.delete_event(db, event_id)
    # return success_response(
    #     {"id": str(event_id)}, message="Event deleted successfully"
    # )
    raise NotImplementedError("Delete not fully implemented in service yet")
