from fastapi import APIRouter

from backend.app.core.config import get_settings
from backend.app.utils.response import APIResponse, success_response

router = APIRouter()
settings = get_settings()


@router.get("", response_model=APIResponse[dict[str, str]])
async def health_check() -> APIResponse[dict[str, str]]:
    """Check application health status."""
    return success_response(
        data={
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.version,
        },
        message="Service is fully operational",
    )
