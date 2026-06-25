"""Strict Pydantic contracts for the scenario catalog.

These DTOs are frozen (immutable) to match the project's contract style used
across `resource_optimization/` and `analytics/`.
"""

from enum import Enum

from pydantic import BaseModel, ConfigDict


class ScenarioCategory(str, Enum):
    """Top-level theme taxonomy. Maps directly to the hackathon problem statement."""

    PLANNED = "PLANNED"
    UNPLANNED = "UNPLANNED"


class ScenarioPayloadDTO(BaseModel):
    """Input payload injected into the simulation + optimization engines."""

    model_config = ConfigDict(frozen=True)
    lat: float
    lng: float
    gori: int
    hvi: bool = False
    rush: bool = False


class ScenarioDefinitionDTO(BaseModel):
    """A single demonstration scenario.

    `expected_outcome` documents what the AI engines should produce so judges
    can validate the demo against the documented expectation (mirrors the
    "10 Demo Scenarios" cheat sheet in DASHBOARD_EXPLANATION.md).
    """

    model_config = ConfigDict(frozen=True)
    id: str
    name: str
    category: ScenarioCategory
    subtype: str  # e.g. "Political Rally", "Sports Egress", "Vehicle Stall"
    description: str
    sim_type: str  # SimulationScenario backend identifier
    icon: str  # lucide-react icon name used by the frontend
    payload: ScenarioPayloadDTO
    expected_outcome: str


class ScenarioCatalogDTO(BaseModel):
    """Grouped catalog served to the frontend."""

    model_config = ConfigDict(frozen=True)
    planned: list[ScenarioDefinitionDTO]
    unplanned: list[ScenarioDefinitionDTO]
    counts: dict[str, int]
