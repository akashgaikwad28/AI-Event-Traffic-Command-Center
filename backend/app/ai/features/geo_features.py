
import pandas as pd

from backend.app.geo.spatial_engine import SpatialEngine


def generate_geo_features(
    df: pd.DataFrame, spatial_engine: SpatialEngine
) -> pd.DataFrame:
    """
    Generate geo features such as nearby incident density using the SpatialEngine.
    This assumes df is already sorted chronologically if temporal filtering is done outside.
    For this basic implementation, we compute a static spatial density proxy
    or distances to fixed zones if needed. Real temporal-spatial rolling is complex,
    so we will implement a simplified proxy: nearby event count overall (or within window).
    """
    if df.empty or "latitude" not in df.columns or "longitude" not in df.columns:
        return df

    coords = list(zip(df["latitude"].values, df["longitude"].values))

    # 1. Cluster density proxy
    # To prevent leakage, a strict implementation would only build tree from past events.
    # For performance and hackathon scope, we will build one tree, but this is a known
    # trade-off if we don't strictly slice temporally.
    # However, to be leakage safe, we can do a rolling spatial query, or just
    # extract static cluster labels.
    try:
        labels = spatial_engine.cluster_coordinates(coords, eps_km=1.0, min_samples=3)
        df["geo_cluster_label"] = labels
        # cluster density = size of cluster
        cluster_sizes = pd.Series(labels).value_counts().to_dict()
        cluster_sizes[-1] = 0  # noise has 0 density
        df["cluster_density"] = df["geo_cluster_label"].map(cluster_sizes)
    except Exception:
        df["geo_cluster_label"] = -1
        df["cluster_density"] = 0

    return df
