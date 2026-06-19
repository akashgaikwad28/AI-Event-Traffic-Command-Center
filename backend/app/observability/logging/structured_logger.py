import json
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
from typing import Any

from backend.app.observability.logging.correlation_id import get_correlation_ids


class StructuredLogger:
    """Enterprise JSON structured logger."""

    def __init__(self, service_name: str):
        self.service_name = service_name
        self._logger = logging.getLogger(service_name)
        self._logger.setLevel(logging.INFO)

        if not self._logger.handlers:
            # Console Handler
            console_handler = logging.StreamHandler()
            self._logger.addHandler(console_handler)

            # Rotating File Handler - write to root logs dir to avoid reload loops
            log_dir = "logs"
            os.makedirs(log_dir, exist_ok=True)
            file_handler = RotatingFileHandler(
                os.path.join(log_dir, "gridwise.log"),
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
            )
            self._logger.addHandler(file_handler)

    def _build_log(
        self,
        level: str,
        event: str,
        status: str,
        latency_ms: int,
        extra: dict[str, Any],
    ) -> str:
        corr_ids = get_correlation_ids()

        # Merge environment metadata
        details = {
            "environment": os.getenv("APP_ENV", "development"),
            "version": os.getenv("APP_VERSION", "1.0.0"),
            "hostname": os.getenv("HOSTNAME", "local"),
            **extra,
        }

        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level,
            "service": self.service_name,
            "event": event,
            "trace_id": corr_ids.get("trace_id", "unknown"),
            "request_id": corr_ids.get("request_id", "unknown"),
            "session_id": corr_ids.get("session_id", "unknown"),
            "latency_ms": latency_ms,
            "status": status,
            "details": details,
        }
        return json.dumps(log_entry)

    def info(
        self, event: str, status: str = "success", latency_ms: int = 0, **extra: Any
    ):
        self._logger.info(self._build_log("INFO", event, status, latency_ms, extra))

    def error(
        self, event: str, status: str = "error", latency_ms: int = 0, **extra: Any
    ):
        self._logger.error(self._build_log("ERROR", event, status, latency_ms, extra))

    def warning(
        self, event: str, status: str = "warning", latency_ms: int = 0, **extra: Any
    ):
        self._logger.warning(self._build_log("WARN", event, status, latency_ms, extra))

    def warn(
        self, event: str, status: str = "warning", latency_ms: int = 0, **extra: Any
    ):
        self.warning(event, status, latency_ms, **extra)

    def debug(
        self, event: str, status: str = "debug", latency_ms: int = 0, **extra: Any
    ):
        self._logger.debug(self._build_log("DEBUG", event, status, latency_ms, extra))

    def critical(
        self, event: str, status: str = "critical", latency_ms: int = 0, **extra: Any
    ):
        self._logger.critical(
            self._build_log("CRITICAL", event, status, latency_ms, extra)
        )


def get_structured_logger(service_name: str) -> StructuredLogger:
    return StructuredLogger(service_name)
