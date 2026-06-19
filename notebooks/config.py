"""
Shared configuration for GridWise AI notebooks.
"""

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = (
    DATA_DIR / "Astram event data_anonymized - Astram event data_anonymizedb40ac87.csv"
)
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CLEANED_DATA_PATH = PROCESSED_DATA_DIR / "cleaned_dataset.parquet"
REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
ARTIFACTS_DIR = BASE_DIR / "backend" / "app" / "ai" / "artifacts"

# Constants
GLOBAL_RANDOM_SEED = 42

# Target Columns
CONGESTION_TARGET = "congestion_proxy_score"
RESPONSE_TIME_TARGET = "resolution_time_minutes"
DEPLOYMENT_TARGET = "deployment_load_class"

# Plotting Settings
PLOT_STYLE = "whitegrid"
