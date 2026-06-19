import React, { useEffect, useState } from 'react';
import { useCopilotStore } from '../../store/copilot.store';
import { useIncidentStore } from '../../store/incident.store';
import { BrainCircuit, Sparkles, AlertTriangle, ChevronRight, Loader2 } from 'lucide-react';
import { api } from '../../services/api';

type CopilotMode = 'EXECUTIVE' | 'DISPATCHER' | 'ANALYST';

export const CopilotPanel: React.FC = () => {
  const selectedId = useIncidentStore((state) => state.selectedIncidentId);
  const selectedIncident = useIncidentStore((state) => selectedId ? state.incidents[selectedId] : null);
  
  const { explanations, isGenerating, setExplanation, setGenerating } = useCopilotStore();
  const [activeMode, setActiveMode] = useState<CopilotMode>('EXECUTIVE');
  
  const currentExplanation = selectedId ? explanations[selectedId] : null;

  useEffect(() => {
    if (selectedIncident && !isGenerating) {
      const fetchExplanation = async () => {
        setGenerating(true);
        try {
          const res = await api.getIncidentExplanation({
            incident_id: selectedIncident.incident_id,
            type: selectedIncident.type,
            gori_score: selectedIncident.gori_score,
            latitude: selectedIncident.latitude,
            longitude: selectedIncident.longitude,
            mode: activeMode // Optional payload if backend supports it
          });
          
          let explanationText = res.explanation || res.narrative || res.data;
          
          if (res.provider) {
             explanationText = `<div class="mb-3 pb-2 border-b border-brand-accent/20 flex items-center justify-between"><span class="text-[9px] font-bold text-brand-accent uppercase tracking-widest flex items-center"><span class="w-1.5 h-1.5 bg-emerald-400 rounded-full mr-1.5 animate-pulse"></span>ACTIVE LLM: ${res.provider}</span></div>${explanationText}`;
          }
          
          // Frontend simulated tone shift if backend returns same text
          if (activeMode === 'EXECUTIVE') {
            explanationText = `<div class="mb-2 font-bold text-white">Executive Summary</div>${explanationText}`;
          } else if (activeMode === 'DISPATCHER') {
            explanationText = `<div class="mb-2 font-bold text-alert-emergency">Tactical Dispatch Required</div><div class="mb-2 text-gray-400">Units must be mobilized immediately.</div>${explanationText}`;
          } else if (activeMode === 'ANALYST') {
            explanationText = `<div class="mb-2 font-bold text-brand-primary">GORI Factor Analysis</div><div class="mb-2 text-gray-400">Deep causal breakdown of current severity metrics.</div>${explanationText}`;
          }

          setExplanation(selectedIncident.incident_id, explanationText);
        } catch (err) {
          console.error(err);
          setExplanation(selectedIncident.incident_id, "Unable to generate AI explanation at this time.");
        } finally {
          setGenerating(false);
        }
      };
      fetchExplanation();
    }
  }, [selectedIncident, activeMode, setExplanation, setGenerating]); // Re-run when mode changes

  return (
    <div className="bg-[#121626] border border-brand-accent/20 rounded-xl p-5 shadow-glow-elevated flex flex-col h-full relative overflow-hidden">
      <div className="absolute top-0 right-0 w-32 h-32 bg-brand-accent/5 rounded-full blur-3xl transform translate-x-1/2 -translate-y-1/2"></div>
      
      <div className="flex flex-col mb-4 z-10 space-y-3">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-gray-200 text-sm tracking-wide flex items-center">
            <BrainCircuit className="w-5 h-5 text-brand-accent mr-2" />
            GridWise Copilot AI
          </h3>
          {isGenerating && <Loader2 className="w-4 h-4 text-brand-accent animate-spin" />}
        </div>

        {/* Mode Toggles */}
        <div className="flex bg-dark-bg/80 border border-dark-border p-1 rounded-lg">
          {(['EXECUTIVE', 'DISPATCHER', 'ANALYST'] as CopilotMode[]).map((mode) => (
            <button
              key={mode}
              onClick={() => setActiveMode(mode)}
              className={`flex-1 text-[10px] font-bold py-1.5 rounded-md transition-colors uppercase tracking-wider ${
                activeMode === mode
                  ? 'bg-brand-accent/20 text-brand-accent border border-brand-accent/30 shadow-glow-elevated'
                  : 'text-gray-500 hover:text-gray-300 hover:bg-dark-border/40 border border-transparent'
              }`}
            >
              {mode}
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar z-10">
        {!selectedIncident ? (
          <div className="h-full flex flex-col items-center justify-center text-center space-y-3 opacity-60">
            <Sparkles className="w-10 h-10 text-brand-primary" />
            <p className="text-xs text-gray-400 font-medium max-w-[200px]">
              Select an incident from the map or feed to generate AI operational insights.
            </p>
          </div>
        ) : (
          <div className="space-y-4">
            <div className="bg-dark-bg/60 border border-dark-border rounded-lg p-3">
              <div className="flex items-center justify-between mb-2 border-b border-dark-border/50 pb-2">
                <span className="text-xs font-bold text-gray-300">Context: {selectedIncident.incident_id}</span>
                <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold ${
                  selectedIncident.gori_score > 70 ? 'bg-alert-emergency/20 text-alert-emergency' : 'bg-brand-primary/20 text-brand-primary'
                }`}>
                  GORI {Math.round(selectedIncident.gori_score)}
                </span>
              </div>
              
              {isGenerating ? (
                <div className="py-4 space-y-3 animate-pulse">
                  <div className="h-2 bg-dark-border rounded w-3/4"></div>
                  <div className="h-2 bg-dark-border rounded w-full"></div>
                  <div className="h-2 bg-dark-border rounded w-5/6"></div>
                </div>
              ) : (
                <div className="text-xs text-gray-300 leading-relaxed prose prose-invert">
                  {currentExplanation ? (
                    <div dangerouslySetInnerHTML={{ __html: currentExplanation.replace(/\n/g, '<br />') }} />
                  ) : (
                    <p className="text-gray-500 italic">No insights available.</p>
                  )}
                </div>
              )}
            </div>

            {currentExplanation && !isGenerating && (
              <div className="bg-brand-accent/5 border border-brand-accent/20 rounded-lg p-3">
                <h4 className="text-xxs font-bold uppercase tracking-wider text-brand-accent mb-2 flex items-center">
                  <AlertTriangle className="w-3 h-3 mr-1" /> Tactical Recommendation
                </h4>
                <p className="text-xs text-gray-300">
                  {selectedIncident.deployment_recommendation || "Initiate standard diversion protocol and deploy fast response units to coordinates."}
                </p>
                <button className="mt-3 w-full bg-brand-accent/10 hover:bg-brand-accent/20 text-brand-accent border border-brand-accent/30 rounded py-1.5 text-xs font-bold transition-colors flex items-center justify-center">
                  Execute Simulation <ChevronRight className="w-3 h-3 ml-1" />
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
