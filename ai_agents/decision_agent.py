import json
from datetime import datetime, timezone

from rag.rag_service import rag_service
from backend.services.gemini_service import gemini_service


class DecisionAgent:
    """
    AI Decision Agent that uses FAISS RAG + Gemini
    to generate grounded operational decisions.
    """

    def __init__(self):
        self.name = "AI Decision Agent"

    def make_decision(self, risk_assessment):

        requires_action = risk_assessment.get(
            "autonomous_decision",
            False,
        )

        risk_event_id = risk_assessment.get(
            "risk_event_id"
        )

        risk_score = risk_assessment.get(
            "risk_score",
            0,
        )

        severity = risk_assessment.get(
            "severity",
            "Unknown",
        )

        # --------------------------------------------------------
        # If risk does not require intervention
        # --------------------------------------------------------

        if not requires_action:

            return {
                "decision": "Continue Risk Monitoring",
                "action_type": "Monitoring",
                "priority": "Low",
                "status": "Monitoring",
                "reason": (
                    "Current risk assessment does not require "
                    "immediate operational intervention."
                ),
                "agent": self.name,
                "risk_event_id": risk_event_id,
                "ai_generated": False,
                "decided_at": datetime.now(
                    timezone.utc
                ).isoformat(),
            }

        # --------------------------------------------------------
        # Retrieve relevant knowledge using FAISS RAG
        # --------------------------------------------------------

        query = (
            f"Energy supply chain risk with severity {severity}, "
            f"risk score {risk_score}. "
            f"Find relevant disruption scenarios, alternative "
            f"supply routes, suppliers and mitigation strategies."
        )

        retrieved_documents = rag_service.retrieve(
            query,
            top_k=3,
        )

        context = json.dumps(
            [
                document["content"]
                for document in retrieved_documents
            ],
            ensure_ascii=False,
        )

        # --------------------------------------------------------
        # Generate grounded decision using Gemini
        # --------------------------------------------------------

        try:

            ai_reasoning = (
                gemini_service.generate_grounded_response(
                    query=(
                        "Analyse this supply-chain risk and determine "
                        "the best operational mitigation strategy. "
                        "Compare available alternatives and recommend "
                        "the most appropriate response."
                    ),
                    context=context,
                )
            )

            return {
                "decision": "AI Generated Mitigation Strategy",
                "action_type": "AI Decision Intelligence",
                "priority": (
                    "Critical"
                    if str(severity).lower() == "critical"
                    else "High"
                ),
                "status": "Recommended",
                "reason": ai_reasoning,
                "agent": self.name,
                "risk_event_id": risk_event_id,
                "risk_score": risk_score,
                "severity": severity,
                "ai_generated": True,
                "llm": "Gemini",
                "rag_enabled": True,
                "retrieved_sources": [
                    document["source"]
                    for document in retrieved_documents
                ],
                "decided_at": datetime.now(
                    timezone.utc
                ).isoformat(),
            }

        # --------------------------------------------------------
        # Safe fallback if Gemini/API becomes unavailable
        # --------------------------------------------------------

        except Exception as error:

            return {
                "decision": "Activate Alternative Supply Strategy",
                "action_type": "Fallback Mitigation",
                "priority": "Critical",
                "status": "Recommended",
                "reason": (
                    "AI service was temporarily unavailable. "
                    "Fallback supply-chain mitigation activated."
                ),
                "agent": self.name,
                "risk_event_id": risk_event_id,
                "risk_score": risk_score,
                "severity": severity,
                "ai_generated": False,
                "rag_enabled": True,
                "error": str(error),
                "decided_at": datetime.now(
                    timezone.utc
                ).isoformat(),
            }


decision_agent = DecisionAgent()