import os

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine
from backend.routes.suppliers import router as suppliers_router
from backend.routes.ports import router as ports_router
from backend.routes.refineries import router as refineries_router
from backend.routes.shipping_routes import router as shipping_routes_router
from backend.routes.risk_intelligence import router as risk_intelligence_router
from backend.routes.recommendations import router as recommendations_router
from backend.routes.simulation import router as simulation_router
from backend.routes.decisions import router as decisions_router
from backend.routes.outcomes import router as outcomes_router
from backend.routes.strategic_reserve import router as strategic_reserve_router
from backend.routes.agents import router as agents_router
from backend.routes.knowledge_graph import router as knowledge_graph_router
from backend.routes.rag import router as rag_router
from backend.routes.news import router as news_router
from backend.services.gemini_service import gemini_service

# Load environment variables
load_dotenv()

APP_NAME = os.getenv("APP_NAME", "AI Risk Intelligence Agent")

app = FastAPI(
    title=APP_NAME,
    description="Energy Supply Chain Resilience Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(suppliers_router)
app.include_router(ports_router)
app.include_router(refineries_router)
app.include_router(shipping_routes_router)
app.include_router(risk_intelligence_router)
app.include_router(recommendations_router)
app.include_router(simulation_router)
app.include_router(decisions_router)
app.include_router(outcomes_router)
app.include_router(strategic_reserve_router)
app.include_router(agents_router)
app.include_router(knowledge_graph_router)
app.include_router(rag_router)
app.include_router(news_router)

@app.get("/")
def root():
    return {
        "application": APP_NAME,
        "platform": "Energy Supply Chain Resilience Platform",
        "status": "running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": APP_NAME,
    }


@app.get("/health/database")
def database_health_check():
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT current_database(), PostGIS_Version();")
            ).fetchone()

        return {
            "status": "healthy",
            "database": result[0],
            "postgis_version": result[1],
        }

    except Exception as error:
        return {
            "status": "unhealthy",
            "error": str(error),
        }
        
@app.post("/gemini/recommendation")
def generate_gemini_recommendation(payload: dict):

    prompt = f"""
You are an AI decision intelligence agent for an Energy Supply Chain
Resilience Platform.

Use the following operational data and generate a concise executive
recommendation.

Simulation:
{payload.get("simulation")}

Impact:
{payload.get("impact")}

Strategic Reserve:
{payload.get("reserve")}

Refineries:
{payload.get("refineries")}

Provide:

1. Risk Summary
2. Recommended Actions
3. Expected Operational Impact

Keep the answer under 250 words.
"""

    recommendation = gemini_service.generate_response(prompt)

    return {
        "recommendation": recommendation
    }