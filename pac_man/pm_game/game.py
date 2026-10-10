from .adapter import MazeAdapter
from .config import Config
from .player import Player
from .level import Level
from .ghost import Ghost, GhostState
import random

class Game:
    def __init__(self, config: Config) -> None:
        self._config = config
        self.current_level = 1
        self.score = 0
        self.lives = config.get("lives")
        self.maze = None
        self.player = None
        self.ghosts = []
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
        ghost_settings = [
                {"color": "red", "chases": True},
                {"color": "pink", "chases": False},
                {"color": "blue", "chases": False},
                {"color": "orange", "chases": False}
                ]
        self.ghosts = []
        for (r, c), settings in zip(
                self.level.ghost_spawns,
                ghost_settings
                ):
            ghost = Ghost(
                    r,
                    c,
                    chases=settings["chases"],
                    color=settings["color"])
            self.ghosts.append(ghost)

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
            for ghost in self.ghosts:
                ghost.become_edible()

    def check_collisions(self) -> None:
        for ghost in self.ghosts:
            if (
                ghost.current_row == self.player.curr_row
                and ghost.current_col == self.player.curr_col
            ):
                if ghost.state == GhostState.CHASE:
                    self.lives -= 1
                    self.player = Player(self.level.width, self.level.height)
                    ghost.reset_position()
                    break
                elif ghost.state == GhostState.EDIBLE:
                    self.score += self._config.get("points_per_ghost")
                    ghost.get_eaten()
                elif ghost.state == GhostState.EATEN:
                    continue
