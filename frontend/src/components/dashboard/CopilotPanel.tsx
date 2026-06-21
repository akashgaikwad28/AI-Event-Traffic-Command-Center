import React, { useEffect, useState, useRef } from 'react';
import { useCopilotStore } from '../../store/copilot.store';
import { useIncidentStore } from '../../store/incident.store';
import { BrainCircuit, Sparkles, AlertTriangle, Send } from 'lucide-react';
import { api } from '../../services/api';

export const CopilotPanel: React.FC = () => {
  const selectedId = useIncidentStore((state) => state.selectedIncidentId);
  const selectedIncident = useIncidentStore((state) => selectedId ? state.incidents[selectedId] : null);

  const { chatHistory, isGenerating, addMessage, setGenerating } = useCopilotStore();
  const [error, setError] = useState<string | null>(null);
  const [inputValue, setInputValue] = useState('');
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const currentHistory = selectedId ? (chatHistory[selectedId] || []) : [];

  useEffect(() => {
    // Scroll to bottom when messages change
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [currentHistory, isGenerating]);

  // Initial greeting if history is empty
  useEffect(() => {
    if (selectedIncident && currentHistory.length === 0 && !isGenerating) {
      addMessage(selectedIncident.incident_id, {
        role: 'assistant',
        content: `Operational Copilot activated for Incident ${selectedIncident.incident_id.split('-')[0]}. How can I assist with this operation?`
      });
    }
  }, [selectedIncident]);

  const handleSendMessage = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!selectedIncident || !inputValue.trim() || isGenerating) return;

    const userMessage = inputValue.trim();
    setInputValue('');
    setError(null);

    // Optimistically add user message
    addMessage(selectedIncident.incident_id, { role: 'user', content: userMessage });
    setGenerating(true);

    try {
      const responsePromise = api.getIncidentExplanation({
        incident_id: selectedIncident.incident_id,
        type: selectedIncident.type,
        gori_score: selectedIncident.gori_score,
        query: userMessage
      });

      const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('TIMEOUT')), 12000);
      });

      const res = await Promise.race([responsePromise, timeoutPromise]) as any;

      const aiResponse = res.explanation || "No insights available.";

      addMessage(selectedIncident.incident_id, { role: 'assistant', content: aiResponse });

    } catch (err: any) {
      console.error(err);
      if (err.message === 'TIMEOUT') {
        setError("LLM request timed out. The provider may be experiencing high latency.");
      } else {
        setError("Failed to fetch explanation due to a network or service error.");
      }
    } finally {
      setGenerating(false);
    }
  };

  return (
    <div className="h-full w-full flex flex-col relative overflow-hidden bg-dark-bg/90">
      <div className="flex flex-col z-10 px-4 py-3 border-b border-dark-border/50 bg-[#0B0F19]">
        <div className="flex items-center justify-between">
          <h3 className="font-bold text-gray-200 text-sm tracking-wide flex items-center">
            <BrainCircuit className="w-5 h-5 text-brand-accent mr-2" />
            GridWise Copilot AI
          </h3>
          {selectedIncident && (
            <span className={`text-[10px] px-2 py-0.5 rounded font-bold ${
              selectedIncident.gori_score > 70 ? 'bg-alert-emergency/20 text-alert-emergency' : 'bg-brand-primary/20 text-brand-primary'
            }`}>
              GORI {Math.round(selectedIncident.gori_score)}
            </span>
          )}
        </div>
      </div>

      <div
        ref={chatContainerRef}
        className="flex-1 overflow-y-auto p-4 custom-scrollbar z-10 flex flex-col space-y-4"
      >
        {!selectedIncident ? (
          <div className="h-full flex flex-col items-center justify-center text-center space-y-3 opacity-60 m-auto">
            <Sparkles className="w-10 h-10 text-brand-primary" />
            <p className="text-xs text-gray-400 font-medium max-w-[200px]">
              Select an incident from the map or feed to open communications.
            </p>
          </div>
        ) : (
          <>
            {currentHistory.map((msg, idx) => (
              <div key={idx} className={`flex w-full ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] rounded-lg px-3 py-2 text-xs leading-relaxed ${
                  msg.role === 'user'
                    ? 'bg-brand-primary/20 border border-brand-primary/30 text-gray-200 rounded-br-none'
                    : 'bg-dark-card border border-dark-border text-gray-300 rounded-bl-none'
                }`}>
                  <div dangerouslySetInnerHTML={{ __html: msg.content.replace(/\n/g, '<br />') }} />
                </div>
              </div>
            ))}

            {isGenerating && (
              <div className="flex justify-start w-full">
                <div className="max-w-[85%] rounded-lg px-4 py-3 bg-dark-card border border-dark-border rounded-bl-none">
                  <div className="flex items-center space-x-1.5">
                    <div className="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-1.5 h-1.5 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                </div>
              </div>
            )}

            {error && (
              <div className="flex flex-col items-center justify-center py-4 px-2 text-center">
                <AlertTriangle className="w-6 h-6 text-red-400/80 mb-2" />
                <p className="text-xs text-red-200/90 mb-3">{error}</p>
                <button
                  onClick={() => setError(null)}
                  className="text-[10px] uppercase font-bold bg-red-500/10 hover:bg-red-500/20 text-red-300 border border-red-500/20 px-4 py-2 rounded transition-colors"
                >
                  Dismiss
                </button>
              </div>
            )}
          </>
        )}
      </div>

      {/* Chat Input Area */}
      {selectedIncident && (
        <div className="p-3 bg-[#0B0F19] border-t border-dark-border/50">
          <form onSubmit={handleSendMessage} className="relative flex items-center">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Ask for operational insights..."
              disabled={isGenerating}
              className="w-full bg-dark-bg/60 border border-dark-border text-xs text-gray-200 rounded-full pl-4 pr-10 py-2.5 focus:outline-none focus:border-brand-accent/50 focus:ring-1 focus:ring-brand-accent/50 disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={!inputValue.trim() || isGenerating}
              className="absolute right-1 w-8 h-8 flex items-center justify-center rounded-full bg-brand-primary text-white hover:bg-brand-primary/80 disabled:opacity-50 disabled:hover:bg-brand-primary transition-colors"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </form>
        </div>
      )}
    </div>
  );
};
