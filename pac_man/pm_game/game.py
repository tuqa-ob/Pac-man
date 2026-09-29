from .adapter import MazeAdapter
from .config import Config
from .player import Player
import random

class Game:
    def __init__(self, config: Config) -> None:
        self._config = config
        self.current_level = 1
        self.score = 0
        self.lives = config.get("lives")
        self.maze = None
        self.player = None

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

    def move_player(self) -> None:
        if self.player.dir is None:
            return
        if not self.maze.has_wall(
                self.player.curr_row,
                self.player.curr_col,
                self.player.dir):
            self.player.move()
