# WebSocket Event Flow

This document visualizes the exact, non-blocking asynchronous event lifecycle that powers the real-time UI synchronization in GridWise AI.

## Real-Time Synchronization Architecture

```mermaid
sequenceDiagram
    participant S as Sensor / Ingestion (IoT)
    participant E as StreamEngine (FastAPI)
    participant ML as PredictionEngine (MLOps)
    participant W as WebSocketManager
    participant UI as React Frontend (Zustand)

    S->>E: POST /simulate-event (Payload: lat, lng, type)
    activate E
    
    Note over E,ML: Async Execution (Thread Pool)
    E->>ML: generate_full_assessment(raw_event)
    activate ML
    ML-->>E: Enriched Event (GORI, Deployment Plan)
    deactivate ML

    E->>E: Add to Priority Queue
    E->>W: _dispatch_queue() (Dequeue Enriched Event)
    deactivate E

    activate W
    W->>UI: Broadcast to topic 'live_events'
    
    alt If GORI > 80 (Critical)
        W->>UI: Broadcast to topic 'gori_alerts'
    end
    deactivate W

    activate UI
    UI->>UI: Zustand Incident Store Updated
    UI->>UI: Zustand GORI Store recalculates City Average
    UI-->>S: Real-time UI reflects exact Sensor state
    deactivate UI
```

## Explanation
*   **Thread-Pooled Inference:** The FastAPI event loop is single-threaded async. Because ML inference (XGBoost/Random Forest) is CPU-bound and blocking, `StreamEngine` pushes the inference request to an `asyncio` ThreadPoolExecutor to prevent blocking other incoming WebSocket connections.
*   **Dual-Topic Broadcasting:** The WebSocket Manager broadcasts the core incident data to `live_events`, but also listens for critical thresholds (GORI > 80) to simultaneously fire alerts to the `gori_alerts` channel, which drives the "Executive Alert Notifications" component on the frontend.
*   **Zustand Recalculation:** The moment the React frontend receives the payload, it not only adds the incident to the map but triggers a mathematical recalculation of the entire city's Average GORI score, instantly updating the macro dashboard dial.
