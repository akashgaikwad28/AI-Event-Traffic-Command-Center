# Environment Configuration

This document outlines the environment variables required to run Gridwise AI. The default setup relies on a `.env` file at the root of the project.

## Core Application Settings
* **`APP_NAME`**: Name of the application (e.g., `Gridwise AI`)
* **`APP_ENV`**: Environment mode, such as `development`, `staging`, or `production`.
* **`DEBUG`**: Enable debug mode for the application (`True` or `False`).
* **`API_V1_PREFIX`**: Prefix for the API endpoints (default: `/api/v1`).
* **`LOG_LEVEL`**: Logging detail level (e.g., `INFO`, `DEBUG`).

## Database Configuration (PostgreSQL / PostGIS)
* **`POSTGRES_HOST`**: Hostname for the Postgres database (e.g., `postgres` for Docker).
* **`POSTGRES_PORT`**: Port for Postgres (default: `5432`).
* **`POSTGRES_DB`**: Name of the database (e.g., `gridwise`).
* **`POSTGRES_USER`**: Postgres user.
* **`POSTGRES_PASSWORD`**: Postgres password.

## Redis Configuration
* **`REDIS_HOST`**: Hostname for the Redis server (e.g., `redis` for Docker).
* **`REDIS_PORT`**: Port for Redis (default: `6379`).

## Service Communication
* **`ML_API_URL`**: Endpoint for the internal ML API service (e.g., `http://ml-api:8001`).
* **`FRONTEND_URL`**: Public URL for the frontend application (e.g., `http://localhost:80`).

## External Integrations
* **`DAGSHUB_USER_TOKEN`**: Required for downloading models and datasets via DVC during build (used in `render_build.sh`).
