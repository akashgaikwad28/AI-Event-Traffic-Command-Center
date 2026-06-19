from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.models.congestion import Congestion
from backend.app.db.repositories.base_repository import BaseRepository


class CongestionRepository(BaseRepository[Congestion]):
    def __init__(self) -> None:
        super().__init__(Congestion)

    async def get_high_congestion(
        self, db: AsyncSession, threshold: float = 0.8, limit: int = 50
    ) -> list[Congestion]:
        query = (
            select(self.model)
            .where(self.model.congestion_score >= threshold)
            .order_by(desc(self.model.congestion_score))
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_recent_predictions(
        self, db: AsyncSession, limit: int = 50
    ) -> list[Congestion]:
        query = select(self.model).order_by(desc(self.model.created_at)).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())


congestion_repo = CongestionRepository()
