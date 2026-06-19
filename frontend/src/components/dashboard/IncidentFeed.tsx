import React from 'react';
import { useIncidentStore } from '../../store/incident.store';
import { AlertCircle, ChevronRight, Activity, Zap } from 'lucide-react';

export const IncidentFeed: React.FC = () => {
  const incidents = useIncidentStore((state) => Object.values(state.incidents));
  const selectedId = useIncidentStore((state) => state.selectedIncidentId);
  const setSelectedId = useIncidentStore((state) => state.setSelectedIncidentId);

  // Sort by GORI score descending to prioritize critical cases
  const sortedIncidents = [...incidents].sort((a, b) => b.gori_score - a.gori_score);

  return (
    <div className="bg-dark-card border border-dark-border rounded-xl flex flex-col h-full overflow-hidden shadow-lg">
      <div className="p-4 border-b border-dark-border flex items-center justify-between shrink-0 bg-dark-bg/25">
        <div>
          <h3 className="font-bold text-gray-200 text-sm tracking-wide flex items-center">
            <Activity className="w-4 h-4 text-brand-primary mr-1.5 animate-pulse" />
            Live Incident Stream
          </h3>
          <p className="text-xxs text-gray-500 font-medium mt-0.5">Prioritized by AI GORI Congestion Severity.</p>
        </div>
        <span className="text-xxs px-2 py-0.5 rounded-full bg-dark-border border border-dark-border text-gray-400 font-bold">
          {incidents.length} Active
        </span>
      </div>

      <div className="flex-1 overflow-y-auto divide-y divide-dark-border/40 p-2 space-y-1">
        {sortedIncidents.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-4 text-gray-500 italic space-y-2">
            <Zap className="w-8 h-8 text-gray-600 animate-pulse" />
            <p className="text-xs">No active operational incidents.</p>
            <p className="text-xxs font-normal text-gray-650 max-w-[200px]">Trigger an AI Simulation below to inject real-time traffic events.</p>
          </div>
        ) : (
          sortedIncidents.map((incident) => {
            const isSelected = incident.incident_id === selectedId;
            const isCritical = incident.gori_score > 70;
            
            return (
              <button
                key={incident.incident_id}
                onClick={() => setSelectedId(incident.incident_id)}
                className={`w-full flex items-center justify-between p-3 rounded-lg border text-left transition-all duration-200 select-none ${
                  isSelected
                    ? 'border-brand-primary bg-brand-primary/10 shadow-sm'
                    : 'border-transparent hover:bg-dark-bg/60 hover:border-dark-border'
                }`}
              >
                <div className="flex items-start space-x-2.5 min-w-0 flex-1">
                  <div className={`mt-0.5 shrink-0 ${isCritical ? 'text-alert-high' : 'text-brand-primary'}`}>
                    <AlertCircle className="w-4.5 h-4.5" />
                  </div>
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center space-x-2">
                      <span className="text-xs font-bold text-gray-300 truncate">{incident.type}</span>
                      {incident.heavy_vehicle && (
                        <span className="text-[9px] px-1.5 py-0.2 bg-purple-500/10 border border-purple-500/25 text-purple-400 font-bold rounded uppercase">
                          HEAVY
                        </span>
                      )}
                    </div>
                    <p className="text-xxs text-gray-500 font-medium truncate mt-0.5">
                      ID: {incident.incident_id} • Bangalore {incident.latitude.toFixed(3)}, {incident.longitude.toFixed(3)}
                    </p>
                  </div>
                </div>

                <div className="flex items-center space-x-2 shrink-0 pl-2">
                  <div className="text-right">
                    <div className={`text-xs font-extrabold ${isCritical ? 'text-alert-high' : 'text-gray-300'}`}>
                      GORI {Math.round(incident.gori_score)}
                    </div>
                    <span className="text-[9px] text-gray-500 leading-none">risk score</span>
                  </div>
                  <ChevronRight className={`w-4 h-4 transition-transform ${isSelected ? 'translate-x-0.5 text-brand-primary' : 'text-gray-600'}`} />
                </div>
              </button>
            );
          })
        )}
      </div>
    </div>
  );
};
