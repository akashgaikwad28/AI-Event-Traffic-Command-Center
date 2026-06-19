from typing import Any

from backend.app.ai.contracts.feature_contract import FeatureContract
from backend.app.ai.engines.gori_engine import GoriEngine
from backend.app.ai.inference.confidence_engine import ConfidenceEngine
from backend.app.ai.inference.model_loader import ModelLoader
from backend.app.ai.inference.preprocessing import PreprocessingEngine
from backend.app.ai.rules.recommendation_rules import RecommendationEngine


class PredictionEngine:
    """
    Core Operational Intelligence Runtime.
    Orchestrates the entire multi-model execution and business logic fallback layers.
    """

    def __init__(self, loader: ModelLoader):
        self.loader = loader
        self.feature_contract = FeatureContract(self.loader.get_feature_contract())

        # In a real implementation we might have dedicated wrappers, but here we load directly
        self.congestion_model = self.loader.get_model("congestion_model")
        self.response_model = self.loader.get_model("response_time_model")
        self.deployment_model = self.loader.get_model("deployment_model")

        self.gori_engine = GoriEngine()
        self.confidence_engine = ConfidenceEngine()
        self.recommendation_engine = RecommendationEngine()

    def generate_full_assessment(self, raw_payload: dict[str, Any]) -> dict[str, Any]:
        """
        Executes the full deterministic operational assessment.
        """
        # 1. Preprocessing & Contract Enforcement
        raw_features = PreprocessingEngine.process_raw_payload(raw_payload)
        df_features = self.feature_contract.validate_and_format(raw_features)

        # 2. Multi-Model Inference (with Fallbacks simulated via robust try-except loops)
        try:
            congestion_score = float(self.congestion_model.predict(df_features)[0])
        except Exception:
            congestion_score = 50.0  # Fallback

        try:
            clearance_mins = float(self.response_model.predict(df_features)[0])
            clearance_mins = max(15.0, clearance_mins)
        except Exception:
            clearance_mins = 45.0  # Fallback

        try:
            deployment_class = self.deployment_model.predict(df_features)[0]
        except Exception:
            deployment_class = "Standard"  # Fallback

        # 3. Operational Risk Intelligence (GORI)
        gori_assessment = self.gori_engine.calculate_gori(
            congestion_score=congestion_score,
            clearance_mins=clearance_mins,
            deployment_class=deployment_class,
            is_rush_hour=raw_features.get("is_peak_hour", False),
            is_closed=raw_features.get("is_closed", False),
        )

        # 4. Action Recommendation AI
        recommendations = self.recommendation_engine.generate_recommendations(
            gori_assessment["gori_score"], clearance_mins, deployment_class
        )

        # 5. Prediction Reliability / Confidence
        confidence_score, reliability_tier = self.confidence_engine.calculate_trust(
            df_features, gori_assessment["gori_score"]
        )

        return {
            "gori": gori_assessment,
            "predictions": {
                "clearance_minutes": round(clearance_mins, 1),
                "congestion_proxy_score": round(congestion_score, 1),
                "deployment_load": deployment_class,
            },
            "trust": {"reliability_score": confidence_score, "tier": reliability_tier},
            "recommendations": recommendations,
            "explainability": {
                "top_factors": [
                    "Operational Priority",
                    "Rush Hour Traffic",
                ]  # Placeholder for SHAP cache
            },
        }
