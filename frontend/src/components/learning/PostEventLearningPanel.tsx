import React, { useEffect, useState } from 'react';
import { useLearningStore } from '../../store/learning.store';
import {
  Brain, CheckCircle, AlertTriangle, TrendingDown,
  ChevronDown, ChevronUp, BarChart3, BookOpen, RefreshCw,
} from 'lucide-react';
import type { DriftStatus, AccuracyMetrics } from '../../types/learning';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const TIER_STYLES: Record<string, { bg: string; text: string; border: string }> = {
  EXCELLENT:  { bg: 'bg-emerald-500/15', text: 'text-emerald-400', border: 'border-emerald-500/30' },
  GOOD:       { bg: 'bg-blue-500/15',    text: 'text-blue-400',    border: 'border-blue-500/30' },
  DEGRADING:  { bg: 'bg-amber-500/15',  text: 'text-amber-400',  border: 'border-amber-500/30' },
  POOR:       { bg: 'bg-red-500/15',    text: 'text-red-400',    border: 'border-red-500/30' },
  NO_DATA:    { bg: 'bg-gray-500/15',   text: 'text-gray-400',   border: 'border-gray-500/30' },
};

const DRIFT_STYLES: Record<DriftStatus, { icon: React.FC<{ className?: string }>; bg: string; text: string }> = {
  STABLE:          { icon: CheckCircle,    bg: 'bg-emerald-500/10', text: 'text-emerald-400' },
  WATCH:           { icon: AlertTriangle,  bg: 'bg-amber-500/10',   text: 'text-amber-400' },
  DRIFT_DETECTED:  { icon: TrendingDown,   bg: 'bg-red-500/10',     text: 'text-red-400' },
};

const BIAS_LABEL: Record<string, string> = {
  OVER: 'Over-predicted',
  UNDER: 'Under-predicted',
  EXACT: 'On target',
};

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export const PostEventLearningPanel: React.FC = () => {
  const { state, loading, error, fetchInsights, resolveIncident } = useLearningStore();
  const [expandedHistory, setExpandedHistory] = useState(true);
  const [resolvingId, setResolvingId] = useState<string | null>(null);
  const [customMins, setCustomMins] = useState('');

  useEffect(() => {
    fetchInsights();
    const interval = setInterval(fetchInsights, 15000);
    return () => clearInterval(interval);
  }, [fetchInsights]);

  const handleResolve = async (incidentId: string) => {
    const mins = parseFloat(customMins);
    if (isNaN(mins) || mins <= 0) return;
    setResolvingId(incidentId);
    await resolveIncident(incidentId, mins);
    setResolvingId(null);
    setCustomMins('');
  };

  const accuracy: AccuracyMetrics = state?.insights?.accuracy ?? {
    resolved_count: 0, mean_absolute_error_mins: 0, root_mean_squared_error_mins: 0,
    mean_bias_mins: 0, over_predict_rate: 0, under_predict_rate: 0,
    accuracy_tier: 'NO_DATA', drift_status: 'STABLE',
  };

  const tierStyle = TIER_STYLES[accuracy.accuracy_tier] ?? TIER_STYLES.NO_DATA;
  const driftStyle = DRIFT_STYLES[accuracy.drift_status];
  const DriftIcon = driftStyle.icon;
  const predictions = state?.recent_predictions ?? [];
  const lessons = state?.insights?.lessons ?? [];

  return (
    <div className="bg-dark-card border border-dark-border rounded-xl p-5 shadow-lg relative overflow-hidden">
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-purple-500 to-blue-500"></div>

      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-purple-500/10 rounded-lg border border-purple-500/20">
            <Brain className="w-5 h-5 text-purple-400" />
          </div>
          <div>
            <h3 className="font-bold text-gray-100 tracking-wide text-md">Post-Event Learning Loop</h3>
            <p className="text-xs text-gray-500">Prediction vs. Actual — system learns from every resolution</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          {loading && <RefreshCw className="w-4 h-4 text-gray-500 animate-spin" />}
          <button
            onClick={fetchInsights}
            className="flex items-center space-x-1 px-2 py-1 rounded-lg border border-dark-border bg-dark-bg text-xs text-gray-400 hover:text-gray-200 transition-colors"
          >
            <RefreshCw className={`w-3 h-3 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-500/10 border border-red-500/20 rounded-lg flex items-center space-x-2 text-xs text-red-400">
          <AlertTriangle className="w-4 h-4 shrink-0" />
          <span>Failed to connect to learning engine. Retrying...</span>
        </div>
      )}

      {/* KPI Cards */}
      <div className="grid grid-cols-4 gap-3 mb-4">
        {/* Accuracy Tier */}
        <div className={`${tierStyle.bg} border ${tierStyle.border} rounded-lg p-3`}>
          <p className="text-[9px] uppercase font-bold text-gray-500 tracking-wider mb-1">Accuracy Tier</p>
          <p className={`text-lg font-black ${tierStyle.text}`}>{accuracy.accuracy_tier}</p>
        </div>

        {/* MAE */}
        <div className="bg-dark-bg border border-dark-border rounded-lg p-3">
          <p className="text-[9px] uppercase font-bold text-gray-500 tracking-wider mb-1">MAE (mins)</p>
          <p className="text-lg font-black text-gray-100">{accuracy.mean_absolute_error_mins}</p>
        </div>

        {/* Bias */}
        <div className="bg-dark-bg border border-dark-border rounded-lg p-3">
          <p className="text-[9px] uppercase font-bold text-gray-500 tracking-wider mb-1">Mean Bias</p>
          <p className={`text-lg font-black ${accuracy.mean_bias_mins > 1 ? 'text-red-400' : accuracy.mean_bias_mins < -1 ? 'text-blue-400' : 'text-emerald-400'}`}>
            {accuracy.mean_bias_mins > 0 ? '+' : ''}{accuracy.mean_bias_mins}m
          </p>
          <p className="text-[8px] text-gray-500 mt-0.5">
            {accuracy.mean_bias_mins > 1 ? 'Under-predicts' : accuracy.mean_bias_mins < -1 ? 'Over-predicts' : 'Well-calibrated'}
          </p>
        </div>

        {/* Drift Status */}
        <div className={`${driftStyle.bg} border border-dark-border rounded-lg p-3`}>
          <p className="text-[9px] uppercase font-bold text-gray-500 tracking-wider mb-1">Drift Status</p>
          <div className="flex items-center space-x-1.5">
            <DriftIcon className={`w-4 h-4 ${driftStyle.text}`} />
            <p className={`text-sm font-black ${driftStyle.text}`}>{accuracy.drift_status}</p>
          </div>
        </div>
      </div>

      {/* Auto-extracted Lessons */}
      {lessons.length > 0 && (
        <div className="mb-4 bg-dark-bg border border-dark-border rounded-lg p-4">
          <div className="flex items-center space-x-2 mb-3">
            <BookOpen className="w-4 h-4 text-purple-400" />
            <h4 className="text-xs font-bold uppercase tracking-wider text-gray-400">Auto-Extracted Lessons</h4>
          </div>
          <ul className="space-y-2">
            {lessons.map((lesson, i) => (
              <li key={i} className="flex items-start space-x-2 text-xs text-gray-300 leading-relaxed">
                <span className="text-purple-400 font-bold mt-0.5 shrink-0">•</span>
                <span>{lesson}</span>
              </li>
            ))}
          </ul>
          {state?.insights?.retraining_recommendation && (
            <div className="mt-3 pt-3 border-t border-dark-border">
              <p className="text-[10px] text-gray-500">
                <span className="font-bold text-purple-400">Retrain: </span>
                {state.insights.retraining_recommendation}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Prediction vs Actual Table */}
      <div className="border border-dark-border rounded-lg overflow-hidden">
        <button
          onClick={() => setExpandedHistory(!expandedHistory)}
          className="w-full flex items-center justify-between p-3 bg-dark-bg hover:bg-dark-bg/80 transition-colors"
        >
          <div className="flex items-center space-x-2">
            <BarChart3 className="w-4 h-4 text-blue-400" />
            <span className="text-xs font-bold uppercase tracking-wider text-gray-400">
              Prediction vs Actual ({predictions.length} records)
            </span>
          </div>
          {expandedHistory ? <ChevronUp className="w-4 h-4 text-gray-500" /> : <ChevronDown className="w-4 h-4 text-gray-500" />}
        </button>

        {expandedHistory && (
          <div className="overflow-x-auto">
            <table className="w-full text-[10px]">
              <thead>
                <tr className="border-b border-dark-border bg-dark-bg/50">
                  <th className="text-left p-2 font-bold text-gray-500 uppercase">Incident</th>
                  <th className="text-center p-2 font-bold text-gray-500 uppercase">GORI</th>
                  <th className="text-center p-2 font-bold text-gray-500 uppercase">Predicted</th>
                  <th className="text-center p-2 font-bold text-gray-500 uppercase">Actual</th>
                  <th className="text-center p-2 font-bold text-gray-500 uppercase">Error</th>
                  <th className="text-center p-2 font-bold text-gray-500 uppercase">Bias</th>
                  <th className="text-center p-2 font-bold text-gray-500 uppercase">Type</th>
                  <th className="text-right p-2 font-bold text-gray-500 uppercase">Resolve</th>
                </tr>
              </thead>
              <tbody>
                {predictions.length === 0 && (
                  <tr>
                    <td colSpan={8} className="text-center p-4 text-gray-600">
                      No predictions yet. Run a scenario to begin the loop.
                    </td>
                  </tr>
                )}
                {predictions.map((row) => {
                  const isResolving = resolvingId === row.incident_id;
                  const isResolved = row.actual_clearance_mins !== null;
                  return (
                    <tr key={row.incident_id} className="border-b border-dark-border/50 hover:bg-dark-bg/30">
                      <td className="p-2 font-mono text-gray-300">{row.incident_id}</td>
                      <td className="p-2 text-center font-mono text-gray-300">{row.gori_score}</td>
                      <td className="p-2 text-center font-mono text-blue-400">{row.predicted_clearance_mins}m</td>
                      <td className="p-2 text-center font-mono text-emerald-400">
                        {isResolved ? `${row.actual_clearance_mins}m` : '—'}
                      </td>
                      <td className={`p-2 text-center font-mono font-bold ${
                        row.error_mins === null ? 'text-gray-600' :
                        row.error_mins > 5 ? 'text-red-400' :
                        row.error_mins < -5 ? 'text-blue-400' : 'text-emerald-400'
                      }`}>
                        {row.error_mins !== null ? `${row.error_mins > 0 ? '+' : ''}${row.error_mins}m` : '—'}
                      </td>
                      <td className="p-2 text-center">
                        {row.prediction_bias ? (
                          <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold ${
                            row.prediction_bias === 'EXACT' ? 'bg-emerald-500/15 text-emerald-400' :
                            row.prediction_bias === 'UNDER' ? 'bg-red-500/15 text-red-400' :
                            'bg-blue-500/15 text-blue-400'
                          }`}>
                            {BIAS_LABEL[row.prediction_bias] ?? row.prediction_bias}
                          </span>
                        ) : <span className="text-gray-600">—</span>}
                      </td>
                      <td className="p-2 text-center">
                        {row.scenario_category ? (
                          <span className={`px-1.5 py-0.5 rounded text-[9px] font-bold ${
                            row.scenario_category === 'PLANNED' ? 'bg-emerald-500/15 text-emerald-400' : 'bg-red-500/15 text-red-400'
                          }`}>
                            {row.scenario_category}
                          </span>
                        ) : <span className="text-gray-600">—</span>}
                      </td>
                      <td className="p-2 text-right">
                        {!isResolved ? (
                          <div className="flex items-center justify-end space-x-1">
                            <input
                              type="number"
                              min="1"
                              step="1"
                              placeholder="mins"
                              value={resolvingId === row.incident_id ? customMins : ''}
                              onChange={(e) => setCustomMins(e.target.value)}
                              disabled={isResolving}
                              className="w-14 px-1.5 py-0.5 rounded bg-dark-bg border border-dark-border text-[9px] font-mono text-gray-300 focus:outline-none focus:border-purple-500/50"
                            />
                            <button
                              onClick={() => handleResolve(row.incident_id)}
                              disabled={isResolving || !customMins}
                              className="px-1.5 py-0.5 rounded bg-purple-500/15 border border-purple-500/30 text-[9px] font-bold text-purple-400 hover:bg-purple-500/25 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                            >
                              {isResolving ? '...' : '✓'}
                            </button>
                          </div>
                        ) : (
                          <span className="flex items-center justify-end space-x-1 text-emerald-400">
                            <CheckCircle className="w-3 h-3" />
                            <span className="text-[9px] font-bold">Resolved</span>
                          </span>
                        )}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
