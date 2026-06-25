"""Scenario catalog: the single source of truth for demo scenarios.

Grouped by the hackathon theme taxonomy:
  - PLANNED: rallies, festivals, sports events, construction, marathons
  - UNPLANNED: accidents, stalls, weather events, equipment failures

The UNPLANNED set preserves the original 9 incidents (Peenya, HSR, Wilson
Garden, Sadashiva, Lalbagh, Jakkur, Kengeri, Whitefield, Hebbal) so existing
demo flows are untouched. The PLANNED set directly closes Gap 1: the theme
explicitly lists "Political rallies, festivals, sports events, construction"
as planned event drivers of congestion.
"""

from backend.app.scenarios.scenario_models import (
    ScenarioCatalogDTO,
    ScenarioCategory,
    ScenarioDefinitionDTO,
    ScenarioPayloadDTO,
)

# ---------------------------------------------------------------------------
# UNPLANNED INCIDENTS (preserved from the original DemoControls panel)
# ---------------------------------------------------------------------------
UNPLANNED_SCENARIOS: list[ScenarioDefinitionDTO] = [
    ScenarioDefinitionDTO(
        id="SCENARIO_1",
        name="Peenya Truck Stall",
        category=ScenarioCategory.UNPLANNED,
        subtype="Vehicle Stall",
        description="LCV breakdown on Highway",
        sim_type="CUSTOM_INCIDENT",
        icon="Car",
        payload=ScenarioPayloadDTO(
            lat=13.0400, lng=77.5180, gori=85, hvi=True, rush=True
        ),
        expected_outcome=(
            "CRITICAL. Maximum officers deployed, barricades required "
            "(heavy tow), immediate graph diversion."
        ),
    ),
    ScenarioDefinitionDTO(
        id="SCENARIO_2",
        name="HSR Heavy Vehicle",
        category=ScenarioCategory.UNPLANNED,
        subtype="Heavy Vehicle Blockage",
        description="Heavy vehicle blockage",
        sim_type="ACCIDENT_CASCADE",
        icon="AlertTriangle",
        payload=ScenarioPayloadDTO(
            lat=12.9218, lng=77.6451, gori=65, hvi=True, rush=False
        ),
        expected_outcome=(
            "MODERATE/HIGH. Barricades deployed due to heavy vehicle "
            "status, moderate officer count."
        ),
    ),
    ScenarioDefinitionDTO(
        id="SCENARIO_3",
        name="Wilson Garden Traffic",
        category=ScenarioCategory.UNPLANNED,
        subtype="Non-Corridor Incident",
        description="Non-corridor incident",
        sim_type="CUSTOM_INCIDENT",
        icon="Car",
        payload=ScenarioPayloadDTO(
            lat=12.9556, lng=77.5857, gori=45, hvi=False, rush=False
        ),
        expected_outcome="LOW. Standard dispatch, no barricades, minor flow relief.",
    ),
    ScenarioDefinitionDTO(
        id="SCENARIO_4",
        name="Sadashiva Tree Fall",
        category=ScenarioCategory.UNPLANNED,
        subtype="Obstruction",
        description="Tree blocking road",
        sim_type="CUSTOM_INCIDENT",
        icon="Wind",
        payload=ScenarioPayloadDTO(
            lat=13.0061, lng=77.5794, gori=75, hvi=False, rush=True
        ),
        expected_outcome=(
            "CRITICAL. High spread velocity due to rush hour, diversion "
            "heavily prioritized."
        ),
    ),
    ScenarioDefinitionDTO(
        id="SCENARIO_5",
        name="Lalbagh Bus Break",
        category=ScenarioCategory.UNPLANNED,
        subtype="Equipment Failure",
        description="Private bus stalled",
        sim_type="LIVE_REPLAY",
        icon="AlertTriangle",
        payload=ScenarioPayloadDTO(
            lat=12.9539, lng=77.5852, gori=35, hvi=True, rush=False
        ),
        expected_outcome=(
            "LOW GORI but Barricades triggered. Proves the AI logic knows "
            "buses need towing regardless of low initial traffic severity."
        ),
    ),
    ScenarioDefinitionDTO(
        id="SCENARIO_6",
        name="Jakkur Multi-Crash",
        category=ScenarioCategory.UNPLANNED,
        subtype="Multi-Crash Cascade",
        description="Amruthahalli accident",
        sim_type="ACCIDENT_CASCADE",
        icon="Zap",
        payload=ScenarioPayloadDTO(
            lat=13.0664, lng=77.5998, gori=96, hvi=True, rush=True
        ),
        expected_outcome=(
            "CATASTROPHIC. Spawns 3 cascading incidents. Total resource "
            "exhaustion, highest budget impact, maximum bypass routing."
        ),
    ),
    ScenarioDefinitionDTO(
        id="SCENARIO_7",
        name="Kengeri BMTC Fail",
        category=ScenarioCategory.UNPLANNED,
        subtype="Equipment Failure",
        description="BMTC bus broken down",
        sim_type="CUSTOM_INCIDENT",
        icon="Construction",
        payload=ScenarioPayloadDTO(
            lat=12.9328, lng=77.4879, gori=55, hvi=True, rush=False
        ),
        expected_outcome="MODERATE. Standard heavy-vehicle recovery protocols.",
    ),
    ScenarioDefinitionDTO(
        id="SCENARIO_9",
        name="Whitefield Flood",
        category=ScenarioCategory.UNPLANNED,
        subtype="Weather Event",
        description="Underpass water logging",
        sim_type="HISTORICAL_REPLAY",
        icon="Droplets",
        payload=ScenarioPayloadDTO(
            lat=13.0008, lng=77.6813, gori=92, hvi=False, rush=True
        ),
        expected_outcome=(
            "CRITICAL. Immediate graph rerouting required due to complete "
            "underpass failure."
        ),
    ),
    ScenarioDefinitionDTO(
        id="SCENARIO_10",
        name="Hebbal Flyover Stall",
        category=ScenarioCategory.UNPLANNED,
        subtype="Vehicle Stall",
        description="Vehicle starting problem",
        sim_type="LIVE_REPLAY",
        icon="Thermometer",
        payload=ScenarioPayloadDTO(
            lat=13.0418, lng=77.5947, gori=25, hvi=False, rush=False
        ),
        expected_outcome=(
            "NOMINAL. Proves the AI does not overreact. Minimal officers "
            "deployed, baseline dashboard state."
        ),
    ),
]

# ---------------------------------------------------------------------------
# PLANNED EVENTS (NEW — closes Gap 1)
# Theme: "Political rallies, festivals, sports events, construction activities"
# ---------------------------------------------------------------------------
PLANNED_SCENARIOS: list[ScenarioDefinitionDTO] = [
    ScenarioDefinitionDTO(
        id="SCENARIO_8",
        name="Chinnaswamy Match",
        category=ScenarioCategory.PLANNED,
        subtype="Sports Egress",
        description="Cricket match egress",
        sim_type="STADIUM_EVENT_EGRESS",
        icon="Shield",
        payload=ScenarioPayloadDTO(
            lat=12.9788, lng=77.5995, gori=82, hvi=False, rush=True
        ),
        expected_outcome=(
            "CRITICAL. Event-driven congestion. Prioritizes rapid clearance "
            "timelines to prevent gridlock."
        ),
    ),
    ScenarioDefinitionDTO(
        id="SCENARIO_11",
        name="Mall Bench Political Rally",
        category=ScenarioCategory.PLANNED,
        subtype="Political Rally",
        description="50,000-attendee rally egress",
        sim_type="STADIUM_EVENT_EGRESS",
        icon="Users",
        payload=ScenarioPayloadDTO(
            lat=12.9756, lng=77.6071, gori=90, hvi=False, rush=True
        ),
        expected_outcome=(
            "CRITICAL. Massive pedestrian-vehicle conflict zone. "
            "Pre-positioned barricades, full corridor diversion, surge "
            "officer deployment."
        ),
    ),
    ScenarioDefinitionDTO(
        id="SCENARIO_12",
        name="Lalbagh Flower Festival",
        category=ScenarioCategory.PLANNED,
        subtype="Festival",
        description="Weekend flower show crowd surge",
        sim_type="STADIUM_EVENT_EGRESS",
        icon="Flower",
        payload=ScenarioPayloadDTO(
            lat=12.9508, lng=77.5848, gori=78, hvi=False, rush=True
        ),
        expected_outcome=(
            "HIGH. Recurring festival hotspot. DBSCAN flags historical "
            "recurrence, staged parking diversion plan."
        ),
    ),
    ScenarioDefinitionDTO(
        id="SCENARIO_13",
        name="Outer Ring Road Marathon",
        category=ScenarioCategory.PLANNED,
        subtype="Public Gathering",
        description="City marathon road closure window",
        sim_type="HISTORICAL_REPLAY",
        icon="Activity",
        payload=ScenarioPayloadDTO(
            lat=12.9352, lng=77.6245, gori=70, hvi=False, rush=True
        ),
        expected_outcome=(
            "HIGH. Scheduled corridor closure. Time-boxed diversion plan "
            "with clearance forecast aligned to event end time."
        ),
    ),
    ScenarioDefinitionDTO(
        id="SCENARIO_14",
        name="Silk Board Construction",
        category=ScenarioCategory.PLANNED,
        subtype="Construction",
        description="Flyover construction lane closure",
        sim_type="CUSTOM_INCIDENT",
        icon="HardHat",
        payload=ScenarioPayloadDTO(
            lat=12.9177, lng=77.6223, gori=68, hvi=True, rush=True
        ),
        expected_outcome=(
            "HIGH. Persistent capacity reduction. Long-duration diversion "
            "routing + static barricade deployment."
        ),
    ),
    ScenarioDefinitionDTO(
        id="SCENARIO_15",
        name="Palace Ground Summit",
        category=ScenarioCategory.PLANNED,
        subtype="Political Summit",
        description="VIP movement + delegate egress",
        sim_type="STADIUM_EVENT_EGRESS",
        icon="Crown",
        payload=ScenarioPayloadDTO(
            lat=13.0067, lng=77.5803, gori=84, hvi=False, rush=True
        ),
        expected_outcome=(
            "CRITICAL. VIP security overlay. Corridor sterilization, "
            "multi-node diversion, maximum officer density."
        ),
    ),
]


class ScenarioCatalog:
    """Read-only accessor over the scenario registry.

    Kept as a class (not a plain dict) so it can later be backed by a database
    or remote config without changing call sites.
    """

    def __init__(
        self,
        planned: list[ScenarioDefinitionDTO] | None = None,
        unplanned: list[ScenarioDefinitionDTO] | None = None,
    ) -> None:
        self._planned = (
            list(planned) if planned is not None else list(PLANNED_SCENARIOS)
        )
        self._unplanned = (
            list(unplanned) if unplanned is not None else list(UNPLANNED_SCENARIOS)
        )

    def all(self) -> list[ScenarioDefinitionDTO]:
        return [*self._planned, *self._unplanned]

    def by_category(self, category: ScenarioCategory) -> list[ScenarioDefinitionDTO]:
        if category == ScenarioCategory.PLANNED:
            return list(self._planned)
        return list(self._unplanned)

    def as_catalog_dto(self) -> ScenarioCatalogDTO:
        return ScenarioCatalogDTO(
            planned=list(self._planned),
            unplanned=list(self._unplanned),
            counts={
                ScenarioCategory.PLANNED.value: len(self._planned),
                ScenarioCategory.UNPLANNED.value: len(self._unplanned),
                "TOTAL": len(self._planned) + len(self._unplanned),
            },
        )


# Singleton instance reused by the API layer.
scenario_catalog = ScenarioCatalog()
