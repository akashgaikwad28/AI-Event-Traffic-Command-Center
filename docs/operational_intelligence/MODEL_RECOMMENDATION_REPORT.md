# MODEL RECOMMENDATION REPORT

## 1. Validation Strategy (CRITICAL)
**DO NOT randomly split traffic data.** Random train-test splits on temporal data cause severe data leakage, as future traffic conditions will leak into the training set. 

**Recommendation:** **Time-Aware Validation.**
- Utilize a strict chronological split (e.g., train on January-September, test on October).
- Alternatively, use `TimeSeriesSplit` for cross-validation to ensure models are always trained on past data and evaluated on future data. This is critical for operational credibility.

## 2. Baseline Architecture
To prove the value of our complex models, we must establish naive baselines. Judges look for evidence that the AI outperforms simple heuristics.
- **Regression Baseline:** `DummyRegressor` (predicts the mean duration) and `LinearRegression`.
- **Classification Baseline:** `LogisticRegression` and a naive rule-based system.

## 3. Advanced Model Recommendations

### Regression: `incident_clearance_duration`
Predicting the exact operational clearance time in minutes.
- **Primary:** `LightGBM Regressor` (Natively handles null categories and spatial floats, extremely fast for command center inference).
- **Secondary:** `XGBoost Regressor`.
- **Avoid:** Neural Networks, LSTMs, Transformers (prone to overfitting on tabular traffic data, slow inference, low explainability).

### Classification: `deployment_load_class` & `congestion_severity`
Categorizing the severity and required manpower for dispatch.
- **Primary:** `XGBoost Classifier` & `LightGBM Classifier` (Often outperform RF on tabular operational data).
- **Benchmark:** `RandomForestClassifier` (Robust against spatial outliers).

## 4. Confidence Scoring (Enterprise AI-Grade)
Predictions alone are insufficient for a true Command Center. Every output must be accompanied by a statistical confidence interval.
- **Regression Output:** Duration prediction + 90% confidence bounds (e.g., "Expected clearance in 45 mins [35 - 60 mins]").
- **Classification Output:** Probability array for the predicted class.
- **Example UI Output:** *"High congestion risk (82%) — Confidence: Medium"*
