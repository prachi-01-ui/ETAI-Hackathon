from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.recommendation import ActionOutcome, DecisionAction


router = APIRouter(
    prefix="/outcomes",
    tags=["Action Outcomes"],
)


@router.get("/")
def get_outcomes(db: Session = Depends(get_db)):
    return db.query(ActionOutcome).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_outcome(
    decision_action_id: int,
    outcome_status: str,
    actual_cost: float = None,
    actual_benefit: float = None,
    actual_risk_reduction: float = None,
    supply_restored_percentage: float = None,
    notes: str = None,
    db: Session = Depends(get_db),
):
    # Check whether the decision exists
    decision = (
        db.query(DecisionAction)
        .filter(DecisionAction.id == decision_action_id)
        .first()
    )

    if not decision:
        raise HTTPException(
            status_code=404,
            detail="Decision action not found",
        )

    # Check whether an outcome already exists for this decision
    existing_outcome = (
        db.query(ActionOutcome)
        .filter(ActionOutcome.decision_action_id == decision_action_id)
        .first()
    )

    if existing_outcome:
        raise HTTPException(
            status_code=400,
            detail="Outcome already exists for this decision action",
        )

    outcome = ActionOutcome(
        decision_action_id=decision_action_id,
        outcome_status=outcome_status,
        actual_cost=actual_cost,
        actual_benefit=actual_benefit,
        actual_risk_reduction=actual_risk_reduction,
        supply_restored_percentage=supply_restored_percentage,
        notes=notes,
    )

    db.add(outcome)
    db.commit()
    db.refresh(outcome)

    return outcome


@router.get("/{outcome_id}")
def get_outcome(
    outcome_id: int,
    db: Session = Depends(get_db),
):
    outcome = (
        db.query(ActionOutcome)
        .filter(ActionOutcome.id == outcome_id)
        .first()
    )

    if not outcome:
        raise HTTPException(
            status_code=404,
            detail="Action outcome not found",
        )

    return outcome