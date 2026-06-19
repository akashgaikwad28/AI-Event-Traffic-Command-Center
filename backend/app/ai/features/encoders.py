from pathlib import Path

import joblib
import pandas as pd

from backend.app.ai.features.constants import UNKNOWN_CATEGORY


class CategoricalEncoder:
    """
    Stateful categorical encoder that safely handles UNKNOWN categories during inference.
    Maps categories to integers based on frequency or simple encoding.
    """

    def __init__(self, unknown_value: int = -1):
        self.mapping = {}
        self.unknown_value = unknown_value

    def fit(self, series: pd.Series):
        """Fit the encoder on a pandas Series, creating a mapping of category -> integer."""
        unique_vals = series.dropna().unique()
        # Create mapping (1-indexed so 0 or -1 can be UNKNOWN/Missing)
        self.mapping = {val: idx + 1 for idx, val in enumerate(unique_vals)}
        # Add explicit unknown mapping just in case
        self.mapping[UNKNOWN_CATEGORY] = self.unknown_value
        return self

    def transform(self, series: pd.Series) -> pd.Series:
        """Transform a series using the fitted mapping. Unseen values map to unknown_value."""
        if not self.mapping:
            raise ValueError("Encoder must be fitted before transform")

        # Fill missing with UNKNOWN_CATEGORY before mapping
        filled_series = series.fillna(UNKNOWN_CATEGORY)

        # Map values, defaulting to unknown_value if not found
        return filled_series.map(lambda x: self.mapping.get(x, self.unknown_value))

    def fit_transform(self, series: pd.Series) -> pd.Series:
        self.fit(series)
        return self.transform(series)

    def save(self, filepath: Path):
        """Persist encoder to disk."""
        joblib.dump(self.mapping, filepath)

    def load(self, filepath: Path):
        """Load encoder from disk."""
        self.mapping = joblib.load(filepath)
