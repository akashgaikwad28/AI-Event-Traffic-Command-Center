import React from 'react';
import { useIncidentStore } from '../../store/incident.store';
import { useGoriStore } from '../../store/gori.store';
import { useSimulationStore } from '../../store/simulation.store';
import { Activity, ShieldAlert, AlertOctagon, Users, Split } from 'lucide-react';

export const KPIBar: React.FC = () => {
  const incidents = useIncidentStore((state) => Object.values(state.incidents));
  const avgGori = useGoriStore((state) => state.avgGori);
  const plans = useSimulationStore((state) => Object.values(state.operationalPlans));

  const activeCount = incidents.length;
  const criticalCount = incidents.filter(i => i.gori_score > 70).length;

  // Sum officers from generated plans
  const totalOfficers = plans.reduce((sum, p) => sum + (p.resource_plan?.police_officers || 0), 0) || (activeCount * 3);
  const activeDiversions = plans.filter(p => p.diversion_plan?.description).length;

  const kpis = [
    {
      name: 'Active Incidents',
      value: activeCount,
      icon: AlertOctagon,
      color: 'text-brand-primary border-brand-primary/20 bg-brand-primary/5',
    },
    {
      name: 'Critical Events',
      value: criticalCount,
      icon: ShieldAlert,
      color: 'text-alert-high border-alert-high/20 bg-alert-high/5',
    },
    {
      name: 'Avg City GORI',
      value: `${avgGori}%`,
      icon: Activity,
      color: avgGori > 70 ? 'text-alert-high border-alert-high/20 bg-alert-high/5' : 'text-emerald-400 border-emerald-500/20 bg-emerald-500/5',
    },
    {
      name: 'Officers Deployed',
      value: totalOfficers,
      icon: Users,
      color: 'text-brand-accent border-brand-accent/20 bg-brand-accent/5',
    },
    {
      name: 'Active Diversions',
      value: activeDiversions,
      icon: Split,
      color: 'text-amber-500 border-amber-500/20 bg-amber-500/5',
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
      {kpis.map((kpi, idx) => {
        const Icon = kpi.icon;
        return (
          <div
            key={idx}
            className={`border rounded-xl p-4 shadow-sm flex items-center space-x-3 bg-dark-card border-dark-border`}
          >
            <div className={`p-2.5 rounded-lg border ${kpi.color}`}>
              <Icon className="w-5 h-5" />
            </div>
            <div>
              <p className="text-xxs font-bold text-gray-500 uppercase tracking-wider leading-none mb-1">{kpi.name}</p>
              <h4 className="text-xl font-extrabold text-gray-100 tracking-tight leading-none">{kpi.value}</h4>
            </div>
          </div>
        );
      })}
    </div>
  );
};
