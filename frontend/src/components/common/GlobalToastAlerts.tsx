import React, { useEffect, useState } from 'react';
import { useAnalyticsStore } from '../../store/analytics.store';
import { AlertTriangle, Bell, Info, ShieldAlert, X } from 'lucide-react';
import { LiveAlert } from '../../types';

interface ToastProps {
  alert: LiveAlert;
  onDismiss: () => void;
}

const Toast: React.FC<ToastProps> = ({ alert, onDismiss }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onDismiss();
    }, 5000);
    return () => clearTimeout(timer);
  }, [onDismiss]);

  const getStyle = () => {
    switch (alert.severity) {
      case 'CRITICAL':
        return 'bg-red-950/90 border-red-500 text-red-100 shadow-[0_0_15px_rgba(239,68,68,0.5)] animate-pulse';
      case 'HIGH':
        return 'bg-orange-950/90 border-orange-500 text-orange-100';
      case 'WARNING':
        return 'bg-amber-950/90 border-amber-500 text-amber-100';
      default:
        return 'bg-blue-950/90 border-blue-500 text-blue-100';
    }
  };

  const getIcon = () => {
    switch (alert.severity) {
      case 'CRITICAL': return <ShieldAlert className="w-5 h-5 text-red-400" />;
      case 'HIGH': return <AlertTriangle className="w-5 h-5 text-orange-400" />;
      case 'WARNING': return <Bell className="w-5 h-5 text-amber-400" />;
      default: return <Info className="w-5 h-5 text-blue-400" />;
    }
  };

  return (
    <div className={`pointer-events-auto flex w-full max-w-sm overflow-hidden rounded-lg border shadow-lg ring-1 ring-black ring-opacity-5 transition-all transform ease-out duration-300 translate-y-0 opacity-100 sm:translate-x-0 ${getStyle()}`}>
      <div className="p-4 w-full">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            {getIcon()}
          </div>
          <div className="ml-3 w-0 flex-1 pt-0.5">
            <p className="text-sm font-bold uppercase tracking-wide">
              SYSTEM ALERT
            </p>
            <p className="mt-1 text-xs font-medium opacity-90">
              {alert.message}
            </p>
          </div>
          <div className="ml-4 flex flex-shrink-0">
            <button
              type="button"
              className="inline-flex rounded-md bg-transparent text-gray-400 hover:text-white focus:outline-none"
              onClick={onDismiss}
            >
              <span className="sr-only">Close</span>
              <X className="h-4 w-4" aria-hidden="true" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export const GlobalToastAlerts: React.FC = () => {
  const alerts = useAnalyticsStore((state) => state.alerts);
  const [activeToasts, setActiveToasts] = useState<LiveAlert[]>([]);

  // Track latest alert
  useEffect(() => {
    if (alerts.length > 0) {
      const latest = alerts[0];
      // Simple heuristic: if it's within the last 5 seconds, show it
      const now = new Date().getTime();
      const alertTime = new Date(latest.timestamp).getTime();
      
      if (now - alertTime < 5000) {
        // Prevent duplicates
        setActiveToasts(current => {
          if (current.find(t => t.alert_id === latest.alert_id)) return current;
          return [latest, ...current].slice(0, 3); // Max 3 toasts
        });
      }
    }
  }, [alerts]);

  const dismissToast = (id: string) => {
    setActiveToasts(current => current.filter(t => t.alert_id !== id));
  };

  if (activeToasts.length === 0) return null;

  return (
    <div
      aria-live="assertive"
      className="pointer-events-none fixed inset-0 flex items-end px-4 py-6 sm:items-start sm:p-6 z-[100]"
    >
      <div className="flex w-full flex-col items-center space-y-4 sm:items-end mt-16">
        {activeToasts.map((toast) => (
          <Toast key={toast.alert_id} alert={toast} onDismiss={() => dismissToast(toast.alert_id)} />
        ))}
      </div>
    </div>
  );
};
