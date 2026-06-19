
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


def create_experiment_notebook(filename, title, goal, load_data_code, modeling_code):
    nb = new_notebook()
    cells = [
        new_markdown_cell(f"# {title}\n\n## 1. Goal\n{goal}\n\n## 2. Imports"),
        new_code_cell(
            """import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add project root
project_root = Path(os.getcwd()).parent.parent
sys.path.append(str(project_root))

from notebooks.config import *
"""
        ),
        new_markdown_cell("## 3. Load Engineered Data"),
        new_code_cell(load_data_code),
        new_markdown_cell("## 4. Modeling & Validation"),
        new_code_cell(modeling_code),
    ]
    nb["cells"] = cells
    with open(f"notebooks/experiments/{filename}", "w") as f:
        nbformat.write(nb, f)


def generate_all_stage2():
    load_code = """df = pd.read_parquet(CLEANED_DATA_PATH)
features = ['latitude', 'longitude', 'hour_of_day', 'day_of_week', 'is_weekend', 'is_peak_hour', 'priority_encoded', 'is_closed']
X = df[features]
"""
    # 05
    create_experiment_notebook(
        "05_baseline_models.ipynb",
        "Baseline Models",
        "Establish baseline performance using TimeSeriesSplit, LinearRegression, and RandomForest.",
        load_code + "y = df[RESPONSE_TIME_TARGET]",
        """from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

tscv = TimeSeriesSplit(n_splits=3)
# Quick evaluation loop logic here
print("Setup TimeSeriesSplit for temporal validation.")
""",
    )

    # 06
    create_experiment_notebook(
        "06_congestion_model_experiments.ipynb",
        "Congestion Proxy Model",
        "Train LightGBM/XGBoost on the congestion proxy score using RandomizedSearchCV.",
        load_code + "y = df[CONGESTION_TARGET]",
        """from sklearn.model_selection import RandomizedSearchCV
# Example LightGBM/XGBoost setup
print("Ready to implement LightGBM RandomizedSearchCV for Congestion Proxy.")
""",
    )

    # 07
    create_experiment_notebook(
        "07_response_time_model_experiments.ipynb",
        "Response Time Model",
        "Train LightGBM/XGBoost to predict resolution_time_minutes.",
        load_code + "y = df[RESPONSE_TIME_TARGET]",
        """# Example LightGBM/XGBoost setup for response time
print("Ready to implement LightGBM/XGBoost for Response Time.")
""",
    )

    # 08
    create_experiment_notebook(
        "08_deployment_model_experiments.ipynb",
        "Deployment Classification Model",
        "Train classification models (LOW, MEDIUM, HIGH) for deployment load.",
        load_code + "y = df[DEPLOYMENT_TARGET]",
        """from sklearn.ensemble import RandomForestClassifier
print("Ready to implement Classifier for Deployment Target.")
""",
    )

    # 09
    create_experiment_notebook(
        "09_model_comparison.ipynb",
        "Model Comparison",
        "Compare inference speed, training time, and operational metrics.",
        "print('Load saved metrics from experiments here')",
        """import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style(PLOT_STYLE)
print("Ready to plot comparison metrics.")
""",
    )

    # 10
    create_experiment_notebook(
        "10_feature_importance_analysis.ipynb",
        "Feature Importance & SHAP",
        "Analyze operational feature importance using SHAP values.",
        "print('Load best models and X_train here')",
        """# import shap
print("Ready to run SHAP explanations.")
""",
    )


if __name__ == "__main__":
    generate_all_stage2()
    print("Stage 2 notebooks generated.")
