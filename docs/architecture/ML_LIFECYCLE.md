# Machine Learning Lifecycle

This document visualizes the exact, sequential flow of the GridWise AI Machine Learning pipeline, highlighting the dependencies between the specialized inference models.

## Operational Intelligence Sequence

```mermaid
graph TD
    subgraph "1. Feature Engineering & Spatial Clustering"
        A[Raw Lat/Lng] --> B(DBSCAN Clustering)
        B -->|Spatial Context| C{Feature Extractor}
        C -->|Rush Hour Boolean| C
        C -->|Heavy Vehicle Boolean| C
    end

    subgraph "2. The Congestion Model (Severity)"
        C -->|Processed Features| D[XGBoost Regression Model]
        D -->|Base Severity Output| E(GORI Math Engine)
        E -->|Time/Spread Penalties| E
        E -->|Final GORI Score: 0-100| F[Grid Operations Risk Index]
    end

    subgraph "3. The Deployment Model (Constraints)"
        F --> G[Random Forest Classifier]
        G -->|Officer Count| H[Deployment Plan]
        G -->|Barricade Count| H
        G -->|Heavy Tow Required?| H
    end

    subgraph "4. The Response Model (Forecasting)"
        H --> I[XGBoost Forecasting Model]
        I -->|Monte Carlo Spread Prob.| J(What-If Timeline)
        J -->|Best Case Clearance| K[Clearance Times]
        J -->|Expected Case Clearance| K
        J -->|Worst Case Clearance| K
    end

    subgraph "5. Post-Event Feedback Loop"
        K -->|Actual Clearance Delta| L[DVC / DagsHub Storage]
        L -->|Retraining Trigger| D
        L -->|Retraining Trigger| G
        L -->|Retraining Trigger| I
    end

    classDef stage1 fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:white;
    classDef stage2 fill:#991b1b,stroke:#ef4444,stroke-width:2px,color:white;
    classDef stage3 fill:#065f46,stroke:#10b981,stroke-width:2px,color:white;
    classDef stage4 fill:#4c1d95,stroke:#8b5cf6,stroke-width:2px,color:white;
    classDef stage5 fill:#1f2937,stroke:#9ca3af,stroke-width:2px,color:white;

    class A,B,C stage1;
    class D,E,F stage2;
    class G,H stage3;
    class I,J,K stage4;
    class L stage5;
```

## Explanation
*   **Sequential Dependency:** The models do not execute in parallel. The Random Forest Deployment model *strictly requires* the GORI output of the XGBoost Congestion model to calculate its dispatch.
*   **Coordinate-First:** Notice that the very first step is DBSCAN clustering. We do not use predefined road junctions. We cluster raw coordinates on the fly to find anomalous densities.
*   **The Feedback Loop:** This demonstrates our MLOps maturity. The final "Actual Clearance Delta" is passed back into DagsHub to trigger retraining, ensuring the system learns from its operational failures.
