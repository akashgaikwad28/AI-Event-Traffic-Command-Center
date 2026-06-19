import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


class DataLoader:
    """
    Ingests raw incident data from CSV or Database sources.
    """

    def __init__(self, data_path: str):
        self.data_path = Path(data_path)

    def load_raw_data(self) -> pd.DataFrame:
        """
        Loads the raw anonymized hackathon dataset.
        """
        logger.info(f"Loading raw data from {self.data_path}")
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")

        df = pd.read_csv(self.data_path)
        logger.info(f"Loaded dataframe with shape: {df.shape}")
        return df
