from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.supply_chain import Supplier
from backend.schemas.supply_chain import (
    SupplierCreate,
    SupplierResponse,
)


router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
)


# ============================================================
# CREATE SUPPLIER
# POST /suppliers/
# ============================================================

@router.post("/", response_model=SupplierResponse, status_code=201)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
):
    new_supplier = Supplier(**supplier.model_dump())

    db.add(new_supplier)
    db.commit()
    db.refresh(new_supplier)

    return new_supplier


# ============================================================
# GET ALL SUPPLIERS
# GET /suppliers/
# ============================================================

@router.get("/", response_model=List[SupplierResponse])
def get_suppliers(
    db: Session = Depends(get_db),
):
    suppliers = db.query(Supplier).all()

    return suppliers


# ============================================================
# GET ONE SUPPLIER
# GET /suppliers/{supplier_id}
# ============================================================

@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
):
    supplier = (
        db.query(Supplier)
        .filter(Supplier.id == supplier_id)
        .first()
    )

    if supplier is None:
        raise HTTPException(
            status_code=404,
            detail="Supplier not found",
        )

    return supplier