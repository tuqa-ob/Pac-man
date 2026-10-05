import pytest

from pm_game.adapter import MazeAdapter
from pm_game.direction import Direction

from pm_game.level import (
    Level,
    find_nearest_free_cell,
    get_corners,
    get_ghost_spawns,
    get_pacgum_positions,
    get_player_spawn,
    get_super_pacgum_positions,
)


def make_maze(width: int, height: int, seed: int = 42) -> list[list[int]]:
    """Return a real maze built by the adapter."""
    adapter = MazeAdapter(width=width, height=height, seed=seed)
    adapter.generate()
    return adapter.maze


# ---------- find_nearest_free_cell ----------


def test_nearest_free_cell_keeps_a_free_start() -> None:
    """A start cell that is already free is returned unchanged."""
    maze = make_maze(15, 15)

    assert maze[7][7] != 15
    assert find_nearest_free_cell(maze, 15, 15, 7, 7) == (7, 7)


def test_nearest_free_cell_leaves_a_solid_cell() -> None:
    """The 20x20 center is part of the 42 logo, so we step off it."""
    maze = make_maze(20, 20)

    assert maze[10][10] == 15
    assert find_nearest_free_cell(maze, 20, 20, 10, 10) == (11, 10)


def test_nearest_free_cell_raises_when_all_solid() -> None:
    """A maze made only of solid cells has no free cell to find."""
    maze = [[15, 15], [15, 15]]

    with pytest.raises(ValueError):
        find_nearest_free_cell(maze, 2, 2, 0, 0)


# ---------- player spawn ----------


def test_player_spawn_square_maze() -> None:
    """On 20x20 the center is solid, so the spawn moves one cell right."""
    maze = make_maze(20, 20)

    assert get_player_spawn(maze, 20, 20) == (11, 10)


def test_player_spawn_non_square_maze() -> None:
    """15x10 (width != height) catches swapped width/height bugs."""
    maze = make_maze(15, 10)
    x, y = get_player_spawn(maze, 15, 10)

    assert (x, y) == (7, 5)
    assert maze[y][x] != 15


# ---------- corners, ghosts, super-pacgums ----------


def test_corners_non_square_maze() -> None:
    """Corners use width - 1 for x and height - 1 for y."""
    assert get_corners(15, 10) == [(0, 0), (14, 0), (0, 9), (14, 9)]


def test_ghosts_and_super_pacgums_sit_in_the_corners() -> None:
    """Both start on the 4 corner cells."""
    corners = get_corners(15, 10)

    assert get_ghost_spawns(15, 10) == corners
    assert get_super_pacgum_positions(15, 10) == corners


# ---------- pacgum positions ----------


def test_pacgum_positions_are_free_and_not_reserved() -> None:
    """15x15 has 207 free cells, minus 5 reserved = 202 pacgums."""
    maze = make_maze(15, 15)
    reserved = set(get_corners(15, 15)) | {get_player_spawn(maze, 15, 15)}

    pacgums = get_pacgum_positions(maze, 15, 15, reserved)

    assert len(pacgums) == 202
    assert len(set(pacgums)) == len(pacgums)
    assert set(pacgums).isdisjoint(reserved)
    assert all(maze[y][x] != 15 for x, y in pacgums)


def test_pacgum_count_non_square_maze() -> None:
    """15x10 has 132 free cells, minus 5 reserved = 127 pacgums."""
    maze = make_maze(15, 10)
    reserved = set(get_corners(15, 10)) | {get_player_spawn(maze, 15, 10)}

    assert len(get_pacgum_positions(maze, 15, 10, reserved)) == 127


# ---------- Level class ----------


def test_level_layout() -> None:
    """A Level puts everything where the helper functions say."""
    level = Level(make_maze(15, 15), 15, 15)

    assert level.player_spawn == (7, 7)
    assert len(level.ghost_spawns) == 4
    assert len(level.super_pacgum_positions) == 4
    assert len(level.pacgum_positions) == 202


def test_level_eat_pacgum() -> None:
    """Eating returns True once, then False for the same cell."""
    level = Level(make_maze(15, 15), 15, 15)
    cell = min(level.pacgum_positions)

    assert level.eat_pacgum(*cell) is True
    assert len(level.pacgum_positions) == 201
    assert level.eat_pacgum(*cell) is False
    assert level.eat_pacgum(*level.player_spawn) is False
    assert level.eat_pacgum(0, 0) is False


def test_level_eat_super_pacgum() -> None:
    """Corners hold super-pacgums, which are eaten separately."""
    level = Level(make_maze(15, 15), 15, 15)

    assert level.eat_super_pacgum(0, 0) is True
    assert level.eat_super_pacgum(0, 0) is False
    assert len(level.super_pacgum_positions) == 3


def test_level_is_cleared_needs_everything_eaten() -> None:
    """The level is cleared only when pacgums AND super-pacgums are gone."""
    level = Level(make_maze(15, 15), 15, 15)
    assert level.is_cleared() is False

    for x, y in list(level.pacgum_positions):
        level.eat_pacgum(x, y)
    assert level.is_cleared() is False

    for x, y in list(level.super_pacgum_positions):
        level.eat_super_pacgum(x, y)
    assert level.is_cleared() is True


# ---------- Level.can_move ----------


def test_can_move_is_blocked_by_borders() -> None:
    """The outer border is walled, so nobody can leave the maze."""
    level = Level(make_maze(15, 10), 15, 10)

    assert level.can_move(0, 0, Direction.UP) is False
    assert level.can_move(0, 0, Direction.LEFT) is False
    assert level.can_move(14, 9, Direction.DOWN) is False
    assert level.can_move(14, 9, Direction.RIGHT) is False


def test_can_move_is_blocked_by_the_logo() -> None:
    """Spawn (11, 10) on 20x20 has the solid logo cell on its left."""
    level = Level(make_maze(20, 20), 20, 20)

    assert level.player_spawn == (11, 10)
    assert level.can_move(11, 10, Direction.LEFT) is False
    assert level.can_move(11, 10, Direction.RIGHT) is True


def test_every_free_cell_is_reachable_from_the_spawn() -> None:
    """Walking with can_move must reach all 132 free cells of 15x10."""
    level = Level(make_maze(15, 10), 15, 10)
    seen = {level.player_spawn}
    todo = [level.player_spawn]

    while todo:
        x, y = todo.pop()
        for direction in Direction:
            dx, dy = direction.value
            step = (x + dx, y + dy)
            if step not in seen and level.can_move(x, y, direction):
                seen.add(step)
                todo.append(step)

    assert len(seen) == 132
