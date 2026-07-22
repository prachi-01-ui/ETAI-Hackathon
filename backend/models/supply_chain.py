from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry

from backend.database import Base


# ============================================================
# SUPPLIER
# Represents countries/companies supplying energy commodities
# ============================================================

class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    country = Column(String(100), nullable=False)

    commodity_type = Column(String(100), nullable=False)

    production_capacity = Column(Float, nullable=True)

    reliability_score = Column(Float, default=0.0)
    current_risk_score = Column(Float, default=0.0)

    status = Column(String(50), default="Active")

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with ports
    ports = relationship(
        "Port",
        back_populates="supplier"
    )


# ============================================================
# PORT
# Represents energy import/export ports
# ============================================================

class Port(Base):
    __tablename__ = "ports"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    country = Column(String(100), nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # PostGIS geographic point
    # SRID 4326 = standard GPS longitude/latitude coordinates
    location = Column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
        ),
        nullable=True,
    )

    capacity = Column(Float, nullable=True)

    operational_status = Column(
        String(50),
        default="Operational"
    )

    congestion_level = Column(Float, default=0.0)
    current_risk_score = Column(Float, default=0.0)

    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id"),
        nullable=True
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    supplier = relationship(
        "Supplier",
        back_populates="ports"
    )

    outgoing_routes = relationship(
        "ShippingRoute",
        foreign_keys="ShippingRoute.origin_port_id",
        back_populates="origin_port"
    )

    incoming_routes = relationship(
        "ShippingRoute",
        foreign_keys="ShippingRoute.destination_port_id",
        back_populates="destination_port"
    )


# ============================================================
# REFINERY
# Represents oil/gas processing facilities
# ============================================================

class Refinery(Base):
    __tablename__ = "refineries"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    country = Column(String(100), nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # PostGIS geographic point
    # SRID 4326 = standard GPS longitude/latitude coordinates
    location = Column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
        ),
        nullable=True,
    )

    processing_capacity = Column(Float, nullable=True)

    current_utilization = Column(Float, default=0.0)

    operational_status = Column(
        String(50),
        default="Operational"
    )

    current_risk_score = Column(Float, default=0.0)

    created_at = Column(DateTime, default=datetime.utcnow)


# ============================================================
# SHIPPING ROUTE
# Represents energy transportation corridors
# ============================================================

class ShippingRoute(Base):
    __tablename__ = "shipping_routes"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)

    origin_port_id = Column(
        Integer,
        ForeignKey("ports.id"),
        nullable=False
    )

    destination_port_id = Column(
        Integer,
        ForeignKey("ports.id"),
        nullable=False
    )

    distance_km = Column(Float, nullable=True)

    estimated_travel_days = Column(Float, nullable=True)

    current_risk_score = Column(Float, default=0.0)

    status = Column(
        String(50),
        default="Operational"
    )

    risk_reason = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    origin_port = relationship(
        "Port",
        foreign_keys=[origin_port_id],
        back_populates="outgoing_routes"
    )

    destination_port = relationship(
        "Port",
        foreign_keys=[destination_port_id],
        back_populates="incoming_routes"
    )