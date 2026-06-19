from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api.v1.schemas.congestion import CongestionCreate, CongestionResponse
from backend.app.db.session import get_db
from backend.app.services.congestion_service import congestion_service
from backend.app.utils.pagination import PaginatedResponse, paginate
from backend.app.utils.response import APIResponse, success_response

router = APIRouter()


@router.post("", response_model=APIResponse[CongestionResponse], status_code=201)
async def create_congestion_prediction(
    prediction_in: CongestionCreate, db: AsyncSession = Depends(get_db)
) -> APIResponse[CongestionResponse]:
    prediction = await congestion_service.create_prediction(db, prediction_in)
    return success_response(CongestionResponse.model_validate(prediction))


@router.get("", response_model=APIResponse[PaginatedResponse[CongestionResponse]])
async def list_congestion_predictions(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> APIResponse[PaginatedResponse[CongestionResponse]]:
    items, total = await congestion_service.list_predictions(db, page, page_size)
    paginated = paginate(
        [CongestionResponse.model_validate(i) for i in items], total, page, page_size
    )
    return success_response(paginated)
