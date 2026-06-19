# FINAL OPERATIONAL AI ARCHITECTURE PLAN
**GridWise AI - Operational Decision Intelligence for Smart Traffic Command Centers**

## 1. System Vision
We built an AI-powered traffic operations intelligence system. The system ingests raw traffic incident coordinates, enriches them with spatial intelligence, models the operational closure duration, and outputs actionable dispatch recommendations through our unified operational intelligence layer.

## 2. Core Target Pivots
- **Primary Target (Regression):** `incident_clearance_duration` (Engineered dynamically by subtracting `start_datetime` from `closed_datetime`). We explicitly abandoned the 99% null `resolved_datetime` to ensure statistical viability.
- **Secondary Target (Classification):** `deployment_load_class` (Heuristically derived from event cause, vehicle type, and priority to simulate dispatch requirements).

## 3. Data Governance & Leakage Defense
- **Dropped Features (Extreme Leakage):** `status`, `modified_datetime`, `closed_by_id`.
- **Validation Protocol:** Strict **Time-Aware Validation** (chronological splits via `TimeSeriesSplit`) to prevent future-data leakage into historical training sets.

## 4. Feature Architecture (Coordinate-First)
Because categorical locations (`zone`, `junction`) are severely sparse, the system reconstructs operational geography dynamically using unsupervised spatial intelligence:
1. **DBSCAN Geo-Clustering:** Creating spatial memory and tracking `historical_cluster_pressure`.
2. **Cascading Intelligence:** `upstream_congestion_probability` and `spillover_corridor_risk`.
3. **Operational Stress:** `temporal_stress_score` and `incident_complexity_score`.

## 5. Model Engine
- **Algorithm:** `LightGBM` & `XGBoost` (Best-in-class for tabular operational data).
- **Baselines:** Validated against `RandomForest` and naive baselines to prove empirical value.
- **Model Trust Score:** Every prediction outputs a `prediction_reliability_score` evaluating the statistical confidence interval to support safe operational decision-making.

## 6. The Command Center Output Layer (The Product)
The final architecture culminates in the Executive Command Center Dashboard (Streamlit app):
- **GridWise Operational Risk Index (GORI):** A synthesized 0-100 Unified Operational Severity Intelligence Layer with explicit Tier definitions (Low, Moderate, Elevated, High, Critical).
- **Action Recommendation AI:** Generates explicit instructions ("Priority Dispatch", "Escalate Manpower").
- **Live Incident Simulation:** Demonstrating real-world capability (e.g. Heavy truck breakdown near a hotspot during rush hour triggering an escalation cascade).
