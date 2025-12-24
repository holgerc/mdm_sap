"""Pydantic schemas for entities."""
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.entity import AuditLevel


class EntityBase(BaseModel):
    """Base entity schema."""
    entity_code: str = Field(..., min_length=1, max_length=50)
    entity_name: str = Field(..., min_length=1, max_length=200)
    entity_description: Optional[str] = None
    icon_class: Optional[str] = None
    color_hex: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')
    is_hierarchical: bool = False
    max_hierarchy_levels: int = 5
    allow_versioning: bool = True
    retention_days: int = 365
    audit_level: AuditLevel = AuditLevel.BASIC
    workflow_enabled: bool = False
    default_workflow_id: Optional[UUID] = None


class EntityCreate(EntityBase):
    """Schema for creating an entity."""
    pass


class EntityUpdate(BaseModel):
    """Schema for updating an entity."""
    entity_name: Optional[str] = None
    entity_description: Optional[str] = None
    icon_class: Optional[str] = None
    color_hex: Optional[str] = None
    is_hierarchical: Optional[bool] = None
    max_hierarchy_levels: Optional[int] = None
    allow_versioning: Optional[bool] = None
    retention_days: Optional[int] = None
    audit_level: Optional[AuditLevel] = None
    workflow_enabled: Optional[bool] = None
    default_workflow_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class EntityResponse(EntityBase):
    """Schema for entity response."""
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EntityListResponse(BaseModel):
    """Schema for paginated entity list."""
    items: List[EntityResponse]
    total: int
    page: int
    page_size: int
    pages: int
