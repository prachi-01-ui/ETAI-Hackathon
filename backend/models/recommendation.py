from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from backend.database import Base


# ============================================================
# RECOMMENDATION
# Stores AI-generated recommendations after risk analysis
# and scenario simulation
# ============================================================

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)

    simulation_run_id = Column(
        Integer,
        ForeignKey("simulation_runs.id"),
        nullable=True,
    )

    risk_event_id = Column(
        Integer,
        ForeignKey("risk_events.id"),
        nullable=True,
    )

    title = Column(String(250), nullable=False)

    description = Column(Text, nullable=False)

    # Examples:
    # Alternative Supplier
    # Alternative Route
    # SPR Release
    # Procurement Action
    # Inventory Adjustment
    recommendation_type = Column(
        String(100),
        nullable=False,
    )

    # Low, Medium, High, Critical
    priority = Column(
        String(50),
        default="Medium",
    )

    # AI confidence in this recommendation
    confidence_score = Column(
        Float,
        default=0.0,
    )

    # Explainable AI reasoning:
    # Why is the system recommending this action?
    reasoning = Column(Text, nullable=True)

    # Expected cost of implementing the recommendation
    estimated_cost = Column(
        Float,
        nullable=True,
    )

    # Expected financial or operational benefit
    estimated_benefit = Column(
        Float,
        nullable=True,
    )

    # Expected reduction in risk score
    expected_risk_reduction = Column(
        Float,
        nullable=True,
    )

    # Pending, Accepted, Rejected, Executed
    status = Column(
        String(50),
        default="Pending",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    decisions = relationship(
        "DecisionAction",
        back_populates="recommendation",
    )


# ============================================================
# ALTERNATIVE OPTION
# Stores ranked alternative suppliers, ports, or routes
# recommended by the AI
# ============================================================

class AlternativeOption(Base):
    __tablename__ = "alternative_options"

    id = Column(Integer, primary_key=True, index=True)

    recommendation_id = Column(
        Integer,
        ForeignKey("recommendations.id"),
        nullable=False,
    )

    # supplier, route, port
    option_type = Column(
        String(50),
        nullable=False,
    )

    # ID of supplier/route/port if available
    entity_id = Column(
        Integer,
        nullable=True,
    )

    entity_name = Column(
        String(200),
        nullable=False,
    )

    # Ranking assigned by recommendation engine
    rank = Column(
        Integer,
        nullable=False,
    )

    suitability_score = Column(
        Float,
        default=0.0,
    )

    risk_score = Column(
        Float,
        default=0.0,
    )

    estimated_cost = Column(
        Float,
        nullable=True,
    )

    estimated_delay_days = Column(
        Float,
        nullable=True,
    )

    reason = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )


# ============================================================
# DECISION ACTION
# Tracks human decisions and execution of AI recommendations
# ============================================================

class DecisionAction(Base):
    __tablename__ = "decision_actions"

    id = Column(Integer, primary_key=True, index=True)

    recommendation_id = Column(
        Integer,
        ForeignKey("recommendations.id"),
        nullable=False,
    )

    # Accepted, Rejected, Executed, Cancelled
    action_type = Column(
        String(50),
        nullable=False,
    )

    # Person/system responsible for the decision
    decided_by = Column(
        String(150),
        nullable=True,
    )

    decision_reason = Column(
        Text,
        nullable=True,
    )

    decided_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    executed_at = Column(
        DateTime,
        nullable=True,
    )

    recommendation = relationship(
        "Recommendation",
        back_populates="decisions",
    )

    outcome = relationship(
        "ActionOutcome",
        back_populates="decision_action",
        uselist=False,
    )


# ============================================================
# ACTION OUTCOME
# Stores the real or simulated outcome after an action
# is executed
# ============================================================

class ActionOutcome(Base):
    __tablename__ = "action_outcomes"

    id = Column(Integer, primary_key=True, index=True)

    decision_action_id = Column(
        Integer,
        ForeignKey("decision_actions.id"),
        nullable=False,
        unique=True,
    )

    # Successful, Partially Successful, Failed
    outcome_status = Column(
        String(50),
        nullable=False,
    )

    actual_cost = Column(
        Float,
        nullable=True,
    )

    actual_benefit = Column(
        Float,
        nullable=True,
    )

    actual_risk_reduction = Column(
        Float,
        nullable=True,
    )

    supply_restored_percentage = Column(
        Float,
        nullable=True,
    )

    notes = Column(
        Text,
        nullable=True,
    )

    recorded_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    decision_action = relationship(
        "DecisionAction",
        back_populates="outcome",
    )