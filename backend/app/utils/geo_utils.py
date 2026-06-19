import math
from collections.abc import Sequence

import numpy as np

from backend.app.exceptions.api_exceptions import InvalidCoordinates
from backend.app.geo.constants import EARTH_RADIUS_KM


def to_radians_coordinates(lat: float, lon: float) -> tuple[float, float]:
    """Convert degrees to radians for use with BallTree and Haversine."""
    return math.radians(lat), math.radians(lon)


def from_radians_coordinates(lat_rad: float, lon_rad: float) -> tuple[float, float]:
    """Convert radians back to degrees."""
    return math.degrees(lat_rad), math.degrees(lon_rad)


def to_radians_array(coords: np.ndarray) -> np.ndarray:
    """Convert array of [lat, lon] from degrees to radians."""
    return np.radians(coords)


def from_radians_array(coords: np.ndarray) -> np.ndarray:
    """Convert array of [lat, lon] from radians to degrees."""
    return np.degrees(coords)


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees) in kilometers.
    """
    lat1_r, lon1_r = to_radians_coordinates(lat1, lon1)
    lat2_r, lon2_r = to_radians_coordinates(lat2, lon2)

    dlon = lon2_r - lon1_r
    dlat = lat2_r - lat1_r

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.asin(math.sqrt(a))
    return c * EARTH_RADIUS_KM


def haversine_vectorized(
    lat1: float, lon1: float, lats2: np.ndarray, lons2: np.ndarray
) -> np.ndarray:
    """
    Vectorized haversine distance computation between a single point and an array of points.
    All inputs should be in DEGREES.
    Returns array of distances in kilometers.
    """
    lat1_rad, lon1_rad = to_radians_coordinates(lat1, lon1)
    lats2_rad = np.radians(lats2)
    lons2_rad = np.radians(lons2)

    dlat = lats2_rad - lat1_rad
    dlon = lons2_rad - lon1_rad

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat1_rad) * np.cos(lats2_rad) * np.sin(dlon / 2) ** 2
    )
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    return EARTH_RADIUS_KM * c


def meters_to_km(meters: float) -> float:
    """Convert meters to kilometers."""
    return meters / 1000.0


def km_to_meters(km: float) -> float:
    """Convert kilometers to meters."""
    return km * 1000.0


def coordinate_validation(lat: float, lon: float) -> None:
    """Validate latitude and longitude ranges."""
    if not (-90.0 <= lat <= 90.0):
        raise InvalidCoordinates(f"Latitude must be between -90 and 90. Got {lat}")
    if not (-180.0 <= lon <= 180.0):
        raise InvalidCoordinates(f"Longitude must be between -180 and 180. Got {lon}")


def coordinate_normalization(lat: float, lon: float) -> tuple[float, float]:
    """Normalize coordinates to standard ranges and validate."""
    coordinate_validation(lat, lon)
    return lat, lon


def bounding_box(
    lat: float, lon: float, radius_km: float
) -> tuple[float, float, float, float]:
    """
    Calculate a bounding box (min_lat, min_lon, max_lat, max_lon)
    around a point with a given radius in kilometers.
    """
    rad_dist = radius_km / EARTH_RADIUS_KM
    lat_rad, lon_rad = to_radians_coordinates(lat, lon)

    min_lat = lat_rad - rad_dist
    max_lat = lat_rad + rad_dist

    dlon = math.asin(math.sin(rad_dist) / math.cos(lat_rad))

    min_lon = lon_rad - dlon
    max_lon = lon_rad + dlon

    return (
        math.degrees(min_lat),
        math.degrees(min_lon),
        math.degrees(max_lat),
        math.degrees(max_lon),
    )


def centroid_calculation(
    coords: Sequence[tuple[float, float]], weights: Sequence[float] | None = None
) -> tuple[float, float]:
    """
    Calculate the center (centroid) of a set of coordinates.
    Supports optional weights (e.g., severity weighting).
    """
    if not coords:
        raise ValueError("Cannot calculate centroid of empty coordinates list.")

    if weights is None:
        weights = [1.0] * len(coords)

    if len(coords) != len(weights):
        raise ValueError("Coordinates and weights must have the same length.")

    total_weight = sum(weights)
    if total_weight == 0:
        return 0.0, 0.0

    weighted_lat = sum(c[0] * w for c, w in zip(coords, weights))
    weighted_lon = sum(c[1] * w for c, w in zip(coords, weights))

    return weighted_lat / total_weight, weighted_lon / total_weight


def calculate_radius(
    coords: Sequence[tuple[float, float]], center_lat: float, center_lon: float
) -> float:
    """
    Calculate the impact radius (in km) encompassing all provided coordinates
    from a center point.
    """
    if not coords:
        return 0.0

    max_dist = 0.0
    for lat, lon in coords:
        dist = haversine_distance(center_lat, center_lon, lat, lon)
        if dist > max_dist:
            max_dist = dist

    return max_dist
