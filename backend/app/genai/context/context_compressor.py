from typing import Any


class ContextCompressor:
    """
    Critically reduces token usage by extracting only the most relevant operational data.
    Never sends raw datasets to the LLM.
    """

    def compress(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        compressed = {}

        # Limit top incidents (max 3)
        incidents = raw_data.get("incidents", [])
        if isinstance(incidents, list):
            compressed["top_incidents"] = [
                {
                    "id": inc.get("id"),
                    "severity": inc.get("severity"),
                    "type": inc.get("type"),
                }
                for inc in incidents[:3]
            ]

        # Top recommendations (max 3)
        recommendations = raw_data.get("recommendations", [])
        if isinstance(recommendations, list):
            compressed["top_recommendations"] = recommendations[:3]

        # GORI
        compressed["current_gori"] = raw_data.get("gori_score", 0.0)

        # Simulation Result Summary
        sim = raw_data.get("simulation")
        if sim:
            compressed["simulation_summary"] = {
                "response_time_reduction": sim.get("improvements", {}).get(
                    "response_time_reduction_mins"
                ),
                "congestion_reduction_pct": sim.get("improvements", {}).get(
                    "congestion_reduction_pct"
                ),
            }

        compressed["confidence_score"] = raw_data.get("confidence", 0.85)

        return compressed


context_compressor = ContextCompressor()
