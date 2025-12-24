"""Pydantic schemas for attributes."""
from typing import Optional, List, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.attribute import (
    DataType, UIComponent, ValidationType, Severity,
    TransformType, ApplyOn, DisplayType
)


class AttributeGroupBase(BaseModel):
    """Base attribute group schema."""
    group_code: str = Field(..., min_length=1, max_length=100)
    group_name: str = Field(..., min_length=1, max_length=200)
    group_icon: Optional[str] = None
    display_type: DisplayType = DisplayType.SECTION
    sort_order: int = 0
    is_collapsible: bool = True
    default_collapsed: bool = False
    visibility_condition: Optional[str] = None


class AttributeGroupCreate(AttributeGroupBase):
    """Schema for creating an attribute group."""
    entity_id: UUID


class AttributeGroupResponse(AttributeGroupBase):
    """Schema for attribute group response."""
    id: UUID
    entity_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AttributeBase(BaseModel):
    """Base attribute schema."""
    attribute_code: str = Field(..., min_length=1, max_length=100)
    attribute_name: str = Field(..., min_length=1, max_length=200)
    attribute_group_id: Optional[UUID] = None
    data_type: DataType
    ui_component: UIComponent = UIComponent.TEXT
    display_order: int = 0
    is_required: bool = False
    is_unique: bool = False
    is_searchable: bool = True
    is_filterable: bool = True
    is_sortable: bool = True
    show_in_list: bool = True
    show_in_detail: bool = True
    is_readonly: bool = False
    is_hidden: bool = False
    is_encrypted: bool = False
    is_pii: bool = False
    default_value: Optional[str] = None
    placeholder: Optional[str] = None
    help_text: Optional[str] = None
    tooltip: Optional[str] = None
    catalog_id: Optional[UUID] = None


class AttributeCreate(AttributeBase):
    """Schema for creating an attribute."""
    entity_id: UUID


class AttributeUpdate(BaseModel):
    """Schema for updating an attribute."""
    attribute_name: Optional[str] = None
    attribute_group_id: Optional[UUID] = None
    ui_component: Optional[UIComponent] = None
    display_order: Optional[int] = None
    is_required: Optional[bool] = None
    is_unique: Optional[bool] = None
    is_searchable: Optional[bool] = None
    is_filterable: Optional[bool] = None
    is_sortable: Optional[bool] = None
    show_in_list: Optional[bool] = None
    show_in_detail: Optional[bool] = None
    is_readonly: Optional[bool] = None
    is_hidden: Optional[bool] = None
    is_encrypted: Optional[bool] = None
    is_pii: Optional[bool] = None
    default_value: Optional[str] = None
    placeholder: Optional[str] = None
    help_text: Optional[str] = None
    tooltip: Optional[str] = None
    catalog_id: Optional[UUID] = None
    is_active: Optional[bool] = None


class AttributeResponse(AttributeBase):
    """Schema for attribute response."""
    id: UUID
    entity_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ValidationBase(BaseModel):
    """Base validation schema."""
    validation_type: ValidationType
    validation_rule: Optional[str] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    regex_pattern: Optional[str] = None
    allowed_values: Optional[List[Any]] = None
    forbidden_values: Optional[List[Any]] = None
    custom_function: Optional[str] = None
    api_endpoint: Optional[str] = None
    error_message: Optional[str] = None
    error_code: Optional[str] = None
    severity: Severity = Severity.ERROR
    execution_order: int = 0


class ValidationCreate(ValidationBase):
    """Schema for creating a validation."""
    attribute_id: UUID


class ValidationResponse(ValidationBase):
    """Schema for validation response."""
    id: UUID
    attribute_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TransformBase(BaseModel):
    """Base transform schema."""
    transform_type: TransformType
    transform_config: Optional[dict] = None
    apply_on: ApplyOn = ApplyOn.INPUT
    execution_order: int = 0
    condition_expression: Optional[str] = None


class TransformCreate(TransformBase):
    """Schema for creating a transform."""
    attribute_id: UUID


class TransformResponse(TransformBase):
    """Schema for transform response."""
    id: UUID
    attribute_id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
