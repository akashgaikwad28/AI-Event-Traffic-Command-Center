import React from 'react';
import { useAnalyticsStore } from '../../store/analytics.store';
import { ShieldAlert, Bell, Flame } from 'lucide-react';

export const AlertFeed: React.FC = () => {
  const alerts = useAnalyticsStore((state) => state.alerts);

  return (
    <div className="bg-dark-card border border-dark-border rounded-xl flex flex-col h-full overflow-hidden shadow-lg">
      <div className="p-4 border-b border-dark-border flex items-center justify-between shrink-0 bg-dark-bg/25">
        <div>
          <h3 className="font-bold text-gray-200 text-sm tracking-wide flex items-center">
            <Bell className="w-4 h-4 text-alert-warning mr-1.5 animate-pulse" />
            Critical Operations Center Alerts
          </h3>
          <p className="text-xxs text-gray-500 font-medium mt-0.5">High-frequency risk alerts & system dispatches.</p>
        </div>
        <span className="text-xxs px-2 py-0.5 rounded-full bg-alert-high/15 border border-alert-high/20 text-alert-high font-bold">
          {alerts.length} Critical
        </span>
      </div>

      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {alerts.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center p-4 text-gray-655 italic space-y-1.5">
            <Flame className="w-7 h-7 text-gray-600" />
            <p className="text-xs text-gray-500">No critical threat alerts detected.</p>
            <p className="text-xxs text-gray-600 font-medium">All corridors operating within safe GORI thresholds.</p>
          </div>
        ) : (
          alerts.map((alert, idx) => (
            <div
              key={alert.alert_id || idx}
              className="border border-red-500/20 bg-red-500/5 rounded-lg p-3 relative overflow-hidden"
            >
              {/* Glowing vertical bar */}
              <div className="absolute top-0 bottom-0 left-0 w-1 bg-red-650 animate-pulse"></div>

              <div className="flex items-start justify-between">
                <div className="flex items-center space-x-2">
                  <span className="text-[10px] font-bold text-alert-high bg-alert-high/10 border border-alert-high/25 px-1.5 py-0.2 rounded">
                    {alert.severity}
                  </span>
                  <span className="text-[10px] text-gray-500 font-bold">{alert.alert_id}</span>
                </div>
                <span className="text-[9px] text-gray-500">Just Now</span>
              </div>

              <p className="text-xs text-gray-200 font-semibold mt-1.5 leading-snug">{alert.message}</p>

              {alert.recommendation && (
                <div className="mt-2 pt-2 border-t border-dark-border/40 text-xxs text-gray-400 flex items-start space-x-1">
                  <ShieldAlert className="w-3.5 h-3.5 text-alert-warning shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold text-gray-300">Dispatch recommendation:</span>{' '}
                    <span>{alert.recommendation}</span>
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
