from functools import wraps

from backend.app.observability.logging.structured_logger import get_structured_logger
from backend.app.observability.metrics.metrics_registry import metrics_registry
from backend.app.observability.monitoring.failure_tracker import failure_tracker


def track_failures(service_name: str):
    logger = get_structured_logger(service_name)

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    f"{func.__name__}_failed", status="error", error_message=str(e)
                )
                metrics_registry.increment_failure(service_name)
                failure_tracker.record_failure(service_name, type(e).__name__, str(e))
                raise

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    f"{func.__name__}_failed", status="error", error_message=str(e)
                )
                metrics_registry.increment_failure(service_name)
                failure_tracker.record_failure(service_name, type(e).__name__, str(e))
                raise

        import inspect

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
