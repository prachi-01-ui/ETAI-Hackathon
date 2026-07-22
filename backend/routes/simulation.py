from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.simulation import (
    Scenario,
    SimulationRun,
    SimulationImpact,
    DigitalTwinSnapshot,
    SimulationTimeline,
)
from backend.schemas.simulation import (
    ScenarioCreate,
    ScenarioResponse,
    SimulationRunCreate,
    SimulationRunResponse,
)

from simulation.simulation_engine import simulation_engine

router = APIRouter(
    prefix="/simulations",
    tags=["Simulations"],
)


# ============================================================
# CREATE SCENARIO
# POST /simulations/scenarios
# ============================================================

@router.post(
    "/scenarios",
    response_model=ScenarioResponse,
    status_code=201,
)
def create_scenario(
    scenario: ScenarioCreate,
    db: Session = Depends(get_db),
):
    new_scenario = Scenario(**scenario.model_dump())

    db.add(new_scenario)
    db.commit()
    db.refresh(new_scenario)

    return new_scenario


# ============================================================
# GET ALL SCENARIOS
# GET /simulations/scenarios
# ============================================================

@router.get(
    "/scenarios",
    response_model=List[ScenarioResponse],
)
def get_scenarios(
    db: Session = Depends(get_db),
):
    return db.query(Scenario).all()


# ============================================================
# GET ONE SCENARIO
# GET /simulations/scenarios/{scenario_id}
# ============================================================

@router.get(
    "/scenarios/{scenario_id}",
    response_model=ScenarioResponse,
)
def get_scenario(
    scenario_id: int,
    db: Session = Depends(get_db),
):
    scenario = (
        db.query(Scenario)
        .filter(Scenario.id == scenario_id)
        .first()
    )

    if scenario is None:
        raise HTTPException(
            status_code=404,
            detail="Scenario not found",
        )

    return scenario


# ============================================================
# CREATE SIMULATION RUN
# POST /simulations/runs
# ============================================================

@router.post(
    "/runs",
    response_model=SimulationRunResponse,
    status_code=201,
)
def create_simulation_run(
    simulation_run: SimulationRunCreate,
    db: Session = Depends(get_db),
):
    scenario = (
        db.query(Scenario)
        .filter(Scenario.id == simulation_run.scenario_id)
        .first()
    )

    if scenario is None:
        raise HTTPException(
            status_code=404,
            detail="Scenario not found",
        )

    new_run = SimulationRun(**simulation_run.model_dump())

    db.add(new_run)
    db.commit()
    db.refresh(new_run)

    # --------------------------------------------------
    # Create Simulation Impact automatically
    # --------------------------------------------------

    impact = SimulationImpact(
        simulation_run_id=new_run.id,

        supply_disruption_percentage=60,

        supply_gap=35,

        shipment_delay_days=7,

        refinery_utilization_impact=28,

        spr_runway_days=42,

        estimated_economic_loss=4.8,

        commodity_price_impact_percentage=12.5,

        summary="Severe disruption in the Strait of Hormuz reduces crude oil supply, increases tanker delays, raises oil prices, and requires Strategic Petroleum Reserve support."
    )
    
    db.add(impact)
    db.commit()


    return new_run


# ============================================================
# GET ALL SIMULATION RUNS
# GET /simulations/runs
# ============================================================

@router.get(
    "/runs",
    response_model=List[SimulationRunResponse],
)
def get_simulation_runs(
    db: Session = Depends(get_db),
):
    return db.query(SimulationRun).all()


# ============================================================
# GET ONE SIMULATION RUN
# GET /simulations/runs/{run_id}
# ============================================================

@router.get(
    "/runs/{run_id}",
    response_model=SimulationRunResponse,
)
def get_simulation_run(
    run_id: int,
    db: Session = Depends(get_db),
):
    simulation_run = (
        db.query(SimulationRun)
        .filter(SimulationRun.id == run_id)
        .first()
    )

    if simulation_run is None:
        raise HTTPException(
            status_code=404,
            detail="Simulation run not found",
        )

    return simulation_run

# ============================================================
# GET SIMULATION IMPACT
# GET /simulations/runs/{run_id}/impact
# ============================================================

@router.get("/runs/{run_id}/impact")
def get_simulation_impact(
    run_id: int,
    db: Session = Depends(get_db),
):
    impact = (
        db.query(SimulationImpact)
        .filter(SimulationImpact.simulation_run_id == run_id)
        .first()
    )

    if impact is None:
        raise HTTPException(
            status_code=404,
            detail="Simulation impact not found",
        )

    return impact

# ============================================================
# GET DIGITAL TWIN SNAPSHOTS FOR A SIMULATION RUN
# GET /simulations/runs/{run_id}/digital-twin
# ============================================================

@router.get("/runs/{run_id}/digital-twin")
def get_digital_twin_snapshots(
    run_id: int,
    db: Session = Depends(get_db),
):
    snapshots = (
        db.query(DigitalTwinSnapshot)
        .filter(DigitalTwinSnapshot.simulation_run_id == run_id)
        .all()
    )

    return snapshots

# ============================================================
# GET SIMULATION TIMELINE
# GET /simulations/runs/{run_id}/timeline
# ============================================================

@router.get("/runs/{run_id}/timeline")
def get_simulation_timeline(
    run_id: int,
    db: Session = Depends(get_db),
):
    timeline = (
        db.query(SimulationTimeline)
        .filter(SimulationTimeline.simulation_run_id == run_id)
        .order_by(SimulationTimeline.simulation_day)
        .all()
    )

    return timeline

# ============================================================
# RUN AI-DRIVEN DISRUPTION SIMULATION
# POST /simulations/engine/run/{scenario_id}
# ============================================================

@router.post("/engine/run/{scenario_id}")
def run_simulation_engine(
    scenario_id: int,
):
    result = simulation_engine.run_simulation(
        scenario_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Simulation scenario not found",
        )

    return result