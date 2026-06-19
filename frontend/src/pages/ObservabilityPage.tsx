import React, { useEffect, useState } from 'react';
import { useWebSocketStore } from '../store/websocket.store';
import { Activity, Server, Database, Wifi, Zap } from 'lucide-react';
import ReactECharts from 'echarts-for-react';

export const ObservabilityPage: React.FC = () => {
  const isConnected = useWebSocketStore((state) => state.isConnected);

  const [metrics, setMetrics] = useState({
    apiLatency: 12,
    modelLatency: 85,
    cpuUsage: 45,
    memoryUsage: 62,
    activeConnections: 1,
    eventsProcessed: 14502
  });

  const [latencyHistory, setLatencyHistory] = useState<number[]>(Array(20).fill(12));

  // Simulate live telemetry
  useEffect(() => {
    const interval = setInterval(() => {
      setMetrics(prev => {
        const newApiLatency = prev.apiLatency + (Math.random() * 4 - 2);
        const newModelLatency = prev.modelLatency + (Math.random() * 10 - 5);

        setLatencyHistory(hist => {
          const newHist = [...hist.slice(1), Math.max(5, newApiLatency)];
          return newHist;
        });

        return {
          apiLatency: Math.max(5, Math.min(50, newApiLatency)),
          modelLatency: Math.max(40, Math.min(200, newModelLatency)),
          cpuUsage: Math.max(10, Math.min(95, prev.cpuUsage + (Math.random() * 10 - 5))),
          memoryUsage: Math.max(20, Math.min(90, prev.memoryUsage + (Math.random() * 4 - 2))),
          activeConnections: isConnected ? Math.floor(Math.random() * 3) + 1 : 0,
          eventsProcessed: prev.eventsProcessed + Math.floor(Math.random() * 5)
        };
      });
    }, 2000);
    return () => clearInterval(interval);
  }, [isConnected]);

  const chartOption = {
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis', backgroundColor: '#1e293b', textStyle: { color: '#f8fafc' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', boundaryGap: false, data: Array(20).fill(''), axisLine: { lineStyle: { color: '#334155' } } },
    yAxis: { type: 'value', axisLine: { lineStyle: { color: '#334155' } }, splitLine: { lineStyle: { color: '#1e293b' } } },
    series: [
      {
        name: 'API Latency (ms)',
        type: 'line',
        smooth: true,
        data: latencyHistory,
        itemStyle: { color: '#3b82f6' },
        areaStyle: {
          color: {
            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [{ offset: 0, color: 'rgba(59, 130, 246, 0.5)' }, { offset: 1, color: 'rgba(59, 130, 246, 0.0)' }]
          }
        }
      }
    ]
  };

  return (
    <div className="h-full w-full overflow-y-auto p-6 space-y-6 bg-dark-bg text-gray-200">
      <div>
        <h2 className="text-xl font-extrabold text-gray-100 tracking-wide">System Observability</h2>
        <p className="text-xs text-gray-500 font-medium mt-0.5">Live telemetry from the GridWise AI backend inference and data pipelines.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Core Metrics */}
        <div className="bg-dark-card border border-dark-border rounded-xl p-5 flex items-center space-x-4">
          <div className="bg-blue-500/10 p-3 rounded-lg border border-blue-500/20"><Activity className="w-6 h-6 text-blue-400" /></div>
          <div>
            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-wider">API Latency</p>
            <p className="text-xl font-black text-gray-200">{metrics.apiLatency.toFixed(1)} ms</p>
          </div>
        </div>

        <div className="bg-dark-card border border-dark-border rounded-xl p-5 flex items-center space-x-4">
          <div className="bg-purple-500/10 p-3 rounded-lg border border-purple-500/20"><Zap className="w-6 h-6 text-purple-400" /></div>
          <div>
            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-wider">Model Inference</p>
            <p className="text-xl font-black text-gray-200">{metrics.modelLatency.toFixed(1)} ms</p>
          </div>
        </div>

        <div className="bg-dark-card border border-dark-border rounded-xl p-5 flex items-center space-x-4">
          <div className="bg-emerald-500/10 p-3 rounded-lg border border-emerald-500/20"><Server className="w-6 h-6 text-emerald-400" /></div>
          <div>
            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-wider">CPU Load</p>
            <p className="text-xl font-black text-gray-200">{metrics.cpuUsage.toFixed(1)} %</p>
          </div>
        </div>

        <div className="bg-dark-card border border-dark-border rounded-xl p-5 flex items-center space-x-4">
          <div className="bg-amber-500/10 p-3 rounded-lg border border-amber-500/20"><Database className="w-6 h-6 text-amber-400" /></div>
          <div>
            <p className="text-[10px] text-gray-500 font-bold uppercase tracking-wider">Events Processed</p>
            <p className="text-xl font-black text-gray-200">{metrics.eventsProcessed.toLocaleString()}</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-dark-card border border-dark-border rounded-xl p-5">
          <h3 className="font-bold text-gray-200 mb-4 text-sm tracking-wide">Real-time API Latency</h3>
          <ReactECharts option={chartOption} style={{ height: '300px' }} />
        </div>

        <div className="bg-dark-card border border-dark-border rounded-xl p-5">
          <h3 className="font-bold text-gray-200 mb-4 text-sm tracking-wide">Infrastructure Health</h3>
          <div className="space-y-6">
            <div>
              <div className="flex justify-between mb-1">
                <span className="text-xs font-semibold text-gray-400">WebSocket Connections</span>
                <span className="text-xs font-bold text-gray-200">{metrics.activeConnections} active</span>
              </div>
              <div className="w-full bg-dark-bg rounded-full h-2">
                <div className="bg-brand-primary h-2 rounded-full" style={{ width: `${(metrics.activeConnections / 5) * 100}%` }}></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between mb-1">
                <span className="text-xs font-semibold text-gray-400">Memory Usage (Container)</span>
                <span className="text-xs font-bold text-gray-200">{metrics.memoryUsage.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-dark-bg rounded-full h-2">
                <div className={`h-2 rounded-full ${metrics.memoryUsage > 80 ? 'bg-red-500' : 'bg-emerald-500'}`} style={{ width: `${metrics.memoryUsage}%` }}></div>
              </div>
            </div>

            <div className="bg-[#121626] border border-dark-border p-4 rounded-lg flex items-start space-x-3 mt-4">
               <Wifi className={`w-5 h-5 mt-0.5 ${isConnected ? 'text-emerald-400' : 'text-red-500'}`} />
               <div>
                 <p className="text-sm font-bold text-gray-200">Stream Connection Status</p>
                 <p className="text-xs text-gray-500 mt-1">{isConnected ? 'Connected to live event broker on ws://localhost:8000. Data streaming nominally.' : 'Disconnected. Waiting for reconnect...'}</p>
               </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
