from datetime import datetime, timezone

from ml.risk_predictor import risk_predictor


class RiskIntelligenceAgent:
    """
    Autonomous agent responsible for analysing detected risk events
    and deciding whether further action is required.
    """

    def __init__(self):
        self.name = "AI Risk Intelligence Agent"

    def analyze_risk(self, risk_event):
        """
        Analyse a risk event and return an agent assessment.
        Supports both SQLAlchemy objects and dictionaries.
        """

        # ====================================================
        # EXTRACT RISK EVENT DATA
        # ====================================================

        if isinstance(risk_event, dict):
            risk_score = risk_event.get(
                "risk_score",
                0,
            ) or 0

            severity = (
                risk_event.get("risk_level")
                or risk_event.get("severity")
                or "Unknown"
            )

            event_id = risk_event.get("id")

            confidence_score = (
                risk_event.get(
                    "confidence_score",
                    80,
                )
                or 80
            )

            multi_source_verified = risk_event.get(
                "multi_source_verified",
                False,
            )

        else:
            risk_score = getattr(
                risk_event,
                "risk_score",
                0,
            ) or 0

            severity = (
                getattr(
                    risk_event,
                    "risk_level",
                    None,
                )
                or getattr(
                    risk_event,
                    "severity",
                    None,
                )
                or "Unknown"
            )

            event_id = getattr(
                risk_event,
                "id",
                None,
            )

            confidence_score = (
                getattr(
                    risk_event,
                    "confidence_score",
                    80,
                )
                or 80
            )

            multi_source_verified = getattr(
                risk_event,
                "multi_source_verified",
                False,
            )

        # ====================================================
        # XGBOOST ML RISK PREDICTION
        # ====================================================

        ml_prediction = risk_predictor.predict(
            risk_score=risk_score,
            severity=severity,
            confidence_score=confidence_score,
            multi_source_verified=multi_source_verified,
        )

        # ====================================================
        # AUTONOMOUS AGENT DECISION
        # ====================================================

        requires_action = (
            ml_prediction["intervention_required"]
            or risk_score >= 70
            or str(severity).lower()
            in ["critical", "high"]
        )

        if requires_action:
            action = "Generate Mitigation Recommendation"
            agent_status = "Action Required"

        else:
            action = "Continue Monitoring"
            agent_status = "Monitoring"

        # ====================================================
        # AGENT RESPONSE
        # ====================================================

        return {
            "agent": self.name,
            "risk_event_id": event_id,
            "risk_score": risk_score,
            "severity": severity,
            "confidence_score": confidence_score,
            "multi_source_verified": multi_source_verified,
            "status": agent_status,
            "recommended_action": action,
            "autonomous_decision": requires_action,
            "ml_prediction": ml_prediction,
            "ml_model": "XGBoost",
            "ml_intervention_probability": ml_prediction[
                "probability"
            ],
            "analyzed_at": datetime.now(
                timezone.utc
            ).isoformat(),
        }


risk_agent = RiskIntelligenceAgent()