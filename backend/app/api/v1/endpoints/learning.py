"""Post-Event Learning REST endpoints.

Closes Gap 2: the hackathon theme calls out "No post-event learning system" as
a core industry problem. These endpoints expose the capture -> resolve ->
insight loop so judges can see the system learning in real time.
"""

from datetime import UTC, datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from backend.app.learning import (
    accuracy_engine,
    lesson_extractor,
    prediction_store,
)
from backend.app.learning.contracts.learning_contracts import (
    AccuracyMetricsDTO,
    LearningInsightDTO,
    LearningStateDTO,
    OutcomeRecordDTO,
    PredictionRecordDTO,
    PredictionWithOutcomeDTO,
)

router = APIRouter()


# ---------------------------------------------------------------------------
# Request schemas (frozen, matching project convention)
# ---------------------------------------------------------------------------
class RecordPredictionRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    incident_id: str
    gori_score: float
    predicted_clearance_mins: float
    deployment_class: str = "Standard"
    scenario_category: str | None = Field(
        default=None, description="PLANNED or UNPLANNED"
    )
    scenario_subtype: str | None = None


class ResolveIncidentRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    actual_clearance_mins: float = Field(..., gt=0)


# ---------------------------------------------------------------------------
# Internal helper: build the aggregate insight bundle from the store
# ---------------------------------------------------------------------------
def _build_state() -> LearningStateDTO:
    accuracy = accuracy_engine.compute(
        prediction_store.get_predictions(), prediction_store.get_outcomes()
    )
    insights = LearningInsightDTO(
        generated_at=datetime.now(UTC),
        accuracy=accuracy,
        lessons=lesson_extractor.extract(prediction_store, accuracy),
        retraining_recommendation=lesson_extractor.retraining_recommendation(accuracy),
    )
    recent = prediction_store.get_joined()[:10]
    return LearningStateDTO(
        loop_active=True, insights=insights, recent_predictions=recent
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@router.get("/insights", response_model=LearningStateDTO)
async def get_insights() -> LearningStateDTO:
    """Aggregate accuracy, drift status, and auto-extracted lessons."""
    return _build_state()


@router.get("/history", response_model=list[PredictionWithOutcomeDTO])
async def get_history() -> list[PredictionWithOutcomeDTO]:
    """Full prediction-vs-actual log (newest first)."""
    return prediction_store.get_joined()


@router.get("/accuracy", response_model=AccuracyMetricsDTO)
async def get_accuracy() -> AccuracyMetricsDTO:
    return accuracy_engine.compute(
        prediction_store.get_predictions(), prediction_store.get_outcomes()
    )


@router.post("/record-prediction", response_model=PredictionRecordDTO)
async def record_prediction(request: RecordPredictionRequest) -> PredictionRecordDTO:
    """Capture a prediction into the learning loop.

    Called automatically by the optimization endpoint and may also be called
    directly for integration testing.
    """
    record = PredictionRecordDTO(
        incident_id=request.incident_id,
        gori_score=request.gori_score,
        predicted_clearance_mins=request.predicted_clearance_mins,
        deployment_class=request.deployment_class,
        scenario_category=request.scenario_category,
        scenario_subtype=request.scenario_subtype,
        predicted_at=datetime.now(UTC),
    )
    prediction_store.record_prediction(record)
    return record


@router.post("/resolve-incident/{incident_id}", response_model=PredictionWithOutcomeDTO)
async def resolve_incident(
    incident_id: str, request: ResolveIncidentRequest
) -> PredictionWithOutcomeDTO:
    """Record the ground-truth clearance time for a resolved incident.

    This is the moment the learning loop closes for one incident: the system
    can now compute its forecast error and feed it back.
    """
    prediction_store.record_outcome(
        OutcomeRecordDTO(
            incident_id=incident_id,
            actual_clearance_mins=request.actual_clearance_mins,
            resolved_at=datetime.now(UTC),
        )
    )

    joined = {row.incident_id: row for row in prediction_store.get_joined()}
    if incident_id not in joined:
        raise HTTPException(status_code=404, detail="Incident prediction not found")
    return joined[incident_id]


@router.post("/reset")
async def reset_learning() -> dict[str, str]:
    """Clear the loop (used by the dashboard Reset Engines button)."""
    prediction_store.clear()
    return {"status": "learning loop reset"}
