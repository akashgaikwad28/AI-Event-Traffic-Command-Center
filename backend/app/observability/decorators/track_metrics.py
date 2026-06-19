from functools import wraps

from backend.app.observability.metrics.metrics_registry import metrics_registry


def track_metrics(service_name: str):
    """Tracks generic execution counts and fallback usage for a service."""

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            metrics_registry.increment_request(service_name)
            # Track fallback usage if the kwarg 'use_fallback' is present and True
            if kwargs.get("use_fallback", False):
                metrics_registry.increment_fallback(service_name)
            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            metrics_registry.increment_request(service_name)
            if kwargs.get("use_fallback", False):
                metrics_registry.increment_fallback(service_name)
            return func(*args, **kwargs)

        import inspect

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper

    return decorator
