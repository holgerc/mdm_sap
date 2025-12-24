"""Security models for MDM system."""
import enum
from sqlalchemy import Column, String, Text, Boolean, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Visibility(str, enum.Enum):
    """Field visibility enumeration."""
    VISIBLE = "VISIBLE"
    HIDDEN = "HIDDEN"
    MASKED = "MASKED"


class Editability(str, enum.Enum):
    """Field editability enumeration."""
    EDITABLE = "EDITABLE"
    READONLY = "READONLY"
    DISABLED = "DISABLED"


class MDMRole(BaseModel):
    """Role definition."""
    __tablename__ = "mdm_role"

    role_code = Column(String(50), unique=True, nullable=False, index=True)
    role_name = Column(String(200), nullable=False)
    role_description = Column(Text, nullable=True)
    is_system = Column(Boolean, default=False)

    # Relationships
    users = relationship("MDMUser", back_populates="role")
    entity_permissions = relationship("MDMEntityPermission", back_populates="role", cascade="all, delete-orphan")
    field_permissions = relationship("MDMFieldPermission", back_populates="role", cascade="all, delete-orphan")


class MDMUser(BaseModel):
    """User definition."""
    __tablename__ = "mdm_user"

    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("mdm_role.id"), nullable=True)
    is_superuser = Column(Boolean, default=False)

    # Relationships
    role = relationship("MDMRole", back_populates="users")


class MDMEntityPermission(BaseModel):
    """Entity-level permissions."""
    __tablename__ = "mdm_entity_permission"

    entity_id = Column(UUID(as_uuid=True), ForeignKey("mdm_entity.id"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("mdm_role.id"), nullable=False)
    can_create = Column(Boolean, default=False)
    can_read = Column(Boolean, default=True)
    can_update = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
    can_export = Column(Boolean, default=False)
    can_import = Column(Boolean, default=False)
    can_approve = Column(Boolean, default=False)
    can_merge = Column(Boolean, default=False)
    data_filter = Column(Text, nullable=True)

    # Relationships
    entity = relationship("MDMEntity", back_populates="entity_permissions")
    role = relationship("MDMRole", back_populates="entity_permissions")


class MDMFieldPermission(BaseModel):
    """Field-level permissions."""
    __tablename__ = "mdm_field_permission"

    attribute_id = Column(UUID(as_uuid=True), ForeignKey("mdm_attribute.id"), nullable=False)
    role_id = Column(UUID(as_uuid=True), ForeignKey("mdm_role.id"), nullable=False)
    visibility = Column(Enum(Visibility), default=Visibility.VISIBLE)
    editability = Column(Enum(Editability), default=Editability.EDITABLE)
    mask_pattern = Column(String(100), nullable=True)
    condition_expression = Column(Text, nullable=True)

    # Relationships
    attribute = relationship("MDMAttribute")
    role = relationship("MDMRole", back_populates="field_permissions")
