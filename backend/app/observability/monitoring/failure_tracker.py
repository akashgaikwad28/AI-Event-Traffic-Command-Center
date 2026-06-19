from datetime import datetime
from typing import Any


class FailureTracker:
    """Centralized failure tracking for APIs, models, providers, and websocket connections."""

    def __init__(self):
        self.failures: list[dict[str, Any]] = []
        self.MAX_FAILURES = 100

    def record_failure(self, service: str, error_type: str, message: str):
        record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": service,
            "error_type": error_type,
            "message": message,
        }
        self.failures.append(record)
        if len(self.failures) > self.MAX_FAILURES:
            self.failures.pop(0)

    def get_recent_failures(self, limit: int = 20) -> list[dict[str, Any]]:
        return list(reversed(self.failures))[:limit]


failure_tracker = FailureTracker()
