import React from 'react';
import { useIncidentStore } from '../../store/incident.store';
import { useSimulationStore } from '../../store/simulation.store';
import { api } from '../../services/api';
import { IncidentTimeline } from './IncidentTimeline';
import { X, Shield, Activity, Compass, DollarSign, BrainCircuit, CheckCircle } from 'lucide-react';

export const IncidentDetailsDrawer: React.FC = () => {
  const selectedId = useIncidentStore((state) => state.selectedIncidentId);
  const selectedIncident = useIncidentStore((state) => selectedId ? state.incidents[selectedId] : null);
  const plan = useSimulationStore((state) => selectedId ? state.operationalPlans[selectedId] : null);
  const isLoading = useSimulationStore((state) => selectedId ? state.loadingPlans[selectedId] : false);
  const setSelectedIncidentId = useIncidentStore((state) => state.setSelectedIncidentId);

  // We need a generatePlan function here since we removed it from the global store
  const setOperationalPlan = useSimulationStore((state) => state.setOperationalPlan);
  const setLoadingPlan = useSimulationStore((state) => state.setLoadingPlan);

  const generatePlan = async (incidentId: string) => {
    if (!selectedIncident) return;
    setLoadingPlan(incidentId, true);
    try {
      const payload = {
        incident_id: selectedIncident.incident_id,
        latitude: selectedIncident.latitude,
        longitude: selectedIncident.longitude,
        gori_score: selectedIncident.gori_score,
        congestion_severity: selectedIncident.gori_score > 75 ? 'CRITICAL' : (selectedIncident.gori_score > 45 ? 'HIGH' : 'NORMAL'),
        requires_closure: selectedIncident.heavy_vehicle || selectedIncident.gori_score > 80,
        heavy_vehicle_involved: selectedIncident.heavy_vehicle,
        is_rush_hour: selectedIncident.is_rush_hour,
        hotspot_recurrence: selectedIncident.gori_score > 70 ? 0.82 : 0.35,
        historical_spread_probability: selectedIncident.gori_score > 70 ? 0.68 : 0.22,
      };

      const newPlan = await api.requestOptimization(payload);
      setOperationalPlan(incidentId, newPlan);
    } catch (err) {
      console.error('Failed to generate operational plan', err);
    } finally {
      setLoadingPlan(incidentId, false);
    }
  };

  if (!selectedIncident) return null;

  return (
    <div className="bg-dark-card border border-dark-border rounded-xl h-full flex flex-col overflow-hidden shadow-2xl relative">
      {/* Header */}
      <div className="p-4 border-b border-dark-border flex items-center justify-between bg-dark-bg/25">
        <div>
          <span className="text-[10px] font-bold text-brand-primary tracking-widest uppercase">AI Incident Intelligence</span>
          <h3 className="font-extrabold text-sm text-gray-200 mt-0.5">{selectedIncident.incident_id}</h3>
        </div>
        <button
          onClick={() => setSelectedIncidentId(null)}
          className="p-1 rounded-lg hover:bg-dark-bg text-gray-400 hover:text-gray-200 transition-colors"
        >
          <X className="w-4 h-4" />
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {/* Top summary row */}
        <div className="grid grid-cols-2 gap-3">
          <div className="bg-dark-bg/60 border border-dark-border rounded-lg p-3 text-center">
            <span className="text-[10px] text-gray-500 font-bold uppercase block mb-1">GORI Risk Score</span>
            <span className={`text-2xl font-extrabold ${
              selectedIncident.gori_score > 70 ? 'text-alert-high animate-pulse' : 'text-amber-500'
            }`}>{Math.round(selectedIncident.gori_score)}</span>
            <span className="text-[9px] text-gray-500 block mt-0.5">congestion index</span>
          </div>

          <div className="bg-dark-bg/60 border border-dark-border rounded-lg p-3 text-center">
            <span className="text-[10px] text-gray-500 font-bold uppercase block mb-1">Impact Level</span>
            <span className={`text-md font-extrabold block mt-1.5 ${
              selectedIncident.gori_score > 70 ? 'text-red-400' : 'text-amber-400'
            }`}>
              {selectedIncident.gori_score > 75 ? 'CRITICAL CRASH' : (selectedIncident.gori_score > 45 ? 'MODERATE SURGE' : 'MINOR BLOCKED')}
            </span>
          </div>
        </div>

        {/* Core details */}
        <div className="bg-dark-bg/40 border border-dark-border/60 rounded-lg p-3.5 space-y-2 text-xs">
          <h4 className="font-bold text-gray-400 uppercase text-[10px] tracking-wider mb-2">Metadata Parameters</h4>
          <div className="flex justify-between">
            <span className="text-gray-500">Incident Type:</span>
            <span className="font-bold text-gray-300">{selectedIncident.type}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500">GPS Coordinates:</span>
            <span className="font-bold text-gray-300">{selectedIncident.latitude.toFixed(5)}, {selectedIncident.longitude.toFixed(5)}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500">Heavy Vehicle:</span>
            <span className="font-bold text-gray-300">{selectedIncident.heavy_vehicle ? 'YES' : 'NO'}</span>
          </div>
          <div className="flex justify-between">
            <span className="text-gray-500">Is Rush Hour:</span>
            <span className="font-bold text-gray-300">{selectedIncident.is_rush_hour ? 'YES' : 'NO'}</span>
          </div>
        </div>

        <IncidentTimeline />

        {/* AI Recommendations & Optimization Engine */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h4 className="font-bold text-gray-400 uppercase text-[10px] tracking-wider flex items-center">
              <BrainCircuit className="w-3.5 h-3.5 text-brand-accent mr-1" />
              Optimization Solutions
            </h4>

            {!plan && !isLoading && (
              <button
                onClick={() => generatePlan(selectedIncident.incident_id)}
                className="text-[10px] font-bold text-brand-primary hover:underline"
              >
                Trigger Optimization
              </button>
            )}
          </div>

          {isLoading ? (
            <div className="bg-dark-bg/60 border border-dark-border rounded-lg p-4 space-y-3 animate-pulse">
              <div className="h-3.5 bg-dark-border rounded w-2/3"></div>
              <div className="h-10 bg-dark-border rounded"></div>
              <div className="h-14 bg-dark-border rounded"></div>
            </div>
          ) : plan ? (
            <div className="space-y-3">
              {/* Resource deployment plan summary */}
              <div className="border border-brand-accent/25 bg-brand-accent/5 rounded-lg p-3.5">
                <div className="flex items-center space-x-1.5 mb-1.5">
                  <Shield className="w-4 h-4 text-brand-accent shrink-0" />
                  <span className="text-xs font-bold text-gray-200">Recommended Dispatch Plan</span>
                </div>
                <p className="text-xs text-purple-200 leading-relaxed font-semibold">{plan.recommended_plan}</p>

                {/* Cost efficiency scoring */}
                <div className="grid grid-cols-4 gap-2 mt-3 pt-3 border-t border-dark-border/40 text-center">
                  <div className="bg-dark-bg/50 border border-dark-border/60 p-1.5 rounded">
                    <span className="text-[8px] text-gray-500 uppercase block font-bold">Officers</span>
                    <span className="text-xs font-extrabold text-gray-300">{plan.resource_plan?.police_officers || 0}</span>
                  </div>
                  <div className="bg-dark-bg/50 border border-dark-border/60 p-1.5 rounded">
                    <span className="text-[8px] text-gray-500 uppercase block font-bold">Barricades</span>
                    <span className="text-xs font-extrabold text-gray-300">{plan.resource_plan?.barricades || 0}</span>
                  </div>
                  <div className="bg-dark-bg/50 border border-dark-border/60 p-1.5 rounded">
                    <span className="text-[8px] text-gray-500 uppercase block font-bold">Vehicles</span>
                    <span className="text-xs font-extrabold text-gray-300">{plan.resource_plan?.patrol_vehicles || 0}</span>
                  </div>
                  <div className="bg-dark-bg/50 border border-dark-border/60 p-1.5 rounded">
                    <span className="text-[8px] text-gray-500 uppercase block font-bold">Cost Est</span>
                    <span className="text-xs font-extrabold text-emerald-400 flex items-center justify-center">
                      <DollarSign className="w-3 h-3" />
                      {plan.resource_plan?.estimated_cost || 0}
                    </span>
                  </div>
                </div>
              </div>

              {/* Graph Diversion Routing */}
              {plan.diversion_plan?.description && (
                <div className="bg-dark-bg/60 border border-dark-border rounded-lg p-3.5 space-y-1.5 text-xs">
                  <div className="flex items-center space-x-1.5 text-brand-primary font-bold">
                    <Compass className="w-4 h-4" />
                    <span>AI Graph Diversion Routing</span>
                  </div>
                  <p className="text-gray-300 leading-relaxed font-semibold">{plan.diversion_plan.description}</p>
                  <div className="bg-dark-bg/80 border border-dark-border/80 px-2.5 py-1.5 rounded flex items-center justify-between text-xxs">
                    <span className="text-gray-500">Estimated Congestion Bypass:</span>
                    <span className="font-extrabold text-emerald-400">-{plan.diversion_plan.congestion_bypass_pct}%</span>
                  </div>
                </div>
              )}

              {/* Scenario-driven simulations: Best Case, Expected Case, Worst Case */}
              <div className="bg-dark-bg/60 border border-dark-border rounded-lg p-3.5 space-y-2.5">
                <div className="flex items-center space-x-1.5 text-amber-500 font-bold text-xs">
                  <Activity className="w-4 h-4" />
                  <span>Scenario Impact Simulations</span>
                </div>

                <div className="space-y-2">
                  {Object.entries(plan.predicted_impact || {}).map(([scenario, data]) => {
                    const isWorst = scenario === 'WORST_CASE';
                    const isBest = scenario === 'BEST_CASE';
                    const labelColor = isWorst ? 'text-red-400' : (isBest ? 'text-emerald-400' : 'text-amber-400');
                    const bgClass = isWorst ? 'bg-red-500/5 border-red-500/20' : (isBest ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-amber-500/5 border-amber-500/20');

                    return (
                      <div key={scenario} className={`border rounded p-2 text-xxs flex justify-between items-center ${bgClass}`}>
                        <div>
                          <span className={`font-bold ${labelColor}`}>{scenario.replace('_', ' ')}</span>
                          <p className="text-gray-500 mt-0.5">Confidence: {(data.confidence * 100).toFixed(0)}%</p>
                        </div>
                        <div className="text-right">
                          <div className="font-bold text-gray-300">
                            {data.estimated_clearance_minutes} mins clearance
                          </div>
                          <span className="text-gray-400 font-semibold">
                            -{data.congestion_reduction}% congestion
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Action items list */}
              <div className="bg-dark-bg/60 border border-dark-border rounded-lg p-3.5 space-y-2">
                <span className="text-xxs font-bold text-gray-500 uppercase tracking-wider block">Recommended Dispatch Checklist</span>
                <ul className="space-y-1.5 text-xxs font-semibold">
                  {plan.recommended_actions?.map((act, i) => (
                    <li key={i} className="flex items-start space-x-1.5 text-gray-300">
                      <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0 mt-0.5" />
                      <span>{act}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Explainability notes */}
              <div className="bg-dark-bg/40 border border-dark-border/40 rounded-lg p-3.5 text-[10px] text-gray-500 space-y-1.5">
                <span className="font-bold uppercase tracking-wider block">Model Attribution Explainability</span>
                {plan.explainability?.map((exp, i) => (
                  <p key={i} className="leading-relaxed leading-normal">{exp}</p>
                ))}
              </div>
            </div>
          ) : (
            <div className="bg-dark-bg/60 border border-dark-border rounded-lg p-4 text-center text-xs text-gray-500 italic space-y-2">
              <p>No operational plan computed yet.</p>
              <button
                onClick={() => generatePlan(selectedIncident.incident_id)}
                className="px-3 py-1.5 rounded bg-brand-primary text-white font-semibold hover:bg-brand-primary/95 transition-colors mt-2"
              >
                Compute AI Optimization
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
