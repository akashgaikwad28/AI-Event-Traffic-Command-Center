from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.v1.schemas.congestion import CongestionCreate
from backend.app.db.models.congestion import Congestion
from backend.app.db.repositories.congestion_repo import congestion_repo


class CongestionService:
    async def create_prediction(
        self, db: AsyncSession, obj_in: CongestionCreate
    ) -> Congestion:
        return await congestion_repo.create(db, obj_in=obj_in.model_dump())

    async def list_predictions(
        self, db: AsyncSession, page: int = 1, page_size: int = 20
    ) -> tuple[list[Congestion], int]:
        skip = (page - 1) * page_size
        items, total = await congestion_repo.get_multi(db, skip=skip, limit=page_size)
        return items, total


congestion_service = CongestionService()
