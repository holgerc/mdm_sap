"""Catalog models for MDM system."""
import enum
from sqlalchemy import Column, String, Boolean, Integer, Enum, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class CatalogType(str, enum.Enum):
    """Catalog type enumeration."""
    SIMPLE = "SIMPLE"
    HIERARCHICAL = "HIERARCHICAL"
    DEPENDENT = "DEPENDENT"


class MDMCatalog(BaseModel):
    """Catalog definition for lookup values."""
    __tablename__ = "mdm_catalog"

    catalog_code = Column(String(50), unique=True, nullable=False, index=True)
    catalog_name = Column(String(200), nullable=False)
    catalog_type = Column(Enum(CatalogType), default=CatalogType.SIMPLE)
    parent_catalog_id = Column(UUID(as_uuid=True), ForeignKey("mdm_catalog.id"), nullable=True)
    is_system = Column(Boolean, default=False)
    allow_user_values = Column(Boolean, default=False)
    cache_enabled = Column(Boolean, default=True)
    cache_ttl_seconds = Column(Integer, default=3600)

    # Relationships
    values = relationship("MDMCatalogValue", back_populates="catalog", cascade="all, delete-orphan")
    attributes = relationship("MDMAttribute", back_populates="catalog")
    parent_catalog = relationship("MDMCatalog", remote_side="MDMCatalog.id", backref="child_catalogs")


class MDMCatalogValue(BaseModel):
    """Catalog value entries."""
    __tablename__ = "mdm_catalog_value"

    catalog_id = Column(UUID(as_uuid=True), ForeignKey("mdm_catalog.id"), nullable=False)
    value_code = Column(String(100), nullable=False)
    value_name = Column(String(500), nullable=False)
    parent_value_id = Column(UUID(as_uuid=True), ForeignKey("mdm_catalog_value.id"), nullable=True)
    dependent_value_id = Column(UUID(as_uuid=True), nullable=True)
    sort_order = Column(Integer, default=0)
    icon_class = Column(String(100), nullable=True)
    color_hex = Column(String(7), nullable=True)
    metadata = Column(JSON, nullable=True)
    valid_from = Column(Date, nullable=True)
    valid_to = Column(Date, nullable=True)
    is_default = Column(Boolean, default=False)

    # Relationships
    catalog = relationship("MDMCatalog", back_populates="values")
    parent_value = relationship("MDMCatalogValue", remote_side="MDMCatalogValue.id", backref="child_values")
