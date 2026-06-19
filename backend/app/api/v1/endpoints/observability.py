
from fastapi import APIRouter

from backend.app.observability.dto.health_models import HealthResponse
from backend.app.observability.dto.metrics_models import (
    MetricsResponse,
    OverviewResponse,
)
from backend.app.observability.services.observability_service import (
    observability_service,
)
from backend.app.observability.services.performance_service import performance_service

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def get_health():
    return observability_service.get_health()


@router.get("/health/detailed", response_model=HealthResponse)
async def get_health_detailed():
    return observability_service.get_health()


@router.get("/health/readiness")
async def get_health_readiness():
    return {"status": "ready"}


@router.get("/health/liveness")
async def get_health_liveness():
    return {"status": "alive"}


@router.get("/metrics/overview", response_model=OverviewResponse)
async def get_metrics_overview():
    return observability_service.get_all_metrics()


@router.get("/metrics/models", response_model=MetricsResponse)
async def get_metrics_models():
    # Return an aggregate or a specific model for demo
    return observability_service.get_service_metrics("congestion_model")


@router.get("/metrics/streaming", response_model=MetricsResponse)
async def get_metrics_streaming():
    return observability_service.get_service_metrics("streaming_engine")


@router.get("/metrics/genai", response_model=MetricsResponse)
async def get_metrics_genai():
    return observability_service.get_service_metrics("genai_provider")


@router.get("/metrics/system", response_model=MetricsResponse)
async def get_metrics_system():
    return observability_service.get_service_metrics("api")


@router.get("/metrics/performance")
async def get_metrics_performance():
    return performance_service.get_performance_summary()


@router.get("/metrics/failures")
async def get_metrics_failures():
    return observability_service.get_recent_failures()


@router.get("/metrics/latency")
async def get_metrics_latency():
    # Helper to get specific latencies quickly
    return observability_service.get_all_metrics().get("latencies", {})


@router.get("/metrics/providers")
async def get_metrics_providers():
    return {
        "gemini": observability_service.get_service_metrics("gemini"),
        "groq": observability_service.get_service_metrics("groq"),
    }
