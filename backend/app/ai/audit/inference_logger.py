import json
import logging
from datetime import datetime
from typing import Any


class InferenceLogger:
    """
    Enterprise inference audit logger.
    Tracks all operational requests for compliance, model drift analysis, and accountability.
    """

    def __init__(self):
        # In production, this would route to Datadog / ELK
        self.logger = logging.getLogger("inference_audit")
        self.logger.setLevel(logging.INFO)

        # Ensure it doesn't duplicate if already added
        if not self.logger.handlers:
            handler = logging.FileHandler("inference_audit.log")
            handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))
            self.logger.addHandler(handler)

    def log_inference(
        self,
        request_id: str,
        payload: dict[str, Any],
        assessment: dict[str, Any],
        latency_ms: float,
    ):
        """
        Logs the complete inference transaction.
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "request_id": request_id,
            "latency_ms": latency_ms,
            "inputs": {
                "latitude": payload.get("latitude"),
                "longitude": payload.get("longitude"),
                "priority": payload.get("priority"),
            },
            "outputs": {
                "gori_score": assessment["gori"]["gori_score"],
                "severity_tier": assessment["gori"]["severity_tier"],
                "clearance_minutes": assessment["predictions"]["clearance_minutes"],
                "confidence": assessment["trust"]["reliability_score"],
            },
            "triggered_rules": assessment["recommendations"],
        }

        self.logger.info(json.dumps(log_entry))
