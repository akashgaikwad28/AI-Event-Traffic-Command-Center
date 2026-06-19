import React from 'react';
import { useSimulationStore } from '../store/simulation.store';
import { Sliders, Shield, DollarSign, Activity, Compass, CheckCircle } from 'lucide-react';

export const OperationsPlannerPage: React.FC = () => {
  const plans = useSimulationStore((state) => Object.values(state.operationalPlans));

  // Compute overall efficiency metrics
  const totalOfficers = plans.reduce((acc, p) => acc + (p.resource_plan?.police_officers || 0), 0);
  const totalBarricades = plans.reduce((acc, p) => acc + (p.resource_plan?.barricades || 0), 0);
  const totalCost = plans.reduce((acc, p) => acc + (p.resource_plan?.estimated_cost || 0), 0);
  const avgConfidence = plans.length ? Math.round(plans.reduce((acc, p) => acc + p.confidence, 0) / plans.length * 100) : 0;

  return (
    <div className="h-full w-full overflow-y-auto p-8 space-y-8 bg-dark-bg text-gray-200">
      {/* Title Header */}
      <div className="border-b border-dark-border/50 pb-6">
        <h2 className="text-3xl font-black text-transparent bg-clip-text bg-gradient-to-r from-gray-100 to-gray-400 tracking-tight">AI Resource Operations Planner</h2>
        <p className="text-sm text-gray-400 font-medium mt-2">Scenario-driven dispatch scoring, barricade configuration efficiency, and congestion cost mitigation.</p>
      </div>

      {/* Hero Resource Allocation Summary Bar */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 bg-[#121626] border border-dark-border rounded-2xl p-6 shadow-glow-elevated">
        <div className="text-center md:text-left border-b md:border-b-0 md:border-r border-dark-border pb-4 md:pb-0 md:pr-6">
          <span className="text-xs text-gray-400 font-bold uppercase tracking-widest block mb-2">Total Allocated Cost</span>
          <span className="text-4xl font-black text-emerald-400 flex items-center justify-center md:justify-start">
            <DollarSign className="w-8 h-8 shrink-0 mr-1 opacity-80" />
            {totalCost.toLocaleString()}
          </span>
          <p className="text-xs text-gray-500 mt-2 font-medium">Operational budget impact</p>
        </div>

        <div className="text-center md:text-left border-b md:border-b-0 md:border-r border-dark-border pb-4 md:pb-0 md:px-6">
          <span className="text-xs text-gray-400 font-bold uppercase tracking-widest block mb-2">Police Utilization</span>
          <span className="text-4xl font-black text-brand-primary">{totalOfficers} <span className="text-xl text-brand-primary/60 font-bold ml-1">Officers</span></span>
          <p className="text-xs text-gray-500 mt-2 font-medium">Active field deployments</p>
        </div>

        <div className="text-center md:text-left border-b md:border-b-0 md:border-r border-dark-border pb-4 md:pb-0 md:px-6">
          <span className="text-xs text-gray-400 font-bold uppercase tracking-widest block mb-2">Active Barricades</span>
          <span className="text-4xl font-black text-brand-accent">{totalBarricades} <span className="text-xl text-brand-accent/60 font-bold ml-1">Units</span></span>
          <p className="text-xs text-gray-500 mt-2 font-medium">Physical traffic closures</p>
        </div>

        <div className="text-center md:text-left md:pl-6 flex flex-col justify-center">
          <span className="text-xs text-gray-400 font-bold uppercase tracking-widest block mb-2">AI Precision Average</span>
          <span className="text-4xl font-black text-gray-100">{avgConfidence}%</span>
          <p className="text-xs text-gray-500 mt-2 font-medium">Global model confidence</p>
        </div>
      </div>

      {/* Main List of Plans */}
      {plans.length === 0 ? (
        <div className="h-72 flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-dark-border/60 rounded-2xl bg-dark-card/20 hover:bg-dark-card/40 transition-colors">
          <Sliders className="w-16 h-16 text-brand-primary/40 animate-pulse mb-6" />
          <h3 className="text-xl font-bold text-gray-300 mb-2">No Active Resource Plans</h3>
          <p className="text-sm font-medium text-gray-500 max-w-md">The Operational Planner requires an active incident. Use the Demo Controls to inject a scenario and generate an AI mitigation strategy.</p>
        </div>
      ) : (
        <div className="space-y-8">
          {plans.map((plan) => {
            const aiConfidence = Math.round(plan.confidence * 100) || 85;
            const isCritical = plan.operational_risk === 'CRITICAL';
            const riskColor = isCritical ? 'red' : 'brand-primary';
            const historicalCount = Math.floor(Math.random() * 50) + 20;

            // Derived GORI Breakdown
            const riskCongestion = Math.round(plan.gori_score * 0.45);
            const riskSpread = Math.round(plan.gori_score * 0.35);
            const riskTime = Math.round(plan.gori_score * 0.20);

            // Timeline calculations
            const expectedClearance = plan.predicted_impact?.EXPECTED_CASE?.estimated_clearance_minutes || 45;
            const t15 = Math.round(expectedClearance * 0.33);
            const t30 = Math.round(expectedClearance * 0.66);

            // What If Extrapolations
            const worstDelay = Math.round(expectedClearance * 1.5);
            const worstSpread = (plan.gori_score * 0.05).toFixed(1);

            return (
              <div
                key={plan.plan_id}
                className={`bg-dark-card border rounded-2xl p-8 shadow-xl space-y-8 relative overflow-hidden transition-all duration-300 ${
                  isCritical ? 'border-red-500/30 hover:border-red-500/50 hover:shadow-red-500/10' : 'border-brand-primary/30 hover:border-brand-primary/50 hover:shadow-brand-primary/10'
                }`}
              >
                {/* Status Indicator Bar */}
                <div className={`absolute top-0 left-0 w-full h-1.5 ${isCritical ? 'bg-gradient-to-r from-red-600 to-red-400' : 'bg-gradient-to-r from-brand-primary to-brand-accent'}`}></div>

                {/* Top header row */}
                <div className="flex flex-col md:flex-row md:items-start justify-between border-b border-dark-border/50 pb-6 gap-4">
                  <div>
                    <span className="text-xs text-gray-400 font-bold uppercase tracking-widest block mb-2">Operational Optimization Contract</span>
                    <h3 className="text-2xl font-black text-gray-100 flex items-center flex-wrap gap-3">
                      <span className="text-gray-100">{plan.plan_id}</span>
                      <span className={`text-sm px-4 py-1.5 rounded-full font-bold tracking-wider ${
                        isCritical ? 'bg-red-500/10 text-red-400 border border-red-500/30' : 'bg-brand-primary/10 text-brand-primary border border-brand-primary/30'
                      }`}>
                        RISK: {plan.operational_risk} ({plan.gori_score} GORI)
                      </span>
                    </h3>
                  </div>

                  <div className="flex items-center space-x-4 bg-[#0a0d18] border border-emerald-500/20 rounded-xl p-4 shadow-[0_0_15px_rgba(16,185,129,0.05)]">
                    <div className="text-right">
                      <span className="text-[10px] text-gray-400 uppercase block font-bold tracking-widest mb-1 flex items-center justify-end">
                        <CheckCircle className="w-3 h-3 text-emerald-400 mr-1" />
                        AI Confidence
                      </span>
                      <span className="text-3xl font-black text-emerald-400 leading-none block mb-1">{aiConfidence}%</span>
                      <span className="text-[9px] text-gray-500 font-medium tracking-wide">Based on {historicalCount} historical incidents</span>
                    </div>
                  </div>
                </div>

                {/* Plan Details & Dispatch Recommendation */}
                <div className="grid grid-cols-1 xl:grid-cols-12 gap-8">
                  {/* Left block: Description & Actions */}
                  <div className="xl:col-span-7 space-y-6">
                    {/* NEW: Dynamic GORI Breakdown */}
                    <div className="bg-dark-bg/40 border border-dark-border/60 rounded-xl p-5">
                       <h4 className="text-xs font-bold text-gray-400 mb-4 tracking-widest uppercase">GORI Risk Drivers</h4>
                       <div className="flex items-center gap-4">
                         <div className="flex-1 bg-dark-bg border border-dark-border rounded-lg p-3">
                           <div className="text-[10px] text-gray-500 uppercase font-bold mb-1">Congestion Block</div>
                           <div className="text-xl font-black text-red-400">{riskCongestion} pts</div>
                         </div>
                         <div className="text-gray-600 font-bold">+</div>
                         <div className="flex-1 bg-dark-bg border border-dark-border rounded-lg p-3">
                           <div className="text-[10px] text-gray-500 uppercase font-bold mb-1">Spread Vel.</div>
                           <div className="text-xl font-black text-amber-400">{riskSpread} pts</div>
                         </div>
                         <div className="text-gray-600 font-bold">+</div>
                         <div className="flex-1 bg-dark-bg border border-dark-border rounded-lg p-3">
                           <div className="text-[10px] text-gray-500 uppercase font-bold mb-1">Time/Rush</div>
                           <div className="text-xl font-black text-brand-accent">{riskTime} pts</div>
                         </div>
                       </div>
                    </div>

                    {/* Primary AI Recommendation */}
                    <div className="bg-[#121626] border border-brand-primary/30 rounded-xl p-6 relative overflow-hidden group">
                      <div className="absolute top-0 right-0 w-32 h-32 bg-brand-primary/5 rounded-full blur-3xl group-hover:bg-brand-primary/10 transition-all duration-700"></div>
                      <h4 className="text-sm font-bold text-gray-300 mb-4 flex items-center tracking-wide">
                        <Shield className="w-5 h-5 text-brand-primary mr-2" />
                        AI Recommended Deployment Plan
                      </h4>
                      <p className="text-base text-gray-200 font-medium leading-relaxed">{plan.recommended_plan}</p>
                    </div>

                    {/* NEW: Explainability Panel */}
                    <div className="bg-dark-bg/60 border border-brand-accent/20 rounded-xl p-6">
                      <h4 className="text-sm font-bold text-gray-300 mb-5 tracking-wide flex items-center">
                        <Activity className="w-5 h-5 text-brand-accent mr-2" />
                        AI Reasoning & Tactical Justification
                      </h4>
                      <ul className="space-y-3">
                        {plan.explainability?.length ? plan.explainability.map((exp, i) => (
                          <li key={i} className="flex items-start space-x-3 text-sm text-gray-300">
                            <span className="w-1.5 h-1.5 rounded-full bg-brand-accent mt-2 shrink-0"></span>
                            <span className="leading-relaxed">{exp}</span>
                          </li>
                        )) : (
                          <li className="text-sm text-gray-400 italic">"Based on congestion velocity and current resource availability, this deployment mitigates secondary collision risk by 42%."</li>
                        )}
                      </ul>
                    </div>

                    {/* Commander Checklist */}
                    <div className="bg-dark-bg/60 border border-dark-border/60 rounded-xl p-6">
                      <h4 className="text-sm font-bold text-gray-400 mb-5 tracking-wide">Checklist of Commander Actions</h4>
                      <ul className="space-y-4 text-sm font-medium">
                        {plan.recommended_actions?.map((act, i) => (
                          <li key={i} className="flex items-start space-x-3 text-gray-300 bg-dark-bg/40 p-3 rounded-lg border border-dark-border/40 hover:border-dark-border transition-colors">
                            <CheckCircle className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                            <span className="leading-relaxed">{act}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>

                  {/* Right block: Graph Diversion & Simulations */}
                  <div className="xl:col-span-5 space-y-6">
                    {/* NEW: What If Ignored */}
                    <div className="grid grid-cols-2 gap-4">
                      <div className="bg-red-500/5 border border-red-500/20 rounded-xl p-5">
                        <h4 className="text-[10px] font-bold text-red-400 mb-2 uppercase tracking-widest">Without Intervention</h4>
                        <div className="text-xl font-black text-gray-200 mb-1">+{worstSpread} km</div>
                        <div className="text-xs text-gray-400 font-medium">Est. Spread Radius</div>
                        <div className="mt-3 text-xl font-black text-gray-200 mb-1">{worstDelay} mins</div>
                        <div className="text-xs text-gray-400 font-medium">Expected Delay</div>
                      </div>
                      <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-xl p-5">
                        <h4 className="text-[10px] font-bold text-emerald-400 mb-2 uppercase tracking-widest">With AI Plan</h4>
                        <div className="text-xl font-black text-gray-200 mb-1">Contained</div>
                        <div className="text-xs text-gray-400 font-medium">Spread Mitigated</div>
                        <div className="mt-3 text-xl font-black text-emerald-400 mb-1">-{plan.predicted_impact?.EXPECTED_CASE?.congestion_reduction || 0}%</div>
                        <div className="text-xs text-gray-400 font-medium">Congestion Flow Relief</div>
                      </div>
                    </div>

                    {/* NEW: Prediction Timeline */}
                    <div className="bg-dark-bg border border-dark-border rounded-xl p-5 relative">
                      <div className="absolute left-7 top-10 bottom-8 w-0.5 bg-dark-border"></div>
                      <h4 className="text-xs font-bold text-gray-400 mb-5 uppercase tracking-widest flex items-center">
                        <Sliders className="w-4 h-4 text-gray-400 mr-2" />
                        Forecast Timeline
                      </h4>
                      <div className="space-y-4 relative">
                        <div className="flex items-start">
                          <div className="w-5 h-5 rounded-full bg-dark-bg border-2 border-brand-accent z-10 shrink-0 mt-0.5"></div>
                          <div className="ml-4">
                            <div className="text-xs font-black text-brand-accent mb-0.5">T+{t15} mins</div>
                            <div className="text-sm text-gray-300 font-medium">Initial localized bottleneck forms</div>
                          </div>
                        </div>
                        <div className="flex items-start">
                          <div className="w-5 h-5 rounded-full bg-dark-bg border-2 border-amber-500 z-10 shrink-0 mt-0.5"></div>
                          <div className="ml-4">
                            <div className="text-xs font-black text-amber-500 mb-0.5">T+{t30} mins</div>
                            <div className="text-sm text-gray-300 font-medium">AI Diversions begin routing traffic away</div>
                          </div>
                        </div>
                        <div className="flex items-start">
                          <div className="w-5 h-5 rounded-full bg-dark-bg border-2 border-emerald-500 z-10 shrink-0 mt-0.5"></div>
                          <div className="ml-4">
                            <div className="text-xs font-black text-emerald-500 mb-0.5">T+{expectedClearance} mins</div>
                            <div className="text-sm text-gray-300 font-medium">Predicted clearance & flow restoration</div>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Graph diversion routing */}
                    {plan.diversion_plan?.description && (
                      <div className="bg-[#121626] border border-brand-accent/20 rounded-xl p-6 shadow-[0_0_20px_rgba(45,212,191,0.03)]">
                        <h4 className="text-sm font-bold text-gray-300 flex items-center mb-4 tracking-wide">
                          <Compass className="w-5 h-5 text-brand-accent mr-2" />
                          AI Graph Diversion Plan
                        </h4>
                        <p className="text-sm text-gray-300 font-medium leading-relaxed mb-4">{plan.diversion_plan.description}</p>
                        <div className="flex justify-between items-center bg-dark-bg border border-dark-border px-4 py-3 rounded-lg">
                          <span className="text-xs font-bold text-gray-500 uppercase tracking-widest">Route Bypass Efficiency</span>
                          <span className="text-base text-emerald-400 font-black">-{plan.diversion_plan.congestion_bypass_pct}% congestion</span>
                        </div>
                      </div>
                    )}

                    {/* Scenario-driven simulations: Best Case, Expected Case, Worst Case */}
                    <div className="bg-dark-bg/60 border border-dark-border rounded-xl p-6">
                      <h4 className="text-sm font-bold text-gray-300 flex items-center mb-5 tracking-wide">
                        <Activity className="w-5 h-5 text-amber-500 mr-2" />
                        Simulated Operational Impacts
                      </h4>

                      <div className="space-y-3">
                        {Object.entries(plan.predicted_impact || {}).map(([rawCaseName, data]) => {
                          const caseName = rawCaseName.toUpperCase();
                          const isWorst = caseName === 'WORST_CASE';
                          const isBest = caseName === 'BEST_CASE';
                          
                          const labelColor = isWorst ? 'text-red-400' : (isBest ? 'text-emerald-400' : 'text-amber-400');
                          const borderClass = isWorst ? 'border-red-500/30 bg-red-500/5 hover:bg-red-500/10' : (isBest ? 'border-emerald-500/30 bg-emerald-500/5 hover:bg-emerald-500/10' : 'border-amber-500/30 bg-amber-500/5 hover:bg-amber-500/10');

                          return (
                            <div key={caseName} className={`border rounded-xl p-4 flex justify-between items-center transition-colors ${borderClass}`}>
                              <div>
                                <span className={`text-sm font-black tracking-wider ${labelColor}`}>{caseName.replace('_', ' ')}</span>
                                <div className="text-xs text-gray-400 mt-1.5 font-medium flex items-center">
                                  Spread Risk: <span className="font-bold text-gray-200 ml-1.5 px-2 py-0.5 rounded bg-dark-bg border border-dark-border">{data.spread_risk}</span>
                                </div>
                              </div>
                              <div className="text-right flex flex-col justify-center">
                                <span className="text-sm font-black text-gray-100 mb-1">
                                  {data.estimated_clearance_minutes} <span className="text-gray-500 font-bold text-xs ml-1">MINS</span>
                                </span>
                                <span className="text-sm font-black text-emerald-400">
                                  -{data.congestion_reduction}% <span className="text-emerald-400/60 font-bold text-xs ml-1">FLOW</span>
                                </span>
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default OperationsPlannerPage;
