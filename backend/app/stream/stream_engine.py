import asyncio
import logging
from typing import Any

from backend.app.stream.cache.stream_cache import stream_cache
from backend.app.stream.dto.stream_models import LiveAlert, StreamEvent
from backend.app.stream.stream_priority import EventPriorityQueue
from backend.app.stream.websocket_manager import ws_manager

logger = logging.getLogger(__name__)


class StreamEngine:
    """
    Central Realtime Orchestrator.
    Handles the Event Enrichment Pipeline without executing ML logic directly.
    """

    def __init__(self):
        self.priority_queue = EventPriorityQueue()
        # In a real app, these would be injected services:
        # self.prediction_engine = PredictionEngine()
        # self.resource_engine = ResourceOptimizationEngine()

    async def process_event(self, raw_event: dict[str, Any]):
        """Ingests raw event, enriches it, and dispatches to queue."""
        # 1. Event Enrichment Pipeline
        enriched_event = await self._enrich_event(raw_event)

        # 2. Add to Priority Queue
        priority = 3 if enriched_event.get("gori_score", 0) > 80 else 1
        stream_event = StreamEvent(
            event_id=raw_event.get("incident_id", "UNKNOWN"),
            event_type="INCIDENT_UPDATE",
            priority_level=priority,
            payload=enriched_event,
        )

        await self.priority_queue.enqueue(stream_event)

        # 3. Trigger async broadcast worker if not running (simplified for hackathon)
        await self._dispatch_queue()

    async def _enrich_event(self, event: dict[str, Any]) -> dict[str, Any]:
        """Calls external services (AI/Geo/Opt) to enrich the event."""
        # STREAM FAILSAFE: Wrap in try/except to guarantee stream continues
        try:
            from backend.app.api.v1.endpoints.predictions import (
                _ENGINE_INSTANCE as prediction_engine,
            )

            loop = asyncio.get_running_loop()
            prediction_req = {
                "latitude": event.get("latitude", 40.712),
                "longitude": event.get("longitude", -74.006),
                "priority": "High" if event.get("heavy_vehicle") else "Medium",
                "requires_road_closure": event.get("heavy_vehicle", False),
            }

            # Run heavy ML inference without blocking the async event loop
            assessment = await loop.run_in_executor(
                None, prediction_engine.generate_full_assessment, prediction_req
            )

            # Extract actual GORI from the ML model output
            gori = assessment.get("gori", {}).get("gori_score", 45.0)

            # Update Cache
            stream_cache.update_gori(gori)
            stream_cache.add_incident(event.get("incident_id", "UNK"), event)

            event["gori_score"] = gori
            recs = assessment.get("recommendations", [])
            event["deployment_recommendation"] = (
                recs[0]
                if recs
                else ("Deploy Heavy Tow" if gori > 80 else "Standard Dispatch")
            )
            event["enrichment_status"] = "SUCCESS_ML"
        except Exception as e:
            logger.error(f"Enrichment failure: {e}")
            event["enrichment_status"] = "DEGRADED_FALLBACK"
            event["gori_score"] = (
                stream_cache.get_latest_gori()
            )  # Fallback to last known

        return event

    async def _dispatch_queue(self):
        """Processes the queue and broadcasts via WebSocketManager."""
        while not self.priority_queue.is_empty():
            event = await self.priority_queue.dequeue()

            # Broadcast to raw events topic
            await ws_manager.broadcast_to_topic("live_events", event.dict())

            # Dispatch specific GORI alerts if critical
            if event.payload.get("gori_score", 0) > 80:
                alert = LiveAlert(
                    alert_id=f"ALT-{event.event_id}",
                    severity="CRITICAL",
                    color_code="#8b0000",
                    message="Critical GORI spike detected in incoming event stream.",
                    recommendation=event.payload.get("deployment_recommendation"),
                )
                await ws_manager.broadcast_to_topic("gori_alerts", alert.dict())


stream_engine = StreamEngine()
