from backend.app.observability.logging.structured_logger import get_structured_logger

logger = get_structured_logger("genai_orchestrator")


class GenAILogger:
    @staticmethod
    def provider_request_started(provider: str, mode: str):
        logger.info("provider_request_started", provider=provider, mode=mode)

    @staticmethod
    def provider_request_completed(
        provider: str,
        mode: str,
        latency_ms: int,
        estimated_tokens: int,
        fallback_triggered: bool = False,
    ):
        logger.info(
            "provider_request_completed",
            provider=provider,
            mode=mode,
            latency_ms=latency_ms,
            estimated_tokens=estimated_tokens,
            fallback_triggered=fallback_triggered,
        )

    @staticmethod
    def provider_fallback(provider: str, next_provider: str, reason: str):
        logger.warning(
            "provider_fallback",
            status="fallback_triggered",
            provider=provider,
            next_provider=next_provider,
            reason=reason,
        )

    @staticmethod
    def copilot_response_generated(
        provider: str,
        mode: str,
        latency_ms: int,
        estimated_tokens: int,
        fallback_triggered: bool = False,
    ):
        logger.info(
            "copilot_response_generated",
            latency_ms=latency_ms,
            provider=provider,
            mode=mode,
            estimated_tokens=estimated_tokens,
            fallback_triggered=fallback_triggered,
        )


genai_logger = GenAILogger()
