from typing import Any

from backend.app.observability.logging.structured_logger import get_structured_logger


def setup_logging() -> None:
    # Now handled internally by StructuredLogger for simplicity
    pass


def get_logger(name: str) -> Any:
    # Thin wrapper to maintain backward compatibility
    return get_structured_logger(name)
