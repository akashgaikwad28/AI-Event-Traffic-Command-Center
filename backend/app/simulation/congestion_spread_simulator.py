from copy import deepcopy
from typing import Any

from backend.app.simulation.simulation_constants import (
    DEFAULT_TIMELINE_STEPS,
    TIMELINE_STEP_MINUTES,
)
from backend.app.simulation.simulation_models import TimelineFrame


class CongestionSpreadSimulator:
    """Simulates the baseline unmitigated spread of congestion over time."""

    def simulate_baseline(
        self, base_state: dict[str, Any], steps: int = DEFAULT_TIMELINE_STEPS
    ) -> list[TimelineFrame]:
        frames = []
        current_gori = base_state["initial_gori"]
        entities = deepcopy(base_state["entities"])
        spread_factor = base_state["spread_factor"]

        current_radius = sum(e.radius or 0 for e in entities if e.type == "hotspot")
        if current_radius == 0:
            current_radius = 50.0  # Base starting radius if no hotspot

        active_incidents = sum(1 for e in entities if e.type == "incident")
        if active_incidents == 0:
            active_incidents = 1

        for i in range(steps):
            time_offset = i * TIMELINE_STEP_MINUTES

            # Unmitigated GORI increases over time
            current_gori = min(100.0, current_gori + (spread_factor * 2.5))

            # Radius expands
            current_radius += spread_factor * 15.0

            # Risk level cascades
            risk = "LOW"
            if current_gori > 80:
                risk = "CRITICAL"
            elif current_gori > 60:
                risk = "HIGH"
            elif current_gori > 40:
                risk = "MEDIUM"

            # Update hotspot entities
            frame_entities = deepcopy(entities)
            for e in frame_entities:
                if e.type == "hotspot":
                    e.radius = current_radius

            frames.append(
                TimelineFrame(
                    time_offset_mins=time_offset,
                    gori_score=current_gori,
                    active_incidents=active_incidents,
                    congestion_radius=current_radius,
                    map_entities=frame_entities,
                    cascading_risk=risk,
                )
            )

        return frames
