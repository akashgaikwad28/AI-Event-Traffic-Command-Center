import { create } from 'zustand';

interface CopilotState {
  executiveSummary: string | null;
  explanations: Record<string, string>;
  isGenerating: boolean;
  setExecutiveSummary: (summary: string) => void;
  setExplanation: (incidentId: string, explanation: string) => void;
  setGenerating: (status: boolean) => void;
  clearCopilot: () => void;
}

export const useCopilotStore = create<CopilotState>((set) => ({
  executiveSummary: null,
  explanations: {},
  isGenerating: false,
  setExecutiveSummary: (summary) => set({ executiveSummary: summary }),
  setExplanation: (incidentId, explanation) => set((state) => ({
    explanations: { ...state.explanations, [incidentId]: explanation }
  })),
  setGenerating: (status) => set({ isGenerating: status }),
  clearCopilot: () => set({ executiveSummary: null, explanations: {} })
}));
