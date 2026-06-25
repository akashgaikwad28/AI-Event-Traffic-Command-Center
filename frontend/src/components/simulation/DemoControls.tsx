import React, { useEffect, useState } from 'react';
import { useIncidentStore } from '../../store/incident.store';
import { useSimulationStore } from '../../store/simulation.store';
import { useAnalyticsStore } from '../../store/analytics.store';
import { RotateCcw, AlertTriangle, Shield, Car, Zap, Wind, Droplets, Thermometer, Construction, Users, Flower2, Activity, HardHat, Crown } from 'lucide-react';
import { api } from '../../services/api';
import { useDemoStore } from '../../store/demo.store';
import { FALLBACK_CATALOG } from '../../constants/scenarios';
import type { SimulationScenario } from '../../constants/scenarios';
import type { DemoScenario, ScenarioCategory, ScenarioCatalogDTO } from '../../types/scenarios';

// ---------------------------------------------------------------------------
// Icon resolver — maps the string icon name from the catalog to a Lucide
// component. Falls back to AlertTriangle for unmapped names.
// ---------------------------------------------------------------------------
const ICON_MAP: Record<string, React.FC<{ className?: string }>> = {
  Car, AlertTriangle, Shield, Zap, Wind, Droplets, Thermometer,
  Construction, Users, Flower2, Activity, HardHat, Crown,
};
function resolveIcon(name: string): React.FC<{ className?: string }> {
  return ICON_MAP[name] ?? AlertTriangle;
}

export const DemoControls: React.FC = () => {
  const { activeScenario, isRunning, startScenario, stopScenario } = useDemoStore();
  const clearIncidents = useIncidentStore((state) => state.clearIncidents);
  const clearSimulation = useSimulationStore((state) => state.clearSimulation);
  const setOperationalPlan = useSimulationStore((state) => state.setOperationalPlan);
  const clearAlerts = useAnalyticsStore((state) => state.clearAlerts);

  const [catalog, setCatalog] = useState<ScenarioCatalogDTO>(FALLBACK_CATALOG);
  const [activeTab, setActiveTab] = useState<ScenarioCategory>('PLANNED');

  const handleScenarioRun = async (scen: DemoScenario) => {
    await startScenario(scen.id, scen.sim_type as SimulationScenario, scen.payload);

    let severity = 'LOW';
    if (scen.payload.gori > 70) severity = 'CRITICAL';
    else if (scen.payload.gori > 40) severity = 'MODERATE';

    const incId = `INC-${Math.floor(Math.random() * 10000)}`;
    try {
      const plan = await api.requestOptimization({
        incident_id: incId,
        latitude: scen.payload.lat,
        longitude: scen.payload.lng,
        gori_score: scen.payload.gori,
        congestion_severity: severity,
        requires_closure: scen.payload.hvi || scen.payload.gori > 80,
        heavy_vehicle_involved: scen.payload.hvi,
        is_rush_hour: scen.payload.rush,
        hotspot_recurrence: scen.payload.gori > 70 ? 4 : 1,
        historical_spread_probability: scen.payload.gori > 70 ? 0.85 : 0.2,
        // Pass scenario taxonomy so the learning loop (Gap 2) can split
        // accuracy across PLANNED vs UNPLANNED event classes.
        scenario_category: scen.category,
        scenario_subtype: scen.subtype,
      });
      setOperationalPlan(incId, plan);
    } catch (e) {
      console.error('Failed to auto-optimize demo scenario', e);
    }
  };

  // Fetch the catalog from the backend (falls back to static if unavailable)
  useEffect(() => {
    (async () => {
      let fetchedCatalog = FALLBACK_CATALOG;
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/scenarios`);
        if (res.ok) {
          fetchedCatalog = await res.json();
          setCatalog(fetchedCatalog);
        }
      } catch {
        // Use FALLBACK_CATALOG already set as default
      }

      // Automatically trigger a scenario on load for the demo effect
      if (!useDemoStore.getState().activeScenario && !useDemoStore.getState().isRunning) {
         const defaultScen = fetchedCatalog.unplanned[0] || FALLBACK_CATALOG.unplanned[0];
         if (defaultScen) {
             handleScenarioRun(defaultScen);
         }
      }
    })();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const clearAll = async () => {
    try {
      await api.clearSimulation();
      await fetch(`${import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'}/learning/reset`, { method: 'POST' });
    } catch (err) {
      console.error(err);
    }
    clearIncidents();
    clearSimulation();
    clearAlerts();
    stopScenario();
  };

  const currentList = activeTab === 'PLANNED' ? catalog.planned : catalog.unplanned;

  return (
    <div className="bg-dark-card border border-dark-border rounded-xl p-5 shadow-lg relative overflow-hidden group">
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-brand-primary to-brand-accent"></div>

      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <div>
          <h3 className="font-bold text-gray-100 tracking-wide text-md flex items-center">
            AI Simulation Injector
            {isRunning && <span className="ml-3 flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-accent opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-primary"></span>
            </span>}
          </h3>
          <p className="text-xs text-gray-500 font-medium">
            {catalog.counts.TOTAL} scenarios — {catalog.counts.PLANNED} planned + {catalog.counts.UNPLANNED} unplanned
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={clearAll}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg border border-dark-border bg-dark-bg text-xs font-semibold text-gray-400 hover:text-gray-200 hover:bg-dark-border/40 transition-colors"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset Engines</span>
          </button>
        </div>
      </div>

      {/* Category Tabs */}
      <div className="flex space-x-1 mb-3">
        {(['PLANNED', 'UNPLANNED'] as ScenarioCategory[]).map((cat) => {
          const count = cat === 'PLANNED' ? catalog.counts.PLANNED : catalog.counts.UNPLANNED;
          const isActive = activeTab === cat;
          return (
            <button
              key={cat}
              onClick={() => setActiveTab(cat)}
              className={`px-3 py-1.5 rounded-lg text-xs font-bold tracking-wider transition-all ${
                isActive
                  ? cat === 'PLANNED'
                    ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'
                    : 'bg-red-500/15 text-red-400 border border-red-500/30'
                  : 'bg-dark-bg text-gray-500 border border-dark-border hover:text-gray-300'
              }`}
            >
              {cat === 'PLANNED' ? '📅 Planned Events' : '🚨 Unplanned Incidents'}
              <span className={`ml-1.5 text-[10px] ${isActive ? 'opacity-100' : 'opacity-50'}`}>({count})</span>
            </button>
          );
        })}
      </div>

      {/* Scenario Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
        {currentList.map((scen) => {
          const Icon = resolveIcon(scen.icon);
          const isCurrent = activeScenario === scen.id;
          return (
            <button
              key={scen.id}
              onClick={() => handleScenarioRun(scen)}
              disabled={isRunning}
              className={`flex flex-col text-left p-3 rounded-lg border transition-all duration-200 select-none ${
                isCurrent
                  ? 'border-brand-primary bg-brand-primary/10 shadow-md ring-1 ring-brand-primary/30'
                  : 'border-dark-border bg-dark-bg/60 hover:bg-dark-bg/95 hover:border-gray-700'
              } ${isRunning ? 'opacity-40 cursor-not-allowed' : 'cursor-pointer'}`}
            >
              <div className="flex items-center space-x-2 mb-1.5 border-b border-dark-border pb-2 w-full">
                <div className="p-1.5 rounded bg-dark-bg border border-dark-border shrink-0">
                  <Icon className="w-3 h-3 text-brand-accent" />
                </div>
                <div className="min-w-0 flex-1">
                  <span className="font-bold text-[11px] text-gray-200 block truncate">{scen.name}</span>
                  <span className={`text-[8px] font-bold tracking-wider ${
                    scen.category === 'PLANNED' ? 'text-emerald-500/70' : 'text-red-400/70'
                  }`}>
                    {scen.subtype}
                  </span>
                </div>
              </div>
              <p className="text-[9px] text-gray-400 font-medium leading-relaxed flex-1 mb-2">{scen.description}</p>

              <div className="bg-dark-bg border border-dark-border rounded p-1.5 w-full">
                <div className="text-[8px] font-mono text-emerald-400">Input Payload:</div>
                <div className="text-[8px] font-mono text-gray-500 mt-0.5">Lat: {scen.payload.lat}</div>
                <div className="text-[8px] font-mono text-gray-500">GORI: {scen.payload.gori}</div>
                <div className="text-[8px] font-mono text-gray-500">Rush: {scen.payload.rush ? 'YES' : 'NO'}</div>
                <div className="text-[8px] font-mono text-gray-500">Heavy: {scen.payload.hvi ? 'YES' : 'NO'}</div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
