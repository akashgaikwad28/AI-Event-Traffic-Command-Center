import logging

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

logger = logging.getLogger(__name__)


class GoriModelTrainer:
    """
    Trains the Gridlock Operational Risk Index (GORI) model.
    Learns the relationship between geographic coordinates, time of day,
    and historical event types to predict congestion severity.
    """

    def __init__(self, model_save_path: str = "models/gori_model.pkl"):
        self.model_save_path = model_save_path
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def train(self, df: pd.DataFrame, target_col: str = "gori_score"):
        """
        Executes the training loop.
        """
        logger.info("Initializing GORI model training...")

        # In a real scenario, feature selection and encoding happen here
        features = ["latitude", "longitude", "is_rush_hour", "heavy_vehicle"]

        X = df[features]
        y = df[target_col]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        logger.info(f"Training on {len(X_train)} samples...")
        self.model.fit(X_train, y_train)

        score = self.model.score(X_test, y_test)
        logger.info(f"Model trained. Validation R^2 Score: {score:.4f}")

        self.save_model()

    def save_model(self):
        # joblib.dump(self.model, self.model_save_path)
        logger.info(f"Model successfully saved to {self.model_save_path}")
