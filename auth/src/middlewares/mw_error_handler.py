from fastapi import Request
from fastapi.responses import JSONResponse

from src.errors import AppServiceError, BusinessValidationError


# @app.exception_handler(Exception)
async def handle_error(request: Request, exc: Exception):
    """Middleware to capture exceptions and to standardise the
    shape of the response to be sent back to the client."""

    if isinstance(exc, AppServiceError):
        return JSONResponse(
            status_code=500,
            content={"message": "Something went wrong."},
        )

    if isinstance(exc, BusinessValidationError):
        return JSONResponse(
            status_code=400,
            content={"message": "This is a business logic validation error."},
        )

    return JSONResponse(
        status_code=500,
        content={"message": "Something went wrong."},
    )
