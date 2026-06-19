import { create } from 'zustand';

interface WebSocketState {
  isConnected: boolean;
  isConnecting: boolean;
  setConnectionStatus: (status: boolean) => void;
  setConnecting: (status: boolean) => void;
}

export const useWebSocketStore = create<WebSocketState>((set) => ({
  isConnected: false,
  isConnecting: true,
  setConnectionStatus: (status) => set({ isConnected: status, isConnecting: false }),
  setConnecting: (status) => set({ isConnecting: status })
}));
