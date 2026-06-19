# LEAKAGE RISK REPORT

## 1. The Danger of Target Leakage
Target leakage occurs when a model is trained using information that will **not** be available at the exact moment a prediction needs to be made in a live production environment (e.g., at the instant an incident is reported). If leakage is not aggressively mitigated, the model will report near-perfect accuracy during training but fail completely when deployed.

## 2. Leakage Vector Analysis

### `status`
- **Leakage Severity:** EXTREME
- **Why Dangerous:** The status changes to "Closed" or "Resolved" only after the incident concludes.
- **Real-World Deployment Consequence:** In production, a new incident always has the status "Open". If the model learns to associate "Closed" with shorter or longer duration times, it will crash when it only sees "Open" inputs during live inference.
- **Mitigation Strategy:** **DROP entirely** before training.

### `modified_datetime`
- **Leakage Severity:** HIGH
- **Why Dangerous:** The last modification time usually corresponds to when the ticket was resolved or updated during resolution.
- **Real-World Deployment Consequence:** The timestamp will act as a proxy for `closed_datetime`. The model will learn to subtract `start_datetime` from `modified_datetime` to perfectly "predict" the duration.
- **Mitigation Strategy:** **DROP entirely** before training.

### `closed_datetime` / `resolved_datetime`
- **Leakage Severity:** CRITICAL (When used as features)
- **Why Dangerous:** These *are* the ground truth values we want to predict.
- **Real-World Deployment Consequence:** Cannot exist at inference time.
- **Mitigation Strategy:** Extract only to create the target variable (`incident_clearance_duration`), then **DROP** the raw timestamps from the feature matrix.

### `closed_by_id` / `resolved_by_id`
- **Leakage Severity:** HIGH
- **Why Dangerous:** An officer is assigned or logs closure only when the incident is finishing.
- **Real-World Deployment Consequence:** If used, the model effectively learns "if Officer X closed it, it took 45 minutes," but Officer X isn't known when the incident first occurs.
- **Mitigation Strategy:** **DROP entirely** before training.

## 3. Safe Features (Available at Creation Time)
- `latitude` & `longitude`
- `event_type` & `event_cause`
- `start_datetime` (used to extract day-of-week, hour-of-day, rush-hour flag)
- `priority` & `requires_road_closure`
- `veh_type`

By strictly segregating these "Creation Time" features from the "Post-Creation" leakage vectors, we ensure our Command Center models mimic true production capabilities.
