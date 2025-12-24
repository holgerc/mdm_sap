"""UI configuration models for MDM system."""
import enum
from sqlalchemy import Column, String, Boolean, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class LayoutType(str, enum.Enum):
    """Layout type enumeration."""
    CREATE = "CREATE"
    EDIT = "EDIT"
    VIEW = "VIEW"
    SEARCH = "SEARCH"


class MDMFormLayout(BaseModel):
    """Form layout configuration."""
    __tablename__ = "mdm_form_layout"

    entity_id = Column(UUID(as_uuid=True), ForeignKey("mdm_entity.id"), nullable=False)
    layout_name = Column(String(200), nullable=False)
    layout_type = Column(Enum(LayoutType), nullable=False)
    columns = Column(Integer, default=2)
    layout_config = Column(JSON, nullable=True)
    role_id = Column(UUID(as_uuid=True), ForeignKey("mdm_role.id"), nullable=True)
    is_default = Column(Boolean, default=False)

    # Relationships
    entity = relationship("MDMEntity", back_populates="form_layouts")
    role = relationship("MDMRole")
