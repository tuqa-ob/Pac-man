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
        self.pacgums = set()
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
        self.super_pac_gum = (
                (0, 0),
                (lev_height - 1, 0),
                (0, lev_width - 1),
                (lev_height - 1, lev_width - 1))
        self._get_pacgum_cells()

    def move_player(self) -> None:
        if self.player.dir is None:
            return
        if not self.maze.has_wall(
                self.player.curr_row,
                self.player.curr_col,
                self.player.dir):
            self.player.move()
            if (
                    (self.player.curr_row, self.player.curr_col)
                    in self.pacgums):
                self.pacgums.remove(
                        (self.player.curr_row, self.player.curr_col))
                self.score += self._config.get("points_per_pacgum")

    def _get_pacgum_cells(self) -> None:
        """Collect cells that pacgums will be there ."""
        NORTH = 1
        EAST = 2
        SOUTH = 4
        WEST = 8
        all_gums_shown = False
        candidates = []
        for r in range(self.maze.height):
            if all_gums_shown:
                break
            for c in range(self.maze.width):
                if (
                        (r == self.player.curr_row
                        and c == self.player.curr_col)
                        or (r, c) in self.super_pac_gum):
                    continue
                if not (
                        self.maze.has_wall(r, c, NORTH)
                        and self.maze.has_wall(r, c, EAST)
                        and self.maze.has_wall(r, c, SOUTH)
                        and self.maze.has_wall(r, c, WEST)):
                    candidates.append((r ,c))
            gum_count = min(self.pac_gum_num, len(candidates))
            self.pacgums = set(random.sample(candidates, gum_count))

