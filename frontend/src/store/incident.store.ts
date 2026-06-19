import { create } from 'zustand';
import { Incident } from '../types';

interface IncidentState {
  incidents: Record<string, Incident>;
  selectedIncidentId: string | null;
  addIncident: (incident: Incident) => void;
  setSelectedIncidentId: (id: string | null) => void;
  clearIncidents: () => void;
}

export const useIncidentStore = create<IncidentState>((set) => ({
  incidents: {},
  selectedIncidentId: null,
  addIncident: (incident) => set((state) => ({
    incidents: { ...state.incidents, [incident.incident_id]: incident }
  })),
  setSelectedIncidentId: (id) => set({ selectedIncidentId: id }),
  clearIncidents: () => set({ incidents: {}, selectedIncidentId: null })
}));
