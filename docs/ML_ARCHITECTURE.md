# GridWise AI Intelligence Lifecycle

GridWise AI transforms reactive traffic management into predictive operational intelligence. This document explains our end-to-end Machine Learning Architecture, explicitly demonstrating how raw data becomes an actionable deployment plan, and how the system learns from its mistakes.

## 1. The Core Architecture

We utilize a modular ML lifecycle consisting of three major pillars:
1. **Data Engineering** (`data_pipeline/`)
2. **ML Engineering** (`ml_pipeline/`)
3. **Real-time Inference** (`backend/app/stream/`)

### Architecture Flow

```mermaid
sequenceDiagram
    participant RawData as Raw Event Data
    participant DP as Data Pipeline
    participant DBSCAN as Spatial Clustering
    participant ML as ML Training Pipeline
    participant Inf as Inference Engine
    participant Ops as Operations Planner
    participant PEL as Post-Event Learning

    %% Phase 1: Training
    RawData->>DP: Ingest sparse CSV data
    DP->>DBSCAN: Reconstruct spatial hotspots (lat/lng)
    DBSCAN->>ML: Pass structured feature set
    ML->>ML: Train RandomForest (GORI Prediction)
    ML->>Inf: Serialize & Deploy Models

    %% Phase 2: Live Inference
    Ops->>Inf: New Live Incident (Coordinates)
    Inf->>Inf: Calculate Congestion & Spread Risk
    Inf->>Ops: Return Optimized Deployment Plan

    %% Phase 3: Learning
    Ops->>PEL: Actual Incident Concludes
    PEL->>PEL: Compare Predicted GORI vs Actual
    PEL-->>ML: Trigger Retraining if Drift Detected
```

## 2. Key Differentiators

### Coordinate-First Spatial Intelligence
Traditional traffic systems rely on static "zones" or "junction names". Our exploratory analysis revealed this categorical data was severely sparse and error-prone.
* **Our Solution:** We discard static zones. Our `data_pipeline/spatial_clustering/` module uses **DBSCAN** algorithms on raw latitude/longitude coordinates to dynamically reconstruct traffic hotspots based on historical densities.

### Post-Event Learning
We directly solved the hackathon challenge requirement: *"No post-event learning system"*.
* **Our Solution:** The `ml_pipeline/post_event_learning/` module evaluates the actual congestion reduction achieved by the deployed officers against the ML's prediction. If the prediction error exceeds 15%, the system triggers an automatic retraining hook to adapt to changing urban conditions.
