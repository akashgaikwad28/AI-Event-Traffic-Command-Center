/**
 * Typed scenario types for the demo catalog.
 *
 * Mirrors backend/app/scenarios/scenario_models.py (ScenarioDefinitionDTO).
 * Bridges Gap 1 — planned events are first-class citizens alongside unplanned
 * incidents, both carrying the same strict payload schema.
 */

export type ScenarioCategory = 'PLANNED' | 'UNPLANNED';

export interface ScenarioPayload {
  lat: number;
  lng: number;
  gori: number;
  hvi: boolean;
  rush: boolean;
}

export interface DemoScenario {
  id: string;
  name: string;
  category: ScenarioCategory;
  subtype: string;
  description: string;
  sim_type: string;
  icon: string;
  payload: ScenarioPayload;
  expected_outcome: string;
}

export interface ScenarioCatalogDTO {
  planned: DemoScenario[];
  unplanned: DemoScenario[];
  counts: Record<string, number>;
}
