"""Attribute models for MDM system."""
import enum
from sqlalchemy import Column, String, Text, Boolean, Integer, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class DataType(str, enum.Enum):
    """Data type enumeration."""
    STRING = "STRING"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    DATE = "DATE"
    DATETIME = "DATETIME"
    BOOLEAN = "BOOLEAN"
    JSON = "JSON"
    BLOB = "BLOB"


class UIComponent(str, enum.Enum):
    """UI component enumeration."""
    TEXT = "TEXT"
    TEXTAREA = "TEXTAREA"
    SELECT = "SELECT"
    RADIO = "RADIO"
    CHECKBOX = "CHECKBOX"
    DATE_PICKER = "DATE_PICKER"
    FILE = "FILE"
    RICH_TEXT = "RICH_TEXT"
    NUMBER = "NUMBER"
    EMAIL = "EMAIL"
    URL = "URL"


class ValidationType(str, enum.Enum):
    """Validation type enumeration."""
    REGEX = "REGEX"
    RANGE = "RANGE"
    LENGTH = "LENGTH"
    CUSTOM = "CUSTOM"
    SCRIPT = "SCRIPT"
    API = "API"


class Severity(str, enum.Enum):
    """Severity level enumeration."""
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class TransformType(str, enum.Enum):
    """Transform type enumeration."""
    UPPERCASE = "UPPERCASE"
    LOWERCASE = "LOWERCASE"
    TRIM = "TRIM"
    NORMALIZE = "NORMALIZE"
    MASK = "MASK"
    ENCRYPT = "ENCRYPT"
    HASH = "HASH"
    CUSTOM = "CUSTOM"


class ApplyOn(str, enum.Enum):
    """Apply on enumeration."""
    INPUT = "INPUT"
    OUTPUT = "OUTPUT"
    BOTH = "BOTH"


class DisplayType(str, enum.Enum):
    """Display type for attribute groups."""
    TAB = "TAB"
    SECTION = "SECTION"
    ACCORDION = "ACCORDION"
    CARD = "CARD"


class MDMAttributeGroup(BaseModel):
    """Attribute group for organizing fields."""
    __tablename__ = "mdm_attribute_group"

    entity_id = Column(UUID(as_uuid=True), ForeignKey("mdm_entity.id"), nullable=False)
    group_code = Column(String(100), nullable=False)
    group_name = Column(String(200), nullable=False)
    group_icon = Column(String(100), nullable=True)
    display_type = Column(Enum(DisplayType), default=DisplayType.SECTION)
    sort_order = Column(Integer, default=0)
    is_collapsible = Column(Boolean, default=True)
    default_collapsed = Column(Boolean, default=False)
    visibility_condition = Column(Text, nullable=True)

    # Relationships
    entity = relationship("MDMEntity", back_populates="attribute_groups")
    attributes = relationship("MDMAttribute", back_populates="attribute_group")


class MDMAttribute(BaseModel):
    """Attribute definition for entities."""
    __tablename__ = "mdm_attribute"

    entity_id = Column(UUID(as_uuid=True), ForeignKey("mdm_entity.id"), nullable=False)
    attribute_code = Column(String(100), nullable=False)
    attribute_name = Column(String(200), nullable=False)
    attribute_group_id = Column(UUID(as_uuid=True), ForeignKey("mdm_attribute_group.id"), nullable=True)
    data_type = Column(Enum(DataType), nullable=False)
    ui_component = Column(Enum(UIComponent), default=UIComponent.TEXT)
    display_order = Column(Integer, default=0)

    # Field behavior
    is_required = Column(Boolean, default=False)
    is_unique = Column(Boolean, default=False)
    is_searchable = Column(Boolean, default=True)
    is_filterable = Column(Boolean, default=True)
    is_sortable = Column(Boolean, default=True)
    show_in_list = Column(Boolean, default=True)
    show_in_detail = Column(Boolean, default=True)
    is_readonly = Column(Boolean, default=False)
    is_hidden = Column(Boolean, default=False)
    is_encrypted = Column(Boolean, default=False)
    is_pii = Column(Boolean, default=False)

    # Default and help
    default_value = Column(Text, nullable=True)
    placeholder = Column(String(200), nullable=True)
    help_text = Column(Text, nullable=True)
    tooltip = Column(String(500), nullable=True)

    # Catalog reference
    catalog_id = Column(UUID(as_uuid=True), ForeignKey("mdm_catalog.id"), nullable=True)

    # Relationships
    entity = relationship("MDMEntity", back_populates="attributes")
    attribute_group = relationship("MDMAttributeGroup", back_populates="attributes")
    validations = relationship("MDMAttributeValidation", back_populates="attribute", cascade="all, delete-orphan")
    transforms = relationship("MDMAttributeTransform", back_populates="attribute", cascade="all, delete-orphan")
    catalog = relationship("MDMCatalog", back_populates="attributes")


class MDMAttributeValidation(BaseModel):
    """Validation rules for attributes."""
    __tablename__ = "mdm_attribute_validation"

    attribute_id = Column(UUID(as_uuid=True), ForeignKey("mdm_attribute.id"), nullable=False)
    validation_type = Column(Enum(ValidationType), nullable=False)
    validation_rule = Column(Text, nullable=True)
    min_value = Column(Numeric, nullable=True)
    max_value = Column(Numeric, nullable=True)
    min_length = Column(Integer, nullable=True)
    max_length = Column(Integer, nullable=True)
    regex_pattern = Column(String(500), nullable=True)
    allowed_values = Column(JSON, nullable=True)
    forbidden_values = Column(JSON, nullable=True)
    custom_function = Column(Text, nullable=True)
    api_endpoint = Column(String(500), nullable=True)
    error_message = Column(String(500), nullable=True)
    error_code = Column(String(50), nullable=True)
    severity = Column(Enum(Severity), default=Severity.ERROR)
    execution_order = Column(Integer, default=0)

    # Relationships
    attribute = relationship("MDMAttribute", back_populates="validations")


class MDMAttributeTransform(BaseModel):
    """Transform rules for attributes."""
    __tablename__ = "mdm_attribute_transform"

    attribute_id = Column(UUID(as_uuid=True), ForeignKey("mdm_attribute.id"), nullable=False)
    transform_type = Column(Enum(TransformType), nullable=False)
    transform_config = Column(JSON, nullable=True)
    apply_on = Column(Enum(ApplyOn), default=ApplyOn.INPUT)
    execution_order = Column(Integer, default=0)
    condition_expression = Column(Text, nullable=True)

    # Relationships
    attribute = relationship("MDMAttribute", back_populates="transforms")
