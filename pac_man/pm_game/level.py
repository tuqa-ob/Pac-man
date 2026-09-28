from collections import deque


def find_nearest_free_cell(
    maze: list[list[int]], width: int, height: int, x: int, y: int
) -> tuple[int, int]:
    """Return the coordinates of the free cell nearest to (x, y).

    A cell is "solid" when its value is 15 (walls on all 4 sides).
    If (x, y) itself is already free, it is returned unchanged.

    Args:
        maze: the maze grid, indexed as maze[row][col] i.e. maze[y][x].
        width: number of columns.
        height: number of rows.
        x: starting column.
        y: starting row.

    Returns:
        The (x, y) coordinates of the nearest free cell.

    Raises:
        ValueError: if no free cell is reachable from (x, y).
    """
    if maze[y][x] != 15:
        return (x, y)

    visited = {(x, y)}
    queue = deque([(x, y)])
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    while queue:
        cx, cy = queue.popleft()

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy

            if not (0 <= nx < width and 0 <= ny < height):
                continue

            if (nx, ny) in visited:
                continue

            visited.add((nx, ny))

            if maze[ny][nx] != 15:
                return (nx, ny)

            queue.append((nx, ny))

    raise ValueError("No free cell found in the maze")


def get_player_spawn(
        maze: list[list[int]], width: int, height: int
        ) -> tuple[int, int]:
    """Return the player's spawn point, at or near the center of the maze."""
    return find_nearest_free_cell(
        maze, width, height, width // 2, height // 2
    )


def get_corners(width: int, height: int) -> list[tuple[int, int]]:
    """Return the 4 corner coordinates of a width x height grid.

    Args:
        width: number of columns.
        height: number of rows.

    Returns:
        A list of 4 (x, y) coordinates: top-left, top-right,
        bottom-left, bottom-right.
    """
    corners = []
    corners.append((0, 0))
    corners.append((width - 1, 0))
    corners.append((0, height - 1))
    corners.append((width - 1, height - 1))

    return corners


def get_ghost_spawns(width: int, height: int) -> list[tuple[int, int]]:
    """Return the 4 ghost starting positions, one per corner.

    Args:
        width: number of columns.
        height: number of rows.

    Returns:
        A list of 4 (x, y) ghost spawn coordinates.
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
        A list of 4 (x, y) super-pacgum coordinates.
    """
    return get_corners(width, height)


def get_pacgum_positions(
        maze: list[list[int]], width: int, height: int,
        reserved: set[tuple[int, int]]
        ) -> list[tuple[int, int]]:
    """Return every free cell that isn't reserved for something else.

    Args:
        maze: the maze grid, indexed as maze[row][col] i.e. maze[y][x].
        width: number of columns.
        height: number of rows.
        reserved: coordinates that must NOT get a pacgum (e.g. corners,
            the player spawn point).

    Returns:
        A list of (x, y) coordinates where a pacgum should be placed.
    """
    free = []
    for y in range(height):
        for x in range(width):
            if maze[y][x] != 15:
                if (x, y) not in reserved:
                    free.append((x, y))

    return free


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

        self.player_spawn = get_player_spawn(maze, width, height)
        self.ghost_spawns = get_ghost_spawns(width, height)
        self.super_pacgum_positions = set(
            get_super_pacgum_positions(width, height)
        )

        # Cells that must not contain a normal pacgum.
        reserved = set(self.ghost_spawns)
        reserved.add(self.player_spawn)
        reserved.update(self.super_pacgum_positions)

        self.pacgum_positions = set(
            get_pacgum_positions(maze, width, height, reserved)
        )

    def eat_pacgum(self, x: int, y: int) -> bool:
        """Remove the normal pacgum at (x, y), if there is one.

        Args:
            x: column of the cell.
            y: row of the cell.

        Returns:
            True if a pacgum was eaten, False if the cell had none.
        """
        if (x, y) in self.pacgum_positions:
            self.pacgum_positions.remove((x, y))
            return True
        return False

    def eat_super_pacgum(self, x: int, y: int) -> bool:
        """Remove the super-pacgum at (x, y), if there is one.

        Args:
            x: column of the cell.
            y: row of the cell.

        Returns:
            True if a super-pacgum was eaten, False if the cell had none.
        """
        if (x, y) in self.super_pacgum_positions:
            self.super_pacgum_positions.remove((x, y))
            return True
        return False

    def is_cleared(self) -> bool:
        """Return True when every pacgum and super-pacgum has been eaten."""
        return not self.pacgum_positions and not self.super_pacgum_positions
