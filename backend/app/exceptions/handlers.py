from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from backend.app.core.logger import get_logger
from backend.app.exceptions.base import BaseAPIException
from backend.app.exceptions.error_codes import ErrorCodes
from backend.app.utils.response import error_response

logger = get_logger("exceptions")


def add_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(BaseAPIException)
    async def base_api_exception_handler(
        request: Request, exc: BaseAPIException
    ) -> JSONResponse:
        logger.warning(
            "api_exception",
            url=str(request.url),
            error_code=exc.error_code,
            message=exc.message,
            status_code=exc.status_code,
            details=exc.details,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(
                code=exc.error_code,
                message=exc.message,
                details=exc.details,
            ).model_dump(exclude_none=True),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        errors = []
        for err in exc.errors():
            loc = err.get("loc", [])
            field = (
                ".".join(str(x) for x in loc[1:])
                if len(loc) > 1
                else (str(loc[0]) if loc else "unknown")
            )
            errors.append(
                {
                    "field": field,
                    "message": err.get("msg", "Invalid value"),
                    "type": err.get("type", "value_error"),
                }
            )

        logger.warning(
            "validation_error",
            url=str(request.url),
            errors=errors,
        )
        return JSONResponse(
            status_code=422,
            content=error_response(
                code=ErrorCodes.VALIDATION_FAILED,
                message="Validation failed",
                details={"errors": errors},
            ).model_dump(exclude_none=True),
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        # Starlette's HTTPException can have standard status codes.
        # Map some common HTTP status codes to custom error codes if needed,
        # otherwise use a generic BAD_REQUEST or HTTP error code.
        error_code = ErrorCodes.BAD_REQUEST
        if exc.status_code == 404:
            # Keep it dynamic or map to EVENT_NOT_FOUND
            error_code = ErrorCodes.EVENT_NOT_FOUND

        logger.warning(
            "http_exception",
            url=str(request.url),
            status_code=exc.status_code,
            message=str(exc.detail),
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(
                code=error_code,
                message=str(exc.detail),
            ).model_dump(exclude_none=True),
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        # Log the full stack trace internally
        logger.error(
            "unhandled_exception",
            url=str(request.url),
            error=str(exc),
            exc_info=True,
        )
        # Sanitized response to client
        return JSONResponse(
            status_code=500,
            content=error_response(
                code=ErrorCodes.INTERNAL_SERVER_ERROR,
                message="An unexpected error occurred",
            ).model_dump(exclude_none=True),
        )
