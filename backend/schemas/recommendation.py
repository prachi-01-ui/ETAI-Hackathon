from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# ============================================================
# RECOMMENDATION SCHEMAS
# ============================================================

class RecommendationBase(BaseModel):
    simulation_run_id: Optional[int] = None
    risk_event_id: Optional[int] = None

    title: str
    description: str

    # Alternative Supplier, Alternative Route,
    # SPR Release, Procurement Action, Inventory Adjustment
    recommendation_type: str

    # Low, Medium, High, Critical
    priority: str = "Medium"

    confidence_score: float = 0.0

    # Explainable AI reasoning
    reasoning: Optional[str] = None

    estimated_cost: Optional[float] = None
    estimated_benefit: Optional[float] = None
    expected_risk_reduction: Optional[float] = None

    # Pending, Accepted, Rejected, Executed
    status: str = "Pending"


class RecommendationCreate(RecommendationBase):
    pass


class RecommendationResponse(RecommendationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)