# GridWise AI Platform Architecture

GridWise AI is not simply a set of machine learning models. It is a comprehensive **Coordinate-First Operational Intelligence System** designed to bridge the gap between raw spatial data and real-time operational decision-making.

The following architecture diagram illustrates the end-to-end intelligence lifecycle, demonstrating how raw traffic and event coordinates are seamlessly transformed into dynamic optimizations and learning loops.

## System Lifecycle Diagram

```mermaid
flowchart TD
    %% Define Styles
    classDef datafill fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef pipelinestart fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef mlfill fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef corefill fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef explainfill fill:#e0f7fa,stroke:#0097a7,stroke-width:2px;
    classDef postfill fill:#fff8e1,stroke:#fbc02d,stroke-width:2px;

    %% Data Ingestion Layer
    subgraph Data Layer
        A1[(Live Traffic APIs)]:::datafill
        A2[(Event Schedules)]:::datafill
        A3[(Weather Feeds)]:::datafill
    end

    %% Pipeline & Spatial Clustering
    subgraph Analytics Pipeline
        B[Real-Time Data Pipeline]:::pipelinestart
        C{Spatial Clustering & DBSCAN}:::pipelinestart
        D[Feature Engineering]:::pipelinestart
    end

    %% Machine Learning Engines
    subgraph Intelligence Engines
        E1[Congestion Proxy Engine]:::mlfill
        E2[Deployment Load Classifier]:::mlfill
        E3[Response Time Forecaster]:::mlfill
    end

    %% Operational Core
    subgraph Operations Core
        F[Resource Optimization Engine]:::corefill
        G[Dynamic WebSocket Streaming]:::corefill
    end

    %% Presentation & Feedback
    subgraph Presentation & Learning
        H[Command Center Dashboard]:::explainfill
        I[AI Copilot Explainer]:::explainfill
        J((Post-Event Learning Loop)):::postfill
    end

    %% Flow Relationships
    A1 --> B
    A2 --> B
    A3 -.-> B

    B --> C
    C --> D

    D --> E1
    D --> E2
    D --> E3

    E1 --> F
    E2 --> F
    E3 --> F

    F --> G
    G --> H
    G --> I

    H --> J
    I --> J
    J -. "Retrains Models" .-> D
```

## Component Overview

1. **Spatial Clustering (DBSCAN)**: Instead of relying on static zones, our system dynamically reconstructs operational clusters based on live incident density, enabling adaptive responses to unpredictable event spreads.
2. **Intelligence Engines**: We utilize XGBoost and Random Forest architectures to predict congestion severity, optimal deployment loads, and clearance times.
3. **Resource Optimization Engine**: Integrates predictive signals to allocate officers and barricades effectively across zones.
4. **WebSocket Streaming**: All intelligence is streamed with sub-second latency to the frontend command center.
5. **AI Copilot Explainer**: An LLM-driven layer translates raw optimizations into plain-English operational rationale (e.g., "Deploying 5 officers to Zone Alpha because historical spread probability is 85%").
6. **Post-Event Learning Loop**: Post-operation analytics automatically feed back into the feature store, ensuring continuous system refinement.
