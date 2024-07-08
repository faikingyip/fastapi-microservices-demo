from fastapi import Request
from fastapi.responses import JSONResponse
from src.errors import CustomError


async def handle_error(request: Request, err: Exception):
    """Middleware to capture exceptions and to standardise the
    shape of the response to be sent back to the client."""

    if isinstance(err, CustomError):
        return JSONResponse(**err.serialize())

    return JSONResponse(
        status_code=500,
        content={
            "detail": [
                {
                    "msg": "Something went wrong.",
                }
            ]
        },
    )
