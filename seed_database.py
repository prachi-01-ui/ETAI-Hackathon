import json
from pathlib import Path

from backend.database import SessionLocal

from backend.models.supply_chain import (
    Supplier,
    Port,
    Refinery,
    ShippingRoute,
)

from backend.models.risk_intelligence import RiskEvent


# ============================================================
# DATA FILE
# ============================================================

DATA_FILE = (
    Path(__file__).parent
    / "data"
    / "supply_chain_data.json"
)


def seed_database():

    db = SessionLocal()

    try:

        # ====================================================
        # LOAD JSON DATA
        # ====================================================

        with open(
            DATA_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)


        # ====================================================
        # 1. SUPPLIERS
        # ====================================================

        for item in data.get("suppliers", []):

            existing = (
                db.query(Supplier)
                .filter(Supplier.id == item["id"])
                .first()
            )

            if existing:
                continue

            supplier = Supplier(
                id=item["id"],
                name=item["name"],
                country=item["country"],

                # JSON commodity -> model commodity_type
                commodity_type=item["commodity"],

                # JSON daily_capacity_barrels
                # -> model production_capacity
                production_capacity=item.get(
                    "daily_capacity_barrels"
                ),

                reliability_score=item.get(
                    "reliability_score",
                    0,
                ),

                current_risk_score=0,

                status="Active",
            )

            db.add(supplier)

        # Make suppliers available before inserting ports
        db.flush()


        # ====================================================
        # 2. PORTS
        # ====================================================

        # Latitude and longitude are required by your
        # SQLAlchemy Port model but are not present in JSON.

        port_coordinates = {

            "Ras Tanura Port": (
                26.64,
                50.16,
            ),

            "Mundra Port": (
                22.74,
                69.70,
            ),
        }


        for item in data.get("ports", []):

            existing = (
                db.query(Port)
                .filter(Port.id == item["id"])
                .first()
            )

            if existing:
                continue


            latitude, longitude = (
                port_coordinates.get(
                    item["name"],
                    (0.0, 0.0),
                )
            )


            # Associate Ras Tanura with the
            # Middle East supplier.

            supplier_id = None

            if item["name"] == "Ras Tanura Port":
                supplier_id = 1


            port = Port(
                id=item["id"],
                name=item["name"],
                country=item["country"],

                latitude=latitude,
                longitude=longitude,

                capacity=None,

                operational_status="Operational",

                congestion_level=0,

                current_risk_score=0,

                supplier_id=supplier_id,
            )

            db.add(port)


        # Make ports available before creating routes
        db.flush()


        # ====================================================
        # 3. REFINERIES
        # ====================================================

        refinery_coordinates = {

            "Indian Energy Refinery": (
                22.40,
                69.80,
            ),
        }


        for item in data.get("refineries", []):

            existing = (
                db.query(Refinery)
                .filter(Refinery.id == item["id"])
                .first()
            )

            if existing:
                continue


            latitude, longitude = (
                refinery_coordinates.get(
                    item["name"],
                    (0.0, 0.0),
                )
            )


            refinery = Refinery(
                id=item["id"],
                name=item["name"],
                country=item["country"],

                latitude=latitude,
                longitude=longitude,

                # JSON daily_requirement_barrels
                # -> model processing_capacity
                processing_capacity=item.get(
                    "daily_requirement_barrels"
                ),

                current_utilization=0,

                operational_status="Operational",

                current_risk_score=0,
            )

            db.add(refinery)


        db.flush()


        # ====================================================
        # 4. SHIPPING ROUTES
        # ====================================================

        risk_mapping = {
            "Low": 20,
            "Medium": 50,
            "High": 75,
            "Critical": 90,
        }


        for item in data.get(
            "shipping_routes",
            [],
        ):

            existing = (
                db.query(ShippingRoute)
                .filter(
                    ShippingRoute.id
                    == item["id"]
                )
                .first()
            )

            if existing:
                continue


            origin = (
                db.query(Port)
                .filter(
                    Port.name
                    == item["origin_port"]
                )
                .first()
            )


            destination = (
                db.query(Port)
                .filter(
                    Port.name
                    == item["destination_port"]
                )
                .first()
            )


            if not origin or not destination:

                print(
                    f"Skipping route "
                    f"{item['name']}: "
                    "origin or destination "
                    "port not found."
                )

                continue


            shipping_route = ShippingRoute(
                id=item["id"],
                name=item["name"],

                origin_port_id=origin.id,

                destination_port_id=(
                    destination.id
                ),

                distance_km=None,

                # JSON transit_days
                # -> estimated_travel_days
                estimated_travel_days=(
                    item.get(
                        "transit_days"
                    )
                ),

                current_risk_score=(
                    risk_mapping.get(
                        item.get(
                            "risk_level"
                        ),
                        0,
                    )
                ),

                status=item.get(
                    "status",
                    "Operational",
                ),

                risk_reason=(
                    f"{item.get('risk_level', 'Unknown')} "
                    "route risk"
                ),
            )

            db.add(shipping_route)


        db.flush()


        # ====================================================
        # 5. RISK EVENTS
        # ====================================================

        for item in data.get(
            "risk_events",
            [],
        ):

            existing = (
                db.query(RiskEvent)
                .filter(
                    RiskEvent.id
                    == item["id"]
                )
                .first()
            )

            if existing:
                continue


            risk_event = RiskEvent(

                id=item["id"],

                title=item["title"],


                # Preserve affected route information
                # inside description.

                description=(
                    f"Affected route: "
                    f"{item.get('affected_route', 'Unknown')}"
                ),


                # JSON risk_type
                # -> model event_type

                event_type=item.get(
                    "risk_type",
                    "Supply Chain Disruption",
                ),


                risk_score=item.get(
                    "risk_score",
                    0,
                ),


                # JSON impact
                # -> model risk_level

                risk_level=item.get(
                    "impact",
                    "Low",
                ),


                # JSON probability is 0-1.
                # Model confidence_score uses percentage.

                confidence_score=(
                    float(
                        item.get(
                            "probability",
                            0,
                        )
                    )
                    * 100
                ),


                explanation=(
                    f"Risk affects "
                    f"{item.get('affected_route', 'an energy route')} "
                    f"with probability "
                    f"{item.get('probability', 0)}."
                ),


                multi_source_verified=False,


                status=item.get(
                    "status",
                    "Active",
                ),
            )

            db.add(risk_event)


        # ====================================================
        # COMMIT EVERYTHING
        # ====================================================

        db.commit()

        print(
            "Database seeded successfully!"
        )


    except Exception as error:

        db.rollback()

        print(
            f"Database seeding failed: {error}"
        )

        raise


    finally:

        db.close()


# ============================================================
# RUN SEED SCRIPT
# ============================================================

if __name__ == "__main__":

    print("Seeding database...")

    seed_database()