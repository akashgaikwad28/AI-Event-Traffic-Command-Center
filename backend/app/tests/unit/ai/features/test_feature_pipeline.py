from datetime import datetime, timedelta

import pandas as pd
import pytest

from backend.app.ai.pipelines.inference_pipeline import InferencePipeline
from backend.app.ai.pipelines.training_pipeline import TrainingPipeline


@pytest.fixture
def mock_event_data():
    now = datetime.now()
    return pd.DataFrame(
        [
            {
                "id": "1",
                "start_time": now - timedelta(hours=2),
                "end_time": now - timedelta(hours=1),
                "latitude": 40.7128,
                "longitude": -74.0060,
                "zone_name": "Downtown",
                "event_type": "accident",
                "event_category": "incident",
                "severity": "high",
                "road_closure": True,
                "congestion_score": 0.8,
            },
            {
                "id": "2",
                "start_time": now - timedelta(hours=1),
                "end_time": now,
                "latitude": 40.7580,
                "longitude": -73.9855,
                "zone_name": "Midtown",
                "event_type": "hazard",
                "event_category": "incident",
                "severity": "low",
                "road_closure": False,
                "congestion_score": 0.3,
            },
        ]
    )


def test_training_pipeline_generates_features(mock_event_data):
    pipeline = TrainingPipeline()
    # We won't save dataset to disk to avoid test side effects, we just call the feature pipeline
    # But wait, we want to test fit_transform
    # We will let it save artifacts since we configured them in a temp folder conceptually,
    # but for this test we'll just let it run.

    ml_ready_df = pipeline.run(mock_event_data, save_dataset=False)

    # Assert
    assert not ml_ready_df.empty
    assert "hour_of_day" in ml_ready_df.columns
    assert "zone_encoded" in ml_ready_df.columns
    assert "type_encoded" in ml_ready_df.columns
    assert "category_encoded" in ml_ready_df.columns
    assert "severity_scaled" in ml_ready_df.columns
    assert "incidents_last_hour" in ml_ready_df.columns


def test_inference_pipeline_consistency(mock_event_data):
    # Train first to generate artifacts
    train_pipeline = TrainingPipeline()
    df_train = train_pipeline.run(mock_event_data, save_dataset=False)

    # Inference
    inference_pipeline = InferencePipeline()

    # Run on the second row
    test_row = mock_event_data.iloc[[1]].copy()
    df_infer = inference_pipeline.run_batch(test_row)

    # Verify column order is identical
    assert list(df_train.columns) == list(df_infer.columns)

    # Verify exact encoded values match
    train_val = df_train.iloc[1]["zone_encoded"]
    infer_val = df_infer.iloc[0]["zone_encoded"]
    assert train_val == infer_val

    # Verify unknown category handling
    test_row["zone_name"] = "UNSEEN_ZONE"
    df_infer_unseen = inference_pipeline.run_batch(test_row)
    assert df_infer_unseen.iloc[0]["zone_encoded"] == -1  # The UNKNOWN_VALUE
