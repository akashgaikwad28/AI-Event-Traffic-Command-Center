from typing import Any

import pandas as pd
from fastapi import APIRouter, Depends, Query

from backend.app.analytics.analytics_engine import AnalyticsEngine

router = APIRouter()


# Dependency
def get_analytics_engine() -> AnalyticsEngine:
    return AnalyticsEngine()


@router.get("/overview")
async def get_analytics_overview(
    time_window: int = Query(24, description="Hours to look back"),
    engine: AnalyticsEngine = Depends(get_analytics_engine),
) -> dict[str, Any]:
    """
    Returns the comprehensive Executive Command Center snapshot.
    Supports dashboard filtering via query params.
    """
    # In production, this would async-fetch from DB Repository.
    # For now, we mock empty dataframes to satisfy the contract.
    mock_current = pd.DataFrame()
    mock_historical = pd.DataFrame()

    snapshot = engine.generate_command_center_snapshot(mock_current, mock_historical)

    return {
        "success": True,
        "filters": {"time_window_hours": time_window},
        "data": snapshot,
    }


@router.get("/city-health")
async def get_city_health(engine: AnalyticsEngine = Depends(get_analytics_engine)):
    """Fast-path endpoint strictly for the top-line health score."""
    mock_current = pd.DataFrame()
    kpis = engine.kpis.generate_executive_kpis(mock_current)
    return {"success": True, "data": kpis}
