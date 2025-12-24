"""Integration models for MDM system."""
import enum
from sqlalchemy import Column, String, Text, Boolean, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class ConnectionType(str, enum.Enum):
    """Connection type enumeration."""
    DATABASE = "DATABASE"
    REST_API = "REST_API"
    SOAP = "SOAP"
    FILE = "FILE"
    KAFKA = "KAFKA"
    MQ = "MQ"
    SFTP = "SFTP"
    SAP_RFC = "SAP_RFC"
    SAP_ODATA = "SAP_ODATA"


class Direction(str, enum.Enum):
    """Integration direction enumeration."""
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"
    BIDIRECTIONAL = "BIDIRECTIONAL"


class SyncMode(str, enum.Enum):
    """Sync mode enumeration."""
    FULL = "FULL"
    INCREMENTAL = "INCREMENTAL"
    CDC = "CDC"
    REAL_TIME = "REAL_TIME"


class ErrorHandling(str, enum.Enum):
    """Error handling enumeration."""
    STOP = "STOP"
    SKIP = "SKIP"
    LOG = "LOG"


class MappingDirection(str, enum.Enum):
    """Mapping direction enumeration."""
    IN = "IN"
    OUT = "OUT"
    BOTH = "BOTH"


class MDMConnection(BaseModel):
    """External system connection."""
    __tablename__ = "mdm_connection"

    connection_name = Column(String(200), nullable=False)
    connection_type = Column(Enum(ConnectionType), nullable=False)
    direction = Column(Enum(Direction), default=Direction.BIDIRECTIONAL)
    host = Column(String(500), nullable=True)
    port = Column(Integer, nullable=True)
    credentials_vault_key = Column(String(200), nullable=True)
    connection_params = Column(JSON, nullable=True)
    retry_attempts = Column(Integer, default=3)
    retry_delay_ms = Column(Integer, default=1000)
    timeout_ms = Column(Integer, default=30000)
    pool_size = Column(Integer, default=5)

    # Relationships
    integration_mappings = relationship("MDMIntegrationMapping", back_populates="connection", cascade="all, delete-orphan")


class MDMIntegrationMapping(BaseModel):
    """Integration mapping configuration."""
    __tablename__ = "mdm_integration_mapping"

    connection_id = Column(UUID(as_uuid=True), ForeignKey("mdm_connection.id"), nullable=False)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("mdm_entity.id"), nullable=False)
    external_object = Column(String(200), nullable=False)
    sync_mode = Column(Enum(SyncMode), default=SyncMode.INCREMENTAL)
    sync_frequency = Column(String(100), nullable=True)
    delta_field = Column(String(100), nullable=True)
    filter_expression = Column(Text, nullable=True)
    batch_size = Column(Integer, default=1000)
    error_handling = Column(Enum(ErrorHandling), default=ErrorHandling.LOG)
    priority = Column(Integer, default=0)

    # Relationships
    connection = relationship("MDMConnection", back_populates="integration_mappings")
    entity = relationship("MDMEntity")
    field_mappings = relationship("MDMFieldMapping", back_populates="integration_mapping", cascade="all, delete-orphan")


class MDMFieldMapping(BaseModel):
    """Field mapping for integrations."""
    __tablename__ = "mdm_field_mapping"

    mapping_id = Column(UUID(as_uuid=True), ForeignKey("mdm_integration_mapping.id"), nullable=False)
    attribute_id = Column(UUID(as_uuid=True), ForeignKey("mdm_attribute.id"), nullable=False)
    external_field = Column(String(200), nullable=False)
    mapping_direction = Column(Enum(MappingDirection), default=MappingDirection.BOTH)
    transformation = Column(Text, nullable=True)
    default_value = Column(Text, nullable=True)
    lookup_config = Column(JSON, nullable=True)
    is_key_field = Column(Boolean, default=False)

    # Relationships
    integration_mapping = relationship("MDMIntegrationMapping", back_populates="field_mappings")
    attribute = relationship("MDMAttribute")
