from typing import Any

from fastapi import APIRouter, BackgroundTasks, WebSocket

from backend.app.stream.cache.stream_cache import stream_cache
from backend.app.stream.dto.stream_models import DashboardSnapshot
from backend.app.stream.ingestion_simulator import simulator
from backend.app.stream.websocket_manager import ws_manager

router = APIRouter()

from backend.app.simulation.simulation_constants import ScenarioType


@router.websocket("/ws/{topic}")
async def websocket_endpoint(websocket: WebSocket, topic: str):
    """
    Real-Time AI Traffic Operations Intelligence Stream.
    Topics: live_events, gori_alerts, deployment_alerts
    """
    await ws_manager.connect(websocket, topic)
    try:
        while True:
            # Keep connection alive; clients can send heartbeats
            data = await websocket.receive_text()
    except Exception:
        pass
    finally:
        ws_manager.disconnect(websocket, topic)


from fastapi.responses import JSONResponse

from backend.app.core.logger import get_logger

logger = get_logger("stream_endpoints")

LEGACY_SCENARIO_MAP = {
    "SCENARIO_1": "ACCIDENT_CASCADE",
    "SCENARIO_2": "STADIUM_EVENT_EGRESS",
    "SCENARIO_3": "CUSTOM_INCIDENT",
    "SCENARIO_4": "STADIUM_EVENT_EGRESS",
    "SCENARIO_5": "LIVE_REPLAY",
    "SCENARIO_6": "LIVE_REPLAY",
    "SCENARIO_7": "CUSTOM_INCIDENT",
    "SCENARIO_8": "HISTORICAL_REPLAY",
    "SCENARIO_9": "HISTORICAL_REPLAY",
    "SCENARIO_10": "ACCIDENT_CASCADE",
}


from pydantic import BaseModel, ConfigDict


class SimulationPayload(BaseModel):
    model_config = ConfigDict(frozen=True)
    lat: float = 40.712
    lng: float = -74.006
    gori: int = 85
    hvi: bool = False
    rush: bool = True


@router.post("/start-simulation/{scenario}")
async def start_simulation(
    scenario: str,
    background_tasks: BackgroundTasks,
    payload: SimulationPayload | None = None,
):
    """Triggers the demo scenario in the background."""

    mapped_scenario = LEGACY_SCENARIO_MAP.get(scenario, scenario)

    if mapped_scenario != scenario:
        logger.warning(
            "legacy_scenario_mapped",
            original=scenario,
            mapped=mapped_scenario,
            message=f"Legacy scenario received: {scenario} -> mapped to {mapped_scenario}",
        )

    valid_scenarios = [e.value for e in ScenarioType]
    if mapped_scenario not in valid_scenarios:
        return JSONResponse(
            status_code=422,
            content={
                "error": "Invalid simulation scenario",
                "received": scenario,
                "allowed": valid_scenarios,
            },
        )

    if payload:
        background_tasks.add_task(
            simulator.run_scenario, mapped_scenario, payload.model_dump()
        )
    else:
        background_tasks.add_task(simulator.run_scenario, mapped_scenario)
    return {"status": "Simulation triggered", "scenario": mapped_scenario}


@router.get("/live-snapshot", response_model=DashboardSnapshot)
async def get_live_snapshot() -> Any:
    """Dashboard bootstrap endpoint using the fast in-memory Stream Cache."""
    cache_state = stream_cache.get_snapshot()

    return DashboardSnapshot(
        active_incidents=cache_state["active_incidents"],
        top_hotspots=cache_state["top_hotspots"],
        avg_gori=cache_state["avg_gori"],
        deployment_pressure="HIGH" if cache_state["avg_gori"] > 60 else "NORMAL",
        critical_alerts=[],  # Would be populated from active alert registry
    )


@router.get("/metrics")
async def get_stream_metrics() -> dict[str, Any]:
    """Exposes Stream Health Monitoring metrics."""
    return {
        "status": "HEALTHY",
        "websocket_metrics": ws_manager.get_metrics(),
        "cache_metrics": stream_cache.get_snapshot(),
    }
