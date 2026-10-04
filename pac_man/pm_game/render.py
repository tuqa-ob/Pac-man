import pygame
from pm_game.adapter import MazeAdapter
from pm_game.player import Player


class Renderer:
    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8
    
    def __init__(self, screen: pygame.Surface, maze: MazeAdapter) -> None:
        self._screen = screen
        self._maze = maze
        self._cell_width = self._screen.get_width() // self._maze.width
        self._cell_height = self._screen.get_height() // self._maze.height
        self.cell_size = min(self._cell_width, self._cell_height)

    def calculate_pos(self) -> tuple[int, int]:
        cell = self.cell_size
        maze_width = self._maze.width * cell
        maze_height = self._maze.height * cell
        offset_x = (self._screen.get_width() - maze_width) // 2
        offset_y = (self._screen.get_height() - maze_height) // 2
        return (offset_x, offset_y)

    def draw_maze(self) -> None:
        cell = self.cell_size
        offset_x, offset_y = self.calculate_pos()
        maze_width = self._maze.width * cell
        maze_height = self._maze.height * cell
        maze_right = offset_x + maze_width - 1
        maze_bottom = offset_y + maze_height - 1
        for r in range(self._maze.height):
            for c in range(self._maze.width):
                if self._maze.has_wall(r, c, self.NORTH):
                    pygame.draw.line(
                        self._screen,
                        (255, 255, 255),
                        (offset_x + c * cell, offset_y + r * cell),
                        (offset_x + (c + 1 ) * cell, offset_y + r * cell))
                if self._maze.has_wall(r, c, self.EAST):
                    x = maze_right if c == self._maze.width - 1 else offset_x + (c + 1) * cell
                    pygame.draw.line(
                            self._screen,
                            (255, 255, 255),
                            (x, offset_y + r * cell),
                            (x, offset_y + (r + 1) * cell))
                if self._maze.has_wall(r, c, self.SOUTH):
                    y = maze_bottom if r == self._maze.height - 1 else offset_y + (r + 1) * cell
                    pygame.draw.line(
                            self._screen,
                            (255, 255, 255),
                            (offset_x + c * cell, y),
                            (offset_x + (c + 1) * cell, y))
                if self._maze.has_wall(r, c, self.WEST):
                    pygame.draw.line(
                            self._screen,
                            (255, 255, 255),
                            (offset_x + c * cell, offset_y + r * cell),
                            (offset_x + c * cell, offset_y + (r + 1) * cell))

    def draw_player(self, player: Player) -> None:
        cell = self.cell_size
        offset_x, offset_y = self.calculate_pos()
        x = offset_x + (player.curr_col + 0.5) * cell
        y = offset_y + (player.curr_row + 0.5) * cell
        pygame.draw.circle(
                self._screen,
                (255, 255, 0),
                (x, y),
                (cell // 3))

    def update_screen(self, screen: pygame.Surface) -> None:
        self._screen = screen
        self._cell_width = self._screen.get_width() // self._maze.width
        self._cell_height = self._screen.get_height() // self._maze.height
        self.cell_size = min(self._cell_width, self._cell_height)

    def draw_pac_gum(self, pacgums: set[tuple[int, int]]) -> None:
        offset_x, offset_y = self.calculate_pos()
        cell = self.cell_size
        for r, c in pacgums:
            x = offset_x + (c + 0.5) * cell
            y = offset_y + (r + 0.5) * cell
            pygame.draw.circle(
                    self._screen,
                    (255, 255, 255),
                    (x, y),
                    (cell // 10))

    def draw_hud(self, score: int, lives: int, level: int) -> None:
        self.font = pygame.font.Font(None, 30)
        score_text = self.font.render(
                f"Score : {score}",
                True,
                (255, 255, 255))
        lives_text = self.font.render(
                f"Lives : {lives}",
                True,
                (255, 255, 255))
        level_text = self.font.render(
                f"Level : {level}",
                True,
                (255, 255, 255))


        
