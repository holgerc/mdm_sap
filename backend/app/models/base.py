"""Base models and mixins for MDM system."""
import uuid
from datetime import datetime
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class AuditMixin:
    """Mixin for audit fields."""
    created_by = Column(UUID(as_uuid=True), nullable=True)
    updated_by = Column(UUID(as_uuid=True), nullable=True)


class BaseModel(Base, TimestampMixin):
    """Base model with common fields."""
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    is_active = Column(Boolean, default=True, nullable=False)
