"""Workflow models for MDM system."""
import enum
from sqlalchemy import Column, String, Text, Boolean, Integer, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class TriggerOn(str, enum.Enum):
    """Trigger event enumeration."""
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    ALL = "ALL"


class StateType(str, enum.Enum):
    """State type enumeration."""
    START = "START"
    INTERMEDIATE = "INTERMEDIATE"
    END = "END"
    ERROR = "ERROR"


class AssigneeType(str, enum.Enum):
    """Assignee type enumeration."""
    USER = "USER"
    ROLE = "ROLE"
    GROUP = "GROUP"
    DYNAMIC = "DYNAMIC"
    AUTO = "AUTO"


class MDMWorkflow(BaseModel):
    """Workflow definition."""
    __tablename__ = "mdm_workflow"

    workflow_code = Column(String(100), unique=True, nullable=False, index=True)
    workflow_name = Column(String(200), nullable=False)
    entity_id = Column(UUID(as_uuid=True), ForeignKey("mdm_entity.id"), nullable=True)
    trigger_on = Column(Enum(TriggerOn), default=TriggerOn.ALL)
    trigger_condition = Column(Text, nullable=True)
    sla_hours = Column(Integer, default=24)
    escalation_enabled = Column(Boolean, default=True)
    parallel_approval = Column(Boolean, default=False)
    version = Column(Integer, default=1)

    # Relationships
    states = relationship("MDMWorkflowState", back_populates="workflow", cascade="all, delete-orphan")
    transitions = relationship("MDMWorkflowTransition", back_populates="workflow", cascade="all, delete-orphan")


class MDMWorkflowState(BaseModel):
    """Workflow state definition."""
    __tablename__ = "mdm_workflow_state"

    workflow_id = Column(UUID(as_uuid=True), ForeignKey("mdm_workflow.id"), nullable=False)
    state_code = Column(String(50), nullable=False)
    state_name = Column(String(200), nullable=False)
    state_type = Column(Enum(StateType), nullable=False)
    assignee_type = Column(Enum(AssigneeType), default=AssigneeType.ROLE)
    assignee_value = Column(String(200), nullable=True)
    sla_hours = Column(Integer, nullable=True)
    auto_action = Column(Text, nullable=True)
    notification_template = Column(String(100), nullable=True)
    sort_order = Column(Integer, default=0)

    # Relationships
    workflow = relationship("MDMWorkflow", back_populates="states")


class MDMWorkflowTransition(BaseModel):
    """Workflow state transitions."""
    __tablename__ = "mdm_workflow_transition"

    workflow_id = Column(UUID(as_uuid=True), ForeignKey("mdm_workflow.id"), nullable=False)
    from_state_id = Column(UUID(as_uuid=True), ForeignKey("mdm_workflow_state.id"), nullable=False)
    to_state_id = Column(UUID(as_uuid=True), ForeignKey("mdm_workflow_state.id"), nullable=False)
    transition_name = Column(String(200), nullable=False)
    condition_expression = Column(Text, nullable=True)
    action_script = Column(Text, nullable=True)
    require_comment = Column(Boolean, default=False)

    # Relationships
    workflow = relationship("MDMWorkflow", back_populates="transitions")
    from_state = relationship("MDMWorkflowState", foreign_keys=[from_state_id])
    to_state = relationship("MDMWorkflowState", foreign_keys=[to_state_id])
