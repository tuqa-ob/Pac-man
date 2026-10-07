from collections import deque
from enum import Enum
import random

from pm_game.direction import Direction
from pm_game.level import Level


class GhostState(Enum):
    """What a ghost is currently doing."""

    CHASE = "chase"
    EDIBLE = "edible"
    EATEN = "eaten"


def get_first_step_toward(
        level: Level,
        start_row: int,
        start_col: int,
        target_row: int,
        target_col: int
        ) -> tuple[int, int]:
    """Return the cell to step into first, on the shortest path to a target.

    Uses a breadth-first search from (start_row, start_col). The search
    only needs to know the *first* step of the shortest path, so it
    stops as soon as the target is found and walks the discovery
    trail back to the one cell next to the start.

    Args:
        level: the current level, used to check for walls.
        start_row: the searching character's current row.
        start_col: the searching character's current column.
        target_row: the target's current row.
        target_col: the target's current column.

    Returns:
        The (row, col) of the next cell to step into. If start and target
        are already the same cell, returns (start_row, start_col). If the
        target cannot be reached at all, also returns (start_row, start_col)
        (stay put) -- this should not happen in a fully connected maze.
    """
    if (start_row, start_col) == (target_row, target_col):
        return (start_row, start_col)

    visited = {(start_row, start_col)}
    queue = deque([(start_row, start_col)])
    # prev[cell] = the cell that discovered it first (never set for the
    # start cell itself -- that absence is how we know when to stop
    # walking backward later).
    prev: dict[tuple[int, int], tuple[int, int]] = {}

    while queue:
        crow, ccol = queue.popleft()

        for direction in Direction:
            if not level.can_move(crow, ccol, direction):
                continue

            drow, dcol = direction.value
            nrow, ncol = crow + drow, ccol + dcol

            if (nrow, ncol) in visited:
                continue

            visited.add((nrow, ncol))
            prev[(nrow, ncol)] = (crow, ccol)

            if (nrow, ncol) == (target_row, target_col):
                # Found it. Walk the trail backward until the NEXT
                # step back would be the start itself -- the cell
                # we're standing on at that point is the first move.
                current = (nrow, ncol)
                while prev[current] != (start_row, start_col):
                    current = prev[current]
                return current

            queue.append((nrow, ncol))

    return (start_row, start_col)  # target unreachable: stay put


class Ghost:
    """A single ghost: position, state, timers, and how it moves."""

    def __init__(
        self,
        row: int,
        col: int,
        chases: bool = True,
        move_interval: float = 0.2,
        edible_duration: float = 8.0,
        eaten_duration: float = 5.0,
        seed: int | None = None,
    ) -> None:
        """Create a ghost that starts CHASE-ing from its corner.

        Args:
            col: starting column, its home corner.
            row: starting row, its home corner.
            chases: if True, moves toward the player while CHASE-ing.
                If False, wanders randomly instead.
            move_interval: seconds between one step and the next.
            edible_duration: seconds an EDIBLE state lasts.
            eaten_duration: seconds an EATEN state lasts before respawn.
            seed: seed for this ghost's own random movement.
        """
        self.current_row = row
        self.current_col = col
        self.home_row = row
        self.home_col = col
        self.chases = chases
        self.state = GhostState.CHASE
        self.move_interval = move_interval
        self.move_timer = 0.0
        self.edible_duration = edible_duration
        self.eaten_duration = eaten_duration
        self.edible_timer = 0.0
        self.eaten_timer = 0.0
        self.random = random.Random(seed)

    def become_edible(self) -> None:
        """Switch to EDIBLE (e.g. the player just ate a super-pacgum)."""
        if self.state != GhostState.EATEN:
            self.state = GhostState.EDIBLE
            self.edible_timer = self.edible_duration

    def get_eaten(self) -> None:
        """Switch to EATEN (e.g. the player just touched this ghost)."""
        self.state = GhostState.EATEN
        self.eaten_timer = self.eaten_duration

    def update(
        self, dt: float, level: Level, player_row: int, player_col: int
    ) -> None:
        """Advance this ghost by dt seconds: timers, state, movement.

        Args:
            dt: seconds elapsed since the last call.
            level: the current level, used to check for walls.
            player_row: the player's current row.
            player_col: the player's current column.
        """
        if self.state == GhostState.EATEN:
            self.eaten_timer -= dt
            if self.eaten_timer <= 0:
                self.current_row = self.home_row
                self.current_col = self.home_col
                self.state = GhostState.CHASE
            return

        if self.state == GhostState.EDIBLE:
            self.edible_timer -= dt
            if self.edible_timer <= 0:
                self.state = GhostState.CHASE

        self.move_timer += dt
        if self.move_timer < self.move_interval:
            return
        self.move_timer = 0.0

        if self.state == GhostState.EDIBLE:
            self._move_away_from(level, player_row, player_col)
        elif self.chases:
            self._move_toward(level, player_row, player_col)
        else:
            self.move_randomly(level)

    def move_randomly(self, level: Level) -> None:
        """Move one step in a random legal direction.

        Args:
            level: the current level, used to check for walls.
        """
        legal_directions = []
        for direction in Direction:
            if level.can_move(self.current_row, self.current_col, direction):
                legal_directions.append(direction)

        chosen = self.random.choice(legal_directions)
        drow, dcol = chosen.value
        self.current_row += drow
        self.current_col += dcol

    def _move_toward(
        self, level: Level, target_row: int, target_col: int
    ) -> None:
        """Take one step along the shortest path toward a target."""
        next_row, next_col = get_first_step_toward(
            level, self.current_row, self.current_col, target_row, target_col
        )
        self.current_row = next_row
        self.current_col = next_col

    def _move_away_from(
        self, level: Level, target_row: int, target_col: int
    ) -> None:
        """Step into whichever legal neighbour is farthest from target."""
        best_direction = None
        best_distance = -1

        for direction in Direction:
            if not level.can_move(self.current_row, self.current_col, direction):
                continue
            drow, dcol = direction.value
            nrow, ncol = self.current_row + drow, self.current_col + dcol
            distance = abs(nrow - target_row) + abs(ncol - target_col)
            if distance > best_distance:
                best_distance = distance
                best_direction = direction

        if best_direction is not None:
            drow, dcol = best_direction.value
            self.current_row += drow
            self.current_col += dcol
