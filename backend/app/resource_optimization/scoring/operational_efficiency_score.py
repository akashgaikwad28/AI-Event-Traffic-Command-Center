from typing import Any


def compute_efficiency_score(
    officers_allocated: int,
    barricades_allocated: int,
    congestion_reduction_pct: float,
    base_gori: float,
) -> dict[str, Any]:
    """
    Computes the Operational Efficiency Score for a deployment plan.
    High reduction with minimal resources = High efficiency.
    """
    # Total resource weight
    resource_cost = (officers_allocated * 2.0) + (barricades_allocated * 1.5)
    if resource_cost == 0:
        return {"efficiency_score": 0.0, "waste_score": 0.0}

    # Benefit derived
    operational_benefit = congestion_reduction_pct + (base_gori * 0.5)

    efficiency = min(100.0, round((operational_benefit / resource_cost) * 10, 1))

    # Waste metric: deploying massive resources for low impact
    waste_score = 0.0
    if resource_cost > 30 and congestion_reduction_pct < 10:
        waste_score = 100.0 - efficiency

    return {
        "efficiency_score": efficiency,
        "waste_score": waste_score,
        "resource_unit_cost": resource_cost,
    }
