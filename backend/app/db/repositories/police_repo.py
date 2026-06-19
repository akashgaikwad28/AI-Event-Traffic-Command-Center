from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.db.models.police_deployment import PoliceDeployment
from backend.app.db.repositories.base_repository import BaseRepository


class PoliceDeploymentRepository(BaseRepository[PoliceDeployment]):
    def __init__(self) -> None:
        super().__init__(PoliceDeployment)

    async def get_active_deployments(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[PoliceDeployment]:
        query = (
            select(self.model)
            .where(self.model.deployment_status == "active")
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())

    async def get_by_station(
        self, db: AsyncSession, station: str, skip: int = 0, limit: int = 100
    ) -> list[PoliceDeployment]:
        query = (
            select(self.model)
            .where(self.model.police_station == station)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())


police_repo = PoliceDeploymentRepository()
