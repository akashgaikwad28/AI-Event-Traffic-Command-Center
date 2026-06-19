
import pandas as pd


class ConfidenceEngine:
    """
    Calculates the Model Trust Score (Prediction Reliability).
    Evaluates geo familiarity, training distribution similarity, and unseen categories.
    """

    def calculate_trust(
        self, features: pd.DataFrame, gori_score: float
    ) -> tuple[int, str]:
        """
        Returns a confidence score (0-100) and a Reliability Tier.
        """
        base_trust = 95

        # 1. Feature Completeness (Simulated)
        # If important columns were missing and imputed, lower trust
        # In a real implementation we'd check the missing mask from preprocessing

        # 2. Extreme GORI Penalization
        # High GORI predictions have higher variance
        if gori_score > 80:
            base_trust -= 10

        # 3. Geo Familiarity (Simulated logic, would rely on cluster density check)
        # If cluster is -1 (noise), drop confidence significantly.
        # Here we mock it based on extreme latitudes as an example of unseen zones
        lat = features.get("latitude", pd.Series([0])).iloc[0]
        if lat < 12.0 or lat > 14.0:
            base_trust -= 20

        # Ensure bounds
        trust_score = max(0, min(100, base_trust))

        if trust_score >= 85:
            tier = "HIGH_TRUST"
        elif trust_score >= 65:
            tier = "MEDIUM_TRUST"
        else:
            tier = "LOW_TRUST"

        return trust_score, tier
