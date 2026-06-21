from typing import Any

from pydantic import BaseModel, Field


class CopilotExplainRequest(BaseModel):
    incident_id: str = Field(..., description="The ID of the incident to explain.")
    query: str = Field(
        ...,
        description="The specific question about the incident (e.g., 'Why was this classified as CRITICAL?').",
    )
    context_overrides: dict[str, Any] | None = Field(
        default=None, description="Optional overrides for simulation scenarios."
    )


class CopilotAnalyzeRequest(BaseModel):
    query: str = Field(
        ...,
        description="The analytical query (e.g., 'Analyze the city-wide congestion trend').",
    )
    scope: str = Field(
        default="CITY_WIDE",
        description="Scope of analysis: CITY_WIDE or INCIDENT_SPECIFIC.",
    )


class CopilotResponse(BaseModel):
    explanation: str = Field(
        ..., description="The grounded, operational explanation from the Copilot."
    )
    confidence: float = Field(
        ..., description="Confidence score of the explanation (0.0 to 1.0)."
    )
    sources: list[str] = Field(
        ..., description="The ML models or rules used to ground this answer."
    )
    latency_ms: int = Field(..., description="Time taken to generate the response.")
