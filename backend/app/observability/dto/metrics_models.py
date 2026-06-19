from pydantic import BaseModel, ConfigDict


class MetricsResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    request_count: int
    success_count: int
    failure_count: int
    fallback_count: int
    avg_latency: float
    p50_latency: float
    p95_latency: float
    p99_latency: float


class OverviewResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    requests: dict[str, int]
    failures: dict[str, int]
    latencies: dict[str, dict[str, float]]
