import React from 'react';
import { useDemoStore } from '../../store/demo.store';
import { ScenarioSelector } from './ScenarioSelector';
import { ImpactComparison } from './ImpactComparison';
import { CascadingRiskPanel } from './CascadingRiskPanel';
import { SimulationTimeline } from './SimulationTimeline';

export const SimulationPanel: React.FC = () => {
  const { runVisualDemo, isRunning, simulationResult } = useDemoStore();

  return (
    <div className="h-full flex flex-col overflow-hidden bg-slate-900 text-slate-200">
      <div className="flex justify-between items-center bg-slate-800 p-4 border-b border-slate-700">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <svg className="w-6 h-6 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
          Simulation Engine
        </h2>
        <button
          onClick={runVisualDemo}
          disabled={isRunning}
          className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold py-2 px-6 rounded-full shadow-lg transition-transform hover:scale-105 active:scale-95 disabled:opacity-50 disabled:scale-100 flex items-center gap-2"
        >
          <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg>
          RUN GRIDWISE STORY
        </button>
      </div>

      <div className="p-4 flex-1 overflow-y-auto">
        {!simulationResult ? (
          <div className="max-w-2xl mx-auto mt-8">
            <ScenarioSelector />
            <div className="text-center text-slate-500 mt-12 p-8 border border-dashed border-slate-700 rounded-lg">
              <svg className="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
              Select a scenario or run the executive demo to view simulation impacts.
            </div>
          </div>
        ) : (
          <div className="space-y-4 max-w-5xl mx-auto">
            <div className="flex justify-between items-center">
              <span className="text-slate-400">Current Scenario: <strong className="text-white uppercase">{simulationResult.scenario_type}</strong></span>
              <button
                onClick={() => useDemoStore.setState({ simulationResult: null })}
                className="text-sm text-slate-400 hover:text-white underline"
              >
                Back to Scenarios
              </button>
            </div>

            <SimulationTimeline />
            <ImpactComparison />
            <CascadingRiskPanel />
          </div>
        )}
      </div>
    </div>
  );
};
