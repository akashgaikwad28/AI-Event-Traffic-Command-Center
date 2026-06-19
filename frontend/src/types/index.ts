export interface LiveAlert {
  alert_id: string;
  severity: 'INFO' | 'WARNING' | 'HIGH' | 'CRITICAL';
  color_code: string;
  message: string;
  recommendation?: string;
  timestamp: string;
}

export interface Incident {
  incident_id: string;
  type: string;
  gori_score: number;
  latitude: number;
  longitude: number;
  is_rush_hour: boolean;
  heavy_vehicle: boolean;
  deployment_recommendation?: string;
}

export interface DashboardSnapshot {
  active_incidents: number;
  top_hotspots: any[];
  avg_gori: number;
  deployment_pressure: string;
  critical_alerts: LiveAlert[];
}
