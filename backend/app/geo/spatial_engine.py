from collections.abc import Sequence

import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.neighbors import BallTree

from backend.app.exceptions.api_exceptions import GeoProcessingFailed
from backend.app.geo.constants import EARTH_RADIUS_KM
from backend.app.geo.types import NearbyEventResult
from backend.app.utils.geo_utils import (
    to_radians_array,
    to_radians_coordinates,
)


class SpatialEngine:
    """
    Core spatial processing engine.
    Stateless, pure computation layer containing no DB or API logic.
    """

    def __init__(self):
        pass

    def cluster_coordinates(
        self, coords: Sequence[tuple[float, float]], eps_km: float, min_samples: int
    ) -> list[int]:
        """
        Cluster geographic coordinates using DBSCAN with Haversine distance.
        Returns a list of cluster labels (-1 means noise).
        """
        if not coords:
            return []

        try:
            # Convert to radians for scikit-learn's haversine metric
            coords_array = np.array(coords)
            radians_coords = to_radians_array(coords_array)

            # DBSCAN parameters: eps must be in radians for haversine
            eps_radians = eps_km / EARTH_RADIUS_KM

            dbscan = DBSCAN(
                eps=eps_radians,
                min_samples=min_samples,
                metric="haversine",
                algorithm="ball_tree",
            )
            labels = dbscan.fit_predict(radians_coords)

            return labels.tolist()
        except Exception as e:
            raise GeoProcessingFailed(f"Clustering failed: {str(e)}")

    def build_spatial_index(self, coords: Sequence[tuple[float, float]]) -> BallTree:
        """
        Build a BallTree index for fast spatial queries.
        Uses Haversine distance metric.
        """
        if not coords:
            raise GeoProcessingFailed(
                "Cannot build spatial index with empty coordinates"
            )

        coords_array = np.array(coords)
        radians_coords = to_radians_array(coords_array)

        # Build tree
        return BallTree(radians_coords, metric="haversine")

    def find_nearby_events(
        self,
        center_lat: float,
        center_lon: float,
        event_coords: Sequence[tuple[float, float]],
        event_ids: Sequence[str],
        radius_km: float,
    ) -> list[NearbyEventResult]:
        """
        Find events within a specified radius using a spatial index.
        """
        if not event_coords or not event_ids:
            return []

        if len(event_coords) != len(event_ids):
            raise GeoProcessingFailed(
                "event_coords and event_ids must have the same length"
            )

        try:
            tree = self.build_spatial_index(event_coords)

            center_rad = np.array([to_radians_coordinates(center_lat, center_lon)])
            radius_rad = radius_km / EARTH_RADIUS_KM

            # Query radius
            ind, dist = tree.query_radius(
                center_rad, r=radius_rad, return_distance=True
            )

            indices = ind[0]
            distances_rad = dist[0]

            results = []
            for idx, dist_rad in zip(indices, distances_rad):
                dist_km = dist_rad * EARTH_RADIUS_KM
                results.append(
                    NearbyEventResult(
                        event_id=event_ids[idx], distance_km=float(dist_km)
                    )
                )

            # Sort by distance
            results.sort(key=lambda x: x.distance_km)
            return results

        except Exception as e:
            raise GeoProcessingFailed(f"Spatial query failed: {str(e)}")

    def generate_density_points(
        self, coords: Sequence[tuple[float, float]]
    ) -> list[tuple[float, float, float]]:
        """
        Generate lightweight density points for heatmap rendering.
        Returns: list of (lat, lon, weight)
        Currently simply returns the coords with a weight of 1,
        but could group them into grids in the future.
        """
        # A simple pass-through with weight 1.0 for now.
        return [(lat, lon, 1.0) for lat, lon in coords]
