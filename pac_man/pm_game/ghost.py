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
    level: Level, start_x: int, start_y: int, target_x: int, target_y: int
) -> tuple[int, int]:
    """Return the cell to step into first, on the shortest path to a target.

    Uses a breadth-first search from (start_x, start_y). The search
    only needs to know the *first* step of the shortest path, so it
    stops as soon as the target is found and walks the discovery
    trail back to the one cell next to the start.

    Args:
        level: the current level, used to check for walls.
        start_x: the searching character's current column.
        start_y: the searching character's current row.
        target_x: the target's current column.
        target_y: the target's current row.

    Returns:
        The (x, y) of the next cell to step into. If start and target
        are already the same cell, returns (start_x, start_y). If the
        target cannot be reached at all, also returns (start_x, start_y)
        (stay put) -- this should not happen in a fully connected maze.
    """
    if (start_x, start_y) == (target_x, target_y):
        return (start_x, start_y)

    visited = {(start_x, start_y)}
    queue = deque([(start_x, start_y)])
    # prev[cell] = the cell that discovered it first (never set for the
    # start cell itself -- that absence is how we know when to stop
    # walking backward later).
    prev: dict[tuple[int, int], tuple[int, int]] = {}

    while queue:
        cx, cy = queue.popleft()

        for direction in Direction:
            if not level.can_move(cx, cy, direction):
                continue

            dx, dy = direction.value
            nx, ny = cx + dx, cy + dy

            if (nx, ny) in visited:
                continue

            visited.add((nx, ny))
            prev[(nx, ny)] = (cx, cy)

            if (nx, ny) == (target_x, target_y):
                # Found it. Walk the trail backward until the NEXT
                # step back would be the start itself -- the cell
                # we're standing on at that point is the first move.
                current = (nx, ny)
                while prev[current] != (start_x, start_y):
                    current = prev[current]
                return current

            queue.append((nx, ny))

    return (start_x, start_y)  # target unreachable: stay put


class Ghost:
    """A single ghost: position, state, timers, and how it moves."""

    def __init__(
        self,
        x: int,
        y: int,
        chases: bool = True,
        move_interval: float = 0.2,
        edible_duration: float = 8.0,
        eaten_duration: float = 5.0,
        seed: int | None = None,
    ) -> None:
        """Create a ghost that starts CHASE-ing from its corner.

        Args:
            x: starting column, its home corner.
            y: starting row, its home corner.
            chases: if True, moves toward the player while CHASE-ing.
                If False, wanders randomly instead.
            move_interval: seconds between one step and the next.
            edible_duration: seconds an EDIBLE state lasts.
            eaten_duration: seconds an EATEN state lasts before respawn.
            seed: seed for this ghost's own random movement.
        """
        self.current_x = x
        self.current_y = y
        self.home_x = x
        self.home_y = y
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
        self, dt: float, level: Level, player_x: int, player_y: int
    ) -> None:
        """Advance this ghost by dt seconds: timers, state, movement.

        Args:
            dt: seconds elapsed since the last call.
            level: the current level, used to check for walls.
            player_x: the player's current column.
            player_y: the player's current row.
        """
        if self.state == GhostState.EATEN:
            self.eaten_timer -= dt
            if self.eaten_timer <= 0:
                self.current_x = self.home_x
                self.current_y = self.home_y
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
            self._move_away_from(level, player_x, player_y)
        elif self.chases:
            self._move_toward(level, player_x, player_y)
        else:
            self.move_randomly(level)

    def move_randomly(self, level: Level) -> None:
        """Move one step in a random legal direction.

        Args:
            level: the current level, used to check for walls.
        """
        legal_directions = []
        for direction in Direction:
            if level.can_move(self.current_x, self.current_y, direction):
                legal_directions.append(direction)

        chosen = self.random.choice(legal_directions)
        dx, dy = chosen.value
        self.current_x += dx
        self.current_y += dy

    def _move_toward(
        self, level: Level, target_x: int, target_y: int
    ) -> None:
        """Take one step along the shortest path toward a target."""
        next_x, next_y = get_first_step_toward(
            level, self.current_x, self.current_y, target_x, target_y
        )
        self.current_x = next_x
        self.current_y = next_y

    def _move_away_from(
        self, level: Level, target_x: int, target_y: int
    ) -> None:
        """Step into whichever legal neighbour is farthest from target."""
        best_direction = None
        best_distance = -1

        for direction in Direction:
            if not level.can_move(self.current_x, self.current_y, direction):
                continue
            dx, dy = direction.value
            nx, ny = self.current_x + dx, self.current_y + dy
            distance = abs(nx - target_x) + abs(ny - target_y)
            if distance > best_distance:
                best_distance = distance
                best_direction = direction

        if best_direction is not None:
            dx, dy = best_direction.value
            self.current_x += dx
            self.current_y += dy
