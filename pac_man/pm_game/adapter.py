from mazegenerator import MazeGenerator

class MazeAdabter:
    """Adapt the external maze generator for the Pac-Man game."""

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    def __init__(self, width: int, height: int, seed: int) -> None:
        """Initialize the maze adapter."""
        self.width = width
        self.height = height = height
        self.seed = seed
        self._maze: list[list[int]] = []

    def generate(self) -> None:
        """Generate a new maze."""
        
        generator = MazeGenerator(
                size=(self.width, self.height),
                entry_cell=(0, 0),
                exit_cell=(self.width - 1, self.height - 1),
                perfect=False,
                seed=self.seed,
                )
        self._maze = generator.maze

    @property
    def maze(self) -> list[list[int]]:
        """Return the generated maze."""

        return self._maze

    def has_wall(self, row: int, column: int, direction: int) -> bool:
        """Return True if a cell has a wall in the given direction."""

        cell = self._maze[row][column]
        return bool(cell & direction)

