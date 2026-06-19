import React from 'react';
import { useSimulationStore } from '../store/simulation.store';
import { PlayCircle, ShieldCheck, Activity, BrainCircuit } from 'lucide-react';
import { DemoControls } from '../components/simulation/DemoControls';

export const SimulationPage: React.FC = () => {
  const plans = useSimulationStore((state) => Object.values(state.operationalPlans));

  // Find the most recent or active simulation result to showcase
  const demoPlan = plans.length > 0 ? plans[plans.length - 1] : null;
  const impact = demoPlan?.predicted_impact?.expected_case || demoPlan?.predicted_impact?.EXPECTED_CASE;

  return (
    <div className="h-full w-full overflow-y-auto p-6 space-y-6 bg-dark-bg text-gray-200">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-wider text-white">Simulation Engine & Demo Mode</h2>
          <p className="text-sm text-gray-400">Real-Time Scenario Injector & AI Impact Analysis</p>
        </div>
      </div>

      <div className="flex flex-col gap-6">
        {/* Control Panel - Now takes full width so the 5-column grid isn't squished */}
        <div className="w-full">
          <DemoControls />
        </div>

        {/* Simulation Results Display - Now takes full width below */}
        <div className="w-full">
          {demoPlan && impact ? (
            <div className="bg-dark-card border border-dark-border rounded-xl p-6 shadow-glow-elevated transform transition-all duration-500 hover:shadow-brand-primary/20">
              <h3 className="text-xl font-bold text-brand-primary mb-6 flex items-center">
                <BrainCircuit className="w-6 h-6 mr-3" />
                AI Optimization Plan Executed
              </h3>
              
              {/* Premium Before/After Visuals */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                {/* Before */}
                <div className="bg-[#121626] border border-red-500/30 p-6 rounded-xl relative overflow-hidden group">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-red-500/10 rounded-full blur-3xl transform translate-x-1/2 -translate-y-1/2 group-hover:bg-red-500/20 transition-all duration-700"></div>
                  <div className="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-red-600 to-red-900"></div>
                  <h4 className="text-sm text-gray-400 font-bold uppercase tracking-wider mb-4 flex items-center">
                    <span className="w-2 h-2 bg-red-500 rounded-full mr-2 animate-pulse"></span>
                    Before Optimization
                  </h4>
                  <div className="flex items-end space-x-3">
                    <span className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-br from-red-400 to-red-700 tracking-tighter">
                      {demoPlan.gori_score_before ? Math.round(demoPlan.gori_score_before) : '85'}
                    </span>
                    <span className="text-sm text-red-500 font-bold uppercase tracking-widest pb-2">GORI Score</span>
                  </div>
                  <p className="text-sm text-red-400/80 mt-4 font-medium">Critical traffic gridlock detected. Unmitigated cascading failure imminent.</p>
                </div>
                
                {/* After */}
                <div className="bg-[#121626] border border-brand-accent/40 p-6 rounded-xl relative overflow-hidden group shadow-[0_0_30px_rgba(45,212,191,0.05)]">
                  <div className="absolute top-0 right-0 w-32 h-32 bg-brand-accent/20 rounded-full blur-3xl transform translate-x-1/2 -translate-y-1/2 group-hover:bg-brand-accent/30 transition-all duration-700"></div>
                  <div className="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-brand-accent to-brand-primary"></div>
                  <h4 className="text-sm text-gray-400 font-bold uppercase tracking-wider mb-4 flex items-center">
                    <span className="w-2 h-2 bg-brand-accent rounded-full mr-2"></span>
                    After AI Intervention
                  </h4>
                  <div className="flex items-end space-x-3">
                    <span className="text-6xl font-black text-transparent bg-clip-text bg-gradient-to-br from-brand-accent to-brand-primary tracking-tighter">
                      {Math.max(0, (demoPlan.gori_score_before || 85) - Math.round(impact.congestion_reduction))}
                    </span>
                    <span className="text-sm text-brand-accent font-bold uppercase tracking-widest pb-2">GORI Score</span>
                  </div>
                  <p className="text-sm text-brand-accent/80 mt-4 font-medium flex items-center">
                    <Activity className="w-4 h-4 mr-2" />
                    Predicted optimal state achieved. Grid flow stabilized.
                  </p>
                </div>
              </div>

              {/* Enhanced Action Readout */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <div className="bg-dark-bg/50 p-5 rounded-xl border border-dark-border/50 relative overflow-hidden">
                  <div className="absolute top-0 left-0 w-1 h-full bg-emerald-500/50"></div>
                  <h4 className="text-xs font-bold text-gray-300 uppercase tracking-wider mb-3">Active Diversion Route</h4>
                  <p className="text-sm text-emerald-100 font-mono leading-relaxed">{demoPlan.diversion_plan?.description || 'Rerouting major arterials to bypass incident zone.'}</p>
                </div>
                
                <div className="bg-dark-bg/50 p-5 rounded-xl border border-dark-border/50 relative overflow-hidden flex flex-col justify-center">
                  <div className="absolute top-0 left-0 w-1 h-full bg-brand-primary/50"></div>
                  <div className="flex items-center space-x-6">
                    <div className="flex flex-col">
                      <span className="text-2xl font-bold text-gray-100">{demoPlan.resource_plan?.police_officers || 0}</span>
                      <span className="text-xs text-gray-500 uppercase tracking-wide font-bold">Officers</span>
                    </div>
                    <div className="flex flex-col">
                      <span className="text-2xl font-bold text-gray-100">{demoPlan.resource_plan?.barricades || 0}</span>
                      <span className="text-xs text-gray-500 uppercase tracking-wide font-bold">Barricades</span>
                    </div>
                    <div className="flex items-center text-sm font-semibold text-brand-primary ml-auto">
                      <ShieldCheck className="w-5 h-5 mr-2" /> Assets Deployed
                    </div>
                  </div>
                </div>
              </div>

            </div>
          ) : (
            <div className="w-full bg-dark-card border border-dark-border border-dashed rounded-xl p-16 flex flex-col items-center justify-center text-gray-500 hover:border-gray-600 transition-colors">
              <PlayCircle className="w-16 h-16 mb-6 opacity-40 text-brand-primary animate-pulse" />
              <p className="font-bold text-2xl text-gray-300 mb-2">Awaiting Simulation Injection</p>
              <p className="text-base text-gray-500 text-center max-w-md">Select one of the 10 real-time simulation scenarios from the control panel above to watch the AI evaluate and resolve gridlock.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
