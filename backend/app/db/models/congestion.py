import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base
from backend.app.db.mixins.timestamp import TimestampMixin

if TYPE_CHECKING:
    from backend.app.db.models.event import Event


class Congestion(Base, TimestampMixin):
    __tablename__ = "congestions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    event_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("events.id"), index=True)
    congestion_score: Mapped[float] = mapped_column(Float)
    predicted_delay_minutes: Mapped[int] = mapped_column(Integer)
    impact_radius_km: Mapped[float] = mapped_column(Float)
    affected_routes: Mapped[list[str]] = mapped_column(ARRAY(String))
    congestion_level: Mapped[str] = mapped_column(String)

    event: Mapped["Event"] = relationship("Event", back_populates="congestions")
