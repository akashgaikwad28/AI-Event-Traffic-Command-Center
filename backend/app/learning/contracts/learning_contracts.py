"""Strict Pydantic contracts for the post-event learning loop.

Frozen models matching the project's contract style (see
`resource_optimization/contracts/` and `analytics/contracts/`).
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict


class DriftStatus(str, Enum):
    """Concept-drift indicator comparing recent error against historical baseline."""

    STABLE = "STABLE"
    WATCH = "WATCH"
    DRIFT_DETECTED = "DRIFT_DETECTED"


class PredictionRecordDTO(BaseModel):
    """A prediction captured at the moment a plan is generated."""

    model_config = ConfigDict(frozen=True)
    incident_id: str
    gori_score: float
    predicted_clearance_mins: float
    deployment_class: str
    scenario_category: str | None = None  # PLANNED / UNPLANNED (Gap 1 linkage)
    scenario_subtype: str | None = None
    predicted_at: datetime


class OutcomeRecordDTO(BaseModel):
    """Ground-truth outcome captured when an incident is resolved."""

    model_config = ConfigDict(frozen=True)
    incident_id: str
    actual_clearance_mins: float
    resolved_at: datetime


class PredictionWithOutcomeDTO(BaseModel):
    """Joined view used by the history table on the frontend."""

    model_config = ConfigDict(frozen=True)
    incident_id: str
    gori_score: float
    predicted_clearance_mins: float
    actual_clearance_mins: float | None
    deployment_class: str
    scenario_category: str | None
    scenario_subtype: str | None
    error_mins: float | None  # actual - predicted (None until resolved)
    prediction_bias: str | None  # OVER / UNDER / EXACT (None until resolved)
    predicted_at: datetime
    resolved_at: datetime | None


class AccuracyMetricsDTO(BaseModel):
    """Aggregate accuracy over all resolved incidents."""

    model_config = ConfigDict(frozen=True)
    resolved_count: int
    mean_absolute_error_mins: float
    root_mean_squared_error_mins: float
    mean_bias_mins: float  # positive = model under-predicts (clearance took longer)
    over_predict_rate: float  # fraction where predicted > actual
    under_predict_rate: float  # fraction where predicted < actual
    accuracy_tier: str  # EXCELLENT / GOOD / DEGRADING / POOR
    drift_status: DriftStatus


class LearningInsightDTO(BaseModel):
    """The full insight bundle surfaced to operators."""

    model_config = ConfigDict(frozen=True)
    generated_at: datetime
    accuracy: AccuracyMetricsDTO
    lessons: list[str]
    retraining_recommendation: str


class LearningStateDTO(BaseModel):
    """Top-level state object served by GET /learning/insights."""

    model_config = ConfigDict(frozen=True)
    loop_active: bool
    insights: LearningInsightDTO
    recent_predictions: list[PredictionWithOutcomeDTO]
