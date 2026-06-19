from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.config import get_settings
from backend.app.core.constants import EventSeverity
from backend.app.db.repositories.event_repo import event_repo
from backend.app.geo.hotspot_detection import HotspotDetector
from backend.app.geo.route_impact import RouteImpactEstimator
from backend.app.geo.spatial_engine import SpatialEngine
from backend.app.geo.types import HotspotResult, RouteImpactResult


class GeoService:
    """
    Thin orchestration layer for Geo Intelligence.
    Fetches data, calls pure spatial computations, and returns results.
    """

    def __init__(self):
        self.settings = get_settings()
        self.spatial_engine = SpatialEngine()
        self.hotspot_detector = HotspotDetector(self.spatial_engine)
        self.route_impact_estimator = RouteImpactEstimator(
            max_impact_radius_km=self.settings.geo_max_impact_radius_km
        )

    def _map_severity_to_score(self, severity: str) -> float:
        mapping = {
            EventSeverity.LOW.value: 1.0,
            EventSeverity.MEDIUM.value: 2.0,
            EventSeverity.HIGH.value: 3.0,
            EventSeverity.CRITICAL.value: 4.0,
        }
        return mapping.get(severity.lower(), 1.0)

    async def get_active_hotspots(self, db: AsyncSession) -> list[HotspotResult]:
        """
        Fetch active events and compute hotspots.
        """
        # Fetch active events from DB
        # To avoid massive queries in a real system, we'd limit or paginate.
        # For this operational dashboard, we get the active ones.
        events, _ = await event_repo.get_active_events(db, skip=0, limit=1000)

        if not events:
            return []

        coords = []
        event_ids = []
        severities = []
        congestion_scores = []

        for e in events:
            coords.append((e.latitude, e.longitude))
            event_ids.append(str(e.id))
            severities.append(self._map_severity_to_score(e.severity))
            # Fallback congestion score if not joined, or extract from metadata
            # For hackathon operational baseline, we can use a heuristic or 0.5
            c_score = 0.5
            if e.metadata_info and "congestion_score" in e.metadata_info:
                c_score = float(e.metadata_info["congestion_score"])
            congestion_scores.append(c_score)

        return self.hotspot_detector.detect_hotspots(
            coords=coords,
            event_ids=event_ids,
            severities=severities,
            congestion_scores=congestion_scores,
            eps_km=self.settings.geo_cluster_eps_km,
            min_samples=self.settings.geo_min_cluster_samples,
            risk_multiplier=self.settings.geo_hotspot_risk_multiplier,
        )

    async def get_route_impacts(self, db: AsyncSession) -> list[RouteImpactResult]:
        """
        Estimate route impact and congestion spread for active events.
        """
        events, _ = await event_repo.get_active_events(db, skip=0, limit=1000)

        if not events:
            return []

        impacts = []
        for e in events:
            sev_score = self._map_severity_to_score(e.severity)
            c_score = 0.5
            if e.metadata_info and "congestion_score" in e.metadata_info:
                c_score = float(e.metadata_info["congestion_score"])

            impact = self.route_impact_estimator.estimate_route_blockage(
                event_id=str(e.id),
                latitude=e.latitude,
                longitude=e.longitude,
                severity_level=e.severity,
                severity_score=sev_score,
                congestion_score=c_score,
                is_road_closed=e.road_closure,
            )
            impacts.append(impact)

        # Sort by impact radius descending
        impacts.sort(key=lambda x: x.impact_radius_km, reverse=True)
        return impacts


geo_service = GeoService()
