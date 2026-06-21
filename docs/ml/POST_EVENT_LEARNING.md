# Post-Event Learning

## Overview
Post-Event Learning refers to the continuous improvement of the Gridwise AI models and GridWise Operational Risk Index (GORI) engine based on actual historical event resolutions.

## Current Mechanism
There are no active post-event training feedback loops or continuous learning scripts explicitly implemented in `backend/app/ai/` or `mlops/`. The `CongestionModel` acts purely as an inference wrapper and does not perform online learning or automated fine-tuning.

## Strategy for Implementation
To introduce robust post-event learning, the following components must be added:
1. **Data Collection Loop**: Capture predictions made by the `CongestionModel` and `GoriEngine`, and correlate them with ground-truth resolution times and actual operational impacts post-event.
2. **Drift Detection**: Although a `mlops/drift_detection/` directory exists, active code for detecting data or concept drift needs to be implemented to trigger retraining.
3. **Automated Retraining Pipeline**: Build scripts (potentially utilizing XGBoost or Random Forest frameworks) to retrain the `.pkl` artifact on newly acquired event data.
4. **Validation and Promotion**: Retrained models should undergo automated evaluation (as outlined in `MODEL_EVALUATION.md`) before `RegistryManager` promotes them to production.
