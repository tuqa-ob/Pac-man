from enum import Enum


class Direction(Enum):
    """The four ways a character can move, as (dx, dy) per step.

    y grows downward: row 0 is the top of the maze.
    """

    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)
