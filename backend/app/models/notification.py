"""Notification models for MDM system."""
import enum
from sqlalchemy import Column, String, Text, Boolean, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class NotificationChannel(str, enum.Enum):
    """Notification channel enumeration."""
    EMAIL = "EMAIL"
    SMS = "SMS"
    PUSH = "PUSH"
    WEBHOOK = "WEBHOOK"
    TEAMS = "TEAMS"
    SLACK = "SLACK"


class TemplateEngine(str, enum.Enum):
    """Template engine enumeration."""
    HANDLEBARS = "HANDLEBARS"
    FREEMARKER = "FREEMARKER"
    VELOCITY = "VELOCITY"
    JINJA2 = "JINJA2"


class TriggerEvent(str, enum.Enum):
    """Trigger event enumeration."""
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    WORKFLOW = "WORKFLOW"
    QUALITY = "QUALITY"
    MATCH = "MATCH"


class RecipientType(str, enum.Enum):
    """Recipient type enumeration."""
    FIXED = "FIXED"
    DYNAMIC = "DYNAMIC"
    ROLE = "ROLE"
    GROUP = "GROUP"


class MDMNotificationTemplate(BaseModel):
    """Notification templates."""
    __tablename__ = "mdm_notification_template"

    template_code = Column(String(100), unique=True, nullable=False, index=True)
    template_name = Column(String(200), nullable=False)
    channel = Column(Enum(NotificationChannel), nullable=False)
    subject_template = Column(String(500), nullable=True)
    body_template = Column(Text, nullable=False)
    template_engine = Column(Enum(TemplateEngine), default=TemplateEngine.JINJA2)
    available_vars = Column(JSON, nullable=True)

    # Relationships
    notification_rules = relationship("MDMNotificationRule", back_populates="template")


class MDMNotificationRule(BaseModel):
    """Notification rules."""
    __tablename__ = "mdm_notification_rule"

    rule_name = Column(String(200), nullable=False)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("mdm_entity.id"), nullable=True)
    template_id = Column(UUID(as_uuid=True), ForeignKey("mdm_notification_template.id"), nullable=False)
    trigger_event = Column(Enum(TriggerEvent), nullable=False)
    trigger_condition = Column(Text, nullable=True)
    recipient_type = Column(Enum(RecipientType), default=RecipientType.FIXED)
    recipients = Column(JSON, nullable=True)
    delay_minutes = Column(Integer, default=0)
    batch_enabled = Column(Boolean, default=False)

    # Relationships
    entity = relationship("MDMEntity")
    template = relationship("MDMNotificationTemplate", back_populates="notification_rules")
