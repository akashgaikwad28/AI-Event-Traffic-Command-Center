import time
from typing import Any

from backend.app.copilot.orchestrator.context_grounding import context_grounding_engine
from backend.app.genai.logging.genai_logger import genai_logger
from backend.app.genai.providers.provider_router import provider_router


class ExplainabilityEngine:
    """
    Core engine responsible for translating raw ML outputs into operational narratives.
    """

    async def explain_incident(
        self, incident_id: str, query: str, raw_context: dict[str, Any]
    ) -> tuple[str, float, list[str]]:
        """
        Explains an incident using grounded context and Gemini fallback handling.
        """
        start_time = time.time()

        # 1. Ground the context
        safe_context = context_grounding_engine.build_incident_context(
            incident_id, raw_context
        )

        # 2. Extract Confidence
        # (In a real system, we'd query the Random Forest model's predict_proba)
        confidence_score = 0.94 if raw_context.get("gori_score", 0) > 80 else 0.85

        # 3. Construct System Prompt with Human-in-the-Loop constraints
        prompt = f"""
        You are the GridWise Operational Intelligence Copilot.
        Your role is to act as an authoritative operational narrator.

        Context Data (Source of Truth):
        {safe_context}

        User Query:
        {query}

        RULES:
        1. Base your answer STRICTLY on the Context Data provided.
        2. Do not hallucinate statistics or locations.
        3. If asked why an action was taken, cite the GORI severity or Spread Risk from the context.
        4. End your response with a brief disclaimer: "Recommendations are advisory and intended to assist traffic command operators."
        """

        # 4. Generate Output via existing abstracted provider
        try:
            raw_output, provider = await provider_router.generate(prompt, raw_context)
        except Exception as e:
            # Fallback logic
            raw_output = f"System Error: Unable to generate explanation. Proceed with standard operational protocols. Details: {str(e)}"
            provider = "System Fallback"
            confidence_score = 0.0

        # 5. Telemetry Logging (Audit Logging)
        latency_ms = int((time.time() - start_time) * 1000)
        tokens = int(len(prompt + raw_output) * 0.25)

        genai_logger.copilot_response_generated(
            provider=provider,
            mode="EXPLAINABILITY",
            latency_ms=latency_ms,
            estimated_tokens=tokens,
            fallback_triggered=(provider == "System Fallback"),
        )

        sources = [
            "XGBoost Congestion Model (GORI)",
            "Random Forest Deployment Model",
            f"LLM Narrator ({provider})",
        ]

        return raw_output, confidence_score, sources


explainability_engine = ExplainabilityEngine()
