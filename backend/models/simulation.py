from datetime import datetime

from sqlalchemy import (
    Boolean,
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
# SCENARIO
# Defines a disruption scenario that can be simulated
# Example: Strait of Hormuz Closure, Red Sea Disruption
# ============================================================

class Scenario(Base):
    __tablename__ = "scenarios"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), nullable=False)

    description = Column(Text, nullable=True)

    # Examples:
    # Hormuz Closure, Red Sea Disruption, OPEC Cut,
    # Port Closure, Sanctions, Natural Disaster
    scenario_type = Column(String(100), nullable=False)

    # Low, Medium, High, Critical
    severity = Column(String(50), default="Medium")

    # Duration of disruption assumed by the scenario
    disruption_duration_days = Column(Integer, nullable=True)

    # Percentage of supply expected to be disrupted
    disruption_percentage = Column(Float, default=0.0)

    # Can be used for the hackathon's primary demo scenario
    is_demo_scenario = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    simulation_runs = relationship(
        "SimulationRun",
        back_populates="scenario",
    )


# ============================================================
# SIMULATION RUN
# Represents one execution of a scenario
# ============================================================

class SimulationRun(Base):
    __tablename__ = "simulation_runs"

    id = Column(Integer, primary_key=True, index=True)

    scenario_id = Column(
        Integer,
        ForeignKey("scenarios.id"),
        nullable=False,
    )

    # Optional link to the real-world event that triggered simulation
    risk_event_id = Column(
        Integer,
        ForeignKey("risk_events.id"),
        nullable=True,
    )

    # Pending, Running, Completed, Failed
    status = Column(String(50), default="Pending")

    # AI/model confidence in simulation results
    confidence_score = Column(Float, default=0.0)

    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    scenario = relationship(
        "Scenario",
        back_populates="simulation_runs",
    )

    impact = relationship(
        "SimulationImpact",
        back_populates="simulation_run",
        uselist=False,
    )

    timeline_entries = relationship(
        "SimulationTimeline",
        back_populates="simulation_run",
    )

    digital_twin_snapshots = relationship(
        "DigitalTwinSnapshot",
        back_populates="simulation_run",
    )


# ============================================================
# SIMULATION IMPACT
# Stores the overall calculated consequences of a simulation
# ============================================================

class SimulationImpact(Base):
    __tablename__ = "simulation_impacts"

    id = Column(Integer, primary_key=True, index=True)

    simulation_run_id = Column(
        Integer,
        ForeignKey("simulation_runs.id"),
        nullable=False,
        unique=True,
    )

    # Estimated percentage reduction in available supply
    supply_disruption_percentage = Column(Float, default=0.0)

    # Estimated energy supply deficit
    supply_gap = Column(Float, default=0.0)

    # Additional shipping delay caused by disruption
    shipment_delay_days = Column(Float, default=0.0)

    # Estimated percentage reduction in refinery utilization
    refinery_utilization_impact = Column(Float, default=0.0)

    # Estimated number of days strategic reserves can cover
    spr_runway_days = Column(Float, nullable=True)

    # Estimated financial/economic loss
    estimated_economic_loss = Column(Float, default=0.0)

    # Estimated commodity price impact percentage
    commodity_price_impact_percentage = Column(
        Float,
        default=0.0,
    )

    summary = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    simulation_run = relationship(
        "SimulationRun",
        back_populates="impact",
    )


# ============================================================
# DIGITAL TWIN SNAPSHOT
# Captures the state of an entity at a specific simulation time
# Used to represent changes in the virtual supply chain
# ============================================================

class DigitalTwinSnapshot(Base):
    __tablename__ = "digital_twin_snapshots"

    id = Column(Integer, primary_key=True, index=True)

    simulation_run_id = Column(
        Integer,
        ForeignKey("simulation_runs.id"),
        nullable=False,
    )

    # supplier, port, route, refinery
    entity_type = Column(String(50), nullable=False)

    # ID of the supplier/port/route/refinery
    entity_id = Column(Integer, nullable=False)

    entity_name = Column(String(200), nullable=False)

    # Simulation time, e.g. Day 0, Day 3, Day 7
    simulation_day = Column(Integer, default=0)

    operational_status = Column(
        String(50),
        default="Operational",
    )

    capacity_utilization = Column(Float, nullable=True)

    risk_score = Column(Float, default=0.0)

    supply_available = Column(Float, nullable=True)

    delay_days = Column(Float, default=0.0)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    simulation_run = relationship(
        "SimulationRun",
        back_populates="digital_twin_snapshots",
    )


# ============================================================
# SIMULATION TIMELINE
# Stores time-based changes during a scenario
# Supports Decision Timeline and time-slider visualization
# ============================================================

class SimulationTimeline(Base):
    __tablename__ = "simulation_timeline"

    id = Column(Integer, primary_key=True, index=True)

    simulation_run_id = Column(
        Integer,
        ForeignKey("simulation_runs.id"),
        nullable=False,
    )

    simulation_day = Column(Integer, nullable=False)

    # Example: Route Closed, Supply Gap Increased,
    # Refinery Utilization Dropped
    event_type = Column(String(100), nullable=False)

    title = Column(String(250), nullable=False)

    description = Column(Text, nullable=True)

    risk_score = Column(Float, nullable=True)

    supply_gap = Column(Float, nullable=True)

    economic_loss = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    simulation_run = relationship(
        "SimulationRun",
        back_populates="timeline_entries",
    )