"""Relationship models for MDM system."""
import enum
from sqlalchemy import Column, String, Boolean, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class RelationshipType(str, enum.Enum):
    """Relationship type enumeration."""
    ONE_TO_ONE = "ONE_TO_ONE"
    ONE_TO_MANY = "ONE_TO_MANY"
    MANY_TO_MANY = "MANY_TO_MANY"


class MDMRelationship(BaseModel):
    """Relationship between entities."""
    __tablename__ = "mdm_relationship"

    relationship_code = Column(String(100), unique=True, nullable=False, index=True)
    relationship_name = Column(String(200), nullable=False)
    source_entity_id = Column(UUID(as_uuid=True), ForeignKey("mdm_entity.id"), nullable=False)
    target_entity_id = Column(UUID(as_uuid=True), ForeignKey("mdm_entity.id"), nullable=False)
    relationship_type = Column(Enum(RelationshipType), nullable=False)
    is_bidirectional = Column(Boolean, default=False)
    cascade_delete = Column(Boolean, default=False)
    cascade_deactivate = Column(Boolean, default=False)
    min_cardinality = Column(Integer, default=0)
    max_cardinality = Column(Integer, nullable=True)
    allow_self_reference = Column(Boolean, default=False)
    valid_from_field = Column(String(100), nullable=True)
    valid_to_field = Column(String(100), nullable=True)

    # Relationships
    source_entity = relationship("MDMEntity", foreign_keys=[source_entity_id])
    target_entity = relationship("MDMEntity", foreign_keys=[target_entity_id])
