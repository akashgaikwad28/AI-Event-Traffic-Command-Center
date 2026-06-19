from typing import Any

from backend.app.observability.metrics.metrics_registry import metrics_registry
from backend.app.observability.monitoring.failure_tracker import failure_tracker
from backend.app.observability.monitoring.health_monitor import health_monitor


class ObservabilityService:
    def get_health(self) -> dict[str, Any]:
        return health_monitor.get_health_status()

    def get_service_metrics(self, service_name: str) -> dict[str, Any]:
        return metrics_registry.get_service_metrics(service_name)

    def get_all_metrics(self) -> dict[str, Any]:
        return metrics_registry.get_all_metrics()

    def get_recent_failures(self) -> list[dict[str, Any]]:
        return failure_tracker.get_recent_failures()


observability_service = ObservabilityService()
