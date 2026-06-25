import { SimulationScenario, SIMULATION_SCENARIOS } from '../constants/scenarios';
const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

export interface OptimizationRequest {
  incident_id: string;
  latitude: number;
  longitude: number;
  gori_score: number;
  congestion_severity: string;
  requires_closure: boolean;
  heavy_vehicle_involved: boolean;
  is_rush_hour: boolean;
  hotspot_recurrence: number;
  historical_spread_probability: number;
  /** Optional taxonomy metadata consumed by the Post-Event Learning loop. */
  scenario_category?: string;
  scenario_subtype?: string;
}

export interface SimulationResult {
  scenario: string;
  estimated_clearance_minutes: number;
  congestion_reduction: number;
  spread_risk: string;
  confidence: number;
}

export interface OperationalPlan {
  plan_id: string;
  incident_id: string;
  gori_score_before?: number;
  simulation_result?: any;
  gori_score: number;
  operational_risk: string;
  recommended_plan: string;
  resource_plan: {
    police_officers: number;
    barricades: number;
    patrol_vehicles: number;
    estimated_cost: number;
  };
  diversion_plan: {
    route_id: string;
    description: string;
    points: [number, number][]; // coordinates for diversion
    congestion_bypass_pct: number;
  };
  predicted_impact: {
    best_case: SimulationResult;
    expected_case: SimulationResult;
    worst_case: SimulationResult;
  };
  confidence: number;
  recommended_actions: string[];
  explainability: string[];
}

export const api = {
  async getLiveSnapshot() {
    const res = await fetch(`${API_BASE}/stream/live-snapshot`);
    if (!res.ok) throw new Error('Failed to fetch live snapshot');
    return res.json();
  },

  async getStreamMetrics() {
    const res = await fetch(`${API_BASE}/stream/metrics`);
    if (!res.ok) throw new Error('Failed to fetch stream metrics');
    return res.json();
  },

  async getAnalyticsOverview(timeWindow = 24) {
    const res = await fetch(`${API_BASE}/analytics/overview?time_window=${timeWindow}`);
    if (!res.ok) throw new Error('Failed to fetch analytics overview');
    return res.json();
  },

  async getCityHealth() {
    const res = await fetch(`${API_BASE}/analytics/city-health`);
    if (!res.ok) throw new Error('Failed to fetch city health score');
    return res.json();
  },

  async requestOptimization(request: OptimizationRequest): Promise<OperationalPlan> {
    const res = await fetch(`${API_BASE}/optimization/incident-response`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    });
    if (!res.ok) {
      const err = await res.text();
      throw new Error(`Optimization failed: ${err}`);
    }
    return res.json();
  },

  async triggerSimulation(scenario: SimulationScenario, payload?: any) {
    if (!Object.values(SIMULATION_SCENARIOS).includes(scenario)) {
      throw new Error(`Invalid simulation scenario: ${scenario}`);
    }

    const res = await fetch(`${API_BASE}/stream/start-simulation/${scenario}`, {
      method: 'POST',
      headers: payload ? { 'Content-Type': 'application/json' } : undefined,
      body: payload ? JSON.stringify(payload) : undefined
    });
    if (!res.ok) throw new Error('Failed to start simulation');
    return res.json();
  },

  async clearSimulation() {
    const response = await fetch(`${API_BASE}/simulation/clear`, {
      method: 'POST',
    });
    return response.json();
  },

  async getIncidentExplanation(incidentData: any) {
    const payload = {
      incident_id: incidentData.incident_id || "UNKNOWN",
      query: incidentData.query || `Provide a ${incidentData.mode} explanation for this incident.`,
      context_overrides: incidentData
    };
    const response = await fetch(`${API_BASE}/copilot/explain`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    if (!response.ok) throw new Error('Failed to fetch explanation');
    return response.json();
  },

  async runVisualSimulation(scenarioType: string, params: any = {}) {
    const res = await fetch(`${API_BASE}/simulation/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ scenario_type: scenarioType, params })
    });
    if (!res.ok) throw new Error('Failed to run visual simulation');
    return res.json();
  },

  async getSimulationHistory() {
    const res = await fetch(`${API_BASE}/simulation/history`);
    if (!res.ok) throw new Error('Failed to fetch simulation history');
    return res.json();
  },

  async runExecutiveDemo() {
    const res = await fetch(`${API_BASE}/simulation/demo`, { method: 'POST' });
    if (!res.ok) throw new Error('Failed to run executive demo');
    return res.json();
  }
};
