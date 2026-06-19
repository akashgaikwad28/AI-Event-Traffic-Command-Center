from typing import Any

from backend.app.exceptions.base import BaseAPIException
from backend.app.exceptions.error_codes import ErrorCodes


class EventNotFound(BaseAPIException):
    def __init__(self, message: str = "Event not found", details: Any = None):
        super().__init__(
            message=message,
            error_code=ErrorCodes.EVENT_NOT_FOUND,
            status_code=404,
            details=details,
        )


class InvalidCoordinates(BaseAPIException):
    def __init__(
        self, message: str = "Invalid coordinates provided", details: Any = None
    ):
        super().__init__(
            message=message,
            error_code=ErrorCodes.INVALID_COORDINATES,
            status_code=400,
            details=details,
        )


class PredictionFailed(BaseAPIException):
    def __init__(
        self, message: str = "Prediction calculation failed", details: Any = None
    ):
        super().__init__(
            message=message,
            error_code=ErrorCodes.PREDICTION_FAILED,
            status_code=500,
            details=details,
        )


class DatabaseOperationFailed(BaseAPIException):
    def __init__(self, message: str = "Database operation failed", details: Any = None):
        super().__init__(
            message=message,
            error_code=ErrorCodes.DATABASE_OPERATION_FAILED,
            status_code=500,
            details=details,
        )


class InvalidPaginationParams(BaseAPIException):
    def __init__(
        self, message: str = "Invalid pagination parameters", details: Any = None
    ):
        super().__init__(
            message=message,
            error_code=ErrorCodes.INVALID_PAGINATION_PARAMS,
            status_code=400,
            details=details,
        )


class CongestionDataNotFound(BaseAPIException):
    def __init__(self, message: str = "Congestion data not found", details: Any = None):
        super().__init__(
            message=message,
            error_code=ErrorCodes.CONGESTION_DATA_NOT_FOUND,
            status_code=404,
            details=details,
        )


class ResourceConflict(BaseAPIException):
    def __init__(self, message: str = "Resource state conflict", details: Any = None):
        super().__init__(
            message=message,
            error_code=ErrorCodes.RESOURCE_CONFLICT,
            status_code=409,
            details=details,
        )


class ValidationFailed(BaseAPIException):
    def __init__(self, message: str = "Validation failed", details: Any = None):
        super().__init__(
            message=message,
            error_code=ErrorCodes.VALIDATION_FAILED,
            status_code=400,
            details=details,
        )


class GeoProcessingFailed(BaseAPIException):
    def __init__(self, message: str = "Geo processing failed", details: Any = None):
        super().__init__(
            message=message,
            error_code=ErrorCodes.GEO_PROCESSING_FAILED,
            status_code=500,
            details=details,
        )


class HotspotDetectionFailed(BaseAPIException):
    def __init__(self, message: str = "Hotspot detection failed", details: Any = None):
        super().__init__(
            message=message,
            error_code=ErrorCodes.HOTSPOT_DETECTION_FAILED,
            status_code=500,
            details=details,
        )


class ModelLoadingFailed(BaseAPIException):
    def __init__(self, message: str = "Model loading failed", details: Any = None):
        super().__init__(
            message=message,
            error_code=ErrorCodes.MODEL_LOADING_FAILED,
            status_code=500,
            details=details,
        )


class InferenceFailed(BaseAPIException):
    def __init__(self, message: str = "Inference failed", details: Any = None):
        super().__init__(
            message=message,
            error_code=ErrorCodes.INFERENCE_FAILED,
            status_code=500,
            details=details,
        )


class FeatureValidationFailed(BaseAPIException):
    def __init__(self, message: str = "Feature validation failed", details: Any = None):
        super().__init__(
            message=message,
            error_code=ErrorCodes.FEATURE_VALIDATION_FAILED,
            status_code=400,
            details=details,
        )


class ArtifactNotFound(BaseAPIException):
    def __init__(self, message: str = "ML artifact not found", details: Any = None):
        super().__init__(
            message=message,
            error_code=ErrorCodes.ARTIFACT_NOT_FOUND,
            status_code=500,
            details=details,
        )


class GORIComputationFailed(BaseAPIException):
    def __init__(self, message: str = "GORI computation failed", details: Any = None):
        super().__init__(
            message=message,
            error_code=ErrorCodes.GORI_COMPUTATION_FAILED,
            status_code=500,
            details=details,
        )
