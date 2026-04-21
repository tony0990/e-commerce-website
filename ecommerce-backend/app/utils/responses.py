"""
Response Utilities (Tony)
==========================
Helper functions for creating standardized API responses.
"""

from typing import Any, Optional, List
from fastapi.responses import JSONResponse
from app.schemas.common import PaginationMeta
import math


def success_response(
    data: Any = None,
    message: str = "Success",
    status_code: int = 200,
) -> JSONResponse:
    """Create a standardized success response."""
    content = {
        "success": True,
        "message": message,
    }
    if data is not None:
        content["data"] = data
    return JSONResponse(content=content, status_code=status_code)


def error_response(
    message: str = "An error occurred",
    status_code: int = 400,
    error_code: Optional[str] = None,
) -> JSONResponse:
    """Create a standardized error response."""
    content = {
        "success": False,
        "detail": message,
    }
    if error_code:
        content["error_code"] = error_code
    return JSONResponse(content=content, status_code=status_code)


def paginated_response(
    data: List[Any],
    total: int,
    page: int,
    page_size: int,
    message: str = "Success",
) -> dict:
    """Create a standardized paginated response."""
    total_pages = math.ceil(total / page_size) if page_size > 0 else 0
    return {
        "success": True,
        "message": message,
        "data": data,
        "pagination": {
            "current_page": page,
            "page_size": page_size,
            "total_items": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1,
        },
    }
