# Docker Setup

Gridwise AI uses Docker and Docker Compose to orchestrate its services. The setup is split into the root `docker-compose.yml` for base services and `infra/docker/docker-compose.yml` for additional app components.

## Services Architecture

The application runs the following services via Docker:
1. **Frontend (`frontend`)**: React/Node based frontend served statically via Nginx on port `80`.
2. **Backend (`backend`)**: FastAPI application on Python 3.12, running on port `8000`.
3. **ML API (`ml-api`)**: Specialized Python 3.11 service for machine learning inference, running on port `8001`.
4. **PostgreSQL (`postgres`)**: Database service using the `postgis/postgis:15-3.3` image. Persists data via the `postgres_data` volume.
5. **Redis (`redis`)**: Caching and task queue broker on port `6379`. Persists data via the `redis_data` volume.

## Dockerfiles Overview

*   **`infra/docker/Dockerfile.frontend`**: A multi-stage build that first uses `node:18-alpine` to install dependencies and build the app, then uses `nginx:alpine` to serve the resulting static assets.
*   **`infra/docker/Dockerfile.backend`**: Uses `python:3.11-slim`, installs standard project requirements, and runs `uvicorn backend.app.main:app`.
*   **`infra/docker/Dockerfile.ml_api`**: Also uses `python:3.11-slim`, but runs `uvicorn ml_pipeline.inference.api:app` and copies ML-specific artifacts from `backend/app/ai/artifacts/`.

## Running the Containers

For local development, we merge the base compose and the infra compose files using the start scripts:
```bash
docker-compose -f docker-compose.yml -f infra/docker/docker-compose.yml up --build -d
```
All containers communicate over a shared custom bridge network named `gridwise-net`.
