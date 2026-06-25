import time
from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.app.learning import prediction_store
from backend.app.learning.contracts.learning_contracts import (
    PredictionRecordDTO,
)
from backend.app.observability.logging.structured_logger import (
    get_structured_logger,
)
from backend.app.resource_optimization.contracts.optimization_contracts import (
    OperationalPlanDTO,
    OptimizationRequestDTO,
)
from backend.app.resource_optimization.logging.optimization_logger import (
    optimization_logger,
)
from backend.app.resource_optimization.resource_engine import ResourceOptimizationEngine

router = APIRouter()


# Dependency
def get_resource_engine() -> ResourceOptimizationEngine:
    return ResourceOptimizationEngine()


@router.post("/incident-response", response_model=OperationalPlanDTO)
async def generate_incident_response(
    request: OptimizationRequestDTO,
    engine: ResourceOptimizationEngine = Depends(get_resource_engine),
) -> Any:
    """
    AI Traffic Operations Command Center Endpoint.
    Generates dynamic resource allocation, graph diversion, and impact simulation.
    """
    start_time = time.perf_counter()
    incident_id = request.dict().get("incident_id", "unknown")
    try:
        debug_logger = get_structured_logger("optimization_debug")
        debug_logger.info("incident_payload_received", incident=request.dict())

        optimization_logger.optimization_started(incident_id)

        # Convert Pydantic request to dict for engine processing
        plan = engine.generate_operational_plan(request.dict())

        latency_ms = int((time.perf_counter() - start_time) * 1000)

        # Additional Hardening: DTO Type Validation
        if isinstance(plan, BaseModel):
            plan_data = (
                plan.model_dump() if hasattr(plan, "model_dump") else plan.dict()
            )
        else:
            plan_data = plan

        # Operational Logging
        officer_count = plan_data.get("resource_plan", {}).get("police_officers", 0)
        barricade_count = plan_data.get("resource_plan", {}).get("barricades", 0)
        diversion_count = len(plan_data.get("diversion_plan", {}).get("points", []))

        # Ensure we don't fail on simulation result DTO conversion inside dict
        expected_case = plan_data.get("predicted_impact", {}).get("expected_case", {})
        if isinstance(expected_case, BaseModel):
            expected_case = (
                expected_case.model_dump()
                if hasattr(expected_case, "model_dump")
                else expected_case.dict()
            )
        elif hasattr(expected_case, "__dict__") and not isinstance(expected_case, dict):
            expected_case = expected_case.__dict__

        congestion_reduction = (
            expected_case.get("congestion_reduction", 0)
            if isinstance(expected_case, dict)
            else 0
        )

        optimization_logger.deployment_plan_generated(
            officer_count=officer_count,
            deployment_zones=1,
            barricade_count=barricade_count,
            diversion_routes=diversion_count,
            estimated_congestion_reduction=congestion_reduction,
            confidence=plan_data.get("confidence", 0.0),
        )

        if barricade_count > 0:
            optimization_logger.barricade_strategy_generated(barricade_count)

        if diversion_count > 0:
            optimization_logger.diversion_strategy_generated(diversion_count)

        # Post-Event Learning Loop (Gap 2): capture the prediction so it can be
        # compared against the actual clearance time once the incident resolves.
        try:
            expected_clearance = (
                expected_case.get("estimated_clearance_minutes", 45)
                if isinstance(expected_case, dict)
                else 45
            )
            prediction_store.record_prediction(
                PredictionRecordDTO(
                    incident_id=incident_id,
                    gori_score=request.gori_score,
                    predicted_clearance_mins=float(expected_clearance),
                    deployment_class=plan_data.get("operational_risk", "Standard"),
                    scenario_category=request.scenario_category,
                    scenario_subtype=request.scenario_subtype,
                    predicted_at=datetime.now(UTC),
                )
            )
        except Exception as learn_err:  # Learning loop must never break dispatch
            debug_logger.warning("learning_capture_failed", error=str(learn_err))

        optimization_logger.optimization_completed(incident_id, latency_ms)
        return plan
    except Exception as e:
        optimization_logger.optimization_failed(incident_id, str(e))
        raise HTTPException(
            status_code=500, detail=f"Optimization failure: {str(e)}"
        ) from e
