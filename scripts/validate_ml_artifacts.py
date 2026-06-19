import sys
import json
import pandas as pd
from backend.app.ai.features.time_features import generate_time_features
from backend.app.ai.engines.gori_engine import GoriEngine
# In a real validation we would import the actual prediction engine:
# from backend.app.ai.models.prediction_engine import PredictionEngine
# But since we're verifying the pipeline logic, let's use the actual features.

def validate_artifacts():
    print("Starting ML Artifact Validation...")
    
    # Check if models exist
    import os
    artifact_dir = "backend/app/ai/artifacts"
    expected = ["congestion_model.pkl", "deployment_model.pkl", "response_time_model.pkl"]
    
    for f in expected:
        path = os.path.join(artifact_dir, f)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"[OK] Found {f} (Size: {size} bytes)")
        else:
            print(f"[FAIL] Missing {f}")
            sys.exit(1)
            
    # Mock payload simulation
    sample_event = {
        "start_time": "2026-06-17T08:30:00Z",
        "severity": "High"
    }
    
    df = pd.DataFrame([sample_event])
    features = generate_time_features(df)
    
    print(f"[OK] Extracted {len(features.columns)} features.")
    
    # Simulate inference step
    gori_engine = GoriEngine()
    gori_res = gori_engine.calculate_gori(
        congestion_score=85.0,
        clearance_mins=45.0,
        deployment_class="Heavy",
        is_rush_hour=True,
        is_closed=False
    )
    
    print(f"[OK] GORI Engine executed. Score: {gori_res['gori_score']}, Tier: {gori_res['severity_tier']}")
    print("Validation Successful")

if __name__ == "__main__":
    validate_artifacts()
