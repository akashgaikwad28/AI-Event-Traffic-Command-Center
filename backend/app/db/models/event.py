import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import JSON, Boolean, DateTime, Float, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base
from backend.app.db.mixins.timestamp import TimestampMixin

if TYPE_CHECKING:
    from backend.app.db.models.congestion import Congestion
    from backend.app.db.models.police_deployment import PoliceDeployment


class Event(Base, TimestampMixin):
    __tablename__ = "events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    event_type: Mapped[str] = mapped_column(String, index=True)
    event_category: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str | None] = mapped_column(String)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    junction_name: Mapped[str | None] = mapped_column(String)
    zone_name: Mapped[str | None] = mapped_column(String, index=True)
    severity: Mapped[str] = mapped_column(String, index=True)
    status: Mapped[str] = mapped_column(String, index=True)
    road_closure: Mapped[bool] = mapped_column(Boolean, default=False)
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    police_station: Mapped[str | None] = mapped_column(String)
    assigned_officer_count: Mapped[int] = mapped_column(Integer, default=0)
    metadata_info: Mapped[dict[str, Any] | None] = mapped_column(JSON)

    congestions: Mapped[list["Congestion"]] = relationship(
        "Congestion", back_populates="event", cascade="all, delete-orphan"
    )
    police_deployments: Mapped[list["PoliceDeployment"]] = relationship(
        "PoliceDeployment", back_populates="event", cascade="all, delete-orphan"
    )
