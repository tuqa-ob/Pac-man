from enum import Enum
from random

from pm_game.direction import Direction
from pm_game.level import Level

class GhostState(Enum):
    """What a ghost is currently doing."""

    CHASE = "chase"
    EDIBLE = "edible"
    EATEN = "eaten"


class Ghost:
     def __init__(
        self,
        x: int,
        y: int,
        edible_duration: float = 8.0,
        eaten_duration: float = 5.0,
        seed: int | None = None,
    ) -> None:
        """Create a ghost that starts CHASE-ing from its corner.

        Args:
            x: starting column, its home corner.
            y: starting row, its home corner.
            edible_duration: seconds an EDIBLE state lasts.
            eaten_duration: seconds an EATEN state lasts before respawn.
            seed: seed for this ghost's own random movement.
        """
        self.current_x = x
        self.current_y = y
        self.home_x = x
        self.home_y = y
        self.state = GhostState.CHASE
        self.edible_duration = edible_duration
        self.eaten_duration = eaten_duration
        self.edible_timer = 0.0
        self.eaten_timer = 0.0
        self.random = random.Random(seed)

        def move_randomly(self, level: Level) -> None:
            """Move one step in a random legal directiom'

            Args:
            level: the current level, used to check for walls.
            """

            legal_direction = []
            for direction in Direction:
                if level.can_move(self.current_x, self.current_y, direction):
                    legal_direction.append(direction)
            
            chosen = self.random.choise(legaal_directions)
            dx, dy = chosen.value
            self.current_x += dx
            self.current_y += dy


        def get_first_step_toward(
                maze: list[list[int, int]], width: int,
                height: int, start_x: int, start_y: int,
                target_x: int, target_y: int
                ) -> tuple[int, int]:

            """Return the cell to move into first, on the shortest path to the target.

            Args:
                maze: the maze grid, indexed as maze[row][col] i.e. maze[y][x].
                width: number of columns.
                height: number of rows.
                start_x: the ghost's current column.
                start_y: the ghost's current row.
                target_x: the player's current column.
                target_y: the player's current row.

            Returns:
                The (x, y) of the next cell to step into. If start and target
                are the same cell, returns (start_x, start_y) unchanged.
            """

            if (start_x, start_y) == (target_x, target_y):
                return (start_x, start_y)

            visited = {(start_x, start_y)}
            queue = deque([(start_x, start_y)])





