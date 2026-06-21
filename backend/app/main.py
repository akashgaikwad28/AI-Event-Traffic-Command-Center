from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.app.api.router import api_router
from backend.app.core.config import get_settings
from backend.app.api.v1.endpoints import (
    analytics,
    congestion,
    events,
    genai,
    health,
    observability,
    optimization,
    predictions,
    simulation,
    stream,
)
from backend.app.copilot.routers import copilot_api
from backend.app.core.logger import get_logger, setup_logging
from backend.app.core.middleware import (
    CorrelationIdMiddleware,
    setup_cors_middleware,
)
from backend.app.exceptions.handlers import add_exception_handlers

settings = get_settings()
setup_logging()
logger = get_logger("app")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    logger.info(
        "Starting up application", env=settings.app_env, version=settings.version
    )
    yield
    logger.info("Shutting down application")


app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description=settings.description,
    debug=settings.debug,
    lifespan=lifespan,
    openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    docs_url=f"{settings.api_v1_prefix}/docs",
    redoc_url=f"{settings.api_v1_prefix}/redoc",
)

setup_cors_middleware(app)
app.add_middleware(CorrelationIdMiddleware)
add_exception_handlers(app)
app.include_router(api_router, prefix=settings.api_v1_prefix)
app.include_router(genai.router, prefix="/api/v1/genai", tags=["GenAI"])
app.include_router(copilot_api.router, prefix="/api/v1/copilot", tags=["Copilot"])

from fastapi.responses import RedirectResponse


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url=f"{settings.api_v1_prefix}/docs")
