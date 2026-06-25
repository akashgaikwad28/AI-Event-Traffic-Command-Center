# Backend Architecture

## Overview
Gridwise AI is built with **FastAPI**. It follows a modular, domain-driven design, utilizing async execution, robust middleware, and structured observability.

```mermaid
flowchart TD
    Client([Frontend React App]) -->|HTTP / WebSocket| FastAPI[FastAPI Backend Entrypoint]

    subgraph Core["⚙️ Core Services"]
        FastAPI --> Middleware{Correlation & Auth Middleware}
        Middleware --> Routers[API Routers]
    end

    subgraph AI["🧠 AI & ML Engines"]
        Routers --> GenAI[GenAI Orchestrator]
        Routers --> PredEngine[Prediction Engine]

        GenAI -->|Primary| Groq[Groq LPU\nLLaMA/Mixtral]
        GenAI -->|Fallback| Gemini[Google Gemini API]

        PredEngine -->|Feature DataFrame| CongestionModel[XGBoost Congestion Model\n.pkl Wrapper]
        PredEngine -->|Feature DataFrame| ResponseModel[Response Time Model]

        CongestionModel --> GORI[GORI Decision Engine]
        ResponseModel --> GORI
    end

    subgraph Ops["🚔 Operational Intelligence"]
        GORI --> OptEngine[Resource Optimization Engine]
        OptEngine --> Plan([Strategic Deployment Plan])
    end

    subgraph Data["💾 Persistence & State"]
        Routers --> Stream[Stream Engine\nLive WebSockets]
        Stream --> Cache[(Stream State Cache)]
        OptEngine --> DB[(PostgreSQL Database)]
    end

    style Core fill:#e8f4f8,color:#000,stroke:#005f73
    style AI fill:#fff3cd,color:#000,stroke:#cc9a06
    style Ops fill:#d4edda,color:#000,stroke:#2b7a2b
    style Data fill:#f3e8ff,color:#000,stroke:#6b21a8
```

## Directory Structure
- `backend/app/main.py`: Application entrypoint configuring FastAPI, middleware, routing, and exception handlers.
- `backend/app/api`: Defines the REST API endpoints and websockets via `router.py`. Versioning is supported (e.g., `v1/`).
- `backend/app/core`: Configuration, core constants, structured logger, and custom middleware (`CorrelationIdMiddleware`, `CORS`).
- `backend/app/services`: Domain services encompassing geo, events, simulation, and resource optimization.
- `backend/app/stream`: Handles Real-Time AI Traffic Operations Intelligence Stream via websockets, fast caching (`stream_cache`), and background simulators.
- `backend/app/resource_optimization`: AI Operations Command Center for generating dynamic resource allocation plans.
- `backend/app/observability`: Registry for metrics tracking, latency recording, and failure tracking.

## Request Flow
1. **Middleware**: All requests pass through `CorrelationIdMiddleware` adding `x-trace-id`, `x-request-id`, and `x-session-id`, tracking overall latency and metrics.
2. **Routers**: Mapped to corresponding functional areas (`events`, `optimization`, `stream`, etc.).
3. **Services / Business Logic**: Separation of routing layer and domain logic processing.
4. **Data Access**: Asynchronous SQLAlchemy usage for database persistence.
