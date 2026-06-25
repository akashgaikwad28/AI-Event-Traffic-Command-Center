"""Lesson extractor.

Translates the raw accuracy metrics into plain-English operational lessons —
the human-readable output of the post-event learning loop. Pure functions only.
"""

from backend.app.learning.contracts.learning_contracts import (
    AccuracyMetricsDTO,
    DriftStatus,
    OutcomeRecordDTO,
    PredictionRecordDTO,
)
from backend.app.learning.prediction_store import PredictionStore


class LessonExtractor:
    """Derives operator-facing lessons from the learning store."""

    def extract(
        self,
        store: PredictionStore,
        accuracy: AccuracyMetricsDTO,
    ) -> list[str]:
        lessons: list[str] = []
        predictions = store.get_predictions()
        outcomes = {o.incident_id: o for o in store.get_outcomes()}

        # --- Lesson 1: overall model trust --------------------------------
        if accuracy.resolved_count == 0:
            lessons.append(
                "No incidents resolved yet. Resolve an incident to start the "
                "post-event learning loop."
            )
        else:
            lessons.append(
                f"Across {accuracy.resolved_count} resolved incident(s), the "
                f"clearance-time model is accurate to within "
                f"{accuracy.mean_absolute_error_mins} min MAE "
                f"({accuracy.accuracy_tier} tier)."
            )

        # --- Lesson 2: bias direction -------------------------------------
        if accuracy.resolved_count > 0:
            bias = accuracy.mean_bias_mins
            if bias > 1.0:
                lessons.append(
                    f"Model UNDER-predicts by {bias:.1f} min on average — actual "
                    "clearance takes longer than forecast. Recommend up-weighting "
                    "spread velocity / rush-hour factors in the GORI engine."
                )
            elif bias < -1.0:
                lessons.append(
                    f"Model OVER-predicts by {abs(bias):.1f} min on average — "
                    "incidents clear faster than forecast. Recommend reducing "
                    "clearance-time baseline to avoid over-deployment."
                )
            else:
                lessons.append(
                    "Clearance forecasts are well-calibrated (bias near zero). "
                    "No GORI reweighting required."
                )

        # --- Lesson 3: concept drift verdict ------------------------------
        if accuracy.drift_status == DriftStatus.DRIFT_DETECTED:
            lessons.append(
                "DRIFT DETECTED: recent error exceeds the 18-min safety "
                "threshold. Trigger a DVC/MLflow retraining run before the next "
                "operational cycle."
            )
        elif accuracy.drift_status == DriftStatus.WATCH:
            lessons.append(
                "Accuracy under watch: error is trending toward the safety "
                "threshold. Monitor the next few resolutions."
            )
        elif accuracy.resolved_count > 0:
            lessons.append(
                "No concept drift detected — models are operationally stable."
            )

        # --- Lesson 4: planned-vs-unplanned insight (Gap 1 linkage) -------
        self._append_taxonomy_lesson(lessons, predictions, outcomes)

        return lessons

    @staticmethod
    def _append_taxonomy_lesson(
        lessons: list[str],
        predictions: list[PredictionRecordDTO],
        outcomes: dict[str, OutcomeRecordDTO],
    ) -> None:
        """Compare forecast accuracy across PLANNED vs UNPLANNED events."""
        bucket_errors: dict[str, list[float]] = {"PLANNED": [], "UNPLANNED": []}
        for pred in predictions:
            outcome = outcomes.get(pred.incident_id)
            if outcome is None or pred.scenario_category is None:
                continue
            bucket = pred.scenario_category
            if bucket in bucket_errors:
                bucket_errors[bucket].append(
                    outcome.actual_clearance_mins - pred.predicted_clearance_mins
                )

        planned_errs = bucket_errors["PLANNED"]
        unplanned_errs = bucket_errors["UNPLANNED"]
        if len(planned_errs) >= 1 and len(unplanned_errs) >= 1:
            planned_mae = sum(abs(e) for e in planned_errs) / len(planned_errs)
            unplanned_mae = sum(abs(e) for e in unplanned_errs) / len(unplanned_errs)
            worse = (
                "PLANNED events"
                if planned_mae > unplanned_mae
                else "UNPLANNED incidents"
            )
            lessons.append(
                f"Forecast accuracy split — PLANNED: {planned_mae:.1f} min MAE | "
                f"UNPLANNED: {unplanned_mae:.1f} min MAE. Model struggles more "
                f"with {worse}; prioritise feature engineering there."
            )

    def retraining_recommendation(self, accuracy: AccuracyMetricsDTO) -> str:
        if accuracy.drift_status == DriftStatus.DRIFT_DETECTED:
            return (
                "RECOMMENDED: schedule a retraining cycle via the DVC/MLflow "
                "pipeline using the most recent resolved incidents."
            )
        if accuracy.drift_status == DriftStatus.WATCH:
            return (
                "OPTIONAL: collect a few more resolutions, then retrain if the "
                "WATCH status persists."
            )
        return (
            "No retraining required — current model artefacts remain production-valid."
        )


lesson_extractor = LessonExtractor()
