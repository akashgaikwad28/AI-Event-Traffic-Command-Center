from typing import Any

from fastapi import APIRouter, HTTPException

from backend.app.genai.providers.provider_router import provider_router
from backend.app.genai.schemas.genai_models import (
    ChatRequest,
    ChatResponse,
    NarratorRequest,
    NarratorResponse,
    ReportRequest,
    ReportResponse,
)
from backend.app.genai.services.copilot_orchestrator import copilot_orchestrator
from backend.app.genai.services.demo_narrator_service import demo_narrator_service
from backend.app.genai.services.report_service import report_service

router = APIRouter()


@router.post("/copilot/chat", response_model=ChatResponse)
async def copilot_chat(request: ChatRequest):
    try:
        response, provider = await copilot_orchestrator.process_chat(
            request.query, request.mode
        )
        return ChatResponse(
            query=request.query,
            explanation=response,
            confidence=0.92,
            sources=[f"GridWise AI Copilot ({provider})"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-report", response_model=ReportResponse)
async def generate_report(request: ReportRequest):
    try:
        markdown = await report_service.generate_report(
            request.report_type, request.data
        )
        return ReportResponse(
            markdown_content=markdown, report_type=request.report_type
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/demo-narration", response_model=NarratorResponse)
async def generate_demo_narration(request: NarratorRequest):
    try:
        narration = await demo_narrator_service.generate_narration(
            request.simulation_result
        )
        return NarratorResponse(narration_text=narration)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/providers/status")
async def get_providers_status():
    return {
        "gemini": "active",
        "groq": "standby",
        "diffusion_gemma": "standby",
        "live_mode": provider_router.enable_live,
    }


# Mock endpoints for the other required endpoints that map to the generic chat/report flows
@router.post("/explain_incident")
async def explain_incident(data: dict[str, Any]):
    res, provider = await copilot_orchestrator.process_chat(
        "Explain this incident.", "DISPATCHER"
    )
    return {"explanation": res, "provider": provider}


@router.post("/explain-gori")
async def explain_gori(data: dict[str, Any]):
    res, provider = await copilot_orchestrator.process_chat(
        "Why is GORI high?", "ANALYST"
    )
    return {"explanation": res, "provider": provider}


@router.post("/generate-alert")
async def generate_alert(data: dict[str, Any]):
    return {"alert_level": "HIGH", "message": "Risk detected."}


@router.post("/deployment-summary")
async def deployment_summary(data: dict[str, Any]):
    res, provider = await copilot_orchestrator.process_chat(
        "Summarize deployment.", "EXECUTIVE"
    )
    return {"summary": res, "provider": provider}


@router.post("/executive-brief")
async def executive_brief(data: dict[str, Any]):
    return await generate_report(
        ReportRequest(report_type="EXECUTIVE_BRIEF", data=data)
    )


@router.post("/incident-summary")
async def incident_summary(data: dict[str, Any]):
    return await generate_report(
        ReportRequest(report_type="INCIDENT_REPORT", data=data)
    )


@router.post("/simulation-explanation")
async def simulation_explanation(data: dict[str, Any]):
    res, provider = await copilot_orchestrator.process_chat(
        "Explain the simulation impact.", "EXECUTIVE"
    )
    return {"explanation": res, "provider": provider}
