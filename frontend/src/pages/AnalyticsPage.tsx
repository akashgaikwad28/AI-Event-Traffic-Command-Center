import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';
import { api } from '../services/api';
import { TrendingUp, Clock, AlertTriangle } from 'lucide-react';

export const AnalyticsPage: React.FC = () => {
  const [metrics, setMetrics] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        setError(false);
        const response = await api.getAnalyticsOverview();
        if (response.success && response.data) {
          setMetrics(response.data);
        }
      } catch (err) {
        console.error('Failed to fetch metrics', err);
        setError(true);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
    const int = setInterval(fetchMetrics, 30000);
    return () => clearInterval(int);
  }, []);

  const getAreaChartOption = () => {
    // Dynamically map backend trend data if available, fallback to empty
    const trendData = metrics?.trends?.historical_gori || [];
    const timestamps = trendData.length > 0 ? trendData.map((_: any, i: number) => `-${(trendData.length - i)}h`) : ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'];
    const values = trendData.length > 0 ? trendData : [0, 0, 0, 0, 0, 0];

    return {
      tooltip: { trigger: 'axis' },
      xAxis: { type: 'category', data: timestamps },
      yAxis: { type: 'value', min: 0, max: 100 },
      series: [
        { data: values, type: 'line', areaStyle: {}, color: '#ef4444', smooth: true },
      ]
    };
  };

  if (loading && !metrics) {
    return (
      <div className="h-full w-full flex items-center justify-center bg-dark-bg text-gray-500 flex-col space-y-4">
        <div className="w-8 h-8 border-4 border-brand-primary border-t-transparent rounded-full animate-spin"></div>
        <p className="text-xs uppercase tracking-widest font-bold">Aggregating Global Telemetry...</p>
      </div>
    );
  }

  if (error && !metrics) {
    return (
      <div className="h-full w-full flex items-center justify-center bg-dark-bg text-red-500 flex-col space-y-4">
        <AlertTriangle className="w-10 h-10" />
        <p className="text-xs uppercase tracking-widest font-bold">Telemetry Connection Lost. Retrying...</p>
      </div>
    );
  }

  const healthScore = metrics?.city_health?.health_score || 0;
  const p50Clearance = metrics?.response_efficiency?.p50_clearance_mins || 0;
  const criticalIncidents = metrics?.city_health?.active_incidents || 0;

  return (
    <div className="h-full w-full overflow-y-auto p-6 space-y-6 bg-dark-bg text-gray-200">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-wider text-white">System Analytics</h2>
          <p className="text-sm text-gray-400">Historical performance & network resilience</p>
        </div>
        <div className="flex items-center space-x-2 text-xs text-gray-500 font-bold uppercase tracking-wider">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>Live Telemetry</span>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-dark-card border border-dark-border p-4 rounded-xl flex items-center space-x-4 shadow-lg relative overflow-hidden">
          <div className="absolute top-0 right-0 p-3 opacity-5"><TrendingUp className="w-16 h-16 text-emerald-400" /></div>
          <div className="p-3 bg-emerald-500/10 rounded-lg shrink-0">
            <TrendingUp className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <p className="text-[10px] uppercase font-bold text-gray-500 tracking-wider">City Health Score</p>
            <h3 className="text-2xl font-black text-gray-100">{Math.round(healthScore)}%</h3>
          </div>
        </div>
        
        <div className="bg-dark-card border border-dark-border p-4 rounded-xl flex items-center space-x-4 shadow-lg relative overflow-hidden">
          <div className="absolute top-0 right-0 p-3 opacity-5"><Clock className="w-16 h-16 text-blue-400" /></div>
          <div className="p-3 bg-blue-500/10 rounded-lg shrink-0">
            <Clock className="w-6 h-6 text-blue-400" />
          </div>
          <div>
            <p className="text-[10px] uppercase font-bold text-gray-500 tracking-wider">P50 Clearance SLA</p>
            <h3 className="text-2xl font-black text-gray-100">{Math.round(p50Clearance)}m</h3>
          </div>
        </div>
        
        <div className="bg-dark-card border border-dark-border p-4 rounded-xl flex items-center space-x-4 shadow-lg relative overflow-hidden">
          <div className="absolute top-0 right-0 p-3 opacity-5"><AlertTriangle className="w-16 h-16 text-red-400" /></div>
          <div className="p-3 bg-red-500/10 rounded-lg shrink-0">
            <AlertTriangle className="w-6 h-6 text-red-400" />
          </div>
          <div>
            <p className="text-[10px] uppercase font-bold text-gray-500 tracking-wider">Active Incidents</p>
            <h3 className="text-2xl font-black text-gray-100">{criticalIncidents}</h3>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-dark-card border border-dark-border rounded-xl p-5 shadow-lg">
          <h3 className="text-xs font-bold uppercase tracking-wider text-gray-400 mb-4">GORI Volatility Trend (Last 24h)</h3>
          <div className="h-64">
            <ReactECharts option={getAreaChartOption()} style={{ height: '100%', width: '100%' }} />
          </div>
        </div>
      </div>
    </div>
  );
};
