from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
    Boolean,
)
from sqlalchemy.orm import relationship

from backend.database import Base


# ============================================================
# RISK EVENT
# Stores geopolitical, energy, supply-chain, and disruption events
# ============================================================

class RiskEvent(Base):
    __tablename__ = "risk_events"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(250), nullable=False)
    description = Column(Text, nullable=True)

    # Examples: War, Sanctions, Port Closure, Natural Disaster
    event_type = Column(String(100), nullable=False)

    country = Column(String(100), nullable=True)
    region = Column(String(150), nullable=True)

    # Original intelligence/news source
    source_name = Column(String(150), nullable=True)
    source_url = Column(Text, nullable=True)

    published_at = Column(DateTime, nullable=True)

    # AI-generated risk assessment
    risk_score = Column(Float, default=0.0)

    # Low, Medium, High, Critical
    risk_level = Column(String(50), default="Low")

    # AI confidence in the assessment
    confidence_score = Column(Float, default=0.0)

    # Explainable AI: why this risk score was assigned
    explanation = Column(Text, nullable=True)

    # Indicates whether multiple sources confirm the event
    multi_source_verified = Column(Boolean, default=False)

    status = Column(String(50), default="Active")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    alerts = relationship(
        "Alert",
        back_populates="risk_event"
    )


# ============================================================
# RISK SCORE HISTORY
# Stores changing risk scores over time for trend analysis
# ============================================================

class RiskScoreHistory(Base):
    __tablename__ = "risk_score_history"

    id = Column(Integer, primary_key=True, index=True)

    # Type of entity being monitored:
    # supplier, port, route, refinery, country, region
    entity_type = Column(String(50), nullable=False)

    # ID of entity when the monitored object exists in our DB
    entity_id = Column(Integer, nullable=True)

    entity_name = Column(String(200), nullable=False)

    risk_score = Column(Float, nullable=False)
    confidence_score = Column(Float, default=0.0)

    risk_level = Column(String(50), nullable=False)

    reason = Column(Text, nullable=True)

    recorded_at = Column(DateTime, default=datetime.utcnow)


# ============================================================
# INTELLIGENCE SOURCE
# Stores sources used for multi-source risk correlation
# ============================================================

class IntelligenceSource(Base):
    __tablename__ = "intelligence_sources"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    # Examples: News, AIS, Commodity Market, Sanctions
    source_type = Column(String(100), nullable=False)

    source_url = Column(Text, nullable=True)

    reliability_score = Column(Float, default=0.0)

    is_active = Column(Boolean, default=True)

    last_checked_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


# ============================================================
# ALERT
# Stores real-time alerts generated when risk thresholds are crossed
# ============================================================

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    risk_event_id = Column(
        Integer,
        ForeignKey("risk_events.id"),
        nullable=True,
    )

    title = Column(String(250), nullable=False)
    message = Column(Text, nullable=False)

    # Info, Warning, High, Critical
    severity = Column(String(50), nullable=False)

    # Examples: geopolitical, route, supplier, port, refinery
    alert_type = Column(String(100), nullable=False)

    is_read = Column(Boolean, default=False)
    is_resolved = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    risk_event = relationship(
        "RiskEvent",
        back_populates="alerts"
    )