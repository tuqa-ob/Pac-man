from pm_game.ghost_state import GhostState
from pm_game.level import Level

class Ghost:
     """Represent one ghost in the Pac-Man game."""

     def__init__(self, level: Level,
                 spawn_postion: tuple[int, int]
                 ) -> None:

