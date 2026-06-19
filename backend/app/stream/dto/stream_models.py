from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class StreamEvent(BaseModel):
    model_config = ConfigDict(frozen=True)
    event_id: str
    event_type: str  # INCIDENT_CREATED, HOTSPOT_DETECTED, GORI_ALERT
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    priority_level: int = 0  # 0: Low, 1: Medium, 2: High, 3: Critical
    payload: dict[str, Any]


class LiveAlert(BaseModel):
    model_config = ConfigDict(frozen=True)
    alert_id: str
    severity: str  # INFO, WARNING, HIGH, CRITICAL
    color_code: str  # Frontend-ready color (#FF0000, etc.)
    message: str
    recommendation: str | None = None
    geo_context: dict[str, float] | None = None
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class DashboardSnapshot(BaseModel):
    model_config = ConfigDict(frozen=True)
    active_incidents: int
    top_hotspots: list[dict[str, Any]]
    avg_gori: float
    deployment_pressure: str
    critical_alerts: list[LiveAlert]
