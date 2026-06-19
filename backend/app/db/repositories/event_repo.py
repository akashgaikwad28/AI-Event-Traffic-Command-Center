from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.models.event import Event
from backend.app.db.repositories.base_repository import BaseRepository


class EventRepository(BaseRepository[Event]):
    def __init__(self) -> None:
        super().__init__(Event)

    async def get_active_events(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> tuple[list[Event], int]:
        query = (
            select(self.model)
            .where(self.model.status == "active")
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        items = list(result.scalars().all())

        count_query = (
            select(func.count())
            .select_from(self.model)
            .where(self.model.status == "active")
        )
        total = (await db.execute(count_query)).scalar_one()
        return items, total

    async def get_by_zone(
        self, db: AsyncSession, zone_name: str, skip: int = 0, limit: int = 100
    ) -> tuple[list[Event], int]:
        query = (
            select(self.model)
            .where(self.model.zone_name == zone_name)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        items = list(result.scalars().all())

        count_query = (
            select(func.count())
            .select_from(self.model)
            .where(self.model.zone_name == zone_name)
        )
        total = (await db.execute(count_query)).scalar_one()
        return items, total

    async def get_by_severity(
        self, db: AsyncSession, severity: str, skip: int = 0, limit: int = 100
    ) -> tuple[list[Event], int]:
        query = (
            select(self.model)
            .where(self.model.severity == severity)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        items = list(result.scalars().all())

        count_query = (
            select(func.count())
            .select_from(self.model)
            .where(self.model.severity == severity)
        )
        total = (await db.execute(count_query)).scalar_one()
        return items, total


event_repo = EventRepository()
