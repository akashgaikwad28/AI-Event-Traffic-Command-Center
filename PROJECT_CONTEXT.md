# PROJECT_CONTEXT.md

````md id="2af0ki"
# PROJECT_CONTEXT.md

## Project Name

GRIDWISE AI

Tagline:
AI-Powered Traffic Incident Operations & Congestion Intelligence Platform

---

# Project Vision

GRIDWISE AI is a smart-city traffic intelligence platform designed to:
- forecast event-driven congestion
- optimize police/resource deployment
- simulate traffic impact
- recommend diversions
- monitor incident lifecycle
- provide operational intelligence to traffic authorities

The system transforms historical and real-time traffic event data into:
- actionable insights
- operational recommendations
- predictive congestion intelligence

Primary goal:
Build a production-style AI traffic command center prototype capable of winning hackathons while maintaining real industry engineering standards.

---

# Core Problem Statement

Using historical and real-time event data, predict:
- traffic congestion impact
- affected regions
- resource requirements
- diversion plans
- incident severity

Provide:
- AI-powered recommendations
- live operational dashboards
- congestion simulations
- post-event analytics

---

# Primary Features

## 1. Event Impact Forecasting
Predict:
- congestion severity
- congestion spread radius
- expected delays
- junction risk

---

## 2. Resource Optimization
Recommend:
- police deployment
- barricade placement
- traffic diversions
- signal adjustments

---

## 3. Incident Intelligence
Track:
- event lifecycle
- response time
- closure time
- SLA breaches
- operational efficiency

---

## 4. Geospatial Intelligence
Provide:
- hotspot detection
- congestion heatmaps
- route impact analysis
- zone-based analytics

---

## 5. Simulation Engine
Simulate:
- event impact propagation
- intervention effectiveness
- congestion reduction scenarios

---

## 6. Operational Dashboard
Display:
- live congestion map
- event overlays
- AI recommendations
- analytics
- operational KPIs

---

# Dataset Characteristics

Dataset includes:
- geospatial coordinates
- junctions
- zones
- police assignments
- event timestamps
- incident lifecycle data
- road closures
- event categories
- response metadata

This is NOT a generic ML dataset.

Architecture should reflect:
- operational intelligence
- geospatial analytics
- incident management
- resource optimization

NOT only prediction pipelines.

---

# Engineering Philosophy

This project follows:
- minimal architecture
- modular design
- production-oriented engineering
- scalable structure
- maintainable services
- reusable components

Avoid:
- overengineering
- excessive abstractions
- tutorial-style code
- unnecessary files
- duplicate logic

Priority:
1. Simplicity
2. Maintainability
3. Reusability
4. Scalability
5. Performance

---

# Architecture Overview

```txt id="v0kgnv"
Frontend
    ↓
API Layer
    ↓
Services Layer
    ↓
Repositories Layer
    ↓
Database

AI + Analytics + Geo + Optimization
    ↓
Operational Intelligence
````

---

# Backend Stack

## Framework

* FastAPI

## Database

* PostgreSQL
* Redis

## ORM

* SQLAlchemy

## Validation

* Pydantic

## Migrations

* Alembic

## AI/ML

* Scikit-learn
* XGBoost
* LightGBM
* Prophet

## Geo

* GeoPandas
* Shapely
* Haversine
* Mapbox

## Streaming

* WebSockets

## Monitoring

* Prometheus
* Grafana

---

# Frontend Stack

## Framework

* Next.js

## Styling

* TailwindCSS

## Maps

* Mapbox GL

## Charts

* Recharts / D3

## State

* Zustand

---

# Core Architectural Rules

## API Layer

Routes must:

* remain thin
* contain no business logic
* contain no database logic
* contain no AI logic

Routes only:

* validate
* call services
* return responses

---

## Services Layer

Business logic belongs ONLY in:

```txt id="a6c9sz"
backend/app/services/
```

Services must:

* remain stateless
* reusable
* composable
* testable

---

## Repository Layer

Database access belongs ONLY in:

```txt id="ys4c40"
repositories/
```

No direct DB access outside repositories.

---

## AI Layer

All ML logic belongs ONLY in:

```txt id="zl9v7q"
backend/app/ai/
```

Separate:

* training
* inference
* feature engineering
* evaluation

---

## Geo Layer

All geospatial logic belongs ONLY in:

```txt id="zfyvzg"
backend/app/geo/
```

Avoid duplicated geo calculations.

---

## Analytics Layer

Analytics belongs ONLY in:

```txt id="5jffz5"
backend/app/analytics/
```

Includes:

* congestion analytics
* SLA analytics
* zone analytics
* operational KPIs

---

## Exception Handling

Use centralized exception handling.

Never expose raw exceptions.

Use:

* custom exceptions
* standardized responses
* structured logging

---

## Logging

Use centralized structured logging.

Never use:

```python id="jpfow3"
print()
```

Use:

```python id="5xb2vw"
logger.info()
logger.error()
logger.warning()
```

---

# AI Development Rules

AI agents MUST:

* minimize code generation
* avoid unnecessary files
* reuse existing services
* avoid duplicate utilities
* avoid placeholder implementations
* avoid fake abstractions

Before creating code:

1. Check existing implementation
2. Reuse existing modules
3. Extend existing service if appropriate

---

# Code Style Rules

Code should be:

* concise
* typed
* modular
* production-oriented
* readable

Prefer:

* small functions
* reusable utilities
* composition over inheritance
* early returns

Avoid:

* giant classes
* giant functions
* deep nesting
* unnecessary patterns

---

# Performance Philosophy

Optimize for:

1. clarity
2. maintainability
3. performance

Do NOT prematurely optimize.

---

# Hackathon Strategy

Primary judging focus:

* operational realism
* AI integration
* visual impact
* system thinking
* deployability
* decision intelligence

Important:
The project should feel like a real smart-city operations platform.

Not merely:

* an ML notebook
* a prediction demo
* a dashboard clone

---

# Key Demo Narrative

Event detected
↓
AI predicts congestion
↓
System recommends interventions
↓
Simulation compares outcomes
↓
Dashboard visualizes impact reduction

Core message:
"AI-assisted traffic operations intelligence for smart cities."

---

# Current Project Priorities

Priority Order:

1. Stable architecture
2. API foundation
3. Logging + exceptions
4. Geo intelligence
5. AI prediction pipelines
6. Dashboard visualization
7. Simulation engine
8. Optimization engine
9. Monitoring
10. MLOps

---

# Non-Goals

Do NOT:

* build unnecessary microservices
* add Kubernetes complexity early
* overbuild authentication
* create excessive abstractions
* implement premature scaling systems

This is a hackathon prototype with production-grade engineering discipline.

---

# Ideal Final Experience

The final system should feel like:

* a traffic command center
* an urban intelligence platform
* a smart-city operations dashboard

It should demonstrate:

* AI forecasting
* operational optimization
* geospatial analytics
* decision intelligence
* simulation capability

while remaining:

* clean
* modular
* maintainable
* minimal
* scalable

```
```
