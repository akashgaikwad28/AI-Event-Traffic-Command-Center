import React, { useState } from 'react';
import { useDemoStore } from '../../store/demo.store';

export const ScenarioSelector: React.FC = () => {
  const { runVisualSimulation, isRunning } = useDemoStore();
  const [customLat, setCustomLat] = useState('40.7128');
  const [customLng, setCustomLng] = useState('-74.0060');
  const [severity, setSeverity] = useState('high');

  const handleCustom = (e: React.FormEvent) => {
    e.preventDefault();
    runVisualSimulation('CUSTOM_INCIDENT', {
      lat: parseFloat(customLat),
      lng: parseFloat(customLng),
      severity
    });
  };

  return (
    <div className="bg-slate-800 p-4 rounded-lg border border-slate-700 mb-4">
      <h3 className="text-lg font-bold text-white mb-3">Select Scenario</h3>
      
      <div className="grid grid-cols-2 gap-4 mb-4">
        <button 
          onClick={() => runVisualSimulation('ACCIDENT_CASCADE')}
          disabled={isRunning}
          className="bg-slate-700 hover:bg-slate-600 text-left p-3 rounded transition-colors disabled:opacity-50 border border-transparent hover:border-slate-500"
        >
          <div className="font-bold text-white">Accident Cascade</div>
          <div className="text-xs text-slate-400">High Risk • Major Intersection</div>
        </button>
        <button 
          onClick={() => runVisualSimulation('STADIUM_EVENT_EGRESS')}
          disabled={isRunning}
          className="bg-slate-700 hover:bg-slate-600 text-left p-3 rounded transition-colors disabled:opacity-50 border border-transparent hover:border-slate-500"
        >
          <div className="font-bold text-white">Stadium Egress</div>
          <div className="text-xs text-slate-400">Medium Risk • Planned Chaos</div>
        </button>
      </div>

      <div className="border-t border-slate-700 pt-4 mt-2">
        <h4 className="text-sm font-semibold text-slate-300 mb-2">Custom Simulation</h4>
        <form onSubmit={handleCustom} className="flex flex-wrap gap-2 items-end">
          <div className="flex-1">
            <label className="text-xs text-slate-400 block">Lat</label>
            <input type="text" value={customLat} onChange={e => setCustomLat(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-sm text-white" />
          </div>
          <div className="flex-1">
            <label className="text-xs text-slate-400 block">Lng</label>
            <input type="text" value={customLng} onChange={e => setCustomLng(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-sm text-white" />
          </div>
          <div className="flex-1">
            <label className="text-xs text-slate-400 block">Severity</label>
            <select value={severity} onChange={e => setSeverity(e.target.value)} className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1 text-sm text-white">
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
          </div>
          <button 
            type="submit" 
            disabled={isRunning}
            className="bg-blue-600 hover:bg-blue-500 text-white px-4 py-1 rounded transition-colors disabled:opacity-50"
          >
            Simulate
          </button>
        </form>
      </div>
    </div>
  );
};
