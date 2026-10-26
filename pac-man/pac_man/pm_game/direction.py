from enum import Enum


class Direction(Enum):
    """The four ways a character can move, as (drow, dcol) per step.

    row grows downward: row 0 is the top of the maze.
    """

    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)
