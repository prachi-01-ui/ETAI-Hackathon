from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.supply_chain import Port
from backend.schemas.supply_chain import (
    PortCreate,
    PortResponse,
)


router = APIRouter(
    prefix="/ports",
    tags=["Ports"],
)


# ============================================================
# CREATE PORT
# POST /ports/
# ============================================================

@router.post(
    "/",
    response_model=PortResponse,
    status_code=201,
)
def create_port(
    port: PortCreate,
    db: Session = Depends(get_db),
):
    new_port = Port(**port.model_dump())

    db.add(new_port)
    db.commit()
    db.refresh(new_port)

    return new_port


# ============================================================
# GET ALL PORTS
# GET /ports/
# ============================================================

@router.get(
    "/",
    response_model=List[PortResponse],
)
def get_ports(
    db: Session = Depends(get_db),
):
    ports = db.query(Port).all()

    return ports


# ============================================================
# GET PORT GEOSPATIAL MAP DATA
# GET /ports/map-data
# ============================================================

@router.get("/map-data")
def get_port_map_data(
    db: Session = Depends(get_db),
):
    """
    Returns port geospatial information using PostGIS.

    ST_X extracts longitude from the PostGIS POINT.
    ST_Y extracts latitude from the PostGIS POINT.

    The response is designed for Leaflet/Mapbox visualization.
    """

    ports = (
        db.query(
            Port.id,
            Port.name,
            Port.country,
            Port.operational_status,
            Port.congestion_level,
            Port.current_risk_score,
            func.ST_X(Port.location).label("longitude"),
            func.ST_Y(Port.location).label("latitude"),
        )
        .filter(Port.location.isnot(None))
        .all()
    )

    return [
        {
            "id": port.id,
            "name": port.name,
            "country": port.country,
            "latitude": port.latitude,
            "longitude": port.longitude,
            "operational_status": port.operational_status,
            "congestion_level": port.congestion_level,
            "risk_score": port.current_risk_score,
        }
        for port in ports
    ]


# ============================================================
# GET ONE PORT
# GET /ports/{port_id}
# ============================================================

@router.get(
    "/{port_id}",
    response_model=PortResponse,
)
def get_port(
    port_id: int,
    db: Session = Depends(get_db),
):
    port = (
        db.query(Port)
        .filter(Port.id == port_id)
        .first()
    )

    if port is None:
        raise HTTPException(
            status_code=404,
            detail="Port not found",
        )

    return port