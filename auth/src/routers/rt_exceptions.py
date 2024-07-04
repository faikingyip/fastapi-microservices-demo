from typing import Optional

from fastapi import HTTPException, status

# def create_bad_request_exception(detail: str):
#     # Produces not found response.
#     return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


def create_item_not_found_exception(message: Optional[str] = None):
    # Produces not found response.
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=message or "Item not found"
    )


def create_validation_errors_exception(message: Optional[str] = None):
    # Produces not found response.
    return HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=message
    )
