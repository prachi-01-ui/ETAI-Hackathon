from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ============================================================
# RISK EVENT SCHEMAS
# ============================================================

class RiskEventBase(BaseModel):
    title: str
    description: Optional[str] = None

    # Examples: War, Sanctions, Political Tension,
    # Port Closure, Natural Disaster, Supply Disruption
    event_type: str

    country: Optional[str] = None
    region: Optional[str] = None

    source_name: Optional[str] = None
    source_url: Optional[str] = None

    published_at: Optional[datetime] = None

    # AI-generated risk assessment
    risk_score: float = 0.0

    # Low, Medium, High, Critical
    risk_level: str = "Low"

    # AI confidence in the assessment
    confidence_score: float = 0.0

    # Explainable AI reasoning
    explanation: Optional[str] = None

    # Whether multiple independent sources confirm the event
    multi_source_verified: bool = False

    status: str = "Active"


class RiskEventCreate(RiskEventBase):
    pass


class RiskEventResponse(RiskEventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# ALERT SCHEMAS
# ============================================================

class AlertBase(BaseModel):
    risk_event_id: Optional[int] = None

    title: str
    message: str

    # Info, Warning, High, Critical
    severity: str

    # geopolitical, route, supplier, port, refinery
    alert_type: str

    is_read: bool = False
    is_resolved: bool = False


class AlertCreate(AlertBase):
    pass


class AlertResponse(AlertBase):
    id: int
    created_at: datetime
    resolved_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)