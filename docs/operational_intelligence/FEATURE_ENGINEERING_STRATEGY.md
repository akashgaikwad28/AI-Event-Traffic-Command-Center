# FEATURE ENGINEERING STRATEGY

To maximize the predictive power of the GridWise AI system, we must look beyond basic categorical encoding and focus on **Spatial Risk Features**, **Geo-Reconstruction**, and **Incident Cascading Intelligence**.

## 1. Spatial Memory Features (Coordinate-First Architecture)
We have discovered that categorical geography (zones, junctions) is fundamentally broken and sparse. The system reconstructs operational geography dynamically using unsupervised spatial intelligence (DBSCAN). Using this coordinate-first foundation, we engineer operational memory:

- **`historical_cluster_pressure`:** Historical incident pressure inside the same geo cluster.
- **`cluster_recurrence_score`:** Frequency of repeated incidents in the same cluster.
- **`cluster_volatility`:** Variance in operational severity inside the cluster.
- **`escalation_frequency`:** How often incidents in the cluster required escalation.
- **`historical_clearance_avg`:** Average clearance duration for the cluster.

## 2. Incident Cascading Intelligence
Real command centers care heavily about secondary disruptions. We model:
- **`upstream_congestion_probability`:** The likelihood of congestion radiating to preceding road nodes.
- **`secondary_incident_likelihood`:** The probability that the primary event triggers secondary accidents within a 2km radius.
- **`spillover_corridor_risk`:** Identifying adjacent operational corridors at risk of blockage.
- **`congestion_amplification_factor`:** A multiplier predicting how rapidly congestion will worsen based on the specific bottleneck characteristics.

## 3. Operational & Temporal Stress Index
Temporal patterns heavily dictate operational severity. These features combine to form the city pressure intelligence:

- **`temporal_stress_score`:** A synthesized metric aggregating rush hour timing, global event density, active hotspot load, and historical closure frequency for the current hour.
- **`is_rush_hour`:** Boolean flag for 07:00-09:30 and 16:30-19:00.
- **`time_since_last_incident`:** Temporal gap since the last major event in the same cluster.

## 4. Incident Complexity Score
A highly predictive meta-feature summarizing the incident's inherent difficulty:
- **`incident_complexity_score`:** A 0-1 weighted sum derived from the presence of heavy vehicles, road closure requirements, hotspot geographic location, multi-corridor impact, and the underlying event cause.

## 5. Imputation Strategy
- **`veh_type` (40% Null):** Impute based on the dominant vehicle type associated with specific `event_cause` categories.
- **`corridor` (0.24% Null):** Impute via spatial K-Nearest Neighbors using latitude/longitude.
- **`priority` (0.02% Null):** Mode imputation based on `event_type`.
