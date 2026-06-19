from datetime import UTC, datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field, ConfigDict

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(frozen=True)
    success: bool
    data: T | None = None
    message: str | None = None
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


class ErrorDetail(BaseModel):
    model_config = ConfigDict(frozen=True)
    code: str
    message: str
    details: Any = None


class APIErrorResponse(BaseModel):
    model_config = ConfigDict(frozen=True)
    success: bool = False
    error: ErrorDetail
    timestamp: str = Field(default_factory=lambda: datetime.now(UTC).isoformat())


def success_response(data: Any = None, message: str | None = None) -> APIResponse[Any]:
    return APIResponse(success=True, data=data, message=message)


def error_response(code: str, message: str, details: Any = None) -> APIErrorResponse:
    return APIErrorResponse(
        success=False,
        error=ErrorDetail(code=code, message=message, details=details),
    )
