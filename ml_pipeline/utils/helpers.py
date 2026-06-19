import logging
import random

import numpy as np


def set_seed(seed: int = 42):
    """
    Enforces reproducibility across the ML pipeline.
    """
    random.seed(seed)
    np.random.seed(seed)
    logging.info(f"Random seed set to {seed}")
