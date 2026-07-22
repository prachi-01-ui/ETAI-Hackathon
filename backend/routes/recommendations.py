from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.recommendation import (
    DecisionAction,
    Recommendation,
)

from backend.schemas.recommendation import (
    RecommendationCreate,
    RecommendationResponse,
)


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


# CREATE RECOMMENDATION
# POST /recommendations/
@router.post(
    "/",
    response_model=RecommendationResponse,
    status_code=201,
)
def create_recommendation(
    recommendation: RecommendationCreate,
    db: Session = Depends(get_db),
):
    new_recommendation = Recommendation(
        **recommendation.model_dump()
    )

    db.add(new_recommendation)
    db.commit()
    db.refresh(new_recommendation)

    return new_recommendation


# GET ALL RECOMMENDATIONS
# GET /recommendations/
@router.get(
    "/",
    response_model=List[RecommendationResponse],
)
def get_recommendations(
    db: Session = Depends(get_db),
):
    recommendations = db.query(Recommendation).all()

    return recommendations

# GET RECOMMENDATIONS SELECTED AS AGENT DECISIONS
# GET /recommendations/selected/decisions
@router.get("/selected/decisions")
def get_selected_recommendations(
    db: Session = Depends(get_db),
):
    selected_recommendations = (
        db.query(Recommendation)
        .join(
            DecisionAction,
            DecisionAction.recommendation_id == Recommendation.id,
        )
        .order_by(DecisionAction.id.desc())
        .all()
    )

    return selected_recommendations

# GET ONE RECOMMENDATION
# GET /recommendations/{recommendation_id}
@router.get(
    "/{recommendation_id}",
    response_model=RecommendationResponse,
)
def get_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
):
    recommendation = (
        db.query(Recommendation)
        .filter(Recommendation.id == recommendation_id)
        .first()
    )

    if recommendation is None:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    return recommendation

# ACCEPT / SELECT RECOMMENDATION
# PUT /recommendations/{recommendation_id}/accept
@router.put("/{recommendation_id}/accept")
def accept_recommendation(
    recommendation_id: int,
    db: Session = Depends(get_db),
):
    recommendation = (
        db.query(Recommendation)
        .filter(Recommendation.id == recommendation_id)
        .first()
    )

    if recommendation is None:
        raise HTTPException(
            status_code=404,
            detail="Recommendation not found",
        )

    # Check whether this recommendation already became a decision
    existing_decision = (
        db.query(DecisionAction)
        .filter(
            DecisionAction.recommendation_id == recommendation_id
        )
        .first()
    )

    if existing_decision:
        raise HTTPException(
            status_code=400,
            detail="A decision already exists for this recommendation",
        )

    # Mark recommendation as accepted
    recommendation.status = "Accepted"

    # Create a new pending operational decision
    decision = DecisionAction(
        recommendation_id=recommendation.id,
        action_type="Pending",
        decided_by="AI Risk Intelligence Agent",
        decision_reason=(
            recommendation.reasoning
            or "Recommendation accepted for operational execution."
        ),
    )

    db.add(decision)
    db.commit()

    db.refresh(recommendation)
    db.refresh(decision)

    return {
        "message": "Recommendation accepted and decision created successfully",
        "recommendation_id": recommendation.id,
        "decision_id": decision.id,
        "decision_status": decision.action_type,
    }
    
