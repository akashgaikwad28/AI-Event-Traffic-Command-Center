from typing import Any


class StreamStateCache:
    """
    In-memory state cache to prevent recomputing expensive analytics repeatedly.
    """

    def __init__(self):
        self._gori_cache: float = 0.0
        self._active_incidents: dict[str, Any] = {}
        self._hotspot_cache: list = []

    def update_gori(self, new_score: float):
        self._gori_cache = new_score

    def get_latest_gori(self) -> float:
        return self._gori_cache

    def add_incident(self, incident_id: str, data: Any):
        self._active_incidents[incident_id] = data

    def get_active_count(self) -> int:
        return len(self._active_incidents)

    def update_hotspots(self, hotspots: list):
        self._hotspot_cache = hotspots

    def get_snapshot(self) -> dict[str, Any]:
        return {
            "avg_gori": self._gori_cache,
            "active_incidents": len(self._active_incidents),
            "top_hotspots": self._hotspot_cache,
        }


# Singleton Cache
stream_cache = StreamStateCache()
