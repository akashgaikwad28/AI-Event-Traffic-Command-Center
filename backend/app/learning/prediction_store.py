"""In-memory prediction + outcome store.

Thread-safe singleton. The store is the *only* mutable state in the learning
module; everything else (accuracy, lessons) is derived from it via pure
functions. This keeps the boundary clean: swap this file for a SQLAlchemy
repository later and the engines/endpoints stay untouched.
"""

import threading
from datetime import UTC, datetime

from backend.app.learning.contracts.learning_contracts import (
    OutcomeRecordDTO,
    PredictionRecordDTO,
    PredictionWithOutcomeDTO,
)


def _utcnow() -> datetime:
    return datetime.now(UTC)


class PredictionStore:
    """Append-only store of predictions, with optional outcome joins."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._predictions: dict[str, PredictionRecordDTO] = {}
        self._outcomes: dict[str, OutcomeRecordDTO] = {}

    # -- write paths --------------------------------------------------------
    def record_prediction(self, prediction: PredictionRecordDTO) -> None:
        """Persist (or overwrite) the prediction for an incident."""
        with self._lock:
            self._predictions[prediction.incident_id] = prediction

    def record_outcome(self, outcome: OutcomeRecordDTO) -> OutcomeRecordDTO:
        """Persist the ground-truth outcome for a resolved incident.

        Auto-stamps `resolved_at` when not supplied by the caller.
        """
        stamped = outcome.model_copy(
            update={"resolved_at": outcome.resolved_at or _utcnow()}
        )
        with self._lock:
            self._outcomes[stamped.incident_id] = stamped
        return stamped

    # -- read paths ---------------------------------------------------------
    def get_predictions(self) -> list[PredictionRecordDTO]:
        with self._lock:
            return list(self._predictions.values())

    def get_outcomes(self) -> list[OutcomeRecordDTO]:
        with self._lock:
            return list(self._outcomes.values())

    def get_joined(self) -> list[PredictionWithOutcomeDTO]:
        """Predictions joined with their outcome (if resolved)."""
        with self._lock:
            joined: list[PredictionWithOutcomeDTO] = []
            for incident_id, pred in self._predictions.items():
                outcome = self._outcomes.get(incident_id)
                error_mins: float | None = None
                bias: str | None = None
                if outcome is not None:
                    error_mins = round(
                        outcome.actual_clearance_mins - pred.predicted_clearance_mins,
                        1,
                    )
                    if error_mins > 0.5:
                        bias = "UNDER"  # model predicted less than reality
                    elif error_mins < -0.5:
                        bias = "OVER"
                    else:
                        bias = "EXACT"
                joined.append(
                    PredictionWithOutcomeDTO(
                        incident_id=pred.incident_id,
                        gori_score=pred.gori_score,
                        predicted_clearance_mins=pred.predicted_clearance_mins,
                        actual_clearance_mins=(
                            outcome.actual_clearance_mins if outcome else None
                        ),
                        deployment_class=pred.deployment_class,
                        scenario_category=pred.scenario_category,
                        scenario_subtype=pred.scenario_subtype,
                        error_mins=error_mins,
                        prediction_bias=bias,
                        predicted_at=pred.predicted_at,
                        resolved_at=outcome.resolved_at if outcome else None,
                    )
                )
            # Newest first — what the dashboard cares about.
            joined.sort(key=lambda r: r.predicted_at, reverse=True)
            return joined

    def resolved_predictions(self) -> list[PredictionRecordDTO]:
        """Only predictions that have a matching outcome (used for accuracy)."""
        with self._lock:
            return [
                pred
                for incident_id, pred in self._predictions.items()
                if incident_id in self._outcomes
            ]

    def clear(self) -> None:
        """Reset the loop (used by tests / reset-engine button)."""
        with self._lock:
            self._predictions.clear()
            self._outcomes.clear()


# Singleton consumed by the API layer and the optimization auto-instrumentation.
prediction_store = PredictionStore()
