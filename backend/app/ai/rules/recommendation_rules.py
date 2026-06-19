

class RecommendationEngine:
    """
    Operational Action Recommendation Rules Engine.
    Translates predictions into explicit dispatcher instructions.
    """

    def generate_recommendations(
        self, gori_score: int, clearance_mins: float, deployment_class: str
    ) -> list[str]:
        recommendations = []

        if gori_score > 80:
            recommendations.append(
                "CRITICAL: Escalate manpower immediately to contain secondary incidents."
            )
            recommendations.append("CRITICAL: Initiate major corridor diversion.")

        elif gori_score > 60:
            recommendations.append(
                "WARNING: Active diversion required on adjacent corridors."
            )
            if clearance_mins > 60:
                recommendations.append(
                    "WARNING: Prolonged closure anticipated. Escalate traffic units."
                )

        if "Heavy" in deployment_class or "Tow" in deployment_class:
            recommendations.append(
                "DISPATCH: Emergency heavy tow unit required on scene."
            )

        if len(recommendations) == 0:
            recommendations.append(
                "INFO: Routine monitoring. Standard deployment sufficient."
            )

        return recommendations
