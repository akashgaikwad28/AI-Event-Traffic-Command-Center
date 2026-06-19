import uuid
from copy import deepcopy
from typing import Any

from backend.app.simulation.simulation_constants import (
    DEFAULT_TIMELINE_STEPS,
    TIMELINE_STEP_MINUTES,
)
from backend.app.simulation.simulation_models import MapEntity, TimelineFrame


class InterventionSimulator:
    """Simulates the spread of congestion when interventions (barricades, diversions) are applied."""

    def simulate_optimized(
        self,
        base_state: dict[str, Any],
        recommendations: list[dict[str, Any]],
        steps: int = DEFAULT_TIMELINE_STEPS,
    ) -> list[TimelineFrame]:
        frames = []
        current_gori = base_state["initial_gori"]
        entities = deepcopy(base_state["entities"])
        spread_factor = base_state["spread_factor"]

        # Add intervention entities
        for rec in recommendations:
            if rec.get("type") in ["diversion", "barricade", "unit"]:
                lat = rec.get("location", {}).get("lat", 40.7128)
                lng = rec.get("location", {}).get("lng", -74.0060)
                entities.append(
                    MapEntity(
                        id=str(uuid.uuid4()),
                        type=rec["type"],
                        lat=lat,
                        lng=lng,
                        metadata=rec,
                    )
                )

        current_radius = sum(e.radius or 0 for e in entities if e.type == "hotspot")
        if current_radius == 0:
            current_radius = 50.0

        active_incidents = sum(1 for e in entities if e.type == "incident")

        # Interventions reduce spread factor by half
        mitigated_spread_factor = spread_factor * 0.4

        for i in range(steps):
            time_offset = i * TIMELINE_STEP_MINUTES

            # GORI spikes initially then drops due to interventions
            if i < 3:
                current_gori = min(
                    100.0, current_gori + (mitigated_spread_factor * 2.0)
                )
            else:
                current_gori = max(20.0, current_gori - (mitigated_spread_factor * 3.0))

            # Radius expands slowly then stabilizes
            if i < 5:
                current_radius += mitigated_spread_factor * 8.0
            else:
                current_radius = max(
                    50.0, current_radius - (mitigated_spread_factor * 2.0)
                )

            # Risk level cascades down
            risk = "LOW"
            if current_gori > 80:
                risk = "CRITICAL"
            elif current_gori > 60:
                risk = "HIGH"
            elif current_gori > 40:
                risk = "MEDIUM"

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
