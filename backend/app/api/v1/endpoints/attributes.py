"""Attribute endpoints."""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.attribute import MDMAttribute, MDMAttributeGroup, MDMAttributeValidation, MDMAttributeTransform
from app.schemas.attribute import (
    AttributeCreate, AttributeUpdate, AttributeResponse,
    AttributeGroupCreate, AttributeGroupResponse,
    ValidationCreate, ValidationResponse,
    TransformCreate, TransformResponse
)

router = APIRouter()


# Attribute Groups
@router.post("/groups", response_model=AttributeGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_attribute_group(
    group_data: AttributeGroupCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new attribute group."""
    group = MDMAttributeGroup(**group_data.model_dump())
    db.add(group)
    await db.commit()
    await db.refresh(group)
    return group


@router.get("/groups", response_model=List[AttributeGroupResponse])
async def list_attribute_groups(
    entity_id: UUID = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """List attribute groups."""
    query = select(MDMAttributeGroup).where(MDMAttributeGroup.is_active == True)
    if entity_id:
        query = query.where(MDMAttributeGroup.entity_id == entity_id)
    query = query.order_by(MDMAttributeGroup.sort_order)

    result = await db.execute(query)
    return result.scalars().all()


# Attributes
@router.post("", response_model=AttributeResponse, status_code=status.HTTP_201_CREATED)
async def create_attribute(
    attribute_data: AttributeCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new attribute."""
    # Check uniqueness within entity
    result = await db.execute(
        select(MDMAttribute).where(
            MDMAttribute.entity_id == attribute_data.entity_id,
            MDMAttribute.attribute_code == attribute_data.attribute_code
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Attribute with code '{attribute_data.attribute_code}' already exists for this entity"
        )

    attribute = MDMAttribute(**attribute_data.model_dump())
    db.add(attribute)
    await db.commit()
    await db.refresh(attribute)
    return attribute


@router.get("", response_model=List[AttributeResponse])
async def list_attributes(
    entity_id: UUID = Query(None),
    group_id: UUID = Query(None),
    is_searchable: bool = Query(None),
    is_filterable: bool = Query(None),
    show_in_list: bool = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """List attributes with optional filters."""
    query = select(MDMAttribute).where(MDMAttribute.is_active == True)

    if entity_id:
        query = query.where(MDMAttribute.entity_id == entity_id)
    if group_id:
        query = query.where(MDMAttribute.attribute_group_id == group_id)
    if is_searchable is not None:
        query = query.where(MDMAttribute.is_searchable == is_searchable)
    if is_filterable is not None:
        query = query.where(MDMAttribute.is_filterable == is_filterable)
    if show_in_list is not None:
        query = query.where(MDMAttribute.show_in_list == show_in_list)

    query = query.order_by(MDMAttribute.display_order)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{attribute_id}", response_model=AttributeResponse)
async def get_attribute(
    attribute_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific attribute."""
    result = await db.execute(
        select(MDMAttribute).where(MDMAttribute.id == attribute_id)
    )
    attribute = result.scalar_one_or_none()

    if not attribute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attribute not found"
        )

    return attribute


@router.put("/{attribute_id}", response_model=AttributeResponse)
async def update_attribute(
    attribute_id: UUID,
    attribute_data: AttributeUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an attribute."""
    result = await db.execute(
        select(MDMAttribute).where(MDMAttribute.id == attribute_id)
    )
    attribute = result.scalar_one_or_none()

    if not attribute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attribute not found"
        )

    update_data = attribute_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(attribute, field, value)

    await db.commit()
    await db.refresh(attribute)
    return attribute


@router.delete("/{attribute_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_attribute(
    attribute_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete an attribute (soft delete)."""
    result = await db.execute(
        select(MDMAttribute).where(MDMAttribute.id == attribute_id)
    )
    attribute = result.scalar_one_or_none()

    if not attribute:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attribute not found"
        )

    attribute.is_active = False
    await db.commit()


# Validations
@router.post("/{attribute_id}/validations", response_model=ValidationResponse, status_code=status.HTTP_201_CREATED)
async def create_validation(
    attribute_id: UUID,
    validation_data: ValidationCreate,
    db: AsyncSession = Depends(get_db)
):
    """Add a validation rule to an attribute."""
    validation = MDMAttributeValidation(
        attribute_id=attribute_id,
        **validation_data.model_dump(exclude={'attribute_id'})
    )
    db.add(validation)
    await db.commit()
    await db.refresh(validation)
    return validation


@router.get("/{attribute_id}/validations", response_model=List[ValidationResponse])
async def list_validations(
    attribute_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """List validations for an attribute."""
    result = await db.execute(
        select(MDMAttributeValidation)
        .where(
            MDMAttributeValidation.attribute_id == attribute_id,
            MDMAttributeValidation.is_active == True
        )
        .order_by(MDMAttributeValidation.execution_order)
    )
    return result.scalars().all()


# Transforms
@router.post("/{attribute_id}/transforms", response_model=TransformResponse, status_code=status.HTTP_201_CREATED)
async def create_transform(
    attribute_id: UUID,
    transform_data: TransformCreate,
    db: AsyncSession = Depends(get_db)
):
    """Add a transformation rule to an attribute."""
    transform = MDMAttributeTransform(
        attribute_id=attribute_id,
        **transform_data.model_dump(exclude={'attribute_id'})
    )
    db.add(transform)
    await db.commit()
    await db.refresh(transform)
    return transform


@router.get("/{attribute_id}/transforms", response_model=List[TransformResponse])
async def list_transforms(
    attribute_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """List transformations for an attribute."""
    result = await db.execute(
        select(MDMAttributeTransform)
        .where(
            MDMAttributeTransform.attribute_id == attribute_id,
            MDMAttributeTransform.is_active == True
        )
        .order_by(MDMAttributeTransform.execution_order)
    )
    return result.scalars().all()
