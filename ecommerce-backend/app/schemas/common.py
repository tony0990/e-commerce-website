"""
Common Schemas (Tony)
======================
Shared Pydantic schemas used across the application.
Includes standard response wrappers and pagination.
"""

from typing import Optional, Any, List, Generic, TypeVar
from pydantic import BaseModel
from datetime import datetime

T = TypeVar("T")


class MessageResponse(BaseModel):
    """Standard message response."""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
    error_code: Optional[str] = None
    success: bool = False


class DataResponse(BaseModel):
    """Standard data response wrapper."""
    data: Any
    message: str = "Success"
    success: bool = True


class PaginationMeta(BaseModel):
    """Pagination metadata."""
    current_page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool


class PaginatedResponse(BaseModel):
    """Paginated list response."""
    data: List[Any]
    pagination: PaginationMeta
    message: str = "Success"
    success: bool = True


class HealthCheckResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str
    environment: str
    timestamp: datetime
