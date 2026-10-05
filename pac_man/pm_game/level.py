import random
from pm_game.adapter import MazeAdapter
from pm_game.direction import Direction


def get_corners(width: int, height: int) -> list[tuple[int, int]]:
    """Return the 4 corner coordinates of a width x height grid.

    Args:
        width: number of columns.
        height: number of rows.

    Returns:
        A list of 4 (row, col) coordinates: top-left,
        bottom-left, top-right, bottom-right.
    """
    corners = []
    corners.append((0, 0))
    corners.append((0, width - 1))
    corners.append((height - 1, 0))
    corners.append((height - 1, width - 1))

    return corners


def get_ghost_spawns(width: int, height: int) -> list[tuple[int, int]]:
    """Return the 4 ghost starting positions, one per corner.

    Args:
        width: number of columns.
        height: number of rows.

    Returns:
        A list of 4 (row, col) ghost spawn coordinates.
    """
    return get_corners(width, height)


def get_super_pacgum_positions(
        width: int, height: int
        ) -> list[tuple[int, int]]:
    """Return the 4 super-pacgum positions, one per corner.

    Args:
        width: number of columns.
        height: number of rows.

    Returns:
        A list of 4 (row, col) super-pacgum coordinates.
    """
    return get_corners(width, height)


class Level:
    """Represent one complete Pac-Man level.

    Attributes:
        maze: the maze grid, indexed as maze[y][x].
        width: number of columns.
        height: number of rows.
        player_spawn: (x, y) where the player starts and respawns.
        ghost_spawns: the 4 (x, y) cells where the ghosts start.
        super_pacgum_positions: (x, y) cells still holding a super-pacgum.
        pacgum_positions: (x, y) cells still holding a normal pacgum.
    """

    def __init__(
        self,
        maze: list[list[int]],
        width: int,
        height: int,
    ) -> None:
        """Create a complete level from a maze.

        Args:
            maze: the maze grid, indexed as maze[y][x].
            width: number of columns.
            height: number of rows.
        """
        self.maze = maze
        self.width = width
        self.height = height
        self.ghost_spawns = get_ghost_spawns(width, height)
        self.super_pacgum_positions = set(
            get_super_pacgum_positions(width, height)
        )
        self.pacgum_positions = set()

    def get_pacgum_cells(
            self,
            player_row: int,
            player_col: int,
            pac_gum_num: int
            ) -> None:

        candidates = []
        for row in range(self.height):
            for col in range(self.width):
                if (
                        (row == player_row and col == player_col)
                        or (row, col) in self.super_pacgum_positions
                ):
                    continue

                if not (
                        self.maze.has_wall(
                            row, col, MazeAdapter.NORTH)
                        and self.maze.has_wall(
                            row, col, MazeAdapter.EAST)
                        and self.maze.has_wall(
                            row, col, MazeAdapter.SOUTH)
                        and self.maze.has_wall(
                            row, col, MazeAdapter.WEST)
                ):
                    candidates.append((row, col))

        gum_count = min(pac_gum_num, len(candidates))
        self.pacgum_positions = set(
                random.sample(candidates, gum_count)
                )

    def eat_pacgum(self, row: int, col: int) -> bool:
        """Remove the normal pacgum at (row, col), if there is one."""
        if (row, col) in self.pacgum_positions:
            self.pacgum_positions.remove((row, col))
            return True
        return False

    def eat_super_pacgum(self, row: int, col: int) -> bool:
        """Remove the super-pacgum at (row, col), if there is one."""
        if (row, col) in self.super_pacgum_positions:
            self.super_pacgum_positions.remove((row, col))
            return True
        return False
    
    def is_cleared(self) -> bool:
        """Return True when every pacgum and super-pacgum has been eaten."""
        return not self.pacgum_positions and not self.super_pacgum_positions

    def can_move(self, row: int, col: int, direction: int) -> bool:
        """Return True if a character at (x, y) can step in a direction.

        Args:
            x: column of the current cell.
            y: row of the current cell.
            direction: the way the character wants to move.

        Returns:
            False if there is a wall on that side or the step would
            leave the maze, True otherwise.
        """
        return not self.maze.has_wall(row, col, direction)
