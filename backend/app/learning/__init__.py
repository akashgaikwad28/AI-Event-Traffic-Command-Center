"""Post-Event Learning module.

Implements the feedback loop documented in docs/ml/POST_EVENT_LEARNING.md:
captures each prediction, records actual outcomes, computes accuracy/drift,
and extracts plain-English lessons for operators.

Designed as a self-contained DDD module mirroring `analytics/` and
`resource_optimization/`. The in-memory `PredictionStore` sits behind a clean
interface so it can be swapped for PostgreSQL/Redis in production without
touching the API layer.
"""

from backend.app.learning.accuracy_engine import AccuracyEngine, accuracy_engine
from backend.app.learning.contracts.learning_contracts import (
    AccuracyMetricsDTO,
    LearningInsightDTO,
    LearningStateDTO,
    OutcomeRecordDTO,
    PredictionRecordDTO,
    PredictionWithOutcomeDTO,
)
from backend.app.learning.lesson_extractor import LessonExtractor, lesson_extractor
from backend.app.learning.prediction_store import prediction_store

__all__ = [
    "AccuracyMetricsDTO",
    "LearningInsightDTO",
    "LearningStateDTO",
    "OutcomeRecordDTO",
    "PredictionRecordDTO",
    "PredictionWithOutcomeDTO",
    "prediction_store",
    "accuracy_engine",
    "AccuracyEngine",
    "lesson_extractor",
    "LessonExtractor",
]
