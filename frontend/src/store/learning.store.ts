import { create } from 'zustand';
import type { LearningState } from '../types/learning';

interface LearningStoreState {
  state: LearningState | null;
  loading: boolean;
  error: boolean;

  fetchInsights: () => Promise<void>;
  resolveIncident: (incidentId: string, actualClearanceMins: number) => Promise<void>;
}

export const useLearningStore = create<LearningStoreState>((set, get) => ({
  state: null,
  loading: false,
  error: false,

  fetchInsights: async () => {
    set({ loading: true, error: false });
    try {
      const base = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
      const res = await fetch(`${base}/learning/insights`);
      if (!res.ok) throw new Error('Failed to fetch learning insights');
      const data: LearningState = await res.json();
      set({ state: data, loading: false });
    } catch {
      set({ loading: false, error: true });
    }
  },

  resolveIncident: async (incidentId: string, actualClearanceMins: number) => {
    try {
      const base = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
      const res = await fetch(`${base}/learning/resolve-incident/${incidentId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ actual_clearance_mins: actualClearanceMins }),
      });
      if (!res.ok) throw new Error('Failed to resolve incident');
      // Refresh insights after resolution
      await get().fetchInsights();
    } catch (err) {
      console.error('resolveIncident error', err);
    }
  },
}));
