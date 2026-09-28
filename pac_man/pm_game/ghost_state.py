from enum import Enum

class GhostState(Enum):
    """What a ghost is currently doing."""

    CHASE = "chase"
    EDIBLE = "edible"
    EATEN = "eaten"
