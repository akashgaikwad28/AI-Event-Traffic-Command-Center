import time
import uuid
from pathlib import Path
from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from backend.app.ai.audit.inference_logger import InferenceLogger
from backend.app.ai.inference.model_loader import ModelLoader
from backend.app.ai.inference.prediction_engine import PredictionEngine
from backend.app.ai.schemas.external.api_schemas import (
    PredictionRequest,
    PredictionResponse,
)

router = APIRouter()

# Global instances for Singleton DI
_ARTIFACTS_DIR = Path("backend/app/ai/artifacts")
_MODEL_LOADER = ModelLoader(_ARTIFACTS_DIR)
_ENGINE_INSTANCE = PredictionEngine(_MODEL_LOADER)
_LOGGER_INSTANCE = InferenceLogger()


# Dependency Injection
def get_prediction_engine() -> PredictionEngine:
    return _ENGINE_INSTANCE


def get_audit_logger() -> InferenceLogger:
    return _LOGGER_INSTANCE


from backend.app.ai.logging.prediction_logger import prediction_logger


@router.post("/full-assessment", response_model=PredictionResponse)
def operational_full_assessment(
    request: PredictionRequest,
    engine: PredictionEngine = Depends(get_prediction_engine),
    logger: InferenceLogger = Depends(get_audit_logger),
) -> Any:
    """
    Unified Operational Traffic Intelligence endpoint.
    Generates GORI, predictions, and operational recommendations.
    """
    start_time = time.time()
    req_id = str(uuid.uuid4())
    inc_id = request.dict().get("incident_id", "unknown")

    # 1. Log Prediction Started
    prediction_logger.prediction_started("v1.2.0", len(request.dict()))

    try:
        # Pass to the prediction engine (thin API layer)
        assessment = engine.generate_full_assessment(request.dict())

        latency_ms = int((time.time() - start_time) * 1000)

        # Log the audit trail
        logger.log_inference(req_id, request.dict(), assessment, latency_ms)

        # 2. Log Prediction Completed
        prediction_logger.prediction_completed(
            model_name="v1.2.0",
            latency_ms=latency_ms,
            confidence=assessment.get("confidence", 0.0),
            gori_score=assessment.get("gori_score", 0),
            severity=assessment.get("severity_tier", "UNKNOWN"),
            estimated_clearance_minutes=assessment.get(
                "predicted_clearance_minutes", 0
            ),
            feature_count=len(request.dict()),
        )

        # 3. Log GORI Calculated
        prediction_logger.gori_calculated(assessment.get("gori_score", 0))

        return {"success": True, **assessment}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
