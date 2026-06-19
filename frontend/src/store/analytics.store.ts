import { create } from 'zustand';
import { LiveAlert } from '../types';

interface AnalyticsState {
  alerts: LiveAlert[];
  addAlert: (alert: LiveAlert) => void;
  clearAlerts: () => void;
}

export const useAnalyticsStore = create<AnalyticsState>((set) => ({
  alerts: [],
  addAlert: (alert) => set((state) => ({ 
    alerts: [alert, ...state.alerts].slice(0, 50) 
  })),
  clearAlerts: () => set({ alerts: [] })
}));
