from pydantic import BaseModel, Field, ConfigDict


class Coordinate(BaseModel):
    model_config = ConfigDict(frozen=True)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)


class GeoPoint(Coordinate):
    id: str | None = None
    weight: float = 1.0


class HotspotResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    latitude: float
    longitude: float
    radius_km: float
    risk_score: float
    confidence_score: float
    event_count: int
    event_ids: list[str]


class RouteImpactResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    event_id: str
    latitude: float
    longitude: float
    impact_radius_km: float
    severity_level: str
    affected_zones: list[str] = Field(default_factory=list)


class NearbyEventResult(BaseModel):
    model_config = ConfigDict(frozen=True)
    event_id: str
    distance_km: float
