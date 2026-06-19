import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
import logging

logger = logging.getLogger(__name__)

class SpatialReconstructor:
    """
    Coordinate-First Spatial Intelligence.
    Instead of relying on categorical text data (like 'zone' or 'junction name') 
    which is often sparse or misspelled, this module reconstructs operational 
    traffic zones dynamically using Density-Based Spatial Clustering (DBSCAN).
    """
    
    def __init__(self, eps_km: float = 0.5, min_samples: int = 5):
        self.eps_km = eps_km
        self.min_samples = min_samples
        # Earth radius in km for Haversine distance
        self.kms_per_radian = 6371.0088

    def fit_predict_hotspots(self, df: pd.DataFrame, lat_col="latitude", lng_col="longitude") -> pd.DataFrame:
        """
        Discovers recurring event zones and hotspots automatically from coordinates.
        """
        logger.info(f"Running DBSCAN clustering with eps={self.eps_km}km")
        
        coords = np.radians(df[[lat_col, lng_col]].to_numpy())
        epsilon = self.eps_km / self.kms_per_radian
        
        db = DBSCAN(eps=epsilon, min_samples=self.min_samples, algorithm='ball_tree', metric='haversine')
        df['dynamic_zone_id'] = db.fit_predict(coords)
        
        n_clusters = len(set(df['dynamic_zone_id'])) - (1 if -1 in df['dynamic_zone_id'].values else 0)
        logger.info(f"Discovered {n_clusters} dynamic spatial hotspots.")
        
        return df
