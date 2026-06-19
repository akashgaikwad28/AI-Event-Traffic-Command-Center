import React from 'react';
import { CommandMap } from '../components/maps/CommandMap';
import { IncidentDetailsDrawer } from '../components/dashboard/IncidentDetailsDrawer';
import { useIncidentStore } from '../store/incident.store';
import { useGoriStore } from '../store/gori.store';

export const LiveOperationsPage: React.FC = () => {
  const selectedId = useIncidentStore((state) => state.selectedIncidentId);
  const incidents = useIncidentStore((state) => Object.values(state.incidents));
  const avgGori = useGoriStore((state) => state.avgGori);

  const activeCount = incidents.length;
  const criticalCount = incidents.filter(i => i.gori_score > 70).length;

  return (
    <div className="h-full w-full flex relative overflow-hidden bg-dark-bg p-4 space-x-4">
      {/* Primary Map view */}
      <div className="flex-1 h-full relative">
        <CommandMap />

        {/* Floating Quick Stats HUD */}
        <div className="absolute top-4 left-4 z-[400] bg-dark-card/90 border border-dark-border p-4 rounded-xl shadow-lg flex items-center space-x-6 backdrop-blur-md">
          <div className="flex items-center space-x-2">
            <div className="w-2.5 h-2.5 rounded-full bg-alert-critical animate-pulse"></div>
            <div>
              <h4 className="text-[10px] text-gray-500 font-bold uppercase tracking-wider leading-none">Map Stream</h4>
              <span className="text-xs text-gray-300 font-bold mt-1 block">Live City Feed</span>
            </div>
          </div>

          <div className="w-px h-8 bg-dark-border"></div>

          <div>
            <h4 className="text-[10px] text-gray-500 font-bold uppercase tracking-wider leading-none">Active Incidents</h4>
            <span className="text-sm text-gray-200 font-extrabold mt-1 block">{activeCount}</span>
          </div>

          <div className="w-px h-8 bg-dark-border"></div>

          <div>
            <h4 className="text-[10px] text-gray-500 font-bold uppercase tracking-wider leading-none">Critical Spikes</h4>
            <span className="text-sm text-alert-high font-extrabold mt-1 block">{criticalCount}</span>
          </div>

          <div className="w-px h-8 bg-dark-border"></div>

          <div>
            <h4 className="text-[10px] text-gray-500 font-bold uppercase tracking-wider leading-none">Average GORI</h4>
            <span className={`text-sm font-extrabold mt-1 block ${
              avgGori > 70 ? 'text-alert-high drop-shadow-[0_0_10px_rgba(239,68,68,0.5)]' : 'text-severity-stable drop-shadow-[0_0_10px_rgba(16,185,129,0.5)]'
            }`}>{avgGori}%</span>
          </div>
        </div>
      </div>

      {/* Slide-out details panel if incident selected */}
      {selectedId && (
        <div className="w-96 shrink-0 h-full">
          <IncidentDetailsDrawer />
        </div>
      )}
    </div>
  );
};

export default LiveOperationsPage;
