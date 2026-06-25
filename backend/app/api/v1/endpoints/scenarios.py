"""Scenario Catalog REST endpoints.

Exposes the demo scenario registry grouped by the hackathon theme taxonomy
(PLANNED vs UNPLANNED). Lets the frontend render a tabbed demo panel instead
of a hard-coded incident list — directly addressing Gap 1 (planned events
under-representation).
"""

from fastapi import APIRouter, Depends, HTTPException, Query

from backend.app.scenarios import (
    ScenarioCatalogDTO,
    ScenarioCategory,
    ScenarioDefinitionDTO,
    scenario_catalog,
)
from backend.app.scenarios.scenario_catalog import ScenarioCatalog

router = APIRouter()


def get_scenario_catalog() -> ScenarioCatalog:
    """Dependency-injectable accessor (defaults to the module singleton)."""
    return scenario_catalog


@router.get("", response_model=ScenarioCatalogDTO)
async def get_catalog(
    catalog: ScenarioCatalog = Depends(get_scenario_catalog),
) -> ScenarioCatalogDTO:
    """Return the full catalog grouped by category."""
    return catalog.as_catalog_dto()


@router.get("/by-category", response_model=list[ScenarioDefinitionDTO])
async def get_by_category(
    category: ScenarioCategory = Query(..., description="PLANNED or UNPLANNED"),
    catalog: ScenarioCatalog = Depends(get_scenario_catalog),
) -> list[ScenarioDefinitionDTO]:
    """Return scenarios for a single category."""
    return catalog.by_category(category)


@router.get("/{scenario_id}", response_model=ScenarioDefinitionDTO)
async def get_scenario(
    scenario_id: str,
    catalog: ScenarioCatalog = Depends(get_scenario_catalog),
) -> ScenarioDefinitionDTO:
    """Fetch a single scenario definition by id."""
    for scenario in catalog.all():
        if scenario.id == scenario_id:
            return scenario
    raise HTTPException(status_code=404, detail=f"Scenario '{scenario_id}' not found")
