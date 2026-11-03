"""Custom exceptions and FastAPI exception handlers."""

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class DocumentNotFoundError(Exception):
    """Raised when a requested document doesn't exist."""

    def __init__(self, document_id: int) -> None:
        self.document_id = document_id
        super().__init__(f"Document {document_id} not found")


async def document_not_found_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, DocumentNotFoundError)

    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "code": "document_not_found",
                "message": str(exc),
                "details": {"document_id": exc.document_id},
            }
        },
    )


async def http_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, HTTPException)

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "http_error",
                "message": str(exc.detail),
                "details": None,
            }
        },
        headers=exc.headers,
    )


async def validation_exception_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "validation_error",
                "message": "Request validation failed",
                "details": exc.errors(),
            }
        },
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom exception handlers."""

    app.add_exception_handler(
        DocumentNotFoundError,
        document_not_found_handler,
    )

    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_exception_handler,
    )