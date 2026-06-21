# Model Evaluation Strategy

## Current Evaluation Framework
As of the current implementation, explicit evaluation code (e.g., scoring scripts, test sets) for specific models (like XGBoost or Random Forest) is **not present** in the repository. The codebase focuses primarily on production inference via `CongestionModel` and model promotion via `RegistryManager`.

## Model Promotion
The MLops pipeline handles model versioning and environment promotion (e.g., from Staging to Production) via the `RegistryManager` in `mlops/model_registry/registry_manager.py`. The `promote_model` function accepts an arbitrary dictionary of metrics alongside the model version and feature lists.

```python
def promote_model(self, version: str, stage: str, features: list, metrics: dict):
    # Registers a model version and its metrics to a stage.
    ...
```

## Future Evaluation Implementation
When explicit training pipelines are introduced, the evaluation module should output metrics that interface with `RegistryManager.promote_model`. Typical metrics for regression or risk prediction models to include would be:
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R-squared (R2)

These metrics would dictate whether a newly trained `.pkl` artifact is promoted to replace `congestion_model.pkl`.
