import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base
from backend.app.db.mixins.timestamp import TimestampMixin

if TYPE_CHECKING:
    from backend.app.db.models.event import Event


class PoliceDeployment(Base, TimestampMixin):
    __tablename__ = "police_deployments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("events.id"), index=True)
    police_station: Mapped[str] = mapped_column(String, index=True)
    officer_count: Mapped[int] = mapped_column(Integer)
    barricade_count: Mapped[int] = mapped_column(Integer, default=0)
    deployment_status: Mapped[str] = mapped_column(String)
    deployed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    event: Mapped["Event"] = relationship("Event", back_populates="police_deployments")
