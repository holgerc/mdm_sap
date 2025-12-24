"""Quality rule models for MDM system."""
import enum
from sqlalchemy import Column, String, Text, Boolean, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class QualityDimension(str, enum.Enum):
    """Quality dimension enumeration."""
    COMPLETENESS = "COMPLETENESS"
    ACCURACY = "ACCURACY"
    CONSISTENCY = "CONSISTENCY"
    TIMELINESS = "TIMELINESS"
    UNIQUENESS = "UNIQUENESS"
    VALIDITY = "VALIDITY"


class RuleType(str, enum.Enum):
    """Rule type enumeration."""
    SQL = "SQL"
    SCRIPT = "SCRIPT"
    API = "API"
    BUILTIN = "BUILTIN"


class QualitySeverity(str, enum.Enum):
    """Quality severity enumeration."""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class MDMQualityRule(BaseModel):
    """Data quality rules."""
    __tablename__ = "mdm_quality_rule"

    rule_code = Column(String(100), unique=True, nullable=False, index=True)
    rule_name = Column(String(200), nullable=False)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("mdm_entity.id"), nullable=False)
    dimension = Column(Enum(QualityDimension), nullable=False)
    rule_type = Column(Enum(RuleType), nullable=False)
    rule_expression = Column(Text, nullable=False)
    severity = Column(Enum(QualitySeverity), default=QualitySeverity.MEDIUM)
    threshold_percent = Column(Numeric(5, 2), default=100.00)
    auto_remediate = Column(Boolean, default=False)
    remediation_action = Column(Text, nullable=True)
    notification_enabled = Column(Boolean, default=True)
    schedule_cron = Column(String(100), nullable=True)

    # Relationships
    entity = relationship("MDMEntity", back_populates="quality_rules")
