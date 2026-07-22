from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ============================================================
# SCENARIO SCHEMAS
# ============================================================

class ScenarioBase(BaseModel):
    name: str
    description: Optional[str] = None
    scenario_type: str
    severity: str = "Medium"
    disruption_duration_days: Optional[int] = None
    disruption_percentage: float = 0.0
    is_demo_scenario: bool = False


class ScenarioCreate(ScenarioBase):
    pass


class ScenarioResponse(ScenarioBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================
# SIMULATION RUN SCHEMAS
# ============================================================

class SimulationRunBase(BaseModel):
    scenario_id: int
    risk_event_id: Optional[int] = None
    status: str = "Pending"
    confidence_score: float = 0.0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class SimulationRunCreate(SimulationRunBase):
    pass


class SimulationRunResponse(SimulationRunBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)