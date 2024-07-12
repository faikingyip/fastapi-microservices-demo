import time

from fastapi import Request


async def request_duration(request: Request, call_next):
    """Add a middleware to take the duration of a request
    and attach it to the header of the response."""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers["duration"] = str(duration)
    return response
