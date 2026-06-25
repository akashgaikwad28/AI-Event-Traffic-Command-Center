"""Scenario Catalog module.

Provides a typed registry of demonstration scenarios grouped by the hackathon
theme taxonomy: PLANNED events (rallies, festivals, sports, construction) and
UNPLANNED incidents (accidents, stalls, weather, equipment failures).
"""

from backend.app.scenarios.scenario_catalog import (
    PLANNED_SCENARIOS,
    UNPLANNED_SCENARIOS,
    scenario_catalog,
)
from backend.app.scenarios.scenario_models import (
    ScenarioCatalogDTO,
    ScenarioCategory,
    ScenarioDefinitionDTO,
)

__all__ = [
    "ScenarioCatalogDTO",
    "ScenarioCategory",
    "ScenarioDefinitionDTO",
    "PLANNED_SCENARIOS",
    "UNPLANNED_SCENARIOS",
    "scenario_catalog",
]
