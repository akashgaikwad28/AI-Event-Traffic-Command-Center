import React, { useState, useEffect } from 'react';
import { CopilotPanel } from '../dashboard/CopilotPanel';
import { BrainCircuit, X } from 'lucide-react';
import { useIncidentStore } from '../../store/incident.store';

export const FloatingCopilotWidget: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const selectedId = useIncidentStore((state) => state.selectedIncidentId);

  // Auto-open the copilot when a new incident is selected
  useEffect(() => {
    if (selectedId) {
      setIsOpen(true);
    }
  }, [selectedId]);

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col items-end">

      {/* The Floating Panel */}
      <div
        className={`transition-all duration-300 ease-in-out origin-bottom-right mb-4 ${
          isOpen ? 'scale-100 opacity-100 pointer-events-auto' : 'scale-95 opacity-0 pointer-events-none'
        }`}
        style={{ width: '400px', height: '600px' }}
      >
        {/* We reuse the exact CopilotPanel component but inside this fixed container */}
        <div className="h-full w-full rounded-2xl shadow-2xl overflow-hidden border border-brand-accent/30 bg-[#0B0F19]">
          <CopilotPanel />
        </div>
      </div>

      {/* The Floating Action Button (FAB) */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`group flex items-center justify-center space-x-2 px-5 py-3.5 rounded-full shadow-glow-elevated transition-all duration-300 hover:scale-105 ${
          isOpen
            ? 'bg-dark-card border border-dark-border text-gray-400 w-14 h-14 !px-0'
            : 'bg-gradient-to-r from-brand-primary to-brand-accent text-white border-2 border-brand-accent/50 min-w-[200px]'
        }`}
      >
        {isOpen ? (
          <X className="w-6 h-6" />
        ) : (
          <>
            <div className="relative">
               <BrainCircuit className="w-6 h-6 animate-pulse" />
               {/* Pulse ring if an incident is selected but panel is closed */}
               {selectedId && (
                 <span className="absolute -top-1 -right-1 flex h-3 w-3">
                   <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>
                   <span className="relative inline-flex rounded-full h-3 w-3 bg-white"></span>
                 </span>
               )}
            </div>
            <span className="font-bold tracking-wide text-sm pr-1">GridWise AI Copilot</span>
          </>
        )}
      </button>

    </div>
  );
};
