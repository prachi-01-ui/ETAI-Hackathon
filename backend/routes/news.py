import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.news_service import news_service
from backend.services.gemini_service import gemini_service


router = APIRouter(
    prefix="/news",
    tags=["News Intelligence"],
)

class NewsAnalysisRequest(BaseModel):
    title: str
    description: str = ""
    source: str = "Unknown"


# ============================================================
# GET ENERGY & SUPPLY-CHAIN RISK NEWS
# GET /news/energy-risk
# ============================================================

@router.get("/energy-risk")
def get_energy_risk_news(
    limit: int = 10,
):
    result = news_service.get_energy_risk_news(
        page_size=limit
    )

    if result.get("status") == "error":
        raise HTTPException(
            status_code=502,
            detail=result.get(
                "message",
                "Failed to retrieve news intelligence",
            ),
        )

    return result


# ============================================================
# ANALYZE LIVE NEWS WITH GEMINI
# POST /news/analyze
# ============================================================

@router.post("/analyze")
def analyze_news(
    article: NewsAnalysisRequest,
):
    try:
        ai_response = gemini_service.analyze_news_risk(
            title=article.title,
            description=article.description,
            source=article.source,
        )

        # Gemini may occasionally wrap JSON in markdown fences.
        cleaned_response = ai_response.strip()

        if cleaned_response.startswith("```json"):
            cleaned_response = cleaned_response[7:]

        elif cleaned_response.startswith("```"):
            cleaned_response = cleaned_response[3:]

        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response[:-3]

        cleaned_response = cleaned_response.strip()

        analysis = json.loads(cleaned_response)

        return {
            "status": "success",
            "analysis": analysis,
        }

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="Gemini returned an invalid JSON response",
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error),
        )