from backend.app.observability.logging.structured_logger import get_structured_logger

logger = get_structured_logger("optimization")


class OptimizationLogger:
    @staticmethod
    def optimization_started(incident_id: str):
        logger.info("optimization_started", incident_id=incident_id)

    @staticmethod
    def optimization_completed(incident_id: str, latency_ms: int):
        logger.info(
            "optimization_completed", incident_id=incident_id, latency_ms=latency_ms
        )

    @staticmethod
    def optimization_failed(incident_id: str, error_message: str):
        logger.error(
            "optimization_failed", incident_id=incident_id, error_message=error_message
        )

    @staticmethod
    def deployment_plan_generated(
        officer_count: int,
        deployment_zones: int,
        barricade_count: int,
        diversion_routes: int,
        estimated_congestion_reduction: int,
        confidence: float,
    ):
        logger.info(
            "deployment_plan_generated",
            officer_count=officer_count,
            deployment_zones=deployment_zones,
            barricade_count=barricade_count,
            diversion_routes=diversion_routes,
            estimated_congestion_reduction=estimated_congestion_reduction,
            confidence=confidence,
        )

    @staticmethod
    def barricade_strategy_generated(barricade_count: int):
        logger.info("barricade_strategy_generated", barricade_count=barricade_count)

    @staticmethod
    def diversion_strategy_generated(diversion_count: int):
        logger.info("diversion_strategy_generated", diversion_count=diversion_count)


optimization_logger = OptimizationLogger()
