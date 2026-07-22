import numpy as np
from xgboost import XGBClassifier


class RiskPredictor:
    """
    Machine Learning risk predictor using XGBoost.

    Predicts whether a supply-chain risk event is likely
    to require operational intervention.
    """

    def __init__(self):
        self.model = XGBClassifier(
            n_estimators=100,
            max_depth=3,
            learning_rate=0.1,
            random_state=42,
            eval_metric="logloss",
        )

        self._train_model()

    # ========================================================
    # TRAIN XGBOOST MODEL
    # ========================================================

    def _train_model(self):
        """
        Train the XGBoost model using representative
        energy supply-chain risk patterns.

        Features:
        1. risk_score
        2. severity_encoded
        3. confidence_score
        4. multi_source_verified
        """

        training_features = np.array([
            [15, 0, 60, 0],
            [20, 0, 65, 0],
            [25, 0, 70, 1],
            [30, 1, 65, 0],
            [35, 1, 70, 0],
            [40, 1, 75, 1],
            [45, 1, 80, 1],
            [50, 2, 70, 0],
            [55, 2, 75, 1],
            [60, 2, 80, 1],
            [65, 2, 82, 1],
            [68, 2, 85, 1],
            [70, 2, 85, 1],
            [72, 2, 88, 1],
            [75, 3, 85, 0],
            [78, 3, 88, 1],
            [80, 3, 90, 1],
            [82, 3, 91, 1],
            [85, 3, 92, 1],
            [87, 3, 93, 1],
            [90, 3, 95, 1],
            [92, 3, 96, 1],
            [95, 3, 97, 1],
            [98, 3, 99, 1],
        ], dtype=float)

        # 0 = Monitor
        # 1 = Operational intervention required
        training_labels = np.array([
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
        ])

        self.model.fit(
            training_features,
            training_labels,
        )

    # ========================================================
    # ENCODE RISK LEVEL
    # ========================================================

    def _encode_severity(
        self,
        severity: str,
    ) -> int:

        severity_mapping = {
            "low": 0,
            "medium": 1,
            "high": 2,
            "critical": 3,
        }

        return severity_mapping.get(
            str(severity).lower(),
            0,
        )

    # ========================================================
    # PREDICT RISK
    # ========================================================

    def predict(
        self,
        risk_score: float,
        severity: str,
        confidence_score: float = 80,
        multi_source_verified: bool = False,
    ):

        severity_encoded = self._encode_severity(
            severity
        )

        features = np.array([[
            float(risk_score),
            float(severity_encoded),
            float(confidence_score),
            int(bool(multi_source_verified)),
        ]])

        prediction = int(
            self.model.predict(features)[0]
        )

        probability = float(
            self.model.predict_proba(features)[0][1]
        )

        return {
            "prediction": prediction,
            "intervention_required": bool(prediction),
            "probability": round(
                probability,
                4,
            ),
            "model": "XGBoost",
            "features": {
                "risk_score": risk_score,
                "severity": severity,
                "confidence_score": confidence_score,
                "multi_source_verified": (
                    multi_source_verified
                ),
            },
        }


risk_predictor = RiskPredictor()