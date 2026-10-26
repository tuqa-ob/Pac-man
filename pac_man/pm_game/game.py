import random

from .adapter import MazeAdapter
from .config import Config
from .ghost import Ghost, GhostState
from .level import Level
from .player import Player


class Game:
    """The state of one game: score, lives, level, player and ghosts."""

    def __init__(self, config: Config) -> None:
        """Create a new game at level 1.

        The maze, the player and the ghosts are created by load_level().

        Args:
            config: the game settings.
        """
        self._seed_rng = random.Random()
        self._config = config
        self.current_level = 1
        self.score = 0
        self.lives: int = config.get("lives")
        self.maze: MazeAdapter
        self.level: Level
        self.player: Player
        self.ghosts: list[Ghost] = []
        self.pac_gum_num = self._config.get("pacgum")
        self.game_won = False
        self.game_over = False
        self.player_name = ""
        self.entering_name = False
        self.cheat_mode = False
        self.invincible = False
        self.ghosts_frozen = False
        self.speed_boost = False

    def load_level(self) -> None:
        """Build the maze, player, pacgums and ghosts of the current level."""
        levels = self._config.get("level")
        lev_width = levels[self.current_level - 1]["width"]
        lev_height = levels[self.current_level - 1]["height"]
        self.player = Player(lev_width, lev_height)
        if self.current_level == 1:
            seed = self._config.get("seed")
        else:
            seed = self._seed_rng.randint(1, 1_000_000)
        maze_adapter = MazeAdapter(lev_width, lev_height, seed)
        maze_adapter.generate()
        self.maze = maze_adapter
        self.level = Level(self.maze, lev_width, lev_height)
        self.level.get_pacgum_cells(
            self.player.curr_row,
            self.player.curr_col,
            self.pac_gum_num,
        )
        ghost_settings = [
            ("red", True),
            ("pink", False),
            ("blue", False),
            ("orange", False),
        ]
        self.ghosts = []
        for (r, c), (color, chases) in zip(
            self.level.ghost_spawns,
            ghost_settings,
        ):
            self.ghosts.append(Ghost(r, c, chases=chases, color=color))

    def move_player(self) -> None:
        """Move the player one step and eat what is on the new cell."""
        if self.player.dir is None:
            return
        if self.level.can_move(
            self.player.curr_row,
            self.player.curr_col,
            self.player.dir,
        ):
            self.player.move()
        if self.level.eat_pacgum(
            self.player.curr_row,
            self.player.curr_col,
        ):
            self.score += self._config.get("points_per_pacgum")
        if self.level.eat_super_pacgum(
            self.player.curr_row,
            self.player.curr_col,
        ):
            self.score += self._config.get("points_per_super_pacgum")
            for ghost in self.ghosts:
                ghost.become_edible()

    def check_collisions(self) -> None:
        """Handle the player touching ghosts.

        A normal ghost costs a life, and an edible ghost gives points.
        With the invincible cheat, a normal ghost does nothing.
        """
        if self.game_over or self.game_won:
            return

        for ghost in self.ghosts:
            if (
                ghost.current_row == self.player.curr_row
                and ghost.current_col == self.player.curr_col
            ):
                if ghost.state == GhostState.CHASE:
                    if self.invincible:
                        continue
                    self.lives -= 1

                    if self.lives <= 0:
                        self.lives = 0
                        self.game_over = True
                        return

                    self.player = Player(
                        self.level.width, self.level.height
                    )
                    for ghost in self.ghosts:
                        ghost.reset_position()
                    break
                elif ghost.state == GhostState.EDIBLE:
                    self.score += self._config.get("points_per_ghost")
                    ghost.get_eaten()
                elif ghost.state == GhostState.EATEN:
                    continue

    def advance_level_if_cleared(self) -> bool:
        """Advance to the next level if the current one is cleared.

        Returns:
            True if a new level was loaded, otherwise False.
        """
        if not self.level.is_cleared():
            return False

        levels = self._config.get("level")

        if self.current_level >= len(levels):
            self.game_won = True
            return False

        self.current_level += 1
        self.lives = self._config.get("lives")
        self.load_level()
        return True

    def skip_level(self) -> None:
        """Cheat: clear the current level at once and go to the next."""
        self.level.pacgum_positions.clear()
        self.level.super_pacgum_positions.clear()
        self.advance_level_if_cleared()

    def toggle_cheat_mode(self) -> None:
        """Turn the cheat mode on or off; turning it off resets the cheats."""
        self.cheat_mode = not self.cheat_mode
        if not self.cheat_mode:
            self.invincible = False
            self.ghosts_frozen = False
            self.speed_boost = False

    def cheat_lines(self) -> list[str]:
        """Return the lines of the cheat help box: the keys and their state."""
        def state(active: bool) -> str:
            """Return ON or OFF for a cheat flag."""
            return "ON" if active else "OFF"

        return [
            "CHEAT MODE",
            f"I  invincible: {state(self.invincible)}",
            f"F  freeze ghosts: {state(self.ghosts_frozen)}",
            f"B  speed boost: {state(self.speed_boost)}",
            "E  extra life",
            "L  skip level",
            "C  cheat mode off",
        ]
