"""Audit models for MDM system."""
import enum
from sqlalchemy import Column, String, Text, Boolean, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel
from app.models.entity import AuditLevel


class MDMAuditConfig(BaseModel):
    """Audit configuration per entity."""
    __tablename__ = "mdm_audit_config"

    entity_id = Column(UUID(as_uuid=True), ForeignKey("mdm_entity.id"), nullable=False, unique=True)
    audit_level = Column(Enum(AuditLevel), default=AuditLevel.BASIC)
    track_create = Column(Boolean, default=True)
    track_update = Column(Boolean, default=True)
    track_delete = Column(Boolean, default=True)
    track_read = Column(Boolean, default=False)
    track_export = Column(Boolean, default=False)
    store_old_values = Column(Boolean, default=True)
    store_new_values = Column(Boolean, default=True)
    retention_days = Column(Integer, default=365)
    archive_enabled = Column(Boolean, default=False)
    archive_location = Column(String(500), nullable=True)

    # Relationships
    entity = relationship("MDMEntity")


class AuditAction(str, enum.Enum):
    """Audit action enumeration."""
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    READ = "READ"
    EXPORT = "EXPORT"
    IMPORT = "IMPORT"
    MERGE = "MERGE"
    APPROVE = "APPROVE"
    REJECT = "REJECT"


class MDMAuditLog(BaseModel):
    """Audit log entries."""
    __tablename__ = "mdm_audit_log"

    entity_id = Column(UUID(as_uuid=True), ForeignKey("mdm_entity.id"), nullable=False)
    record_id = Column(UUID(as_uuid=True), nullable=False)
    action = Column(Enum(AuditAction), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("mdm_user.id"), nullable=True)
    old_values = Column(JSON, nullable=True)
    new_values = Column(JSON, nullable=True)
    changed_fields = Column(JSON, nullable=True)
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    action_timestamp = Column(DateTime, nullable=False)
    additional_info = Column(JSON, nullable=True)

    # Relationships
    entity = relationship("MDMEntity")
    user = relationship("MDMUser")
