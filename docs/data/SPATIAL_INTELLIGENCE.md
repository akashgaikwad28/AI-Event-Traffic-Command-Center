# Spatial Intelligence

Gridwise AI pivots away from traditional "Category-Based Routing" toward a **Coordinate-First Spatial Intelligence** approach. 

## The Failure of Categorical Geography
Historically, systems relied heavily on categorical text data (like 'zone', 'junction name', or hardcoded map zones). Our analysis showed that these labels are fundamentally broken:
- Highly sparse and frequently missing.
- Subject to human error and misspellings.
- Inflexible to dynamically shifting city infrastructure and traffic patterns.

## DBSCAN Spatial Reconstruction
To resolve this, the system reconstructs operational geography dynamically using unsupervised spatial intelligence. We use **DBSCAN (Density-Based Spatial Clustering of Applications with Noise)** to create a reliable, coordinate-first operational map.

### Implementation Details (`SpatialReconstructor`)
Located in `data_pipeline/spatial_clustering/dbscan_reconstructor.py`.

- **Algorithm:** Uses DBSCAN with the `ball_tree` algorithm and `haversine` metric.
- **Inputs:** Raw `latitude` and `longitude` arrays, converted to radians.
- **Parameters:** 
  - `eps_km` (default 0.5km): The maximum distance between two samples for one to be considered as in the neighborhood of the other. Converted to radians dynamically using Earth's radius (`6371.0088 km`).
  - `min_samples` (default 5): The number of samples in a neighborhood for a point to be considered as a core point.
- **Output:** Assigns a `dynamic_zone_id` to each data point. Points in sparse areas are marked as noise (`cluster -1`).

### Operational Memory
By mapping raw coordinates to these historical DBSCAN clusters, we can:
1. Engineer "spatial memory" to track `historical_cluster_pressure`.
2. Flag recurring operational traffic hotspots dynamically.
3. Rapidly map live incidents to these dynamically generated zones to assess severity.
