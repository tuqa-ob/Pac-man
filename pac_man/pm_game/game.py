from .adapter import MazeAdapter
from .config import Config
from .player import Player
from .level import Level
import random

class Game:
    def __init__(self, config: Config) -> None:
        self._config = config
        self.current_level = 1
        self.score = 0
        self.lives = config.get("lives")
        self.maze = None
        self.player = None
        self.pac_gum_num = self._config.get("pacgum")

    def load_level(self) -> None:
        levels = self._config.get("level")
        lev_width = levels[self.current_level - 1]["width"]
        lev_height = levels[self.current_level - 1]["height"]
        self.player = Player(lev_width, lev_height)
        if self.current_level == 1:
            seed = self._config.get("seed")
        else:
            seed = random.randint(0, 1000)
        maze_adapter = MazeAdapter(lev_width, lev_height, seed)
        maze_adapter.generate()
        self.maze = maze_adapter
        self.level = Level(
                self.maze,
                lev_width,
                lev_height)
        self.level.get_pacgum_cells(
                self.player.curr_row,
                self.player.curr_col,
                self.pac_gum_num)

    def move_player(self) -> None:
        if self.player.dir is None:
            return
        if self.level.can_move(
            self.player.curr_row,
            self.player.curr_col,
            self.player.dir):
            self.player.move()
        if self.level.eat_pacgum(
                self.player.curr_row,
                self.player.curr_col
                ):
            self.score += self._config.get("points_per_pacgum")
        if self.level.eat_super_pacgum(
                self.player.curr_row,
                self.player.curr_col
                ):
            self.score += self._config.get(
                    "points_per_super_pacgum")
