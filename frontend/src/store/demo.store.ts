import { create } from 'zustand';
import { api } from '../services/api';
import { SimulationScenario } from '../constants/scenarios';

export interface MapEntity {
  id: string;
  type: string;
  lat: number;
  lng: number;
  radius?: number;
  metadata?: any;
}

export interface TimelineFrame {
  time_offset_mins: number;
  gori_score: number;
  active_incidents: number;
  congestion_radius: number;
  map_entities: MapEntity[];
  cascading_risk: string;
}

export interface SimulationStateData {
  timeline_frames: TimelineFrame[];
  final_gori: number;
  estimated_clearance_mins: number;
  total_congestion_radius: number;
  cascading_risk_level: string;
}

export interface VisualSimulationResult {
  scenario_id: string;
  scenario_type: string;
  baseline_state: SimulationStateData;
  optimized_state: SimulationStateData;
  improvements: {
    response_time_reduction_mins: number;
    congestion_reduction_pct: number;
    gori_reduction: number;
    spread_reduction_radius: number;
    officer_efficiency_gain_pct: number;
    diversion_effectiveness_score: number;
    estimated_citizens_impacted: number;
  };
  confidence: number;
  recommendations: any[];
}

interface DemoState {
  activeScenario: string | null;
  isRunning: boolean;

  // Phase 12 Visual Simulation
  simulationResult: VisualSimulationResult | null;
  simulationHistory: VisualSimulationResult[];
  playbackFrameIndex: number;
  playbackSpeed: number; // 1, 2, 5, 10
  playbackState: 'PLAYING' | 'PAUSED' | 'STOPPED';

  startScenario: (uiId: string, simType: SimulationScenario, payload?: any) => Promise<void>;
  stopScenario: () => void;

  runVisualDemo: () => Promise<void>;
  runVisualSimulation: (type: string, params?: any) => Promise<void>;
  setPlaybackState: (state: 'PLAYING' | 'PAUSED' | 'STOPPED') => void;
  setPlaybackSpeed: (speed: number) => void;
  setPlaybackFrame: (frame: number) => void;
  loadHistory: () => Promise<void>;
}

export const useDemoStore = create<DemoState>((set, get) => ({
  activeScenario: null,
  isRunning: false,

  simulationResult: null,
  simulationHistory: [],
  playbackFrameIndex: 0,
  playbackSpeed: 1,
  playbackState: 'STOPPED',

  startScenario: async (uiId: string, simType: SimulationScenario, payload?: any) => {
    set({ isRunning: true, activeScenario: uiId });
    try {
      await api.triggerSimulation(simType, payload);
    } catch (err) {
      set({ isRunning: false, activeScenario: null });
    }
  },

  stopScenario: () => {
    set({ isRunning: false, activeScenario: null });
  },

  runVisualDemo: async () => {
    set({ isRunning: true });
    try {
      const result = await api.runExecutiveDemo();
      set({
        simulationResult: result,
        playbackState: 'PLAYING',
        playbackFrameIndex: 0,
        isRunning: true
      });
      get().loadHistory();
    } catch (e) {
      console.error(e);
      set({ isRunning: false });
    }
  },

  runVisualSimulation: async (type, params = {}) => {
    set({ isRunning: true });
    try {
      const result = await api.runVisualSimulation(type, params);
      set({
        simulationResult: result,
        playbackState: 'PLAYING',
        playbackFrameIndex: 0,
        isRunning: true
      });
      get().loadHistory();
    } catch (e) {
      console.error(e);
      set({ isRunning: false });
    }
  },

  setPlaybackState: (state) => set({ playbackState: state }),
  setPlaybackSpeed: (speed) => set({ playbackSpeed: speed }),
  setPlaybackFrame: (frame) => set({ playbackFrameIndex: frame }),

  loadHistory: async () => {
    try {
      const history = await api.getSimulationHistory();
      set({ simulationHistory: history });
    } catch (e) {
      console.error(e);
    }
  }
}));
