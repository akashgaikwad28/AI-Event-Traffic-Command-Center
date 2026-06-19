import { create } from 'zustand';
import { OperationalPlan } from '../services/api';

interface SimulationState {
  operationalPlans: Record<string, OperationalPlan>;
  loadingPlans: Record<string, boolean>;
  isDemoMode: boolean;
  setOperationalPlan: (incidentId: string, plan: OperationalPlan) => void;
  setLoadingPlan: (incidentId: string, isLoading: boolean) => void;
  toggleDemoMode: () => void;
  clearSimulation: () => void;
}

export const useSimulationStore = create<SimulationState>((set) => ({
  operationalPlans: {},
  loadingPlans: {},
  isDemoMode: false,
  setOperationalPlan: (incidentId, plan) => set((state) => ({
    operationalPlans: { ...state.operationalPlans, [incidentId]: plan }
  })),
  setLoadingPlan: (incidentId, isLoading) => set((state) => ({
    loadingPlans: { ...state.loadingPlans, [incidentId]: isLoading }
  })),
  toggleDemoMode: () => set((state) => ({ isDemoMode: !state.isDemoMode })),
  clearSimulation: () => set({ operationalPlans: {}, loadingPlans: {} })
}));
