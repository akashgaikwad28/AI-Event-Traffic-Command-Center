from pathlib import Path

PROJECT_NAME = "gridwise-ai"

folders = [
    # Root
    "requirements",
    "docs/architecture",
    "docs/api",
    "docs/ml",
    "docs/deployment",
    "scripts",
    "configs",
    # Infra
    "infra/docker",
    "infra/k8s",
    "infra/terraform",
    # Data
    "data/raw",
    "data/processed",
    "data/interim",
    "data/features",
    "data/external",
    "data/models",
    # Notebook
    "notebooks/eda",
    "notebooks/features",
    "notebooks/training",
    "notebooks/experiments",
    # Backend
    "backend/app/api/v1/endpoints",
    "backend/app/api/v1/schemas",
    "backend/app/core",
    "backend/app/db/models",
    "backend/app/db/repositories",
    "backend/app/db/migrations",
    "backend/app/services",
    # NEW GEO MODULES
    "backend/app/geo",
    # NEW INCIDENT MODULES
    "backend/app/incident_management",
    # NEW RESOURCE OPTIMIZATION
    "backend/app/resource_optimization",
    # NEW ANALYTICS
    "backend/app/analytics",
    # STREAMING
    "backend/app/stream",
    # AI
    "backend/app/ai/pipelines",
    "backend/app/ai/models",
    "backend/app/ai/training",
    "backend/app/ai/inference",
    "backend/app/ai/evaluation",
    "backend/app/ai/features",
    "backend/app/ai/feature_store",
    # Integrations
    "backend/app/integrations",
    # Utils
    "backend/app/utils",
    # Exceptions
    "backend/app/exceptions",
    # Logging
    "backend/app/logs",
    # Monitoring
    "backend/app/monitoring",
    # Tests
    "backend/app/tests/unit",
    "backend/app/tests/integration",
    "backend/app/tests/e2e",
    # Frontend
    "frontend/public",
    "frontend/src/app",
    "frontend/src/pages",
    "frontend/src/components/maps",
    "frontend/src/components/dashboard",
    "frontend/src/components/charts",
    "frontend/src/components/simulation",
    "frontend/src/components/analytics",
    "frontend/src/components/common",
    "frontend/src/services",
    "frontend/src/store",
    "frontend/src/hooks",
    "frontend/src/utils",
    "frontend/src/types",
    "frontend/src/styles",
    # MLOps
    "mlops/mlflow",
    "mlops/model_registry",
    "mlops/drift_detection",
    # Monitoring Stack
    "monitoring/grafana",
    "monitoring/prometheus",
    "monitoring/loki",
]

files = [
    # Root
    "README.md",
    ".env",
    ".env.example",
    ".gitignore",
    "docker-compose.yml",
    "pyproject.toml",
    "Makefile",
    # Config
    "configs/settings.yaml",
    "configs/logging.yaml",
    # Requirements
    "requirements/base.txt",
    "requirements/dev.txt",
    "requirements/prod.txt",
    # Backend Core
    "backend/app/main.py",
    "backend/app/core/config.py",
    "backend/app/core/logger.py",
    "backend/app/core/constants.py",
    "backend/app/core/security.py",
    "backend/app/core/middleware.py",
    # API
    "backend/app/api/router.py",
    "backend/app/api/v1/endpoints/events.py",
    "backend/app/api/v1/endpoints/predictions.py",
    "backend/app/api/v1/endpoints/analytics.py",
    "backend/app/api/v1/endpoints/deployments.py",
    "backend/app/api/v1/endpoints/simulation.py",
    # Services
    "backend/app/services/event_service.py",
    "backend/app/services/prediction_service.py",
    "backend/app/services/recommendation_service.py",
    # GEO
    "backend/app/geo/spatial_engine.py",
    "backend/app/geo/hotspot_detection.py",
    "backend/app/geo/route_impact.py",
    # Incident
    "backend/app/incident_management/incident_service.py",
    "backend/app/incident_management/lifecycle_tracker.py",
    "backend/app/incident_management/sla_monitor.py",
    # Resource Optimization
    "backend/app/resource_optimization/police_allocator.py",
    "backend/app/resource_optimization/barricade_optimizer.py",
    "backend/app/resource_optimization/diversion_engine.py",
    # Analytics
    "backend/app/analytics/congestion_analytics.py",
    "backend/app/analytics/zone_analytics.py",
    "backend/app/analytics/response_time_analytics.py",
    # Streaming
    "backend/app/stream/realtime_ingestion.py",
    "backend/app/stream/websocket_manager.py",
    # AI
    "backend/app/ai/pipelines/training_pipeline.py",
    "backend/app/ai/pipelines/inference_pipeline.py",
    "backend/app/ai/features/feature_engineering.py",
    # Exceptions
    "backend/app/exceptions/base.py",
    "backend/app/exceptions/handlers.py",
    # Utils
    "backend/app/utils/geo_utils.py",
    "backend/app/utils/time_utils.py",
    # Logging
    "backend/app/logs/app.log",
    "backend/app/logs/error.log",
]

root = Path(PROJECT_NAME)

for folder in folders:
    path = root / folder
    path.mkdir(parents=True, exist_ok=True)

    if "frontend" not in str(path):
        init_file = path / "__init__.py"
        init_file.touch(exist_ok=True)

for file in files:
    file_path = root / file
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if not file_path.exists():
        file_path.touch()

print(f"✅ Enterprise AI Traffic Platform structure created at: {PROJECT_NAME}")
