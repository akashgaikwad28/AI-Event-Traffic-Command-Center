from collections import defaultdict
from collections.abc import Sequence

from backend.app.exceptions.api_exceptions import HotspotDetectionFailed
from backend.app.geo.spatial_engine import SpatialEngine
from backend.app.geo.types import HotspotResult
from backend.app.utils.geo_utils import calculate_radius, centroid_calculation


class HotspotDetector:
    """
    Detects operational traffic hotspots using spatial clustering.
    Provides noise filtering, risk scoring, and confidence scoring.
    """

    def __init__(self, spatial_engine: SpatialEngine):
        self.engine = spatial_engine

    def detect_hotspots(
        self,
        coords: Sequence[tuple[float, float]],
        event_ids: Sequence[str],
        severities: Sequence[float],
        congestion_scores: Sequence[float],
        eps_km: float,
        min_samples: int,
        risk_multiplier: float = 1.0,
    ) -> list[HotspotResult]:
        """
        Detect hotspots from parallel lists of event properties.
        """
        if not coords:
            return []

        try:
            # 1. Cluster the coordinates
            labels = self.engine.cluster_coordinates(coords, eps_km, min_samples)

            # 2. Group by cluster label
            # label -> list of indices
            clusters = defaultdict(list)
            for idx, label in enumerate(labels):
                if label != -1:  # Filter out noise points
                    clusters[label].append(idx)

            hotspots = []

            # 3. Process each valid cluster
            for label, indices in clusters.items():
                cluster_coords = [coords[i] for i in indices]
                cluster_event_ids = [event_ids[i] for i in indices]
                cluster_severities = [severities[i] for i in indices]
                cluster_congestion = [congestion_scores[i] for i in indices]

                # Weighted centroid based on severity
                center_lat, center_lon = centroid_calculation(
                    cluster_coords, weights=cluster_severities
                )

                # Impact radius
                radius_km = calculate_radius(cluster_coords, center_lat, center_lon)
                # Ensure minimum radius for visual rendering
                radius_km = max(radius_km, 0.1)

                # Avg metrics
                avg_severity = sum(cluster_severities) / len(cluster_severities)
                avg_congestion = sum(cluster_congestion) / len(cluster_congestion)

                # Density calculation (events per sq km). Add a small epsilon to avoid div zero
                area = 3.14159 * (radius_km**2)
                density = len(indices) / max(area, 0.01)

                # Risk Score (Critical Differentiator)
                # Formula: weighted combination
                base_risk = (
                    (avg_severity * 0.4)
                    + (avg_congestion * 10 * 0.3)
                    + (min(density, 100) / 100 * 0.3)
                )
                risk_score = min(base_risk * risk_multiplier * 10, 100.0)  # scale 0-100

                # Confidence Score
                # Based on cluster size (more events = more confident) and density
                confidence = min(
                    (len(indices) / (min_samples * 2)) * 50 + (density * 5), 100.0
                )

                hotspots.append(
                    HotspotResult(
                        latitude=center_lat,
                        longitude=center_lon,
                        radius_km=radius_km,
                        risk_score=round(risk_score, 2),
                        confidence_score=round(confidence, 2),
                        event_count=len(indices),
                        event_ids=cluster_event_ids,
                    )
                )

            # Sort by risk score descending
            hotspots.sort(key=lambda h: h.risk_score, reverse=True)
            return hotspots

        except Exception as e:
            raise HotspotDetectionFailed(f"Failed to detect hotspots: {str(e)}")
