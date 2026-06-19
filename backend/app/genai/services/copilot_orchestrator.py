import time

from backend.app.genai.context.context_builder import context_builder
from backend.app.genai.guards.hallucination_guard import hallucination_guard
from backend.app.genai.logging.genai_logger import genai_logger
from backend.app.genai.providers.provider_router import provider_router


class CopilotOrchestrator:
    """
    The Brain of the Copilot. Routes intents to internal engines before LLM execution.
    """

    async def process_chat(self, query: str, mode: str) -> str:
        start_time = time.time()
        # Step 1: Intent Routing (simplified for hackathon)
        intent = self._determine_intent(query)

        raw_data = {}
        sources = []

        # Step 2: Query background engines based on intent
        if intent == "risk_explanation":
            # Call Analytics & GORI Engines
            raw_data["gori_score"] = 84.5
            raw_data["incidents"] = [
                {"id": "INC-123", "severity": "high", "type": "accident"}
            ]
            sources = ["GORI Engine", "Analytics Engine"]
        elif intent == "simulation_impact":
            # Call Simulation & Resource Optimization Engines
            raw_data["recommendations"] = [{"type": "unit", "amount": 10}]
            raw_data["simulation"] = {
                "improvements": {
                    "response_time_reduction_mins": 15,
                    "congestion_reduction_pct": 35,
                }
            }
            sources = ["Simulation Engine", "Resource Optimization Engine"]
        else:
            # Fallback to general executive snapshot
            raw_data["gori_score"] = 62.0
            sources = ["Analytics Engine"]

        # Step 3: Compress context
        context = context_builder.build_context(raw_data)

        # Step 4: Generate via Router with strict Anti-Hallucination guard
        prompt = f"""
        Mode: {mode}
        Query: {query}
        Context: {context}

        CRITICAL INSTRUCTION: You are GridWise AI, a tactical AI orchestrator.
        You MUST base your entire answer ONLY on the provided Context.
        DO NOT invent, hallucinate, or assume any statistics, resource numbers, or geographic locations that are not explicitly present in the Context.
        If the Context does not contain the answer, simply state: 'Data unavailable in current ML optimization context.'
        """
        raw_output, provider = await provider_router.generate(prompt, context)

        # Step 5: Guardrails
        safe_output = hallucination_guard.validate(raw_output, context)

        latency_ms = int((time.time() - start_time) * 1000)
        # Approximate tokens 1 char ~ 0.25 tokens
        tokens = int(len(prompt + safe_output) * 0.25)

        is_fallback = provider != "Gemini AI"

        # We now know the exact provider used here since router handles fallback.
        genai_logger.copilot_response_generated(
            provider=provider,
            mode=mode,
            latency_ms=latency_ms,
            estimated_tokens=tokens,
            fallback_triggered=is_fallback,
        )

        return safe_output, provider

    def _determine_intent(self, query: str) -> str:
        query_lower = query.lower()
        if (
            "deploy" in query_lower
            or "if we" in query_lower
            or "simulate" in query_lower
        ):
            return "simulation_impact"
        elif "why" in query_lower or "risk" in query_lower or "gori" in query_lower:
            return "risk_explanation"
        return "general_summary"


copilot_orchestrator = CopilotOrchestrator()
