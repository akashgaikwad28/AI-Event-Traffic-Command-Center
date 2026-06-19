from backend.app.geo.spatial_engine import SpatialEngine


def test_cluster_coordinates():
    engine = SpatialEngine()
    # Three points close together, one far away
    coords = [
        (40.7128, -74.0060),  # NY1
        (40.7130, -74.0065),  # NY2
        (40.7125, -74.0055),  # NY3
        (51.5074, -0.1278),  # London (Noise)
    ]

    labels = engine.cluster_coordinates(coords, eps_km=1.0, min_samples=2)

    assert len(labels) == 4
    assert labels[0] == labels[1] == labels[2] != -1
    assert labels[3] == -1  # London should be noise


def test_find_nearby_events():
    engine = SpatialEngine()
    coords = [
        (40.7128, -74.0060),
        (40.7200, -74.0100),
        (51.5074, -0.1278),
    ]
    event_ids = ["e1", "e2", "e3"]

    # Query around NY
    results = engine.find_nearby_events(
        center_lat=40.7128,
        center_lon=-74.0060,
        event_coords=coords,
        event_ids=event_ids,
        radius_km=5.0,
    )

    assert len(results) == 2
    assert any(r.event_id == "e1" for r in results)
    assert any(r.event_id == "e2" for r in results)
    assert all(r.event_id != "e3" for r in results)
