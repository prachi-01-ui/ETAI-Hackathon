from fastapi import APIRouter


router = APIRouter(
    prefix="/strategic-reserve",
    tags=["Strategic Reserve"],
)


# ============================================================
# GET STRATEGIC RESERVE OVERVIEW
# GET /strategic-reserve/
# ============================================================

@router.get("/")
def get_strategic_reserve():

    return {
        "total_reserve": 5.33,
        "total_reserve_unit": "Million Metric Tonnes",

        "days_of_supply": 9.5,

        "fill_level": 84,

        "emergency_level": "Moderate",

        "reserve_sites": [
            {
                "name": "Visakhapatnam",
                "capacity": 1.33,
                "fill_percentage": 92,
                "status": "Operational"
            },
            {
                "name": "Mangalore",
                "capacity": 1.50,
                "fill_percentage": 78,
                "status": "Operational"
            },
            {
                "name": "Padur",
                "capacity": 2.50,
                "fill_percentage": 82,
                "status": "Operational"
            }
        ],

        "ai_recommendation": (
            "Elevated geopolitical risk around the Strait of Hormuz "
            "may threaten crude oil supply continuity. Maintain reserve "
            "readiness and consider increasing strategic inventory while "
            "diversifying near-term crude import routes."
        ),

        "recommended_actions": [
            "Increase Reserve",
            "Diversify Imports"
        ]
    }