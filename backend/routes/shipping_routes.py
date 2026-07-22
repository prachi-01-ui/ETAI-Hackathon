from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.supply_chain import ShippingRoute
from backend.schemas.supply_chain import (
    ShippingRouteCreate,
    ShippingRouteResponse,
)


router = APIRouter(
    prefix="/shipping-routes",
    tags=["Shipping Routes"],
)


# CREATE SHIPPING ROUTE
# POST /shipping-routes/
@router.post("/", response_model=ShippingRouteResponse, status_code=201)
def create_shipping_route(
    route: ShippingRouteCreate,
    db: Session = Depends(get_db),
):
    new_route = ShippingRoute(**route.model_dump())

    db.add(new_route)
    db.commit()
    db.refresh(new_route)

    return new_route


# GET ALL SHIPPING ROUTES
# GET /shipping-routes/
@router.get("/", response_model=List[ShippingRouteResponse])
def get_shipping_routes(
    db: Session = Depends(get_db),
):
    routes = db.query(ShippingRoute).all()

    return routes


# GET ONE SHIPPING ROUTE
# GET /shipping-routes/{route_id}
@router.get("/{route_id}", response_model=ShippingRouteResponse)
def get_shipping_route(
    route_id: int,
    db: Session = Depends(get_db),
):
    route = (
        db.query(ShippingRoute)
        .filter(ShippingRoute.id == route_id)
        .first()
    )

    if route is None:
        raise HTTPException(
            status_code=404,
            detail="Shipping route not found",
        )

    return route