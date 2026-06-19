from backend.app.observability.logging.structured_logger import get_structured_logger

logger = get_structured_logger("ml_prediction")


class PredictionLogger:
    @staticmethod
    def prediction_started(model_name: str, feature_count: int):
        logger.info(
            "prediction_started", model_name=model_name, feature_count=feature_count
        )

    @staticmethod
    def prediction_completed(
        model_name: str,
        latency_ms: int,
        confidence: float,
        gori_score: float,
        severity: str,
        estimated_clearance_minutes: int,
        feature_count: int,
    ):
        logger.info(
            "prediction_completed",
            latency_ms=latency_ms,
            model_name=model_name,
            confidence=confidence,
            gori_score=gori_score,
            severity=severity,
            estimated_clearance_minutes=estimated_clearance_minutes,
            feature_count=feature_count,
        )

    @staticmethod
    def gori_calculated(gori_score: float):
        logger.info("gori_calculated", gori_score=gori_score)


prediction_logger = PredictionLogger()
