import time
import uuid

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from backend.app.core.config import get_settings
from backend.app.core.logger import get_logger
from backend.app.observability.logging.correlation_id import (
    set_correlation_ids,
)
from backend.app.observability.metrics.metrics_registry import metrics_registry
from backend.app.observability.monitoring.failure_tracker import failure_tracker

logger = get_logger("middleware")
settings = get_settings()


class CorrelationIdMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        headers = dict(scope.get("headers", []))

        def get_header(name: str, default: str) -> str:
            val = headers.get(name.encode("utf-8"))
            return val.decode("utf-8") if val else default

        trace_id = get_header("x-trace-id", str(uuid.uuid4()))
        request_id = get_header("x-request-id", str(uuid.uuid4()))
        session_id = get_header("x-session-id", "anonymous")

        set_correlation_ids(trace_id, request_id, session_id)

        start_time = time.perf_counter()

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                process_time = time.perf_counter() - start_time
                new_headers = [
                    (b"x-trace-id", trace_id.encode("utf-8")),
                    (b"x-request-id", request_id.encode("utf-8")),
                    (b"x-session-id", session_id.encode("utf-8")),
                    (b"x-process-time", str(process_time).encode("utf-8")),
                ]
                message.setdefault("headers", []).extend(new_headers)
                scope["status_code"] = message.get("status", 500)
            await send(message)

        try:
            if scope["type"] == "http":
                await self.app(scope, receive, send_wrapper)
                process_time = time.perf_counter() - start_time
                latency_ms = int(process_time * 1000)
                logger.info(
                    "request_completed",
                    method=scope.get("method"),
                    url=scope.get("path"),
                    status_code=scope.get("status_code", 500),
                    latency_ms=latency_ms,
                )
                metrics_registry.record_latency("api", latency_ms)
                metrics_registry.increment_request("api")
            else:
                # Websocket
                await self.app(scope, receive, send)
        except Exception as e:
            process_time = time.perf_counter() - start_time
            latency_ms = int(process_time * 1000)
            logger.error(
                "request_failed",
                method=scope.get("method", "websocket"),
                url=scope.get("path"),
                latency_ms=latency_ms,
                error_message=str(e),
            )
            metrics_registry.increment_failure("api")
            failure_tracker.record_failure("api", type(e).__name__, str(e))
            raise


def setup_cors_middleware(app: FastAPI) -> None:
    import os

    # Default to '*' if FRONTEND_URL is not provided for local testing.
    frontend_url = os.getenv("FRONTEND_URL", "*")
    origins = (
        [u.strip() for u in frontend_url.split(",")] if frontend_url != "*" else ["*"]
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
