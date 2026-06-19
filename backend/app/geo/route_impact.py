from collections.abc import Sequence

from backend.app.exceptions.api_exceptions import GeoProcessingFailed
from backend.app.geo.types import RouteImpactResult
from backend.app.utils.geo_utils import haversine_distance


class RouteImpactEstimator:
    """
    Heuristic route and traffic impact estimation.
    Operates without a routing engine or graph traversal.
    """

    def __init__(self, max_impact_radius_km: float = 2.0):
        self.max_impact_radius_km = max_impact_radius_km

    def calculate_traffic_spread(
        self,
        severity_level: str,
        severity_score: float,
        congestion_score: float,
        is_road_closed: bool,
    ) -> float:
        """
        Calculate the expected congestion spread radius heuristically based on
        event severity, congestion, and road closure status.
        """
        # Base spread depending on perceived severity text or score
        base_spread = 0.1  # 100 meters base

        # severity_score could be 1-5
        severity_multiplier = severity_score * 0.2

        # congestion score usually 0.0 - 1.0
        congestion_multiplier = 1.0 + (congestion_score * 2.0)

        closure_multiplier = 2.0 if is_road_closed else 1.0

        spread = base_spread + (
            severity_multiplier * congestion_multiplier * closure_multiplier
        )

        return min(spread, self.max_impact_radius_km)

    def estimate_route_blockage(
        self,
        event_id: str,
        latitude: float,
        longitude: float,
        severity_level: str,
        severity_score: float,
        congestion_score: float,
        is_road_closed: bool,
    ) -> RouteImpactResult:
        """
        Estimate the blockage and spread for a single event.
        """
        try:
            impact_radius = self.calculate_traffic_spread(
                severity_level, severity_score, congestion_score, is_road_closed
            )

            # Heuristic zone tagging based on radius
            affected_zones = ["Local Area"]
            if impact_radius > 0.5:
                affected_zones.append("Adjacent Corridors")
            if impact_radius > 1.0:
                affected_zones.append("Major Arterials")

            return RouteImpactResult(
                event_id=event_id,
                latitude=latitude,
                longitude=longitude,
                impact_radius_km=round(impact_radius, 2),
                severity_level=severity_level,
                affected_zones=affected_zones,
            )
        except Exception as e:
            raise GeoProcessingFailed(
                f"Failed to estimate route blockage for {event_id}: {str(e)}"
            )

    def estimate_corridor_impact(
        self,
        route_coords: Sequence[tuple[float, float]],
        event_lat: float,
        event_lon: float,
        impact_radius_km: float,
    ) -> bool:
        """
        Determine if a sequence of coordinates (a corridor) intersects
        with the given event's impact radius.
        """
        if not route_coords:
            return False

        for lat, lon in route_coords:
            dist = haversine_distance(event_lat, event_lon, lat, lon)
            if dist <= impact_radius_km:
                return True

        return False
