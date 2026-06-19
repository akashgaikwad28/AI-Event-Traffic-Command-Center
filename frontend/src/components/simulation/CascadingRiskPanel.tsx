import React from 'react';
import { useDemoStore } from '../../store/demo.store';

export const CascadingRiskPanel: React.FC = () => {
  const { simulationResult, playbackFrameIndex } = useDemoStore();

  if (!simulationResult) return null;

  const currentFrame = simulationResult.optimized_state.timeline_frames[playbackFrameIndex];
  if (!currentFrame) return null;

  const getRiskColor = (risk: string) => {
    switch(risk) {
      case 'CRITICAL': return 'bg-red-500';
      case 'HIGH': return 'bg-orange-500';
      case 'MEDIUM': return 'bg-yellow-500';
      default: return 'bg-green-500';
    }
  };

  const steps = [
    { label: "Primary Incident", active: currentFrame.time_offset_mins >= 0 },
    { label: "Secondary Congestion", active: currentFrame.time_offset_mins >= 10 },
    { label: "Route Saturation", active: currentFrame.time_offset_mins >= 20 },
    { label: "Network Risk", active: currentFrame.time_offset_mins >= 30 }
  ];

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-lg p-4 mt-4">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-white font-bold">Cascading Risk Assessment</h3>
        <span className={`px-2 py-1 rounded text-xs font-bold text-white ${getRiskColor(currentFrame.cascading_risk)}`}>
          {currentFrame.cascading_risk} RISK
        </span>
      </div>

      <div className="flex justify-between items-center relative">
        <div className="absolute left-0 top-1/2 w-full h-1 bg-slate-700 -z-0 -translate-y-1/2"></div>
        <div
          className="absolute left-0 top-1/2 h-1 bg-blue-500 -z-0 -translate-y-1/2 transition-all duration-300"
          style={{ width: `${(playbackFrameIndex / (simulationResult.optimized_state.timeline_frames.length - 1)) * 100}%` }}
        ></div>

        {steps.map((step, idx) => (
          <div key={idx} className="flex flex-col items-center z-10">
            <div className={`w-4 h-4 rounded-full border-2 transition-colors duration-300 ${step.active ? 'bg-blue-500 border-blue-400 shadow-[0_0_10px_rgba(59,130,246,0.8)]' : 'bg-slate-800 border-slate-600'}`}></div>
            <span className={`text-[10px] mt-2 font-semibold ${step.active ? 'text-white' : 'text-slate-500'}`}>{step.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
