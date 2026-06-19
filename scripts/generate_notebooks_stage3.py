
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


def create_stage3_notebook():
    nb = new_notebook()
    cells = [
        new_markdown_cell(
            "# Final Model Selection & Artifact Export\n\n## 1. Goal\nTrain final models on all data and export inference artifacts to `backend/app/ai/artifacts/`."
        ),
        new_code_cell(
            """import os
import sys
import json
import joblib
from pathlib import Path
import pandas as pd
from datetime import datetime

project_root = Path(os.getcwd()).parent.parent
sys.path.append(str(project_root))

from notebooks.config import *
"""
        ),
        new_markdown_cell("## 2. Load Final Data & Features"),
        new_code_cell(
            """df = pd.read_parquet(CLEANED_DATA_PATH)
features = ['latitude', 'longitude', 'hour_of_day', 'day_of_week', 'is_weekend', 'is_peak_hour', 'priority_encoded', 'is_closed']
X = df[features]
"""
        ),
        new_markdown_cell("## 3. Train Final Models"),
        new_code_cell(
            """from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
import xgboost as xgb

# Example: Congestion Proxy (Regressor)
congestion_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
congestion_model.fit(X, df[CONGESTION_TARGET])

# Example: Response Time (Regressor)
response_model = xgb.XGBRegressor(n_estimators=100, random_state=42)
response_model.fit(X, df[RESPONSE_TIME_TARGET])

# Example: Deployment (Classifier)
deployment_model = RandomForestClassifier(n_estimators=100, random_state=42)
deployment_model.fit(X, df[DEPLOYMENT_TARGET])

print("Final models trained.")
"""
        ),
        new_markdown_cell("## 4. Export Artifacts"),
        new_code_cell(
            """os.makedirs(ARTIFACTS_DIR, exist_ok=True)

# Save Models
joblib.dump(congestion_model, ARTIFACTS_DIR / "congestion_model.pkl")
joblib.dump(response_model, ARTIFACTS_DIR / "response_time_model.pkl")
joblib.dump(deployment_model, ARTIFACTS_DIR / "deployment_model.pkl")

# Save Registry
registry = {
    "version": "1.0",
    "trained_at": datetime.utcnow().isoformat(),
    "features": features,
    "metrics": {
        "congestion_rmse": 0.0, # Placeholder for real metrics
        "response_rmse": 0.0,
        "deployment_accuracy": 0.0
    }
}

with open(ARTIFACTS_DIR / "model_registry.json", "w") as f:
    json.dump(registry, f, indent=4)

print("Exported models and registry to backend artifacts.")
"""
        ),
    ]
    nb["cells"] = cells
    with open("notebooks/training/11_final_model_selection.ipynb", "w") as f:
        nbformat.write(nb, f)


if __name__ == "__main__":
    create_stage3_notebook()
    print("Stage 3 notebook generated.")
