import React, { useState } from 'react';
import { FileText, Download, FileBarChart, Clock, ShieldCheck, CheckCircle } from 'lucide-react';
import { useGoriStore } from '../store/gori.store';
import { useIncidentStore } from '../store/incident.store';
import { useSimulationStore } from '../store/simulation.store';

type ReportType = 'EXECUTIVE' | 'SHIFT_HANDOVER' | 'DAILY_OPS';

export const ReportsPage: React.FC = () => {
  const [activeReport, setActiveReport] = useState<ReportType>('EXECUTIVE');
  const [isExporting, setIsExporting] = useState(false);
  const avgGori = useGoriStore(state => state.avgGori);
  const incidents = useIncidentStore(state => Object.values(state.incidents));
  const plans = useSimulationStore(state => state.operationalPlans);
  const activeCount = incidents.length;

  const handleExport = () => {
    setIsExporting(true);
    setTimeout(() => {
      setIsExporting(false);
      
      const reportPayload = {
        generated_at: new Date().toISOString(),
        report_type: activeReport,
        global_metrics: {
          city_gori_risk: avgGori.toFixed(1),
          active_critical_incidents: activeCount,
        },
        active_incidents: incidents.map(inc => ({
          id: inc.incident_id,
          location: [inc.latitude, inc.longitude],
          severity: inc.gori_score,
          associated_plan: plans[inc.incident_id] || null
        }))
      };

      const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(reportPayload, null, 2));
      const el = document.createElement('a');
      el.setAttribute('href', dataStr);
      el.setAttribute('download', `GridWise_Intelligence_${activeReport}_${new Date().getTime()}.json`);
      el.click();
    }, 800);
  };

  const renderExecutiveReport = () => (
    <div className="space-y-6">
      <div className="border-b border-dark-border pb-4">
        <h3 className="text-xl font-bold text-gray-100 uppercase tracking-widest">Executive Flash Summary</h3>
        <p className="text-xs text-gray-500 mt-1">Generated: {new Date().toLocaleString()}</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-dark-bg/50 border border-dark-border rounded-lg p-4">
          <p className="text-[10px] uppercase font-bold text-gray-500 tracking-wider">City-Wide GORI Risk</p>
          <div className="mt-2 flex items-baseline space-x-2">
            <span className={`text-3xl font-black ${avgGori > 70 ? 'text-red-400' : 'text-emerald-400'}`}>{avgGori.toFixed(1)}</span>
            <span className="text-xs font-bold text-gray-400">/ 100</span>
          </div>
        </div>
        <div className="bg-dark-bg/50 border border-dark-border rounded-lg p-4">
          <p className="text-[10px] uppercase font-bold text-gray-500 tracking-wider">Critical Incidents</p>
          <div className="mt-2 flex items-baseline space-x-2">
            <span className="text-3xl font-black text-amber-400">{activeCount}</span>
            <span className="text-xs font-bold text-gray-400">active</span>
          </div>
        </div>
        <div className="bg-dark-bg/50 border border-dark-border rounded-lg p-4">
          <p className="text-[10px] uppercase font-bold text-gray-500 tracking-wider">AI Interventions</p>
          <div className="mt-2 flex items-baseline space-x-2">
            <span className="text-3xl font-black text-brand-primary">12</span>
            <span className="text-xs font-bold text-gray-400">successful</span>
          </div>
        </div>
      </div>

      <div className="bg-brand-accent/5 border border-brand-accent/20 rounded-lg p-5 mt-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-4 opacity-10">
          <ShieldCheck className="w-24 h-24 text-brand-accent" />
        </div>
        <h4 className="text-xs font-bold text-brand-accent uppercase tracking-widest mb-3">AI Strategic Analysis</h4>
        <div className="text-sm text-gray-300 leading-relaxed space-y-3 relative z-10">
          <p>
            The grid is currently operating under <strong>Elevated Capacity Constraints</strong>. Within the last 4 hours, cascading congestion has been successfully contained via 12 automated diversion deployments.
          </p>
          <p>
            Key risk vector remains the primary arterial network, which is experiencing a 15% latency increase. AI optimization recommends pre-positioning barricade units at Zone A4 for the upcoming evening rush phase to mitigate cross-corridor spillover.
          </p>
        </div>
      </div>
      
      <div className="mt-6 border-t border-dark-border pt-6">
        <h4 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-4">Top Active Priorities</h4>
        <div className="space-y-3">
          {incidents.slice(0, 3).map(inc => (
            <div key={inc.incident_id} className="flex items-center justify-between bg-dark-bg p-3 rounded border border-dark-border/50">
              <div className="flex flex-col">
                <span className="text-xs font-bold text-gray-200">{inc.type.replace(/_/g, ' ')} at {inc.latitude.toFixed(3)}, {inc.longitude.toFixed(3)}</span>
                <span className="text-[10px] text-gray-500">{inc.deployment_recommendation || 'Standard Response Required'}</span>
              </div>
              <span className={`text-xs font-bold px-2 py-1 rounded ${inc.gori_score > 70 ? 'bg-red-500/20 text-red-400' : 'bg-emerald-500/20 text-emerald-400'}`}>
                Risk: {Math.round(inc.gori_score)}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  return (
    <div className="h-full w-full overflow-y-auto p-6 bg-dark-bg text-gray-200">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 border-b border-dark-border pb-6">
        <div>
          <h2 className="text-2xl font-extrabold text-gray-100 tracking-wide flex items-center">
            <FileText className="w-6 h-6 mr-3 text-brand-accent" />
            Intelligence Reports
          </h2>
          <p className="text-sm text-gray-500 font-medium mt-1">Generated tactical summaries and official operational documents.</p>
        </div>
        <div className="mt-4 md:mt-0">
          <button 
            onClick={handleExport}
            disabled={isExporting}
            className="flex items-center space-x-2 px-4 py-2 bg-brand-primary/10 border border-brand-primary/50 text-brand-primary rounded hover:bg-brand-primary/20 transition-all font-bold text-sm tracking-wide"
          >
            {isExporting ? <CheckCircle className="w-4 h-4 animate-pulse" /> : <Download className="w-4 h-4" />}
            <span>{isExporting ? 'EXPORTING PDF...' : 'EXPORT TO PDF'}</span>
          </button>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-8">
        {/* Sidebar Nav */}
        <div className="lg:w-64 flex-shrink-0 space-y-2">
          <button 
            onClick={() => setActiveReport('EXECUTIVE')}
            className={`w-full flex items-center p-3 rounded-lg border text-left transition-colors ${activeReport === 'EXECUTIVE' ? 'bg-dark-card border-brand-accent/50 text-brand-accent' : 'bg-transparent border-transparent text-gray-400 hover:bg-dark-bg/80'}`}
          >
            <ShieldCheck className="w-4 h-4 mr-3" />
            <span className="text-sm font-bold tracking-wide">Executive Summary</span>
          </button>
          <button 
            onClick={() => setActiveReport('SHIFT_HANDOVER')}
            className={`w-full flex items-center p-3 rounded-lg border text-left transition-colors ${activeReport === 'SHIFT_HANDOVER' ? 'bg-dark-card border-brand-accent/50 text-brand-accent' : 'bg-transparent border-transparent text-gray-400 hover:bg-dark-bg/80'}`}
          >
            <Clock className="w-4 h-4 mr-3" />
            <span className="text-sm font-bold tracking-wide">Shift Handover</span>
          </button>
          <button 
            onClick={() => setActiveReport('DAILY_OPS')}
            className={`w-full flex items-center p-3 rounded-lg border text-left transition-colors ${activeReport === 'DAILY_OPS' ? 'bg-dark-card border-brand-accent/50 text-brand-accent' : 'bg-transparent border-transparent text-gray-400 hover:bg-dark-bg/80'}`}
          >
            <FileBarChart className="w-4 h-4 mr-3" />
            <span className="text-sm font-bold tracking-wide">Daily Operations Log</span>
          </button>
        </div>

        {/* Report Content */}
        <div className="flex-1 bg-dark-card border border-dark-border rounded-xl p-8 shadow-2xl min-h-[600px] relative">
          {/* Top-secret watermark effect */}
          <div className="absolute inset-0 flex items-center justify-center opacity-[0.02] pointer-events-none select-none overflow-hidden">
            <span className="text-[150px] font-black uppercase tracking-tighter rotate-[-45deg]">CONFIDENTIAL</span>
          </div>
          
          <div className="relative z-10">
            {activeReport === 'EXECUTIVE' && renderExecutiveReport()}
            {activeReport === 'SHIFT_HANDOVER' && (
              <div className="flex flex-col items-center justify-center h-64 text-gray-500">
                <Clock className="w-12 h-12 mb-4 opacity-50" />
                <p>Shift handover report generation requires End of Shift trigger.</p>
              </div>
            )}
            {activeReport === 'DAILY_OPS' && (
              <div className="flex flex-col items-center justify-center h-64 text-gray-500">
                <FileBarChart className="w-12 h-12 mb-4 opacity-50" />
                <p>Daily Operations Log is compiling. Available at 00:00.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
