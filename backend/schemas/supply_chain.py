from typing import Optional

from pydantic import BaseModel, ConfigDict


# ============================================================
# SUPPLIER SCHEMAS
# ============================================================

class SupplierBase(BaseModel):
    name: str
    country: str
    commodity_type: str
    production_capacity: Optional[float] = None
    reliability_score: float = 0.0
    current_risk_score: float = 0.0
    status: str = "Active"


class SupplierCreate(SupplierBase):
    pass


class SupplierResponse(SupplierBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# PORT SCHEMAS
# ============================================================

class PortBase(BaseModel):
    name: str
    country: str
    latitude: float
    longitude: float
    capacity: Optional[float] = None
    operational_status: str = "Operational"
    congestion_level: float = 0.0
    current_risk_score: float = 0.0
    supplier_id: Optional[int] = None


class PortCreate(PortBase):
    pass


class PortResponse(PortBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# REFINERY SCHEMAS
# ============================================================

class RefineryBase(BaseModel):
    name: str
    country: str
    latitude: float
    longitude: float
    processing_capacity: Optional[float] = None
    current_utilization: float = 0.0
    operational_status: str = "Operational"
    current_risk_score: float = 0.0


class RefineryCreate(RefineryBase):
    pass


class RefineryResponse(RefineryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# SHIPPING ROUTE SCHEMAS
# ============================================================

class ShippingRouteBase(BaseModel):
    name: str
    origin_port_id: int
    destination_port_id: int
    distance_km: Optional[float] = None
    estimated_travel_days: Optional[float] = None
    current_risk_score: float = 0.0
    status: str = "Operational"
    risk_reason: Optional[str] = None


class ShippingRouteCreate(ShippingRouteBase):
    pass


class ShippingRouteResponse(ShippingRouteBase):
    id: int

    model_config = ConfigDict(from_attributes=True)