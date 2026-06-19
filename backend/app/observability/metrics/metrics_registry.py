import statistics
from collections import defaultdict
from typing import Any


class MetricsRegistry:
    """
    In-memory metrics abstraction. Designed to be easily plugged into a Prometheus exporter later.
    Tracks model-specific metrics like p95 and p99 latency.
    """

    def __init__(self):
        self.requests = defaultdict(int)
        self.successes = defaultdict(int)
        self.failures = defaultdict(int)
        self.fallbacks = defaultdict(int)
        self.latencies = defaultdict(list)

    def increment_request(self, service: str):
        self.requests[f"gridwise_{service}_requests_total"] += 1

    def increment_success(self, service: str):
        self.successes[f"gridwise_{service}_success_total"] += 1

    def increment_failure(self, service: str):
        self.failures[f"gridwise_{service}_failures_total"] += 1

    def increment_fallback(self, service: str):
        self.fallbacks[f"gridwise_{service}_fallbacks_total"] += 1

    def record_latency(self, service: str, latency_ms: int):
        self.latencies[f"gridwise_{service}_latency_ms"].append(latency_ms)
        # Prevent unbounded growth
        if len(self.latencies[f"gridwise_{service}_latency_ms"]) > 1000:
            self.latencies[f"gridwise_{service}_latency_ms"] = self.latencies[
                f"gridwise_{service}_latency_ms"
            ][-1000:]

    def get_service_metrics(self, service: str) -> dict[str, Any]:
        l_list = self.latencies.get(f"gridwise_{service}_latency_ms", [])
        return {
            "request_count": self.requests.get(f"gridwise_{service}_requests_total", 0),
            "success_count": self.successes.get(f"gridwise_{service}_success_total", 0),
            "failure_count": self.failures.get(f"gridwise_{service}_failures_total", 0),
            "fallback_count": self.fallbacks.get(
                f"gridwise_{service}_fallbacks_total", 0
            ),
            "avg_latency": statistics.mean(l_list) if l_list else 0.0,
            "p50_latency": (
                statistics.quantiles(l_list, n=2)[0]
                if len(l_list) >= 2
                else (statistics.mean(l_list) if l_list else 0.0)
            ),
            "p95_latency": (
                statistics.quantiles(l_list, n=20)[18]
                if len(l_list) >= 20
                else (statistics.mean(l_list) if l_list else 0.0)
            ),
            "p99_latency": (
                statistics.quantiles(l_list, n=100)[98]
                if len(l_list) >= 100
                else (statistics.mean(l_list) if l_list else 0.0)
            ),
        }

    def get_all_metrics(self) -> dict[str, Any]:
        # Return all in-memory metrics formatted for Grafana/Dashboard

        # Build detailed percentiles for all tracked latencies
        detailed_latencies = {}
        for key, l_list in self.latencies.items():
            # Strip prefix to get clean service name for dashboard
            service_name = key.replace("gridwise_", "").replace("_latency_ms", "")
            detailed_latencies[service_name] = {
                "avg_latency": statistics.mean(l_list) if l_list else 0.0,
                "p50_latency": (
                    statistics.quantiles(l_list, n=2)[0]
                    if len(l_list) >= 2
                    else (statistics.mean(l_list) if l_list else 0.0)
                ),
                "p95_latency": (
                    statistics.quantiles(l_list, n=20)[18]
                    if len(l_list) >= 20
                    else (statistics.mean(l_list) if l_list else 0.0)
                ),
                "p99_latency": (
                    statistics.quantiles(l_list, n=100)[98]
                    if len(l_list) >= 100
                    else (statistics.mean(l_list) if l_list else 0.0)
                ),
            }

        return {
            "requests": dict(self.requests),
            "failures": dict(self.failures),
            "latencies": detailed_latencies,
        }


metrics_registry = MetricsRegistry()
