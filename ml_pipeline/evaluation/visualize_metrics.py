import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

logger = logging.getLogger(__name__)


class ModelVisualizer:
    """
    Generates presentation-ready visualizations for ML models including
    Confusion Matrices and Feature Importances.
    """

    def __init__(self, output_dir: str = "reports/figures"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        # Use a clean, professional style
        try:
            plt.style.use("seaborn-v0_8-whitegrid")
        except:
            pass  # Fallback if style not available

    def plot_confusion_matrix(
        self,
        cm: list,
        class_names: list,
        filename: str = "deployment_confusion_matrix.png",
    ):
        """Plots and saves a beautiful confusion matrix."""
        try:
            plt.figure(figsize=(8, 6))
            sns.heatmap(
                cm,
                annot=True,
                fmt="d",
                cmap="Blues",
                xticklabels=class_names,
                yticklabels=class_names,
                cbar_kws={"label": "Number of Incidents"},
            )
            plt.title(
                "Deployment Load Classification - Confusion Matrix", fontsize=14, pad=15
            )
            plt.ylabel("True Deployment Load", fontsize=12, fontweight="bold")
            plt.xlabel("Predicted Deployment Load", fontsize=12, fontweight="bold")
            plt.tight_layout()

            output_path = self.output_dir / filename
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            plt.close()
            logger.info(f"Saved confusion matrix to {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot confusion matrix: {e}")

    def plot_feature_importance(
        self, model, feature_names: list, title: str, filename: str
    ):
        """Extracts and plots feature importances from a tree-based model."""
        try:
            if hasattr(model, "feature_importances_"):
                importances = model.feature_importances_
            else:
                logger.warning(
                    f"Model {type(model)} does not have feature_importances_"
                )
                return

            indices = np.argsort(importances)[::-1]
            sorted_importances = importances[indices]
            sorted_features = [feature_names[i] for i in indices]

            plt.figure(figsize=(10, 6))
            sns.barplot(x=sorted_importances, y=sorted_features, palette="viridis")
            plt.title(title, fontsize=14, pad=15)
            plt.xlabel("Relative Importance", fontsize=12, fontweight="bold")
            plt.ylabel("Features", fontsize=12, fontweight="bold")
            plt.tight_layout()

            output_path = self.output_dir / filename
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            plt.close()
            logger.info(f"Saved feature importance to {output_path}")
        except Exception as e:
            logger.error(f"Failed to plot feature importance: {e}")
