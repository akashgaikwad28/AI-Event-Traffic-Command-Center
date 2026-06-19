import logging

import pandas as pd
from scipy.stats import ks_2samp

logger = logging.getLogger(__name__)


class DriftMonitor:
    """
    Monitors incoming production data against the training snapshot
    to detect covariate shift and concept drift.
    """

    def __init__(self, p_value_threshold: float = 0.05):
        self.p_value_threshold = p_value_threshold

    def detect_drift(self, reference_data: pd.Series, current_data: pd.Series) -> bool:
        """
        Uses the Kolmogorov-Smirnov test to detect distribution drift.
        Returns True if drift is detected.
        """
        stat, p_value = ks_2samp(reference_data, current_data)
        has_drift = p_value < self.p_value_threshold

        if has_drift:
            logger.warning(f"Data Drift Detected! p_value={p_value:.4f}")
        else:
            logger.info("No significant drift detected in feature distribution.")

        return has_drift
