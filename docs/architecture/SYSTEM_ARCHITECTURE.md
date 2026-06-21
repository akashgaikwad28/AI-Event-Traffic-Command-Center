# System Architecture

This document visualizes the high-level system architecture of GridWise AI, illustrating the flow of data from ingestion to UI visualization.

## High-Level Data Flow

```mermaid
graph TD
    subgraph "External/Simulated IoT Layer"
        A[IoT Sensors / Cameras] -->|Raw Lat/Lng & Velocity| B(Ingestion Simulator)
        B -->|Event Payload| C[WebSocket Ingestion]
    end

    subgraph "FastAPI Backend Core"
        C --> D{Stream Engine}
        D --> E[Priority Queue]
        
        E -->|Dequeued Event| F(WebSocket Manager)
        
        D -->|Enrichment Request| G((Prediction Engine))
    end

    subgraph "ML Operations Layer"
        G --> H[XGBoost Congestion Model]
        G --> I[Random Forest Deployment Model]
        G --> J[XGBoost Response Model]
        
        H -->|GORI Score| G
        I -->|Officer/Barricade Counts| G
        J -->|Clearance Timeline| G
    end

    subgraph "Data & Graph Layer"
        G --> K[NetworkX Diversion Engine]
        K -->|Bypass Efficiency & Polyline| G
        
        G --> L[(PostgreSQL / TimescaleDB)]
    end

    subgraph "React Frontend (Zustand)"
        F -->|Live Broadcast| M[Incident Store]
        M --> N[Executive Dashboard]
        M --> O[Operations Planner]
        
        O -->|Trigger Analysis| P[GenAI Copilot]
        P -->|Role-Based Context| O
    end

    classDef core fill:#1e3a8a,stroke:#3b82f6,stroke-width:2px,color:white;
    classDef ml fill:#065f46,stroke:#10b981,stroke-width:2px,color:white;
    classDef ui fill:#7c2d12,stroke:#f97316,stroke-width:2px,color:white;
    classDef db fill:#4c1d95,stroke:#8b5cf6,stroke-width:2px,color:white;

    class D,E,F core;
    class G,H,I,J ml;
    class M,N,O,P ui;
    class K,L db;
```

## Explanation
*   **External Layer:** Simulates real-world traffic camera feeds entering the system.
*   **Backend Core:** Built on FastAPI, it uses asynchronous queues to handle massive throughput without blocking UI updates.
*   **ML Operations:** The multi-model sequential pipeline that calculates the proprietary Grid Operations Risk Index (GORI) and translates it into physical deployment constraints.
*   **React Frontend:** Subscribes to the WebSocket Manager to instantly reflect incident severity and calculate macro-level city averages.
