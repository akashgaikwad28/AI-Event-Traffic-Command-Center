# Project Structure

GridWise AI follows a modular, scalable monolithic architecture. This structure ensures clear separation of concerns across the frontend, backend, AI pipelines, and infrastructure.

## Root Directories

- `backend/`: FastAPI application code. Contains controllers, business services, repositories, and WebSocket endpoints.
- `frontend/`: React + Vite frontend code. Includes Zustand for state management and TailwindCSS for styling.
- `data/`: Local data directory. Used for storing intermediate datasets (typically ignored in git, managed via DVC).
- `data_pipeline/`: Data ingestion and cleaning scripts for processing event and traffic metadata.
- `ml_pipeline/`: Machine learning model training and inference pipelines.
- `mlops/`: DagsHub and MLflow related configurations for experiment tracking.
- `infra/`: Infrastructure as Code. Includes Dockerfiles, docker-compose configurations, and deployment manifests.
- `notebooks/`: Jupyter notebooks for exploratory data analysis, prototyping, and algorithm testing.
- `scripts/`: Utility, scaffolding, and automation scripts.
- `tests/`: Automated test suite for the backend, frontend, and ML pipelines.
- `configs/`: Application and environment configuration files.
- `docs/`: Project documentation, architecture diagrams, and guidelines.
- `reports/`: Generated analytics, execution summaries, or pipeline outputs.
- `logs/`: Application execution logs for both backend and data pipelines.

## Key Files

- `README.md`: The main entry point for understanding the project, features, and quickstart instructions.
- `CONTRIBUTING.md`: Guidelines for community contributions.
- `CODE_OF_CONDUCT.md`: The rules and standards for participation in the community.
- `docker-compose.yml`: Orchestrates the local development environment containing the backend, frontend, and any necessary databases.
- `pyproject.toml` / `requirements.txt`: Python backend and data pipeline dependencies.
- `Makefile`: Convenient shortcuts for common tasks like testing, building, and running the application.
