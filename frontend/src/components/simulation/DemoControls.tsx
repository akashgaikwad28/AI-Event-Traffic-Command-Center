import React from 'react';
import { useIncidentStore } from '../../store/incident.store';
import { useSimulationStore } from '../../store/simulation.store';
import { useAnalyticsStore } from '../../store/analytics.store';
import { RotateCcw, AlertTriangle, Shield, Car, Zap, Wind, Droplets, Thermometer, Construction } from 'lucide-react';
import { api } from '../../services/api';
import { useDemoStore } from '../../store/demo.store';
import { useNavigate } from 'react-router-dom';
import { SIMULATION_SCENARIOS } from '../../constants/scenarios';

export const DemoControls: React.FC = () => {
  const { activeScenario, isRunning, startScenario, stopScenario } = useDemoStore();
  const clearIncidents = useIncidentStore((state) => state.clearIncidents);
  const clearSimulation = useSimulationStore((state) => state.clearSimulation);
  const setOperationalPlan = useSimulationStore((state) => state.setOperationalPlan);
  const clearAlerts = useAnalyticsStore((state) => state.clearAlerts);
  const navigate = useNavigate();

  const clearAll = async () => {
    try {
      await api.clearSimulation();
    } catch (err) {
      console.error(err);
    }
    clearIncidents();
    clearSimulation();
    clearAlerts();
    stopScenario();
  };

  const scenarios = [
    { id: 'SCENARIO_1', simType: SIMULATION_SCENARIOS.CUSTOM_INCIDENT, name: 'Peenya Truck Stall', desc: 'LCV breakdown on Highway', icon: Car, payload: { lat: 13.0400, lng: 77.5180, gori: 85, hvi: true, rush: true } },
    { id: 'SCENARIO_2', simType: SIMULATION_SCENARIOS.ACCIDENT_CASCADE, name: 'HSR Heavy Vehicle', desc: 'Heavy vehicle blockage', icon: AlertTriangle, payload: { lat: 12.9218, lng: 77.6451, gori: 65, hvi: true, rush: false } },
    { id: 'SCENARIO_3', simType: SIMULATION_SCENARIOS.CUSTOM_INCIDENT, name: 'Wilson Garden Traffic', desc: 'Non-corridor incident', icon: Car, payload: { lat: 12.9556, lng: 77.5857, gori: 45, hvi: false, rush: false } },
    { id: 'SCENARIO_4', simType: SIMULATION_SCENARIOS.CUSTOM_INCIDENT, name: 'Sadashiva Tree Fall', desc: 'Tree blocking road', icon: Wind, payload: { lat: 13.0061, lng: 77.5794, gori: 75, hvi: false, rush: true } },
    { id: 'SCENARIO_5', simType: SIMULATION_SCENARIOS.LIVE_REPLAY, name: 'Lalbagh Bus Break', desc: 'Private bus stalled', icon: AlertTriangle, payload: { lat: 12.9539, lng: 77.5852, gori: 35, hvi: true, rush: false } },
    { id: 'SCENARIO_6', simType: SIMULATION_SCENARIOS.ACCIDENT_CASCADE, name: 'Jakkur Multi-Crash', desc: 'Amruthahalli accident', icon: Zap, payload: { lat: 13.0664, lng: 77.5998, gori: 96, hvi: true, rush: true } },
    { id: 'SCENARIO_7', simType: SIMULATION_SCENARIOS.CUSTOM_INCIDENT, name: 'Kengeri BMTC Fail', desc: 'BMTC bus broken down', icon: Construction, payload: { lat: 12.9328, lng: 77.4879, gori: 55, hvi: true, rush: false } },
    { id: 'SCENARIO_8', simType: SIMULATION_SCENARIOS.STADIUM_EVENT_EGRESS, name: 'Chinnaswamy Match', desc: 'Cricket match egress', icon: Shield, payload: { lat: 12.9788, lng: 77.5995, gori: 82, hvi: false, rush: true } },
    { id: 'SCENARIO_9', simType: SIMULATION_SCENARIOS.HISTORICAL_REPLAY, name: 'Whitefield Flood', desc: 'Underpass water logging', icon: Droplets, payload: { lat: 13.0008, lng: 77.6813, gori: 92, hvi: false, rush: true } },
    { id: 'SCENARIO_10', simType: SIMULATION_SCENARIOS.LIVE_REPLAY, name: 'Hebbal Flyover Stall', desc: 'Vehicle starting problem', icon: Thermometer, payload: { lat: 13.0418, lng: 77.5947, gori: 25, hvi: false, rush: false } },
  ];

  const handleScenarioRun = async (scen: any) => {
    // 1. Start the simulation with specific coordinates payload
    await startScenario(scen.id, scen.simType, scen.payload);

    // Determine dynamic severity
    let severity = 'LOW';
    if (scen.payload.gori > 70) severity = 'CRITICAL';
    else if (scen.payload.gori > 40) severity = 'MODERATE';

    // 2. Automatically request optimization so Operations Planner populates
    const incId = `INC-${Math.floor(Math.random() * 10000)}`;
    try {
      const plan = await api.requestOptimization({
        incident_id: incId,
        latitude: scen.payload.lat,
        longitude: scen.payload.lng,
        gori_score: scen.payload.gori,
        congestion_severity: severity,
        requires_closure: scen.payload.gori > 80,
        heavy_vehicle_involved: scen.payload.hvi,
        is_rush_hour: scen.payload.rush,
        hotspot_recurrence: scen.payload.gori > 70 ? 4 : 1,
        historical_spread_probability: scen.payload.gori > 70 ? 0.85 : 0.2
      });
      setOperationalPlan(incId, plan);
      navigate('/planner'); // Jump to planner to see the result
    } catch (e) {
      console.error('Failed to auto-optimize demo scenario', e);
    }
  };

  return (
    <div className="bg-dark-card border border-dark-border rounded-xl p-5 shadow-lg relative overflow-hidden group">
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-brand-primary to-brand-accent"></div>

      <div className="flex justify-between items-center mb-4">
        <div>
          <h3 className="font-bold text-gray-100 tracking-wide text-md flex items-center">
            AI Simulation Injector
            {isRunning && <span className="ml-3 flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-accent opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-primary"></span>
            </span>}
          </h3>
          <p className="text-xs text-gray-500 font-medium">Trigger real-time scenarios for judging demonstrations.</p>
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

      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {scenarios.map((scen) => {
          const Icon = scen.icon;
          const isCurrent = activeScenario === scen.id;
          return (
            <button
              key={scen.id}
              onClick={() => handleScenarioRun(scen)}
              disabled={isRunning && !isCurrent}
              className={`flex flex-col text-left p-3 rounded-lg border transition-all duration-200 select-none ${
                isCurrent
                  ? 'border-brand-primary bg-brand-primary/10 shadow-md ring-1 ring-brand-primary/30'
                  : 'border-dark-border bg-dark-bg/60 hover:bg-dark-bg/95 hover:border-gray-700'
              } ${isRunning && !isCurrent ? 'opacity-40 cursor-not-allowed' : 'cursor-pointer'}`}
            >
              <div className="flex items-center space-x-2 mb-2 border-b border-dark-border pb-2 w-full">
                <div className={`p-1.5 rounded bg-dark-bg border border-dark-border shrink-0`}>
                  <Icon className="w-3 h-3 text-brand-accent" />
                </div>
                <span className="font-bold text-[11px] text-gray-200 truncate">{scen.name}</span>
              </div>
              <p className="text-[9px] text-gray-400 font-medium leading-relaxed flex-1 mb-2">{scen.desc}</p>

              <div className="bg-dark-bg border border-dark-border rounded p-1.5 w-full">
                <div className="text-[8px] font-mono text-emerald-400">Input Payload:</div>
                <div className="text-[8px] font-mono text-gray-500 mt-0.5">Lat: {scen.payload.lat}</div>
                <div className="text-[8px] font-mono text-gray-500">GORI: {scen.payload.gori}</div>
                <div className="text-[8px] font-mono text-gray-500">Rush Hour: {scen.payload.rush ? 'YES' : 'NO'}</div>
                <div className="text-[8px] font-mono text-gray-500">Heavy Veh: {scen.payload.hvi ? 'YES' : 'NO'}</div>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
};
