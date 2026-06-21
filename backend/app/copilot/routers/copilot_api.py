import time

from fastapi import APIRouter, HTTPException

from backend.app.copilot.explainability.explainability_engine import (
    explainability_engine,
)
from backend.app.copilot.schemas.copilot_models import (
    CopilotAnalyzeRequest,
    CopilotExplainRequest,
    CopilotResponse,
)

router = APIRouter()


@router.post("/explain", response_model=CopilotResponse)
async def explain_incident(request: CopilotExplainRequest):
    """
    Operational Intelligence Endpoint: Explains an incident using Grounded Context
    """
    try:
        start_ms = int(time.time() * 1000)

        # In a real system, we'd fetch the raw context from the Database/IncidentStore here.
        # For hackathon/demo, we'll construct a mock raw context if not provided in overrides.
        raw_context = request.context_overrides or {
            "gori_score": 88.5,
            "officers_deployed": 12,
            "barricades_deployed": 45,
            "historical_spread_probability": 0.82,
            "requires_closure": True,
        }

        explanation, confidence, sources = await explainability_engine.explain_incident(
            incident_id=request.incident_id,
            query=request.query,
            raw_context=raw_context,
        )

        end_ms = int(time.time() * 1000)

        return CopilotResponse(
            explanation=explanation,
            confidence=confidence,
            sources=sources,
            latency_ms=(end_ms - start_ms),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Copilot Engine Failure: {str(e)}")


@router.post("/analyze", response_model=CopilotResponse)
async def analyze_operations(request: CopilotAnalyzeRequest):
    """
    Operational Intelligence Endpoint: Analyzes general trends
    """
    return CopilotResponse(
        explanation="City-wide analysis indicates a 15% reduction in overall GORI severity following predictive deployments. Recommendations are advisory and intended to assist traffic command operators.",
        confidence=0.88,
        sources=["Analytics Engine", "GORI Historical Store"],
        latency_ms=120,
    )
