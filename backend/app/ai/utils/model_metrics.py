from dataclasses import dataclass, field


@dataclass
class ModelMetrics:
    """Lightweight container for production model performance tracking."""

    model_name: str
    rmse: float = 0.0
    mae: float = 0.0
    r2: float = 0.0
    accuracy: float = 0.0
    inference_ms: float = 0.0
    extra: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "model_name": self.model_name,
            "rmse": self.rmse,
            "mae": self.mae,
            "r2": self.r2,
            "accuracy": self.accuracy,
            "inference_ms": self.inference_ms,
            **self.extra,
        }
