"""Entity model for MDM system."""
import enum
from sqlalchemy import Column, String, Text, Boolean, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, AuditMixin


class AuditLevel(str, enum.Enum):
    """Audit level enumeration."""
    NONE = "NONE"
    BASIC = "BASIC"
    FULL = "FULL"
    FORENSIC = "FORENSIC"


class MDMEntity(BaseModel, AuditMixin):
    """Master Data Entity configuration."""
    __tablename__ = "mdm_entity"

    entity_code = Column(String(50), unique=True, nullable=False, index=True)
    entity_name = Column(String(200), nullable=False)
    entity_description = Column(Text, nullable=True)
    icon_class = Column(String(100), nullable=True)
    color_hex = Column(String(7), nullable=True)
    is_hierarchical = Column(Boolean, default=False)
    max_hierarchy_levels = Column(Integer, default=5)
    allow_versioning = Column(Boolean, default=True)
    retention_days = Column(Integer, default=365)
    audit_level = Column(Enum(AuditLevel), default=AuditLevel.BASIC)
    workflow_enabled = Column(Boolean, default=False)
    default_workflow_id = Column(UUID(as_uuid=True), ForeignKey("mdm_workflow.id"), nullable=True)

    # Relationships
    attributes = relationship("MDMAttribute", back_populates="entity", cascade="all, delete-orphan")
    attribute_groups = relationship("MDMAttributeGroup", back_populates="entity", cascade="all, delete-orphan")
    quality_rules = relationship("MDMQualityRule", back_populates="entity", cascade="all, delete-orphan")
    match_rules = relationship("MDMMatchRule", back_populates="entity", cascade="all, delete-orphan")
    entity_permissions = relationship("MDMEntityPermission", back_populates="entity", cascade="all, delete-orphan")
    form_layouts = relationship("MDMFormLayout", back_populates="entity", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<MDMEntity(code={self.entity_code}, name={self.entity_name})>"
