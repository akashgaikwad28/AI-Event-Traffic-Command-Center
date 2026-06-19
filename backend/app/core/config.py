from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Gridwise AI"
    version: str = "0.1.0"
    description: str = "GRIDWISE AI Platform Foundation"
    app_env: Literal["development", "production", "testing"] = "development"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    cors_origins: list[str] = ["*"]

    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "gridwise"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"

    redis_host: str = "redis"
    redis_port: int = 6379

    log_level: str = "INFO"

    geo_cluster_eps_km: float = 0.5
    geo_min_cluster_samples: int = 4
    geo_max_impact_radius_km: float = 2.0
    geo_hotspot_risk_multiplier: float = 1.0

    # AI Inference Config
    ai_artifacts_dir: str = "backend/app/ai/artifacts"
    ai_model_version: str = "1.0"

    # GORI Weights (must sum to 1.0)
    gori_weight_congestion: float = 0.25
    gori_weight_hotspot: float = 0.20
    gori_weight_rush_hour: float = 0.15
    gori_weight_cascading: float = 0.20
    gori_weight_deployment: float = 0.20

    # Confidence Thresholds
    confidence_high_threshold: float = 0.75
    confidence_medium_threshold: float = 0.45

    # Deployment Level Boundaries
    deployment_medium_threshold: float = 2.5
    deployment_high_threshold: float = 5.0
    deployment_critical_threshold: float = 7.5

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
