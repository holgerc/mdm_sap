"""Catalog endpoints."""
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.database import get_db
from app.models.catalog import MDMCatalog, MDMCatalogValue
from app.schemas.catalog import (
    CatalogCreate, CatalogUpdate, CatalogResponse,
    CatalogValueCreate, CatalogValueUpdate, CatalogValueResponse
)

router = APIRouter()


# Catalogs
@router.post("", response_model=CatalogResponse, status_code=status.HTTP_201_CREATED)
async def create_catalog(
    catalog_data: CatalogCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new catalog."""
    # Check if catalog code exists
    result = await db.execute(
        select(MDMCatalog).where(MDMCatalog.catalog_code == catalog_data.catalog_code)
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Catalog with code '{catalog_data.catalog_code}' already exists"
        )

    catalog = MDMCatalog(**catalog_data.model_dump())
    db.add(catalog)
    await db.commit()
    await db.refresh(catalog)
    return catalog


@router.get("", response_model=List[CatalogResponse])
async def list_catalogs(
    is_system: bool = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """List all catalogs."""
    query = select(MDMCatalog).where(MDMCatalog.is_active == True)

    if is_system is not None:
        query = query.where(MDMCatalog.is_system == is_system)

    query = query.order_by(MDMCatalog.catalog_name)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{catalog_id}", response_model=CatalogResponse)
async def get_catalog(
    catalog_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific catalog."""
    result = await db.execute(
        select(MDMCatalog)
        .options(selectinload(MDMCatalog.values))
        .where(MDMCatalog.id == catalog_id)
    )
    catalog = result.scalar_one_or_none()

    if not catalog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catalog not found"
        )

    return catalog


@router.get("/code/{catalog_code}", response_model=CatalogResponse)
async def get_catalog_by_code(
    catalog_code: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a catalog by code."""
    result = await db.execute(
        select(MDMCatalog)
        .options(selectinload(MDMCatalog.values))
        .where(MDMCatalog.catalog_code == catalog_code)
    )
    catalog = result.scalar_one_or_none()

    if not catalog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catalog not found"
        )

    return catalog


@router.put("/{catalog_id}", response_model=CatalogResponse)
async def update_catalog(
    catalog_id: UUID,
    catalog_data: CatalogUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a catalog."""
    result = await db.execute(
        select(MDMCatalog).where(MDMCatalog.id == catalog_id)
    )
    catalog = result.scalar_one_or_none()

    if not catalog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catalog not found"
        )

    if catalog.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="System catalogs cannot be modified"
        )

    update_data = catalog_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(catalog, field, value)

    await db.commit()
    await db.refresh(catalog)
    return catalog


@router.delete("/{catalog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_catalog(
    catalog_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a catalog (soft delete)."""
    result = await db.execute(
        select(MDMCatalog).where(MDMCatalog.id == catalog_id)
    )
    catalog = result.scalar_one_or_none()

    if not catalog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catalog not found"
        )

    if catalog.is_system:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="System catalogs cannot be deleted"
        )

    catalog.is_active = False
    await db.commit()


# Catalog Values
@router.post("/{catalog_id}/values", response_model=CatalogValueResponse, status_code=status.HTTP_201_CREATED)
async def create_catalog_value(
    catalog_id: UUID,
    value_data: CatalogValueCreate,
    db: AsyncSession = Depends(get_db)
):
    """Add a value to a catalog."""
    # Verify catalog exists
    result = await db.execute(
        select(MDMCatalog).where(MDMCatalog.id == catalog_id)
    )
    catalog = result.scalar_one_or_none()
    if not catalog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catalog not found"
        )

    # Check for duplicate value code
    result = await db.execute(
        select(MDMCatalogValue).where(
            MDMCatalogValue.catalog_id == catalog_id,
            MDMCatalogValue.value_code == value_data.value_code
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Value with code '{value_data.value_code}' already exists in this catalog"
        )

    value = MDMCatalogValue(
        catalog_id=catalog_id,
        **value_data.model_dump(exclude={'catalog_id'})
    )
    db.add(value)
    await db.commit()
    await db.refresh(value)
    return value


@router.get("/{catalog_id}/values", response_model=List[CatalogValueResponse])
async def list_catalog_values(
    catalog_id: UUID,
    parent_value_id: UUID = Query(None),
    include_inactive: bool = Query(False),
    db: AsyncSession = Depends(get_db)
):
    """List values for a catalog."""
    query = select(MDMCatalogValue).where(MDMCatalogValue.catalog_id == catalog_id)

    if not include_inactive:
        query = query.where(MDMCatalogValue.is_active == True)

    if parent_value_id:
        query = query.where(MDMCatalogValue.parent_value_id == parent_value_id)

    query = query.order_by(MDMCatalogValue.sort_order, MDMCatalogValue.value_name)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{catalog_id}/values/{value_id}", response_model=CatalogValueResponse)
async def get_catalog_value(
    catalog_id: UUID,
    value_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific catalog value."""
    result = await db.execute(
        select(MDMCatalogValue).where(
            MDMCatalogValue.id == value_id,
            MDMCatalogValue.catalog_id == catalog_id
        )
    )
    value = result.scalar_one_or_none()

    if not value:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catalog value not found"
        )

    return value


@router.put("/{catalog_id}/values/{value_id}", response_model=CatalogValueResponse)
async def update_catalog_value(
    catalog_id: UUID,
    value_id: UUID,
    value_data: CatalogValueUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a catalog value."""
    result = await db.execute(
        select(MDMCatalogValue).where(
            MDMCatalogValue.id == value_id,
            MDMCatalogValue.catalog_id == catalog_id
        )
    )
    value = result.scalar_one_or_none()

    if not value:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catalog value not found"
        )

    update_data = value_data.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        setattr(value, field, val)

    await db.commit()
    await db.refresh(value)
    return value


@router.delete("/{catalog_id}/values/{value_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_catalog_value(
    catalog_id: UUID,
    value_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """Delete a catalog value (soft delete)."""
    result = await db.execute(
        select(MDMCatalogValue).where(
            MDMCatalogValue.id == value_id,
            MDMCatalogValue.catalog_id == catalog_id
        )
    )
    value = result.scalar_one_or_none()

    if not value:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Catalog value not found"
        )

    value.is_active = False
    await db.commit()
