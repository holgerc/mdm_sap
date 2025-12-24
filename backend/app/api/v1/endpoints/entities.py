"""Entity endpoints."""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.models.entity import MDMEntity
from app.schemas.entity import (
    EntityCreate, EntityUpdate, EntityResponse, EntityListResponse
)

router = APIRouter()


@router.post("", response_model=EntityResponse, status_code=status.HTTP_201_CREATED)
async def create_entity(
    entity_data: EntityCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new master data entity."""
    # Check if entity code exists
    result = await db.execute(
        select(MDMEntity).where(MDMEntity.entity_code == entity_data.entity_code)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Entity with code '{entity_data.entity_code}' already exists"
        )

    entity = MDMEntity(**entity_data.model_dump())
    db.add(entity)
    await db.commit()
    await db.refresh(entity)
    return entity


@router.get("", response_model=EntityListResponse)
async def list_entities(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str = Query(None),
    is_active: bool = Query(True),
    db: AsyncSession = Depends(get_db)
):
    """List all master data entities with pagination."""
    # Base query
    query = select(MDMEntity).where(MDMEntity.is_active == is_active)

    # Add search filter
    if search:
        query = query.where(
            (MDMEntity.entity_code.ilike(f"%{search}%")) |
            (MDMEntity.entity_name.ilike(f"%{search}%"))
        )

    # Get total count
    count_result = await db.execute(
        select(func.count()).select_from(query.subquery())
    )
    total = count_result.scalar()

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).order_by(MDMEntity.entity_name)

    result = await db.execute(query)
    entities = result.scalars().all()

    return EntityListResponse(
        items=entities,
        total=total,
        page=page,
        page_size=page_size,
        pages=(total + page_size - 1) // page_size if total > 0 else 0
    )


@router.get("/{entity_id}", response_model=EntityResponse)
async def get_entity(
    entity_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific entity by ID."""
    result = await db.execute(
        select(MDMEntity)
        .options(
            selectinload(MDMEntity.attributes),
            selectinload(MDMEntity.attribute_groups)
        )
        .where(MDMEntity.id == entity_id)
    )
    entity = result.scalar_one_or_none()

    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found"
        )

    return entity


@router.get("/code/{entity_code}", response_model=EntityResponse)
async def get_entity_by_code(
    entity_code: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific entity by code."""
    result = await db.execute(
        select(MDMEntity)
        .options(
            selectinload(MDMEntity.attributes),
            selectinload(MDMEntity.attribute_groups)
        )
        .where(MDMEntity.entity_code == entity_code)
    )
    entity = result.scalar_one_or_none()

    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found"
        )

    return entity


@router.put("/{entity_id}", response_model=EntityResponse)
async def update_entity(
    entity_id: UUID,
    entity_data: EntityUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update an existing entity."""
    result = await db.execute(
        select(MDMEntity).where(MDMEntity.id == entity_id)
    )
    entity = result.scalar_one_or_none()

    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found"
        )

    # Update fields
    update_data = entity_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(entity, field, value)

    await db.commit()
    await db.refresh(entity)
    return entity


@router.delete("/{entity_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_entity(
    entity_id: UUID,
    hard_delete: bool = Query(False),
    db: AsyncSession = Depends(get_db)
):
    """Delete an entity (soft delete by default)."""
    result = await db.execute(
        select(MDMEntity).where(MDMEntity.id == entity_id)
    )
    entity = result.scalar_one_or_none()

    if not entity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found"
        )

    if hard_delete:
        await db.delete(entity)
    else:
        entity.is_active = False

    await db.commit()
