from typing import Any

from pydantic import BaseModel, ConfigDict


class ChatRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    query: str
    mode: str  # EXECUTIVE, DISPATCHER, ANALYST


class ChatResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    query: str
    explanation: str
    confidence: float
    sources: list[str]


class ReportRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    report_type: str  # EXECUTIVE_BRIEF, INCIDENT_REPORT, SHIFT_HANDOVER, DAILY_INTELLIGENCE, SIMULATION_IMPACT
    data: dict[str, Any]


class ReportResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    markdown_content: str
    report_type: str


class NarratorRequest(BaseModel):
    model_config = ConfigDict(frozen=True)
    scenario_id: str
    simulation_result: dict[str, Any]


class NarratorResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    narration_text: str
    audio_url: str | None = None
