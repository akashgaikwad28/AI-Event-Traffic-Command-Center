from typing import Any

from backend.app.resource_optimization.contracts.optimization_contracts import (
    OptimizationRequestDTO,
)


class IncidentPlaybookEngine:
    """
    Enterprise Operational Playbook Engine.
    Maps complex incident profiles to predefined response templates.
    """

    def fetch_playbook(self, request: OptimizationRequestDTO) -> dict[str, Any]:

        playbook = {
            "playbook_name": "Standard Operational Procedure",
            "escalation_protocol": "Standard",
            "predefined_actions": [],
        }

        if (
            request.heavy_vehicle_involved
            and request.is_rush_hour
            and request.hotspot_recurrence > 0.5
        ):
            playbook["playbook_name"] = "PLAYBOOK-OMEGA: Heavy Vehicle Cascade Risk"
            playbook["escalation_protocol"] = "Automatic Multi-Agency Response"
            playbook["predefined_actions"] = [
                "Immediate dispatch of Class-A Heavy Tow",
                "Pre-position mobile traffic units at upstream junctions",
                "Broadcast regional diversion advisory",
            ]

        elif request.congestion_severity == "Critical":
            playbook["playbook_name"] = "PLAYBOOK-ALPHA: Critical Congestion Relief"
            playbook["escalation_protocol"] = "Rapid Diversion"
            playbook["predefined_actions"] = [
                "Activate dynamic message signs for diversion",
                "Deploy manual traffic control at chokepoints",
            ]

        return playbook
