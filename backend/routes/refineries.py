from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.supply_chain import Refinery
from backend.schemas.supply_chain import (
    RefineryCreate,
    RefineryResponse,
)


router = APIRouter(
    prefix="/refineries",
    tags=["Refineries"],
)


# CREATE REFINERY
# POST /refineries/
@router.post("/", response_model=RefineryResponse, status_code=201)
def create_refinery(
    refinery: RefineryCreate,
    db: Session = Depends(get_db),
):
    new_refinery = Refinery(**refinery.model_dump())

    db.add(new_refinery)
    db.commit()
    db.refresh(new_refinery)

    return new_refinery


# GET ALL REFINERIES
# GET /refineries/
@router.get("/", response_model=List[RefineryResponse])
def get_refineries(
    db: Session = Depends(get_db),
):
    refineries = db.query(Refinery).all()

    return refineries


# GET ONE REFINERY
# GET /refineries/{refinery_id}
@router.get("/{refinery_id}", response_model=RefineryResponse)
def get_refinery(
    refinery_id: int,
    db: Session = Depends(get_db),
):
    refinery = (
        db.query(Refinery)
        .filter(Refinery.id == refinery_id)
        .first()
    )

    if refinery is None:
        raise HTTPException(
            status_code=404,
            detail="Refinery not found",
        )

    return refinery