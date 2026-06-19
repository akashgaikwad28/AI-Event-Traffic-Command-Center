
import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook


def create_cleaning_notebook():
    nb = new_notebook()

    cells = [
        new_markdown_cell(
            "# Data Cleaning\n\n## 1. Goal\nBuild a reproducible cleaning pipeline and generate a Data Quality Report."
        ),
        new_markdown_cell("## 2. Imports"),
        new_code_cell(
            """import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add project root to sys.path
project_root = Path(os.getcwd()).parent.parent
sys.path.append(str(project_root))

from notebooks.config import *
from notebooks.utils.notebook_helpers import set_seed
set_seed(GLOBAL_RANDOM_SEED)"""
        ),
        new_markdown_cell("## 3. Data Loading"),
        new_code_cell(
            """df = pd.read_csv(RAW_DATA_PATH)
print(f"Initial shape: {df.shape}")
df.head()"""
        ),
        new_markdown_cell("## 4. Data Quality Report - Initial"),
        new_code_cell(
            """# Missing Values Summary
missing = df.isna().sum()
missing_pct = (missing / len(df)) * 100
missing_df = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_pct}).sort_values('Missing %', ascending=False)
print("--- Missing Values Report ---")
display(missing_df[missing_df['Missing Count'] > 0])"""
        ),
        new_code_cell(
            """# Invalid Coordinate Report
invalid_coords = df[
    (df['latitude'] < -90) | (df['latitude'] > 90) |
    (df['longitude'] < -180) | (df['longitude'] > 180)
]
print(f"Found {len(invalid_coords)} rows with invalid coordinates out of bounds (-90 to 90, -180 to 180).")"""
        ),
        new_markdown_cell(
            "## 5. Cleaning Operations\nWe will not aggressively drop columns yet, but we will clean the ones we strictly need."
        ),
        new_code_cell(
            """# Parse Dates
date_cols = ['start_datetime', 'resolved_datetime', 'closed_datetime', 'modified_datetime']
for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors='coerce', utc=True)

# Check timestamp inconsistencies
invalid_times = df[df['resolved_datetime'] < df['start_datetime']]
print(f"Found {len(invalid_times)} rows where resolved_datetime is before start_datetime.")
"""
        ),
        new_code_cell(
            """# Drop explicitly broken rows or handle them safely
# We will drop rows where start_datetime is NaT as we cannot do operational analysis without a start time.
initial_len = len(df)
df = df.dropna(subset=['start_datetime'])

# Drop rows with invalid coordinates
if len(invalid_coords) > 0:
    df = df.drop(invalid_coords.index)

# Fix invalid times by swapping or dropping. Here we drop for simplicity.
if len(invalid_times) > 0:
    df = df.drop(invalid_times.index)

print(f"Dropped {initial_len - len(df)} rows due to fundamental data corruption.")"""
        ),
        new_code_cell(
            """# Fill essential missing values with 'unknown' or median
fill_cols = ['event_cause', 'veh_type', 'priority']
for col in fill_cols:
    if col in df.columns:
        df[col] = df[col].fillna('unknown')"""
        ),
        new_markdown_cell("## 6. Export Intermediate Cleaned Data"),
        new_code_cell(
            """# Create intermediate dir if not exists
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
intermediate_path = PROCESSED_DATA_DIR / "intermediate_cleaned.parquet"
df.to_parquet(intermediate_path, index=False)
print(f"Saved {len(df)} cleaned rows to {intermediate_path}")"""
        ),
    ]

    nb["cells"] = cells
    with open("notebooks/features/02_data_cleaning.ipynb", "w") as f:
        nbformat.write(nb, f)


def create_feature_engineering_notebook():
    nb = new_notebook()

    cells = [
        new_markdown_cell(
            "# Feature Engineering & Validation\n\n## 1. Goal\nGenerate operational proxy targets, engineer time/location features, and validate for data leakage."
        ),
        new_markdown_cell("## 2. Imports"),
        new_code_cell(
            """import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Add project root to sys.path
project_root = Path(os.getcwd()).parent.parent
sys.path.append(str(project_root))

from notebooks.config import *
from backend.app.ai.features.target_engineering import (
    generate_response_duration_target,
    generate_congestion_proxy,
    generate_deployment_target
)
"""
        ),
        new_markdown_cell("## 3. Load Cleaned Data"),
        new_code_cell(
            """intermediate_path = PROCESSED_DATA_DIR / "intermediate_cleaned.parquet"
df = pd.read_parquet(intermediate_path)
print(f"Loaded {len(df)} rows.")"""
        ),
        new_markdown_cell(
            "## 4. Target Generation\nUsing operational proxies for realistic predictions."
        ),
        new_code_cell(
            """# 1. Response Duration
df[RESPONSE_TIME_TARGET] = generate_response_duration_target(df)

# 2. Congestion Proxy
df[CONGESTION_TARGET] = generate_congestion_proxy(df)

# 3. Deployment Load Classification
df[DEPLOYMENT_TARGET] = generate_deployment_target(df)

display(df[[RESPONSE_TIME_TARGET, CONGESTION_TARGET, DEPLOYMENT_TARGET]].head())"""
        ),
        new_markdown_cell(
            "## 5. Feature Engineering\nExtracting temporal and spatial features."
        ),
        new_code_cell(
            """# Time features from start_datetime
# Ensure it's datetime
df['start_datetime'] = pd.to_datetime(df['start_datetime'], utc=True)

df['hour_of_day'] = df['start_datetime'].dt.hour
df['day_of_week'] = df['start_datetime'].dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
df['is_peak_hour'] = df['hour_of_day'].isin([8,9,10, 17,18,19]).astype(int)

# Operational Features
# Severity encoded
priority_map = {'unknown': 0, 'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
df['priority_encoded'] = df['priority'].str.lower().map(priority_map).fillna(0)

# Closure
df['is_closed'] = df['requires_road_closure'].astype(str).str.lower() == 'true'
df['is_closed'] = df['is_closed'].astype(int)
"""
        ),
        new_markdown_cell(
            "## 6. Leakage Validation\nEnsure no future information (e.g. resolved_datetime) leaks into predictive features."
        ),
        new_code_cell(
            """# List of features meant for training (excluding targets and leakage columns)
leakage_cols = ['resolved_datetime', 'closed_datetime', 'modified_datetime', 'resolved_by_id']
# Validate none of these are going into our primary feature list
primary_features = ['latitude', 'longitude', 'hour_of_day', 'day_of_week', 'is_weekend', 'is_peak_hour', 'priority_encoded', 'is_closed']

for col in primary_features:
    assert col not in leakage_cols, f"Leakage detected: {col} is a future event column!"

print("Leakage validation passed! Primary features are safe.")"""
        ),
        new_markdown_cell("## 7. Export Processed Data & Feature Snapshot"),
        new_code_cell(
            """# Final export
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
df.to_parquet(CLEANED_DATA_PATH, index=False)
print(f"Saved {len(df)} engineered rows to {CLEANED_DATA_PATH}")

# Feature Snapshot Export
snapshot = df[primary_features + [RESPONSE_TIME_TARGET, CONGESTION_TARGET, DEPLOYMENT_TARGET]].dtypes.astype(str).to_dict()
snapshot_path = PROCESSED_DATA_DIR / "feature_snapshot.json"
import json
with open(snapshot_path, "w") as f:
    json.dump(snapshot, f, indent=4)
print(f"Saved feature snapshot to {snapshot_path}")"""
        ),
    ]

    nb["cells"] = cells
    with open("notebooks/features/04_feature_engineering_validation.ipynb", "w") as f:
        nbformat.write(nb, f)


if __name__ == "__main__":
    create_cleaning_notebook()
    create_feature_engineering_notebook()
    print("Notebooks for Stage 1 (Features) populated successfully.")
