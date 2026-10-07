from .direction import Direction


class Player:
    def __init__(self, width: int, height: int) -> None:
        if width % 2 == 0:
            self.curr_col = width // 2 - 1
        else:
            self.curr_col = width // 2
        if height % 2 == 0:
            self.curr_row = height // 2 - 1
        else:
            self.curr_row = height // 2
        self.dir = None

    def move(self) -> None:
        drow, dcol = self.dir.value
        self.curr_row += drow
        self.curr_col += dcol
