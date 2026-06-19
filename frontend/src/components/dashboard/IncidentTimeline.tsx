import React from 'react';
import { useIncidentStore } from '../../store/incident.store';
import { useSimulationStore } from '../../store/simulation.store';
import { Clock, TrendingUp, Cpu, Activity, CheckCircle, BrainCircuit } from 'lucide-react';

export const IncidentTimeline: React.FC = () => {
  const selectedId = useIncidentStore((state) => state.selectedIncidentId);
  const incident = useIncidentStore((state) => selectedId ? state.incidents[selectedId] : null);
  const plan = useSimulationStore((state) => selectedId ? state.operationalPlans[selectedId] : null);

  if (!incident) return null;

  const events = [
    {
      id: 'creation',
      time: 'T-0',
      title: 'Anomaly Detected',
      desc: `High confidence anomaly: ${incident.type}`,
      icon: <Activity className="w-4 h-4 text-gray-400" />,
      color: 'bg-dark-border',
      completed: true,
    },
    {
      id: 'spike',
      time: 'T+2m',
      title: 'GORI Spike',
      desc: `Risk elevated to ${Math.round(incident.gori_score)}/100`,
      icon: <TrendingUp className="w-4 h-4 text-alert-high" />,
      color: incident.gori_score > 70 ? 'bg-alert-high' : 'bg-alert-warning',
      completed: true,
    },
    {
      id: 'optimization',
      time: 'T+4m',
      title: 'AI Copilot Analysis',
      desc: plan ? 'Optimization plan synthesized' : 'Awaiting simulation...',
      icon: <BrainCircuit className={`w-4 h-4 ${plan ? 'text-brand-accent' : 'text-gray-500 animate-pulse'}`} />,
      color: plan ? 'bg-brand-accent' : 'bg-dark-border',
      completed: !!plan,
    },
    {
      id: 'simulation',
      time: 'T+5m',
      title: 'Graph Rebalancing',
      desc: plan ? `Simulated ${plan.simulation_result.predicted_gori_reduction}% GORI reduction` : 'Pending...',
      icon: <Cpu className={`w-4 h-4 ${plan ? 'text-brand-primary' : 'text-gray-500'}`} />,
      color: plan ? 'bg-brand-primary' : 'bg-dark-border',
      completed: !!plan,
    },
    {
      id: 'resolution',
      time: 'T+?m',
      title: 'Operational Readiness',
      desc: plan ? 'Ready for tactical deployment' : 'Pending...',
      icon: <CheckCircle className={`w-4 h-4 ${plan ? 'text-severity-stable' : 'text-gray-500'}`} />,
      color: plan ? 'bg-severity-stable' : 'bg-dark-border',
      completed: !!plan,
    }
  ];

  return (
    <div className="bg-dark-card border border-dark-border p-4 rounded-xl shadow-lg mt-4">
      <h3 className="text-xs font-bold uppercase tracking-wider text-gray-400 mb-4 flex items-center">
        <Clock className="w-4 h-4 mr-2" />
        Incident Lifecycle Timeline
      </h3>
      <div className="relative pl-3 space-y-6">
        {/* Vertical Line */}
        <div className="absolute top-2 bottom-2 left-[15px] w-px bg-dark-border z-0"></div>

        {events.map((evt) => (
          <div key={evt.id} className={`relative z-10 flex items-start space-x-4 ${evt.completed ? 'opacity-100' : 'opacity-40'}`}>
            <div className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 border-2 border-dark-card ${evt.color}`}>
              {evt.icon}
            </div>
            <div className="-mt-1">
              <div className="flex items-center space-x-2">
                <span className="text-xs font-bold text-gray-200">{evt.title}</span>
                <span className="text-[10px] font-mono text-gray-500">{evt.time}</span>
              </div>
              <p className="text-xs text-gray-400 mt-0.5">{evt.desc}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
