from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.risk_intelligence import (
    RiskEvent,
    RiskScoreHistory,
)
from backend.models.simulation import (
    Scenario,
    SimulationRun,
    SimulationImpact,
    DigitalTwinSnapshot,
    SimulationTimeline,
)
from backend.models.recommendation import Recommendation, DecisionAction

from backend.schemas.risk_intelligence import (
    RiskEventCreate,
    RiskEventResponse,
)

router = APIRouter(
    prefix="/risk-intelligence",
    tags=["Risk Intelligence"],
)

# CREATE RISK EVENT
# POST /risk-intelligence/events
@router.post(
    "/events",
    response_model=RiskEventResponse,
    status_code=201,
)
def create_risk_event(
    event: RiskEventCreate,
    db: Session = Depends(get_db),
):
    new_event = RiskEvent(**event.model_dump())

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event

# GET CRITICAL RISK EVENTS
# GET /risk-intelligence/events/critical
@router.get(
    "/events/critical",
    response_model=List[RiskEventResponse],
)
def get_critical_risk_events(
    db: Session = Depends(get_db),
):
    events = (
        db.query(RiskEvent)
        .filter(RiskEvent.risk_level == "Critical")
        .all()
    )

    return events

# GET ALL RISK EVENTS
@router.get("/events")
def get_risk_events(db: Session = Depends(get_db)):
    events = db.query(RiskEvent).all()
    return events

# ============================================================
# GET RISK SCORE TREND HISTORY
# GET /risk-intelligence/trends/risk-score
# ============================================================

@router.get("/trends/risk-score")
def get_risk_score_trend(
    db: Session = Depends(get_db),
):
    history = (
        db.query(RiskScoreHistory)
        .order_by(RiskScoreHistory.recorded_at.asc())
        .all()
    )

    return [
        {
            "id": item.id,
            "entity_type": item.entity_type,
            "entity_id": item.entity_id,
            "entity_name": item.entity_name,
            "risk_score": item.risk_score,
            "confidence_score": item.confidence_score,
            "risk_level": item.risk_level,
            "reason": item.reason,
            "recorded_at": item.recorded_at,
        }
        for item in history
    ]

# GET HIGH-RISK EVENTS
# GET /risk-intelligence/events/high-risk
@router.get(
    "/events/high-risk",
    response_model=List[RiskEventResponse],
)
def get_high_risk_events(
    db: Session = Depends(get_db),
):
    events = (
        db.query(RiskEvent)
        .filter(RiskEvent.risk_score >= 70)
        .all()
    )

    return events

# GET ONE RISK EVENT
@router.get("/events/{event_id}")
def get_risk_event(
    event_id: int,
    db: Session = Depends(get_db),
):
    event = (
        db.query(RiskEvent)
        .filter(RiskEvent.id == event_id)
        .first()
    )

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Risk event not found",
        )

    return event

# RUN RISK-TO-RECOMMENDATION WORKFLOW
# POST /risk-intelligence/events/{event_id}/run-workflow
@router.post("/events/{event_id}/run-workflow")
def run_risk_workflow(
    event_id: int,
    db: Session = Depends(get_db),
):
    # Get the risk event
    event = (
        db.query(RiskEvent)
        .filter(RiskEvent.id == event_id)
        .first()
    )

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Risk event not found",
        )

    # Create a disruption scenario
    scenario = Scenario(
        name=f"Disruption Scenario - {event.title}",
        description=event.description,
        scenario_type=event.event_type,
        severity=event.risk_level,
        disruption_percentage=60.0,
        is_demo_scenario=False,
    )

    db.add(scenario)
    db.flush()

    # Create simulation run
    simulation_run = SimulationRun(
        scenario_id=scenario.id,
        risk_event_id=event.id,
        status="Completed",
        confidence_score=event.confidence_score,
    )

    db.add(simulation_run)
    db.flush()

    # Create recommendation
    recommendation = Recommendation(
        simulation_run_id=simulation_run.id,
        risk_event_id=event.id,
        title="Activate Alternative Supply Strategy",
        description=(
            "Activate an alternative supply strategy to reduce "
            "exposure to the detected disruption."
        ),
        recommendation_type="Alternative Route",
        priority=event.risk_level,
        confidence_score=event.confidence_score,
        reasoning=event.explanation,
        expected_risk_reduction=45.0,
        status="Pending",
    )

    db.add(recommendation)
    db.commit()

    db.refresh(scenario)
    db.refresh(simulation_run)
    db.refresh(recommendation)
    
    # Create simulation impact automatically
    simulation_impact = SimulationImpact(
        simulation_run_id=simulation_run.id,
        supply_disruption_percentage=35,
        supply_gap=25,
        shipment_delay_days=7,
        refinery_utilization_impact=20,
        spr_runway_days=30,
        estimated_economic_loss=5000000,
        commodity_price_impact_percentage=12,
        summary="Simulation predicts significant supply disruption, shipping delays, and economic impact.",
    )

    db.add(simulation_impact)
    db.commit()
    db.refresh(simulation_impact)
    
    # Create digital twin snapshots automatically
    digital_twin_snapshots = [
        DigitalTwinSnapshot(
            simulation_run_id=simulation_run.id,
            entity_type="route",
            entity_id=1,
            entity_name="Strait of Hormuz Shipping Route",
            simulation_day=0,
         operational_status="At Risk",
            capacity_utilization=65,
            risk_score=92,
            supply_available=65,
            delay_days=0,
            notes="Critical geopolitical disruption risk detected.",
        ),
        DigitalTwinSnapshot(
            simulation_run_id=simulation_run.id,
            entity_type="route",
            entity_id=1,
            entity_name="Strait of Hormuz Shipping Route",
            simulation_day=7,
            operational_status="Disrupted",
            capacity_utilization=35,
            risk_score=95,
            supply_available=35,
            delay_days=7,
            notes="Supply capacity reduced due to simulated disruption.",
        ),
    ]
    db.add_all(digital_twin_snapshots)
    db.commit()
    
    # Create simulation timeline automatically
    simulation_timeline = [
        SimulationTimeline(
            simulation_run_id=simulation_run.id,
            simulation_day=0,
            event_type="Risk Detected",
            title="Critical Supply Route Risk Detected",
            description="High geopolitical risk detected along the Strait of Hormuz shipping route.",
            risk_score=92,
            supply_gap=10,
            economic_loss=1000000,
        ),
         SimulationTimeline(
            simulation_run_id=simulation_run.id,
            simulation_day=3,
            event_type="Supply Disruption",
            title="Supply Gap Increased",
            description="Disruption begins affecting crude oil supply and shipping operations.",
            risk_score=94,
            supply_gap=20,
            economic_loss=3000000,
        ),
        SimulationTimeline(
            simulation_run_id=simulation_run.id,
            simulation_day=7,
            event_type="Major Disruption",
            title="Route Capacity Severely Reduced",
            description="Shipping route capacity falls significantly due to the simulated disruption.",
            risk_score=95,
            supply_gap=25,
            economic_loss=5000000,
        ),
    ]
    
    db.add_all(simulation_timeline)
    db.commit()
    
    # Create automatic decision action
    decision= DecisionAction(
        recommendation_id=recommendation.id,
        action_type="Pending",
        decided_by="AI Risk Intelligence Agent",
        decision_reason="Automatically generated from the risk intelligence workflow.",
    )
    
    db.add(decision)
    db.commit()
    db.refresh(decision)

    return {
        "message": "Risk workflow completed successfully",
        "risk_event_id": event.id,
        "scenario_id": scenario.id,
        "simulation_run_id": simulation_run.id,
        "recommendation_id": recommendation.id,
        "decision_id": decision.id,
    }