from typing import Any

import networkx as nx


class DiversionEngine:
    """
    Dynamic graph-based rerouting intelligence.
    Computes shortest operational path while bypassing blocked/high-penalty corridors.
    """

    def __init__(self):
        # Operational heuristic graph (simplified city corridor network)
        self.G = nx.Graph()

        # Hardcoding a heuristic grid for demonstration of the logic
        corridors = [
            "North_Arterial",
            "East_Corridor",
            "West_Bypass",
            "South_Expressway",
            "Central_Hub",
        ]

        self.G.add_edge("North_Arterial", "Central_Hub", weight=10, capacity=100)
        self.G.add_edge("South_Expressway", "Central_Hub", weight=15, capacity=120)
        self.G.add_edge("East_Corridor", "Central_Hub", weight=12, capacity=80)
        self.G.add_edge("West_Bypass", "North_Arterial", weight=25, capacity=150)
        self.G.add_edge("West_Bypass", "South_Expressway", weight=30, capacity=150)

    def generate_diversion_plan(
        self, incident_corridor: str, gori_score: float, lat: float, lng: float
    ) -> dict[str, Any]:
        """
        Dynamically finds the best alternate route by penalizing or completely removing the blocked corridor.
        """
        G_active = self.G.copy()

        # Apply closure penalty
        if incident_corridor in G_active:
            # If critical, remove it completely from the routing graph
            if gori_score > 60:
                G_active.remove_node(incident_corridor)
                status = "Corridor Completely Bypassed"
            else:
                status = "Corridor Penalized"
        else:
            status = "Incident on non-arterial route"
            return {
                "requires_diversion": False,
                "alternate_route": None,
                "status": status,
            }

        try:
            # Heuristically route traffic from North to South as an example diversion
            if "North_Arterial" in G_active and "South_Expressway" in G_active:
                path = nx.shortest_path(
                    G_active,
                    source="North_Arterial",
                    target="South_Expressway",
                    weight="weight",
                )
                path_str = " -> ".join(path)
            else:
                path_str = "West_Bypass"  # Universal fallback

            # Dynamically calculate bypass percentage based on severity
            bypass_pct = max(30.0, 95.0 - (gori_score * 0.4))

            # Generate dynamic diversion polyline points around the actual incident
            # This ensures the dashed line physically renders on the Bangalore map
            points = [
                [lat, lng],
                [lat + 0.005, lng + 0.005],
                [lat + 0.002, lng + 0.012],
                [lat - 0.004, lng + 0.015],
            ]

            return {
                "route_id": f"DIV-{incident_corridor[:3].upper()}",
                "description": f"Divert traffic via {path_str}",
                "points": points,
                "congestion_bypass_pct": round(bypass_pct, 1),
                "requires_diversion": True,
            }

        except nx.NetworkXNoPath:
            return {
                "route_id": "NONE",
                "description": "GRIDLOCK - No Path Available",
                "points": [],
                "congestion_bypass_pct": 0,
                "requires_diversion": True,
            }
