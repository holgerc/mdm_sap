"""Match and Merge models for MDM system."""
import enum
from sqlalchemy import Column, String, Boolean, Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class MatchAlgorithm(str, enum.Enum):
    """Match algorithm enumeration."""
    EXACT = "EXACT"
    FUZZY = "FUZZY"
    SOUNDEX = "SOUNDEX"
    METAPHONE = "METAPHONE"
    LEVENSHTEIN = "LEVENSHTEIN"
    JARO_WINKLER = "JARO_WINKLER"
    ML = "ML"


class ComparisonType(str, enum.Enum):
    """Comparison type enumeration."""
    EXACT = "EXACT"
    FUZZY = "FUZZY"
    PHONETIC = "PHONETIC"
    NUMERIC = "NUMERIC"
    DATE = "DATE"


class NullHandling(str, enum.Enum):
    """Null handling enumeration."""
    MATCH = "MATCH"
    NO_MATCH = "NO_MATCH"
    IGNORE = "IGNORE"


class StrategyType(str, enum.Enum):
    """Merge strategy type enumeration."""
    MOST_RECENT = "MOST_RECENT"
    MOST_TRUSTED = "MOST_TRUSTED"
    MOST_COMPLETE = "MOST_COMPLETE"
    AGGREGATE = "AGGREGATE"
    MANUAL = "MANUAL"
    CUSTOM = "CUSTOM"


class MDMMatchRule(BaseModel):
    """Match rules for deduplication."""
    __tablename__ = "mdm_match_rule"

    entity_id = Column(UUID(as_uuid=True), ForeignKey("mdm_entity.id"), nullable=False)
    rule_name = Column(String(200), nullable=False)
    algorithm = Column(Enum(MatchAlgorithm), default=MatchAlgorithm.FUZZY)
    match_threshold = Column(Numeric(3, 2), default=0.80)
    auto_merge_threshold = Column(Numeric(3, 2), default=0.95)
    blocking_fields = Column(JSON, nullable=True)
    weight_total = Column(Numeric(5, 2), default=1.00)

    # Relationships
    entity = relationship("MDMEntity", back_populates="match_rules")
    match_fields = relationship("MDMMatchField", back_populates="match_rule", cascade="all, delete-orphan")


class MDMMatchField(BaseModel):
    """Match fields configuration."""
    __tablename__ = "mdm_match_field"

    match_rule_id = Column(UUID(as_uuid=True), ForeignKey("mdm_match_rule.id"), nullable=False)
    attribute_id = Column(UUID(as_uuid=True), ForeignKey("mdm_attribute.id"), nullable=False)
    comparison_type = Column(Enum(ComparisonType), default=ComparisonType.FUZZY)
    weight = Column(Numeric(3, 2), default=0.50)
    null_handling = Column(Enum(NullHandling), default=NullHandling.IGNORE)
    transform_before = Column(JSON, nullable=True)
    tolerance = Column(String(50), nullable=True)

    # Relationships
    match_rule = relationship("MDMMatchRule", back_populates="match_fields")
    attribute = relationship("MDMAttribute")


class MDMMergeStrategy(BaseModel):
    """Merge strategy configuration."""
    __tablename__ = "mdm_merge_strategy"

    entity_id = Column(UUID(as_uuid=True), ForeignKey("mdm_entity.id"), nullable=False)
    attribute_id = Column(UUID(as_uuid=True), ForeignKey("mdm_attribute.id"), nullable=False)
    strategy_type = Column(Enum(StrategyType), default=StrategyType.MOST_RECENT)
    trust_source_order = Column(JSON, nullable=True)
    aggregate_function = Column(String(50), nullable=True)
    custom_function = Column(String, nullable=True)

    # Relationships
    entity = relationship("MDMEntity")
    attribute = relationship("MDMAttribute")
