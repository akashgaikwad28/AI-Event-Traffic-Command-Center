# API Reference

Base Path: `/api/v1`

## Events (`/events`)
- `POST /events`: Create a new event. Payload: `EventCreate`. Response: `EventResponse`.
- `GET /events`: List events with pagination and filters. Response: `PaginatedResponse[EventResponse]`.
- `GET /events/{event_id}`: Get a single event by ID. Response: `EventResponse`.
- `PATCH /events/{event_id}`: Update an existing event. (Not Implemented)
- `DELETE /events/{event_id}`: Delete an event. (Not Implemented)

## Stream (`/stream`)
- `POST /stream/start-simulation/{scenario}`: Triggers a simulation scenario in the background. Optional payload: `SimulationPayload` (lat, lng, gori, hvi, rush).
- `GET /stream/live-snapshot`: Returns dashboard snapshot using fast in-memory Stream Cache. Response: `DashboardSnapshot`.
- `GET /stream/metrics`: Exposes Stream Health Monitoring metrics.

## Optimization (`/optimization`)
- `POST /optimization/incident-response`: AI Traffic Operations Command Center Endpoint. Generates dynamic resource allocation, graph diversion, and impact simulation. Request: `OptimizationRequestDTO`, Response: `OperationalPlanDTO`.

## Copilot (`/copilot`)
- `POST /copilot/explain`: Analyzes and explains a specific event, incident, or operational anomaly. Request: `CopilotExplainRequest`, Response: `CopilotResponse`.
- `POST /copilot/analyze`: Performs deep analysis on traffic patterns, resource allocations, or systemic issues. Request: `CopilotAnalyzeRequest`, Response: `CopilotResponse`.

## Other Endpoints
Additional routers are mounted for `/health`, `/analytics`, `/predictions`, `/simulation`, `/genai`, and `/observability`.
