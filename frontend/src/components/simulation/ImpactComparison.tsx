import React from 'react';
import { useDemoStore } from '../../store/demo.store';

export const ImpactComparison: React.FC = () => {
  const { simulationResult } = useDemoStore();

  if (!simulationResult) return null;

  const { improvements, baseline_state, optimized_state } = simulationResult;

  const MetricCard = ({ label, value, unit, isPositive }: any) => (
    <div className="bg-slate-800 p-4 rounded-lg border border-slate-700 flex flex-col items-center justify-center text-center transition-all hover:bg-slate-750 hover:border-slate-600">
      <span className="text-slate-400 text-xs font-semibold uppercase tracking-wider mb-2">{label}</span>
      <div className={`text-2xl font-bold ${isPositive ? 'text-green-400' : 'text-blue-400'}`}>
        {value}{unit}
      </div>
    </div>
  );

  return (
    <div className="space-y-4">
      <h3 className="text-xl font-bold text-white mb-4 border-b border-slate-700 pb-2">Business Impact Analysis</h3>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <MetricCard
          label="Response Time Reduced"
          value={improvements.response_time_reduction_mins}
          unit="m"
          isPositive={true}
        />
        <MetricCard
          label="Congestion Drop"
          value={improvements.congestion_reduction_pct}
          unit="%"
          isPositive={true}
        />
        <MetricCard
          label="GORI Improvement"
          value={improvements.gori_reduction}
          unit=" pts"
          isPositive={true}
        />
        <MetricCard
          label="Spread Prevented"
          value={improvements.spread_reduction_radius}
          unit="m"
          isPositive={true}
        />
        <MetricCard
          label="Officer Efficiency"
          value={`+${improvements.officer_efficiency_gain_pct}`}
          unit="%"
          isPositive={true}
        />
        <MetricCard
          label="Diversion Effectiveness"
          value={improvements.diversion_effectiveness_score}
          unit="/100"
          isPositive={false}
        />
        <MetricCard
          label="Citizens Saved"
          value={`~${improvements.estimated_citizens_impacted}`}
          unit=""
          isPositive={true}
        />
      </div>

      <div className="bg-slate-800 p-4 rounded-lg border border-slate-700 mt-4">
        <h4 className="text-sm text-slate-300 font-semibold mb-3 uppercase">GORI Evolution Timeline</h4>
        <div className="h-32 flex items-end gap-2 relative border-b border-l border-slate-600 pb-2 pl-2">
          {baseline_state.timeline_frames.map((frame, i) => {
            const optFrame = optimized_state.timeline_frames[i] || frame;
            const baseHeight = `${Math.min(100, frame.gori_score)}%`;
            const optHeight = `${Math.min(100, optFrame.gori_score)}%`;
            return (
              <div key={i} className="flex-1 flex items-end justify-center group relative gap-1">
                <div className="w-full bg-red-900/50 rounded-t transition-all" style={{ height: baseHeight }}></div>
                <div className="w-full bg-emerald-500/80 rounded-t transition-all absolute left-0 bottom-0" style={{ height: optHeight }}></div>
                <div className="opacity-0 group-hover:opacity-100 absolute -top-8 bg-slate-900 text-xs p-1 rounded z-10 whitespace-nowrap">
                  T+{frame.time_offset_mins}: {frame.gori_score.toFixed(0)} vs {optFrame.gori_score.toFixed(0)}
                </div>
              </div>
            );
          })}
        </div>
        <div className="flex justify-between text-xs text-slate-500 mt-2">
          <span>Start</span>
          <span>Timeline</span>
          <span>End</span>
        </div>
      </div>
    </div>
  );
};
