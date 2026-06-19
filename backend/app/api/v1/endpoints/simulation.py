from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict

from backend.app.services.simulation_service import simulation_service
from backend.app.simulation.simulation_constants import ScenarioType
from backend.app.simulation.simulation_models import SimulationResult

router = APIRouter()


class RunSimulationRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    scenario_type: ScenarioType
    params: dict[str, Any] = {}


class CustomSimulationRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    lat: float
    lng: float
    severity: str


import time

from backend.app.demo.logging.demo_logger import demo_logger
from backend.app.simulation.logging.simulation_logger import simulation_logger


@router.post("/run", response_model=SimulationResult)
async def run_simulation(request: RunSimulationRequest):
    start_time = time.perf_counter()
    scenario_str = (
        request.scenario_type.name
        if hasattr(request.scenario_type, "name")
        else str(request.scenario_type)
    )
    simulation_logger.simulation_started(scenario=scenario_str)
    try:
        result = simulation_service.run_scenario(request.scenario_type, request.params)

        latency_ms = int((time.perf_counter() - start_time) * 1000)
        simulation_logger.simulation_completed(
            scenario=scenario_str,
            duration_ms=latency_ms,
            before_gori=result.get("baseline_state", {}).get("final_gori", 0),
            after_gori=result.get("optimized_state", {}).get("final_gori", 0),
            improvement_percent=result.get("improvements", {}).get("gori_reduction", 0),
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/custom", response_model=SimulationResult)
async def run_custom_simulation(request: CustomSimulationRequest):
    try:
        params = {"lat": request.lat, "lng": request.lng, "severity": request.severity}
        return simulation_service.run_scenario(ScenarioType.CUSTOM_INCIDENT, params)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/replay", response_model=SimulationResult)
async def run_replay_simulation(request: RunSimulationRequest):
    try:
        return simulation_service.run_scenario(
            ScenarioType.HISTORICAL_REPLAY, request.params
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/scenarios", response_model=list[dict[str, str]])
async def get_scenarios():
    return simulation_service.get_scenarios()


@router.get("/history", response_model=list[SimulationResult])
async def get_simulation_history():
    return simulation_service.get_history()


@router.post("/demo", response_model=SimulationResult)
async def run_demo_simulation():
    demo_logger.executive_demo_started()
    try:
        result = simulation_service.run_scenario(ScenarioType.ACCIDENT_CASCADE)
        demo_logger.incident_detected()
        demo_logger.gori_spike_detected()
        demo_logger.optimization_recommended()
        demo_logger.simulation_completed()
        demo_logger.executive_summary_generated()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/clear")
async def clear_simulation():
    try:
        # Currently a no-op that satisfies the frontend requirement
        return {"status": "cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
