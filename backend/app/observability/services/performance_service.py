from typing import Any

from backend.app.observability.metrics.metrics_registry import metrics_registry


class PerformanceService:
    """Calculates top slow endpoints, top failing models, etc."""

    def get_performance_summary(self) -> dict[str, Any]:
        all_metrics = metrics_registry.get_all_metrics()

        latencies = all_metrics.get("latencies", {})
        failures = all_metrics.get("failures", {})

        # Sort latencies
        sorted_latencies = sorted(
            latencies.items(), key=lambda item: item[1], reverse=True
        )
        top_slow = [
            {"service": k, "avg_latency_ms": v} for k, v in sorted_latencies[:5]
        ]

        # Sort failures
        sorted_failures = sorted(
            failures.items(), key=lambda item: item[1], reverse=True
        )
        top_failing = [
            {"service": k, "failure_count": v} for k, v in sorted_failures[:5]
        ]

        return {"top_slow_services": top_slow, "top_failing_services": top_failing}


performance_service = PerformanceService()
