/**
 * Post-Event Learning types.
 *
 * Mirrors backend/app/learning/contracts/learning_contracts.py.
 * No `any` — fully typed for strict TypeScript.
 */

export type DriftStatus = 'STABLE' | 'WATCH' | 'DRIFT_DETECTED';

export interface AccuracyMetrics {
  resolved_count: number;
  mean_absolute_error_mins: number;
  root_mean_squared_error_mins: number;
  mean_bias_mins: number;
  over_predict_rate: number;
  under_predict_rate: number;
  accuracy_tier: string;
  drift_status: DriftStatus;
}

export interface LearningInsight {
  generated_at: string;
  accuracy: AccuracyMetrics;
  lessons: string[];
  retraining_recommendation: string;
}

export interface PredictionWithOutcome {
  incident_id: string;
  gori_score: number;
  predicted_clearance_mins: number;
  actual_clearance_mins: number | null;
  deployment_class: string;
  scenario_category: string | null;
  scenario_subtype: string | null;
  error_mins: number | null;
  prediction_bias: 'OVER' | 'UNDER' | 'EXACT' | null;
  predicted_at: string;
  resolved_at: string | null;
}

export interface LearningState {
  loop_active: boolean;
  insights: LearningInsight;
  recent_predictions: PredictionWithOutcome[];
}
