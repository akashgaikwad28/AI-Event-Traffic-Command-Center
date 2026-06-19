from backend.app.observability.logging.structured_logger import get_structured_logger

logger = get_structured_logger("simulation")


class SimulationLogger:
    @staticmethod
    def simulation_started(scenario: str):
        logger.info("simulation_started", scenario=scenario)

    @staticmethod
    def simulation_completed(
        scenario: str,
        duration_ms: int,
        before_gori: float,
        after_gori: float,
        improvement_percent: float,
    ):
        logger.info(
            "simulation_completed",
            duration_ms=duration_ms,
            scenario=scenario,
            before_gori=before_gori,
            after_gori=after_gori,
            improvement_percent=improvement_percent,
        )


simulation_logger = SimulationLogger()
