# Deployment Guide

This guide details how to build, run, and deploy the Gridwise AI platform.

## Local Development Deployment

To start the entire stack locally for development:

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd gridwise-ai
   ```

2. **Environment Variables**:
   Copy the example environment variables file to `.env`:
   ```bash
   cp .env.example .env
   ```

3. **Start the Platform**:
   Use the provided startup scripts which handle copying the `.env` file and running the proper `docker-compose` commands.
   *   **On Windows**: Run `scripts\start_dev.bat`
   *   **On Linux / macOS**: Run `scripts/start_dev.sh`

   These scripts will spin up the database (PostGIS), Redis, Backend, ML API, and Frontend.

4. **Access the Services**:
   *   **Frontend**: `http://localhost:80`
   *   **Backend API**: `http://localhost:8000`
   *   **ML API**: `http://localhost:8001`

## Render / Cloud Deployment

Gridwise AI includes a build script (`scripts/render_build.sh`) designed for cloud deployments such as Render. 

This script performs the following critical steps:
1. **Installs Dependencies**: Runs `pip install -r requirements.txt`.
2. **Configures Writable Directories**: Sets temporary folders for DVC to avoid read-only filesystem errors in cloud environments.
3. **Authenticates DVC**: Uses the `DAGSHUB_USER_TOKEN` environment variable to securely authenticate with DagsHub.
4. **Pulls Artifacts**: Executes `dvc pull -r origin` to download the trained ML models and datasets needed for the `ml-api` to function correctly.

Ensure that `DAGSHUB_USER_TOKEN` is set as a secret in your cloud provider environment before deploying.
