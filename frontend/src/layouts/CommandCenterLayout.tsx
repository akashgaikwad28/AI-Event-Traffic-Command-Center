import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import { useWebSocketStore } from '../store/websocket.store';
import { useGoriStore } from '../store/gori.store';
import { useSimulationStore } from '../store/simulation.store';
import { LayoutDashboard, Map as MapIcon, Sliders, BarChart3, Wifi, WifiOff, Activity, PlaySquare, FileText } from 'lucide-react';
import { GlobalToastAlerts } from '../components/common/GlobalToastAlerts';

export const CommandCenterLayout: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const isConnected = useWebSocketStore((state) => state.isConnected);
  const avgGori = useGoriStore((state) => state.avgGori);
  const isDemoMode = useSimulationStore((state) => state.isDemoMode);
  const location = useLocation();

  const menuItems = [
    { id: '/', name: 'Live Operations Map', icon: MapIcon },
    { id: '/dashboard', name: 'Executive Dashboard', icon: LayoutDashboard },
    { id: '/planner', name: 'Operations Planner', icon: Sliders },
    { id: '/analytics', name: 'Analytics Intelligence', icon: BarChart3 },
    { id: '/simulation', name: 'Simulation Engine', icon: PlaySquare },
    { id: '/observability', name: 'System Telemetry', icon: Activity },
    { id: '/reports', name: 'Intelligence Reports', icon: FileText },
  ];

  return (
    <div className="h-screen w-screen flex flex-col bg-dark-bg text-gray-100 overflow-hidden font-sans">
      {/* Header */}
      <header className="h-16 border-b border-dark-border bg-dark-card flex items-center justify-between px-6 z-20">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 rounded-lg bg-brand-primary flex items-center justify-center font-bold text-white shadow-md shadow-brand-primary/20">
            GW
          </div>
          <div>
            <h1 className="text-md font-bold tracking-wider text-gray-100 flex items-center">
              GRIDWISE AI <span className="text-xs text-brand-accent ml-2 border border-brand-accent/30 bg-brand-accent/10 px-1.5 py-0.5 rounded font-semibold">V2.0</span>
            </h1>
            <p className="text-xxs text-gray-500 uppercase font-semibold tracking-widest leading-none">Traffic Operations Command Center</p>
          </div>
        </div>

        {/* Real-time System Metrics */}
        <div className="flex items-center space-x-4 text-sm">
          {/* AI Status */}
          <div className="hidden md:flex items-center space-x-1.5 bg-dark-bg/60 border border-dark-border px-2.5 py-1 rounded-full">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-primary"></span>
            </span>
            <span className="text-[10px] text-gray-300 font-bold uppercase tracking-wider">AI Copilot</span>
          </div>

          {isDemoMode && (
            <div className="hidden lg:flex items-center space-x-1.5 bg-brand-accent/10 border border-brand-accent/30 px-2.5 py-1 rounded-full">
              <PlaySquare className="w-3 h-3 text-brand-accent animate-pulse" />
              <span className="text-[10px] text-brand-accent font-bold uppercase tracking-wider">Sim Active</span>
            </div>
          )}

          <div className="flex items-center space-x-2 bg-dark-bg/60 border border-dark-border px-3 py-1 rounded-full">
            <span className="text-[10px] text-gray-400 font-bold uppercase tracking-wider">Avg GORI</span>
            <span className={`text-xs font-black ${
              avgGori > 75 ? 'text-red-400 animate-pulse' : avgGori > 45 ? 'text-amber-400' : 'text-emerald-400'
            }`}>{avgGori}%</span>
          </div>

          {/* WebSocket Status */}
          <div className="flex items-center space-x-2">
            {isConnected ? (
              <div className="flex items-center space-x-1.5 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-full text-emerald-400">
                <Wifi className="w-3 h-3" />
                <span className="text-[10px] font-bold uppercase tracking-wider">Stream Active</span>
              </div>
            ) : (
              <div className="flex items-center space-x-1.5 bg-red-500/10 border border-red-500/20 px-3 py-1 rounded-full text-red-500 animate-pulse">
                <WifiOff className="w-3 h-3" />
                <span className="text-[10px] font-bold uppercase tracking-wider">Stream Offline</span>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Container */}
      <div className="flex flex-1 overflow-hidden">
        {/* Sidebar */}
        <aside className="w-64 border-r border-dark-border bg-dark-card flex flex-col justify-between py-6 z-10 shrink-0">
          <nav className="space-y-1 px-3">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.id || (item.id !== '/' && location.pathname.startsWith(item.id));
              return (
                <Link
                  key={item.id}
                  to={item.id}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-sm font-semibold transition-all duration-200 group relative ${
                    isActive
                      ? 'bg-brand-primary text-white shadow-lg shadow-brand-primary/10'
                      : 'text-gray-400 hover:bg-dark-bg hover:text-gray-200'
                  }`}
                >
                  <Icon className={`w-5 h-5 transition-transform duration-200 group-hover:scale-105 ${
                    isActive ? 'text-white' : 'text-gray-400 group-hover:text-gray-200'
                  }`} />
                  <span>{item.name}</span>
                  {isActive && (
                    <span className="absolute right-3 w-1.5 h-1.5 rounded-full bg-white animate-ping"></span>
                  )}
                </Link>
              );
            })}
          </nav>

          {/* Footer Info */}
          <div className="px-6 border-t border-dark-border/60 pt-4 text-xxs text-gray-500 space-y-1">
            <p className="font-semibold uppercase tracking-wider">COMMAND CENTER SECURE SHELL</p>
            <p>LATENCY: &lt;10ms (Local loop)</p>
            <p>HOST: ws://localhost:8000</p>
          </div>
        </aside>

        {/* Main Content Area */}
        <main className="flex-1 relative bg-dark-bg/50 overflow-hidden">
          {children}
        </main>

        {/* Global Modals / Overlays */}
        <GlobalToastAlerts />
      </div>
    </div>
  );
};
