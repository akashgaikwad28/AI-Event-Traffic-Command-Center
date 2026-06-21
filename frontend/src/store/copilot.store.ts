import { create } from 'zustand';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

interface CopilotState {
  chatHistory: Record<string, ChatMessage[]>;
  isGenerating: boolean;
  addMessage: (incidentId: string, message: ChatMessage) => void;
  setGenerating: (status: boolean) => void;
  clearHistory: (incidentId: string) => void;
}

export const useCopilotStore = create<CopilotState>((set) => ({
  chatHistory: {},
  isGenerating: false,
  addMessage: (incidentId, message) => set((state) => {
    const existing = state.chatHistory[incidentId] || [];
    return { chatHistory: { ...state.chatHistory, [incidentId]: [...existing, message] } };
  }),
  setGenerating: (status) => set({ isGenerating: status }),
  clearHistory: (incidentId) => set((state) => ({
    chatHistory: { ...state.chatHistory, [incidentId]: [] }
  }))
}));
