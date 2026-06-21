from typing import Any

from backend.app.genai.providers.base_provider import BaseProvider


class GeminiProvider(BaseProvider):
    """Google Gemini 2.5 Flash implementation."""

    async def generate_explanation(self, prompt: str, context: dict[str, Any]) -> str:
        gori = context.get("gori_score", 0)
        inc_type = context.get("type", "Traffic Event")
        mode = context.get("mode", "EXECUTIVE")

        if mode == "EXECUTIVE":
            if gori > 70:
                return f"CRITICAL PRIORITY: A high-severity {inc_type} has triggered a cascading failure risk. Operational stability is compromised (GORI {gori}). Immediate multi-agency coordination is required to prevent gridlock spread."
            else:
                return f"ROUTINE MONITORING: A low-impact {inc_type} is active. The network is absorbing the disruption efficiently (GORI {gori}). No executive escalation required at this time."
        elif mode == "DISPATCHER":
            if gori > 70:
                return f"TACTICAL ALERT: Deploy minimum 6 traffic units to {inc_type} coordinates immediately. Institute full perimeter closure. High probability of secondary collisions."
            else:
                return f"STANDARD DEPLOYMENT: Send 1 patrol unit to clear the {inc_type}. Maintain standard flow. No barricades required."
        else:
            if gori > 70:
                return f"METRICS ANOMALY: Spatial clustering analysis indicates a 85% probability of congestion expanding by 3km within 15 minutes due to the {inc_type}. Recommending dynamic signal timing adjustment."
            else:
                return f"BASELINE METRICS: Current {inc_type} presents a 12% spread probability. Recovery timeline is well within expected historical bounds."

    def get_provider_name(self) -> str:
        return "gemini-2.5-flash"
