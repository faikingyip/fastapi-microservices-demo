# import traceback

from fastapi import Request
from fastapi.responses import JSONResponse

from src.errors import CustomError


async def handle_error(request: Request, err: Exception):
    """Middleware to capture exceptions and to standardise the
    shape of the response to be sent back to the client."""

    # tb = "".join(
    #     traceback.format_exception(type(err), err, err.__traceback__),
    # )
    # print(tb)

    if isinstance(err, CustomError):
        serialized = {
            "status_code": err.status_code,
            "content": {"detail": err.detail()},
        }
        return JSONResponse(**serialized)

    return JSONResponse(
        status_code=500,
        content={
            "detail": [
                {
                    "msg": f"Encountered unanticipated exception: {err}",
                }
            ]
        },
    )
