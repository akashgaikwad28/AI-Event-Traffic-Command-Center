import json
from typing import Any


class ContextGroundingEngine:
    """
    RAG Restriction Layer: Ensures the LLM only receives strict, token-safe
    operational context from internal GridWise ML pipelines and simulations.
    """

    def build_incident_context(self, incident_id: str, raw_data: dict[str, Any]) -> str:
        """
        Extracts only the operationally relevant data points from a raw incident payload
        to prevent hallucination and token bloat.
        """
        # Defensive extraction
        gori_score = raw_data.get("gori_score", 0.0)
        officers_deployed = raw_data.get("officers_deployed", 0)
        barricades_deployed = raw_data.get("barricades_deployed", 0)
        spread_probability = raw_data.get("historical_spread_probability", 0.0)
        requires_closure = raw_data.get("requires_closure", False)

        # Operational Snapshot
        context = {
            "incident_id": incident_id,
            "gori_severity": gori_score,
            "classification": (
                "CRITICAL"
                if gori_score > 75
                else ("HIGH" if gori_score > 45 else "NORMAL")
            ),
            "recommended_officers": officers_deployed,
            "recommended_barricades": barricades_deployed,
            "spread_risk": f"{spread_probability * 100}%",
            "physical_closure_required": requires_closure,
        }

        # Deterministic Serialization
        return json.dumps(context, indent=2)


context_grounding_engine = ContextGroundingEngine()
