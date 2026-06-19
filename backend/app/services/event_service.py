import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.v1.schemas.event import EventCreate
from backend.app.db.models.event import Event
from backend.app.db.repositories.event_repo import event_repo
from backend.app.exceptions.api_exceptions import EventNotFound


class EventService:
    async def create_event(self, db: AsyncSession, obj_in: EventCreate) -> Event:
        return await event_repo.create(db, obj_in=obj_in.model_dump())

    async def get_event(self, db: AsyncSession, id: uuid.UUID) -> Event:
        event = await event_repo.get_by_id(db, id)
        if not event:
            raise EventNotFound()
        return event

    async def list_events(
        self, db: AsyncSession, page: int = 1, page_size: int = 20
    ) -> tuple[list[Event], int]:
        skip = (page - 1) * page_size
        items, total = await event_repo.get_multi(db, skip=skip, limit=page_size)
        return items, total


event_service = EventService()
