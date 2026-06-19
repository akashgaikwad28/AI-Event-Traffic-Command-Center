from backend.app.observability.logging.structured_logger import get_structured_logger

logger = get_structured_logger("executive_demo")


class DemoLogger:
    @staticmethod
    def executive_demo_started():
        logger.info("executive_demo_started")

    @staticmethod
    def incident_detected():
        logger.info("incident_detected")

    @staticmethod
    def gori_spike_detected():
        logger.info("gori_spike_detected")

    @staticmethod
    def optimization_recommended():
        logger.info("optimization_recommended")

    @staticmethod
    def simulation_completed():
        logger.info("simulation_completed")

    @staticmethod
    def executive_summary_generated():
        logger.info("executive_summary_generated")


demo_logger = DemoLogger()
