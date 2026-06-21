import asyncio
import random
import uuid

from backend.app.stream.stream_engine import stream_engine


class IngestionSimulator:
    """
    Simulates real-time enterprise load and specific demo scenarios.
    """

    async def run_scenario(self, scenario_name: str, payload: dict = None):
        if not payload:
            payload = {
                "lat": 40.712,
                "lng": -74.006,
                "hvi": False,
                "rush": True,
                "gori": 85,
            }

        if (
            scenario_name == "HEAVY_VEHICLE_BREAKDOWN"
            or scenario_name == "STADIUM_EVENT_EGRESS"
            or scenario_name == "CUSTOM_INCIDENT"
        ):
            await self._simulate_heavy_breakdown(payload)
        elif (
            scenario_name == "ACCIDENT_CASCADE" or scenario_name == "HISTORICAL_REPLAY"
        ):
            await self._simulate_cascade(payload)
        else:
            await self._simulate_normal(payload)

    async def _simulate_heavy_breakdown(self, payload: dict):
        """Demo Scenario: Major point-incident leading to GORI spike."""
        event = {
            "incident_id": f"INC-{str(uuid.uuid4())[:6]}",
            "type": "Critical Target Event",
            "heavy_vehicle": payload.get("hvi", True),
            "is_rush_hour": payload.get("rush", True),
            "latitude": payload.get("lat"),
            "longitude": payload.get("lng"),
            "gori_score": payload.get("gori", 85),
        }
        await stream_engine.process_event(event)

    async def _simulate_cascade(self, payload: dict):
        """Demo Scenario: Multiple incidents cluster around target location."""
        base_lat = payload.get("lat")
        base_lng = payload.get("lng")
        for i in range(3):
            event = {
                "incident_id": f"INC-{str(uuid.uuid4())[:6]}",
                "type": "Cascading Collision",
                "heavy_vehicle": payload.get("hvi", False),
                "latitude": base_lat + (random.uniform(-0.005, 0.005)),
                "longitude": base_lng + (random.uniform(-0.005, 0.005)),
                "gori_score": payload.get("gori", 65),
            }
            await stream_engine.process_event(event)
            await asyncio.sleep(0.5)

    async def _simulate_normal(self, payload: dict):
        event = {
            "incident_id": f"INC-{str(uuid.uuid4())[:6]}",
            "type": "Minor Event",
            "heavy_vehicle": False,
            "latitude": payload.get("lat"),
            "longitude": payload.get("lng"),
            "gori_score": payload.get("gori", 25),
        }
        await stream_engine.process_event(event)


simulator = IngestionSimulator()
