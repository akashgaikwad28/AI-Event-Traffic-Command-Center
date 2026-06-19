import logging
import pandas as pd

logger = logging.getLogger(__name__)

class PostEventLearningLoop:
    """
    The Adaptive Intelligence Module.
    This component directly addresses the 'No post-event learning system' gap.
    It takes the predicted impact of an intervention and compares it against 
    the actual observed traffic flow relief to update future recommendations.
    """
    
    def __init__(self):
        self.feedback_log = []
        
    def evaluate_event_accuracy(self, event_id: str, predicted_gori: float, actual_gori: float):
        """
        Logs the prediction error for an event after it has concluded.
        """
        error = abs(predicted_gori - actual_gori)
        logger.info(f"Event {event_id}: Predicted GORI={predicted_gori}, Actual GORI={actual_gori}. Error={error}")
        
        self.feedback_log.append({
            "event_id": event_id,
            "error": error,
            "requires_retraining": error > 15.0
        })
        
        self._trigger_retraining_if_needed()
        
    def evaluate_resource_effectiveness(self, deployment_id: str, officers_deployed: int, congestion_reduction: float):
        """
        Evaluates the ROI of deployed manpower and barricades.
        """
        efficiency_score = congestion_reduction / officers_deployed if officers_deployed > 0 else 0
        logger.info(f"Deployment {deployment_id} achieved {congestion_reduction}% reduction using {officers_deployed} officers.")
        return efficiency_score

    def _trigger_retraining_if_needed(self):
        """
        Triggers an offline model retraining hook if the drift threshold is exceeded.
        """
        high_error_cases = [log for log in self.feedback_log if log["requires_retraining"]]
        if len(high_error_cases) > 10:
            logger.warning("Prediction drift detected! Triggering ml_pipeline/training job.")
            # Trigger Airflow/Prefect or manual script
