from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    status: str
    uptime: str
    version: str
    services: dict[str, str]
