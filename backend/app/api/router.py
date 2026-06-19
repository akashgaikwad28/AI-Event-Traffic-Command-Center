from fastapi import APIRouter

from backend.app.api.v1.endpoints import (
    analytics,
    events,
    genai,
    health,
    observability,
    optimization,
    predictions,
    simulation,
    stream,
)

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(events.router, prefix="/events", tags=["Events"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(
    predictions.router, prefix="/predictions", tags=["Predictions"]
)
api_router.include_router(
    optimization.router, prefix="/optimization", tags=["Optimization"]
)
api_router.include_router(stream.router, prefix="/stream", tags=["Stream"])
api_router.include_router(simulation.router, prefix="/simulation", tags=["Simulation"])
api_router.include_router(genai.router, prefix="/genai", tags=["GenAI"])
api_router.include_router(
    observability.router, prefix="/observability", tags=["Observability"]
)
