from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.risk_intelligence import RiskEvent
from ai_agents.orchestrator import agent_orchestrator


router = APIRouter(
    prefix="/agents",
    tags=["AI Agents"],
)


@router.post("/analyze/{risk_event_id}")
def analyze_risk_with_agents(
    risk_event_id: int,
    db: Session = Depends(get_db),
):
    risk_event = (
        db.query(RiskEvent)
        .filter(RiskEvent.id == risk_event_id)
        .first()
    )

    if not risk_event:
        raise HTTPException(
            status_code=404,
            detail="Risk event not found",
        )

    result = agent_orchestrator.process_risk_event(risk_event)

    return result