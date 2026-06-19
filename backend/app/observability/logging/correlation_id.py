import contextvars
import uuid

# Context variables for distributed tracing
_trace_id_ctx = contextvars.ContextVar("trace_id", default=None)
_request_id_ctx = contextvars.ContextVar("request_id", default=None)
_session_id_ctx = contextvars.ContextVar("session_id", default=None)


def set_correlation_ids(
    trace_id: str | None = None,
    request_id: str | None = None,
    session_id: str | None = None,
) -> None:
    _trace_id_ctx.set(trace_id or str(uuid.uuid4()))
    _request_id_ctx.set(request_id or str(uuid.uuid4()))
    _session_id_ctx.set(session_id or "anonymous")


def get_correlation_ids() -> dict[str, str]:
    return {
        "trace_id": _trace_id_ctx.get() or "unknown",
        "request_id": _request_id_ctx.get() or "unknown",
        "session_id": _session_id_ctx.get() or "unknown",
    }


def clear_correlation_ids() -> None:
    _trace_id_ctx.set(None)
    _request_id_ctx.set(None)
    _session_id_ctx.set(None)
