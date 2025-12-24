"""Common Pydantic schemas."""
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response schema."""
    items: List[T]
    total: int
    page: int
    page_size: int
    pages: int


class HealthResponse(BaseModel):
    """Health check response schema."""
    status: str
    version: str
    database: str
    redis: Optional[str] = None


class MessageResponse(BaseModel):
    """Generic message response schema."""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
    error_code: Optional[str] = None
