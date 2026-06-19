from backend.app.exceptions.api_exceptions import (
    CongestionDataNotFound,
    DatabaseOperationFailed,
    EventNotFound,
    InvalidCoordinates,
    InvalidPaginationParams,
    PredictionFailed,
    ResourceConflict,
    ValidationFailed,
)
from backend.app.exceptions.base import BaseAPIException
from backend.app.exceptions.error_codes import ErrorCodes
from backend.app.exceptions.handlers import add_exception_handlers

__all__ = [
    "BaseAPIException",
    "ErrorCodes",
    "add_exception_handlers",
    "EventNotFound",
    "InvalidCoordinates",
    "PredictionFailed",
    "DatabaseOperationFailed",
    "InvalidPaginationParams",
    "CongestionDataNotFound",
    "ResourceConflict",
    "ValidationFailed",
]
