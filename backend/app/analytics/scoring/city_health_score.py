def compute_city_health(
    active_incidents: int, avg_gori: float, sla_breach_rate: float
) -> float:
    """
    Computes the City Operational Health Score (0-100).
    100 = Perfect Flow, 0 = Gridlock.
    """
    base_health = 100.0

    # Penalize based on average operational severity (GORI)
    base_health -= avg_gori * 0.4

    # Penalize based on volume of active incidents
    incident_penalty = min(30.0, active_incidents * 0.5)
    base_health -= incident_penalty

    # Penalize based on SLA clearance failures
    base_health -= sla_breach_rate * 0.3

    return max(0.0, round(base_health, 1))


def compute_operational_pressure(
    active_incidents: int, high_priority_count: int
) -> float:
    """Computes load pressure on dispatchers (0-100)."""
    base = min(100.0, active_incidents * 2.0)
    priority_multiplier = 1.0 + (high_priority_count / max(1, active_incidents))
    return min(100.0, round(base * priority_multiplier, 1))
