from mazegenerator import MazeGenerator


class MazeGenerationError(Exception):
    """Raised when the external maze generator fails to build a maze."""


class MazeAdapter:
    """Adapt the external maze generator for the Pac-Man game."""

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(self, width: int, height: int, seed: int) -> None:
        """Initialize the maze adapter."""
        self.width = width
        self.height = height
        self.seed = seed
        self._maze: list[list[int]] = []

    def generate(self) -> None:
        """Generate a new maze.
       
           Raises:
            MazeGenerationError: if the external generator fails for
                this width, height and seed.

        """
        try:

            generator = MazeGenerator(
                    size=(self.width, self.height),
                    entry_cell=(0, 0),
                    exit_cell=(self.width - 1, self.height - 1),
                    perfect=False,
                    seed=self.seed,
                    )
        except Exception as e:
            raise MazeGenerationError(
                    f"Failed to generate a {self.width}x{self.height} maze "
                    f"(seed={self.seed}): {e}"
            ) from e

        self._maze = generator.maze

    @property
    def maze(self) -> list[list[int]]:
        """Return the generated maze."""

        return self._maze

    def has_wall(self, x: int, y: int, direction: int) -> bool:
        """Return True if a cell has a wall in the given direction.

        Args:
            x: column of the cell.
            y: row of the cell.
            direction: NORTH, EAST, SOUTH or WEST.

        Returns:
            True if the cell has a wall on that side.
        """
        cell = self._maze[y][x]
        return bool(cell & direction)
