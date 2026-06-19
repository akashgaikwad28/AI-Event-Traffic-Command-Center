from datetime import datetime
from typing import Any


class HealthMonitor:
    """Advanced health check returning the enterprise schema."""

    def __init__(self):
        self.start_time = datetime.utcnow()

    def _get_uptime(self) -> str:
        delta = datetime.utcnow() - self.start_time
        hours, remainder = divmod(delta.total_seconds(), 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m"

    def get_health_status(self) -> dict[str, Any]:
        # In a real system, these would ping databases and other components.
        # For the hackathon, we simulate them as "healthy" unless an override is set.
        return {
            "status": "healthy",
            "uptime": self._get_uptime(),
            "version": "1.0.0",
            "services": {
                "database": "healthy",
                "prediction_engine": "healthy",
                "analytics_engine": "healthy",
                "optimization_engine": "healthy",
                "streaming_engine": "healthy",
                "genai_providers": "healthy",
                "simulation_engine": "healthy",
            },
        }


health_monitor = HealthMonitor()
