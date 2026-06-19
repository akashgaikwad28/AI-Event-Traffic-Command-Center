# Data Pipeline Architecture

The data pipeline is responsible for ingesting, cleaning, and transforming raw incident data into an AI-ready dataset. It is organized into several modules within the `data_pipeline/` directory.

## 1. Data Ingestion (`data_pipeline/ingestion/data_loader.py`)
- The `DataLoader` class loads raw anonymized hackathon datasets (from CSV or database sources) into pandas DataFrames.
- Validates the existence of the data source and provides basic logging of data shape upon load.

## 2. Preprocessing (`data_pipeline/preprocessing/cleaner.py`)
- The `DataCleaner` parses essential date columns (`start_datetime`, `resolved_datetime`, `closed_datetime`, `modified_datetime`) into UTC datetimes.
- Handles missing values by dropping records without a `start_datetime`.
- Resolves inconsistencies by dropping records where `resolved_datetime` occurs before `start_datetime`.
- Drops invalid geographic coordinates (outside the expected latitude/longitude ranges).
- Fills critical missing categoricals (`event_cause`, `veh_type`, `priority`) with "unknown".

## 3. Spatial Clustering (`data_pipeline/spatial_clustering/dbscan_reconstructor.py`)
- Utilizes the `SpatialReconstructor` to implement Coordinate-First Spatial Intelligence.
- Replaces sparse or misspelled categorical location text (e.g., 'zone' or 'junction name') with dynamic spatial hotspots.
- Employs Density-Based Spatial Clustering (DBSCAN) using the Haversine distance metric to dynamically reconstruct recurring event zones and operational traffic hotspots.

## 4. Feature Engineering (`data_pipeline/feature_engineering/feature_generator.py`)
- Generates new predictive features from the cleaned data.
- Provides engineered features such as `hour_of_day`, `day_of_week`, `is_weekend`, `is_peak_hour`, `priority_encoded`, and generates target proxies needed for downstream modeling.

## 5. Dataset Orchestration (`data_pipeline/dataset_builder/builder.py`)
- The `DatasetBuilder` class orchestrates the entire data engineering pipeline sequentially.
- Passes the DataFrame through ingestion -> cleaning -> spatial clustering -> feature generation.
- Exports the final processed dataset to Parquet format (e.g., `data/processed/cleaned_dataset.parquet`) for use in the ML pipeline.
