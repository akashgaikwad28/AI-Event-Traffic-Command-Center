import math

import pytest

from backend.app.exceptions.api_exceptions import InvalidCoordinates
from backend.app.utils.geo_utils import (
    centroid_calculation,
    coordinate_validation,
    haversine_distance,
)


def test_haversine_distance():
    # New York (40.7128, -74.0060) to London (51.5074, -0.1278)
    # Approx 5570 km
    dist = haversine_distance(40.7128, -74.0060, 51.5074, -0.1278)
    assert math.isclose(dist, 5570, rel_tol=0.01)


def test_coordinate_validation_valid():
    coordinate_validation(45.0, 90.0)
    assert True


def test_coordinate_validation_invalid_lat():
    with pytest.raises(InvalidCoordinates):
        coordinate_validation(91.0, 0.0)


def test_coordinate_validation_invalid_lon():
    with pytest.raises(InvalidCoordinates):
        coordinate_validation(0.0, 181.0)


def test_centroid_calculation():
    coords = [(0.0, 0.0), (0.0, 2.0), (2.0, 0.0), (2.0, 2.0)]
    lat, lon = centroid_calculation(coords)
    assert math.isclose(lat, 1.0)
    assert math.isclose(lon, 1.0)


def test_centroid_calculation_weighted():
    coords = [(0.0, 0.0), (10.0, 10.0)]
    weights = [1.0, 3.0]
    lat, lon = centroid_calculation(coords, weights)
    # Expected lat: (0*1 + 10*3) / 4 = 7.5
    assert math.isclose(lat, 7.5)
    assert math.isclose(lon, 7.5)
