import { create } from 'zustand';

interface GoriState {
  avgGori: number;
  setAvgGori: (score: number) => void;
  updateGoriFromIncidents: (incidents: Record<string, any>) => void;
}

export const useGoriStore = create<GoriState>((set) => ({
  avgGori: 0,
  setAvgGori: (score) => set({ avgGori: score }),
  updateGoriFromIncidents: (incidents) => {
    const values = Object.values(incidents);
    const avg = values.length 
      ? Math.round(values.reduce((sum, i) => sum + i.gori_score, 0) / values.length) 
      : 0;
    set({ avgGori: avg });
  }
}));
