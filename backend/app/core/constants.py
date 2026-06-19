# Application constants
from enum import Enum

APP_VERSION = "0.1.0"
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100
API_V1_PREFIX = "/api/v1"


class EventSeverity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EventStatus(str, Enum):
    ACTIVE = "active"
    RESOLVING = "resolving"
    RESOLVED = "resolved"
    FALSE_ALARM = "false_alarm"


class CongestionLevel(str, Enum):
    LIGHT = "light"
    MODERATE = "moderate"
    HEAVY = "heavy"
    SEVERE = "severe"


class DeploymentStatus(str, Enum):
    DISPATCHED = "dispatched"
    ON_SCENE = "on_scene"
    RETURNING = "returning"
    AVAILABLE = "available"
