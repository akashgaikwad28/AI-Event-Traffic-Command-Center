# Data Pipeline Architecture

The Gridwise AI data engineering pipeline is orchestrated sequentially to transform raw incident data into an AI-ready spatial dataset. The pipeline strictly enforces a coordinate-first architecture to bypass the sparsity and unreliability of categorical geography.

## Pipeline Orchestration

The pipeline is defined in `data_pipeline/dataset_builder/builder.py` and consists of five core stages:

### 1. Ingestion (`DataLoader`)
Loads the raw historical incident data. The system reads from raw sources such as `Astram event data_anonymized - Astram event data_anonymizedb40ac87.csv`. 

### 2. Preprocessing (`DataCleaner`)
Cleans and normalizes the raw DataFrame. Ensures that core spatial coordinates (`latitude`, `longitude`) are properly cast and validated before downstream processing.

### 3. Spatial Clustering (`SpatialReconstructor`)
The most critical phase of the pipeline. Instead of relying on predefined map zones or junctions, the pipeline dynamically discovers recurring event zones and hotspots automatically from raw coordinates. 
- Utilizes **DBSCAN (Density-Based Spatial Clustering of Applications with Noise)**.
- Reconstructs operational traffic zones based on historical coordinate densities.

### 4. Feature Engineering (`FeatureGenerator`)
Generates temporal and operational features. Crucially, it leverages the `dynamic_zone_id` (generated in the previous step) to calculate historical cluster pressure and operational memory.

### 5. Export
The fully structured dataset is exported to `data/processed/cleaned_dataset.parquet` in a highly optimized Parquet format, making it immediately available for the ML modeling pipeline.
