"""Pydantic schemas for catalogs."""
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime, date
from pydantic import BaseModel, Field
from app.models.catalog import CatalogType


class CatalogBase(BaseModel):
    """Base catalog schema."""
    catalog_code: str = Field(..., min_length=1, max_length=50)
    catalog_name: str = Field(..., min_length=1, max_length=200)
    catalog_type: CatalogType = CatalogType.SIMPLE
    parent_catalog_id: Optional[UUID] = None
    is_system: bool = False
    allow_user_values: bool = False
    cache_enabled: bool = True
    cache_ttl_seconds: int = 3600


class CatalogCreate(CatalogBase):
    """Schema for creating a catalog."""
    pass


class CatalogUpdate(BaseModel):
    """Schema for updating a catalog."""
    catalog_name: Optional[str] = None
    catalog_type: Optional[CatalogType] = None
    parent_catalog_id: Optional[UUID] = None
    allow_user_values: Optional[bool] = None
    cache_enabled: Optional[bool] = None
    cache_ttl_seconds: Optional[int] = None
    is_active: Optional[bool] = None


class CatalogResponse(CatalogBase):
    """Schema for catalog response."""
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CatalogValueBase(BaseModel):
    """Base catalog value schema."""
    value_code: str = Field(..., min_length=1, max_length=100)
    value_name: str = Field(..., min_length=1, max_length=500)
    parent_value_id: Optional[UUID] = None
    dependent_value_id: Optional[UUID] = None
    sort_order: int = 0
    icon_class: Optional[str] = None
    color_hex: Optional[str] = None
    extra_metadata: Optional[dict] = None
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    is_default: bool = False


class CatalogValueCreate(CatalogValueBase):
    """Schema for creating a catalog value."""
    catalog_id: UUID


class CatalogValueUpdate(BaseModel):
    """Schema for updating a catalog value."""
    value_name: Optional[str] = None
    parent_value_id: Optional[UUID] = None
    dependent_value_id: Optional[UUID] = None
    sort_order: Optional[int] = None
    icon_class: Optional[str] = None
    color_hex: Optional[str] = None
    extra_metadata: Optional[dict] = None
    valid_from: Optional[date] = None
    valid_to: Optional[date] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None


class CatalogValueResponse(CatalogValueBase):
    """Schema for catalog value response."""
    id: UUID
    catalog_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
