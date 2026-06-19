from typing import TypedDict


class FeatureConfig(TypedDict):
    """Configuration for feature generation."""

    peak_hours_morning: tuple[int, int]
    peak_hours_evening: tuple[int, int]
    late_night_hours: tuple[int, int]
    max_impact_radius_km: float
    rolling_window_hours: int
    rolling_window_days: int
