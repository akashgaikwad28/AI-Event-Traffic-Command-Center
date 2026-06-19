from typing import Any

from backend.app.resource_optimization.contracts.optimization_contracts import (
    OperationalConstraintsContract,
)


class ConstraintsEngine:
    """
    Validates operational constraints for realistic response scenarios.
    """

    def __init__(self, constraints: OperationalConstraintsContract = None):
        self.constraints = constraints or OperationalConstraintsContract()

    def validate_deployment(
        self, requested_officers: int, requested_barricades: int
    ) -> dict[str, Any]:
        """
        Validates if the requested resources are within limits.
        If not, returns the capped available resources to force plan adjustment.
        """
        available_officers = max(
            0,
            self.constraints.max_available_officers
            - self.constraints.active_deployed_officers,
        )
        available_barricades = max(
            0, self.constraints.max_barricades - self.constraints.active_barricades
        )

        is_valid = True
        allocated_officers = requested_officers
        allocated_barricades = requested_barricades

        if requested_officers > available_officers:
            is_valid = False
            allocated_officers = available_officers

        if requested_barricades > available_barricades:
            is_valid = False
            allocated_barricades = available_barricades

        return {
            "is_valid": is_valid,
            "allocated_officers": allocated_officers,
            "allocated_barricades": allocated_barricades,
            "shortage_warning": not is_valid,
        }
