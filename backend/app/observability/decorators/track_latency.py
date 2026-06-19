import time
from functools import wraps

from backend.app.observability.logging.structured_logger import get_structured_logger
from backend.app.observability.metrics.metrics_registry import metrics_registry


def track_latency(service_name: str):
    logger = get_structured_logger(service_name)

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = await func(*args, **kwargs)
            latency_ms = int((time.perf_counter() - start) * 1000)
            logger.info(f"{func.__name__}_completed", latency_ms=latency_ms)
            metrics_registry.record_latency(service_name, latency_ms)
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            latency_ms = int((time.perf_counter() - start) * 1000)
            logger.info(f"{func.__name__}_completed", latency_ms=latency_ms)
            metrics_registry.record_latency(service_name, latency_ms)
            return result

        import inspect

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
