from backend.app.core.logger import get_logger
from backend.app.exceptions.api_exceptions import FeatureValidationFailed

logger = get_logger("ai.feature_validator")

# Hyderabad metro area bounding box
LAT_BOUNDS = (16.5, 18.0)
LON_BOUNDS = (77.5, 79.5)


def validate_coordinates(lat: float, lon: float) -> None:
    if not (LAT_BOUNDS[0] <= lat <= LAT_BOUNDS[1]):
        raise FeatureValidationFailed(
            f"Latitude {lat} out of operational bounds {LAT_BOUNDS}"
        )
    if not (LON_BOUNDS[0] <= lon <= LON_BOUNDS[1]):
        raise FeatureValidationFailed(
            f"Longitude {lon} out of operational bounds {LON_BOUNDS}"
        )


def validate_feature_vector(
    features: dict,
    expected_columns: list[str],
) -> dict:
    """Enforce strict feature schema contract."""
    missing = [c for c in expected_columns if c not in features]
    extra = [c for c in features if c not in expected_columns]

    if missing:
        logger.warning("Missing features, filling defaults", missing=missing)
        for col in missing:
            features[col] = 0.0

    if extra:
        logger.warning("Unexpected features, dropping", extra=extra)
        for col in extra:
            del features[col]

    # Enforce ordering
    return {col: features[col] for col in expected_columns}
