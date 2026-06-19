import { useWebSocketStore } from '../store/websocket.store';
import { useIncidentStore } from '../store/incident.store';
import { useAnalyticsStore } from '../store/analytics.store';
import { useGoriStore } from '../store/gori.store';

class WebSocketService {
  private sockets: Record<string, WebSocket> = {};
  private reconnectAttempts: Record<string, number> = {};
  private maxReconnectAttempts = 5;
  private baseReconnectInterval = 1000; // 1 second base
  private topics = ['live_events', 'gori_alerts'];
  private pingIntervals: Record<string, number> = {};

  connect() {
    this.topics.forEach((topic) => {
      this.reconnectAttempts[topic] = 0;
      this.connectToTopic(topic);
    });
  }

  private connectToTopic(topic: string) {
    if (
      this.sockets[topic]?.readyState === WebSocket.OPEN ||
      this.sockets[topic]?.readyState === WebSocket.CONNECTING
    ) {
      return;
    }

    const url = `ws://localhost:8000/api/v1/stream/ws/${topic}`;
    console.log(`Connecting to ${topic} WebSocket: ${url}`);

    const socket = new WebSocket(url);

    socket.onopen = () => {
      console.log(`Connected to WebSocket topic: ${topic}`);
      this.reconnectAttempts[topic] = 0; // reset
      this.updateConnectionStatus();

      // Start heartbeat
      this.pingIntervals[topic] = window.setInterval(() => {
        if (socket.readyState === WebSocket.OPEN) {
          socket.send(JSON.stringify({ type: 'ping' }));
        }
      }, 30000); // 30s ping
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        if (data.type === 'pong') return; // ignore heartbeat responses
        this.handleMessage(topic, data);
      } catch (err) {
        console.error(`Error parsing message on topic ${topic}:`, err);
      }
    };

    socket.onclose = () => {
      this.cleanupSocket(topic);
      this.updateConnectionStatus();

      const attempts = this.reconnectAttempts[topic];
      if (attempts < this.maxReconnectAttempts) {
        const delay = Math.min(10000, this.baseReconnectInterval * Math.pow(2, attempts));
        console.warn(`WebSocket topic ${topic} closed. Reconnecting in ${delay}ms...`);
        this.reconnectAttempts[topic]++;
        setTimeout(() => this.connectToTopic(topic), delay);
      } else {
        console.error(`WebSocket topic ${topic} failed after ${attempts} reconnects.`);
      }
    };

    socket.onerror = (error) => {
      console.error(`WebSocket topic ${topic} error:`, error);
    };

    this.sockets[topic] = socket;
  }

  private handleMessage(topic: string, data: any) {
    if (topic === 'live_events') {
      if (data.event_type === 'INCIDENT_UPDATE' || data.event_type === 'INCIDENT_CREATED') {
        const incidentStore = useIncidentStore.getState();
        incidentStore.addIncident(data.payload);

        // Also update GORI since incidents changed
        useGoriStore.getState().updateGoriFromIncidents(incidentStore.incidents);
      }
    } else if (topic === 'gori_alerts') {
      useAnalyticsStore.getState().addAlert(data);
    }
  }

  private cleanupSocket(topic: string) {
    if (this.pingIntervals[topic]) {
      window.clearInterval(this.pingIntervals[topic]);
      delete this.pingIntervals[topic];
    }
  }

  private updateConnectionStatus() {
    const anyConnected = Object.values(this.sockets).some(
      (socket) => socket?.readyState === WebSocket.OPEN
    );
    useWebSocketStore.getState().setConnectionStatus(anyConnected);
  }

  disconnect() {
    Object.keys(this.sockets).forEach((topic) => {
      this.cleanupSocket(topic);
      const socket = this.sockets[topic];
      if (socket) {
        socket.close();
      }
    });
    this.sockets = {};
    useWebSocketStore.getState().setConnectionStatus(false);
  }
}

export const wsService = new WebSocketService();
