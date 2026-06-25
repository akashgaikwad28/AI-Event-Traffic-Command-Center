"""Accuracy / drift engine.

Pure, side-effect-free functions. Computes aggregate accuracy metrics over the
resolved predictions in the store. No I/O, fully unit-testable.
"""

import math

from backend.app.learning.contracts.learning_contracts import (
    AccuracyMetricsDTO,
    DriftStatus,
    OutcomeRecordDTO,
    PredictionRecordDTO,
)

# Tunable thresholds for the hackathon demo. In production these would come
# from a model registry / config service.
_MAE_EXCELLENT = 5.0
_MAE_GOOD = 12.0
_MAE_DEGRADING = 25.0
_DRIFT_WATCH_BIAS = 8.0
_DRIFT_DETECTED_BIAS = 18.0


class AccuracyEngine:
    """Computes accuracy + concept-drift indicators from resolved records."""

    def compute(
        self,
        predictions: list[PredictionRecordDTO],
        outcomes: list[OutcomeRecordDTO],
    ) -> AccuracyMetricsDTO:
        outcome_by_id = {o.incident_id: o for o in outcomes}
        errors: list[float] = []  # actual - predicted
        over = 0  # predicted > actual
        under = 0  # predicted < actual

        for pred in predictions:
            outcome = outcome_by_id.get(pred.incident_id)
            if outcome is None:
                continue
            delta = outcome.actual_clearance_mins - pred.predicted_clearance_mins
            errors.append(delta)
            if delta < -0.5:
                over += 1
            elif delta > 0.5:
                under += 1

        resolved_count = len(errors)
        if resolved_count == 0:
            return AccuracyMetricsDTO(
                resolved_count=0,
                mean_absolute_error_mins=0.0,
                root_mean_squared_error_mins=0.0,
                mean_bias_mins=0.0,
                over_predict_rate=0.0,
                under_predict_rate=0.0,
                accuracy_tier="NO_DATA",
                drift_status=DriftStatus.STABLE,
            )

        mae = sum(abs(e) for e in errors) / resolved_count
        rmse = math.sqrt(sum(e * e for e in errors) / resolved_count)
        mean_bias = sum(errors) / resolved_count
        over_rate = over / resolved_count
        under_rate = under / resolved_count

        return AccuracyMetricsDTO(
            resolved_count=resolved_count,
            mean_absolute_error_mins=round(mae, 1),
            root_mean_squared_error_mins=round(rmse, 1),
            mean_bias_mins=round(mean_bias, 1),
            over_predict_rate=round(over_rate, 2),
            under_predict_rate=round(under_rate, 2),
            accuracy_tier=self._accuracy_tier(mae),
            drift_status=self._drift_status(mean_bias),
        )

    @staticmethod
    def _accuracy_tier(mae: float) -> str:
        if mae <= _MAE_EXCELLENT:
            return "EXCELLENT"
        if mae <= _MAE_GOOD:
            return "GOOD"
        if mae <= _MAE_DEGRADING:
            return "DEGRADING"
        return "POOR"

    @staticmethod
    def _drift_status(mean_bias: float) -> DriftStatus:
        abs_bias = abs(mean_bias)
        if abs_bias >= _DRIFT_DETECTED_BIAS:
            return DriftStatus.DRIFT_DETECTED
        if abs_bias >= _DRIFT_WATCH_BIAS:
            return DriftStatus.WATCH
        return DriftStatus.STABLE


accuracy_engine = AccuracyEngine()
