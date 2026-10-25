from .direction import Direction


class Player:
    """The player (Pac-Man): its cell and the direction it faces."""

    def __init__(self, width: int, height: int) -> None:
        """Place the player in the middle of the maze.

        Args:
            width: number of columns of the maze.
            height: number of rows of the maze.
        """
        if width % 2 == 0:
            self.curr_col = width // 2 - 1
        else:
            self.curr_col = width // 2
        if height % 2 == 0:
            self.curr_row = height // 2 - 1
        else:
            self.curr_row = height // 2
        self.dir: Direction | None = None

    def move(self) -> None:
        """Move the player one cell in the direction it faces."""
        if self.dir is None:
            return
        drow, dcol = self.dir.value
        self.curr_row += drow
        self.curr_col += dcol
