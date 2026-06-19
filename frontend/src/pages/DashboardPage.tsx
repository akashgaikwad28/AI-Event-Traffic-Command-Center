import React from 'react';
import { KPIBar } from '../components/dashboard/KPIBar';
import { IncidentFeed } from '../components/dashboard/IncidentFeed';
import { CommandMap } from '../components/maps/CommandMap';
import { DemoControls } from '../components/simulation/DemoControls';
import { useGoriStore } from '../store/gori.store';
import { useSimulationStore } from '../store/simulation.store';
import { ShieldCheck, Flame, Compass } from 'lucide-react';
import { CopilotPanel } from '../components/dashboard/CopilotPanel';

export const DashboardPage: React.FC = () => {
  const avgGori = useGoriStore((state) => state.avgGori);
  const plans = useSimulationStore((state) => Object.values(state.operationalPlans));

  return (
    <div className="h-full w-full overflow-y-auto p-6 space-y-6 bg-dark-bg">
      {/* Top Title Bar */}
      <div className="flex flex-col md:flex-row md:items-center md:justify-between space-y-2 md:space-y-0">
        <div>
          <h2 className="text-xl font-extrabold text-gray-100 tracking-wide">Operations Command Dashboard</h2>
          <p className="text-xs text-gray-500 font-medium mt-0.5">Real-time GORI intelligence engine, resource optimizations, and cascading simulations.</p>
        </div>
        <div className="flex items-center space-x-3 text-xxs font-bold uppercase tracking-wider">
          <span className="text-gray-500">System Time:</span>
          <span className="text-gray-400 bg-dark-card border border-dark-border px-2.5 py-1 rounded">
            {new Date().toLocaleTimeString()}
          </span>
        </div>
      </div>

      {/* KPI Bar */}
      <KPIBar />

      {/* Main Grid: Map Preview & Incident Stream */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Map preview and Demo injection */}
        <div className="lg:col-span-8 flex flex-col space-y-6">
          <div className="bg-dark-card border border-dark-border rounded-xl p-4 flex flex-col h-96 shadow-lg">
            <div className="flex items-center justify-between mb-3 shrink-0">
              <span className="font-bold text-gray-200 text-sm tracking-wide">Live Operations Map Preview</span>
              <span className="text-xxs text-gray-500 font-bold">Bangalore Grid View</span>
            </div>
            <div className="flex-1 min-h-0">
              <CommandMap />
            </div>
          </div>

          <DemoControls />
        </div>

        {/* Right Column: Incident feeds & GORI Risk Panel */}
        <div className="lg:col-span-4 flex flex-col space-y-6">
          {/* Live GORI Risk Panel */}
          <div className="bg-dark-card border border-dark-border rounded-xl p-5 shadow-lg relative overflow-hidden shrink-0">
            <div className="absolute top-0 right-0 p-4 opacity-5">
              <Flame className="w-24 h-24 text-red-500" />
            </div>
            <h3 className="font-bold text-gray-200 text-sm tracking-wide mb-3">AI Congestion Volatility (GORI)</h3>
            <div className="flex items-center space-x-4">
              <div className="relative flex items-center justify-center w-20 h-20 shrink-0">
                {/* Circular indicator */}
                <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
                  <path
                    className="text-dark-border"
                    strokeWidth="3.5"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <path
                    className={avgGori > 70 ? 'text-red-500' : 'text-emerald-400'}
                    strokeWidth="3.5"
                    strokeDasharray={`${avgGori}, 100`}
                    strokeLinecap="round"
                    stroke="currentColor"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                </svg>
                <div className="absolute text-center">
                  <span className="text-lg font-black text-gray-150 leading-none">{avgGori}</span>
                  <span className="text-[9px] text-gray-500 block leading-none font-bold">%</span>
                </div>
              </div>
              <div className="flex-1 w-full">
                <div className="flex justify-between items-end mb-2">
                  <div>
                    <span className="text-[10px] text-gray-500 uppercase tracking-wider block font-bold">Risk Status</span>
                    <span className={`text-md font-extrabold block mt-0.5 ${
                      avgGori > 70 ? 'text-red-400 animate-pulse' : (avgGori > 45 ? 'text-amber-400' : 'text-emerald-400')
                    }`}>
                      {avgGori > 70 ? 'CRITICAL SPIKE' : (avgGori > 45 ? 'ELEVATED FLOW' : 'NOMINAL RANGE')}
                    </span>
                  </div>
                </div>

                {/* 5-Component Drill-down */}
                <div className="space-y-2.5 mt-3">
                  {[
                    { label: 'Congestion Risk', val: Math.min(100, avgGori * 1.1) },
                    { label: 'Hotspot Severity', val: Math.min(100, avgGori * 1.25) },
                    { label: 'Deployment Pressure', val: Math.max(10, avgGori * 0.8) },
                    { label: 'Cascading Spread', val: avgGori > 60 ? 85 : 20 },
                    { label: 'Rush-Hour Stress', val: Math.min(100, avgGori * 0.9) }
                  ].map((comp, idx) => (
                    <div key={idx} className="relative">
                      <div className="flex justify-between text-[9px] font-bold text-gray-400 mb-1 uppercase tracking-wider">
                        <span>{comp.label}</span>
                        <span className={comp.val > 75 ? 'text-red-400' : 'text-gray-300'}>{Math.round(comp.val)}%</span>
                      </div>
                      <div className="w-full bg-dark-bg/80 rounded-full h-1.5 overflow-hidden">
                        <div
                          className={`h-1.5 rounded-full transition-all duration-1000 ease-out ${
                            comp.val > 75 ? 'bg-gradient-to-r from-red-500 to-red-400' :
                            comp.val > 50 ? 'bg-gradient-to-r from-amber-500 to-amber-400' :
                            'bg-gradient-to-r from-emerald-500 to-emerald-400'
                          }`}
                          style={{ width: `${comp.val}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="h-64">
            <IncidentFeed />
          </div>

          <div className="flex-1 min-h-[300px]">
            <CopilotPanel />
          </div>
        </div>
      </div>

      {/* Bottom Row: AI Optimizations Summary */}
      <div className="bg-dark-card border border-dark-border rounded-xl p-5 shadow-lg">
        <h3 className="font-bold text-gray-200 text-sm tracking-wide mb-4 flex items-center">
          <Compass className="w-4 h-4 text-brand-accent mr-1.5" />
          Active Strategic Operations Summary
        </h3>

        {plans.length === 0 ? (
          <div className="text-center py-6 text-gray-500 italic text-xs space-y-1">
            <ShieldCheck className="w-8 h-8 text-gray-600 mx-auto" />
            <p>No active dispatch optimizations deployed.</p>
            <p className="text-xxs font-normal text-gray-650">Deploy a scenario or click an incident to generate plans.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {plans.slice(0, 3).map((p, i) => (
              <div key={i} className="bg-dark-bg/60 border border-dark-border rounded-lg p-3.5 space-y-2">
                <div className="flex justify-between items-center">
                  <span className="text-xs font-bold text-purple-400">{p.plan_id}</span>
                  <span className="text-[9px] px-1.5 py-0.2 bg-emerald-500/10 border border-emerald-500/25 text-emerald-400 font-bold rounded">
                    Risk: {p.operational_risk}
                  </span>
                </div>
                <p className="text-xs text-gray-300 font-bold leading-relaxed">{p.recommended_plan}</p>
                <div className="flex justify-between text-xxs text-gray-500 border-t border-dark-border/40 pt-2 font-medium">
                  <span>Officers: {p.resource_plan?.police_officers}</span>
                  <span>Bypass: -{p.diversion_plan?.congestion_bypass_pct}%</span>
                  <span className="text-emerald-400 font-bold">Cost: ${p.resource_plan?.estimated_cost}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;
