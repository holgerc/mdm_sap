"""Translation models for MDM system."""
import enum
from sqlalchemy import Column, String, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from app.models.base import BaseModel


class ObjectType(str, enum.Enum):
    """Object type enumeration for translations."""
    ENTITY = "ENTITY"
    ATTRIBUTE = "ATTRIBUTE"
    CATALOG = "CATALOG"
    VALUE = "VALUE"
    GROUP = "GROUP"
    WORKFLOW = "WORKFLOW"


class MDMTranslation(BaseModel):
    """Translation entries for i18n support."""
    __tablename__ = "mdm_translation"

    object_type = Column(Enum(ObjectType), nullable=False)
    object_id = Column(UUID(as_uuid=True), nullable=False)
    field_name = Column(String(100), nullable=False)
    locale = Column(String(10), nullable=False)
    translated_value = Column(Text, nullable=False)
