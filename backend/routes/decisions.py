from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.recommendation import (
    DecisionAction,
    Recommendation,
    ActionOutcome,
)


router = APIRouter(
    prefix="/decisions",
    tags=["Decision Actions"],
)


@router.get("/")
def get_decisions(db: Session = Depends(get_db)):
    return db.query(DecisionAction).all()


@router.post("/", status_code=201)
def create_decision(
    recommendation_id: int,
    action_type: str,
    decided_by: str = None,
    decision_reason: str = None,
    db: Session = Depends(get_db),
):
    recommendation = (
        db.query(Recommendation)
        .filter(Recommendation.id == recommendation_id)
        .first()
    )

    if not recommendation:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    decision = DecisionAction(
        recommendation_id=recommendation_id,
        action_type=action_type,
        decided_by=decided_by,
        decision_reason=decision_reason,
    )

    # Update recommendation status based on decision
    recommendation.status = action_type

    db.add(decision)
    db.commit()
    db.refresh(decision)

    return decision


@router.get("/{decision_id}")
def get_decision(
    decision_id: int,
    db: Session = Depends(get_db),
):
    decision = (
        db.query(DecisionAction)
        .filter(DecisionAction.id == decision_id)
        .first()
    )

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Decision not found",
        )

    return decision

@router.put("/{decision_id}/execute")
def execute_decision(
    decision_id: int,
    db: Session = Depends(get_db),
):
    decision = (
        db.query(DecisionAction)
        .filter(DecisionAction.id == decision_id)
        .first()
    )

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Decision action not found",
        )

    decision.action_type = "Executed"
    decision.executed_at = datetime.now(timezone.utc)
    
    # Automatically create an outcome when the decision is executed
    existing_outcome=(
        db.query(ActionOutcome)
        .filter(ActionOutcome.decision_action_id==decision.id)
        .first()
    )
    
    if not existing_outcome:
        outcome=ActionOutcome(
            decision_action_id=decision.id,
            outcome_status="Successful",
            actual_cost=450000,
            actual_benefit=2000000,
            actual_risk_reduction=45,
            supply_restored_percentage=90,
            notes="Outcome automatically created when the decision was executed.",
        )
        db.add(outcome)
    
    db.commit()
    db.refresh(decision)

    return decision