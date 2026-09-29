class Player:
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    def __init__(self, width: int, height: int) -> None:
        self.curr_row = height // 2
        self.curr_col = width // 2
        self.dir = None

    def move(self) -> None:
        if self.dir == self.NORTH:
            self.curr_row -= 1
        elif self.dir == self.SOUTH:
            self.curr_row += 1
        elif self.dir == self.EAST:
            self.curr_col += 1
        elif self.dir == self.WEST:
            self.curr_col -= 1
