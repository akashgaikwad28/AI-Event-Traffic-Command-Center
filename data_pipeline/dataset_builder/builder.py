import logging
from pathlib import Path

from data_pipeline.ingestion.data_loader import DataLoader
from data_pipeline.preprocessing.cleaner import DataCleaner
from data_pipeline.feature_engineering.feature_generator import FeatureGenerator
from data_pipeline.spatial_clustering.dbscan_reconstructor import SpatialReconstructor

logger = logging.getLogger(__name__)

class DatasetBuilder:
    """
    Orchestrates the entire Data Engineering pipeline sequentially.
    """
    def __init__(self, raw_path: str, output_path: str):
        self.raw_path = raw_path
        self.output_path = Path(output_path)
        
        self.loader = DataLoader(self.raw_path)
        self.cleaner = DataCleaner()
        self.feature_gen = FeatureGenerator()
        self.spatial = SpatialReconstructor()
        
    def build(self):
        logger.info("Starting Dataset Build Pipeline...")
        
        # 1. Ingestion
        df = self.loader.load_raw_data()
        
        # 2. Preprocessing
        df = self.cleaner.clean(df)
        
        # 3. Spatial Clustering
        df = self.spatial.fit_predict_hotspots(df)
        
        # 4. Feature Engineering
        df = self.feature_gen.generate_features(df)
        
        # 5. Export
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(self.output_path, index=False)
        logger.info(f"Successfully built and exported final dataset to {self.output_path}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    builder = DatasetBuilder(
        raw_path="data/Astram event data_anonymized - Astram event data_anonymizedb40ac87.csv", 
        output_path="data/processed/cleaned_dataset.parquet"
    )
    builder.build()
