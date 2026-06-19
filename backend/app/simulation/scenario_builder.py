import uuid
from typing import Any

from backend.app.simulation.simulation_constants import ScenarioType
from backend.app.simulation.simulation_models import MapEntity


class ScenarioBuilder:
    """Builds the base initial state for various simulation scenarios."""

    def build_scenario(
        self, scenario_type: ScenarioType, params: dict[str, Any] = None
    ) -> dict[str, Any]:
        params = params or {}

        if scenario_type == ScenarioType.ACCIDENT_CASCADE:
            return self._build_accident_cascade()
        elif scenario_type == ScenarioType.STADIUM_EVENT_EGRESS:
            return self._build_stadium_egress()
        elif scenario_type == ScenarioType.CUSTOM_INCIDENT:
            return self._build_custom_incident(params)
        elif scenario_type in [
            ScenarioType.HISTORICAL_REPLAY,
            ScenarioType.LIVE_REPLAY,
        ]:
            return self._build_replay(params)

        return self._build_custom_incident(params)

    def _build_accident_cascade(self) -> dict[str, Any]:
        # Major intersection placeholder
        lat, lng = 40.7128, -74.0060
        return {
            "initial_gori": 42.0,
            "entities": [
                MapEntity(
                    id=str(uuid.uuid4()),
                    type="incident",
                    lat=lat,
                    lng=lng,
                    metadata={"severity": "high", "type": "accident"},
                ),
                MapEntity(
                    id=str(uuid.uuid4()),
                    type="hotspot",
                    lat=lat,
                    lng=lng,
                    radius=100.0,
                    metadata={"congestion": "heavy"},
                ),
            ],
            "spread_factor": 1.5,
            "base_response_time": 25.0,
            "cascading_risk": "HIGH",
        }

    def _build_stadium_egress(self) -> dict[str, Any]:
        lat, lng = 40.7505, -73.9934
        return {
            "initial_gori": 55.0,
            "entities": [
                MapEntity(
                    id=str(uuid.uuid4()),
                    type="hotspot",
                    lat=lat,
                    lng=lng,
                    radius=300.0,
                    metadata={"congestion": "critical", "type": "event"},
                )
            ],
            "spread_factor": 2.0,
            "base_response_time": 60.0,
            "cascading_risk": "MEDIUM",
        }

    def _build_custom_incident(self, params: dict[str, Any]) -> dict[str, Any]:
        lat = params.get("lat", 40.730610)
        lng = params.get("lng", -73.935242)
        severity = params.get("severity", "medium")

        gori_map = {"low": 20.0, "medium": 45.0, "high": 75.0, "critical": 90.0}

        return {
            "initial_gori": gori_map.get(severity, 45.0),
            "entities": [
                MapEntity(
                    id=str(uuid.uuid4()),
                    type="incident",
                    lat=lat,
                    lng=lng,
                    metadata={"severity": severity},
                )
            ],
            "spread_factor": 1.2 if severity == "low" else 1.8,
            "base_response_time": 20.0 if severity == "medium" else 40.0,
            "cascading_risk": "HIGH" if severity in ["high", "critical"] else "LOW",
        }

    def _build_replay(self, params: dict[str, Any]) -> dict[str, Any]:
        # Would fetch from DB in a real scenario
        return self._build_custom_incident(params)
