import { useEffect } from 'react';
import { CommandCenterLayout } from './layouts/CommandCenterLayout';
import { DashboardPage } from './pages/DashboardPage';
import { LiveOperationsPage } from './pages/LiveOperationsPage';
import { OperationsPlannerPage } from './pages/OperationsPlannerPage';
import { AnalyticsPage } from './pages/AnalyticsPage';
import { SimulationPage } from './pages/SimulationPage';
import { ObservabilityPage } from './pages/ObservabilityPage';
import { ReportsPage } from './pages/ReportsPage';
import { wsService } from './services/websocket.service';
import { useGoriStore } from './store/gori.store';
import { useAnalyticsStore } from './store/analytics.store';
import { api } from './services/api';

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

function App() {
  const setAvgGori = useGoriStore((state) => state.setAvgGori);
  const addAlert = useAnalyticsStore((state) => state.addAlert);

  useEffect(() => {
    wsService.connect();

    const fetchSnapshot = async () => {
      try {
        const data = await api.getLiveSnapshot();
        setAvgGori(Math.round(data.avg_gori || 0));
        if (data.critical_alerts) {
          data.critical_alerts.forEach((alert: any) => addAlert(alert));
        }
      } catch (err) {
        console.error('Failed to bootstrap from snapshot:', err);
      }
    };

    fetchSnapshot();

    return () => {
      wsService.disconnect();
    };
  }, [setAvgGori, addAlert]);

  return (
    <BrowserRouter>
      <CommandCenterLayout>
        <Routes>
          <Route path="/" element={<LiveOperationsPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/planner" element={<OperationsPlannerPage />} />
          <Route path="/analytics" element={<AnalyticsPage />} />
          <Route path="/simulation" element={<SimulationPage />} />
          <Route path="/observability" element={<ObservabilityPage />} />
          <Route path="/reports" element={<ReportsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </CommandCenterLayout>
    </BrowserRouter>
  );
}

export default App;
